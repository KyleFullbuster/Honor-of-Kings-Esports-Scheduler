"""
🏆 Honor of Kings Esports Scheduler - Interfaz Principal ESTABLE
Versión: 7.2 Professional Edition - CON TODAS LAS MEJORAS
Interfaz modular con pestañas separadas
"""

import time
import streamlit as st

from scheduler import Scheduler
from styles import CSS_COMPLETO  # Importar CSS desde archivo separado

# Importar las pestañas
from tabs.tab1_events import show_events_tab
from tabs.tab2_add import show_add_tab
from tabs.tab3_search import show_search_tab
from tabs.tab4_delete import show_delete_tab
from tabs.tab5_details import show_details_tab
from tabs.tab6_system import show_system_tab

# ==============================================
# 0. CONFIGURACIÓN DE ESTADO - PREVENIR RECARGAS
# ==============================================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.prevent_actions = False
    st.session_state.last_interaction = time.time()
    st.session_state.selected_event_type = "scrim"

if "selected_event_type" not in st.session_state:
    st.session_state.selected_event_type = "scrim"

# ==============================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==============================================
st.set_page_config(
    page_title="HoK Esports Scheduler Pro",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": """
        ## 🏆 Honor of Kings Esports Scheduler Pro
        **Versión 7.2 Professional Edition** - Enero 2026

        Sistema de gestión profesional para equipos competitivos.
        Implementa TODAS las restricciones requeridas del proyecto.

        Características principales:
        • ✅ Sistema de tipos de eventos (Scrim, 1v1, Práctica, Análisis, Torneo)
        • ✅ Validación mejorada: misma cantidad de héroes que jugadores
        • ✅ Validación de posiciones en eventos importantes
        • ✅ Restricción: solo una sala por evento
        • ✅ Nombre único para eventos
        • ✅ Sala de Torneo VIP con requisitos especiales
        • ✅ Búsqueda inteligente con creación directa
        • ✅ Persistencia completa en JSON
        • 🎨 Fondo local con paneles negros elegantes
        • ⚡ Selectores de hora fáciles de usar

        Tipos de eventos disponibles:
        1. 🏆 Scrim (5v5) - Entrenamiento completo de equipo
        2. ⚔️ 1v1 Duelo - Enfrentamiento individual
        3. 🎯 Práctica de Héroe - Práctica específica
        4. 📊 Análisis - Revisión de partidas
        5. 🏅 Torneo - Competencia oficial con transmisión

        Proyecto de Programación - Primer Semestre
        """,
    },
)

# ==============================================
# 2. INICIALIZACIÓN OPTIMIZADA
# ==============================================
def init_scheduler():
    """Inicializa el scheduler una sola vez"""
    scheduler = Scheduler()
    # Agregar tipos de instalaciones especializadas
    instalaciones_necesarias = [
        "Dispositivo Android Elite",
        "Sala de Duelo 1v1",
        "Sala de Práctica Individual",
        "Sala de Análisis",
        "Sala de Torneo (VIP)",
        "Estación de Transmisión",
        "Área de Prensa"
    ]
    
    for inst in instalaciones_necesarias:
        if inst not in scheduler.instalaciones:
            scheduler.instalaciones.append(inst)
    
    return scheduler

@st.cache_data(ttl=10)
def get_cached_stats(_scheduler):
    """Obtiene estadísticas con caché"""
    return _scheduler.get_statistics()

# Cargar scheduler (usar estado de sesión para persistencia)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = init_scheduler()

scheduler = st.session_state.scheduler

# ==============================================
# 3. APLICAR CSS DESDE ARCHIVO SEPARADO
# ==============================================
st.markdown(CSS_COMPLETO, unsafe_allow_html=True)

# ==============================================
# 4. SIDEBAR COMPLETA CON ESTADÍSTICAS
# ==============================================
with st.sidebar:
    # Encabezado
    st.markdown(
        """
    <div style='
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(20, 20, 30, 0.9));
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        border: 2px solid rgba(255, 255, 255, 0.15);
        text-align: center;
        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.8),
            inset 0 0 20px rgba(255, 255, 255, 0.05);
    '>
        <div style='font-size: 3rem; color: #FFFFFF; text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); margin-bottom: 10px;'>⚔️</div>
        <h3 style='color: #FFFFFF; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8); margin: 15px 0;'>HONOR OF KINGS</h3>
        <p style='color: #CCCCCC; text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8); margin: 0; font-size: 1em; font-weight: bold; letter-spacing: 1px;'>
            ESPORTS SCHEDULER PRO v7.2
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Estadísticas en tiempo real
    st.markdown("### 📊 DASHBOARD EN TIEMPO REAL")
    stats = get_cached_stats(scheduler)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📅 Eventos", stats["total_eventos"])
        st.metric("⏱️ Min. Scrim", f"{stats['total_minutos_scrim']}")
    with col2:
        st.metric("🔮 Futuros", stats["eventos_futuros"])
        st.metric("🔧 Reglas", stats["restricciones_activas"])

    st.markdown("---")

    # Tipos de eventos activos
    st.markdown("### 🎮 TIPOS DE EVENTOS")
    event_types_count = {"scrim": 0, "1v1": 0, "practica": 0, "analisis": 0, "torneo": 0}

    for event in scheduler.events:
        event_name = event["name"].lower()
        if "scrim" in event_name or "vs" in event_name or "equipo" in event_name:
            event_types_count["scrim"] += 1
        elif "1v1" in event_name or "duelo" in event_name:
            event_types_count["1v1"] += 1
        elif "práctica" in event_name or "practica" in event_name:
            event_types_count["practica"] += 1
        elif "análisis" in event_name or "analisis" in event_name:
            event_types_count["analisis"] += 1
        elif "torneo" in event_name or "tornament" in event_name:
            event_types_count["torneo"] += 1
        else:
            event_types_count["scrim"] += 1

    for event_type, count in event_types_count.items():
        if count > 0:
            from utils.helpers import get_event_type_requirements
            reqs = get_event_type_requirements(event_type)
            st.caption(f"{reqs['icon']} {reqs['name']}: {count}")

    st.markdown("---")

    # Recursos más utilizados
    st.markdown("### 🏆 RECURSOS POPULARES")
    if stats["recursos_mas_usados"]:
        for recurso, count in stats["recursos_mas_usados"][:3]:
            nombre = recurso.split(": ")[1] if "Héroe:" in recurso else recurso
            nombre = nombre[:15] + "..." if len(nombre) > 15 else nombre
            porcentaje = min(count / 5, 1.0)
            st.progress(porcentaje, text=f"{nombre}: {count} usos")
    else:
        st.info("📭 No hay datos de uso aún")

    st.markdown("---")

    # Información del sistema
    st.markdown("### ⚙️ INFORMACIÓN DEL SISTEMA")
    st.caption(f"📁 **Datos:** {scheduler.data_file}")
    st.caption(f"⚡ **Héroes:** {len(scheduler.all_heroes)} cargados")
    st.caption(f"👥 **Jugadores:** {len(scheduler.jugadores)} disponibles")
    st.caption(f"🏢 **Instalaciones:** {len(scheduler.instalaciones)} tipos")
    st.caption("🎮 **Tipos de evento:** 5 configurados")

    st.markdown("---")
    st.markdown("**🎨 SISTEMA MODULARIZADO**")
    st.caption("• CSS en archivo separado")
    st.caption("• Fondo local offline")
    st.caption("• Mejor mantenimiento")

# ==============================================
# 5. TÍTULO PRINCIPAL
# ==============================================
st.title("⚔️ HONOR OF KINGS ESPORTS SCHEDULER PRO")
st.markdown(
    """
    <div style='
        text-align: center;
        color: #FFFFFF;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
        font-style: italic;
        margin-bottom: 35px;
        padding: 20px;
        background: rgba(0, 0, 0, 0.85);
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.7),
            inset 0 0 20px rgba(255, 255, 255, 0.05);
    '>
        <p style='font-size: 1.2rem; margin: 0;'>
            <strong>Sistema profesional con 5 tipos de eventos • Versión 7.2 Modularizado</strong><br>
            <span style='font-size: 1rem; color: #CCCCCC;'>
                🏆 Scrim 5v5 • ⚔️ Duelo 1v1 • 🎯 Práctica • 📊 Análisis • 🏅 Torneo
            </span>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================
# 6. TABS PRINCIPALES
# ==============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📅 EVENTOS", "➕ AGREGAR", "🔍 BUSCAR", "🗑️ ELIMINAR", "📊 DETALLES", "⚙️ SISTEMA"]
)

# ==============================================
# 7. CARGAR CADA PESTAÑA
# ==============================================
with tab1:
    show_events_tab(scheduler)

with tab2:
    show_add_tab(scheduler)

with tab3:
    show_search_tab(scheduler)

with tab4:
    show_delete_tab(scheduler)

with tab5:
    show_details_tab(scheduler)

with tab6:
    show_system_tab(scheduler, init_scheduler)

# ==============================================
# 8. FOOTER
# ==============================================
st.markdown("---")
st.markdown(
    """
    <div style='
        text-align: center;
        color: #888;
        font-size: 14px;
        padding: 25px;
        background: rgba(0, 0, 0, 0.9);
        border-radius: 15px;
        border-top: 3px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        margin-top: 40px;
        box-shadow:
            0 -5px 25px rgba(0, 0, 0, 0.8),
            inset 0 0 20px rgba(255, 255, 255, 0.05);
    '>
        <p style='font-size: 18px; color: #FFFFFF; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8); margin-bottom: 15px; font-weight: bold;'>
            🏆 <strong>Honor of Kings Esports Scheduler Pro v7.2</strong>
        </p>
        <p style='margin-bottom: 8px; color: #CCCCCC;'>
            ⚔️ <strong>Sistema Modularizado • CSS Separado • Fondo Local</strong>
        </p>
        <p style='margin-bottom: 8px; color: #AAAAAA;'>
            🎮 <strong>🏆 Scrim 5v5 • ⚔️ Duelo 1v1 • 🎯 Práctica • 📊 Análisis • 🏅 Torneo</strong>
        </p>
        <p style='margin: 0; color: #999999; font-size: 0.9em;'>
            📅 Proyecto de Programación - Primer Semestre | Enero 2026
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================
# 9. MANEJO DE DATOS PRE-DEFINIDOS
# ==============================================
if "nombre_predef" in st.session_state:
    st.toast("📋 Datos de búsqueda disponibles en 'Agregar'", icon="ℹ️")

# ==============================================
# 10. RESET DE ESTADO SI ES NECESARIO
# ==============================================
current_time = time.time()
if current_time - st.session_state.get("last_interaction", 0) > 30:
    st.session_state.prevent_actions = False
    st.session_state.last_interaction = current_time