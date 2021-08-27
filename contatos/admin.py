from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'data_cria',
                    'categoria', 'mostrar')
    #Coloca um link nos campos especificados em baixo
    list_display_links = ('id', 'nome', 'sobrenome')
    #Coloca um filtro na página
    #list_filter = ('nome', 'sobrenome')
    #Vai ser exibido apenas 10 elementos por página
    list_per_page = 5
    #Adiciona um campo de busca para esses campos em baixo
    search_fields = ('nome', 'sobrenome', 'telefone')
    #Pwermite editar os  campos facilmente
    list_editable = ('telefone', 'mostrar')

admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
