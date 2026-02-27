from django.urls import path
from . import views
from django.contrib import admin
from pawportalapp import views

urlpatterns = [
    path('pawportalapp', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path("login/", views.google_login, name="login"),
    path("oauth2callback/", views.google_callback, name="oauth2callback"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("kennel/", views.kennel, name="kennel"),
    path("socialization/", views.socialization, name="socialization"),
    path("adoption/", views.adoption, name="adoption"),
]
