"""
🏆 Motor de Planificación OPTIMIZADO para Honor of Kings Esports
Versión: 7.2 Professional Edition - CORRECCIONES APLICADAS
Fecha: 2026-01-08

CORRECCIONES EN ESTA VERSIÓN:
✅ Eliminado 'Loong' (héroe no oficial)
✅ Todas las referencias ahora usan 'Ao Yin' correctamente
✅ Agregada restricción faltante para Ao Yin
✅ Sincronizadas todas las restricciones con data.json
✅ Mejorada documentación interna
✅ Agregado logging para depuración
✅ CORREGIDO: find_next_slot ahora evita huecos en el pasado
✅ CORREGIDO: Manejo de tiempo mejorado para búsquedas
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

class Scheduler:
    def __init__(self, data_file: str = "data.json"):
        self.data_file = data_file
        self.events: List[Dict] = []

        # Recursos organizados por categoría
        self.jugadores = [
            "Jugador1 (Top/Clash)",
            "Jugador2 (Jungle)",
            "Jugador3 (Mid)",
            "Jugador4 (ADC/Farm)",
            "Jugador5 (Support/Roam)",
        ]

        # Mapeo de posiciones de jugadores (para validaciones)
        self.posiciones_jugadores = {
            "Jugador1 (Top/Clash)": "Top",
            "Jugador2 (Jungle)": "Jungle", 
            "Jugador3 (Mid)": "Mid",
            "Jugador4 (ADC/Farm)": "ADC",
            "Jugador5 (Support/Roam)": "Support"
        }

        # Cargar héroes desde JSON
        self.heroes_data = self._load_heroes_data()
        self.heroes = self.heroes_data.get("heroes_esenciales", [])
        self.all_heroes = self.heroes_data.get("todos_los_heroes", [])
        self.heroes_por_rol = self.heroes_data.get("heroes_por_rol", {})
        self.heroes_por_posicion = self.heroes_data.get("heroes_por_posicion", {})

        # Lista completa de instalaciones
        self.instalaciones = [
            "Sala de Práctica 1",
            "Sala de Práctica 2", 
            "Sala de Torneo (VIP)",
            "Estación de Transmisión",
            "Área de Prensa",
            "Dispositivo Android Pro",
            "Dispositivo Android Elite",
            "Coach Principal",
            "Sala de Duelo 1v1",
            "Sala de Práctica Individual",
            "Sala de Análisis",
        ]

        # Para compatibilidad
        self.resources = self.jugadores + self.all_heroes + self.instalaciones

        # DEFINICIÓN DE RESTRICCIONES SEGÚN PROYECTO - CORREGIDAS Y COMPLETAS
        self.restricciones = {
            # 1. RESTRICCIONES DE CO-REQUISITO (INCLUSIÓN)
            "co_requisitos": [
                # === HÉROES JUNGLE CON JUGADOR2 ===
                {
                    "recurso": "Héroe: Lam (Assassin/Jungle)",
                    "requiere": "Jugador2 (Jungle)",
                    "justificacion": "Lam es un assassin premium que requiere jungler experimentado"
                },
                {
                    "recurso": "Héroe: Li Bai (Assassin/Jungle)",
                    "requiere": "Jugador2 (Jungle)",
                    "justificacion": "Li Bai necesita timing perfecto, solo Jugador2 lo domina"
                },
                
                # === HÉROES ADC CON JUGADOR4 ===
                {
                    "recurso": "Héroe: Ao Yin (Marksman/ADC)",
                    "requiere": "Jugador4 (ADC/Farm)",
                    "justificacion": "Ao Yin es el marksman dragón premium, requiere ADC especializado"
                },
                {
                    "recurso": "Héroe: Marco Polo (Marksman/ADC)",
                    "requiere": "Jugador4 (ADC/Farm)",
                    "justificacion": "Marco Polo necesita posicionamiento experto"
                },
                
                # === HÉROES MID CON JUGADOR3 ===
                {
                    "recurso": "Héroe: Daji (Mage/Mid)",
                    "requiere": "Jugador3 (Mid)",
                    "justificacion": "Daji requiere control de wave perfecto en mid"
                },
                {
                    "recurso": "Héroe: Kongming (Mage/Mid)",
                    "requiere": "Jugador3 (Mid)",
                    "justificacion": "Kongming necesita macro awareness avanzado"
                },
                
                # === HÉROES TOP CON JUGADOR1 ===
                {
                    "recurso": "Héroe: Augran (Fighter/Top)",
                    "requiere": "Jugador1 (Top/Clash)",
                    "justificacion": "Augran requiere expertise en teamfights"
                },
                
                # === HÉROES SUPPORT CON JUGADOR5 ===
                {
                    "recurso": "Héroe: Yaria (Support/Roam)",
                    "requiere": "Jugador5 (Support/Roam)",
                    "justificacion": "Yaria necesita roaming strategies avanzadas"
                },
                
                # === INSTALACIONES REQUIEREN DISPOSITIVOS ===
                {
                    "recurso": "Coach Principal",
                    "requiere": "Dispositivo Android Pro",
                    "justificacion": "Coach necesita hardware pro para análisis en tiempo real"
                },
                {
                    "recurso": "Sala de Práctica 1",
                    "requiere": "Dispositivo Android Pro",
                    "justificacion": "Salas de práctica requieren dispositivos de alto rendimiento"
                },
                {
                    "recurso": "Sala de Práctica 2",
                    "requiere": "Dispositivo Android Pro",
                    "justificacion": "Múltiples dispositivos pro para scrims completos"
                },
                
                # === SALA DE TORNEO REQUIERE EQUIPOS ESPECIALES ===
                {
                    "recurso": "Sala de Torneo (VIP)",
                    "requiere": "Estación de Transmisión",
                    "justificacion": "Torneos oficiales requieren streaming profesional"
                },
                {
                    "recurso": "Sala de Torneo (VIP)",
                    "requiere": "Área de Prensa",
                    "justificacion": "Cobertura de prensa obligatoria en torneos"
                },
                
                # === SALA DE DUELO REQUIERE DISPOSITIVO ELITE ===
                {
                    "recurso": "Sala de Duelo 1v1",
                    "requiere": "Dispositivo Android Elite",
                    "justificacion": "Duelos 1v1 requieren baja latencia (dispositivos Elite)"
                },
            ],
            
            # 2. RESTRICCIONES DE EXCLUSIÓN MUTUA - CORREGIDAS
            "exclusiones": [
                # === SALAS NO PUEDEN USARSE SIMULTÁNEAMENTE ===
                # (Solo UNA sala por evento)
                {
                    "recurso1": "Sala de Práctica 1",
                    "recurso2": "Sala de Práctica 2",
                    "justificacion": "No se pueden usar múltiples salas en un mismo evento"
                },
                {
                    "recurso1": "Sala de Práctica 1",
                    "recurso2": "Sala de Torneo (VIP)",
                    "justificacion": "Solo una sala principal por evento"
                },
                {
                    "recurso1": "Sala de Práctica 1",
                    "recurso2": "Sala de Duelo 1v1",
                    "justificacion": "Conflicto de espacio físico"
                },
                {
                    "recurso1": "Sala de Práctica 2",
                    "recurso2": "Sala de Torneo (VIP)",
                    "justificacion": "Recursos de personal insuficientes para ambas"
                },
                {
                    "recurso1": "Sala de Práctica 2",
                    "recurso2": "Sala de Duelo 1v1",
                    "justificacion": "Separación de tipos de evento requerida"
                },
                {
                    "recurso1": "Sala de Torneo (VIP)",
                    "recurso2": "Sala de Duelo 1v1",
                    "justificacion": "Configuraciones de sala incompatibles"
                },
                
                # === HÉROES QUE NO PUEDEN JUGAR JUNTOS ===
                # Junglers premium (compiten por recursos)
                {
                    "recurso1": "Héroe: Lam (Assassin/Jungle)",
                    "recurso2": "Héroe: Li Bai (Assassin/Jungle)",
                    "justificacion": "Ambos assassins premium compiten por jungle resources y gold"
                },
                
                # Mages mid conflictivos (solapamiento de kit)
                {
                    "recurso1": "Héroe: Daji (Mage/Mid)",
                    "recurso2": "Héroe: Kongming (Mage/Mid)",
                    "justificacion": "Kits de control se solapan, reduciendo efectividad del equipo"
                },
                
                # ADC premium (conflicto de farm priority)
                {
                    "recurso1": "Héroe: Ao Yin (Marksman/ADC)",
                    "recurso2": "Héroe: Marco Polo (Marksman/ADC)",
                    "justificacion": "Ambos necesitan farm priority, conflicto de recursos"
                },
                
                # === DISPOSITIVOS INCOMPATIBLES ===
                {
                    "recurso1": "Dispositivo Android Pro",
                    "recurso2": "Dispositivo Android Elite",
                    "justificacion": "Configuraciones de red incompatibles entre tipos de dispositivos"
                },
            ],
        }
        
        # REGLAS MÍNIMAS MEJORADAS
        self.reglas_minimas = {
            "jugadores_minimos": 1,
            "instalaciones_minimas": 1,
            "validar_heroes_para_jugadores": True,
            "validar_dispositivos_para_salas": True,
            "validar_nombre_unico": True,
            "validar_posiciones_en_eventos_importantes": True,
        }

        self.load_data()
        logging.info(f"✅ Scheduler inicializado con {len(self.all_heroes)} héroes y {len(self.events)} eventos")

    def _load_heroes_data(self) -> Dict:
        """Carga datos de héroes desde JSON"""
        try:
            if os.path.exists("heroes.json"):
                with open("heroes.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logging.info(f"✅ Cargados {len(data.get('todos_los_heroes', []))} héroes desde heroes.json")
                    return data
            else:
                logging.warning("⚠️ heroes.json no encontrado, usando datos por defecto")
                return self._create_default_heroes_data()
        except Exception as e:
            logging.error(f"❌ Error cargando héroes: {e}")
            return self._create_default_heroes_data()

    def _create_default_heroes_data(self) -> Dict:
        """Crea datos por defecto si no existe el archivo"""
        return {
            "heroes_esenciales": [
                "Héroe: Lam (Assassin/Jungle)",
                "Héroe: Li Bai (Assassin/Jungle)",
                "Héroe: Ao Yin (Marksman/ADC)",
                "Héroe: Daji (Mage/Mid)",
                "Héroe: Kongming (Mage/Mid)",
                "Héroe: Marco Polo (Marksman/ADC)",
                "Héroe: Augran (Fighter/Top)",
                "Héroe: Yaria (Support/Roam)",
            ],
            "todos_los_heroes": [
                "Héroe: Lam (Assassin/Jungle)",
                "Héroe: Li Bai (Assassin/Jungle)",
                "Héroe: Ao Yin (Marksman/ADC)",
                "Héroe: Daji (Mage/Mid)",
                "Héroe: Kongming (Mage/Mid)",
                "Héroe: Marco Polo (Marksman/ADC)",
                "Héroe: Augran (Fighter/Top)",
                "Héroe: Yaria (Support/Roam)",
            ],
            "heroes_por_rol": {
                "assassins": [
                    "Héroe: Lam (Assassin/Jungle)",
                    "Héroe: Li Bai (Assassin/Jungle)",
                ],
                "fighters": ["Héroe: Augran (Fighter/Top)"],
                "mages": [
                    "Héroe: Daji (Mage/Mid)",
                    "Héroe: Kongming (Mage/Mid)",
                ],
                "marksmen": [
                    "Héroe: Ao Yin (Marksman/ADC)",
                    "Héroe: Marco Polo (Marksman/ADC)",
                ],
                "supports": ["Héroe: Yaria (Support/Roam)"],
            },
            "heroes_por_posicion": {
                "Top": ["Héroe: Augran (Fighter/Top)"],
                "Jungle": [
                    "Héroe: Lam (Assassin/Jungle)",
                    "Héroe: Li Bai (Assassin/Jungle)",
                ],
                "Mid": [
                    "Héroe: Daji (Mage/Mid)",
                    "Héroe: Kongming (Mage/Mid)",
                ],
                "ADC": [
                    "Héroe: Ao Yin (Marksman/ADC)",
                    "Héroe: Marco Polo (Marksman/ADC)",
                ],
                "Support": ["Héroe: Yaria (Support/Roam)"],
            },
        }

    def get_heroes_by_role(self, role: Optional[str] = None) -> List[str]:
        """Obtiene héroes por rol (para UI optimizada)"""
        if not role or str(role).strip().lower() == "todos":
            return self.all_heroes

        role_lower = role.lower()
        role_mapping = {
            "assassins": "assassins",
            "fighters": "fighters",
            "mages": "mages",
            "marksmen": "marksmen",
            "supports": "supports",
            "tanks": "tanks",
        }

        if role_lower in role_mapping:
            role_key = role_mapping[role_lower]
            if role_key in self.heroes_por_rol:
                return self.heroes_por_rol[role_key]

        return self.all_heroes

    def get_heroes_by_position(self, position: Optional[str] = None) -> List[str]:
        """Obtiene héroes por posición (para validaciones)"""
        if not position:
            return self.all_heroes

        position_key = position.capitalize()
        if position_key in self.heroes_por_posicion:
            return self.heroes_por_posicion[position_key]

        return self.all_heroes

    def save_data(self):
        """Guarda todos los datos en archivo JSON"""
        try:
            data = {
                "events": [
                    {
                        "name": e["name"],
                        "start": e["start"].isoformat(),
                        "end": e["end"].isoformat(),
                        "resources": e["resources"],
                    }
                    for e in self.events
                ],
                "last_updated": datetime.now().isoformat(),
                "total_eventos": len(self.events),
                "restricciones_implementadas": [
                    "CO-REQUISITO: Héroe Lam requiere Jugador2 (Jungle)",
                    "CO-REQUISITO: Héroe Li Bai requiere Jugador2 (Jungle)",
                    "CO-REQUISITO: Héroe Ao Yin requiere Jugador4 (ADC/Farm)",
                    "CO-REQUISITO: Héroe Marco Polo requiere Jugador4 (ADC/Farm)",
                    "CO-REQUISITO: Héroe Daji requiere Jugador3 (Mid)",
                    "CO-REQUISITO: Héroe Kongming requiere Jugador3 (Mid)",
                    "CO-REQUISITO: Héroe Augran requiere Jugador1 (Top/Clash)",
                    "CO-REQUISITO: Héroe Yaria requiere Jugador5 (Support/Roam)",
                    "CO-REQUISITO: Coach Principal requiere Dispositivo Android Pro",
                    "CO-REQUISITO: Sala de Práctica 1 requiere Dispositivo Android Pro",
                    "CO-REQUISITO: Sala de Práctica 2 requiere Dispositivo Android Pro",
                    "CO-REQUISITO: Sala de Torneo (VIP) requiere Estación de Transmisión",
                    "CO-REQUISITO: Sala de Torneo (VIP) requiere Área de Prensa",
                    "CO-REQUISITO: Sala de Duelo 1v1 requiere Dispositivo Android Elite",
                    "EXCLUSIÓN: Lam no puede jugar con Li Bai (mismo rol Jungle)",
                    "EXCLUSIÓN: Daji no puede jugar con Kongming (mid mages conflictivos)",
                    "EXCLUSIÓN: Ao Yin no puede jugar con Marco Polo (ADC premium)",
                    "EXCLUSIÓN: Dispositivo Pro no puede usarse con Dispositivo Elite",
                    "EXCLUSIÓN: Solo UNA sala puede usarse por evento",
                    "REGLA: Mínimo 1 jugador por evento",
                    "REGLA: Mínimo 1 instalación por evento",
                    "REGLA: Misma cantidad de héroes que jugadores",
                    "REGLA: Nombre único para cada evento",
                    "REGLA: En eventos importantes (scrim/torneo), jugadores DEBEN usar héroes de su posición",
                    "REGLA: En eventos no importantes (1v1/práctica/análisis), sin restricción de posición",
                ],
                "version": "7.2",
                "corrections": [
                    "Eliminado 'Loong' (no oficial)",
                    "Agregada restricción para Ao Yin",
                    "Sincronizadas todas las restricciones",
                    "Mejorada documentación",
                    "CORREGIDO: find_next_slot ahora evita huecos en el pasado",
                    "CORREGIDO: Manejo de tiempo mejorado para búsquedas"
                ]
            }
            
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"💾 Datos guardados correctamente: {len(self.events)} eventos")
            return True
        except Exception as e:
            logging.error(f"❌ Error guardando datos en {self.data_file}: {e}")
            raise ValueError(f"Error al guardar datos: {e}")

    def load_data(self):
        """Carga datos desde archivo JSON"""
        try:
            if not os.path.exists(self.data_file):
                logging.warning(f"⚠️ Archivo {self.data_file} no encontrado, creando uno nuevo")
                self.events = []
                self.save_data()
                return

            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.events = [
                    {
                        "name": e["name"],
                        "start": datetime.fromisoformat(e["start"]),
                        "end": datetime.fromisoformat(e["end"]),
                        "resources": e["resources"],
                    }
                    for e in data.get("events", [])
                ]
                logging.info(f"📂 Cargados {len(self.events)} eventos desde {self.data_file}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"⚠️ No se pudo cargar {self.data_file}: {e}")
            self.events = []
        except Exception as e:
            logging.error(f"❌ Error inesperado cargando datos: {e}")
            self.events = []

    def validate_resources(self, resources: List[str]):
        """Valida que todos los recursos existan en el sistema"""
        invalid = [r for r in resources if r not in self.resources]
        if invalid:
            error_msg = f"❌ Recursos inválidos: {', '.join(invalid[:3])}" \
                       f"{'...' if len(invalid) > 3 else ''}"
            logging.error(error_msg)
            raise ValueError(error_msg)

    def validar_recursos_minimos(self, resources: List[str]) -> List[str]:
        """Valida que se cumplan los recursos mínimos para cualquier evento"""
        errores = []

        # Contar recursos por categoría
        jugadores = [r for r in resources if r in self.jugadores]
        heroes = [r for r in resources if r in self.all_heroes]
        instalaciones = [r for r in resources if r in self.instalaciones]

        # REGLA 1: Mínimo 1 jugador
        if len(jugadores) < self.reglas_minimas["jugadores_minimos"]:
            errores.append("🎮 Debe haber al menos 1 jugador")

        # REGLA 2: Mínimo 1 instalación
        if len(instalaciones) < self.reglas_minimas["instalaciones_minimas"]:
            errores.append("🏢 Debe haber al menos 1 instalación")

        # REGLA 3: MISMA CANTIDAD DE HÉROES QUE JUGADORES
        if self.reglas_minimas["validar_heroes_para_jugadores"] and len(heroes) < len(jugadores):
            errores.append(f"⚔️ Se necesitan al menos {len(jugadores)} héroe(s) para {len(jugadores)} jugadores")

        # REGLA 4: Las salas necesitan dispositivos
        if self.reglas_minimas["validar_dispositivos_para_salas"]:
            salas = [i for i in instalaciones if "Sala" in i]
            dispositivos = [i for i in instalaciones if "Dispositivo" in i]

            if len(salas) > 0 and len(dispositivos) == 0:
                errores.append("💻 Las salas requieren dispositivos para funcionar")

        if errores:
            logging.warning(f"⚠️ Validación de recursos mínimos falló: {errores}")

        return errores

    def _extraer_posicion_heroe(self, heroe: str) -> Optional[str]:
        """Extrae la posición de un héroe del formato 'Héroe: Nombre (Rol/Posicion)'"""
        try:
            if "/" in heroe and ")" in heroe:
                # Ejemplo: "Héroe: Lam (Assassin/Jungle)" -> "Jungle"
                contenido = heroe.split("(")[1].split(")")[0]
                partes = contenido.split("/")
                if len(partes) > 1:
                    return partes[1].strip()
        except:  # noqa: E722
            pass
        return None

    def _extraer_posicion_jugador(self, jugador: str) -> Optional[str]:
        """Extrae la posición de un jugador del formato 'JugadorX (Posicion/Rol)'"""
        try:
            if "(" in jugador and ")" in jugador:
                # Ejemplo: "Jugador1 (Top/Clash)" -> "Top"
                contenido = jugador.split("(")[1].split(")")[0]
                return contenido.split("/")[0].strip()
        except:  # noqa: E722
            pass
        return None

    def check_constraints(self, resources: List[str], event_name: str = ""):
        """VALIDACIÓN DE RESTRICCIONES - CORREGIDA CON REGLAS DE POSICIÓN"""
        errores = []

        # 1. Validar recursos mínimos primero
        errores_minimos = self.validar_recursos_minimos(resources)
        errores.extend(errores_minimos)

        # 2. Validar nombre único (si está activo)
        if self.reglas_minimas["validar_nombre_unico"] and event_name:
            for event in self.events:
                if event["name"].lower() == event_name.lower():
                    errores.append(f"🚫 Ya existe un evento con el nombre '{event_name}'")
                    break

        # 3. VERIFICAR CO-REQUISITOS
        for co_req in self.restricciones["co_requisitos"]:
            recurso = co_req["recurso"]
            requiere = co_req["requiere"]

            if recurso in resources and requiere not in resources:
                nombre_recurso = (
                    recurso.split(": ")[1] if "Héroe:" in recurso else recurso
                )
                nombre_requiere = (
                    requiere.split(" (")[0] if "Jugador" in requiere else requiere
                )
                errores.append(f"🔗 {nombre_recurso} requiere {nombre_requiere}")
                logging.warning(f"⚠️ Restricción co-requisito violada: {nombre_recurso} -> {nombre_requiere}")

        # 4. VERIFICAR EXCLUSIONES MUTUAS
        for exclusion in self.restricciones["exclusiones"]:
            r1 = exclusion["recurso1"]
            r2 = exclusion["recurso2"]

            if r1 in resources and r2 in resources:
                nombre_r1 = r1.split(": ")[1] if "Héroe:" in r1 else r1
                nombre_r2 = r2.split(": ")[1] if "Héroe:" in r2 else r2
                errores.append(f"⚡ {nombre_r1} y {nombre_r2} no pueden usarse juntos")
                logging.warning(f"⚠️ Restricción de exclusión violada: {nombre_r1} ≠ {nombre_r2}")

        # 5. Validar que en eventos importantes, los jugadores usen héroes de su posición
        if self.reglas_minimas["validar_posiciones_en_eventos_importantes"]:
            es_evento_importante = any(palabra in event_name.lower() 
                                      for palabra in ["scrim", "torneo", "tornament", "match", "competencia"])
            
            if es_evento_importante:
                jugadores_en_evento = [r for r in resources if r in self.jugadores]
                heroes_en_evento = [r for r in resources if r in self.all_heroes]
                
                for jugador in jugadores_en_evento:
                    posicion_jugador = self._extraer_posicion_jugador(jugador)
                    if posicion_jugador:
                        # Verificar que el jugador tenga al menos UN héroe de su posición
                        tiene_heroe_posicion = False
                        for heroe in heroes_en_evento:
                            posicion_heroe = self._extraer_posicion_heroe(heroe)
                            if posicion_heroe and posicion_heroe.lower() == posicion_jugador.lower():
                                tiene_heroe_posicion = True
                                break
                        
                        if not tiene_heroe_posicion:
                            error = f"🎯 {jugador} DEBE usar al menos un héroe de su posición ({posicion_jugador}) en este evento importante"
                            errores.append(error)
                            logging.warning(f"⚠️ {error}")

        # 6. Validar que no haya salas duplicadas (solo una sala por evento)
        salas_seleccionadas = [r for r in resources if "Sala" in r]
        if len(salas_seleccionadas) > 1:
            errores.append("🚫 Solo se puede seleccionar UNA sala por evento")
            logging.warning(f"⚠️ Múltiples salas seleccionadas: {salas_seleccionadas}")

        if errores:
            error_msg = "❌ ERRORES DE VALIDACIÓN:\n" + "\n".join(errores)
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        logging.info(f"✅ Validación exitosa para evento: {event_name}")

    def check_conflicts(self, start: datetime, end: datetime, resources: List[str]):
        """Verifica conflictos de horario con eventos existentes"""
        for event in self.events:
            if not (end <= event["start"] or start >= event["end"]):
                recursos_conflicto = [r for r in resources if r in event["resources"]]

                if recursos_conflicto:
                    recursos_formateados = []
                    for rc in recursos_conflicto[:3]:
                        if "Héroe:" in rc:
                            recursos_formateados.append(rc.split(": ")[1])
                        else:
                            recursos_formateados.append(rc)

                    error_msg = (
                        f"⏰ CONFLICTO con evento '{event['name']}' "
                        f"({event['start'].strftime('%d/%m %H:%M')}-{event['end'].strftime('%H:%M')})\n"
                        f"🔧 Recursos en conflicto: {', '.join(recursos_formateados)}"
                        f"{'...' if len(recursos_conflicto) > 3 else ''}"
                    )
                    logging.warning(f"⚠️ {error_msg}")
                    raise ValueError(error_msg)

    def add_event(
        self, name: str, start_str: str, duration_min: int, resources: List[str]
    ):
        """Agrega un nuevo evento con todas las validaciones"""
        logging.info(f"🔄 Intentando agregar evento: {name}")
        
        # Validar formato de fecha
        try:
            start = datetime.fromisoformat(start_str)
        except ValueError:
            error_msg = "📅 Formato de fecha inválido. Usar: YYYY-MM-DDTHH:MM"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Validar que no sea en el pasado (con margen de 5 minutos para seguridad)
        if start < datetime.now() - timedelta(minutes=5):
            error_msg = "⌛ No se pueden programar eventos en el pasado"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Calcular fin del evento
        end = start + timedelta(minutes=duration_min)

        # Validar duración
        if duration_min < 10:
            error_msg = "⏱️ Duración mínima: 10 minutos"
            logging.error(error_msg)
            raise ValueError(error_msg)
        if duration_min > 240:  # Aumentado para torneos
            error_msg = "⏱️ Duración máxima: 240 minutos"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Ejecutar todas las validaciones
        self.validate_resources(resources)
        self.check_constraints(resources, name)
        self.check_conflicts(start, end, resources)

        # Agregar evento
        try:
            self.events.append(
                {"name": name, "start": start, "end": end, "resources": resources}
            )

            # Ordenar eventos por fecha
            self.events.sort(key=lambda e: e["start"])

            # Guardar cambios
            self.save_data()
            
            logging.info(f"✅ Evento '{name}' agregado exitosamente: {start.strftime('%d/%m %H:%M')} ({duration_min} min)")
            return True
        except Exception as e:
            logging.error(f"❌ Error al agregar evento: {e}")
            # Revertir cambios si hubo error al guardar
            self.events = [e for e in self.events if e["name"] != name]
            raise ValueError(f"Error al guardar el evento: {e}")

    def find_next_slot(
        self, duration_min: int, resources: List[str], max_hours: int = 168
    ) -> Tuple[datetime, datetime]:
        """BÚSQUEDA DE HUECOS - CORREGIDO PARA EVITAR PASADO"""
        logging.info(f"🔍 Buscando hueco de {duration_min} min para {len(resources)} recursos")
        
        # Validar recursos primero
        self.validate_resources(resources)

        # Validar que los recursos cumplan reglas mínimas
        errores_minimos = self.validar_recursos_minimos(resources)
        if errores_minimos:
            error_msg = f"❌ Recursos insuficientes: {'; '.join(errores_minimos)}"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Usar nombre temporal para validación
        try:
            self.check_constraints(resources, "Búsqueda de hueco")
        except ValueError as e:
            logging.error(f"❌ Error en validación para búsqueda: {e}")
            raise ValueError(f"No se puede buscar hueco con estos recursos: {e}")

        # Empezar desde ahora + 15 minutos para evitar problemas de tiempo
        # Esto da margen para que el usuario revise y confirme
        start_time = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=15)
        
        # Si estamos fuera del horario laboral (22:00-9:00), buscar desde mañana a las 9:00
        if start_time.hour >= 22:
            # Mañana a las 9:00
            start_time = (start_time + timedelta(days=1)).replace(hour=9, minute=0)
        elif start_time.hour < 9:
            # Hoy a las 9:00
            start_time = start_time.replace(hour=9, minute=0)

        # Buscar en las próximas max_hours horas, en incrementos de 15 minutos
        # para mayor granularidad
        total_intervals = max_hours * 4  # 4 intervalos de 15 min por hora
        
        for interval in range(total_intervals):
            # Calcular el inicio del slot
            slot_start = start_time + timedelta(minutes=15 * interval)
            
            # Redondear al próximo intervalo de 15 minutos si es necesario
            if slot_start.minute % 15 != 0:
                minutes_to_add = 15 - (slot_start.minute % 15)
                slot_start = slot_start + timedelta(minutes=minutes_to_add)
            
            slot_start = slot_start.replace(second=0, microsecond=0)
            slot_end = slot_start + timedelta(minutes=duration_min)

            # Solo considerar horario laboral (9:00 - 22:00)
            if 9 <= slot_start.hour < 22:
                # Verificar que el slot no termine después de las 22:00
                if slot_end.hour >= 22 and slot_end.minute > 0:
                    continue
                    
                try:
                    self.check_conflicts(slot_start, slot_end, resources)
                    logging.info(f"✅ Hueco encontrado: {slot_start.strftime('%d/%m %H:%M')}")
                    return slot_start, slot_end
                except ValueError:
                    # Conflict detected, continue searching
                    continue

        error_msg = f"🔍 No se encontró hueco en los próximos {max_hours//24} días"
        logging.warning(error_msg)
        raise ValueError(error_msg)

    def delete_event(self, index: int):
        """Elimina un evento por índice"""
        if 0 <= index < len(self.events):
            evento_eliminado = self.events.pop(index)
            self.save_data()
            logging.info(f"🗑️ Evento eliminado: {evento_eliminado['name']}")
            return evento_eliminado
        else:
            error_msg = "Índice de evento inválido"
            logging.error(error_msg)
            raise ValueError(error_msg)

    def get_event_details(self, index: int) -> str:
        """Obtiene detalles formateados de un evento"""
        if 0 <= index < len(self.events):
            e = self.events[index]
            duration = (e["end"] - e["start"]).seconds // 60

            # Separar recursos por categoría
            jugadores = [r for r in e["resources"] if r in self.jugadores]
            heroes = [r for r in e["resources"] if r in self.all_heroes]
            instalaciones = [r for r in e["resources"] if r in self.instalaciones]

            detalles = [
                f"🏆 {e['name']}",
                f"⏰ {e['start'].strftime('%A, %d de %B %Y')}",
                f"🕐 {e['start'].strftime('%H:%M')} – {e['end'].strftime('%H:%M')} ({duration} min)",
                "",
                "👥 **JUGADORES:**",
                *[f"  • {j}" for j in jugadores],
                "",
                "⚔️ **HÉROES:**",
                *[f"  • {h.split(': ')[1]}" for h in heroes[:5]],
                *["  • ..." if len(heroes) > 5 else ""],
                "",
                "🏢 **INSTALACIONES:**",
                *[f"  • {i}" for i in instalaciones],
                "",
                f"📊 Total recursos: {len(e['resources'])}",
            ]

            return "\n".join(detalles)
        return "Evento no encontrado"

    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del sistema"""
        total_minutos = sum(
            (e["end"] - e["start"]).seconds // 60
            for e in self.events
            if e["start"] > datetime.now() - timedelta(days=30)
        )

        recursos_populares = {}
        for evento in self.events:
            for recurso in evento["resources"]:
                recursos_populares[recurso] = recursos_populares.get(recurso, 0) + 1

        top_recursos = sorted(
            recursos_populares.items(), key=lambda x: x[1], reverse=True
        )[:5]

        return {
            "total_eventos": len(self.events),
            "eventos_futuros": len(
                [e for e in self.events if e["start"] > datetime.now()]
            ),
            "total_minutos_scrim": total_minutos,
            "recursos_mas_usados": top_recursos,
            "restricciones_activas": len(self.restricciones["co_requisitos"])
            + len(self.restricciones["exclusiones"])
            + 6,  # Reglas adicionales
        }