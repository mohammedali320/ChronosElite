from django.urls import path
from . import views 

urlpatterns = [
    path('', views.category_index, name='category_index'),
    path('about/', views.about, name='about'),
    path('<int:category_id>/', views.category_detail, name='category-detail'),
    path('category/<int:category_id>/watches/', views.show_watches, name='show_watches'),
]