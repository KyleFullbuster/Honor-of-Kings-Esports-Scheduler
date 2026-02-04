"""
🏆 Honor of Kings Esports Scheduler - Interfaz Principal ESTABLE
Versión: 6.1 Professional Edition - CON TODAS LAS MEJORAS
Interfaz completa con todas las validaciones mejoradas y nuevo tipo de evento Torneo
"""

import time
from datetime import datetime, timedelta

import streamlit as st

from scheduler import Scheduler

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
        **Versión 6.1 Professional Edition** - Diciembre 2025

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
        • 🎨 Fondo original con paneles negros elegantes
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

# Cargar componentes (solo una vez)
scheduler = init_scheduler()

# ==============================================
# 3. CSS CON FONDO ORIGINAL, PANELES NEGROS Y HEADER NEGRO PURO
# ==============================================
css_completo_negro_puro = """
<style>
    /* ============================================== */
    /* HEADER SUPERIOR NEGRO PURO - NUEVA SECCIÓN */
    /* ============================================== */
    
    /* Header principal de Streamlit (Deploy, Config, Hamburger) */
    header[data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 1) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.8) !important;
        z-index: 999999 !important;
        position: sticky !important;
        top: 0 !important;
    }
    
    /* Contenedor interno del header */
    header[data-testid="stHeader"] > div {
        background-color: transparent !important;
    }
    
    /* Toolbar (donde está Deploy y los 3 puntos) */
    .stDeployButton {
        background-color: transparent !important;
    }
    
    /* Botón de Deploy */
    button[kind="header"] {
        background-color: rgba(20, 20, 20, 0.95) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
    }
    
    button[kind="header"]:hover {
        background-color: rgba(40, 40, 40, 0.95) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6) !important;
    }
    
    /* Menú de 3 puntos (configuración) */
    button[data-testid="baseButton-header"] {
        background-color: transparent !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    button[data-testid="baseButton-header"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Botón hamburguesa para colapsar/expandir sidebar */
    button[kind="headerNoPadding"] {
        background-color: transparent !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    button[kind="headerNoPadding"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Iconos en el header (hamburguesa, config) */
    header[data-testid="stHeader"] svg {
        fill: #FFFFFF !important;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.8)) !important;
    }
    
    /* ============================================== */
    /* FONDO ORIGINAL - RESTAURADO */
    /* ============================================== */
    .stApp {
        background: linear-gradient(
            135deg,
            rgba(15, 15, 30, 0.95) 0%,
            rgba(25, 25, 50, 0.95) 50%,
            rgba(10, 10, 25, 0.95) 100%
        ), url('https://images.unsplash.com/photo-1542751371-adc38448a05e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2850&q=80') !important;

        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-blend-mode: overlay !important;
        min-height: 100vh;
    }

    /* Capa para mejorar legibilidad */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(10, 10, 20, 0.75);
        z-index: -1;
    }

    /* ============================================== */
    /* SIDEBAR - NEGRO PURO CON TRANSPARENCIA */
    /* ============================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            rgba(0, 0, 0, 0.95) 0%,
            rgba(10, 10, 10, 0.95) 50%,
            rgba(0, 0, 0, 0.95) 100%
        ) !important;
        border-right: 2px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    /* ============================================== */
    /* CONTENEDOR PRINCIPAL - NEGRO PURO ELEGANTE */
    /* ============================================== */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.92) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 16px;
        padding: 25px;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border: 2px solid rgba(255, 255, 255, 0.15);
        box-shadow:
            0 10px 40px rgba(0, 0, 0, 0.7),
            inset 0 0 20px rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    .main .block-container:hover {
        box-shadow:
            0 15px 50px rgba(0, 0, 0, 0.8),
            inset 0 0 30px rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.25);
    }

    /* ============================================== */
    /* TÍTULOS ELEGANTES - BLANCO CON SOMBRA */
    /* ============================================== */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }

    h1 {
        font-size: 2.8rem;
        text-align: center;
        padding-bottom: 15px;
        border-bottom: 3px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 2rem;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
    }

    h2 {
        font-size: 2.2rem;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.15);
    }

    /* ============================================== */
    /* BOTONES ELEGANTES - CONTRASTE SOBRE NEGRO */
    /* ============================================== */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a2e, #16213e) !important;
        color: #FFFFFF !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease !important;
        margin: 8px 0;
        cursor: pointer !important;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: 0.5s;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #22223b, #1d2d44) !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.7);
        border-color: rgba(255, 255, 255, 0.3);
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
    }

    /* ============================================== */
    /* INPUTS Y SELECTORES - NEGRO CON BORDES BLANCOS */
    /* ============================================== */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        background: rgba(20, 20, 20, 0.95) !important;
        color: #FFFFFF !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px;
        padding: 14px 16px !important;
        font-size: 1rem;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow:
            0 0 0 3px rgba(255, 255, 255, 0.1),
            inset 0 2px 5px rgba(0, 0, 0, 0.5) !important;
        background: rgba(25, 25, 25, 0.95) !important;
    }

    /* ============================================== */
    /* MULTISELECT - NEGRO ELEGANTE */
    /* ============================================== */
    .stMultiSelect>div>div {
        background: rgba(20, 20, 20, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px;
        min-height: 52px;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    .stMultiSelect>div>div:hover {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(40, 40, 40, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        margin: 4px;
        padding: 6px 12px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }

    .stMultiSelect [data-baseweb="tag"]:hover {
        background: rgba(50, 50, 50, 0.95) !important;
        transform: scale(1.05);
        border-color: rgba(255, 255, 255, 0.3);
    }

    /* ============================================== */
    /* TABS - NEGRO CON ACENTOS */
    /* ============================================== */
    .stTabs {
        margin-top: 2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10, 10, 10, 0.95) !important;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        gap: 5px;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #AAAAAA !important;
        border-radius: 8px;
        padding: 12px 24px;
        margin: 0 3px;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a1a2e, #16213e) !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transform: translateY(-2px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* ============================================== */
    /* BADGES PARA TIPOS DE EVENTOS */
    /* ============================================== */
    .event-type-badge {
        display: inline-block;
        padding: 6px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
        margin: 5px;
        border: 2px solid;
        color: #000000;
        text-shadow: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }

    .scrim-badge {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        border-color: #FF6B6B;
    }

    .duelo-badge {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        border-color: #4ECDC4;
    }

    .practica-badge {
        background: linear-gradient(135deg, #FFA500, #FFD700);
        border-color: #FFA500;
    }

    .analisis-badge {
        background: linear-gradient(135deg, #7B68EE, #9370DB);
        border-color: #7B68EE;
    }

    /* ============================================== */
    /* ALERTAS - NEGRO CON BORDES */
    /* ============================================== */
    .stAlert {
        background-color: rgba(15, 15, 15, 0.95) !important;
        border-radius: 12px;
        border-left: 6px solid;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }

    /* ============================================== */
    /* MÉTRICAS - NEGRO ELEGANTE */
    /* ============================================== */
    .stMetric {
        background: rgba(15, 15, 15, 0.95) !important;
        border-radius: 14px;
        padding: 20px;
        border: 2px solid rgba(255, 255, 255, 0.15);
        box-shadow:
            0 6px 20px rgba(0, 0, 0, 0.6),
            inset 0 0 15px rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.8),
            inset 0 0 20px rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.25);
    }

    .stMetric [data-testid="stMetricLabel"] {
        color: #CCCCCC !important;
        font-weight: 600;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }

    .stMetric [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.8);
    }

    .stMetric [data-testid="stMetricDelta"] {
        color: #AAAAAA !important;
    }

    /* ============================================== */
    /* PROGRESS BARS */
    /* ============================================== */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    /* ============================================== */
    /* EXPANDERS - NEGRO CON DETALLES */
    /* ============================================== */
    .streamlit-expanderHeader {
        background: rgba(20, 20, 20, 0.95) !important;
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.15);
        font-weight: 600;
        color: #FFFFFF;
        padding: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }

    .streamlit-expanderHeader:hover {
        background: rgba(30, 30, 30, 0.95) !important;
        border-color: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
    }

    /* ============================================== */
    /* SCROLLBAR ELEGANTE */
    /* ============================================== */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(20, 20, 20, 0.8);
        border-radius: 6px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
        border-radius: 6px;
        border: 3px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #22223b, #1d2d44);
        border-color: rgba(255, 255, 255, 0.25);
    }

    /* ============================================== */
    /* TEXTO GENERAL - BLANCO SOBRE NEGRO */
    /* ============================================== */
    p, label, span, .st-c8, .st-c9, .st-c10, .st-c7, .st-cq {
        color: #DDDDDD !important;
        font-weight: 400;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
    }

    strong, b {
        color: #FFFFFF !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
    }

    .sidebar .stMarkdown {
        color: #FFFFFF !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }

    /* ============================================== */
    /* SLIDERS - SOBRE NEGRO */
    /* ============================================== */
    .stSlider > div > div > div {
        background: rgba(40, 40, 40, 0.5) !important;
        border-radius: 10px;
        height: 10px;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #1a1a2e, #16213e) !important;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    .stSlider > div > div > div > div > div {
        background: #FFFFFF !important;
        border: 2px solid #1a1a2e;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    /* ============================================== */
    /* TOAST NOTIFICATIONS */
    /* ============================================== */
    .stNotification {
        background: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        backdrop-filter: blur(15px);
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.8);
    }

    /* ============================================== */
    /* CHECKBOXES */
    /* ============================================== */
    .stCheckbox > label {
        color: #DDDDDD !important;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
    }

    .stCheckbox > div > div {
        background: rgba(20, 20, 20, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    /* ============================================== */
    /* SELECTBOX ARROW */
    /* ============================================== */
    .stSelectbox svg {
        fill: #FFFFFF !important;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.8));
    }

    /* ============================================== */
    /* SUCCESS/ERROR/WARNING/INFO MESSAGES */
    /* ============================================== */
    .stSuccess {
        background: rgba(20, 40, 20, 0.9) !important;
        border-color: rgba(100, 255, 100, 0.3) !important;
    }

    .stError {
        background: rgba(40, 20, 20, 0.9) !important;
        border-color: rgba(255, 100, 100, 0.3) !important;
    }

    .stWarning {
        background: rgba(40, 40, 20, 0.9) !important;
        border-color: rgba(255, 255, 100, 0.3) !important;
    }

    .stInfo {
        background: rgba(20, 20, 40, 0.9) !important;
        border-color: rgba(100, 100, 255, 0.3) !important;
    }

    /* ============================================== */
    /* RADIO BUTTONS */
    /* ============================================== */
    .stRadio > div {
        background: rgba(20, 20, 20, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px;
        padding: 10px;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5);
    }

    /* ============================================== */
    /* DIVIDERS */
    /* ============================================== */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 25px 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
    }
</style>
"""

st.markdown(css_completo_negro_puro, unsafe_allow_html=True)

# ==============================================
# 4. FUNCIONES AUXILIARES PARA TIPOS DE EVENTOS
# ==============================================

def get_event_type_badge(event_type):
    """Devuelve el badge HTML para el tipo de evento"""
    badges = {
        "scrim": "🏆 Scrim",
        "1v1": "⚔️ Duelo 1v1",
        "practica": "🎯 Práctica",
        "analisis": "📊 Análisis",
        "torneo": "🏅 Torneo",
    }
    colors = {
        "scrim": "scrim-badge",
        "1v1": "duelo-badge",
        "practica": "practica-badge",
        "analisis": "analisis-badge",
        "torneo": "scrim-badge",  # Mismo color que scrim
    }
    badge_text = badges.get(event_type, "🏆 Evento")
    badge_class = colors.get(event_type, "scrim-badge")

    return f'<span class="event-type-badge {badge_class}">{badge_text}</span>'

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

# ==============================================
# 5. SIDEBAR - NEGRA PURO CON DETALLES
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
            ESPORTS SCHEDULER PRO v6.1
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Estadísticas en tiempo real (con cache)
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
        elif "torneo" in event_name or "tornament" in event_name or "competencia" in event_name:
            event_types_count["torneo"] += 1
        else:
            event_types_count["scrim"] += 1

    for event_type, count in event_types_count.items():
        if count > 0:
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
    st.markdown("**🎨 DISEÑO MEJORADO**")
    st.caption("• Fondo original restaurado")
    st.caption("• Paneles negros puros elegantes")
    st.caption("• Selectores de hora fáciles")
    st.caption("• Interfaz profesional oscura")

# ==============================================
# 6. TÍTULO PRINCIPAL
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
            <strong>Sistema profesional con 5 tipos de eventos • Versión 6.1 Mejoras Completas</strong><br>
            <span style='font-size: 1rem; color: #CCCCCC;'>
                🏆 Scrim 5v5 • ⚔️ Duelo 1v1 • 🎯 Práctica • 📊 Análisis • 🏅 Torneo
            </span>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================
# 7. TABS PRINCIPALES
# ==============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📅 EVENTOS", "➕ AGREGAR", "🔍 BUSCAR", "🗑️ ELIMINAR", "📊 DETALLES", "⚙️ SISTEMA"]
)

# ==============================================
# TAB 1: Eventos Planificados (MEJORADO)
# ==============================================
with tab1:
    st.header("📅 CALENDARIO DE EVENTOS")

    if scheduler.events:
        ahora = datetime.now()
        eventos_futuros = [e for e in scheduler.events if e["end"] > ahora]
        eventos_pasados = [e for e in scheduler.events if e["end"] <= ahora]

        # Eventos futuros
        if eventos_futuros:
            st.subheader(f"🟢 PRÓXIMOS EVENTOS ({len(eventos_futuros)})")
            for i, evento in enumerate(eventos_futuros[:5]):
                # Determinar tipo de evento
                event_type = "scrim"
                event_name = evento["name"].lower()
                if "1v1" in event_name or "duelo" in event_name:
                    event_type = "1v1"
                elif "práctica" in event_name or "practica" in event_name:
                    event_type = "practica"
                elif "análisis" in event_name or "analisis" in event_name:
                    event_type = "analisis"
                elif "torneo" in event_name or "tornament" in event_name:
                    event_type = "torneo"

                badge_html = get_event_type_badge(event_type)

                with st.expander(
                    f"{badge_html} **{i+1}. {evento['name']}** | {evento['start'].strftime('%d/%m %H:%M')} - {evento['end'].strftime('%H:%M')}",
                    expanded=(i == 0),
                ):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown("**📋 RECURSOS ASIGNADOS:**")

                        jugadores = [
                            r for r in evento["resources"] if r in scheduler.jugadores
                        ]
                        heroes = [
                            r for r in evento["resources"] if r in scheduler.all_heroes
                        ]
                        instalaciones = [
                            r
                            for r in evento["resources"]
                            if r in scheduler.instalaciones
                        ]

                        if jugadores:
                            st.markdown(f"**👥 JUGADORES ({len(jugadores)}):**")
                            for j in jugadores[:5]:
                                st.markdown(f"• {j}")
                            if len(jugadores) > 5:
                                st.markdown(f"• ... y {len(jugadores) - 5} más")

                        if heroes:
                            st.markdown(f"**⚔️ HÉROES ({len(heroes)}):**")
                            for h in heroes[:3]:
                                nombre_heroe = h.split(": ")[1] if ": " in h else h
                                st.markdown(f"• {nombre_heroe}")
                            if len(heroes) > 3:
                                st.markdown(f"• ... y {len(heroes) - 3} más")

                        if instalaciones:
                            st.markdown(f"**🏢 INSTALACIONES ({len(instalaciones)}):**")
                            for inst in instalaciones:
                                st.markdown(f"• {inst}")

                    with col2:
                        duracion = (evento["end"] - evento["start"]).seconds // 60
                        st.metric("⏱️ DURACIÓN", f"{duracion} min")
                        st.metric("🔧 RECURSOS", len(evento["resources"]))
                        st.metric("🎮 TIPO", event_type.upper())

            if len(eventos_futuros) > 5:
                st.info(f"📋 Mostrando 5 de {len(eventos_futuros)} eventos futuros")

        # Eventos pasados
        if eventos_pasados:
            st.subheader(f"🔴 HISTORIAL ({len(eventos_pasados)})")
            for evento in eventos_pasados[:3]:
                event_type = "scrim"
                event_name = evento["name"].lower()
                if "1v1" in event_name or "duelo" in event_name:
                    event_type = "1v1"
                elif "torneo" in event_name or "tornament" in event_name:
                    event_type = "torneo"

                badge_html = get_event_type_badge(event_type)

                with st.expander(
                    f"{badge_html} {evento['name']} - {evento['start'].strftime('%d/%m %H:%M')}",
                    expanded=False,
                ):
                    st.markdown(
                        f"**Horario:** {evento['start'].strftime('%H:%M')} - {evento['end'].strftime('%H:%M')}"
                    )
                    st.markdown(f"**Recursos:** {len(evento['resources'])} asignados")
                    st.markdown(f"**Tipo:** {event_type}")
    else:
        st.info(
            """
            🎯 **NO HAY EVENTOS PLANIFICADOS**

            Para comenzar:
            1. Ve a la pestaña **➕ AGREGAR**
            2. Selecciona el tipo de evento
            3. Completa los recursos específicos
            4. El sistema validará automáticamente
            """
        )

# ==============================================
# TAB 2: Agregar Nuevo Evento (CON SELECTORES DE HORA EN NEGRO)
# ==============================================
with tab2:
    st.header("➕ AGREGAR NUEVO EVENTO")

    # VERIFICAR SI HAY DATOS PREDEFINIDOS DE BÚSQUEDA
    usar_datos_predefinidos = False
    if "nombre_predef" in st.session_state and "recursos_predef" in st.session_state:
        usar_datos_predefinidos = True
        st.success("📋 **DATOS DE BÚSQUEDA CARGADOS AUTOMÁTICAMENTE**")
        st.info(
            f"Evento: {st.session_state['nombre_predef']} | Recursos: {len(st.session_state['recursos_predef'])}"
        )

    # Selección de tipo de evento
    st.markdown("### 🎮 SELECCIONA EL TIPO DE EVENTO")

    if usar_datos_predefinidos and "selected_event_type" in st.session_state:
        event_type = st.session_state["selected_event_type"]
    else:
        event_type = st.session_state.get("selected_event_type", "scrim")

    # Botones de selección de tipo
    col_type1, col_type2, col_type3, col_type4, col_type5 = st.columns(5)

    with col_type1:
        if st.button("🏆 Scrim 5v5", use_container_width=True, key="btn_scrim"):
            st.session_state.selected_event_type = "scrim"
            st.rerun()

    with col_type2:
        if st.button("⚔️ Duelo 1v1", use_container_width=True, key="btn_1v1"):
            st.session_state.selected_event_type = "1v1"
            st.rerun()

    with col_type3:
        if st.button("🎯 Práctica", use_container_width=True, key="btn_practica"):
            st.session_state.selected_event_type = "practica"
            st.rerun()

    with col_type4:
        if st.button("📊 Análisis", use_container_width=True, key="btn_analisis"):
            st.session_state.selected_event_type = "analisis"
            st.rerun()

    with col_type5:
        if st.button("🏅 Torneo", use_container_width=True, key="btn_torneo"):
            st.session_state.selected_event_type = "torneo"
            st.rerun()

    reqs = get_event_type_requirements(event_type)

    st.markdown(
        f"""
    <div style='
        background: linear-gradient(90deg, rgba(0, 0, 0, 0.8), rgba(20, 20, 30, 0.8));
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        border-left: 5px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(8px);
        box-shadow:
            0 4px 15px rgba(0, 0, 0, 0.6),
            inset 0 0 15px rgba(255, 255, 255, 0.03);
    '>
        <h4 style='color: #FFFFFF; text-shadow: 0 2px 5px rgba(0, 0, 0, 0.8); margin: 0 0 10px 0;'>{reqs['icon']} {reqs['name']}</h4>
        <p style='color: #CCCCCC; margin: 0 0 10px 0; font-size: 1em;'>{reqs['description']}</p>
        <p style='color: #999999; margin: 0; font-size: 0.9em;'>
            • Jugadores: {reqs['min_players']}-{reqs['max_players']} • Héroes: {reqs['min_heroes']}+ • Duración: {reqs['duration_min']}-{reqs['duration_max']}min
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Formulario en dos columnas
    col1, col2 = st.columns(2)

    with col1:
        # NOMBRE DEL EVENTO
        nombre_default = st.session_state.get("nombre_predef", "")
        nombre = st.text_input(
            f"🏷️ **NOMBRE DEL EVENTO*** ({reqs['icon']} {reqs['name'].split(' ')[0]})",
            value=nombre_default,
            placeholder=(
                f"Ej: {reqs['name'].split(' ')[0]} vs Team Flash"
                if event_type == "scrim"
                else f"Ej: {reqs['name']} - Especificar"
            ),
            help=f"Nombre descriptivo del evento {reqs['name']}",
            key="add_nombre",
        )

        # FECHA Y HORA
        st.markdown("### 📅 **SELECCIONAR FECHA Y HORA**")

        # Fecha
        fecha_actual = datetime.now()

        # Determinar fecha por defecto
        if usar_datos_predefinidos and "fecha_predef" in st.session_state:
            try:
                fecha_predef = datetime.fromisoformat(st.session_state["fecha_predef"])
                fecha_por_defecto = fecha_predef.date()
            except:  # noqa: E722
                fecha_por_defecto = fecha_actual.date() + timedelta(days=1)
        else:
            fecha_por_defecto = fecha_actual.date() + timedelta(days=1)

        fecha_minima = fecha_actual.date()
        fecha_maxima = (fecha_actual + timedelta(days=30)).date()

        fecha_seleccionada = st.date_input(
            "**FECHA:**",
            value=fecha_por_defecto,
            min_value=fecha_minima,
            max_value=fecha_maxima,
            key="add_fecha_select",
        )

        # Hora
        st.markdown("**HORA:**")

        # Determinar hora por defecto
        hora_por_defecto = "18:00"
        if usar_datos_predefinidos and "fecha_predef" in st.session_state:
            try:
                fecha_predef = datetime.fromisoformat(st.session_state["fecha_predef"])
                hora_por_defecto = fecha_predef.strftime("%H:%M")
            except:  # noqa: E722
                hora_por_defecto = "18:00"

        # Botones rápidos para horas comunes
        if event_type == "scrim":
            suggested_times = ["16:00", "18:00", "20:00", "22:00"]
        elif event_type == "1v1":
            suggested_times = ["15:00", "17:00", "19:00", "21:00"]
        elif event_type == "practica":
            suggested_times = ["14:00", "16:00", "18:00", "20:00"]
        elif event_type == "torneo":
            suggested_times = ["15:00", "17:00", "19:00", "21:00"]
        else:
            suggested_times = ["15:00", "17:00", "19:00", "21:00"]

        col_horas = st.columns(4)
        hora_seleccionada = None

        for idx, hora in enumerate(suggested_times):
            with col_horas[idx]:
                if st.button(
                    f"{hora}", key=f"hora_btn_{idx}", use_container_width=True
                ):
                    hora_seleccionada = hora
                    st.session_state.selected_hour = hora

        # También permitir selección manual
        if "selected_hour" not in st.session_state:
            st.session_state.selected_hour = hora_por_defecto

        hora_manual = st.text_input(
            "**O ingresa hora manualmente (HH:MM):**",
            value=st.session_state.get("selected_hour", hora_por_defecto),
            placeholder="Ej: 18:30",
            key="add_hora_manual",
        )

        # Convertir a formato ISO
        if hora_seleccionada:
            hora_final = hora_seleccionada
        else:
            hora_final = hora_manual if hora_manual else hora_por_defecto

        # Validar formato de hora
        try:
            datetime.strptime(hora_final, "%H:%M")
            hora_valida = True
        except ValueError:
            hora_valida = False
            st.error("⚠️ Formato de hora inválido. Usa HH:MM (ej: 18:30)")

        # Crear fecha y hora final en formato ISO
        fecha_hora_iso = f"{fecha_seleccionada}T{hora_final}"

        # Mostrar fecha y hora seleccionada
        st.info(
            f"**📅 Fecha y hora seleccionadas:** {fecha_seleccionada.strftime('%d/%m/%Y')} a las {hora_final}"
        )

        # DURACIÓN
        duracion_default = st.session_state.get(
            "duracion_predef", min(60, reqs["duration_max"])
        )
        duracion = st.slider(
            f"⏱️ **DURACIÓN (MINUTOS)*** [{reqs['duration_min']}-{reqs['duration_max']}]",
            min_value=reqs["duration_min"],
            max_value=reqs["duration_max"],
            value=duracion_default,
            step=5,
            help=f"Duración recomendada para {reqs['name']}",
            key="add_duracion",
        )

    with col2:
        st.markdown(
            f"### 🔧 RECURSOS PARA {reqs['icon']} {reqs['name'].split(' ')[0].upper()}"
        )

        # RECURSOS (PRECARGAR SI HAY DATOS)
        if usar_datos_predefinidos:
            # Separar recursos predefinidos por categoría
            recursos_predef = st.session_state.get("recursos_predef", [])
            jugadores_predef = [r for r in recursos_predef if r in scheduler.jugadores]
            heroes_predef = [r for r in recursos_predef if r in scheduler.all_heroes]
            instalaciones_predef = [
                r for r in recursos_predef if r in scheduler.instalaciones
            ]
        else:
            jugadores_predef = []
            heroes_predef = []
            instalaciones_predef = []

        # Tabs para cada categoría
        tab_jug, tab_her, tab_inst = st.tabs(["Jugadores", "Héroes", "Instalaciones"])

        with tab_jug:
            # Configurar valores por defecto según tipo O PREDEFINIDOS
            if usar_datos_predefinidos and jugadores_predef:
                default_players = jugadores_predef
            else:
                default_players = []
                if event_type == "scrim":
                    default_players = (
                        scheduler.jugadores[:5]
                        if len(scheduler.jugadores) >= 5
                        else scheduler.jugadores
                    )
                elif event_type == "1v1":
                    default_players = (
                        scheduler.jugadores[:2]
                        if len(scheduler.jugadores) >= 2
                        else scheduler.jugadores
                    )
                elif event_type == "practica":
                    default_players = (
                        scheduler.jugadores[:1] if scheduler.jugadores else []
                    )
                elif event_type == "torneo":
                    default_players = (
                        scheduler.jugadores[:5]
                        if len(scheduler.jugadores) >= 5
                        else scheduler.jugadores
                    )
                else:
                    default_players = (
                        scheduler.jugadores[:3]
                        if len(scheduler.jugadores) >= 3
                        else scheduler.jugadores
                    )

            jugadores_seleccionados = st.multiselect(
                f"Seleccionar Jugadores ({reqs['min_players']}-{reqs['max_players']}):",
                scheduler.jugadores,
                default=default_players,
                help=f"Debes seleccionar entre {reqs['min_players']} y {reqs['max_players']} jugadores",
                key="add_jugadores",
                max_selections=reqs["max_players"],
            )

        with tab_her:
            # Filtro por rol
            st.markdown("**Filtrar por rol:**")
            roles = ["Todos", "Assassins", "Fighters", "Mages", "Marksmen", "Supports", "Tanks"]
            rol_seleccionado = st.selectbox(
                "Rol del héroe:",
                roles,
                index=0,
                key="filter_role",
                label_visibility="collapsed",
            )

            # Obtener héroes según filtro
            heroes_opciones = scheduler.get_heroes_by_role(rol_seleccionado)

            # VALOR POR DEFECTO INTELIGENTE según tipo O PREDEFINIDOS
            if usar_datos_predefinidos and heroes_predef:
                default_value = heroes_predef
            else:
                default_value = []
                if heroes_opciones:
                    if event_type == "1v1" and len(heroes_opciones) >= 2:
                        default_value = heroes_opciones[:2]
                    elif event_type == "scrim" and len(heroes_opciones) >= 5:
                        default_value = heroes_opciones[: min(5, len(heroes_opciones))]
                    elif event_type == "torneo" and len(heroes_opciones) >= 5:
                        default_value = heroes_opciones[: min(5, len(heroes_opciones))]
                    elif heroes_opciones:
                        default_value = [heroes_opciones[0]]

            max_selections = (
                10 if event_type in ["scrim", "torneo"] else (2 if event_type == "1v1" else 5)
            )

            heroes_seleccionados = st.multiselect(
                f"Seleccionar Héroes (mínimo {len(jugadores_seleccionados)}):",
                heroes_opciones,
                default=default_value,
                help=f"Se necesitan al menos {len(jugadores_seleccionados)} héroe(s) para {len(jugadores_seleccionados)} jugadores",
                key="add_heroes",
                max_selections=max_selections,
            )

        with tab_inst:
            # Sugerencias según tipo de evento
            suggested_installations = []
            if event_type == "1v1":
                suggested_installations = [
                    "Sala de Duelo 1v1",
                    "Dispositivo Android Elite",
                ]
            elif event_type == "scrim":
                suggested_installations = [
                    "Sala de Práctica 1",
                    "Sala de Práctica 2",
                    "Dispositivo Android Pro",
                ]
            elif event_type == "practica":
                suggested_installations = [
                    "Sala de Práctica Individual",
                    "Dispositivo Android Pro",
                ]
            elif event_type == "analisis":
                suggested_installations = [
                    "Sala de Análisis",
                    "Dispositivo Android Pro",
                ]
            elif event_type == "torneo":
                suggested_installations = [
                    "Sala de Torneo (VIP)",
                    "Estación de Transmisión",
                    "Área de Prensa",
                    "Dispositivo Android Pro",
                ]

            # Filtrar sugerencias disponibles
            if usar_datos_predefinidos and instalaciones_predef:
                default_installations = instalaciones_predef
            else:
                default_installations = [
                    inst
                    for inst in suggested_installations
                    if inst in scheduler.instalaciones
                ]
                if not default_installations and scheduler.instalaciones:
                    default_installations = [scheduler.instalaciones[0]]

            instalaciones_seleccionadas = st.multiselect(
                "Seleccionar Instalaciones (solo UNA sala):",
                scheduler.instalaciones,
                default=default_installations,
                help=f"Se recomienda: {', '.join(suggested_installations[:3])}. ¡Solo se puede seleccionar UNA sala!",
                key="add_instalaciones",
            )

    # Combinar todos los recursos seleccionados
    recursos = (
        jugadores_seleccionados + heroes_seleccionados + instalaciones_seleccionadas
    )

    # Mostrar validación en tiempo real
    if recursos or nombre:
        st.markdown("### 📋 VALIDACIÓN EN TIEMPO REAL")

        # Validar según tipo de evento
        errors, warnings = validate_event_resources(
            event_type,
            jugadores_seleccionados,
            heroes_seleccionados,
            instalaciones_seleccionadas,
        )

        col_val1, col_val2, col_val3 = st.columns(3)

        with col_val1:
            st.markdown(
                f"**👤 JUGADORES** ({reqs['min_players']}-{reqs['max_players']})"
            )
            st.write(f"{len(jugadores_seleccionados)} seleccionados")
            if len(jugadores_seleccionados) < reqs["min_players"]:
                st.error(f"❌ Mínimo {reqs['min_players']} requerido")
            elif len(jugadores_seleccionados) > reqs["max_players"]:
                st.error(f"❌ Máximo {reqs['max_players']} permitido")
            else:
                st.success("✅ OK")

        with col_val2:
            st.markdown(f"**⚔️ HÉROES** (mínimo {len(jugadores_seleccionados)})")
            st.write(f"{len(heroes_seleccionados)} seleccionados")
            if len(heroes_seleccionados) < len(jugadores_seleccionados):
                st.error(f"❌ Se necesitan al menos {len(jugadores_seleccionados)} héroes")
            elif len(heroes_seleccionados) < reqs["min_heroes"]:
                st.warning(f"⚠️ Mínimo {reqs['min_heroes']} recomendado para {reqs['name']}")
            else:
                # Validación específica por tipo de evento
                if event_type in ["scrim", "torneo"]:
                    # Verificar que cada jugador tenga héroe de su posición
                    posiciones_ok = True
                    for jugador in jugadores_seleccionados:
                        posicion_jugador = extraer_posicion_jugador(jugador)
                        if posicion_jugador:
                            tiene_heroe = False
                            for heroe in heroes_seleccionados:
                                posicion_heroe = extraer_posicion_heroe(heroe)
                                if posicion_heroe and posicion_heroe.lower() == posicion_jugador.lower():
                                    tiene_heroe = True
                                    break
                            
                            if not tiene_heroe:
                                st.warning(f"⚠️ {jugador} necesita héroe {posicion_jugador}")
                                posiciones_ok = False
                    
                    if posiciones_ok:
                        st.success("✅ Cada jugador tiene héroe de su posición")
                else:
                    st.success("✅ OK (sin restricción de posición)")

        with col_val3:
            st.markdown("**🏢 INSTALACIONES**")
            st.write(f"{len(instalaciones_seleccionadas)} seleccionadas")

            # Validación especial para salas y dispositivos
            salas = [i for i in instalaciones_seleccionadas if "Sala" in i]
            dispositivos = [
                i for i in instalaciones_seleccionadas if "Dispositivo" in i
            ]

            if len(salas) > 1:
                st.error("❌ Solo se puede seleccionar UNA sala por evento")
            elif not salas:
                st.error("❌ Se requiere al menos una sala")
            elif not dispositivos:
                st.error("❌ Se requiere al menos un dispositivo")
            else:
                # Validación especial para torneo
                if event_type == "torneo":
                    if "Sala de Torneo (VIP)" not in salas:
                        st.error("❌ Los torneos requieren Sala de Torneo (VIP)")
                    elif "Estación de Transmisión" not in instalaciones_seleccionadas:
                        st.error("❌ Los torneos requieren Estación de Transmisión")
                    elif "Área de Prensa" not in instalaciones_seleccionadas:
                        st.error("❌ Los torneos requieren Área de Prensa")
                    else:
                        st.success("✅ OK")
                elif event_type == "1v1" and "Dispositivo Android Elite" not in dispositivos:
                    st.warning("⚠️ Para 1v1 se recomienda Dispositivo Android Elite")
                else:
                    st.success("✅ OK")

        # Mostrar errores y advertencias
        if errors:
            st.error("**❌ ERRORES DE VALIDACIÓN:**")
            for error in errors:
                st.markdown(f"• {error}")

        if warnings:
            st.warning("**⚠️ ADVERTENCIAS:**")
            for warning in warnings:
                st.markdown(f"• {warning}")

        st.markdown(f"**📊 TOTAL DE RECURSOS:** {len(recursos)}")

    # Botón de acción
    st.markdown("---")

    if st.button(
        f"✅ **CONFIRMAR Y AGENDAR {reqs['name'].upper().split(' ')[0]}**",
        type="primary",
        use_container_width=True,
        key="btn_agregar_fixed",
    ):
        # Validación básica
        if not nombre:
            st.error("⚠️ **ERROR:** El nombre del evento es requerido")
        elif not hora_valida:
            st.error("⚠️ **ERROR:** La hora seleccionada no es válida")
        else:
            # Validación específica por tipo
            errors, warnings = validate_event_resources(
                event_type,
                jugadores_seleccionados,
                heroes_seleccionados,
                instalaciones_seleccionadas,
            )

            if errors:
                st.error("**❌ ERRORES DE VALIDACIÓN:** No se puede crear el evento")
                for error in errors[:3]:
                    st.markdown(f"• {error}")
            else:
                try:
                    # Mostrar spinner
                    with st.spinner(
                        f"🔄 **CREANDO {reqs['name'].upper().split(' ')[0]}...**"
                    ):
                        # Pequeño delay para estabilidad
                        time.sleep(0.5)
                        success = scheduler.add_event(
                            nombre, fecha_hora_iso, duracion, recursos
                        )

                    if success:
                        st.success(
                            f"🎉 **¡{reqs['name'].upper().split(' ')[0]} AGENDADO EXITOSAMENTE!**"
                        )
                        st.info(
                            f"📋 **{nombre}** creado para {fecha_seleccionada.strftime('%d/%m/%Y')} a las {hora_final}"
                        )

                        # Limpiar datos después de crear
                        if "selected_hour" in st.session_state:
                            del st.session_state.selected_hour

                        # Limpiar todos los datos predefinidos
                        claves_a_limpiar = [
                            "nombre_predef",
                            "fecha_predef",
                            "duracion_predef",
                            "recursos_predef",
                            "selected_event_type",
                        ]
                        for clave in claves_a_limpiar:
                            if clave in st.session_state:
                                del st.session_state[clave]

                        # Delay antes de recargar
                        time.sleep(1.5)
                        st.rerun()

                except ValueError as e:
                    st.error(f"❌ **ERROR DE VALIDACIÓN:**\n\n{str(e)}")
                except Exception as e:
                    st.error(f"💥 **ERROR INESPERADO:** {str(e)}")

# ==============================================
# TAB 3: Buscar Hueco Disponible - COMPLETAMENTE CORREGIDO
# ==============================================
with tab3:
    st.header("🔍 BUSCAR HUECO DISPONIBLE")

    st.markdown("""
    **Encuentra automáticamente el próximo horario libre** que cumpla con todas las restricciones  
    y **crea el evento directamente desde aquí** ⚡
    
    ⚠️ **NOTA:** Los huecos se buscan con al menos 10 minutos de anticipación para evitar errores de tiempo.
    """)

    col_tipo, col_dur = st.columns(2)
    with col_tipo:
        tipo_busqueda = st.selectbox(
            "**Tipo de evento a buscar:**",
            options=["scrim", "1v1", "practica", "analisis", "torneo"],
            format_func=lambda x: get_event_type_requirements(x)["name"],
            index=0,
            key="tipo_busqueda_tab3"
        )

    with col_dur:
        reqs = get_event_type_requirements(tipo_busqueda)
        duracion_busqueda = st.slider(
            "**Duración del evento (minutos):**",
            min_value=reqs["duration_min"],
            max_value=reqs["duration_max"],
            value=reqs["duration_min"],
            step=10,
            help="Ajustada automáticamente al tipo de evento",
            key="duracion_busqueda_tab3"
        )

    # Recursos según tipo
    st.markdown(f"### 📋 Recursos requeridos para {reqs['name']}")
    
    # Inicializar variables
    jugadores_seleccionados = []
    heroes_seleccionados = []
    instalaciones_seleccionadas = []
    
    # Jugadores
    st.markdown("**👥 Jugadores necesarios**")
    jugadores_seleccionados = st.multiselect(
        f"Selecciona jugadores (mínimo {reqs['min_players']}, máximo {reqs['max_players']})",
        options=scheduler.jugadores,
        default=scheduler.jugadores[:min(reqs['min_players'], len(scheduler.jugadores))],
        key="jugadores_busq_tab3"
    )
    
    # Héroes
    if jugadores_seleccionados:
        st.markdown("**⚔️ Héroes a practicar/jugar**")
        st.info(f"💡 Se requieren al menos {len(jugadores_seleccionados)} héroes (uno por jugador)")
        
        # Filtrar héroes por posición si es evento importante
        heroes_opciones = scheduler.all_heroes
        if tipo_busqueda in ["scrim", "torneo"]:
            st.warning("🎯 **EVENTO IMPORTANTE:** Cada jugador debe seleccionar al menos un héroe de su posición")
            heroes_filtrados = []
            for jugador in jugadores_seleccionados:
                posicion_jugador = extraer_posicion_jugador(jugador)
                if posicion_jugador:
                    heroes_de_posicion = scheduler.get_heroes_by_position(posicion_jugador)
                    heroes_filtrados.extend(heroes_de_posicion)
            if heroes_filtrados:
                heroes_opciones = list(set(heroes_filtrados))
        
        heroes_seleccionados = st.multiselect(
            f"Selecciona al menos {len(jugadores_seleccionados)} héroes",
            options=heroes_opciones,
            default=heroes_opciones[:min(len(jugadores_seleccionados), len(heroes_opciones))],
            key="heroes_busq_tab3"
        )

    # Instalaciones
    st.markdown("**🏢 Instalaciones requeridas**")
    
    # Sugerencias según tipo de evento
    sugerencias_instalaciones = reqs.get("installations", ["Sala de Práctica 1"])
    sugerencias_dispositivos = reqs.get("devices", ["Dispositivo Android Pro"])
    
    # Filtrar solo las instalaciones que existen
    sugerencias_filtradas = []
    for inst in sugerencias_instalaciones + sugerencias_dispositivos:
        if inst in scheduler.instalaciones:
            sugerencias_filtradas.append(inst)
    
    instalaciones_seleccionadas = st.multiselect(
        "Selecciona instalaciones (solo UNA sala permitida)",
        options=scheduler.instalaciones,
        default=sugerencias_filtradas,
        key="instalaciones_busq_tab3"
    )

    # Nombre del evento
    st.markdown("**🏷️ Nombre del evento**")
    nombre_evento = st.text_input(
        "Nombre único y descriptivo (obligatorio)",
        value=f"{reqs['name'].split(' ')[0]} Práctica",
        placeholder=f"Ej: {reqs['name'].split(' ')[0]} vs Nova Esports",
        help="Debe ser único. Ejemplos: 'Scrim Intensivo', 'Práctica Ao Yin', 'Torneo KPL Prep'",
        key="nombre_evento_busq_tab3"
    )

    # Combinar todos los recursos
    recursos_busqueda = jugadores_seleccionados + heroes_seleccionados + instalaciones_seleccionadas
    
    # Validación previa
    errores_validacion = []
    if jugadores_seleccionados:
        if len(jugadores_seleccionados) < reqs["min_players"]:
            errores_validacion.append(f"❌ Se requieren mínimo {reqs['min_players']} jugadores")
        if len(jugadores_seleccionados) > reqs["max_players"]:
            errores_validacion.append(f"❌ Máximo {reqs['max_players']} jugadores permitidos")
    
    if heroes_seleccionados and len(heroes_seleccionados) < len(jugadores_seleccionados):
        errores_validacion.append(f"❌ Se necesitan al menos {len(jugadores_seleccionados)} héroes para {len(jugadores_seleccionados)} jugadores")
    
    # Validar salas
    salas_seleccionadas = [inst for inst in instalaciones_seleccionadas if "Sala" in inst]
    if len(salas_seleccionadas) > 1:
        errores_validacion.append("❌ Solo se puede seleccionar UNA sala por evento")
    elif not salas_seleccionadas:
        errores_validacion.append("❌ Se requiere al menos una sala")
    
    # Mostrar errores de validación
    if errores_validacion:
        st.error("**❌ ERRORES DE VALIDACIÓN:**")
        for error in errores_validacion:
            st.markdown(f"• {error}")

    # Botón de búsqueda
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        buscar_disabled = (len(errores_validacion) > 0 or 
                          not nombre_evento.strip() or 
                          not jugadores_seleccionados or 
                          not heroes_seleccionados or 
                          not instalaciones_seleccionadas)
        
        if st.button("🔍 BUSCAR PRÓXIMO HUECO", 
                    use_container_width=True, 
                    type="secondary",
                    disabled=buscar_disabled,
                    key="btn_buscar_hueco_tab3"):
            
            with st.spinner("🔍 Buscando hueco disponible (comienza en 10+ minutos, horario 9:00-22:00)..."):
                try:
                    inicio, fin = scheduler.find_next_slot(
                        duration_min=duracion_busqueda,
                        resources=recursos_busqueda,
                        max_hours=168
                    )

                    st.success(
                        f"✅ **¡HUECO ENCONTRADO!**\n\n"
                        f"📅 **Fecha:** {inicio.strftime('%A %d de %B %Y')}\n"
                        f"🕐 **Horario:** {inicio.strftime('%H:%M')} → {fin.strftime('%H:%M')} ({duracion_busqueda} min)\n"
                        f"📋 **Tipo:** {reqs['name']}"
                    )

                    # Guardar datos en el estado de sesión
                    st.session_state.busqueda_hueco_encontrado = {
                        "nombre": nombre_evento.strip(),
                        "inicio": inicio.isoformat(),
                        "duracion": duracion_busqueda,
                        "recursos": recursos_busqueda,
                        "tipo": tipo_busqueda,
                        "fecha_formateada": inicio.strftime('%d/%m/%Y %H:%M')
                    }
                    
                    # Mostrar botón de creación
                    st.rerun()

                except ValueError as e:
                    st.error(f"❌ **No se encontró hueco:** {str(e)}")
                    st.info("💡 Intenta con menos recursos, duración más corta o en otro horario")
                except Exception as e:
                    st.error(f"💥 **Error inesperado:** {str(e)}")

    # Botón de creación (solo visible si hay búsqueda exitosa)
    if "busqueda_hueco_encontrado" in st.session_state:
        datos = st.session_state.busqueda_hueco_encontrado
        
        with col_btn2:
            if st.button("✅ CREAR EVENTO EN ESTE HUECO", 
                        use_container_width=True, 
                        type="primary",
                        key="btn_crear_desde_busqueda_tab3"):
                
                try:
                    # Verificar que no exista evento con mismo nombre
                    nombre_limpio = datos["nombre"]
                    if any(e["name"].lower() == nombre_limpio.lower() for e in scheduler.events):
                        st.error(f"❌ Ya existe un evento con el nombre '{nombre_limpio}'")
                        st.stop()
                    
                    # Verificar que la fecha no sea en el pasado (seguridad adicional)
                    inicio_dt = datetime.fromisoformat(datos["inicio"])
                    if inicio_dt < datetime.now():
                        st.error("❌ El hueco encontrado ya está en el pasado. Por favor, busca de nuevo.")
                        del st.session_state.busqueda_hueco_encontrado
                        st.rerun()
                    
                    # Crear el evento
                    with st.spinner(f"🔄 Creando evento '{nombre_limpio}'..."):
                        success = scheduler.add_event(
                            name=nombre_limpio,
                            start_str=datos["inicio"],
                            duration_min=datos["duracion"],
                            resources=datos["recursos"]
                        )
                    
                    if success:
                        st.success(f"🏆 **¡Evento '{nombre_limpio}' creado exitosamente!**")
                        st.toast(f"✅ Evento creado para {datos['fecha_formateada']}", icon="🎉")
                        
                        # Limpiar estado de búsqueda
                        del st.session_state.busqueda_hueco_encontrado
                        
                        # Actualizar scheduler en estado de sesión
                        st.session_state.scheduler = scheduler
                        
                        # Forzar recarga de la página
                        time.sleep(2)
                        st.rerun()
                        
                except ValueError as e:
                    st.error(f"🚫 **Error de validación:**\n{str(e)}")
                    st.info("🔧 Verifica que los recursos cumplan todas las restricciones")
                except Exception as e:
                    st.error(f"💥 **Error inesperado al crear evento:** {str(e)}")

    # Separador e información
    st.markdown("---")
    
    # Mostrar detalles del hueco encontrado si existe
    if "busqueda_hueco_encontrado" in st.session_state:
        datos = st.session_state.busqueda_hueco_encontrado
        with st.expander("📋 **DETALLES DEL HUECO ENCONTRADO**", expanded=True):
            st.markdown(f"""
            **🏷️ Nombre del evento:** {datos['nombre']}
            
            **📅 Fecha y hora:** {datos['fecha_formateada']}
            
            **⏱️ Duración:** {datos['duracion']} minutos
            
            **👥 Jugadores:** {len([r for r in datos['recursos'] if r in scheduler.jugadores])}
            
            **⚔️ Héroes:** {len([r for r in datos['recursos'] if r in scheduler.all_heroes])}
            
            **🏢 Instalaciones:** {len([r for r in datos['recursos'] if r in scheduler.instalaciones])}
            
            ⚠️ **Este hueco está reservado temporalmente. Haz clic en 'CREAR EVENTO' para confirmar.**
            """)

    st.caption("🔍 La búsqueda comienza 10 minutos en el futuro • Horario laboral: 9:00-22:00 • Máximo: 7 días adelante")
# ==============================================
# TAB 4: Eliminar Evento (CORREGIDO)
# ==============================================
with tab4:
    st.header("🗑️ ELIMINAR EVENTO")

    if scheduler.events:
        ahora = datetime.now()
        eventos_futuros = [e for e in scheduler.events if e["end"] > ahora]

        if eventos_futuros:
            st.warning("⚠️ **Esta acción no se puede deshacer**")

            evento_opciones = [
                f"{e['name']} ({e['start'].strftime('%d/%m %H:%M')})"
                for e in eventos_futuros
            ]

            if evento_opciones:
                evento_seleccionado = st.selectbox(
                    "**SELECCIONA EVENTO A ELIMINAR:**",
                    evento_opciones,
                    key="eliminar_select_fixed",
                )

                evento_idx = evento_opciones.index(evento_seleccionado)
                evento = eventos_futuros[evento_idx]

                # Determinar tipo
                event_type = "scrim"
                event_name = evento["name"].lower()
                if "1v1" in event_name or "duelo" in event_name:
                    event_type = "1v1"
                elif "práctica" in event_name or "practica" in event_name:
                    event_type = "practica"
                elif "análisis" in event_name or "analisis" in event_name:
                    event_type = "analisis"
                elif "torneo" in event_name or "tornament" in event_name:
                    event_type = "torneo"

                badge_html = get_event_type_badge(event_type)

                # CORRECCIÓN: Mover el badge dentro del expander
                with st.expander(
                    f"📋 Ver detalles del evento: {evento['name']}", 
                    expanded=False
                ):
                    # Mostrar badge correctamente renderizado
                    st.markdown(badge_html, unsafe_allow_html=True)
                    
                    col_det1, col_det2 = st.columns(2)
                    
                    with col_det1:
                        st.markdown("**📅 FECHA Y HORA**")
                        st.write(f"• Inicio: {evento['start'].strftime('%d/%m/%Y %H:%M')}")
                        st.write(f"• Fin: {evento['end'].strftime('%H:%M')}")
                        st.write(f"• Duración: {(evento['end'] - evento['start']).seconds // 60} min")
                        
                    with col_det2:
                        st.markdown("**🔧 DETALLES**")
                        st.write(f"• Tipo: {event_type.upper()}")
                        st.write(f"• Recursos: {len(evento['resources'])} asignados")
                        
                        # Contar recursos por tipo
                        jugadores = len([r for r in evento["resources"] if r in scheduler.jugadores])
                        heroes = len([r for r in evento["resources"] if r in scheduler.all_heroes])
                        instalaciones = len([r for r in evento["resources"] if r in scheduler.instalaciones])
                        
                        st.write(f"• Jugadores: {jugadores}")
                        st.write(f"• Héroes: {heroes}")
                        st.write(f"• Instalaciones: {instalaciones}")

                confirmar = st.checkbox(
                    "✅ **Confirmo que quiero eliminar este evento**",
                    key="eliminar_confirm_fixed",
                )

                if st.button(
                    "🗑️ **ELIMINAR EVENTO**",
                    type="secondary",
                    disabled=not confirmar,
                    use_container_width=True,
                    key="btn_eliminar_fixed",
                ):
                    try:
                        indice_global = scheduler.events.index(evento)
                        evento_eliminado = scheduler.delete_event(indice_global)

                        st.success(
                            f"✅ **'{evento_eliminado['name']}' eliminado correctamente**"
                        )

                        # Delay antes de recargar
                        time.sleep(1.5)
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("📭 **No hay eventos futuros para eliminar**")
    else:
        st.info("📭 **No hay eventos en el sistema**")

# ==============================================
# TAB 5: Detalles y Agenda
# ==============================================
with tab5:
    st.header("📊 DETALLES Y AGENDA")

    if scheduler.events:
        evento_opciones = [
            f"{e['name']} - {e['start'].strftime('%d/%m %H:%M')}"
            for e in scheduler.events
        ]

        evento_seleccionado = st.selectbox(
            "**SELECCIONAR EVENTO:**",
            range(len(evento_opciones)),
            format_func=lambda i: evento_opciones[i],
            key="detalles_select_fixed",
        )

        if evento_seleccionado is not None:
            detalles = scheduler.get_event_details(evento_seleccionado)

            # Determinar tipo para mostrar badge
            evento = scheduler.events[evento_seleccionado]
            event_type = "scrim"
            event_name = evento["name"].lower()
            if "1v1" in event_name or "duelo" in event_name:
                event_type = "1v1"
            elif "práctica" in event_name or "practica" in event_name:
                event_type = "practica"
            elif "análisis" in event_name or "analisis" in event_name:
                event_type = "analisis"
            elif "torneo" in event_name or "tornament" in event_name:
                event_type = "torneo"

            badge_html = get_event_type_badge(event_type)

            st.markdown(f"{badge_html} **Tipo de evento:** {event_type.upper()}")
            st.text_area(
                "**📋 DETALLES COMPLETOS:**",
                detalles,
                height=300,
                key="detalles_area_fixed",
            )
    else:
        st.info("📭 **No hay eventos para mostrar**")

# ==============================================
# TAB 6: Sistema y Configuración
# ==============================================
with tab6:
    st.header("⚙️ SISTEMA Y CONFIGURACIÓN")

    col_sys1, col_sys2, col_sys3 = st.columns(3)

    with col_sys1:
        st.markdown("#### 🔧 RESTRICCIONES")
        st.metric("Co-requisitos", len(scheduler.restricciones["co_requisitos"]))
        st.metric("Exclusiones", len(scheduler.restricciones["exclusiones"]))
        st.metric("Tipos de eventos", 5)

    with col_sys2:
        st.markdown("#### 🗃️ RECURSOS")
        st.metric("Jugadores", len(scheduler.jugadores))
        st.metric("Héroes", len(scheduler.all_heroes))
        st.metric("Instalaciones", len(scheduler.instalaciones))

    with col_sys3:
        st.markdown("#### 💾 SISTEMA")
        st.metric("Eventos", len(scheduler.events))
        st.metric("Versión", "6.1 Mejoras Completas")

        if st.button(
            "🔄 Recargar datos", use_container_width=True, key="reload_data_fixed"
        ):
            scheduler.load_data()
            st.success("✅ Datos recargados")
            time.sleep(0.5)
            st.rerun()

    st.markdown("---")

    # Tipos de eventos configurados
    st.markdown("### 🎮 TIPOS DE EVENTOS CONFIGURADOS")

    event_cols = st.columns(5)
    event_types = ["scrim", "1v1", "practica", "analisis", "torneo"]

    for idx, event_type in enumerate(event_types):
        with event_cols[idx]:
            reqs = get_event_type_requirements(event_type)
            st.markdown(
                f"""
            <div style='
                background: rgba(0, 0, 0, 0.9);
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                border: 2px solid rgba(255, 255, 255, 0.15);
                margin-bottom: 10px;
                box-shadow:
                    0 4px 10px rgba(0, 0, 0, 0.6),
                    inset 0 0 10px rgba(255, 255, 255, 0.05);
            '>
                <div style='font-size: 2rem;'>{reqs['icon']}</div>
                <div style='font-weight: bold; color: #FFFFFF; text-shadow: 0 2px 5px rgba(0, 0, 0, 0.8);'>{reqs['name'].split(' ')[0]}</div>
                <div style='font-size: 0.8em; color: #AAAAAA;'>
                    {reqs['min_players']}-{reqs['max_players']} jugadores<br>
                    {reqs['duration_min']}-{reqs['duration_max']} min
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Información técnica
    with st.expander("📋 **ESPECIFICACIONES TÉCNICAS**", expanded=False):
        st.markdown(
            """
        **✅ SISTEMA COMPLETO IMPLEMENTADO:**

        • **5 Tipos de Eventos:** Scrim, 1v1, Práctica, Análisis, Torneo
        • **Validación mejorada:** Misma cantidad de héroes que jugadores
        • **Validación de posiciones:** En eventos importantes (scrim/torneo), jugadores DEBEN usar héroes de su posición
        • **Restricciones corregidas:** Solo una sala por evento
        • **Nombre único:** No se permiten eventos con mismo nombre
        • **Sala de Torneo VIP:** Con requisitos especiales (transmisión, prensa)
        • **Búsqueda inteligente:** Con creación directa de eventos
        • **Diseño Mejorado:** Fondo original con paneles negros puros
        • **Interfaz:** 6 tabs, diseño elegante oscuro, responsive

        **🎯 REGLAS POR TIPO DE EVENTO:**
        • 🏆 **Scrim (5v5):** 5-10 jugadores, sala grande, 45-180min, jugadores DEBEN usar héroes de su posición
        • ⚔️ **1v1 Duelo:** 2 jugadores exactos, Dispositivo Elite, 10-20min, sin restricción de posición
        • 🎯 **Práctica:** 1-3 jugadores, sala individual, 20-60min, sin restricción de posición
        • 📊 **Análisis:** 1-10 jugadores, sala de análisis, 30-90min, sin restricción de posición
        • 🏅 **Torneo:** 5-10 jugadores, Sala VIP, transmisión, prensa, 60-240min, jugadores DEBEN usar héroes de su posición

        **🎨 INTERFAZ MEJORADA:**
        • Fondo original con imagen de Honor of Kings
        • Paneles negros puros con transparencia
        • Texto blanco elegante con sombras
        • Bordes grises sutiles
        • Badges coloridos que contrastan
        """
        )

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
            🏆 <strong>Honor of Kings Esports Scheduler Pro v6.1</strong>
        </p>
        <p style='margin-bottom: 8px; color: #CCCCCC;'>
            ⚔️ <strong>Mejoras Completas • Validación Avanzada • Torneo VIP</strong>
        </p>
        <p style='margin-bottom: 8px; color: #AAAAAA;'>
            🎮 <strong>🏆 Scrim 5v5 • ⚔️ Duelo 1v1 • 🎯 Práctica • 📊 Análisis • 🏅 Torneo</strong>
        </p>
        <p style='margin: 0; color: #999999; font-size: 0.9em;'>
            📅 Proyecto de Programación - Primer Semestre | Diciembre 2025
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