from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
  path('', views.lista_produtos, name='lista'),
  path("<int:pk>/", views.detalhe_produto, name='detalhe'),
  path('novo/', views.inserir_produto, name='inserir_produto'),
  path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
  path('categorias/nova/', views.inserir_categoria, name='inserir_categoria'),

]