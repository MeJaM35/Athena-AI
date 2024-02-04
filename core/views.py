from django.shortcuts import render,redirect 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import Userdetails
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
    context = {
        'msg': 'Brand Builder'
    }
    return render(request, 'core/index.html', context)
def login(request):
    context = {
        'msg': 'Brand Builder'
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('index')  # Replace 'index' with the actual name or URL of your index page
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'base/login.html', context)
def register(request):
    context = {
        'msg': 'Brand Builder'
    }
    if request.method == 'POST':
        firstname = request.POST.get("firstname")
        lastname =request.POST.get("lastname")
        tel =  request.POST.get("tel")
        email =request.POST.get("email")
       
        passward = request.POST.get("passward")
        userdetails= Userdetails(firstname=firstname,lastname=lastname,tel=tel, email=email,passward=passward)
        userdetails.save()

    return render(request, 'base/register.html', context)


# Create your views here.
