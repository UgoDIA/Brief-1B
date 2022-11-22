from django.urls import path, re_path
from . import views

urlpatterns = [
    path('accueil', views.pa1, name='accueilCollab'),
    path('session/<int:idsession>', views.ce, name="conditionExamen"),
    path('eval-quiz', views.initQuiz, name="quizReal"),
    path('train-quiz', views.trainquizz, name="trainQ"),
    re_path(r'^nextQuestion$', views.nextQuestion),
    path("score",views.score,name="score"),
    path('page1', views.page1, name="p1"),
    re_path(r'^incremente$', views.incremente),
    path('page2',views.page2,name="p2"),
]