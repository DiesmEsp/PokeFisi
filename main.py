"""
Demo interactivo para la carga y visualización de pokémones, movimientos y sprites.

Este archivo es solo un ejemplo educativo. El equipo puede borrar o reemplazar
completamente este `main.py` en cualquier momento: la lógica principal está en
`tests/pokemon.py`, `tests/movimiento.py`, `tests/habilidad.py` y `tests/sprites.py`.

Aquí se enseña cómo:
- cargar datos desde JSON
- seleccionar un pokémon
- mostrar género bajo demanda
- resolver movimientos por sus IDs
- ver información, stats, movimientos y sprites
- crear un menú interactivo simple para pruebas y demostración
"""

from movimiento import Movimiento
from pokemon import Pokemon


def mostrar_lista_pokemons(pokemons: list[Pokemon]) -> None:
    """Imprime una lista numerada de pokémones disponibles."""
    print("\n=== Lista de pokémones disponibles ===")
    for index, pokemon in enumerate(pokemons, start=1):
        tipo_label = "/".join(pokemon.types) if pokemon.types else "Sin tipo"
        print(f"{index}. {pokemon.name} ({tipo_label})")
    print("====================================\n")


def seleccionar_pokemon(pokemons: list[Pokemon]) -> Pokemon:
    """Solicita al usuario que elija un pokémon por número de la lista."""
    while True:
        try:
            seleccion = int(input("Elige un pokémon por número: "))
            if 1 <= seleccion <= len(pokemons):
                return pokemons[seleccion - 1]
            print("Número fuera de rango. Intenta otra vez.")
        except ValueError:
            print("Debes ingresar un número válido.")


def mostrar_genero_si_el_usuario_lo_pide(pokemon: Pokemon) -> None:
    """Pregunta si el usuario quiere ver el género del pokémon seleccionado."""
    if pokemon.genderless:
        print("Este pokémon es genderless y no tiene género.")
        return

    opcion = input("¿Deseas ver el género de este pokémon? (s/N): ").strip().lower()
    if opcion in ("s", "si", "y", "yes"):
        print(f"Género: {pokemon.gender or 'Desconocido (generado aleatoriamente según JSON)'}")
    else:
        print("No se mostrará el género por ahora.")


def mostrar_opciones_menu() -> None:
    """Imprime las opciones del menú interactivo."""
    print("\n=== Menú de visualización ===")
    print("1) Ver información general del pokémon")
    print("2) Ver stats y puntos de vida")
    print("3) Ver movimientos asignados")
    print("4) Ver URLs de sprites de Generación 5")
    print("5) Ver toda la información junta")
    print("0) Salir")
    print("==============================")


def mostrar_info_general(pokemon: Pokemon) -> None:
    """Muestra la información principal del pokémon seleccionado."""
    tipos = "/".join(pokemon.types) if pokemon.types else "Sin tipo"
    print(f"\n--- Información general de {pokemon.name} ---")
    print(f"Nombre: {pokemon.name}")
    print(f"Nivel: {pokemon.level}")
    print(f"Tipo(s): {tipos}")
    print(f"Género: {pokemon.gender or 'Desconocido'}")
    print(f"Habilidad: {pokemon.ability.nombre if pokemon.ability else 'Ninguna'}")
    print(f"Estado de batalla: {pokemon.state or 'Ninguno'}")
    print(f"IDs de movimientos: {pokemon.move_ids}")
    print("------------------------------------\n")


def mostrar_stats(pokemon: Pokemon) -> None:
    """Imprime los stats básicos del pokémon y sus puntos de vida actuales."""
    print(f"\n--- Stats de {pokemon.name} ---")
    for nombre_stat, valor in pokemon.stats.items():
        print(f"{nombre_stat.upper():>10}: {valor}")
    print(f"HP actual: {pokemon.current_hp}")
    print("--------------------------------\n")


def mostrar_movimientos(pokemon: Pokemon) -> None:
    """Imprime los movimientos que tiene asignado el pokémon."""
    print(f"\n--- Movimientos de {pokemon.name} ---")
    if not pokemon.moves:
        print("Este pokémon no tiene movimientos asignados.")
    else:
        for movimiento in pokemon.moves:
            print(
                f"[{movimiento.id}] {movimiento.nombre} | Tipo: {movimiento.tipo} | "
                f"Potencia: {movimiento.potencia} | Precisión: {movimiento.precision} | "
                f"Categoría: {movimiento.categoria}"
            )
    print("-----------------------------------\n")


def mostrar_sprites(pokemon: Pokemon) -> None:
    """Carga y muestra las URLs de sprites de Generación 5 para el pokémon."""
    print(f"\nCargando sprites de Generación 5 para {pokemon.name}...")
    pokemon.load_sprite_urls()
    print(f"--- Sprites de {pokemon.name} ---")
    for key, url in pokemon.sprite_urls.items():
        print(f"{key}: {url}")
    print("--------------------------------\n")


def main() -> None:
    """Ejemplo de uso completo: carga datos, selección e interacción con un menú."""
    pokemons = Pokemon.load_all_from_json("data/pokemon.json")
    movimientos = Movimiento.load_all_from_json("data/moves.json")

    # Mostrar los pokémones que existen en el JSON.
    mostrar_lista_pokemons(pokemons)

    # Elegir un pokémon para ver sus datos.
    seleccionado = seleccionar_pokemon(pokemons)

    # Mostrar el género sólo si el usuario lo solicita.
    mostrar_genero_si_el_usuario_lo_pide(seleccionado)

    # Convertir los move_ids del pokémon en objetos Movimiento completos.
    seleccionado.resolve_moves(movimientos)

    # Menú interactivo para ver distintos bloques de información.
    while True:
        mostrar_opciones_menu()
        opcion = input("Elige lo que quieres ver: ").strip()

        if opcion == "1":
            mostrar_info_general(seleccionado)
        elif opcion == "2":
            mostrar_stats(seleccionado)
        elif opcion == "3":
            mostrar_movimientos(seleccionado)
        elif opcion == "4":
            mostrar_sprites(seleccionado)
        elif opcion == "5":
            mostrar_info_general(seleccionado)
            mostrar_stats(seleccionado)
            mostrar_movimientos(seleccionado)
            mostrar_sprites(seleccionado)
        elif opcion == "0":
            print("Saliendo. Gracias por usar el demo interactivo.")
            break
        else:
            print("Opción inválida. Elige 0, 1, 2, 3, 4 o 5.")


if __name__ == "__main__":
    main()
