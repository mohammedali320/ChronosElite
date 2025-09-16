from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Watch
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginView(LoginView):
    template_name = 'login.html' 


def home(request):
    return render(request, 'login.html')


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
def category_detail(request, category_id):
    cat = Category.objects.get(id=category_id)
    return render(request, 'cats/detail.html', {'cat': cat})


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


# Correct way to protect CBVs with login
class WatchCreate(LoginRequiredMixin, CreateView):
    model = Watch
    fields = ['category', 'name', 'brand', 'price', 'description', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)


class WatchUpdate(LoginRequiredMixin, UpdateView):
    model = Watch
    fields = ['category', 'name', 'brand', 'price', 'description', 'image']


class WatchDelete(LoginRequiredMixin, DeleteView):
    model = Watch
    success_url = '/'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
