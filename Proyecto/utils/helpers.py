"""
Funciones auxiliares para la interfaz de Honor of Kings Esports Scheduler
"""

def get_event_type_badge(event_type):
    """Devuelve el texto del badge para el tipo de evento (sin HTML)"""
    badges = {
        "scrim": "🏆 Scrim",
        "1v1": "⚔️ Duelo 1v1",
        "practica": "🎯 Práctica",
        "analisis": "📊 Análisis",
        "torneo": "🏅 Torneo",
    }
    return badges.get(event_type, "🏆 Evento")

def get_event_type_requirements(event_type):
    """Devuelve los requisitos para cada tipo de evento"""
    requirements = {
        "scrim": {
            "name": "🏆 Scrim (5v5)",
            "description": "Entrenamiento completo de equipo. Requiere 5+ jugadores y sala adecuada.",
            "min_players": 5,
            "max_players": 10,
            "min_heroes": 5,
            "installations": ["Sala de Práctica 1", "Sala de Práctica 2", "Sala de Torneo (VIP)"],
            "devices": ["Dispositivo Android Pro", "Estación de Transmisión", "Área de Prensa"],
            "duration_min": 45,
            "duration_max": 180,
            "icon": "🏆",
        },
        "1v1": {
            "name": "⚔️ Duelo 1v1",
            "description": "Enfrentamiento individual entre dos jugadores. Ideal para practicar matchups.",
            "min_players": 2,
            "max_players": 2,
            "min_heroes": 2,
            "installations": ["Sala de Duelo 1v1"],
            "devices": ["Dispositivo Android Elite"],
            "duration_min": 10,
            "duration_max": 20,
            "icon": "⚔️",
        },
        "practica": {
            "name": "🎯 Práctica de Héroe",
            "description": "Práctica específica de un héroe con análisis detallado.",
            "min_players": 1,
            "max_players": 3,
            "min_heroes": 1,
            "installations": ["Sala de Práctica Individual"],
            "devices": ["Dispositivo Android Pro", "Dispositivo Android Elite"],
            "duration_min": 20,
            "duration_max": 60,
            "icon": "🎯",
        },
        "analisis": {
            "name": "📊 Análisis de Partida",
            "description": "Revisión de gameplay y análisis estratégico.",
            "min_players": 1,
            "max_players": 10,
            "min_heroes": 0,
            "installations": ["Sala de Análisis"],
            "devices": ["Dispositivo Android Pro"],
            "duration_min": 30,
            "duration_max": 90,
            "icon": "📊",
        },
        "torneo": {
            "name": "🏅 Torneo Oficial",
            "description": "Competencia oficial con transmisión y prensa. Requiere sala VIP.",
            "min_players": 5,
            "max_players": 10,
            "min_heroes": 5,
            "installations": ["Sala de Torneo (VIP)"],
            "devices": ["Dispositivo Android Pro", "Estación de Transmisión", "Área de Prensa"],
            "duration_min": 60,
            "duration_max": 240,
            "icon": "🏅",
        },
    }
    return requirements.get(event_type, requirements["scrim"])

def extraer_posicion_jugador(jugador_str):
    """Extrae la posición de un jugador del formato 'JugadorX (Posicion/Rol)'"""
    try:
        if "(" in jugador_str and ")" in jugador_str:
            # Ejemplo: "Jugador1 (Top/Clash)" -> "Top"
            contenido = jugador_str.split("(")[1].split(")")[0]
            return contenido.split("/")[0].strip()
    except:  # noqa: E722
        pass
    return None

def extraer_posicion_heroe(heroe_str):
    """Extrae la posición de un héroe del formato 'Héroe: Nombre (Rol/Posicion)'"""
    try:
        if "/" in heroe_str and ")" in heroe_str:
            # Ejemplo: "Héroe: Lam (Assassin/Jungle)" -> "Jungle"
            contenido = heroe_str.split("(")[1].split(")")[0]
            partes = contenido.split("/")
            if len(partes) > 1:
                return partes[1].strip()
    except:  # noqa: E722
        pass
    return None

def validate_event_resources(event_type, jugadores, heroes, instalaciones):
    """Valida los recursos según el tipo de evento - CORREGIDA"""
    reqs = get_event_type_requirements(event_type)
    errors = []
    warnings = []

    # Validar jugadores
    if len(jugadores) < reqs["min_players"]:
        errors.append(
            f"Se requieren mínimo {reqs['min_players']} jugadores para {reqs['name']}"
        )
    elif len(jugadores) > reqs["max_players"]:
        errors.append(
            f"Máximo {reqs['max_players']} jugadores permitidos para {reqs['name']}"
        )

    # Validar héroes - MISMA CANTIDAD QUE JUGADORES
    if len(heroes) < len(jugadores):
        errors.append(
            f"Se necesitan al menos {len(jugadores)} héroes para {len(jugadores)} jugadores"
        )
    elif len(heroes) < reqs["min_heroes"]:
        errors.append(
            f"Se requieren mínimo {reqs['min_heroes']} héroes para {reqs['name']}"
        )

    # Validar instalaciones
    instalaciones_validas = False
    for inst in reqs["installations"]:
        if inst in instalaciones:
            instalaciones_validas = True
            break

    if not instalaciones_validas:
        errors.append(
            f"Se requiere una de las siguientes instalaciones: {', '.join(reqs['installations'])}"
        )

    # Validar dispositivos (para ciertos tipos)
    if event_type in ["1v1", "torneo"]:
        device_requirements = {
            "1v1": ["Dispositivo Android Elite"],
            "torneo": ["Estación de Transmisión", "Área de Prensa"]
        }
        
        if event_type == "1v1":
            if "Dispositivo Android Elite" not in instalaciones:
                errors.append(
                    "Los duelos 1v1 requieren Dispositivo Android Elite para baja latencia"
                )
        elif event_type == "torneo":
            for device in device_requirements["torneo"]:
                if device not in instalaciones:
                    errors.append(
                        f"Los torneos requieren {device}"
                    )

    # Validación de posición héroe-jugador (SOLO para eventos importantes)
    if event_type in ["scrim", "torneo"]:
        # Para cada jugador, verificar que tenga al menos UN héroe de su posición
        for jugador in jugadores:
            posicion_jugador = extraer_posicion_jugador(jugador)
            if posicion_jugador:
                # Buscar héroes de la posición del jugador
                tiene_heroe_posicion = False
                for heroe in heroes:
                    posicion_heroe = extraer_posicion_heroe(heroe)
                    if posicion_heroe and posicion_heroe.lower() == posicion_jugador.lower():
                        tiene_heroe_posicion = True
                        break
                
                if not tiene_heroe_posicion:
                    errors.append(f"🎯 {jugador} DEBE seleccionar al menos un héroe de su posición ({posicion_jugador}) para este evento importante")
        
        # Adicional: Verificar cobertura de posiciones
        posiciones_presentes = set()
        for heroe in heroes:
            posicion = extraer_posicion_heroe(heroe)
            if posicion:
                posiciones_presentes.add(posicion)
        
        if len(posiciones_presentes) < 3 and len(jugadores) >= 3:
            warnings.append("⚠️ Se recomienda tener héroes de al menos 3 posiciones diferentes para un equipo balanceado")
    
    # Para eventos NO importantes (1v1, práctica, análisis), NO hay restricción de posición
    elif event_type in ["1v1", "practica", "analisis"]:
        # Los jugadores pueden usar cualquier héroe (sin restricción)
        # Solo verificar que haya suficientes héroes
        if len(heroes) < len(jugadores):
            warnings.append(f"⚠️ Se recomienda al menos {len(jugadores)} héroe(s) para {len(jugadores)} jugador(es)")
        
        # Advertencia si hay muchos héroes de la misma posición
        posiciones_count = {}
        for heroe in heroes:
            posicion = extraer_posicion_heroe(heroe)
            if posicion:
                posiciones_count[posicion] = posiciones_count.get(posicion, 0) + 1
        
        for posicion, count in posiciones_count.items():
            if count > 2 and len(jugadores) < 4:
                warnings.append(f"⚠️ Muchos héroes de la misma posición ({posicion}): {count}")

    # Validar salas exclusivas (no pueden usarse dos salas a la vez)
    salas_seleccionadas = [inst for inst in instalaciones if "Sala" in inst]
    if len(salas_seleccionadas) > 1:
        errors.append("🚫 Solo se puede seleccionar UNA sala por evento")

    return errors, warnings