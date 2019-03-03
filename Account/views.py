from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import HashPassword, User

def account(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]
    return render(request, "Account/index.html", {"user": user})

def view(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]
    return render(request, "Account/view.html", {"user": user})

def upload(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]
    return render(request, "Account/upload.html", {"user": user})

def predict(request):
    return HttpResponse("predict")

def encPasswd(request):
    if 'passwd' not in request.GET:
        return HttpResponse("Incorrect GET request")
    return HttpResponse(HashPassword(request.GET['passwd']))