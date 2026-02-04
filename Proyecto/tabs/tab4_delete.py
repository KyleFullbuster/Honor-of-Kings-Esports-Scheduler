import streamlit as st
import time
from datetime import datetime
from utils.helpers import get_event_type_badge

def show_delete_tab(scheduler):
    """Muestra la pestaña para eliminar eventos"""
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
                    key="eliminar_select_fixed_tab4",
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

                badge_text = get_event_type_badge(event_type)

                # Mostrar detalles del evento
                with st.expander(
                    f"📋 Ver detalles del evento: {evento['name']}", 
                    expanded=False
                ):
                    st.markdown(f"**Tipo:** {badge_text}")
                    
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
                    key="eliminar_confirm_fixed_tab4",
                )

                if st.button(
                    "🗑️ **ELIMINAR EVENTO**",
                    type="secondary",
                    disabled=not confirmar,
                    use_container_width=True,
                    key="btn_eliminar_fixed_tab4",
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