# forms.py

from django import forms
from django.forms import modelformset_factory
from .models import Entrenamiento, Serie, Musculo, Ejercicio

class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ['ejercicio']

class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['peso_levantado', 'repeticiones']

SerieFormSet = modelformset_factory(Serie, form=SerieForm, extra=3, can_delete=True)



class MusculoForm(forms.ModelForm):
    class Meta:
        model = Musculo
        fields = '__all__'

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = '__all__'