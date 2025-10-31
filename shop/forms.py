from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import Product, Category, UserProfile
from django.utils.translation import gettext_lazy as _

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'description', 
            'original_price', 'discount_percentage', 'image', 'stock', 
            'is_prime'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'original_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_prime': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'category': _('Categoría'),
            'name': _('Nombre del producto'),
            'slug': _('URL amigable'),
            'description': _('Descripción'),
            'original_price': _('Precio original (opcional)'),
            'discount_percentage': _('Porcentaje de descuento (0-100)'),
            'image': _('Imagen del producto'),
            'stock': _('Cantidad en inventario'),
            'is_prime': _('Producto Prime'),
        }
        help_texts = {
            'slug': _('URL amigable para el producto (usar guiones en lugar de espacios)'),
            'original_price': _('Solo completar si hay un descuento'),
            'discount_percentage': _('Porcentaje de descuento (0-100)'),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Correo electrónico')})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre')})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Apellido')})
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Número de teléfono (opcional)')})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Dirección (opcional)')})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number', 'address', 'captcha']
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Nombre de usuario')
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Contraseña')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Confirmar contraseña')
        })
    
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Update the UserProfile with phone and address
            profile = user.profile
            profile.phone_number = self.cleaned_data.get('phone_number', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.save()
        
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre de usuario')})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Contraseña')})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
