from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import HashPassword, User, Feedback
from Frontend import settings
from Frontend.TelegramBot import send as telegram_send
import os, json, time, subprocess, datetime

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

    if settings.ON_SERVER:
        res_dir = "/root/common/npcmr/DICOM_FINAL/"
    else:
        res_dir = settings.BASE_DIR + "/research/"
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

def feedback(request):
    if 'id' not in request.session:
        return buildJSONRespose({"message": 'Error: you are not authorized', "success": True})
    if 'title' not in request.POST or 'text' not in request.POST:
        return buildJSONRespose({"message": 'Error: invalid request data', "success": True})
    
    feedback = Feedback.objects.create(user_id=request.session['id'], title=request.POST['title'],
                text=request.POST['text'], time=datetime.datetime.now())
    feedback.save()

    if settings.TELEGRAM_FEEDBACK:
        user = User.objects.filter(id=request.session['id'])[0]
        telegram_msg = 'Title: ' + feedback.title + '\nText: ' + feedback.text + '\nFrom: ' + str(user)
        telegram_send(settings.FeedbackTelegramChannelToken, settings.FeedbackTelegramChatId, telegram_msg)

    return buildJSONRespose({"message": "", "success": True})

