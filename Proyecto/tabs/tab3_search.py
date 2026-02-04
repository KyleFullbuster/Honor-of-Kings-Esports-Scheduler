import streamlit as st
import time
from datetime import datetime
from utils.helpers import (
    get_event_type_requirements,
    extraer_posicion_jugador,
    extraer_posicion_heroe,
    validate_event_resources
)

def show_search_tab(scheduler):
    """Muestra la pestaña de búsqueda de huecos"""
    st.header("🔍 BUSCAR HUECO DISPONIBLE")

    st.markdown("""
    **Encuentra automáticamente el próximo horario libre** que cumpla con todas las restricciones  
    y **crea el evento directamente desde aquí** ⚡
    
    ⚠️ **NOTA:** Los huecos se buscan con al menos 15 minutos de anticipación para evitar errores de tiempo.
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
            
            with st.spinner("🔍 Buscando hueco disponible (comienza en 15+ minutos, horario 9:00-22:00)..."):
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
                        st.balloons()
                        
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

    st.caption("🔍 La búsqueda comienza 15 minutos en el futuro • Horario laboral: 9:00-22:00 • Máximo: 7 días adelante")