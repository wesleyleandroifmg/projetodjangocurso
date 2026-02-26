"""
URL configuration for projeto_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf.urls import handler403

urlpatterns = [
    path('', include('core.urls')),
    path('produtos/', include('produtos.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('django.contrib.auth.urls')),
]


def custom_400(request, exception):
    return render(request, "errors/400.html", status=400)

def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)

def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)


handler400 = custom_400
handler403 = custom_403
handler404 = custom_404