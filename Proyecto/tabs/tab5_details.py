import streamlit as st
from utils.helpers import get_event_type_badge

def show_details_tab(scheduler):
    """Muestra la pestaña de detalles y agenda"""
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
            key="detalles_select_fixed_tab5",
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

            badge_text = get_event_type_badge(event_type)

            st.markdown(f"{badge_text} **Tipo de evento:** {event_type.upper()}")
            st.text_area(
                "**📋 DETALLES COMPLETOS:**",
                detalles,
                height=300,
                key="detalles_area_fixed_tab5",
            )
    else:
        st.info("📭 **No hay eventos para mostrar**")