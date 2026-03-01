from django.http import HttpResponse
from django.shortcuts import render
from .models import Animal, AnimalLocation

def dashboard(request):
    return render(request, "dashboard.html")

def kennel(request):
    animals = Animal.objects.all()
    kennel = AnimalLocation.objects.all()
    return render(request, "kennel.html", {"animals": animals, "kennel": kennel})

def socialization(request):
    return render(request, "socialization.html")

def adoption(request):
    return render(request, "adoption.html")