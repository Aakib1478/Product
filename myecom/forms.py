from django import forms
from .models import *
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'tags', 'category','description', 'image']

class UserForm(forms.ModelForm):
    class Meta:
    	model = User
    	fields = ['username', 'password']
    
class UserRegistrationForm(forms.ModelForm):
    class Meta:
    	model = User
    	fields = [
    	    	'first_name', 
    		    'last_name',
    		    'username', 
    		    'password', 
    		    'email', 
    	]