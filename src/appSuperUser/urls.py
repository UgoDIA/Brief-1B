from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    path('gestion-session', views.tbd, name='tbd'),
    path('uploadQuizz/', views.uploadQuizz, name='uploadQuizz'),
    path('ajout-personnel', views.addDataInDB, name='ajoutEmp'),
    re_path(r'^addDataInDB$', views.addDataInDB, name='addDataInDB'),
    path('accueil', views.pa, name='pa'),
    path('addsession/',views.addS, name='addS'),
    path('addsession/addrecord/', views.addrecord, name='addrecord'),
    path('delete/<int:idsession>', views.deleteS, name='deleteS'),
    path('modification/<int:idsession>',views.modificationS,name='modification'),
    path('modification/updaterecord/<int:idsession>',views.updaterecord,name='updaterecord'),
    path('assigner/<int:idsession>',views.assigner,name='assigner'),
    path('assigner/delete/<int:idhisto>', views.deleteC, name='deleteC'),
    path('assigner/ajouter/<str:matricule>', views.ajouter, name='ajouter'),
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)