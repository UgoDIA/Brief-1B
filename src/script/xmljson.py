import xmltodict, json
from os import walk
import os

def  getListeFichiers(dossier) :
    listeFichiers = []
    for (repertoire, sousRepertoires, fichiers) in walk(dossier):
        listeFichiers.extend(fichiers)
        break                            
    # print(listeFichiers)
    return listeFichiers

def traiterUnFichier(fichierQuizz):
    with open(fichierQuizz,'r',encoding="ISO-8859-1") as myfile:
        obj = xmltodict.parse(myfile.read())
    return obj

# \..* 
# import re

monRepertoire = 'questionnaires/'
listeFichiers = getListeFichiers(monRepertoire)
if not os.path.exists('qjsonTemp/'):
   os.makedirs('qjsonTemp/')

for fich in range(len(listeFichiers)):
    json_data = json.dumps(traiterUnFichier(monRepertoire+listeFichiers[fich]))
    # print(json_data)
    # x = re.sub("\..*","" ,listeFichiers[fich])
    pathOutput = "qjson/"+listeFichiers[fich] +".json"
    with open(pathOutput, "w") as outfile:outfile.write(json_data)
    pathOutputTemp = "qjsonTemp/"+listeFichiers[fich] +".json"
    with open(pathOutputTemp, "w") as outfile:outfile.write(json_data)

