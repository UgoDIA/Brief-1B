from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from quiz.models import Quizz, Personnel, Collaborateur, Superuser, Sessionquizz
import json, os
from django.http import JsonResponse
import pdb
from django.urls import reverse

def pa1(request):
    session=Sessionquizz.objects.all().values()
    context={'session':session}
    return render(request, 'page_accueil.html',context)
    

def ce(request, idsession):
    print(idsession)
    request.session["idsession"]=idsession
    context={'session':idsession}
   
    return render(request, 'condi_exam.html',context)

# ** 
# Save data in session and send the first question
# - quiz(dict)           : the question sheet
# - numQuestion(int)     : question number
# - pointsDuCandidat(int): score of the candidate over the questions
# **
def initQuiz(request):
    # idsession=request.session.get("idsession")
    # session= Sessionquizz.objects.get(idsession=idsession)
    file="qjson/31.quv.json" #Quizz.objects.get(idquizz=session.idquizz_id)
    
    with open(file) as f: data = json.load(f) # .urlfichier
    request.session['pointsDuCandidat'] = 0
    request.session['quiz'] = data
    request.session['numQuestion'] = 0
    context = dataToDict(request.session.get('quiz'), request.session.get('numQuestion'))
    context.update({"totalQ": len(data["questionnaire"]["question"])})
    return render(request, 'evalQuiz.html', context=context)


# **
# Submit next question
# - incremente numQuestion
# **
def nextQuestion(request):
    if request.method == "POST":
        data = request.session.get("quiz")
        numQuestion =  request.session.get('numQuestion')
        repUser = request.POST.getlist('result[]', False)
        request.session["pointsDuCandidat"]  = request.session.get("pointsDuCandidat") + verifResponses(data, repUser, numQuestion)
        if(numQuestion < len(data["questionnaire"]["question"])-1):
            request.session["numQuestion"] = numQuestion +1
            context = dataToDict(data, numQuestion + 1)
            return JsonResponse({"data":context})
        else:
            return JsonResponse({"data":numQuestion})

def score(request):
    score =  request.session.get("pointsDuCandidat")
    return render(request, 'finQuizz.html', context={"score":score})     

# ** 
# Extracts data from quiz
# return(dict) with only the elements for the realization of the quiz
# **
def dataToDict(data, numQuestion):
    duree       = convertTimeToSec(data["questionnaire"]["question"][numQuestion]["@duree"])
    titre       = data["questionnaire"]["question"][numQuestion]["titre"]
    intitule    = data["questionnaire"]["question"][numQuestion]["intitule"]
    reponses    = data["questionnaire"]["question"][numQuestion]['listerep']["reponse"]
    context={"duree"       : duree,
             "titre"       : titre,
             "intitule"    : intitule,
             "reponses"    : reponses,
             "numQuestion" : numQuestion}
    return context

#**
# Convert string time to float representing the second
# return(float) second
# ** 
def convertTimeToSec(t): 
    s = t.split(':');  # exemple: "00:00:30.00" -> ["00","00","30.00"]
    sec = float(s[0])*3600+float(s[1])*60+float(s[2]);  
    return sec

#** Checks and assigns the point
#**
def verifResponses(data, repUser, numQuestion):
    bonneRep = data["questionnaire"]["question"][numQuestion]["@bonne"]
    coeff    = data["questionnaire"]["question"][numQuestion]["@coeff"]
    point    = 0 
    # tests if the user has checked boxes
    if(repUser):
        # test si le nombre de réponse attendu est le même nombre de case à coché
        if(len(repUser) == len(bonneRep)): 
            # checks if the correct answer corresponds to the checked box
            if(bonneRep == repUser[0]):
                point = 1*int(coeff)
    return point
        


def trainquizz(request):
    return render(request, 'trainQuizz.html')
        
# --------------------------------------------------------------------------------------------------

def page1(request): 
    # load and init data
    request.session["nb"] = 0
    context = {"nb": 0}
    return render(request, 'page1.html', context)

def incremente(request): 
    request.session["nb"] = request.session.get("nb") +1
    print(request.session.get("nb") +1)
    return JsonResponse({"nb": request.session.get("nb")})

def page2(request):
    return render(request, "page2.html")  