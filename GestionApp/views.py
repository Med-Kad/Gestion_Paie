from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse,HttpResponse
from .forms import *
from django.contrib import messages  # Importer le module messages
from .models import *
from django.core.paginator import Paginator
from django.core import serializers
import json
import datetime

# Fichier pour stocker les données utilisateur
fichier_utilisateur = "utilisateur.json"

# Create your views here.
def firstfct(request):
    return render(request,"add_employe.html")


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
        if form.is_valid():  # Valide les données
            # Vérification supplémentaire pour s'assurer que le RIB est unique si modifié
            new_rib = form.cleaned_data['Rib_Employe']
            if new_rib != employe.Rib_Employe and Employe.objects.filter(Rib_Employe=new_rib).exists():
                form.add_error('Rib_Employe', "Le RIB que vous avez entré existe déjà.")
            else:
                form.save()  # Enregistre les modifications dans la base de données
                messages.success(request, "L'employé a été modifié avec succès.")
                return redirect('employe_list')  # Redirige vers la liste des employés
    else:
        # Pré-remplissage du formulaire avec les données de l'employé
        form = EmployeForm(instance=employe)

    return render(request, 'modifier_employe.html', {'form': form, 'employe': employe})

# Vue pour supprimer un employé
def supprimer_employe(request, rib):
    employe = get_object_or_404(Employe, Rib_Employe=rib)
    if request.method == 'POST':
        employe.delete()
        messages.success(request, "L'employé a été supprimé avec succès.")
        return redirect('employe_list')

###################################################   Fichier Paie   ########################################################

def ajouter_fichier_paie(request):
    if request.method == 'POST':
        form = FichierPaieForm(request.POST)
        if form.is_valid():
            if FichierPaie.objects.filter(date=form.cleaned_data['date'],type=form.cleaned_data['type']).exists():
                messages.error(request, "Ce fichier de paie existe déjà.")
                return render(request, 'ajouter_fichier_paie.html', {'form': form})
            form.save()
            messages.success(request, "Le fichier de paie a été ajouté avec succès.")
            return redirect('ajouter_fichier_paie')  # Remplacez par la vue ou page souhaitée
    else:
        form = FichierPaieForm()
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
        fichier.delete()
        messages.success(request, "Le fichier a été supprimé avec succès.")
    return redirect('list_fichier_paie')

def modifier_fichier_paie(request, id):
    fichier = get_object_or_404(FichierPaie, id=id)
    date = fichier.date
    mois = date.split('/')[1]
    annee = date.split('/')[0]
    if request.method == "POST":
        form = FichierPaieForm(request.POST, instance=fichier)
        mois = form.data['mois'].zfill(2)
        
        annee = form.data['annee']
        if form.is_valid():
            form.save()
            messages.success(request, "Le fichier de paie a été modifié avec succès.")
            return redirect('list_fichier_paie')  # Remplacez par le nom de votre page de liste
        
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

            fichier_id = form.data['fiche_paie']
            fichier = FichierPaie.objects.get(pk=fichier_id)

            # Vérifier si l'employé existe dans les fiche de paie avec employe et fiche de paie
            fiche = FichePaie.objects.filter(employe=employe_id, fiche_paie=fichier_id).first()

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
    if request.method == "POST":
        form = FichePaieForm(request.POST, instance=fiche)
        if form.is_valid():
            form.save()
            messages.success(request, "La fiche de paie a été modifiée avec succès.")
            return redirect('list_fiches')  # Rediriger vers la liste des fiches de paie
    else:
        form = FichePaieForm(instance=fiche)

    return render(request, 'modifier_fiche.html', {'form': form, 'fiche': fiche})


def delete_fiche(request, id):
    if request.method == "POST":
        fiche = get_object_or_404(FichePaie, id=id)
        fiche.delete()
        messages.success(request, "La fiche de paie a été supprimée avec succès.")
    return redirect('list_fiches')  # Rediriger vers la liste des fiches de paie


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
        'employe_query': employe_name_query,
        'employe_rib_query': employe_rib_query,
        'montant_query': montant_query,
        'libelle_query': libelle_query,
        'fichier_description_query': fichier_description_query,
        'fichier_date_query': fichier_date_query,
        'fichier_type_query': fichier_type_query,
    }

    return render(request, 'list_fiches.html', context)

###################################################   DOWNLOAD   ########################################################


def telecharger_fichier_paie(request, fichier_id):
    
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
            #contenu += f"Employé: {f.employe}, Montant: {f.Montant}, Libellé: {f.Libelle}\n"
        nb_fiches = str(len(fiches)).zfill(6)
        montant_total=str(montant_total).zfill(16)
        premiere_ligne = f"VIRM{Bank_User}01001{Rib_User}    {Fullname_User}{' '*(50-len(Fullname_User))}{Address_User}{' '*(70-len(Address_User))}{annee}{mois}{jour}{reference}{nb_fiches}{montant_total}{31*' '}\n"
        contenu+=f"FVIR{96*' '}"
        contenu = premiere_ligne + contenu
        # Créer une réponse HTTP avec le fichier texte
        response = HttpResponse(contenu, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename=fiche_paie_{fichier_id}.txt"

        return response

    except FichePaie.DoesNotExist:
        return HttpResponse("Fiche de paie introuvable.", status=404)



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
        #return JsonResponse({"message": "Données enregistrées avec succès !"})
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
        # Logique pour traiter le contenu du fichier
        #Traiter le contenu du fichier ligne par ligne
        lignes = contenu.splitlines()
        for ligne in lignes:
            if len(ligne) == 220:
                annee = ligne[156:160]
                mois = ligne[160:162]
                banque = ligne[4:7]
                if banque == "003":
                    typeFichier = "BADR"
                else:
                    typeFichier = "confraires"
                # Vérifier si la fichier de paie existe déjà
                fiche_paie = FichierPaie.objects.filter(date=f"{annee}/{mois}",type=typeFichier).first()
                if not fiche_paie:
                    
                    fiche_paie = FichierPaie(date=f"{annee}/{mois}",type=typeFichier ,description=f"Fiche de paie {mois} {annee}")
                    fiche_paie.save()
                
                else:
                    notice+=f"Le fichier pour {fiche_paie.date} avec le type {typeFichier} existe déjà.\n"
                
                continue
            if len(ligne) == 100:
                break


            rib = ligne[11:31]
            fullname = ligne[35:85].strip()
            address = ligne[85:155].strip()
            montant = ligne[155:170].lstrip('0')
            libelle = ligne[170:240].strip()

            # Vérifier si l'employé existe déjà
            employe = Employe.objects.filter(Rib_Employe=rib).first()
            if not employe:
                employe = Employe(Rib_Employe=rib, Fullname=fullname, Address=address)
                employe.save()
            else:
                notice+=f"L'employé {employe.Fullname} avec le RIB {employe.Rib_Employe} existe déjà.\n"
            
            # Vérifier si la fiche de paie existe déjà
            fiche = FichePaie.objects.filter(employe=employe, fiche_paie=fiche_paie, Montant=montant).first()
            if not fiche:
                fiche = FichePaie(employe=employe, fiche_paie=fiche_paie, Montant=montant, Libelle=libelle)
                fiche.save()
            else:
                notice+=f"La fiche de paie pour {employe.Fullname} et le mois {fiche_paie.date} existe déjà.\n"
            
        if notice:

            messages.warning(request, notice)
            
        else:
            messages.success(request, f"Fichier {fichier.name} importé avec succès.")
            return redirect('list_fichier_paie')  # Redirige vers la liste des fichiers de paie

    return redirect('list_fichier_paie')


