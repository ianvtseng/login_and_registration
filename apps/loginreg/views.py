from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages

def index(request):
    # Users.objects.all().delete()
    context = {
        "users": Users.objects.all()
    }
    return render(request, "loginreg/index.html", context)

def register(request):
    if request.method == "POST":
        modelResponse = Users.objects.register(request.POST)
        if modelResponse["registered"]:
            print "yay"
            request.session["id"] = modelResponse["user"].id
            request.session["first_name"] = modelResponse["user"].first_name
            request.session["last_name"] = modelResponse["user"].last_name
            request.session["welcome_message"] = "registered."
            return redirect("loginreg:success")
        else:
            for error in modelResponse["errors"]:
                messages.error(request, error)
            return redirect("loginreg:index")

def login(request):
    if request.method == "POST":
        modelResponse = Users.objects.login(request.POST)
        if modelResponse["loggedin"]:
            request.session["id"] = modelResponse["user"].id
            request.session["first_name"] = modelResponse["user"].first_name
            request.session["last_name"] = modelResponse["user"].last_name
            request.session["welcome_message"] = "logged in."
            return redirect("loginreg:success")
        else:
            for error in modelResponse["errors"]:
                messages.error(request, error)
            return redirect("loginreg:index")

def success(request):
    return render(request, "loginreg/success.html")
