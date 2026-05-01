from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import Animal
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
import requests
from urllib.parse import urlencode
from datetime import datetime

def dashboard(request):
    user = request.session.get("user")

    if not user:
        return render(request, "LoginPage.html")

    return render(request, "dashboard.html")

def socialization(request):
    try:
        animals = Animal.objects.all()
       
    except Exception as e:
        print(f"Database error: {e}")
        animals = []

  
    context = {
        'animals': animals,
    }

    #context = sorted(context.animals.animalname)
    return render(request, 'socialization.html', context)

def adoption(request):
    return render(request, "adoption.html")

def add_animal(request):
    print("REQUEST METHOD:", request.method)
    print("POST DATA:", request.POST)

    if request.method == "POST":
        name = request.POST.get("animalName")
        species = request.POST.get("animalSpecies")
        age = request.POST.get("animalAge")

        print("Name:", name)
        print("Species:", species)

        try:
            new_animal = Animal.objects.create(
                animalname=name,
                animalspecies=species,
                animalage = age
            )
            return JsonResponse({"status": "success"})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"status": "error"})

    return JsonResponse({"status": "error", "message": "Invalid Request"})

def remove_animal(request):
    if request.method == "POST":
        import json
        try:
            data= json.loads(request.body)
            animal_id = data.get("id")
            animal_obj = Animal.objects.get(animalid = animal_id)
            animal_obj.delete()
            return JsonResponse({"status": "success"})
        except Animal.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Animal not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def kennel(request):
    try:
        animals = Animal.objects.all()
        kennels = Animal.objects.values_list("animallocation", flat=True).distinct()  # Fetch distinct kennel locations
    except Exception as e:
        animals = []
        kennels = ["A01", "B01", "C01", "D01", "E01", "A02"]

        print(f"Database error: {e}")
    
    
    return render(request, 'kennel.html', {'animals': animals, 'kennels': kennels})

def location_update(request):
    print("METHOD:", request.method)
    print("BODY:", request.body)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("PARSED JSON:", data)

            animal_id = data.get("animal_id")
            kennel_id = data.get("kennel_id")

            print("animal_id:", animal_id)
            print("kennel_id:", kennel_id)

            animal = Animal.objects.get(animalid=animal_id)
            animal.animallocation = kennel_id
            animal.save()

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error"}, status=400)

def google_login(request):
    """
    Redirects the user to Google's OAuth 2.0 authorization endpoint.
    """
    
    # --- demo check for placeholder client ID/secret ---
    cid = settings.GOOGLE_CLIENT_ID
    csecret = settings.GOOGLE_CLIENT_SECRET
    # if "REPLACE WITH YOUR GOOGLE CLIENT ID" in cid or "REPLACE WITH YOUR GOOGLE CLIENT SECRET" in csecret:
    #     return HttpResponse(
    #         "<h1 style='color:red; font-size:2rem;'>"
    #         "Google OAuth is NOT configured"
    #         "</h1>"
    #         "<p>Set real GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in settings.py.</p>"
    #         f"<pre style='background:#222;color:#ff0000;padding:1rem;'>"
    #         f"GOOGLE_CLIENT_ID    = {cid!r}\n"
    #         f"GOOGLE_CLIENT_SECRET = {csecret!r}"
    #         "</pre>"
    #     )
    # --- end demo check ---




    # Random string to protect against CSRF
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state
    

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
    }

    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    return redirect(url)


def google_callback(request):
    """
    Handles Google's redirect back:
      - checks 'state'
      - exchanges 'code' for an access token
      - fetches user info
      - stores email in the session
    """
    if request.GET.get("state") != request.session.get("oauth_state"):
        # template = loader.get_template('Homepage.html')
        # return HttpResponse(template.render())
        return HttpResponseBadRequest("Invalid state " + request.GET.get("state", "") +" vs " + request.session.get("oauth_state", "")) 

    code = request.GET.get("code")
    if not code:
        return HttpResponseBadRequest("Missing code")

    # Exchange code for tokens
    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    )
    if not token_res.ok:
        return HttpResponseBadRequest("Token request failed")

    access_token = token_res.json().get("access_token")
    if not access_token:
        return HttpResponseBadRequest("No access token")

    # Fetch basic user info
    userinfo_res = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if not userinfo_res.ok:
        return HttpResponseBadRequest("Userinfo request failed")

    userinfo = userinfo_res.json()

    # Store just the email in the session for this demo
    request.session["user"] = {"email": userinfo.get("email")}
    request.session.pop("oauth_state", None)

    return redirect("/")


def logout_view(request):
    request.session.flush()
    return redirect("/")
