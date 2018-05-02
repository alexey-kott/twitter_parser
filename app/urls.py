# chat/urls.py
from django.conf.urls import url, include
from django.contrib import admin


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^twitter-report/', views.twitter_report, name='twitter-report'),
]