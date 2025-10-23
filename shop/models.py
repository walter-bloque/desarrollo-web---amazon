from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('nombre'), max_length=200)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = _('categoría')
        verbose_name_plural = _('categorías')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('categoría'))
    name = models.CharField(_('nombre'), max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(_('descripción'))
    price = models.DecimalField(_('precio'), max_digits=10, decimal_places=2)
    original_price = models.DecimalField(_('precio original'), max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.IntegerField(_('porcentaje de descuento'), default=0)
    image = models.ImageField(_('imagen'), upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(_('stock'), default=0)
    available = models.BooleanField(_('disponible'), default=True)
    rating = models.DecimalField(_('calificación'), max_digits=3, decimal_places=1, default=0.0)
    reviews_count = models.IntegerField(_('número de reseñas'), default=0)
    is_prime = models.BooleanField(_('Prime'), default=False)
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)
    
    class Meta:
        verbose_name = _('producto')
        verbose_name_plural = _('productos')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name + ' - ' + self.category.name
    
    @property
    def has_discount(self):
        return self.discount_percentage > 0
