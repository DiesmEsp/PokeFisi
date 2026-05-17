"""Modelo de habilidad para pokémones.

Esta clase es un placeholder para que el equipo pueda ampliar las habilidades
con efectos específicos más adelante.
"""

class Habilidad:
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion

    def aplicar(self, pokemon, evento: str = ""):
        """Método base para aplicar un efecto de habilidad durante el combate."""
        # Aquí el equipo puede implementar lógicas de habilidad según eventos.
        return None

    def __repr__(self) -> str:
        return f"<Habilidad {self.nombre}>"

    def to_dict(self) -> dict:
        return {"nombre": self.nombre, "descripcion": self.descripcion}

