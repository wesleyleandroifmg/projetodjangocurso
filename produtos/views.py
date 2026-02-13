from urllib import request
from django.shortcuts import render # Importa a função render para renderizar templates
from .models import Produto, Categoria # Importa o modelo Produto
from django.shortcuts import get_object_or_404 # Importa a função get_object_or_404 para lidar com objetos não encontrados
from django.shortcuts import redirect # Importa a função redirect para redirecionar após criar um produto
from .forms import ProdutoForm, CategoriaForm # Importa os formulários para criar produtos e categorias

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

def inserir_produto(request):
    if request.method == "POST": # Verifica se o método da requisição é POST, indicando que o formulário foi enviado
        form = ProdutoForm(request.POST) # Cria uma instância do formulário com os dados enviados pelo usuário
        if form.is_valid(): # Verifica se os dados do formulário são válidos
            form.save() # Salva o novo produto no banco de dados
            # Redireciona para a lista de produtos após criar um novo produto
            # usa a url reversa para redirecionar para a lista de produtos, garantindo que a URL seja gerada corretamente mesmo que as rotas mudem no futuro
            return redirect("produtos:lista")
    else:
        form = ProdutoForm() # Se o método da requisição não for POST, cria uma instância vazia do formulário para exibir ao usuário

    # Renderiza o template 'criar_produto.html' com o formulário para criar um novo produto
    return render(request, "produtos/produtoForm.html", {"form": form}) 

def inserir_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("produtos:lista")
    else:
        form = CategoriaForm()

    return render(request, "produtos/categoriaForm.html", {"form": form})