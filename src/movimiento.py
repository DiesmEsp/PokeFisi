"""Modelo de movimiento Pokémon y soporte para carga desde JSON."""

from pathlib import Path
import json


class Movimiento:
    """Representa un movimiento con sus propiedades básicas."""

    def __init__(
        self,
        id: int,
        nombre: str,
        tipo: str,
        potencia: int,
        precision: int,
        categoria: str,
        efecto: str = "",
    ):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.potencia = potencia
        self.precision = precision
        self.categoria = categoria
        self.efecto = efecto

    @classmethod
    def from_dict(cls, data: dict) -> "Movimiento":
        """Crea un Movimiento a partir de un diccionario cargado desde JSON."""
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            tipo=data["tipo"],
            potencia=data["potencia"],
            precision=data["precision"],
            categoria=data["categoria"],
            efecto=data.get("efecto", ""),
        )

    @staticmethod
    def load_all_from_json(path: str) -> list["Movimiento"]:
        """Carga todos los movimientos desde un archivo JSON relativo al proyecto."""
        base_path = Path(__file__).resolve().parent.parent
        json_path = Path(path)
        if not json_path.is_absolute():
            json_path = base_path / path
        with open(json_path, encoding="utf-8") as file:
            data = json.load(file)
        return [Movimiento.from_dict(item) for item in data.get("movimientos", [])]

    def __repr__(self) -> str:
        return (
            f"<Movimiento {self.nombre} tipo={self.tipo} categoria={self.categoria} "
            f"potencia={self.potencia} precision={self.precision}>"
        )

    def to_dict(self) -> dict:
        """Convierte el movimiento a un diccionario para guardar o depurar."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "potencia": self.potencia,
            "precision": self.precision,
            "categoria": self.categoria,
            "efecto": self.efecto,
        }

