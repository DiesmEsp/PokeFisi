"""Modelo de pokémones con carga desde JSON, estado de combate y selección de género."""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional

from .habilidad import Habilidad
from .movimiento import Movimiento
from .sprites import fetch_pokemon_sprites


class Pokemon:
    """Representa un pokémon con sus estadísticas, movimientos y sprites."""

    def __init__(
        self,
        name: str,
        level: int,
        types: List[str],
        stats: Dict[str, int],
        abilities: List[str],
        gender: Optional[str] = None,
        gender_random: bool = False,
        genderless: bool = False,
        move_ids: Optional[List[int]] = None,
        sprite_files: Optional[Dict[str, str]] = None,
        state: Optional[str] = None,
    ):
        self.name = name
        self.level = level
        self.types = types
        self.stats = stats
        self.current_hp = stats.get("hp", 0)
        self.abilities = abilities
        self.ability = Habilidad(random.choice(abilities)) if abilities else None
        self.gender = gender
        self.gender_random = gender_random
        self.genderless = genderless
        self.move_ids = move_ids or []
        self.moves: List[Movimiento] = []
        self.sprite_files = sprite_files or {}
        self.sprite_urls: Dict[str, Optional[str]] = {}
        self.state = state

        if self.gender is None and self.gender_random and not self.genderless:
            self.gender = random.choice(["Macho", "Hembra"])

        if self.genderless:
            self.gender = None

    @classmethod
    def from_dict(cls, data: Dict) -> "Pokemon":
        """Crea un objeto Pokemon a partir de un diccionario cargado desde JSON."""
        return cls(
            name=data["name"],
            level=data.get("level", 50),
            types=data.get("types", []),
            stats=data.get("stats", {}),
            abilities=data.get("abilities", []),
            gender=data.get("gender"),
            gender_random=data.get("gender_random", False),
            genderless=data.get("genderless", False),
            move_ids=data.get("move_ids", []),
            sprite_files=data.get("sprite_files", {}),
            state=data.get("state"),
        )

    @staticmethod
    def load_all_from_json(path: str) -> List["Pokemon"]:
        """Carga todos los pokémones desde un archivo JSON relativo al proyecto."""
        base_path = Path(__file__).resolve().parent.parent
        json_path = Path(path)
        if not json_path.is_absolute():
            json_path = base_path / path
        with open(json_path, encoding="utf-8") as file:
            data = json.load(file)
        return [Pokemon.from_dict(item) for item in data.get("pokemons", [])]

    def load_sprite_urls(self) -> None:
        """Carga las URLs de sprites en `self.sprite_urls` usando PokeAPI."""
        self.sprite_urls = fetch_pokemon_sprites(self.name)

    def resolve_moves(self, move_list: List[Movimiento]) -> None:
        """Resuelve la lista de IDs de movimientos en objetos Movimiento completos."""
        move_by_id = {move.id: move for move in move_list}
        self.moves = [move_by_id[move_id] for move_id in self.move_ids if move_id in move_by_id]

    def recibir_dano(self, cantidad: int) -> int:
        """Reduce el HP actual del pokémon en `cantidad`, sin bajar de 0."""
        self.current_hp = max(self.current_hp - cantidad, 0)
        return self.current_hp

    def esta_consciente(self) -> bool:
        """Devuelve True si el pokémon aún tiene puntos de vida."""
        return self.current_hp > 0

    def reset_hp(self) -> None:
        """Restablece el HP actual al valor base definido en los stats."""
        self.current_hp = self.stats.get("hp", 0)

    def to_dict(self) -> Dict:
        """Convierte el estado del pokémon a un diccionario serializable."""
        return {
            "name": self.name,
            "level": self.level,
            "types": self.types,
            "stats": self.stats,
            "abilities": self.abilities,
            "ability": self.ability.to_dict() if self.ability else None,
            "gender": self.gender,
            "gender_random": self.gender_random,
            "genderless": self.genderless,
            "move_ids": self.move_ids,
            "sprite_files": self.sprite_files,
            "sprite_urls": self.sprite_urls,
            "state": self.state,
            "current_hp": self.current_hp,
        }

    def __repr__(self) -> str:
        type_label = "/".join(self.types) if self.types else "Sin tipo"
        return (
            f"<Pokemon {self.name} Nv.{self.level} {type_label} "
            f"HP={self.current_hp}/{self.stats.get('hp', 0)} "
            f"habilidad={self.ability.nombre if self.ability else 'None'}>"
        )

    def __str__(self) -> str:
        type_label = "/".join(self.types) if self.types else "Sin tipo"
        return (
            f"{self.name} (Nv. {self.level}) Tipo: {type_label} "
            f"HP: {self.current_hp}/{self.stats.get('hp', 0)} "
            f"Habilidad: {self.ability.nombre if self.ability else 'None'}"
        )

