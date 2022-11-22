from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

def home(request):
    return HttpResponse('<h1> HOME </h1>')

#@login_required
def page1(request):
    return render(request, 'quiz/p1.html', {})

# @login_required
# @notAccessForCollaborateur
def page2(request):
    return render(request, 'quiz/p2.html', {})
   

def redirectPNF(request, exception):
    return redirect('home')

def page3(request):
    return redirect('home')

def quiz(request):
    return render(request, 'quiz/quiz.html')


def index(request):
    return redirect('login')

def test(request):
    return render(request, 'quiz/test.html')