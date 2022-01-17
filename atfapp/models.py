from django.db import models

# Create your models here.

class UserDetails(models.Model):
    fingerprint=models.ImageField(upload_to='fingerprint_img')
    photo=models.ImageField(upload_to='face_image')

class Transaction(models.Model):
    fingerprint=models.ImageField(upload_to='fingerprint_img')
    photo=models.ImageField(upload_to='face_image')
    CurrentDate=models.DateField()
    status=models.IntegerField()
