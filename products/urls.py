from django.urls import path
# from cart.views import add_to_cart, remove_from_cart, CartView, decreaseCart
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('products/', views.product_list, name='product-list'),
    path(
        'products/<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category'
    ),
    path('products/<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
   
    # path('cart/', CartView, name='cart-home'),
    # path('cart/<slug>', add_to_cart, name='cart'),
    # path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
    # path('remove/<slug>', remove_from_cart, name='remove-cart'),
]
