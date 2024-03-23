from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

class Brand(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    size = models.IntegerField(default=-1)  # -1 means not


class Instagram(models.Model):
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE)
    url = models.URLField()
    tag = models.CharField(max_length=256, blank=True, null=True)
    totalposts = models.IntegerField()
    totalfollows = models.IntegerField()
    tenthlikes = models.IntegerField()
    eleventhlikes = models.IntegerField()
    twelthlikes = models.IntegerField()
    lastninereach = models.IntegerField()
