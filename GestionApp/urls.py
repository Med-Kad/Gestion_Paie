from django.urls import path, include
from .views import *

urlpatterns = [

path('AddEmploye/', Add_Employe, name='Add_Employe'),
path('', Home, name='Home'),
path('employe_list/', employe_list, name='employe_list'),
path('modifier-employe/<str:rib>/', modifier_employe, name='modifier_employe'),
path('supprimer-employe/<str:rib>/', supprimer_employe, name='supprimer_employe'),
path('fiche_paie/', ajouter_fichier_paie, name='ajouter_fichier_paie'),
path('list_fichier_paie/', fichier_paie_list, name='list_fichier_paie'),
path('delete-fichier/<int:id>/', delete_fichier, name='delete_fichier'),
path('modifier-fichier/<int:id>/', modifier_fichier_paie, name='modifier_fichier_paie'),
path('select2/', include('django_select2.urls')),  # Ajout pour Select2
path('ajouter_fiche_paie/', ajouter_fiche_paie, name='ajouter_fiche_paie'),
path('search_employe/', search_employe, name='search_employe'),
path('search_fichier_paie/', search_fichier_paie, name='search_fichier_paie'),
path('list_fiches/', list_fiches, name='list_fiches'),
path('delete-fiche/<int:id>/', delete_fiche, name='delete_fiche'),
path('modifier-fiche/<int:id>/', modifier_fiche, name='modifier_fiche'),
path('telecharger/<int:fichier_id>/', telecharger_fichier_paie, name='telecharger_fichier_paie'),
path("formulaire/", formulaire_utilisateur, name="enregistrer_utilisateur"),
path('importer-fichier-txt/', importer_fichier_txt, name='importer_fichier_txt'),
path('clone_fichier_paie/', clone_fichier_paie, name='clone_fichier_paie'),
path('fichier/pdf/<int:id>/', download_etats, name='download_etats'),

]