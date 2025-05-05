from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    return render(request, 'pokemon/profile.html')

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
    """Vista para mostrar detalles de un Pokémon específico"""
    try:
        # Obtener datos básicos del Pokémon
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/"
        
        pokemon_data = requests.get(pokemon_url).json()
        species_data = requests.get(species_url).json()
        
        # Procesamiento de datos
        details = {
            'name': pokemon_data['name'].title(),
            'id': pokemon_data['id'],
            'image': pokemon_data['sprites']['other']['official-artwork']['front_default'],
            'types': [t['type']['name'] for t in pokemon_data['types']],
            'height': pokemon_data['height'] / 10,  # Convertir a metros
            'weight': pokemon_data['weight'] / 10,  # Convertir a kg
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']},
            'abilities': [ability['ability']['name'] for ability in pokemon_data['abilities']],
            'description': next((flavor['flavor_text'] for flavor in species_data['flavor_text_entries'] 
                                if flavor['language']['name'] == 'es'), None),
            'habitat': species_data.get('habitat', {}).get('name', 'Desconocido'),
            'generation': species_data.get('generation', {}).get('name', 'Desconocida')
        }
        
        return render(request, 'pokemon/pokemon_detail.html', {'pokemon': details})
        
    except requests.exceptions.RequestException:
        messages.error(request, "No se pudo cargar la información del Pokémon")
        return redirect('dashboard')