from django.contrib import admin
from .models import Produto, Categoria


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'categoria')
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'categoria__nome')
    list_filter = ('categoria',)
    ordering = ('nome',)
    list_per_page = 25


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 25

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)