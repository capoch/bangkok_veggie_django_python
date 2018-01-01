"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from .views import location_list, location_create, location_detail, location_edit, posts_list, posts_create, posts_detail, posts_edit, posts_delete, about, vdict, thai_dishes, contact

urlpatterns = [
    url(r'^$', posts_list, name="home"),
    url(r'^location/$', location_list, name="locations"),
    url(r'^location/create/$', location_create, name="create_location"),
    url(r'^location/(?P<slug>[\w-]+)/$', location_detail, name="detail_location"),
    url(r'^location/(?P<slug>[\w-]+)/edit/$', location_edit, name="edit_location"),
    url(r'^create/$', posts_create, name="create"),
    url(r'^about/$', about, name="about"),
    url(r'^dict/$', vdict, name="dict"),
    url(r'^thai_dishes/$', thai_dishes, name="thai_dishes"),
    url(r'^contact/$', contact, name="contact"),
    url(r'^(?P<slug>[\w-]+)/$', posts_detail, name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$', posts_edit, name="edit"),
    url(r'^(?P<slug>[\w-]+)/delete/$', posts_delete, name="delete"),

]
