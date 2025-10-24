from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def index(request):
    """Vista principal que muestra los productos destacados"""
    base_products = Product.objects.filter(available=True, stock__gt=0)
    prioritized_products = base_products.filter(
        Q(is_prime=True) | Q(discount_percentage__gt=0) | Q(rating__gte=4)
    ).order_by('-is_prime', '-discount_percentage', '-rating', '-reviews_count', '-created_at')[:8]

    featured_products = list(prioritized_products)
    if len(featured_products) < 8:
        remaining_slots = 8 - len(featured_products)
        fallback_products = base_products.exclude(
            id__in=[product.id for product in featured_products]
        ).order_by('-created_at')[:remaining_slots]
        featured_products.extend(list(fallback_products))

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
