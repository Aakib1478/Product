from django.urls import path, include
from . import views


urlpatterns = [
	path('login/', views.signin, name='signin'),
	path('logout/', views.signout, name='signout'),
	path('signup/', views.signup, name='signup'),
    path('register', views.register, name="register"),
    path(r'^products/$', views.products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/update/<int:product_id>', views.update_product, name='update_product'),
    path('products/delete/<int:product_id>', views.delete_product, name='delete_product'),
]
