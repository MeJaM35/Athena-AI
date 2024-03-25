
from django.urls import path , include 
from . import views


urlpatterns = [
    path('', views.profile, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('prompt', views.prompt, name='prompt'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('cards', views.cards, name='cards'),
    path('profile', views.profile, name='profile'),
    path('competitors', views.competitorDisplay, name='competitor-display'),



    
]