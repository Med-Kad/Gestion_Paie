from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
import calendar
from django_select2.forms import *

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['Rib_Employe', 'Fullname', 'Address']
    
    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        # Validation pour Rib_Employe
        rib = cleaned_data.get('Rib_Employe')
        if rib:
            # Vérifie la longueur du RIB
            if len(rib) > 20:
                errors.setdefault('Rib_Employe', []).append("Le RIB ne doit pas depasser 20 chiffres.")
            if len(rib) < 20:
                errors.setdefault('Rib_Employe', []).append("Le RIB doit contenir 20 chiffres.")
            # Vérifie le format du RIB
            if not re.match(r'^\d{20}$', rib):
                errors.setdefault('Rib_Employe', []).append("Le format de RIB est invalide, inserez des chiffres seulement.")

            # Vérifie l'unicité du RIB (uniquement si le formulaire est pour un ajout ou une modification avec un RIB modifié)
            if self.instance and self.instance.Rib_Employe != rib:
                if Employe.objects.filter(Rib_Employe=rib).exists():
                    errors.setdefault('Rib_Employe', []).append("Ce RIB est déjà enregistré.")


        # Validation pour Fullname
        fullname = cleaned_data.get('Fullname')
        if fullname:
            if len(fullname) > 50:
                errors.setdefault('Fullname', []).append("Le nom complet ne doit pas dépasser 50 caractères.")
            if not re.match(r'^[0-9a-zA-Z ]*$', fullname):
                errors.setdefault('Fullname', []).append("Le nom complet est invalide, il doit contenir des lettres et des chiffres seulement.")

        # Validation pour Address
        address = cleaned_data.get('Address')
        if address:
            if len(address) > 70:
                errors.setdefault('Address', []).append("L'adresse ne doit pas dépasser 70 caractères.")
            if not re.match(r'^[0-9a-zA-Z ]*$', address):
                errors.setdefault('Address', []).append("L'adresse est invalide, elle doit contenir des lettres et des chiffres seulement.")

        # Si des erreurs existent, les ajouter à chaque champ correspondant
        if errors:
            for field, field_errors in errors.items():
                self.add_error(field, ValidationError(field_errors))

        return cleaned_data

    
class FichierPaieForm(forms.ModelForm):

    class Meta:
        model = FichierPaie
        fields = ['mois', 'annee', 'type', 'description']

    mois = forms.ChoiceField(
        choices=[(str(i), f"{i}: {calendar.month_name[i]}") for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'bg-gray-300 text-black w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )

    annee = forms.CharField(

        widget=forms.TextInput(attrs={'class': 'bg-gray-300 text-black w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )

    type = forms.ChoiceField(
        choices=FichierPaie.TYPE_CHOICES,
        initial='BADR',
        widget=forms.Select(attrs={'class': 'bg-gray-300 text-black w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )

    description = forms.CharField(
        required=False,
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'bg-gray-300 text-black w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    def clean(self):
        cleaned_data = super().clean()
        mois = cleaned_data.get('mois')
        annee = cleaned_data.get('annee')
        description = cleaned_data.get('description')
        errors = {}
        
        if annee:
            if len(annee) != 4:
                errors.setdefault('annee', []).append("L'année doit contenir 4 chiffres.")
            if not re.match(r'^\d{4}$', annee):
                errors.setdefault('annee', []).append("Le format de l'année est invalide, inserez 4 chiffres seulement.")
            else:
                if int(annee)<1950:
                    errors.setdefault('annee', []).append("L'année doit être supérieure à 1950.")

        if description:
            if len(description) > 50:
                errors.setdefault('description', []).append("La description ne doit pas dépasser 50 caractères.")
            if not re.match(r'^[0-9a-zA-Z ]*$', description):
                errors.setdefault('description', []).append("La description est invalide, elle doit contenir des lettres et des chiffres seulement.")


        # Si des erreurs existent, les ajouter à chaque champ correspondant
        if errors:
            for field, field_errors in errors.items():
                self.add_error(field, ValidationError(field_errors))

        # Vérifier que le mois et l'année sont présents et concaténer
        if mois and annee:
            date = f"{annee}/{mois.zfill(2)}"  # Ajouter un zéro devant si le mois est inférieur à 10
            cleaned_data['date'] = date
        return cleaned_data

    def save(self, commit=True):
        # Assurez-vous que 'date' est bien assignée avant de sauvegarder l'objet
        instance = super().save(commit=False)  # Crée l'instance sans l'enregistrer pour l'instant
        if 'date' in self.cleaned_data:
            instance.date = self.cleaned_data['date']  # Assignation explicite de la date
        if commit:
            instance.save()  # Enregistrement dans la base de données
        return instance
    
#     

class FichePaieForm(forms.ModelForm):
    
    employe = forms.ModelChoiceField(
        queryset=Employe.objects.all(),  # Initialement vide, rempli via AJAX
        widget=ModelSelect2Widget(
            model=Employe,
            search_fields=['Fullname__icontains'],  # Recherche dynamique par nom
            attrs={
                'class': 'select2',
                'data-placeholder': 'Rechercher un employé...',
                'data-minimum-input-length': 0,
                'data-ajax--url': '/search_employe/',  # Fournir explicitement l'URL
            },
        )
    )

    fiche_paie = forms.ModelChoiceField(
        queryset=FichierPaie.objects.all(),  # Initialement vide, rempli via AJAX
        widget=ModelSelect2Widget(
            model=FichierPaie,
            search_fields=['description__icontains'],  # Recherche dynamique par description
            attrs={
                'class': 'select2',
                'data-placeholder': 'Rechercher un fichier de paie...',
                'data-minimum-input-length': 0,
                'data-ajax--url': '/search_fichier_paie/',
            },
        )
    )
    
    class Meta:
        model = FichePaie
        fields = ['employe', 'fiche_paie', 'Montant', 'Libelle']




    Montant = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-300 text-black w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    Libelle = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-300 text-black w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        # Validation pour Montant
        montant = cleaned_data.get('Montant')
        if montant:
            if not re.match(r'^[0-9]*$', montant):
                errors.setdefault('Montant', []).append("Le montant est invalide, il doit contenir des chiffres seulement.")
            elif int(montant) >= 100000000 :
                errors.setdefault('Montant', []).append("Le montant ne doit depasser 100000000.")
        # Validation pour Libelle
        libelle = cleaned_data.get('Libelle')
        if libelle:
            if len(libelle) > 70:
                errors.setdefault('Libelle', []).append("Le libellé ne doit pas dépasser 70 caractères.")
            if not re.match(r'^[0-9a-zA-Z ]*$', libelle):
                errors.setdefault('Libelle', []).append("Le libellé est invalide, il doit contenir des lettres et des chiffres seulement.")

        # Si des erreurs existent, les ajouter à chaque champ correspondant
        if errors:
            for field, field_errors in errors.items():
                self.add_error(field, ValidationError(field_errors))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)  # Crée l'instance sans l'enregistrer pour l'instant
        if commit:
            instance.save()  # Enregistrement dans la base de données
        return instance