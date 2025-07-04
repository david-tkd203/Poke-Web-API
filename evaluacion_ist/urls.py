"""
URL configuration for evaluacion_ist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, reverse_lazy  # Añade reverse_lazy aquí
from django.contrib.auth import views as auth_views
from django.urls import include
from pokemon.views_api import PokemonListAPI, PokemonDetailAPI
from pokemon.views import (
    home, 
    login_view, 
    logout_view, 
    dashboard_view, 
    pokemon_detail,
    profile_view, 
    edit_profile_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('pokemon/<str:pokemon_name>/', pokemon_detail, name='pokemon_detail'),
    
    # URLs de perfil
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    
    # URLs de autenticación integradas
    path('password-change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='pokemon/password_change.html',
            success_url=reverse_lazy('profile')  # Ahora reverse_lazy está importado
        ), 
        name='password_change'),
    
    path('password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='pokemon/password_change_done.html'
        ),
        name='password_change_done'),
    #ruta para rest
    path('', include('pokemon.urls')),
]