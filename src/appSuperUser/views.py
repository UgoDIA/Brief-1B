from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import xmltodict, json, os, glob, shutil
from os import walk,listdir
from os.path import isfile, join
from pathlib import Path
from quiz.models import Quizz
from django.contrib.auth.decorators import login_required
from quiz.models import Personnel, Collaborateur, Superuser, Secteur, Sessionquizz, Historique
from django.urls import reverse



def tbd(request):
    context={}
    session=Sessionquizz.objects.all().values()
    # qq=Sessionquizz.objects.values_list('idquizz',flat=True)
    # import pdb; pdb.set_trace()
    # qa=Quizz.objects.get(idquizz=qq)
    # qz=Quizz.objects.values_list('nomfichier',flat=True)
    # print(session)
    context={'session':session}
    return render(request,'tbd_sc.html', context=context)

def addS(request):
    context={}
    session=Sessionquizz.objects.all().values()
    qz=Quizz.objects.values_list('idquizz',flat=True)
    # qp=Collaborateur.objects.values_list('matricule_id',flat=True)
    # print(qp)
    context={'qz':qz, 'session':session}
    
    return render(request,'addsession.html',context)

def addrecord(request):
    x = request.POST['nquizz']
    y = request.POST['dateC']
    z = request.POST['dateE']
    w = request.POST['timer']
    e = request.POST['eva']
    user=request.user
    session = Sessionquizz(idquizz_id=x, datecreation=y, dateexpiration=z, timer=w, evaluation=e, matricule_id=user.matricule)
    session.save()
    # return HttpResponseRedirect(reverse('collab'))
    return HttpResponseRedirect(reverse('tbd'))


def assigner(request,idsession):
    request.session['idsession']=idsession
    session=Sessionquizz.objects.get(idsession=idsession)
    histo=Historique.objects.filter(idsession_id=idsession)
    qp=Collaborateur.objects.filter(historique__isnull=True).values_list('matricule_id',flat=True)
    test=Collaborateur.objects.select_related('matricule').values_list('matricule_id',flat=True)
    t=Historique.objects.select_related('collaborateur').values_list('matricule_id',flat=True)
    # qc=Personnel.objects.filter(collaborateur__matricule='00').values()
    print(t)
    context={'qp':qp,'histo':histo,'session':session}
    return render(request,'assigner.html',context)
 
def ajouter(request,matricule):
    idsession=request.session.get("idsession")
    mat=Collaborateur.objects.get(matricule_id=matricule)
    histo=Historique(idsession_id=idsession,matricule=mat)
    histo.save()
    # context={'session':session}
    return HttpResponseRedirect(reverse('assigner',kwargs={'idsession':idsession}))
    
def deleteS(request, idsession):
    session= Sessionquizz.objects.get(idsession=idsession)
    session.delete()
    return HttpResponseRedirect(reverse('tbd'))

def deleteC(request, idhisto):
    histo= Historique.objects.get(idhisto=idhisto)
    idsession=request.session.get("idsession")
    histo.delete()
    return HttpResponseRedirect(reverse('assigner',kwargs={'idsession':idsession}))

def modificationS(request, idsession):
    session=Sessionquizz.objects.get(idsession=idsession)
    qz=Quizz.objects.values_list('idquizz',flat=True)
    context = { 'qz':qz,
        'session':session
    }
    return render(request,'modificationSession.html',context)

def updaterecord(request, idsession):
    x = request.POST['nquizz']
    y = request.POST['dateC']
    z = request.POST['dateE']
    w = request.POST['timer']
    e = request.POST['eva']
    user=request.user
    session=Sessionquizz.objects.get(idsession=idsession)
    session.idquizz_id=x
    session.datecreation=y
    session.dateexpiration=z
    session.timer=w
    session.evaluation=e
    session.matricule_id=user.matricule
    session.save()
    return HttpResponseRedirect(reverse('tbd'))

def pa(request):
    return render(request,'page_aut.html')

def uploadQuizz(request):
    monRepertoireQ = 'questionnaires/'
    monRepertoireTemp = 'qjsonTemp/'
    monRepertoire='qjson/'
    context ={}
    delete(monRepertoireTemp),
    delete(monRepertoireQ),
    if request.method =='POST':
        for f in request.FILES.getlist('document'):
            quizz=f
            # print(str(f))
            fs=FileSystemStorage()
            fs.save(quizz.name,quizz)           
        exec(open("script/xmljson.py").read())
        listeFichiers=[f for f in listdir(monRepertoireTemp) if isfile(join(monRepertoireTemp,f))]
        urlFichiers=[monRepertoire + f for f in listeFichiers]
        context['noms']=listeFichiers    
        for i in range(len(listeFichiers)):
            nQ= Quizz(nomfichier=listeFichiers[i], urlfichier = urlFichiers[i])
            nQ.save()           
    #     return redirect('uploadQuizz')
    # else:
    return render(request,'uploadQuizz.html', context=context)


def delete(dossier):
    for root, dirs, files in os.walk(dossier):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def addEmp(request):
    return render(request, 'addEmployee.html', {})

def addDataInDB(request):
    if request.method == "POST": 
        #import pdb; pdb.set_trace()
        # print(request.POST)
        for i in range(1, ((len(request.POST)-1)//4)+1): # on ne prend pas la valeur csrfmiddlewaretoken. 
                                                    # Il y a pour l'instant quatres colonnes.
            matricule = request.POST['result['+str(i)+'][matricule]']
            prenom    = request.POST['result['+str(i)+'][prenom]'] 
            nom       = request.POST['result['+str(i)+'][nom]'] 
            password  = request.POST['result['+str(i)+'][password]'] 
            p = Personnel.objects.create_user(prenom=prenom, nom=nom, matricule=matricule, codesecteur="MKT", password=password); p.save()
            c = Collaborateur.objects.create(matricule=Personnel.objects.get(pk=matricule)); c.save()
        #import pdb; pdb.set_trace()
    return render(request, 'addEmployee.html')
