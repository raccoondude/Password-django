from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from .models import User
import random
import string
# Create your views here.

def index(request):
    if request.method == "POST":
        Password = request.POST["password"]
        Hash = hashlib.sha256(Password.encode()).hexdigest()
        return HttpResponse(Hash)
    return render(request, "index.html")

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


def signup(request):
    if request.method == "POST":
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
            return HttpResponse("Login successful!")
        else:
            return HttpResponse("Login Failed")
    return render(request, "signin.html")
