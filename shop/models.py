from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    @property
    def rating_rounded(self) -> int:
        if self.rating is None:
            return 0

        value = Decimal(str(self.rating))
        rounded = value.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return max(0, min(5, int(rounded)))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('usuario'))
    phone_number = models.CharField(_('número de teléfono'), max_length=20, blank=True)
    address = models.TextField(_('dirección'), blank=True)
    
    class Meta:
        verbose_name = _('perfil de usuario')
        verbose_name_plural = _('perfiles de usuario')
    
    def __str__(self):
        return f'{self.user.username} - {_("Perfil")}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
