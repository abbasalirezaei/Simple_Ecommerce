from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib import messages


from products.models import Product

from .forms import CartAddProductForm
from .models import Cart, Order
from .cart import Cartt


@require_POST
def cart_add(request, product_id):
    cart = Cartt(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    cart.add(
        product=product,
        quantity=cd['quantity'],
        override_quantity=cd['override']
    )
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cartt(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cartt(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
    return render(request, 'cart/detail.html', {'cart': cart})
