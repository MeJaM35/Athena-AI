
from django.urls import path , include 
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('cards', views.cards, name='cards'),



    
]