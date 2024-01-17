from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


def index(request):
    context = {
        'msg': 'Brand Builder'
    }
    return render(request, 'core/index.html', context)
def login(request):
    context = {
        'msg': 'Brand Builder'
    }
    return render(request, 'base/login.html', context)
def register(request):
    context = {
        'msg': 'Brand Builder'
    }
    return render(request, 'base/register.html', context)

# Create your views here.
