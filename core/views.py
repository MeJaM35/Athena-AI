from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


def index(request):
    context = {
        'msg': 'Brand Builder'
    }
    return HttpResponse(context)

# Create your views here.
