from django.http import HttpResponse
from django.shortcuts import render
<<<<<<< HEAD
#from .models import Animal, AnimalLocation
||||||| 54e06d5
=======
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import secrets
import requests
from .models import animal
>>>>>>> e9861d82279a3eadbde6e804f349320a1579a1fd

def dashboard(request):
    user = request.session.get("user")
    if not user:
        return render(request, "LoginPage.html")

<<<<<<< HEAD
def kennel(request):
    #animals = Animal.objects.all()
    #kennel = AnimalLocation.objects.all()
    return render(request, "kennel.html")
||||||| 54e06d5
def kennel(request):
    return render(request, "kennel.html")
=======
    return render(request, "dashboard.html")
>>>>>>> e9861d82279a3eadbde6e804f349320a1579a1fd

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

def getData(animal_id):
    try:
        itemrequest = animal.objects.filter(animalid=animal_id).values()  # Fetch animal at id
    except Exception as e:
        itemrequest = []
        print(f"Database error: {e}")
    return itemrequest


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
    """Clear the session and go back to home."""
    request.session.pop("user", None)
    request.session.pop("oauth_state", None)
    return redirect("/")
