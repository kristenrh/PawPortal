from django.http import HttpResponse
from django.shortcuts import render
from .models import animal

def dashboard(request):
    return render(request, "dashboard.html")

def socialization(request):
    return render(request, "socialization.html")

def adoption(request):
    return render(request, "adoption.html")

def kennel(request):
    try:
        products = animal.objects.all()  # Fetch all products
    except Exception as e:
        products = []
        print(f"Database error: {e}")
    return render(request, 'kennel.html', {'products': products})