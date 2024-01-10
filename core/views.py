from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def index(request):
    context = {
        'msg': 'Brand Builder'
    }
    return Response(context)

# Create your views here.
