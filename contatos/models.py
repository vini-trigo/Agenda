from django.db import models
from django.utils import timezone

"""
CONTATOS
nome: STR * (obrigatório)
sobrenome: STR (opcional)
telefone: STR * (obrigatório)
email: STR (opcional)
data_criacao: DATETIME (automático)
descricao: texto
categoria: CATEGORIA (outro model)

CATEGORIA
nome: STR * (obrigatório)
"""


class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    #Faz os campos aparecerem com o nome original
    def __str__(self):
        return self.nome

class Contato(models.Model):
    #CharField é campo string, quando um campo tem blank=True ele se torna opcional
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    #O default=timezone.now cria a data de quando foi inscrito pela primeira vez
    data_cria = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    #ForeignKey está fazendo relação com a tabela categoria e quando o nome for deletado ele não vai fazer nada
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)
    #O blank true não obriga o campo a ser preenchido
    foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/')
    # Faz os campos aparecerem com o nome original
    def __str__(self):
        return self.nome

