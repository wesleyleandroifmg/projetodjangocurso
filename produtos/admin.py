from django.contrib import admin
from .models import Produto, Categoria


class ProdutoAdmin(admin.ModelAdmin):
    # Define quais campos serão exibidos como colunas na listagem do admin
    list_display = ('id', 'nome', 'preco', 'categoria')

    # Define quais campos da listagem serão clicáveis para abrir o detalhe do objeto
    list_display_links = ('id', 'nome')

    # Define quais campos poderão ser pesquisados na barra de busca do admin
    # 'categoria__nome' permite buscar pelo nome da categoria relacionada (ForeignKey)
    search_fields = ('nome', 'categoria__nome')

    # Cria filtros laterais no admin para facilitar a navegação
    # Aqui filtra os produtos pela categoria
    list_filter = ('categoria',)

    # Define a ordenação padrão da listagem (ordem alfabética pelo nome)
    ordering = ('nome',)

    # Define quantos registros aparecem por página na listagem do admin
    list_per_page = 25



class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 25

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)