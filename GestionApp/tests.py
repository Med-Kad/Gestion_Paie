from django.test import TestCase

# Create your tests here.
from models import Employe
for employe in Employe.objects.filter(id=None):
    employe.delete()