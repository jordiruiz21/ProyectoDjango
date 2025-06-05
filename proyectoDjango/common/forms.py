# contact/forms.py
from django import forms
from .models import Centro


class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


class CentroForm(forms.ModelForm):
    class Meta:
        model = Centro
        fields = '__all__'

