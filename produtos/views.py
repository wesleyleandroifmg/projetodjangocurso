from django.shortcuts import render # Importa a função render para renderizar templates
from .models import Produto, Categoria # Importa o modelo Produto
from django.shortcuts import get_object_or_404 # Importa a função get_object_or_404 para lidar com objetos não encontrados


def lista_produtos(request):
    # Recupera todos os produtos do banco de dados, ordenados por nome
    produtos = Produto.objects.all().order_by('nome')
    contexto = {
        'itens': produtos,
    }

    # Renderiza o template 'produtos/lista.html' com o contexto contendo os produtos
    return render(request, 'produtos/lista.html', context=contexto)


def detalhe_produto(request, pk):
    # Recupera um produto específico pelo ID ou retorna 404 se não encontrado
    produto = get_object_or_404(Produto, pk=pk)
    contexto = {
        'produto': produto,
    }

    return render(request, 'produtos/detalhe.html', context=contexto)