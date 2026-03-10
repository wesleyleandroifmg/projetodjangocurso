from django.urls import path
from . import views

app_name = 'produtos'

'''
urlpatterns = [
  path('', views.listar_produtos, name='produto_list'),
  path("<int:pk>/", views.detalhe_produto, name='produto_detail'),
  path('novo/', views.inserir_produto, name='produto_create'),
  path('editar/<int:id>/', views.editar_produto, name='produto_update'),
]
'''

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name="produto_list"),
    path("<int:pk>/", views.ProdutoDetailView.as_view(), name="produto_detail"),
    path("novo/", views.ProdutoCreateView.as_view(), name="produto_create"),
    path("<int:pk>/editar/", views.ProdutoUpdateView.as_view(), name="produto_update"),
    path("<int:pk>/excluir/", views.ProdutoDeleteView.as_view(), name="produto_delete"),
]
