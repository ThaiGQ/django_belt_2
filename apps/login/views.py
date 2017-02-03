from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import User

# Create your views here.
def index(request):
    return render(request, "login/index.html")

def register(request):
    if request.method == "POST":
        submitted_data = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "alias": request.POST["alias"],
            "email": request.POST["email"],
            "password": request.POST["password"],
            "confirm_password": request.POST["confirm_password"],
            "dob": request.POST["dob"]
        }
        print type(request.POST["dob"])
        results = User.objects.registration_validator(submitted_data)
        print results
        if results[0]:
            for error in results[1]:
                messages.error(request, error)
            return redirect(reverse("login:main"))
        request.session["logged_in_user"] = results[1].id
        messages.success(request, "User successfully registered! Welcome, " + results[1].first_name + "!")
        return redirect(reverse("poke:main"))
    else:
        return redirect(reverse("login:main"))

def login(request):
    if request.method == "POST":
        submitted_data = {
            "email": request.POST["email"],
            "password": request.POST["password"]
        }
        results = User.objects.login_validator(submitted_data)
        if not results[0]:
            messages.error(request, results[1])
            return redirect(reverse("login:main"))
        else:
            request.session["logged_in_user"] = results[1].id
            messages.success(request, "Welcome back, " + results[1].first_name + "!")
            return redirect(reverse("poke:main"))
    else:
        return redirect(reverse("login:main"))

def success(request, user_id):
    user = User.objects.get(id = request.session["logged_in_user"])
    return redirect(reverse("poke:main"))

def logout(request):
    request.session.pop("logged_in_user")
    return redirect("login:main")
