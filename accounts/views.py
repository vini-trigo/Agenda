from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
#Voce só pode acessar uma pagina com o login: login_required
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    #Se nada for postado ele retorna a tela de login
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    #Veirifica se o usuario e a senha estão cadastrados
    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, 'Login ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        messages.success(request, 'Voce esta logado')
        auth.login(request, user)
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    #Campos de validação do formuário
    #Exibe uma mensagem de erro se algum campo estiver vazio
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode estar vazio')
        return render(request, 'accounts/cadastro.html')

    #Levanta uma exceção caso o email seja inválido
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/cadastro.html')

    #Exibe uma menssagem de erro caso o campo senha tenha menos de 6 letras
    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter mais de 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    #Exibe uma menssagem de erro caso o campo usuario tenha menos de 6 letras
    if len(usuario) < 6:
        messages.error(request, 'Usuario precisa ter mais de 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    #Verifica se as senhas são iguais
    if senha != senha2:
        messages.error(request, 'As senhas precisam ser iguais')
        return render(request, 'accounts/cadastro.html')

    #Verifica se o usuario do formulário já existe
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário existente')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email existente')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Registrado com sucesso!')

    user = User.objects.create_user(username=usuario, email=email, password=senha,
                                    first_name=nome, last_name=sobrenome)
    #Salva o usuario
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    #pega os dados postados do formulario dashboard
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao validar o formulario, verifique os campos')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    #Verifica se a descrição tem mais de 5 letras
    descricao = request.POST.get('descricao')
    if len(descricao) < 7:
        messages.error(request, 'A descrição precisa ser maior que 7 caracteres')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} cadastrado!')
    return redirect('dashboard')
