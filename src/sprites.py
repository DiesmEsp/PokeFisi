"""Módulo de utilidades para obtener sprites de PokeAPI."""

import json
import urllib.error
import urllib.request
from typing import Dict, Optional

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon/"


def normalize_name(nombre: str) -> str:
    """Normaliza el nombre del pokémon para las URLs de PokeAPI."""
    nombre = nombre.strip().lower()
    nombre = nombre.replace(" ", "-")
    nombre = nombre.replace(".", "")
    nombre = nombre.replace("'", "")
    nombre = nombre.replace("♀", "-f")
    nombre = nombre.replace("♂", "-m")
    return nombre


def fetch_pokemon_sprites(nombre: str) -> Dict[str, Optional[str]]:
    """Busca los sprites de Generación 5 (Black/White) usando PokeAPI.

    Retorna un diccionario con claves front, back, front_animated y back_animated.
    Si la API no responde, devuelve valores None para cada clave.
    """
    pokemon_name = normalize_name(nombre)
    request_url = f"{POKEAPI_BASE}{pokemon_name}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        request = urllib.request.Request(request_url, headers=headers)
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.load(response)
    except urllib.error.URLError:
        return {
            "front": None,
            "back": None,
            "front_animated": None,
            "back_animated": None,
        }

    version_data = data.get("sprites", {}).get("versions", {}).get("generation-v", {}).get("black-white", {})
    animated = version_data.get("animated", {})

    return {
        "front": version_data.get("front_default"),
        "back": version_data.get("back_default"),
        "front_animated": animated.get("front_default"),
        "back_animated": animated.get("back_default"),
    }
