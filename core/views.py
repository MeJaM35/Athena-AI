from django.shortcuts import render,redirect 
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User



def index(request):
    context = {
        'msg': 'Brand Builder'
    }
    return render(request, 'core/index.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        print(f"{email} {password}")

        

        user = authenticate(request, username=email, password=password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'core/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('landing')



# Create your views here.
