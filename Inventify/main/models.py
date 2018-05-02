from django.db import models
'''Just in case we need them.
from decimal import *'''
from datetime import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
'''from django.conf.urls import url
from django.contrib import admin
from main import views
from django.contrib auth import views as auth_views
import MySQLdb'''

#variables = lowercase_with_underscores
#class names = InitialCaps


class Listing(models.Model):
    TYPE_CHOICES = (('V', 'Venue'), ('S', 'Service'))
    listing_type = models.CharField(max_length=1,choices=TYPE_CHOICES, default='V')
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    short_description = models.CharField(max_length=100) #Brief info for previews
    description = models.TextField()  #Full info for listing's page
    hours = models.CharField(max_length=80, blank=True)   
    average_rating = models.FloatField(default=0.0)  # Zero for no reviews; updated when new review is added
    capacity = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=10, blank=True)  # Must be (XXX)XXX-XXXX format
    email = models.EmailField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    website = models.URLField(blank=True)
    picture = models.URLField()


class Review(models.Model):
    class Meta:
        unique_together = ('author', 'listing') #only one review per listing per author
        
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE) #listing review is in reference to
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.PositiveIntegerField() #https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
    date = models.DateTimeField(auto_now_add=True)

class UserList(models.Model): #user-made list of venues/services
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    
class ListElements(models.Model): #elements of UserList
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    parent_list = models.ForeignKey(UserList, on_delete=models.CASCADE)
    
class ListingAttribute(models.Model): #act as tags for a listing
    class Meta:
        unique_together = ('type', 'listing') #no duplicate tags for a listing

    TYPE_CHOICES = (('CA', 'Catering available'), ('OF', 'No outside food or beverages'), ('AA', 'Animals allowed'), ('21', 'Age 21+'), ('18', 'Age 18+'), ('FF', 'Family-friendly'), ('AP', 'Alcohol permitted'), ('SP', 'Smoking permitted'), ('VF', 'Vegan food available'), ('VE', 'Vegetarian food available'), ('SE', 'Sound equipment provided'), ('OD', 'Outdoors'), ('ID', 'Indoors'), ('IO', 'Indoors and outdoors'))
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    
class Email(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    title = models.CharField(max_length=50)
    content = models.TextField()
  
    
