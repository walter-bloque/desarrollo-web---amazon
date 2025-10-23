from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
]
