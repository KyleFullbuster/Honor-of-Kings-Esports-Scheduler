import streamlit as st
from datetime import datetime
from utils.helpers import get_event_type_badge

def show_events_tab(scheduler):
    """Muestra la pestaña de eventos"""
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

                badge_text = get_event_type_badge(event_type)

                with st.expander(
                    f"{badge_text} **{i+1}. {evento['name']}** | {evento['start'].strftime('%d/%m %H:%M')} - {evento['end'].strftime('%H:%M')}",
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

                badge_text = get_event_type_badge(event_type)

                with st.expander(
                    f"{badge_text} {evento['name']} - {evento['start'].strftime('%d/%m %H:%M')}",
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