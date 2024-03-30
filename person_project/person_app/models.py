from django.db import models

CHOICES = (('male','male'), ('female','female'), ('other','other'))

class Person(models.Model):
    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 50)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='images/')
    gender = models.CharField(max_length=20, choices = CHOICES)
    city = models.CharField(max_length= 50)
    address = models.TextField()
    pincode = models.IntegerField()
