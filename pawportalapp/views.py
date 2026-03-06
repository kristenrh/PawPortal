from django.http import HttpResponse
from django.shortcuts import render

def dashboard(request):
    loginPage = loader.get_template('LoginPage.html')
    user = request.session.get("user")
    if not user:
        return render(request, "LoginPage.html")

    return render(request, "dashboard.html")

def kennel(request):
    return render(request, "kennel.html")

def socialization(request):
    return render(request, "socialization.html")

def adoption(request):
    return render(request, "adoption.html")