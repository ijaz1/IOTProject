from django.db import models

# Create your models here.

class UserDetails(models.Model):
    fingerprint=models.CharField(max_length=200)
    photo=models.ImageField()

class Transaction(models.Model):
    fingerprint=models.CharField(max_length=200)
    photo=models.ImageField()
    CurrentDate=models.DateField()
    status=models.IntegerField()
