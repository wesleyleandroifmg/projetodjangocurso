from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
    class Meta:

        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    categoria = models.ForeignKey(
        Categoria,     
        on_delete=models.CASCADE,
        related_name="produtos"
    )

    def __str__(self):
        return self.nome
    
    class Meta:

        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'