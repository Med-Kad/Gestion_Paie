from django.db import models
from django.core.validators import *
from django.core.exceptions import ValidationError
from django import forms

# Create your models here.

class Employe(models.Model):
    Rib_Employe= models.CharField(
        max_length=1000,
        validators=[RegexValidator(r'^\d{20}$')],
        unique=True)
    Fullname = models.CharField(max_length=1000,blank=False
                                 ,validators=[RegexValidator(r'^[0-9a-zA-Z ]*$')]
                                )
    Address = models.CharField(max_length=1000,blank=False
                                ,validators=[RegexValidator(r'^[0-9a-zA-Z ]*$')]
                               )
    
    error_messages = {
            'Rib_Employe': {
                'required': "Le RIB est obligatoire.",
                'unique': "Ce RIB est déjà enregistré.",
                'max_length': "Le RIB ne doit pas dépasser 20 caractères",
                'invalid': "Le format de RIB est invalide, Inserez 20 chiffres."
            },
            'Fullname': {
                'required': "Le nom complet est obligatoire.",
                'max_length': "Le nom complet ne doit pas dépasser 50 caractères.",
                'invalid': "Le nom complet est invalide, il doit contenir des lettres et des chiffres seulement."
            },
            'Address': {
                'required': "L'adresse est obligatoire.",
                'max_length': "L'adresse ne doit pas dépasser 70 caractères.",
                'invalid': "L'adresse est invalide, elle doit contenir des lettres et des chiffres seulement."
            }
        } 
    
    def __str__(self):
        return f"{self.Rib_Employe}  -  {self.Fullname}"
    
    



class FichierPaie(models.Model):
    TYPE_CHOICES = [
        ('confraires', 'confraires'),
        ('BADR', 'BADR'),
    ]
    date = models.CharField(max_length=7, validators=[RegexValidator(r'^\d{4}/\d{2}$')])
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,default='BADR')
    description = models.CharField(max_length=1000,blank=True,validators=[RegexValidator(r'^[0-9a-zA-Z ]*$')])

    def __str__(self):
        return f"{self.date} - {self.type} - {self.description}"
    
    

class FichePaie(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    fiche_paie = models.ForeignKey(FichierPaie, on_delete=models.CASCADE)
    Montant = models.CharField(max_length=15,validators=[RegexValidator(r'^[0-9]*$')])
    Libelle = models.CharField(max_length=70,blank= True,validators=[RegexValidator(r'^[0-9a-zA-Z ]*$')])

    def __str__(self):
        return f"{self.employe.Fullname} - {self.fiche_paie.date} "




