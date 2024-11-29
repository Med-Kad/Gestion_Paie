from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse,HttpResponse
# from forms import EmployeForm
from django.contrib import messages  # Importer le module messages
from models import *
from django.core.paginator import Paginator
from django.core import serializers

# from models import Employe
for employe in Employe.objects.filter(id=None):
    employe.delete()
