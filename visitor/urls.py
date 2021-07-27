from django.contrib import admin
from django.urls import path,include
from admin1 import views 
urlpatterns = [
	path('index', views.index)
]
 