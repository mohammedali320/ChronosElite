from django.shortcuts import render
from .models import Category,Watch

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Hello</h1>')

def about(request):
    return render(request, 'about.html')
# Create a list of Category instances
categories = [
    Category(name='Mens', description='Watches for men.'),
    Category(name='Womens', description='Watches for women.'),
    Category(name='Kids', description='Watches for kids.')
]

# Create a list of Watch instances assigned to categories
watches = [
    Watch(category=categories[0], name='ChronoMax', brand='Omega', price=4999.99),
    Watch(category=categories[0], name='Speedster', brand='Rolex', price=12500.50),
    Watch(category=categories[1], name='ElegantTime', brand='Seiko', price=350.00),
    Watch(category=categories[1], name='SilverLine', brand='Fossil', price=150.00),
    Watch(category=categories[2], name='MiniSport', brand='Casio', price=199.99),
    Watch(category=categories[2], name='TinyTime', brand='Timex', price=120.00)
]


from .models import Category  # Make sure you import your models

def category_index(request):
    # Fetch all categories with their watches
    # categories = Category.objects.prefetch_related('watches').all()
    return render(request, 'categories/index.html', {'categories': categories})


def watch_index(request):
    # Fetch all categories with their watches
    # categories = Category.objects.prefetch_related('watches').all()
    return render(request, 'categories/index.html', {'watches': watches})

