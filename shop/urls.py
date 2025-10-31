from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.profile_view, name='profile'),
    path('producto/agregar/', login_required(views.add_product), name='add_product'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
]
