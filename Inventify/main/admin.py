from django.contrib import admin
from .models import Listing, Review, ListingAttribute, Email#, User
'''
from django.db import models
from django.conf import settings
from django.conf.urls import url, include#, patterns
'''


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('listing_type', 'name', 'address', 'short_description', 'description', 'average_rating', 'capacity', 'phone_number', 'email', 'facebook', 'twitter', 'website')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'listing', 'title', 'rating', 'date')

@admin.register(ListingAttribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('type', 'listing')
    
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('date', 'email', 'title', 'content')
