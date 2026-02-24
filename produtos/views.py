from django.contrib import messages # Importa o módulo de mensagens para exibir mensagens de sucesso ou erro para o usuário
from django.shortcuts import render, HttpResponse # Importa a função render para renderizar templates e HttpResponse para retornar respostas HTTP
from django.shortcuts import get_object_or_404 # Importa a função get_object_or_404 para lidar com objetos não encontrados
from django.shortcuts import redirect # Importa a função redirect para redirecionar após criar um produto
# Importa o decorador login_required para proteger as views que exigem autenticação e permission_required para proteger as views que exigem permissões específicas
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied # Importa a exceção PermissionDenied para lidar com casos de acesso negado
from .models import Produto, Categoria # Importa o modelo Produto
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

@login_required # Decorador para garantir que apenas usuários autenticados possam acessar essa view
def inserir_produto(request):

    # Verifica se o usuário tem a permissão 'app.add_produto', caso contrário, renderiza uma página de erro 403 personalizada
    if not request.user.has_perm('produtos.add_produto'):
        return render(request, "core/403.html", {"message": "Você não tem permissão para inserir produtos."})
    
    if request.method == "POST": # Verifica se o método da requisição é POST, indicando que o formulário foi enviado
        form = ProdutoForm(request.POST) # Cria uma instância do formulário com os dados enviados pelo usuário
        if form.is_valid(): # Verifica se os dados do formulário são válidos
            form.save() # Salva o novo produto no banco de dados
            # Redireciona para a lista de produtos após criar um novo produto
            # usa a url reversa para redirecionar para a lista de produtos, garantindo que a URL seja gerada corretamente mesmo que as rotas mudem no futuro
            return redirect("produtos:lista")
    else:
        form = ProdutoForm() # Se o método da requisição não for POST, cria uma instância vazia do formulário para exibir ao usuário

    # Renderiza o template 'produtoForm.html' com o formulário para criar um novo produto
    return render(request, "produtos/produtoForm.html", {"form": form})

@login_required
# Decorador para garantir que apenas usuários autenticados possam acessar essa view
#@permission_required('produtos.change_produto', raise_exception=True)
def editar_produto(request, id):

    # Verifica se o usuário tem a permissão 'app.change_produto', caso contrário, renderiza uma página de erro 403 personalizada
    if not request.user.has_perm('produtos.change_produto'):
        return render(request, "core/403.html", {"message": "Você não tem permissão para editar produtos."})

    # Busca o objeto no banco, se não encontrar, retorna 404 (página não encontrada)
    produto = get_object_or_404(Produto, id=id)

    if not request.user.is_staff:
        raise PermissionDenied("Você não tem permissão para editar produtos.")
    
    # Se for POST, atualiza o objeto, só que agora, ao invés de criar um novo, liga o formulário ao objeto existente usando o parâmetro instance
    if request.method == "POST":
        
        # Cria o formulário com os dados enviados
        # e liga ao objeto existente
        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():
            # Atualiza o objeto existente
            form.save()

            # Redireciona para a página lista de produtos
            # Mensagem de sucesso
            messages.success(request, "Produto salvo com sucesso!")

            # Redirect (parte essencial do PRG - Post/Redirect/Get) para evitar reenvio do formulário se o usuário atualizar a página
            return redirect("produtos:lista")

    else:
        # Se for GET, apenas mostra os dados já preenchidos
        form = ProdutoForm(instance=produto)

    return render(request, "produtos/produtoForm.html", {"form": form})


@login_required # Decorador para garantir que apenas usuários autenticados possam acessar essa view
def inserir_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("produtos:lista")
    else:
        form = CategoriaForm()

    return render(request, "produtos/categoriaForm.html", {"form": form})