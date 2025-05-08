from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse,HttpResponse
from .forms import *
from django.contrib import messages  # Importer le module messages
from .models import *
from django.core.paginator import Paginator
from django.core import serializers
from django.template.loader import get_template
from xhtml2pdf import pisa
import json
import datetime
import re

months_str = {   '01': 'Janvier',
                 '02': 'Février',
                 '03': 'Mars',
                 '04': 'Avril',
                 '05': 'Mai',
                 '06': 'Juin',
                 '07': 'Juillet',
                 '08': 'Août',
                 '09': 'Septembre',
                 '10': 'Octobre',
                 '11': 'Novembre',
                 '12': 'Décembre'}

# Fichier pour stocker les données utilisateur
fichier_utilisateur = "utilisateur.json"

def Home(request):
    return render(request,"navbar.html")

###################################################   Employe   ########################################################

def Add_Employe(request):
    if request.method == "POST":
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'L\'employé a été ajouté avec succès.')  # Ajouter un message de succès
            return redirect('/AddEmploye')
    else:
        form = EmployeForm()

    return render(request, 'add_employe.html', {'form': form})




def employe_list(request):
    rib_query = request.GET.get('rib', '')
    fullname_query = request.GET.get('fullname', '')
    address_query = request.GET.get('address', '')

    # Filtrage des employés en fonction des champs de recherche
    employes = Employe.objects.all()
    if rib_query:
        employes = employes.filter(Rib_Employe__icontains=rib_query)
    if fullname_query:
        employes = employes.filter(Fullname__icontains=fullname_query)
    if address_query:
        employes = employes.filter(Address__icontains=address_query)

    # Pagination
    paginator = Paginator(employes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'rib_query': rib_query,
        'fullname_query': fullname_query,
        'address_query': address_query,
    }

    return render(request, 'list_employe.html', context)


# Vue pour modifier un employé
def modifier_employe(request, rib):
    employe = get_object_or_404(Employe, Rib_Employe=rib)  # Récupération de l'employé à modifier

    if request.method == 'POST':
        # Associer les données POST au formulaire existant
        form = EmployeForm(request.POST, instance=employe)
        previous_url = request.POST.get('previousUrl', 'employe_list')  # Utilisation de la redirection précédente
        if form.is_valid():  # Valide les données
            # Vérification supplémentaire pour s'assurer que le RIB est unique si modifié
            new_rib = form.cleaned_data['Rib_Employe']
            if new_rib != employe.Rib_Employe and Employe.objects.filter(Rib_Employe=new_rib).exists():
                form.add_error('Rib_Employe', "Le RIB que vous avez entré existe déjà.")
            else:
                form.save()  # Enregistre les modifications dans la base de données
                messages.success(request, "L'employé a été modifié avec succès.")
                return redirect(previous_url)
    else:
        # Pré-remplissage du formulaire avec les données de l'employé
        form = EmployeForm(instance=employe)

    return render(request, 'modifier_employe.html', {'form': form, 'employe': employe})

# Vue pour supprimer un employé
def supprimer_employe(request, rib):
    employe = get_object_or_404(Employe, Rib_Employe=rib)
    #recuperer la valeur d'un input du form envoyé
    if request.method == 'POST':
        previous_url = request.POST.get('previousUrl')
        if not previous_url:  # Si previousUrl n'est pas défini, retourne à la liste des employés
            previous_url = 'employe_list'
        employe.delete()
        messages.success(request, "L'employé a été supprimé avec succès.")
        return redirect(previous_url)

###################################################   Fichier Paie   ########################################################

def ajouter_fichier_paie(request):
    
    try:
        with open(fichier_utilisateur, "r") as fichier:
            data = json.load(fichier)
            bank = data.get("bank", "")
    except FileNotFoundError:
        bank = ""
    
    if request.method == 'POST':
        form = FichierPaieForm(request.POST, bank=bank)
        verif_type= None
        type = form.data['type']
        mois = form.data['mois'].zfill(2)
        annee = form.data['annee']
        date = f"{annee}/{mois}"
        verif_type= FichierPaie.objects.filter(date=date,type=type).first()
        if verif_type:
            messages.error(request, "Un fichier de paie avec ce type et cette date existe déjà.")
            return render(request, 'ajouter_fichier_paie.html', {'form': form})
        if form.is_valid():
            if FichierPaie.objects.filter(date=form.cleaned_data['date'],type=form.cleaned_data['type']).exists():
                messages.error(request, "Ce fichier de paie existe déjà.")
                return render(request, 'ajouter_fichier_paie.html', {'form': form})
            form.save()
            messages.success(request, "Le fichier de paie a été ajouté avec succès.")
            return redirect('ajouter_fichier_paie')  # Remplacez par la vue ou page souhaitée
    else:
        form = FichierPaieForm(bank=bank)
    return render(request, 'ajouter_fichier_paie.html', {'form': form})


def fichier_paie_list(request):
    description = request.GET.get('description', '')
    date_query = request.GET.get('date', '')
    type_query = request.GET.get('type', '')

    # Filtrage des fichiers de paie
    fichiers_paie = FichierPaie.objects.all()
    
    if description:
        fichiers_paie = fichiers_paie.filter(description__icontains=description)
    if date_query:
        fichiers_paie = fichiers_paie.filter(date__icontains=date_query)
    if type_query:
        if type_query == "CPA":
            # Filtrer les fichiers de paie de type exactement CPA
            fichiers_paie = fichiers_paie.filter(type="CPA")
        elif type_query == "BADR":
            fichiers_paie = fichiers_paie.filter(type="BADR")
        else:
            fichiers_paie = fichiers_paie.filter(type__icontains=type_query)
    # Pagination
    paginator = Paginator(fichiers_paie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    context = {
        'page_obj': page_obj,
        'description': description,
        'date_query': date_query,
        'type_query': type_query,
    }

    return render(request, 'list_fichier_paie.html', context)


def delete_fichier(request, id):
    if request.method == "POST":
        fichier = get_object_or_404(FichierPaie, id=id)
        previous_url = request.POST.get('previousUrl')
        if not previous_url:  # Si previousUrl n'est pas défini, retourne à la liste des employés
            previous_url = 'list_fichier_paie'
        fichier.delete()
        messages.success(request, "Le fichier a été supprimé avec succès.")
    return redirect(previous_url)

def modifier_fichier_paie(request, id):
    fichier = get_object_or_404(FichierPaie, id=id)
    type = fichier.type
    date = fichier.date
    mois = date.split('/')[1]
    annee = date.split('/')[0]
    verif_type= None
    if request.method == "POST":
        form = FichierPaieForm(request.POST, instance=fichier)
        previous_url = request.POST.get('previousUrl', 'list_fichier_paie')  # Utilisation de la redirection précédente
        new_date= form.data['annee'] + '/' + form.data['mois'].zfill(2)
        mois = form.data['mois'].zfill(2)
        verif_type= FichierPaie.objects.filter(date=new_date,type=form.data['type']).first()

        if verif_type and verif_type.id != id:
            messages.error(request, "Un fichier de paie avec ce type et cette date existe déjà.")
            return render(request, 'modifier_fichier_paie.html', {'form': form, 'mois':mois,'annee':annee})
        annee = form.data['annee']
        if form.is_valid():
            form.save()
            messages.success(request, "Le fichier de paie a été modifié avec succès.")
            return redirect(previous_url)  # Remplacez par le nom de votre page de liste
        
    else:
        form = FichierPaieForm(instance=fichier)
        
    
    return render(request, 'modifier_fichier_paie.html', {'form': form, 'mois':mois,'annee':annee})

###################################################   Fiche Paie   ########################################################

def ajouter_fiche_paie(request):
    if request.method == 'POST':
        employe_initial = None
        fiche_paie_initial = None
        Montant_initial = None
        Libelle_initial = None
        form = FichePaieForm(request.POST)


        if form.is_valid():
            # Récupération des états de verrouillage
            lock_employe = request.POST.get("lock_employe")  # locked ou unlocked
            lock_fiche_paie = request.POST.get("lock_fiche_paie")
            lock_Montant = request.POST.get("lock_Montant")
            lock_Libelle = request.POST.get("lock_Libelle")

            # Si le champ Employé est verrouillé, conserver sa valeur
            if lock_employe == "locked":
                employe_initial = form.cleaned_data['employe']  # Valeur validée
                
            # Si le champ Fiche de Paie est verrouillé, conserver sa valeur
            if lock_fiche_paie == "locked":
                fiche_paie_initial = form.cleaned_data['fiche_paie']
                
            if lock_Montant == "locked":
                Montant_initial = form.cleaned_data['Montant']
            
            if lock_Libelle == "locked":
                Libelle_initial = form.cleaned_data['Libelle']
                

            #recuperer l'employe entré dans le formulaire
            employe_id = form.data['employe']
            #recuperer lenom de l'employe apartir de son id
            employe = Employe.objects.get(pk=employe_id)
            #recuperer la banque de l'employé
            banque = employe.Rib_Employe[0:3]
            print(banque)
            fichier_id = form.data['fiche_paie']
            fichier = FichierPaie.objects.get(pk=fichier_id)
            #recuperer le type de fichier
            type_fichier = fichier.type
            print(type_fichier)

            # Vérifier si l'employé existe dans les fiche de paie avec employe et fiche de paie
            fiche = FichePaie.objects.filter(employe=employe_id, fiche_paie=fichier_id).first()

            # verifier si l'employé peut appartenir a ce fichier
            if type_fichier == "BADR":
                if banque != "003":
                    messages.error(request, f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque n'est pas la BADR.")
                    return render(request, 'ajouter_fiche.html', {'form': form})
            elif type_fichier == "confraires_BADR":
                if banque == "003":
                    messages.error(request, f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque est la BADR.")    
                    return render(request, 'ajouter_fiche.html', {'form': form})
            # elif type_fichier == "CPA":
            #     if banque != "004":
            #         messages.error(request, f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque n'est pas la CPA.")
            #         return render(request, 'ajouter_fiche.html', {'form': form})
            # elif type_fichier == "confraires_CPA":
            #     print("confraires_CPA")
            #     if banque == "004":
            #         messages.error(request, f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque est la CPA.")
            #         return render(request, 'ajouter_fiche.html', {'form': form})


            if not fiche: 
                # Sauvegarde de la fiche de paie
                form.save()
                messages.success(request, "La fiche de paie a été ajoutée avec succès.")

                # Réinitialiser le formulaire avec les valeurs verrouillées
                form = FichePaieForm(initial={
                    'employe': employe_initial,
                    'fiche_paie': fiche_paie_initial,
                    'Montant': Montant_initial,
                    'Libelle': Libelle_initial,
                })



                context = {'form': form}
                return render(request, 'ajouter_fiche.html', context)
            else:
                # ajouter un message dans le formulaire
                messages.error(request, f"L'employe : \" {employe} \" existe deja dans la fiche de paie: \" {fichier} \" ")
        

    else:
        # Requête GET : initialiser un formulaire vide
        form = FichePaieForm()

    context = {'form': form}
    return render(request, 'ajouter_fiche.html', context)

def search_employe(request):
    query = request.GET.get('q', '')
    employes = Employe.objects.filter(Fullname__icontains=query)[:10]  # Limitez les résultats
    results = [{'id': employe.pk, 'text': employe.Rib_Employe + ' ' +employe.Fullname} for employe in employes]
    return JsonResponse({'results': results})


def search_fichier_paie(request):
    query = request.GET.get('q', '')
    fichiers = FichierPaie.objects.filter(date__icontains=query)[:10]  # Limitez les résultats
    results = [{'id': fichier.pk, 'text': fichier.date + ' ' + fichier.type + ' ' +fichier.description } for fichier in fichiers]
    return JsonResponse({'results': results})


def modifier_fiche(request, id):
    fiche = get_object_or_404(FichePaie, id=id)
    existence = None
    previous_url = request.POST.get('previousUrl', 'list_fiches')  # Utilisation de la redirection précédente
    if request.method == "POST":
        form = FichePaieForm(request.POST, instance=fiche)
        employe = Employe.objects.get(pk=form.data['employe'])

        fichier = FichierPaie.objects.get(pk=form.data['fiche_paie'])
        # Vérifier si l'employé existe dans les fiche de paie avec employe et fiche de paie
        fiche = FichePaie.objects.filter(employe=employe, fiche_paie=fichier).first()
        if fiche and fiche.id != id:
            messages.error(request, f"L'employe : \" {employe} \" existe deja dans la fiche de paie: \" {fichier} \" ")
            return render(request, 'modifier_fiche.html', {'form': form, 'fiche': fiche})
        

        if form.is_valid():
            form.save()
            messages.success(request, "La fiche de paie a été modifiée avec succès.")
            return redirect(previous_url)  # Rediriger vers la liste des fiches de paie
    else:
        form = FichePaieForm(instance=fiche)

    return render(request, 'modifier_fiche.html', {'form': form, 'fiche': fiche})


def delete_fiche(request, id):
    if request.method == "POST":
        fiche = get_object_or_404(FichePaie, id=id)
        previous_url = request.POST.get('previousUrl')
        if not previous_url:  # Si previousUrl n'est pas défini, retourne à la liste des employés
            previous_url = 'list_fiches'
        fiche.delete()
        messages.success(request, "La fiche de paie a été supprimée avec succès.")
    return redirect(previous_url)  # Rediriger vers la liste des fiches de paie


def list_fiches(request):
    # Récupération des critères de filtrage
    employe_name_query = request.GET.get('employe_name', '')
    employe_rib_query = request.GET.get('employe_rib', '')
    montant_query = request.GET.get('montant', '')
    libelle_query = request.GET.get('libelle', '')
    fichier_description_query = request.GET.get('description', '')
    fichier_date_query = request.GET.get('date', '')
    fichier_type_query = request.GET.get('type', '')

    # Filtrage des fiches de paie
    fiches = FichePaie.objects.all()
    if employe_name_query:
        fiches = fiches.filter(employe__Fullname__icontains=employe_name_query)
    if employe_rib_query:
        fiches = fiches.filter(employe__Rib_Employe__icontains=employe_rib_query)
    if montant_query:
        fiches = fiches.filter(Montant__icontains=montant_query)
    if libelle_query:
        fiches = fiches.filter(Libelle__icontains=libelle_query)
    if fichier_description_query:
        fiches = fiches.filter(fiche_paie__description__icontains=fichier_description_query)
    if fichier_date_query:
        fiches = fiches.filter(fiche_paie__date__icontains=fichier_date_query)
    if fichier_type_query:
        fiches = fiches.filter(fiche_paie__type__icontains=fichier_type_query)

    # Pagination
    paginator = Paginator(fiches, 10)  # 10 fiches par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'employe_name_query': employe_name_query,
        'employe_rib_query': employe_rib_query,
        'montant_query': montant_query,
        'libelle_query': libelle_query,
        'description_query': fichier_description_query,
        'date_query': fichier_date_query,
        'type_query': fichier_type_query,
    }

    # print("context",context)

    return render(request, 'list_fiches.html', context)

###################################################   DOWNLOAD   ########################################################


def telecharger_fichier_paie(request, fichier_id):
    fichier= FichierPaie.objects.get(id=fichier_id)
    valider_fichier,message = Valider_fichier(fichier_id)
    if not valider_fichier:
        messages.error(request, message)
        return redirect('list_fichier_paie')

    if fichier.type=="BADR" or fichier.type=="confraires_BADR": 
        return telecharger_fichier_paie_BADR(request, fichier_id)
    elif fichier.type=="CPA":
        return telecharger_fichier_paie_CPA(request, fichier_id)


def download_etats(request, id):

    # Récupérer le fichier de paie associé
    fichier = FichierPaie.objects.get(id=id)

    # Vérifier si le fichier est valide
    validite_fichier, message = Valider_fichier(fichier.id)
    if not validite_fichier:
        messages.error(request, message)
        return redirect('list_fiches')

    # Générer le PDF
    return download_pdf(request, id)
    
 ############################################################
    

def Valider_fichier(fichier_id):
    fichier= FichierPaie.objects.get(id=fichier_id)
    type_fichier = fichier.type
    fiches = FichePaie.objects.filter(fiche_paie=fichier_id)
    validite_fichier = True
    notice=""
    for f in fiches:
        employe = f.employe
        rib = employe.Rib_Employe
        banque = rib[0:3]
        if type_fichier == "BADR":
            if banque != "003":
                validite_fichier = False
                notice+=f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque n'est pas la BADR. \n"
                continue
        elif type_fichier == "confraires_BADR":
            if banque == "003":
                validite_fichier = False
                notice+=f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque est la BADR. \n"
                continue
        # elif type_fichier == "CPA":
        #     if banque != "004":
        #         validite_fichier = False
        #         notice+=f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque n'est pas la CPA. \n"
        #         continue
        # elif type_fichier == "confraires_CPA":
        #     if banque == "004":
        #         validite_fichier = False
        #         notice+=f"L'employé : \" {employe} \" ne peut pas appartenir à ce fichier de paie car sa banque est la CPA. \n"
        #         continue
        
    if notice != "":
        message = "Le fichier de paie n'est pas valide. \n" +" \n"+ notice
    else:
        message = "Le fichier de paie est valide."

    return validite_fichier, message





def telecharger_fichier_paie_CPA(request, fichier_id):
    try:
            with open(fichier_utilisateur, "r") as fichier:
                data = json.load(fichier)
    except FileNotFoundError:
            data = {}

    try:
        # Récupérer la fiche de paie correspondante
        Rib_User = data.get("rib", "")
        Fullname_User = data.get("fullname", "")
        Address_User = data.get("address", "")
        Bank_User = data.get("bank", "")
        
        
        fiches = FichePaie.objects.filter(fiche_paie=fichier_id)
        fichier= FichierPaie.objects.get(id=fichier_id)
        mois = fichier.date.split('/')[1]
        annee = fichier.date.split('/')[0]
        i=0
        montant_total=0
        #recuperer le jour seulement de la date actuelle
        
        date = datetime.datetime.now()
        jour = date.strftime("%d").zfill(2)
        if fichier_id<1000:
            reference=f"{fichier_id}".zfill(3)
        else:
            reference=f"123"

        # Générer le contenu du fichier texte
        contenu = ""
        for f in fiches:
            i+=1
            dixpremiers = str(i).zfill(6)+mois+annee[2:]
            # remplir les champs pour avoir une longueur fixe
            Fullname = f.employe.Fullname
            Adresse = f.employe.Address
            Libelle = f.Libelle
            lengthFullname = 50 - len(f.employe.Fullname)
            lengthAdresse = 70 - len(f.employe.Address)
            lengthLibelle = 70 - len(f.Libelle)
            montant_total=montant_total+int(f.Montant)
            Montant = f.Montant.zfill(15)
            contenu += f"{dixpremiers}1{f.employe.Rib_Employe}    {Fullname}{lengthFullname*' '}{Adresse}{lengthAdresse*' '}{Montant}{Libelle}{lengthLibelle*' '}{80*' '}\n"
        nb_fiches = str(len(fiches)).zfill(6)
        montant_total=str(montant_total).zfill(16)
        premiere_ligne = f"VIRM{Bank_User}01001{Rib_User}    {Fullname_User}{' '*(50-len(Fullname_User))}{Address_User}{' '*(70-len(Address_User))}{annee}{mois}{jour}{reference}{nb_fiches}{montant_total}{31*' '}\n"
        contenu+=f"FVIR{96*' '}"
        contenu = premiere_ligne + contenu
        # Créer une réponse HTTP avec le fichier texte
        response = HttpResponse(contenu, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename=fiche_paie_{mois}_{annee}__{fichier.type}.txt"

        return response

    except FichePaie.DoesNotExist:
        return HttpResponse("Fiche de paie introuvable.", status=404)

#############################################################    
def telecharger_fichier_paie_BADR(request, fichier_id):
    try:
            with open(fichier_utilisateur, "r") as fichier:
                data = json.load(fichier)
    except FileNotFoundError:
            data = {}

    try:
        # Récupérer la fiche de paie correspondante
        Rib_User = data.get("rib", "")
        Fullname_User = data.get("fullname", "")
        Address_User = data.get("address", "")
        Bank_User = data.get("bank", "")
        
        
        fiches = FichePaie.objects.filter(fiche_paie=fichier_id)
        fichier= FichierPaie.objects.get(id=fichier_id)
        mois = fichier.date.split('/')[1]
        annee = fichier.date.split('/')[0]
        i=0
        montant_total=0
        #recuperer le jour seulement de la date actuelle
        
        date = datetime.datetime.now()
        jour = date.strftime("%d").zfill(2)
        reference=f"{fichier_id}".zfill(3)

        # Générer le contenu du fichier texte
        contenu = ""
        for f in fiches:
            i+=1
            dixpremiers = str(i).zfill(6)+mois+annee[2:]
            # remplir les champs pour avoir une longueur fixe
            Fullname = f.employe.Fullname
            Adresse = f.employe.Address
            Libelle = f.Libelle
            lengthFullname = 50 - len(f.employe.Fullname)
            lengthAdresse = 70 - len(f.employe.Address)
            lengthLibelle = 70 - len(f.Libelle)
            montant_total=montant_total+int(f.Montant)
            Montant = f.Montant.zfill(15)
            contenu += f"{dixpremiers}1{f.employe.Rib_Employe}    {Fullname}{lengthFullname*' '}{Adresse}{lengthAdresse*' '}{Montant}{Libelle}{lengthLibelle*' '}{80*' '}\n"
        nb_fiches = str(len(fiches)).zfill(6)
        montant_total=str(montant_total).zfill(16)
        premiere_ligne = f"VIRM{Bank_User}01001{Rib_User}    {Fullname_User}{' '*(50-len(Fullname_User))}{Address_User}{' '*(70-len(Address_User))}{annee}{mois}{jour}{reference}{nb_fiches}{montant_total}{31*' '}\n"
        contenu+=f"FVIR{96*' '}"
        contenu = premiere_ligne + contenu
        # Créer une réponse HTTP avec le fichier texte
        response = HttpResponse(contenu, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename=fiche_paie_{mois}_{annee}__{fichier.type}.txt"

        return response

    except FichePaie.DoesNotExist:
        return HttpResponse("Fiche de paie introuvable.", status=404)



def download_pdf(request,id):
    fichier= FichierPaie.objects.get(id=id)
    fiches = FichePaie.objects.filter(fiche_paie=id)
    template_path = 'etats_pdf.html'
    i=1
    lignes = []
    mois=fichier.date.split('/')[1]
    annee=fichier.date.split('/')[0]
    mois=months_str[mois]

    try:
        with open(fichier_utilisateur, "r") as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        data = {}

    try:
        # Récupérer la fiche de paie correspondante
        Rib_User = data.get("rib", "")
        Fullname_User = data.get("fullname", "")
        Address_User = data.get("address", "")
        Bank_User = data.get("bank", "")
    except FichePaie.DoesNotExist:
        return HttpResponse("Fiche de paie introuvable.", status=404)


    for fiche in fiches:
        employe= fiche.employe.Fullname
        rib= fiche.employe.Rib_Employe
        montant= fiche.Montant
        # diviser le montant sur deux parties jusqua le deux derniers chiffres
        newmontant = montant[:-2] + ',' + montant[-2:]
        

        



        ligne = {
            'numero': i,
            'employe': employe,
            'rib': rib,
            'montant': newmontant,
            
        }
    
        i+=1
        lignes.append(ligne)


    
    context = {'lignes': lignes, 'mois': mois, 'annee': annee,'Fullname_User': Fullname_User,}

    #Charger le template HTML
    template = get_template(template_path)
    html = template.render(context)

    # Créer la réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="etats_{mois}_{annee}.pdf"'

    # Générer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Une erreur s\'est produite lors de la génération du PDF')
    return response




###################################################   User   ########################################################

# Vue pour afficher le formulaire
def formulaire_utilisateur(request):
    if request.method == "POST":
        # Récupération des données envoyées par le formulaire
        data = {
            "rib": request.POST.get("rib"),
            "fullname": request.POST.get("fullname"),
            "address": request.POST.get("address"),
            "bank": request.POST.get("bank"),
        }
        # Sauvegarde dans le fichier JSON
        with open(fichier_utilisateur, "w") as fichier:
            json.dump(data, fichier)

        messages.success(request, "Données enregistrées avec succès !")
    else:
        # Affichage des données existantes
        try:
            with open(fichier_utilisateur, "r") as fichier:
                data = json.load(fichier)
        except FileNotFoundError:
            data = {}

    context = {
        "rib": data.get("rib", ""),
        "fullname": data.get("fullname", ""),
        "address": data.get("address", ""),
        "bank": data.get("bank", ""),
    }
    # Affichage du formulaire
    return render(request, "add_user.html",context)

###################################################   IMPORT   ########################################################

def importer_fichier_txt(request):
    if request.method == 'POST' and request.FILES.get('fichier_txt'):
        fichier = request.FILES['fichier_txt']
        contenu = fichier.read().decode('utf-8')  # Décoder le contenu en UTF-8
        annee = ""
        mois = ""
        notice=""
        i=0
        invalid=False
        nonvide=False
        existedeja=False
        TypeBanqueNVligne =""
        banque=""
        try:
            with open(fichier_utilisateur, "r") as fichier:
                data = json.load(fichier)
        except FileNotFoundError:
            data = {}

        try:
            # Récupérer la fiche de paie correspondante
            Rib_User = data.get("rib", "")
            Fullname_User = data.get("fullname", "")
            Address_User = data.get("address", "")
            Bank_User = data.get("bank", "")
        except FichePaie.DoesNotExist:
            return HttpResponse("Fiche de paie introuvable.", status=404)
        
        # Logique pour traiter le contenu du fichier
        #Traiter le contenu du fichier ligne par ligne
        lignes = contenu.splitlines()
        fiche_paie = None
        for ligne in lignes:
            invalid=False
            i+=1
            if i==1 and len(ligne) == 220:
                debut = ligne[0:4]
                if debut != "VIRM":
                    notice+="La premiere ligne n'est pas valide.\n"
                    break
                
                
                annee = ligne[156:160]
                mois = ligne[160:162]
                banquePayeur=ligne[4:7]
                #banque = ligne[4:7]
                
                

                # si annee nest pas un nombre qui contient 4 chiffres ou plus grand que 1950
                if not annee.isdigit() or len(annee) != 4 or int(annee) < 1950:
                    notice+="L'année de la premiere ligne n'est pas valide.\n"
                    break

                # si mois nest pas un nombre qui contient 2 chiffres ou plus grand que 1 et plus petit que 12
                if not mois.isdigit() or len(mois) != 2 or int(mois) < 1 or int(mois) > 12:
                    notice+="Le mois de la premiere ligne n'est pas valide.\n"
                    break

                # si la banque n'est pas valide
                if not banquePayeur.isdigit() or len(banquePayeur) != 3:
                    notice+="La banque du donneur d'ordre n'est pas valide.\n"
                    break              
                continue
            elif i==1 and len(ligne) != 220:
                notice+="La premiere ligne n'est pas valide, elle doit contenir 220 caracteres\n"
                continue


            if len(ligne) == 100:
                break
            
            banque = ligne[11:14]
            if i==2:

                if banquePayeur=="003":
                    if banque == "003":
                        typeFichier = "BADR"
                    else:
                        typeFichier = "confraires_BADR"
                elif banquePayeur=="004":
                    # if banque == "004":
                    typeFichier = "CPA"
                    # else:
                    #     typeFichier = "confraires_CPA"
                else:
                    notice+="La banque du donneur d'ordre n'est pas valide. Veuillez inserer un fichier avec un compte donneur d'ordre appartenant a la BADR ou la CPA.\n"
                    break

                # TypeBanqueNVligne=typeFichier

                # Vérifier si la fichier de paie existe déjà
                fiche_paie = FichierPaie.objects.filter(date=f"{annee}/{mois}", type=typeFichier).first()
                if not fiche_paie:
                    try:
                        fiche_paie = FichierPaie(
                            date=f"{annee}/{mois}",
                            type=typeFichier,
                            description=f"Fiche de paie {mois} {annee}"
                        )
                        fiche_paie.save()
                        if not fiche_paie.id:
                            raise ValueError("L'enregistrement de FichierPaie a échoué.")
                    except Exception as e:
                        notice += f"Erreur lors de la création du fichier de paie : {e}\n"
                        invalid = True
                        break
                else:
                    notice += f"Le fichier pour {fiche_paie.date} avec le type {typeFichier} existe déjà.\n"
                    existedeja = True


            invalid=False
            rib = ligne[11:31]
            fullname = ligne[35:85].strip()
            address = ligne[85:155].strip()
            montant = ligne[155:170].lstrip('0')
            libelle = ligne[170:240].strip()
            mois = ligne[6:8]
            annee = ligne[8:10]
            
            

            if typeFichier =="BADR":
                if banque != "003":
                    notice += f"La banque de l'employé {fullname} de la ligne numero {i} du fichier, n'est pas valide. cet employé doit etre situé dans le type \" confraires_BADR \" \n"
                    invalid = True
                    continue
            elif typeFichier=="confraires_BADR":
                if banque == "003":
                    notice += f"La banque de l'employé {fullname} de la ligne numero {i} du fichier, n'est pas valide. cet employé doit etre situé dans le type \" BADR \" \n"
                    invalid = True
                    continue
            # elif typeFichier=="CPA":
            #     if banque != "004":
            #         notice += f"La banque de l'employé {fullname} de la ligne numero {i} du fichier, n'est pas valide. cet employé doit etre situé dans le type \" confraires_CPA \" \n"
            #         invalid = True
            #         continue
            # elif typeFichier=="confraires_CPA":
            #     if banque == "004":
            #         notice += f"La banque de l'employé {fullname} de la ligne numero {i} du fichier, n'est pas valide. cet employé doit etre situé dans le type \" CPA \" \n"
            #         invalid = True
            #         continue

            # if typeFichier != TypeBanqueNVligne:
            #     notice += f"Type de fichier invalide. L'employé {fullname} a la ligne: {i} du fichier,n'appartient pas a ce type de fichier.\n"
            #     invalid = True
            #     break

            if mois not in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
                invalid=True
                notice+=f"Le mois {mois} "
            if not annee.isdigit():
                invalid=True
                notice+=f"L'année {annee} "

            if not rib.isdigit() or len(rib) != 20:
                invalid=True
                notice+=f"Le RIB {rib},"
            
            if not re.match(r'^[A-Za-zÀ-ÿ0-9\s]+$', fullname) or len(fullname) > 50:
                invalid=True
                notice+=f" Le nom {fullname},"
            if not re.match(r'^[A-Za-zÀ-ÿ0-9\s]+$', address) or len(address) > 70:
                invalid=True
                notice+=f" L'adresse {address},"
            if not re.match(r'^[0-9]+$', montant) or len(montant) > 15:
                invalid=True
                notice+=f" Le montant {montant},"
            if not re.match(r'^[A-Za-zÀ-ÿ0-9\s]+$', libelle) or len(libelle) > 70:
                invalid=True
                notice+=f" Le libelle {libelle},"
            
            if invalid:
                notice+=f" de l'employé {rib} {fullname} de la ligne numero {i} du fichier, n'est pas valide.\n"
                continue

            # Vérifier si l'employé existe déjà
            employe = Employe.objects.filter(Rib_Employe=rib).first()
            if not employe:
                employe = Employe(Rib_Employe=rib, Fullname=fullname, Address=address)
                nonvide=True
                employe.save()
            else:
                notice+=f"L'employé {employe.Fullname} avec le RIB {employe.Rib_Employe} existe déjà.\n"
                nonvide=True
            
            # Vérifier si la fiche de paie existe déjà
            fiche = FichePaie.objects.filter(employe=employe, fiche_paie=fiche_paie).first()
            if not fiche:
                fiche = FichePaie(employe=employe, fiche_paie=fiche_paie, Montant=montant, Libelle=libelle)
                fiche.save()
                nonvide=True
            else:
                notice+=f"La fiche de paie pour {employe.Fullname} et le mois {fiche_paie.date} existe déjà.\n"
                nonvide=True


        #if nonvide est faux alors supprimer le fichier de paie    
        if not nonvide and fiche_paie and not existedeja:
            notice+=f"Le fichier de paie pour le mois {fiche_paie.date} est vide donc il n'a pas été ajouté.\n"
            fiche_paie.delete()


        if notice:

            messages.warning(request, notice)
            
        else:
            messages.success(request, f"Fichier {fichier.name} importé sans erreur.")
            
    return redirect('list_fichier_paie')



def clone_fichier_paie(request):
    if request.method == 'POST':
        # enlevez le champ original_fichier_id du request.POST
        request_copy = request.POST.copy()
        request_copy.pop('original_fichier_id')
        form = FichierPaieForm(request_copy)
        if form.is_valid():
            try:
                original_fichier_id = request.POST.get('original_fichier_id')
                mois = request.POST.get('mois')
                mois = mois.zfill(2)
                annee = request.POST.get('annee')
                type = request.POST.get('type')
                description = request.POST.get('description')

            # Récupérer le fichier d'origine
                original_fichier = get_object_or_404(FichierPaie, id=original_fichier_id)

            # Créer un nouveau fichier
                new_fichier = FichierPaie.objects.create(
                    date=f"{annee}/{mois}",
                    type=type,
                    description=description
                )

            # Cloner les fiches de paie associées
                fiches = FichePaie.objects.filter(fiche_paie=original_fichier)
                Libelle=f"fiche de paie du {mois} {annee}"
                for fiche in fiches:
                    FichePaie.objects.create(
                        employe=fiche.employe,
                        fiche_paie=new_fichier,
                        Montant=fiche.Montant,
                        Libelle=Libelle
                    )

                messages.success(request, f"Le fichier de paie {mois}/{annee} a été cloné avec succès.")
                return redirect('list_fichier_paie')
            except FichierPaie.DoesNotExist:
                form.add_error(None, "Le fichier d'origine spécifié est introuvable.")
        else:
        


            description = request.GET.get('description', '')
            date_query = request.GET.get('date', '')
            type_query = request.GET.get('type', '')

            # Filtrage des fichiers de paie
            fichiers_paie = FichierPaie.objects.all()
            
            if description:
                fichiers_paie = fichiers_paie.filter(description__icontains=description)
            if date_query:
                fichiers_paie = fichiers_paie.filter(date__icontains=date_query)
            if type_query:
                fichiers_paie = fichiers_paie.filter(type__icontains=type_query)
            # Pagination
            paginator = Paginator(fichiers_paie, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            mois = request.POST.get('mois')
            description = request.POST.get('description')


            context = {
                'page_obj': page_obj,
                'description': description,
                'date_query': date_query,
                'type_query': type_query,
                'formpopup': form,
                'show_popup': True,
                'mois':mois,
                'description':description,
                'original_fichier_id': request.POST.get('original_fichier_id'),
            }

            return render(request, 'list_fichier_paie.html', context)
    return redirect('list_fichier_paie')