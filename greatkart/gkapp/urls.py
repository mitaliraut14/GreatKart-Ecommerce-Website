from django.urls import path
from gkapp import views

urlpatterns = [
     path('',views.index),
]