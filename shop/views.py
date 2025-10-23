from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def index(request):
    """Vista principal que muestra los productos destacados"""
    featured_products = Product.objects.filter(available=True)[:12]
    prime_products = Product.objects.filter(available=True, is_prime=True)[:8]
    discounted_products = Product.objects.filter(available=True, discount_percentage__gt=0)[:8]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'prime_products': prime_products,
        'discounted_products': discounted_products,
        'categories': categories,
    }
    
    return render(request, 'shop/index.html', context)


def product_detail(request, slug):
    """Vista de detalle de un producto individual"""
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Productos relacionados de la misma categoría
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'shop/product_detail.html', context)
