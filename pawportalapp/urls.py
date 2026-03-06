from django.urls import path
from . import views
from django.contrib import admin
from pawportalapp import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("kennel/", views.kennel, name="kennel"),
    path("socialization/", views.socialization, name="socialization"),
    path("adoption/", views.adoption, name="adoption"),
    path("login/", views.google_login, name="login"),
    path("oauth2callback/", views.google_callback, name="oauth2callback"),
    path("logout/", views.logout_view, name="logout"),
]
