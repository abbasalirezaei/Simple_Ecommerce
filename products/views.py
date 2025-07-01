from django.views.generic import ListView
from products.models import Product, Category
from django.shortcuts import get_object_or_404, render
from .filters import ProductFilter
from cart.forms import CartAddProductForm

class Home(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        "products": products,
        "categories": categories,
        "category": category,
    }
    return render(request, 'products/list.html', context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'products/detail.html',
        {'product': product,'cart_product_form': cart_product_form}
    )
