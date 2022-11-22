# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Secteur(models.Model):
    codesecteur = models.CharField(db_column='codeSecteur', primary_key=True, max_length=10)  # Field name made lowercase.
    nomsecteur = models.CharField(db_column='nomSecteur', max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'secteur'


class Personnel(models.Model):
    matricule = models.CharField(primary_key=True, max_length=10)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    codesecteur = models.ForeignKey('Secteur', models.DO_NOTHING, db_column='codeSecteur')  # Field name made lowercase.

    class Meta:
        db_table = 'personnel'

class Collaborateur(models.Model):
    matricule = models.OneToOneField('Personnel', models.DO_NOTHING, db_column='matricule', primary_key=True)

    class Meta:
        db_table = 'collaborateur'
           

class Superuser(models.Model):
    matricule = models.OneToOneField(Personnel, models.DO_NOTHING, db_column='matricule', primary_key=True)
    role = models.BooleanField()

    class Meta:
        db_table = 'superuser'
        


class Historique(models.Model):
    idhisto = models.AutoField(db_column='idHisto', primary_key=True)  # Field name made lowercase.
    matricule = models.ForeignKey(Collaborateur, models.DO_NOTHING, db_column='matricule')
    idsession = models.ForeignKey('Sessionquizz', models.DO_NOTHING, db_column='idSession')  # Field name made lowercase.
    score = models.IntegerField(blank=True, null=True)
    dateparticipation = models.DateField(db_column='dateParticipation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'historique'



class Quizz(models.Model):
    idquizz = models.AutoField(db_column='idQuizz', primary_key=True)  # Field name made lowercase.
    nomfichier = models.CharField(db_column='nomFichier', max_length=30)  # Field name made lowercase.
    urlfichier = models.CharField(db_column='urlFichier', max_length=200)  # Field name made lowercase.
    codesecteur = models.ForeignKey('Secteur', models.DO_NOTHING, db_column='codeSecteur')  # Field name made lowercase.
    matricule = models.ForeignKey('Superuser', models.DO_NOTHING, db_column='matricule', blank=True, null=True)

    class Meta:
        db_table = 'quizz'



class Sessionquizz(models.Model):
    idsession = models.AutoField(db_column='idSession', primary_key=True)  # Field name made lowercase.
    evaluation = models.BooleanField()
    datecreation = models.DateField(db_column='dateCreation')  # Field name made lowercase.
    dateexpiration = models.DateField(db_column='dateExpiration', blank=True, null=True)  # Field name made lowercase.
    matricule = models.ForeignKey('Superuser', models.DO_NOTHING, db_column='matricule')
    idquizz = models.ForeignKey(Quizz, models.DO_NOTHING, db_column='idQuizz')  # Field name made lowercase.
    timer = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'sessionQuizz'

