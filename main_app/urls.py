from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='home'),
    path('category/', views.category_index, name='category_index'),
    path('about/', views.about, name='about'),
    path('category/<int:category_id>/watches/', views.show_watches, name='show_watches'),
    path('watch/<int:watch_id>/', views.watch_detail, name='watch_detail'),
    path('watch/create/', views.WatchCreate.as_view(), name='watch-create'),
    path('watch/<int:pk>/update/', views.WatchUpdate.as_view(), name='watch-update'),
    path('watch/<int:pk>/delete/', views.WatchDelete.as_view(), name='watch-delete'), 
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cart/', views.view_cart, name='view_cart'),
    path('watch/<int:watch_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.order_history, name='order-history'),
    
]