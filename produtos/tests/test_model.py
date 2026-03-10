'''import pytest
from produtos.models import Produto, Categoria

# Permite que o teste acesse o banco de dados
@pytest.mark.django_db
def test_criar_produto_sucesso():
    # 1. Preparação
    cat = Categoria.objects.get_or_create(nome="Alimentos")[0]  # Cria ou obtém a categoria "Alimentos"

    # 2. Execução
    p = Produto.objects.create(nome="SSD 1TB", preco=350.00, categoria=cat)

    # 3. Verificação (Assertion)
    assert p.nome == "SSD 1TB"
    assert p.categoria.nome == "Alimentos"
    assert Produto.objects.count() == 1'''

import pytest
from produtos.models import Produto, Categoria

@pytest.mark.django_db
def test_crud_produto():
    # --- CREATE ---
    cat = Categoria.objects.create(nome="Hardware")
    prod = Produto.objects.create(nome="Teclado", preco=100.0, categoria=cat)
    assert Produto.objects.count() == 1

    # --- READ ---
    prod_no_banco = Produto.objects.get(id=prod.id)
    assert prod_no_banco.nome == "Teclado"

    # --- UPDATE ---
    prod_no_banco.preco = 150.0
    prod_no_banco.save()
    prod_atualizado = Produto.objects.get(id=prod.id)
    assert prod_atualizado.preco == 150.0

    # --- DELETE ---
    prod_atualizado.delete()
    assert Produto.objects.count() == 0