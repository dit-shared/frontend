from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import HashPassword, User
from Frontend import settings
import os, json, time, subprocess

def runCommand(commands):
    subprocess.run(commands)

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

    res_dir = "/root/common/npcmr/DICOM_FINAL/"
    files = os.listdir(res_dir)
    
    response = list()
    ind = 0
    for i, f in enumerate(files):
        if f[0] != '.':
            ind += 1
            response.append({"index": ind, "dirname": f, "snapshots": len(os.listdir(res_dir + f)),
                             "weight": os.path.getsize(res_dir + f) // 1024})

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
    runCommand(["docker", "exec", "-i", "-t", "root_jupyter_1_826396f9a729", "/bin/bash", "/radio/temp/for_npcmr/run.sh"])
    #runCommand(["/radio/temp/for_npcmr/run.sh"])
    return buildJSONRespose({"message": "", "success": True})

def encPasswd(request):
    if 'passwd' not in request.GET:
        return HttpResponse("Incorrect GET request")
    return HttpResponse(HashPassword(request.GET['passwd']))
