"""
🏆 CSS completo para Honor of Kings Esports Scheduler
Versión: 7.2 - Estilos profesionales con fondo local
"""

CSS_COMPLETO = """
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