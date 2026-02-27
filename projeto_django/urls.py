from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
# Importa as views para a API de produtos e as views para autenticação JWT
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from produtos import views

router = DefaultRouter() # Cria um roteador para a API
# Registra a viewset do Produto no roteador, associando-a à URL 'produtos/'
router.register(r'produtos', views.ProdutoViewSet)

urlpatterns = [
    path('', include('core.urls')), # Inclui as URLs do aplicativo 'core' e 'produtos'
    path('produtos/', include('produtos.urls')), # Inclui as URLs do aplicativo 'produtos'
    path('admin/', admin.site.urls, name='admin'), # URL para o painel de administração do Django
    path('accounts/', include('django.contrib.auth.urls')), # Inclui as URLs de autenticação do Django para login, logout, etc.
    path('api/', include(router.urls)), # Inclui as URLs do roteador para a API
    # URLs para autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Configurações para tratamento de erros personalizados
def custom_400(request, exception):
    return render(request, "errors/400.html", status=400)

def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)

def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

handler400 = custom_400
handler403 = custom_403
handler404 = custom_404