import streamlit as st
import time
from utils.helpers import get_event_type_requirements

def show_system_tab(scheduler, init_scheduler):
    """Muestra la pestaña de sistema y configuración"""
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
        st.metric("Versión", "7.2 Mejoras Completas")

        if st.button(
            "🔄 Recargar datos", use_container_width=True, key="reload_data_fixed_tab6"
        ):
            scheduler.load_data()
            st.session_state.scheduler = scheduler  # Actualizar estado
            st.success("✅ Datos recargados y estado actualizado")
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