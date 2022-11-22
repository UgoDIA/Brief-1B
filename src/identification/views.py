from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from quiz.models import Collaborateur, Superuser
from django.template import loader

# Create your views here.
def login_user(request):
    if request.method == "POST":
        matricule = request.POST['matricule']
        password = request.POST['password']
        user = authenticate(request, matricule=matricule, password=password)
        if user is not None:
            login(request, user)
            if user.isCollabUser():
                return redirect('accueilCollab')
            if user.isSuperUser():
                return redirect("pa")
        else:
            messages.success(request, ("Erreur de matricule ou de mot de passe, veuillez ressayer"))
            return redirect('login')
    else:
        return render(request, 'identification/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("Session deconnectée"))
    return redirect('login')


