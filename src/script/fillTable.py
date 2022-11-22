###################################################
########## À partir du shell python ###############
###################################################

import names
from quiz.models import Personnel, Collaborateur, Superuser, Secteur, Quizz
from random import randint
import os
import re
#import json

print("\n=============== start ===============")

print("--- Ajout d'employé ---")
s1 = Secteur.objects.create(nomsecteur="marketing", codesecteur="MKT"); s1.save()
s2 = Secteur.objects.create(nomsecteur="informatique", codesecteur="INF"); s2.save()
for i in range(0, 20):
       n = names.get_full_name().split(" ")
       print(n[0] + " " + n[1])
       p = Personnel.objects.create_user(prenom=n[0], nom=n[1], matricule=str(i).zfill(2), codesecteur="MKT", password=str(i).zfill(2))
       p.save()
       if i < 10:
              c = Collaborateur.objects.create(matricule=Personnel.objects.get(pk=str(i).zfill(2))); c.save()
       else:
              su = Superuser.objects.create(matricule=Personnel.objects.get(pk=str(i).zfill(2)), role=randint(0,1)); su.save()


print("dir execution path: " + os.getcwd())
print("--- Ajout de quiz ---")
quizPath = "qjson"
ldir     = os.listdir(quizPath)
for i in range(0, len(ldir)):
       print("fichier: " + ldir[i])
       Quizz.objects.create(nomfichier  = re.sub("\\.json", "", ldir[i]), 
                            urlfichier  = os.path.abspath(os.path.join(quizPath, ldir[i])),
                            codesecteur = Secteur.objects.get(codesecteur="MKT"),
                            matricule   = Superuser.objects.get(matricule="12")).save()
                            
       

print("=============== end ===============")

