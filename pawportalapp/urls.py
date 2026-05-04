from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("kennel/", views.kennel, name="kennel"),
    path("add_animal/", views.add_animal, name="add_animal"),
    path("remove_animal/", views.remove_animal, name="remove_animal"),
    path("location_update/", views.location_update, name="location_update"),
    path("socialization/", views.socialization, name="socialization"),
    path("adoption/", views.adoption, name="adoption"),
    path("login/", views.google_login, name="login"),
    path("oauth2callback/", views.google_callback, name="oauth2callback"),
    path("logout/", views.logout_view, name="logout"),
    path('save-adoption-event/', views.save_adoption_event, name='save_adoption_event'),
]

