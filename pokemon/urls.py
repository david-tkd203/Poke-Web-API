# pokemon/urls.py
from django.urls import path
from .views import liberar_pokemon
from .views_api import PokemonListAPI, PokemonDetailAPI
from . import views


urlpatterns = [
    path('api/pokemon/', PokemonListAPI.as_view(), name='api_pokemon_list'),
    path('api/pokemon/<str:name>/', PokemonDetailAPI.as_view(), name='api_pokemon_detail'),
    path('liberar/<str:nombre_pokemon>/', liberar_pokemon, name='liberar_pokemon'),
    path('pokemon/<str:nombre_pokemon>/detalle/', views.agregar_detalles_pokemon, name='agregar_detalles_pokemon'),
]
