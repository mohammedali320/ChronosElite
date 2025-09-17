from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Watch, Cart, CartItem, Order, OrderItem
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'login.html' 

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    featured_watches = Watch.objects.all()[:8] 
    return render(request, 'home.html', {'featured_watches': featured_watches})

def about(request):
    return render(request, 'about.html')


@login_required
def category_index(request):
    categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': categories})


@login_required
def watch_index(request):
    categories = Category.objects.prefetch_related('watches').all()
    return render(request, 'categories/index.html', {'categories': categories})


@login_required
def show_watches(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    watches = Watch.objects.filter(category=category)
    return render(request, 'categories/show_watches.html', {
        'category': category,
        'watches': watches
    })


@login_required
def watch_detail(request, watch_id):
    watch = get_object_or_404(Watch, id=watch_id)
    return render(request, 'watch/detail.html', {
        'watch': watch
    })


class WatchCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Watch
    fields = ['category', 'name', 'brand', 'price', 'description', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Only superusers can access this view
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect non-superusers to category page
        from django.shortcuts import redirect
        return redirect('category_index')


class WatchUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Watch
    fields = ['category', 'name', 'brand', 'price', 'description', 'image']

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('category_index')

class WatchDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Watch
    success_url = '/category/'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('category_index')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

@login_required
def view_cart(request):
    # Get the logged-in user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get all items in the cart
    items = cart.items.all()  # <-- here is `cart.items.all()`
    
    total = cart.total_price()
    
    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total': total})

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return self.get_redirect_url() or '/category/'


@login_required
def add_to_cart(request, watch_id):
    watch = get_object_or_404(Watch, id=watch_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created_item = CartItem.objects.get_or_create(cart=cart, watch=watch)
    if not created_item:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{watch.name} has been added to your cart.")
    return redirect('watch_detail', watch_id=watch.id)

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    if not items:
        messages.warning(request, "Your cart is empty!")
        return redirect('view_cart')

    order = Order.objects.create(user=request.user, status='pending')

    total_price = 0

    for item in items:
        OrderItem.objects.create(
            order=order,
            watch=item.watch,
            quantity=item.quantity,
            price=item.watch.price
        )
        total_price += item.watch.price * item.quantity
    order.total_price = total_price
    order.save()
    items.delete()

    messages.success(request, f"Your order #{order.id} has been placed successfully!")
    return render(request, 'checkout.html', {'order': order, 'total': total_price})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def order_history(request):
    # Get all orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Optionally, include order items in context (can be accessed in template via order.items.all())
    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)