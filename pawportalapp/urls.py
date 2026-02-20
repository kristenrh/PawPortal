from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("kennel/", views.kennel, name="kennel"),
    path("socialization/", views.socialization, name="socialization"),
    path("adoption/", views.adoption, name="adoption"),
]