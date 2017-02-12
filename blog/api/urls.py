from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    PostCreateAPIView,
    PostDeleteAPIView,
    PostDetailAPIView,
    PostListAPIView,
    PostUpdateAPIView,
    )


urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name="list"),
    url(r'^create/$', PostCreateAPIView.as_view(), name="create"),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name="edit"),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name="delete"),

    # url(r'^$', posts_list, name="home"),
    # url(r'^create/$', posts_create, name="create"),
    # url(r'^(?P<slug>[\w-]+)/$', posts_detail, name="detail"),
    # url(r'^(?P<slug>[\w-]+)/edit/$', posts_edit, name="edit"),
    # url(r'^(?P<slug>[\w-]+)/delete/$', posts_delete, name="delete"),
]
