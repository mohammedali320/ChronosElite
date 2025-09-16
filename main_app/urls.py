from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('/category', views.category_index, name='category_index'),
    path('about/', views.about, name='about'),
    path('<int:category_id>/', views.category_detail, name='category-detail'),
    path('category/<int:category_id>/watches/', views.show_watches, name='show_watches'),
    path('watch/<int:watch_id>/', views.watch_detail, name='watch_detail'),
    path('watch/create/', views.WatchCreate.as_view(), name='watch-create'),
    path('watch/<int:pk>/update/', views.WatchUpdate.as_view(), name='watch-update'),
    path('watch/<int:pk>/delete/', views.WatchDelete.as_view(), name='watch-delete'), 
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='category_index'), name='logout'),
]