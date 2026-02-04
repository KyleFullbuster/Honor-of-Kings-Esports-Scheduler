import streamlit as st
import time
from datetime import datetime, timedelta
from utils.helpers import (
    get_event_type_requirements, 
    extraer_posicion_jugador, 
    extraer_posicion_heroe, 
    validate_event_resources
)

def show_add_tab(scheduler):
    """Muestra la pestaña para agregar eventos"""
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
        if st.button("🏆 Scrim 5v5", use_container_width=True, key="btn_scrim_tab2"):
            st.session_state.selected_event_type = "scrim"
            st.rerun()

    with col_type2:
        if st.button("⚔️ Duelo 1v1", use_container_width=True, key="btn_1v1_tab2"):
            st.session_state.selected_event_type = "1v1"
            st.rerun()

    with col_type3:
        if st.button("🎯 Práctica", use_container_width=True, key="btn_practica_tab2"):
            st.session_state.selected_event_type = "practica"
            st.rerun()

    with col_type4:
        if st.button("📊 Análisis", use_container_width=True, key="btn_analisis_tab2"):
            st.session_state.selected_event_type = "analisis"
            st.rerun()

    with col_type5:
        if st.button("🏅 Torneo", use_container_width=True, key="btn_torneo_tab2"):
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
            key="add_nombre_tab2",
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
            key="add_fecha_select_tab2",
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
                    f"{hora}", key=f"hora_btn_{idx}_tab2", use_container_width=True
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
            key="add_hora_manual_tab2",
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
            key="add_duracion_tab2",
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
                key="add_jugadores_tab2",
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
                key="filter_role_tab2",
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
                key="add_heroes_tab2",
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
                key="add_instalaciones_tab2",
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
        key="btn_agregar_fixed_tab2",
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