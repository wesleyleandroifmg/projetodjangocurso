from django import forms
from .models import Produto, Categoria

class ProdutoForm(forms.ModelForm):
  class Meta:
    model = Produto
    fields = ["nome", "preco", "categoria"]
    # fields = '__all__' # para pegar todos os campos do model

class CategoriaForm(forms.ModelForm):
  class Meta:
    model = Categoria
    fields = ["nome"]