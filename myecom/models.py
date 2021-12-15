from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    tags = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/', default='static/img/default.jpg')