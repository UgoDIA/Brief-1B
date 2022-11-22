from quiz.models import Personnel, Collaborateur, Superuser, Secteur, Quizz
# Quizz.objects.all().delete()
Collaborateur.objects.all().delete()
Superuser.objects.all().delete()
Secteur.objects.all().delete()
Personnel.objects.all().delete()