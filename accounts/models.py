from django.db import models
from contatos.models import Contato
from django import forms


#formulário do dashboard
class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = '__all__'
        exclude = ('mostrar',)

