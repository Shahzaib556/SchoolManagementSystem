from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SiteSettings


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    return render(request, "sitepages/home.html")


def about(request):
    return render(request, "sitepages/about.html")


def services(request):
    return render(request, "sitepages/services.html")


def contact(request):
    if request.method == "POST":
        messages.success(request, "Thanks for reaching out! Our office will get back to you shortly.")
        return redirect("sitepages:contact")
    return render(request, "sitepages/contact.html")
