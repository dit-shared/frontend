from django.shortcuts import render
from django.http import HttpResponse
from .models import HashPassword

def index(request):
    return render(request, "Account/index.html")

def encPasswd(request):
    if 'passwd' not in request.GET:
        return HttpResponse("Incorrect GET request")
    return HttpResponse(HashPassword(request.GET['passwd']))