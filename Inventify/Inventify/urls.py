"""Inventify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main import views
from django.template import loader
from django.shortcuts import render, redirect
from main import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name ='home'),
    url(r'^sign_up/$', views.sign_up, name ='sign_up'),
    url(r'^log_in/$', auth_views.login, {'template_name': 'main/log_in.html'}, name='log_in'),
    url(r'^log_out/$', views.log_out, name ='log_out'),
    url(r'^view_listing/$', views.listing_page, name ='view_listing'),
    url(r'^home/(?P<listing>[\'\,\w ]+)/$', views.listing_page, name = 'venuePage'),
    url(r'^userPage/$', views.user_page, name ='User Page'),
    url(r'^confirmationPage/$', views.confirmationPage, name = "Confirmation Page"),
    url(r'^delete_list/$', views.delete_list, name = "delete_list"),
    url(r'^delete_list_item/$', views.delete_list_item, name = "delete_list_item"),
    url(r'^email/$', views.emailView, name= 'email'),
    url(r'^success/$', views.successView, name= 'success'),
    url(r'^delete_review/$', views.delete_review, name= 'delete_review'),
]
