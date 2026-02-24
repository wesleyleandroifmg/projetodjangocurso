from django.urls import path
from django.contrib.auth import views as auth_views # Importa as views de autenticação do Django para lidar com login e logout
from . import views

app_name = 'core'

urlpatterns = [
  path('', views.home, name='home'),
  path('sobre/', views.sobre, name='sobre'),
  path('contato/', views.contato, name='contato'),
  path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
  path("logout/", auth_views.LogoutView.as_view(), name="logout"),

]