from django import forms
from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'tags', 'category','description', 'image']