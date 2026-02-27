'''from django.shortcuts import render, HttpResponse # Importa a função render para renderizar templates e HttpResponse para retornar respostas HTTP
from django.shortcuts import get_object_or_404 # Importa a função get_object_or_404 para lidar com objetos não encontrados
from django.shortcuts import redirect # Importa a função redirect para redirecionar após criar um produto
# Importa o decorador login_required para proteger as views que exigem autenticação e permission_required para proteger as views que exigem permissões específicas
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied # Importa a exceção PermissionDenied para lidar com casos de acesso negado
#from .forms import ProdutoForm, CategoriaForm # Importa os formulários para criar produtos e categorias
'''

from django.contrib import messages # Importa o módulo de mensagens para exibir mensagens de sucesso ou erro para o usuário
from .models import Produto, Categoria # Importa o modelo Produto e Categoria para usar nas views
# Importa os mixins de autenticação para usar em views baseadas em classe, 
# garantindo que apenas usuários autenticados possam acessar essas views
from django.contrib.auth.mixins import LoginRequiredMixin
# Importa PermissionRequiredMixin para usar em views baseadas em classe, 
# garantindo que apenas usuários com permissões específicas possam acessar essas views
from django.contrib.auth.mixins import PermissionRequiredMixin
# Importa a função render para renderizar templates e get_object_or_404 para lidar com objetos não encontrados
from django.core.exceptions import PermissionDenied

# Importa ListView para criar uma view baseada em classe para listar produtos, se necessário
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Importa reverse_lazy para usar em views baseadas em classe para redirecionar após criar, atualizar ou deletar um produto
from django.urls import reverse_lazy

#importações para funcionamento da API
from rest_framework import viewsets # Importa viewsets para criar uma viewset para a API de produtos, que fornece ações padrão para listar, criar, atualizar e deletar produtos
from .serializers import ProdutoSerializer # Importa o serializer para o modelo Produto, que define como os dados do produto serão convertidos para JSON e vice-versa
# Importa IsAuthenticatedOrReadOnly para usar como permissão na API, permitindo que usuários autenticados possam criar, atualizar e deletar produtos, enquanto usuários não autenticados podem apenas ler os produtos
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Sobrescreve o método handle_no_permission para personalizar o comportamento quando um usuário autenticado sem permissão tenta acessar a view
class CustomPermissionMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated: # Verifica se o usuário não está autenticado
            return super().handle_no_permission() # Se o usuário não estiver autenticado, redireciona para a página de login
        raise PermissionDenied # Se o usuário estiver autenticado, mas não tiver a permissão necessária, levanta uma exceção PermissionDenied para exibir a página de erro 403 personalizada

# Classe baseada em ListView para listar produtos, caso queira usar uma abordagem baseada em classe
class ProdutoListView(ListView):
    model = Produto # Especifica o modelo que esta view irá usar para recuperar os dados
    template_name = "produtos/produto_list.html" # Template para renderizar a lista de produtos
    context_object_name = "itens" # Nome do contexto para acessar os produtos no template
    paginate_by = 5 # quantidade por página

class ProdutoDetailView(DetailView):
    model = Produto
    template_name = "produtos/produto_detail.html"
    context_object_name = "item"

class ProdutoCreateView(LoginRequiredMixin, CustomPermissionMixin ,CreateView):
    model = Produto
    fields = ["nome", "categoria", "preco"]
    template_name = "produtos/produto_form.html"
    success_url = reverse_lazy("produtos:produto_list")
    permission_required = "produtos.add_produto" # Permissão necessária para acessar esta view

    # Sobrescreve o método form_valid para adicionar uma mensagem de sucesso após criar um produto
    def form_valid(self, form):
        messages.success(self.request, "Produto criado com sucesso!")
        return super().form_valid(form)

class ProdutoUpdateView(LoginRequiredMixin,CustomPermissionMixin,UpdateView):
    model = Produto
    fields = ["nome", "categoria", "preco"]
    template_name = "produtos/produto_form.html"
    success_url = reverse_lazy("produtos:produto_list")
    permission_required = "produtos.change_produto" # Permissão necessária para acessar esta view
    
    def form_valid(self, form):
        messages.success(self.request, "Produto editado com sucesso!")
        return super().form_valid(form)

class ProdutoDeleteView(LoginRequiredMixin, CustomPermissionMixin, DeleteView):
    model = Produto
    template_name = "produtos/produto_confirm_delete.html"
    success_url = reverse_lazy("produtos:produto_list")
    permission_required = "produtos.delete_produto" # Permissão necessária para acessar esta view

    def form_valid(self, form):
        messages.success(self.request, "Produto deletado com sucesso!")
        return super().form_valid(form)
    
# Views para funcionamento da API usando Django REST Framework
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    # Permissão que permite que usuários autenticados possam criar, atualizar e deletar produtos, 
    # enquanto usuários não autenticados podem apenas ler os produtos
    permission_classes = [IsAuthenticatedOrReadOnly]



'''
# View baseada em função para listar produtos, caso queira usar uma abordagem baseada em função
def listar_produtos(request):
    # Recupera todos os produtos do banco de dados, ordenados por nome
    produtos = Produto.objects.all().order_by('nome')
    contexto = {
        'itens': produtos,
    }

    # Renderiza o template 'produtos/lista.html' com o contexto contendo os produtos
    return render(request, 'produtos/produto_list.html', context=contexto)


def detalhe_produto(request, pk):
    # Recupera um produto específico pelo ID ou retorna 404 se não encontrado
    produto = get_object_or_404(Produto, pk=pk)
    contexto = {
        'produto': produto,
    }

    return render(request, 'produtos/produto_detail.html', context=contexto)

@login_required # Decorador para garantir que apenas usuários autenticados possam acessar essa view
def inserir_produto(request):

    # Verifica se o usuário tem a permissão 'app.add_produto', caso contrário, renderiza uma página de erro 403 personalizada
    #if not request.user.has_perm('produtos.add_produto'):
     #   return render(request, "403.html", {"message": "Você não tem permissão para inserir produtos."})
    
    if request.method == "POST": # Verifica se o método da requisição é POST, indicando que o formulário foi enviado
        form = ProdutoForm(request.POST) # Cria uma instância do formulário com os dados enviados pelo usuário
        if form.is_valid(): # Verifica se os dados do formulário são válidos
            form.save() # Salva o novo produto no banco de dados
            # Redireciona para a lista de produtos após criar um novo produto
            # usa a url reversa para redirecionar para a lista de produtos, garantindo que a URL seja gerada corretamente mesmo que as rotas mudem no futuro
            return redirect("produtos:produto_list")
    else:
        form = ProdutoForm() # Se o método da requisição não for POST, cria uma instância vazia do formulário para exibir ao usuário

    # Renderiza o template 'produtoForm.html' com o formulário para criar um novo produto
    return render(request, "produtos/produto_form.html", {"form": form})

@login_required
# Decorador para garantir que apenas usuários autenticados possam acessar essa view
#@permission_required('produtos.change_produto', raise_exception=True)
def editar_produto(request, id):

    # Verifica se o usuário tem a permissão 'app.change_produto', caso contrário, renderiza uma página de erro 403 personalizada
    if not request.user.has_perm('produtos.change_produto'):
        return render(request, "403.html", {"message": "Você não tem permissão para editar produtos."})

    # Busca o objeto no banco, se não encontrar, retorna 404 (página não encontrada)
    produto = get_object_or_404(Produto, id=id)
    
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
            return redirect("produtos:produto_list")

    else:
        # Se for GET, apenas mostra os dados já preenchidos
        form = ProdutoForm(instance=produto)

    return render(request, "produtos/produto_form.html", {"form": form})

@login_required
# Decorador para garantir que apenas usuários autenticados possam acessar essa view
#@permission_required('produtos.change_produto', raise_exception=True)
def deletar_produto(request, id):

    # Verifica se o usuário tem a permissão 'app.change_produto', caso contrário, renderiza uma página de erro 403 personalizada
    if not request.user.has_perm('produtos.delete_produto'):
        return render(request, "403.html", {"message": "Você não tem permissão para deletar produtos."})

    # Busca o objeto no banco, se não encontrar, retorna 404 (página não encontrada)
    produto = get_object_or_404(Produto, id=id)
    
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
            return redirect("produtos:produto_list")

    else:
        # Se for GET, apenas mostra os dados já preenchidos
        form = ProdutoForm(instance=produto)

    return render(request, "produtos/produto_form.html", {"form": form})


@login_required # Decorador para garantir que apenas usuários autenticados possam acessar essa view
def inserir_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("produtos:produtos")
    else:
        form = CategoriaForm()

    return render(request, "produtos/categoria_form.html", {"form": form})

'''