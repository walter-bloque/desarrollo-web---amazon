from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from .models import Product, Category
from .forms import ProductForm, UserRegisterForm, UserLoginForm


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
    categories = Category.objects.all()[:5]

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


def add_product(request):
    """Vista para agregar un nuevo producto"""
    print("Accediendo a la vista add_product")  # Depuración
    
    if request.method == 'POST':
        print("Método POST detectado")  # Depuración
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("Formulario válido")  # Depuración
            try:
                product = form.save(commit=False)
                
                # Calcular el precio final basado en el precio original y el descuento
                if product.original_price and product.discount_percentage > 0:
                    # Calcular precio con descuento - convertir a Decimal
                    discount_percentage_decimal = Decimal(str(product.discount_percentage))
                    discount_amount = product.original_price * (discount_percentage_decimal / Decimal('100'))
                    product.price = product.original_price - discount_amount
                elif product.original_price:
                    # Si no hay descuento, el precio es igual al precio original
                    product.price = product.original_price
                    product.discount_percentage = 0
                else:
                    # Si no se proporciona precio original, establecer valores por defecto
                    product.price = Decimal('0')
                    product.discount_percentage = 0
                
                # Establecer rating en 0.0 y reviews_count en 0 para productos nuevos
                product.rating = Decimal('0.0')
                product.reviews_count = 0
                
                # Establecer disponibilidad basada en el stock
                product.available = product.stock > 0
                
                product.save()
                print(f"Producto guardado con ID: {product.id}")  # Depuración
                messages.success(request, _('¡Producto agregado exitosamente!'))
                return redirect('shop:product_detail', slug=product.slug)
            except Exception as e:
                print(f"Error al guardar el producto: {str(e)}")  # Depuración
                messages.error(request, _('Ocurrió un error al guardar el producto. Por favor, inténtalo de nuevo.'))
        else:
            print("Errores en el formulario:", form.errors)  # Depuración
    else:
        print("Mostrando formulario vacío")  # Depuración
        form = ProductForm()
    
    context = {
        'form': form,
        'title': _('Agregar nuevo producto')
    }
    return render(request, 'shop/product_form.html', context)


def register_view(request):
    """Vista para registrar un nuevo usuario"""
    if request.user.is_authenticated:
        return redirect('shop:index')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _(f'¡Cuenta creada exitosamente para {username}! Ya puedes iniciar sesión.'))
            return redirect('shop:login')
        else:
            messages.error(request, _('Por favor corrige los errores en el formulario.'))
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
        'title': _('Crear cuenta')
    }
    return render(request, 'shop/register.html', context)


def login_view(request):
    """Vista para iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('shop:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _(f'¡Bienvenido de nuevo, {username}!'))
                next_url = request.GET.get('next', 'shop:index')
                return redirect(next_url)
        else:
            messages.error(request, _('Usuario o contraseña incorrectos.'))
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'title': _('Iniciar sesión')
    }
    return render(request, 'shop/login.html', context)


@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, _('Has cerrado sesión exitosamente.'))
    return redirect('shop:index')


@login_required
def profile_view(request):
    """Vista del perfil del usuario"""
    context = {
        'title': _('Mi perfil')
    }
    return render(request, 'shop/profile.html', context)
