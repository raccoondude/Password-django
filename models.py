from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    salt = models.CharField(max_length=4)
    passhash = models.CharField(max_length=64)
