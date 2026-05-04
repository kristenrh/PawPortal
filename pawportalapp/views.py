from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone

from .models import AdoptionEvent, Animal

from urllib.parse import urlencode
from datetime import datetime

import json
import secrets
import requests


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
        "animals": animals,
    }

    return render(request, "socialization.html", context)


def kennel(request):
    try:
        animals = Animal.objects.filter(isadopted=False)
        kennels = Animal.objects.values_list("animallocation", flat=True).distinct()

    except Exception as e:
        print(f"Database error: {e}")
        animals = []
        kennels = ["A01", "B01", "C01", "D01", "E01", "A02"]

    return render(request, "kennel.html", {
        "animals": animals,
        "kennels": kennels,
    })


def adoption(request):
    animals = Animal.objects.all()
    all_events = AdoptionEvent.objects.all()

    events_dict = {}

    for event in all_events:
        date_key = event.adoption_date.strftime("%Y-%m-%d")
        time_str = event.adoption_time.strftime("%H:%M")

        if date_key not in events_dict:
            events_dict[date_key] = []

        events_dict[date_key].append({
            "id": event.id,
            "animal": event.animal.animalname,
            "adopter": event.adopter_name,
            "time": time_str,
            "notes": event.notes if event.notes else "",
        })

    return render(request, "adoption.html", {
        "animals": animals,
        "events_json": json.dumps(events_dict),
    })


def delete_adoption_event(request):
    if request.method == "POST":
        target_id = request.POST.get("event_id")
        event_to_delete = get_object_or_404(AdoptionEvent, id=target_id)
        event_to_delete.delete()
        return redirect("adoption")

    return redirect("adoption")


def add_animal(request):
    if request.method == "POST":
        name = request.POST.get("animalName", "").strip()
        species = request.POST.get("animalSpecies", "").strip()
        age = request.POST.get("animalAge", "").strip()
        next_url = request.POST.get("next", "")

        # These fields only come from the socialization form.
        # The kennel form does not send these.
        location = request.POST.get("animallocation", None)
        lw_raw = request.POST.get("lastwalk", None)

        lw = None

        if lw_raw:
            try:
                lw = datetime.fromisoformat(lw_raw)

                if timezone.is_naive(lw):
                    lw = timezone.make_aware(lw)

            except Exception as e:
                print("Date error:", e)

                if next_url == "/kennel/":
                    return JsonResponse({
                        "status": "error",
                        "message": "Invalid date format.",
                    })

                return redirect(next_url or "socialization")

        try:
            animal = Animal.objects.filter(animalname__iexact=name).first()

            if animal:
                animal.animalname = name
                animal.animalspecies = species
                animal.animalage = age

                # Only update kennel location if the form actually sent it.
                # This prevents the kennel add form from wiping drag/drop location.
                if location is not None:
                    animal.animallocation = location.strip()

                # Only update lastwalk if the form actually sent it.
                # This prevents the kennel add form from wiping socialization data.
                if lw_raw is not None:
                    animal.lastwalk = lw

                animal.save()

                message = "Animal updated successfully."

            else:
                new_location = ""

                if location is not None:
                    new_location = location.strip()

                animal = Animal.objects.create(
                    animalname=name,
                    animalspecies=species,
                    animalage=age,
                    animallocation=new_location,
                    lastwalk=lw,
                )

                message = "Animal added successfully."

            # Kennel add uses fetch(), so it expects JSON.
            if next_url == "/kennel/":
                return JsonResponse({
                    "status": "success",
                    "message": message,
                    "animalId": animal.animalid,
                    "animalName": animal.animalname,
                })

            # Socialization form uses normal POST, so redirect back.
            if next_url:
                return redirect(next_url)

            return redirect("socialization")

        except Exception as e:
            print(f"Error saving animal: {e}")

            if next_url == "/kennel/":
                return JsonResponse({
                    "status": "error",
                    "message": str(e),
                })

            return redirect(next_url or "socialization")

    return redirect("kennel")


def remove_animal(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            animal_id = data.get("id")

            print("REMOVE ID:", animal_id)

            if not animal_id:
                return JsonResponse({
                    "status": "error",
                    "message": "No animal ID received.",
                })

            animal_obj = Animal.objects.get(animalid=int(animal_id))
            animal_obj.delete()

            return JsonResponse({
                "status": "success",
                "message": "Animal removed successfully.",
            })

        except Animal.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Animal not found in database.",
            })

        except Exception as e:
            print("DELETE ERROR:", e)

            return JsonResponse({
                "status": "error",
                "message": str(e),
            })

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method.",
    })


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
            return JsonResponse({
                "status": "error",
                "message": str(e),
            }, status=400)

    return JsonResponse({"status": "error"}, status=400)


def google_login(request):
    """
    Redirects the user to Google's OAuth 2.0 authorization endpoint.
    """

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
      - checks state
      - exchanges code for an access token
      - fetches user info
      - stores email in the session
    """

    if request.GET.get("state") != request.session.get("oauth_state"):
        return HttpResponseBadRequest(
            "Invalid state "
            + request.GET.get("state", "")
            + " vs "
            + request.session.get("oauth_state", "")
        )

    code = request.GET.get("code")

    if not code:
        return HttpResponseBadRequest("Missing code")

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

    userinfo_res = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if not userinfo_res.ok:
        return HttpResponseBadRequest("Userinfo request failed")

    userinfo = userinfo_res.json()

    request.session["user"] = {
        "email": userinfo.get("email"),
    }

    request.session.pop("oauth_state", None)

    return redirect("/")


def logout_view(request):
    request.session.flush()
    return redirect("/")


def save_adoption_event(request):
    if request.method == "POST":
        try:
            animal_id = request.POST.get("animalId")
            animal = get_object_or_404(Animal, animalid=animal_id)

            date_str = request.POST.get("adoption_date")
            time_str = request.POST.get("adoption_time")

            combined_dt = datetime.strptime(
                f"{date_str} {time_str}",
                "%Y-%m-%d %H:%M",
            )

            AdoptionEvent.objects.create(
                animal=animal,
                adopter_name=request.POST.get("adopter_name"),
                adoption_date=combined_dt.date(),
                adoption_time=combined_dt.time(),
                notes=request.POST.get("notes"),
            )

            return redirect("adoption")

        except Exception as e:
            print(f"Error saving adoption: {e}")
            return render(request, "adoption.html", {
                "error": "Check your date/time format!",
            })

    return redirect("adoption")