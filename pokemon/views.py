from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PokemonRegistro
from .forms import PokemonCapturaForm

"""Para la visual de Rest"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

def home(request):
    """Vista para la página de inicio (puede redirigir al dashboard o mostrar contenido inicial)"""
    return redirect('dashboard')  # Redirige al dashboard por defecto
    # O si prefieres una página de inicio separada:
    # return render(request, 'pokemon/home.html')

def login_view(request):
    """Vista para el login de usuarios"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'pokemon/login.html')

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    return redirect('home')

#Funciones con sesion iniciada

@login_required
def profile_view(request):
    user = request.user

    # Obtener lista de nombres únicos de Pokémon vistos (sin usar distinct('field'))
    vistos_nombres = (
        PokemonRegistro.objects
        .filter(usuario=user, estado='visto')
        .values_list('nombre_pokemon', flat=True)
        .distinct()
    )

    # Obtener todos los registros de atrapados (pueden repetirse)
    atrapados = PokemonRegistro.objects.filter(usuario=user, estado='atrapado')

    # Obtener el total de especies de Pokémon disponibles desde la API
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon-species/')
        response.raise_for_status()
        total_pokemon = response.json().get('count', 151)  # fallback a 151 si falla
    except:
        total_pokemon = 151

    # Calcular porcentaje de completado respecto al total de especies
    porcentaje = round((atrapados.count() / total_pokemon) * 100, 2)

    context = {
        'vistos_count': len(vistos_nombres),
        'atrapados_count': atrapados.count(),
        'porcentaje_completado': porcentaje,
        'vistos': list(vistos_nombres),  # pasar lista de nombres únicos
        'atrapados': atrapados,
        'user': user,
    }

    return render(request, 'pokemon/profile.html', context)

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'pokemon/edit_profile.html', {'form': form})

@login_required
def dashboard_view(request):
    search_query = request.GET.get('q', '').strip().lower()
    
    try:
        # Obtener lista completa de Pokémon
        list_url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
        list_response = requests.get(list_url, timeout=10)
        list_response.raise_for_status()
        all_pokemon = list_response.json()['results']
        
        # Filtrar por búsqueda si existe
        if search_query:
            all_pokemon = [p for p in all_pokemon if search_query in p['name'].lower()]
        
        # Obtener información detallada para los Pokémon filtrados (limitamos a 50 para performance)
        detailed_pokemons = []
        type_counter = {}
        
        # Primero obtenemos todos los tipos existentes de la API
        types_url = "https://pokeapi.co/api/v2/type/"
        types_response = requests.get(types_url)
        types_data = types_response.json()
        all_types = {t['name']: 0 for t in types_data['results'] if t['name'] != 'shadow' and t['name'] != 'unknown'}
        
        for pokemon in all_pokemon[:50]:
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon['name']}/"
            pokemon_response = requests.get(pokemon_url, timeout=5)
            pokemon_response.raise_for_status()
            pokemon_data = pokemon_response.json()
            
            # Procesar tipos para estadísticas
            types = [t['type']['name'] for t in pokemon_data['types']]
            for type_name in types:
                if type_name in all_types:
                    all_types[type_name] += 1
            
            # Estructurar datos para el template
            detailed_pokemons.append({
                'name': pokemon_data['name'],
                'image': pokemon_data['sprites']['other']['official-artwork']['front_default'],
                'types': types,
                'height': pokemon_data['height'] / 10,  # Convertido a metros
                'weight': pokemon_data['weight'] / 10,  # Convertido a kg
                'id': pokemon_data['id']
            })
        
        # Ordenar tipos por frecuencia (mayor a menor)
        sorted_types = sorted(all_types.items(), key=lambda x: x[1], reverse=True)
        
        return render(request, 'pokemon/dashboard.html', {
            'total_pokemons': len(all_pokemon),
            'type_distribution': sorted_types,
            'pokemons': detailed_pokemons,
            'search_query': search_query
        })
        
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al cargar datos: {str(e)}")
        return render(request, 'pokemon/dashboard.html', {
            'total_pokemons': 0,
            'type_distribution': [],
            'pokemons': []
        })

@login_required
def pokemon_detail(request, pokemon_name):
    nombre = pokemon_name.lower()

    # Manejo de botones
    if request.method == 'POST':
        if 'visto' in request.POST:
            _, creado = PokemonRegistro.objects.get_or_create(
                usuario=request.user,
                nombre_pokemon=nombre,
                estado='visto'
            )
            if creado:
                messages.success(request, f'{nombre.title()} ha sido marcado como visto.')
            else:
                messages.info(request, f'{nombre.title()} ya estaba marcado como visto.')
            return redirect('pokemon_detail', pokemon_name=nombre)

        elif 'atrapar' in request.POST:
            _, creado = PokemonRegistro.objects.get_or_create(
                usuario=request.user,
                nombre_pokemon=nombre,
                estado='atrapado'
            )
            if creado:
                messages.success(request, f'{nombre.title()} ha sido marcado como atrapado.')
            else:
                messages.info(request, f'{nombre.title()} ya estaba marcado como atrapado.')
            return redirect('pokemon_detail', pokemon_name=nombre)

    try:
        # Obtener datos desde PokeAPI
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{nombre}/"
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{nombre}/"

        pokemon_data = requests.get(pokemon_url, timeout=10).json()
        species_data = requests.get(species_url, timeout=10).json()

        details = {
            'name': pokemon_data['name'].title(),
            'id': pokemon_data['id'],
            'image': pokemon_data['sprites']['other']['official-artwork']['front_default'],
            'types': [t['type']['name'] for t in pokemon_data['types']],
            'height': pokemon_data['height'] / 10,
            'weight': pokemon_data['weight'] / 10,
            'stats': {s['stat']['name']: s['base_stat'] for s in pokemon_data['stats']},
            'abilities': [a['ability']['name'] for a in pokemon_data['abilities']],
            'description': next((flavor['flavor_text'] for flavor in species_data['flavor_text_entries']
                                if flavor['language']['name'] == 'es'), None),
            'habitat': species_data.get('habitat', {}).get('name', 'Desconocido'),
            'generation': species_data.get('generation', {}).get('name', 'Desconocida')
        }

        # Verificar si ya fue marcado como visto y/o atrapado
        ya_visto = PokemonRegistro.objects.filter(
            usuario=request.user,
            nombre_pokemon=nombre,
            estado='visto'
        ).exists()

        ya_atrapado = PokemonRegistro.objects.filter(
            usuario=request.user,
            nombre_pokemon=nombre,
            estado='atrapado'
        ).exists()

        return render(request, 'pokemon/pokemon_detail.html', {
            'pokemon': details,
            'ya_visto': ya_visto,
            'ya_atrapado': ya_atrapado
        })

    except requests.exceptions.RequestException:
        messages.error(request, "No se pudo cargar la información del Pokémon")
        return redirect('dashboard')
    
@login_required
def liberar_pokemon(request, nombre_pokemon):
    if request.method == 'POST':
        registros = PokemonRegistro.objects.filter(
            usuario=request.user,
            nombre_pokemon=nombre_pokemon.lower(),
            estado='atrapado'
        )
        if registros.exists():
            registros.delete()
            messages.success(request, f'{nombre_pokemon.title()} fue liberado exitosamente.')
        else:
            messages.warning(request, f'{nombre_pokemon.title()} no está en tu lista de capturados.')
    return redirect('profile')

@login_required
def agregar_detalles_pokemon(request, nombre_pokemon):
    if request.method == 'POST':
        form = PokemonCapturaForm(request.POST)
        if form.is_valid():
            capturado = form.save(commit=False)
            capturado.usuario = request.user
            capturado.nombre_pokemon = nombre_pokemon.lower()
            capturado.estado = 'atrapado'  # asegúrate de asignar este estado
            capturado.save()
            return redirect('profile')  # o dashboard
    else:
        form = PokemonCapturaForm(initial={'nombre_pokemon': nombre_pokemon.lower()})

    return render(request, 'pokemon/registro_detalle.html', {'form': form, 'pokemon': nombre_pokemon.title()})

