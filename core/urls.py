
from django.urls import path , include 
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('prompt', views.prompt, name='prompt'),
    path('register', views.register, name='register'),
    path('', views.index, name='dashboard'),
    path('cards', views.cards, name='cards'),
    path('profile', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit'),

    path('competitors', views.competitorDisplay, name='competitor-display'),
    path('analysis/<str:pk>', views.analysis, name='analysis'),


    #charts urls




    
]