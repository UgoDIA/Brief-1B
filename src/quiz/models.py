from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyUserManager(BaseUserManager):
    
    def create_user(self, matricule, prenom, nom, codesecteur, password=None):
        if not prenom:
            raise ValueError("Prenom requis")
        if not nom:
            raise ValueError("nom requis")
        if not matricule:
            raise ValueError("matricule requis")
        if not codesecteur:
            raise ValueError("codesecteur requis")
        
        secteur, __ = Secteur.objects.get_or_create(
            codesecteur=codesecteur, defaults={'nomsecteur': codesecteur}
        )
        
        user=self.model(
            prenom = prenom,
            nom = nom,
            matricule = matricule,
            codesecteur = secteur
        )
        user.set_password(password)
        user.save()
        # user.save(using=self._db)
        return user
    
    def create_superuser(self, prenom, nom, matricule, codesecteur, password=None):
        user=self.create_user(
            prenom = prenom,
            nom = nom,
            matricule = matricule,
            codesecteur = codesecteur,
            password = password            
        )
        
        user.is_admin=True
        user.is_superuser=True
        # user.save(using=self._db)
        user.save()
        return user


class Secteur(models.Model):
    codesecteur = models.CharField(db_column='codesecteur', primary_key=True, max_length=10)  # Field name made lowercase.
    nomsecteur = models.CharField(db_column='nomsecteur', max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'secteur'
    
class Personnel(AbstractBaseUser): #models.Model #AbstractBaseUser
    prenom = models.CharField(verbose_name = "prenom", max_length=20)
    nom = models.CharField(verbose_name = "nom", max_length=20)
    matricule = models.CharField(verbose_name="matricule", max_length=20, primary_key=True)
    codesecteur = models.ForeignKey(Secteur, on_delete=models.CASCADE)
    
    USERNAME_FIELD="matricule"
    REQUIRED_FIELDS = ["nom", "prenom", "codesecteur"]
    
    def isSuperUser(self):
        return Superuser.objects.filter(matricule=self.matricule).exists()
    
    def isCollabUser(self):
        return Collaborateur.objects.filter(matricule=self.matricule).exists()
    
    def __str__(self):
        return '%s %s (%s)' % (self.prenom, self.nom, self.codesecteur.codesecteur) 
    
    
    objects = MyUserManager()
    
    class Meta:
        db_table = "Personnel"



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
    matricule = models.ForeignKey(Collaborateur, on_delete=models.CASCADE, db_column='matricule')
    idsession = models.ForeignKey('Sessionquizz', on_delete=models.CASCADE, db_column='idSession')  # Field name made lowercase.
    score = models.IntegerField(blank=True, null=True)
    dateparticipation = models.DateField(db_column='dateParticipation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'historique'
        unique_together = ('matricule', 'idsession',)



class Quizz(models.Model):
    idquizz = models.AutoField(db_column='idQuizz', primary_key=True)  # Field name made lowercase.
    nomfichier = models.CharField(db_column='nomFichier', max_length=30)  # Field name made lowercase.
    urlfichier = models.CharField(db_column='urlFichier', max_length=200)  # Field name made lowercase.
    codesecteur = models.ForeignKey('Secteur', on_delete=models.CASCADE, db_column='codesecteur',blank=True, null=True)  # Field name made lowercase.
    matricule = models.ForeignKey('Superuser', on_delete=models.CASCADE, db_column='matricule', blank=True, null=True)

    class Meta:
        db_table = 'quizz'



class Sessionquizz(models.Model):
    idsession = models.AutoField(db_column='idSession', primary_key=True)  # Field name made lowercase.
    evaluation = models.BooleanField()
    datecreation = models.DateField(db_column='dateCreation')  # Field name made lowercase.
    dateexpiration = models.DateField(db_column='dateExpiration', blank=True, null=True)  # Field name made lowercase.
    matricule = models.ForeignKey('Superuser', models.DO_NOTHING, db_column='matricule')
    idquizz = models.ForeignKey(Quizz, db_column='idQuizz',on_delete=models.CASCADE)  # Field name made lowercase.
    timer = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'sessionQuizz'
