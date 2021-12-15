from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('products/', views.products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/update/<int:product_id>', views.update_product, name='update_product'),
    path('products/delete/<int:product_id>', views.delete_product, name='delete_product'),
]
