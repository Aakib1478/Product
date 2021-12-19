from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import *
from .forms import ProductForm, UserForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages


def signin(request):
	if request.method == "POST":
		username = request.POST['username']
		password =  request.POST['password']
		user = authenticate(
				request, 
				username=username, 
				password=password
		)
		if user is None:
			return HttpResponse("Invalid credentials.")
		login(request, user)
		return redirect('products')
	else:
		form = UserForm()
		return render(request, 'registration/login.html', {'form':form})
			
def signout(request):
	logout(request)
	return redirect('signin')
			
def signup(request):
	form = UserRegistrationForm()
	if request.method=="POST":
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		newuser = User.objects.create_user(
			first_name=first_name, 
			last_name=last_name,
			username=username,
			password=password,
			email=email
		)
		newuser.save()
	else:
		form = UserRegistrationForm()
	return render(request, 'registration/signup.html', {'form':form})  

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('login')
	else:
		form = UserCreationForm()

	return render(request, 'registration/signup.html',
	{'form': form,
	})

def products(request):
	products = Product.objects.all()
	return render(request, 'myecom/home.html', {'products':products})

def add_product(request):
	product = ProductForm()
	if request.method == 'POST':
		product = ProductForm(request.POST, request.FILES)
		if product.is_valid():
			product.save()
			return redirect('products')
	return render(request, 'myecom/add_product.html', {'product_form':product})

def update_product(request, product_id):
	product_id = int(product_id)
	try:
		products = Product.objects.get(id = product_id)
	except Product.DoesNotExist:
		return redirect('products')
	product_form = ProductForm(request.POST or None, instance = products)
	if product_form.is_valid():
	   product_form.save()
	   return redirect('products')
	return render(request, 'myecom/add_product.html', {'product_form':product_form})

def delete_product(request, product_id):

	product_id = int(product_id)
	try:
		product = Product.objects.get(id = product_id)
	except Book.DoesNotExist:
		return redirect('products')
	product.delete()
	return redirect('products')