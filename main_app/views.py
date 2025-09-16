from django.shortcuts import render,  get_object_or_404
from .models import Category,Watch
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

class CustomLoginView(LoginView):
    template_name = 'login.html' 

# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Hello</h1>')

def about(request):
    return render(request, 'about.html')
# Create a list of Category instances

from .models import Category  # Make sure you import your models

def category_index(request):
    # Fetch all categories with their watches
    categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': categories})


def watch_index(request):
    # Fetch all categories with their watches
    categories = Category.objects.prefetch_related('watches').all()
    return render(request, 'categories/index.html', {'categories': categories})

def category_detail(request, category_id):
    cat = Category.objects.get(id=category_id)
    return render(request, 'cats/detail.html', {'cat': cat})

def show_watches(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    watches = Watch.objects.filter(category=category)
    return render(request, 'categories/show_watches.html', {
        'category': category,
        'watches': watches
    })

def watch_detail(request, watch_id):
    watch = get_object_or_404(Watch, id=watch_id)
    return render(request, 'watch/detail.html', {
        'watch': watch
    })
    
class WatchCreate(CreateView):
    model = Watch
    fields = ['category', 'name', 'brand', 'price', 'description', 'image']

class WatchUpdate(UpdateView):
    model = Watch
    fields = ['category', 'name', 'brand', 'price', 'description', 'image']

class WatchDelete(DeleteView):
    model = Watch
    success_url = '/'
