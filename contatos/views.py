from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    #Ordenando por id, porém em ordem decrecente e filtrando todos os campos que tenham mostrar = True
    contato = Contato.objects.order_by('-id').filter(
        mostrar=True
    )
    paginator = Paginator(contato, 5)
    page = request.GET.get('p')
    contato = paginator.get_page(page)
    return render(request, 'contatos/index.html', {
        'contato': contato
    })

def busca(request):
    #pega o valor digitado no busca e armazena em uma variavel chamada termo
    termo = request.GET.get('termo')

    #Se a pesquisa for igual a none ou o campo vazio aparece erro
    if termo is None or not termo:
        messages.add_message\
            (request, messages.ERROR,
             'Campo busca não pode ficar vazio.'
             )
        return redirect('index')

    #Faz a união dos campos nome e sobrenome na pesquisa, sendo o Value o espaço entre o nome e o sobrenome
    campos = Concat('nome', Value(' '), 'sobrenome')
    #Ordenando por id, porém em ordem decrecente e filtrando todos os campos que tenham mostrar = True
    contato = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        #O Q() e o | funcionam como um ou, vai buscar tanto pelo nome quanto pelo telefone
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )

    paginator = Paginator(contato, 5)
    page = request.GET.get('p')
    contato = paginator.get_page(page)
    return render(request, 'contatos/busca.html', {
        'contato': contato
    })

def ver_contato(request, contato_id):
    #contatos = Contato.objects.get(id=contato_id)
    contatos = get_object_or_404(Contato, id=contato_id)

    if not contatos.mostrar:
        raise Http404()

    return render(request, 'contatos/ver_contato.html', {
        'contatos': contatos
    })
