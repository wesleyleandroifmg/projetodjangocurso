from urllib import request
from django.shortcuts import render # render é usado para retornar templates
from django.http import HttpResponse # HttpResponse é usado para retornar respostas simples

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
