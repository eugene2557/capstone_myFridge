from django.urls import path
from . import views

urlpatterns = [
    path('', views.fridge, name='fridge'),
]