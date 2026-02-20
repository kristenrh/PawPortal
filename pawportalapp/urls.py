from django.urls import path
from . import views

urlpatterns = [
    path('pawportalapp', views.index, name="index"),
]