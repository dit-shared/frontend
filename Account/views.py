from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import HashPassword, User
from Frontend import settings
import os, json, time, subprocess

def runShell(path, sh_input = ''):
    shellscript = subprocess.Popen([settings.BASE_DIR + '/' + path], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = shellscript.communicate(sh_input)
    returncode = shellscript.returncode
    return returncode, stdout, stderr

def buildJSONRespose(responseData):
	return HttpResponse(json.dumps(responseData), content_type="application/json")

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

    files = os.listdir(settings.BASE_DIR + "/research")
    
    response = list()
    for i, f in enumerate(files):
        response.append({"dirname": f, "snapshots": len(os.listdir(settings.BASE_DIR + "/research/" + f)),
                            "weight": os.path.getsize(settings.BASE_DIR + "/research/" + f)})

    return render(request, "Account/view.html", {"user": user, "response": response})

def upload(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]
    return render(request, "Account/upload.html", {"user": user})

def predict_view(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]

    return render(request, "Account/predict.html", {"user": user})

def predict(request):
    code, out, err = runShell("run.sh")
    return buildJSONRespose({"message": str(out, 'utf-8'), "success": True})

def encPasswd(request):
    if 'passwd' not in request.GET:
        return HttpResponse("Incorrect GET request")
    return HttpResponse(HashPassword(request.GET['passwd']))