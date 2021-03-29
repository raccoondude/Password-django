SECERTKEY = ""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import hashlib
from .models import User, Token
import random
import string
import urllib
import urllib.request
import urllib3
import requests
# Create your views here.

def index(request):
    if request.method == "POST":
        Password = request.POST["password"]
        Hash = hashlib.sha256(Password.encode()).hexdigest()
        return HttpResponse(Hash)
    try:
        tokencookie = request.COOKIES['token']
        token = Token.objects.get(tokenID=tokencookie)
        username = token.userowo.username
    except:
        username = ""
    return render(request, "index.html", {"username":username})

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


def signup(request):
    if request.method == "POST":
        recaptcha_response = request.POST['g-recaptcha-response']
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
                'secret': SECERTKEY,
                'response': recaptcha_response
        }
        req = requests.post(url, data=values)
        result_json = req.json()
        if not result_json['success']:
            return render(request, "signup.html")
        user = request.POST["user"]
        Password = request.POST["password"]
        Salt = random_char(4)
        Passalt = Password + Salt
        Hash = hashlib.sha256(Passalt.encode()).hexdigest()
        Newuser = True
        UWU = User.objects.all()
        for owo in UWU:
            if owo.username == user:
                Newuser = False
        if Newuser == True:
            NewUser = User(passhash=Hash, salt=Salt, username=user).save()
            return HttpResponse("user saved, password hash: {}".format(Hash))
        else:
            return HttpResponse("User taken")
    else:
        return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        recaptcha_response = request.POST['g-recaptcha-response']
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
                'secret': SECERTKEY,
                'response': recaptcha_response
        }
        req = requests.post(url, data=values)
        result_json = req.json()
        if not result_json['success']:
            return render(request, "signin.html")
        user = request.POST["user"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=user)
        except:
            return HttpResponse("Failed")
        salt = user.salt
        passhash = user.passhash
        saltpass = password + salt
        if hashlib.sha256(saltpass.encode()).hexdigest() == passhash:
            newtokenID = random_char(40)
            newtoken = Token(tokenID=newtokenID, userowo=user).save()
            response = HttpResponseRedirect("/")
            response.set_cookie("token", newtokenID)
            return response
        else:
            return HttpResponse("Login Failed")
    return render(request, "signin.html")
