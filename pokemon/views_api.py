# pokemon/views_api.py

from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class PokemonListAPI(APIView):
    def get(self, request):
        search = request.GET.get('search', '').lower()
        url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Error al acceder a la PokeAPI"}, status=500)

        results = response.json()["results"]

        if search:
            results = [p for p in results if search in p["name"]]

        return Response(results)

class PokemonDetailAPI(APIView):
    def get(self, request, name):
        try:
            url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
            response = requests.get(url)
            if response.status_code != 200:
                return Response({"error": "Pokémon no encontrado"}, status=404)

            data = response.json()
            result = {
                "name": data["name"],
                "id": data["id"],
                "height_m": data["height"] / 10,
                "weight_kg": data["weight"] / 10,
                "types": [t["type"]["name"] for t in data["types"]],
                "image": data["sprites"]["other"]["official-artwork"]["front_default"],
                "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
            }
            return Response(result)

        except Exception:
            return Response({"error": "Error al obtener datos"}, status=500)
