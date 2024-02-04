from django.db import models


class Userdetails(models.Model):
   firstname = models.CharField(max_length=20)
   lastname =models.CharField(max_length=20)
   tel =  models.CharField(max_length=12)
   email = models.CharField(max_length=40)
   passward = models.CharField(max_length=20, blank=True, null=True )
