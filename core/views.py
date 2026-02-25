from django.shortcuts import render, redirect # render é usado para retornar templates e redirect é usado para redirecionar para outras páginas
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def home(request):
  nome = 'Wesley'
  curso = 'Django do Zero'
  itens = ['Introdução', 'POO', 'Banco de Dados']
  contexto = {
    "nome": nome,
    "curso": curso,
    'lista': itens
  }

  return render(request, "core/home.html", contexto)

def contato(request):
  return render(request, "core/contato.html")

def sobre(request):
  return render(request, "core/sobre.html")

def login_view(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("core:home")
    else:
        messages.error(request, "Usuário ou senha inválidos")
  else:
    form = AuthenticationForm()

  return render(request, "core/login.html", {"form": form})
