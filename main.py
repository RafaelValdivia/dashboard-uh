import os
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plots
from PIL import Image
from st_clickable_images import clickable_images as stci

import streamlit as st


def trigger_reset():
    st.session_state.trigger_reset = True


with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Dashboard Universitario",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.config.set_option("theme.base", "light")


# Sistema de autenticación básico
def authenticate_user(username, password, users_db):
    """Autentica al usuario verificando sus credenciales"""
    if username in users_db:
        stored_password = users_db[username]["password"]
        # En un sistema real, usaríamos hash más seguro
        if password == stored_password:
            return True, users_db[username]
    return False, None


def init_session_state():
    """Inicializa el estado de la sesión"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "ratings" not in st.session_state:
        st.session_state.rating = pd.read_csv("Semester_Rating.csv")
        st.session_state.rating.set_index("Facultad", inplace=True)
    if "classes" not in st.session_state:
        st.session_state.classes = pd.read_csv("MATCOM_Classes.csv")
    if "vd" not in st.session_state:
        st.session_state.vd = pd.read_csv("VD_Rating.csv")
    if "rating_MATCOM" not in st.session_state:
        st.session_state.rating_MATCOM = pd.read_csv("MATCOM_Rating.csv")
    if "comments" not in st.session_state:
        st.session_state.comments = load_sample_comments()
        placeholder = ("Comparte tu experiencia general del semestre...",)
    if "reset_trigger" not in st.session_state:
        st.session_state.reset_trigger = False


def load_sample_comments():
    """Carga comentarios de ejemplo"""
    comments = [
        {
            "estudiante": "María González",
            "facultad": "INSTEC",
            "clase": "Programación",
            "profesor": "Dr. Carlos Méndez",
            "comentario": "Excelente profesor, explica muy bien los conceptos complejos.",
            "calificacion": 8.2,
            "fecha": "2023-12-10",
        },
        {
            "estudiante": "Carlos Rodríguez",
            "facultad": "FBIO",
            "clase": "Biología Molecular",
            "profesor": "Dra. Ana García",
            "comentario": "La materia es interesante pero la carga de trabajo es excesiva.",
            "calificacion": 6,
            "fecha": "2023-12-05",
        },
        {
            "estudiante": "Anónimo",
            "facultad": "FHS",
            "clase": "Historia",
            "profesor": "Dra. Laura Rodríguez",
            "comentario": "Me gustó la forma en que relaciona los hechos históricos con la actualidad.",
            "calificacion": 8.1,
            "fecha": "2023-12-08",
        },
        {
            "estudiante": "Javier López",
            "facultad": "FF",
            "clase": "Cálculo I",
            "profesor": "Dr. Carlos Méndez",
            "comentario": "Muy difícil pero aprendí mucho. El profesor está dispuesto a ayudar.",
            "calificacion": 7,
            "fecha": "2023-12-12",
        },
        {
            "estudiante": "Laura Sánchez",
            "facultad": "FQ",
            "clase": "Química",
            "profesor": "Dr. Eugenia del Río",
            "comentario": "Los laboratorios son muy prácticos y ayudan a entender la teoría.",
            "calificacion": 8.8,
            "fecha": "2023-06-20",
        },
    ]
    return comments


def load_users_db():
    """Carga la base de datos de usuarios (en un sistema real esto vendría de una DB)"""
    users_db = {
        "estudiante1": {
            "password": "1234",
            "nombre": "Juan Pérez",
            "facultad": "MATCOM",
            "semestre_actual": "2023-2",
            "role": "estudiante",
        },
        "estudiante2": {
            "password": "1234",
            "nombre": "Ana Gómez",
            "facultad": "FF",
            "semestre_actual": "2023-2",
            "role": "estudiante",
        },
        "admin": {
            "password": "admin123",
            "nombre": "Administrador",
            "facultad": "Todas",
            "semestre_actual": "2023-2",
            "role": "administrador",
        },
    }
    return users_db


def login_section():
    """Muestra la sección de inicio de sesión"""
    st.markdown(
        "<h1 class='main-header'>🎓 Sistema de Evaluación Universitaria</h1>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Iniciar Sesión")

        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Iniciar Sesión"):
                users_db = load_users_db()
                auth_result, user_info = authenticate_user(username, password, users_db)

                if auth_result:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_info["nombre"]
                    st.session_state.user_role = user_info["role"]
                    st.session_state.user_faculty = user_info["facultad"]
                    st.session_state.semestre_actual = user_info["semestre_actual"]
                    st.success(f"¡Bienvenido(a), {user_info['nombre']}!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")

        with col_b:
            if st.button("Modo Invitado"):
                st.session_state.logged_in = True
                st.session_state.current_user = "Invitado"
                st.session_state.user_role = "invitado"
                st.session_state.user_faculty = "General"
                st.session_state.semestre_actual = "2023-2"
                st.success(
                    "Has ingresado como invitado. Puedes ver las evaluaciones pero no participar."
                )
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Credenciales de prueba")
        st.markdown("""
        - **Estudiante 1:** Usuario: `estudiante1` | Contraseña: `1234`
        - **Estudiante 2:** Usuario: `estudiante2` | Contraseña: `1234`
        - **Administrador:** Usuario: `admin` | Contraseña: `admin123`
        """)
        st.markdown("</div>", unsafe_allow_html=True)


def main_dashboard():
    """Muestra el dashboard principal después del login"""
    # Barra lateral
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.current_user}")
        st.markdown(f"**Rol:** {st.session_state.user_role}")
        st.markdown(f"**Facultad:** {st.session_state.user_faculty}")
        st.markdown(f"**Semestre actual:** {st.session_state.semestre_actual}")

        st.markdown("---")

        # Navegación
        st.markdown("### Navegación")
        page_options = [
            "📊 Dashboard Principal",
            "🎓 Dashboard Facultad",
            "⭐ Evaluar Semestre",
            "📚 Evaluar Clase",
            "💬 Comentarios",
            "📈 Estadísticas",
        ]

        if st.session_state.user_role == "administrador":
            page_options.append("👨‍💼 Panel de Administración")

        selected_page = st.radio("Ir a:", page_options)

        st.markdown("---")

        if st.button("🚪 Cerrar Sesión"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.user_role = None
            st.rerun()

    # Páginas principales
    if selected_page == "📊 Dashboard Principal":
        show_main_dashboard()
    elif selected_page == "⭐ Evaluar Semestre":
        evaluate_semester()
    elif selected_page == "📚 Evaluar Clase":
        evaluate_class()
    elif selected_page == "💬 Comentarios":
        show_comments()
    elif selected_page == "📈 Estadísticas":
        show_statistics()
    elif selected_page == "🎓 Dashboard Facultad":
        show_faculty_dashboard()
    elif (
        selected_page == "👨‍💼 Panel de Administración"
        and st.session_state.user_role == "administrador"
    ):
        show_admin_panel()


def show_main_dashboard():
    """Muestra el dashboard principal con métricas y gráficos"""
    st.markdown(
        "<h1 class='main-header'>Dashboard Universitario</h1>",
        unsafe_allow_html=True,
    )

    # Métricas principales
    st.markdown(
        "<div class='sub-header'>📈 Métricas Generales del Semestre</div>",
        unsafe_allow_html=True,
    )

    df = st.session_state.rating
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(plots.color_legend()[0])
    col1, col2 = st.columns(2)
    with col1:
        avg_semester = df.loc["GENERAL"].mean()
        st.pyplot(plots.rating_pie(avg_semester)[0])

    with col2:
        rating_semester = df.loc["GENERAL"]
        st.pyplot(plots.rating_hist(rating_semester)[0])

    with st.expander("Datos de facultades"):
        st.pyplot(plots.fac_avrg(df)[0])

    st.markdown("<div class='sub-header'>📊 Facultades</div>", unsafe_allow_html=True)

    img_names = [i for i in os.listdir("logos/") if "png" in i]
    images = [Image.open(f"logos/{i}") for i in img_names]
    cols = st.columns(3)

    for index, image in enumerate(images):
        with cols[index % 3]:
            with st.container(height=300):
                st.image(image, width=250)
            st.button(
                f"Ir a la pagina de {img_names[index].capitalize().replace('.png', '')}"
            )


def show_faculty_dashboard():
    """Muestra el dashboard principal con métricas y gráficos"""
    st.markdown(
        "<h1 class='main-header'>Dashboard MATCOM</h1>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image("logos/matcom.png", width=300)
    # Métricas principales
    st.markdown(
        "<div class='sub-header'>📈 Métricas Generales de MATCOM</div>",
        unsafe_allow_html=True,
    )

    df = st.session_state.rating_MATCOM
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(plots.color_legend()[0])
    col1, col2 = st.columns(2)
    with col1:
        avg_semester = df.loc["GENERAL"].mean()
        st.pyplot(plots.rating_pie(avg_semester)[0])

    with col2:
        rating_semester = df.loc["GENERAL"]
        st.pyplot(plots.rating_hist(rating_semester)[0])

    with st.expander("Datos de facultades"):
        st.pyplot(plots.fac_avrg(df)[0])

    st.markdown("<div class='sub-header'>📊 Facultades</div>", unsafe_allow_html=True)

    img_names = [i for i in os.listdir("logos/") if "png" in i]
    images = [Image.open(f"logos/{i}") for i in img_names]
    cols = st.columns(3)

    for index, image in enumerate(images):
        with cols[index % 3]:
            with st.container(height=300):
                st.image(image, width=250)
            st.button(
                f"Ir a la pagina de {img_names[index].capitalize().replace('.png', '')}"
            )


def evaluate_semester():
    """Permite a los estudiantes evaluar el semestre"""
    st.markdown(
        "<div class='sub-header'>⭐ Evaluar Semestre Actual</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.user_role == "invitado":
        st.warning(
            "⚠️ Los invitados no pueden realizar evaluaciones. Inicia sesión como estudiante para participar."
        )
        return

    with st.form("evaluar_semestre"):
        st.markdown("### Califica el semestre actual")
        columns = st.columns(2)
        for index, category in enumerate(st.session_state.rating.columns):
            with columns[index % 2]:
                st.slider(category, min_value=0, max_value=10, value=6)

        submitted = st.form_submit_button("Enviar Evaluación del Semestre")
        if submitted:
            # Aquí normalmente guardaríamos en una base de datos
            nueva_evaluacion = {
                "estudiante_id": st.session_state.current_user,
                "facultad": st.session_state.user_faculty,
                "fecha": datetime.now().strftime("%Y-%m-%d"),
            }

            st.success(
                "✅ ¡Gracias por evaluar tu semestre! Tu feedback es valioso para mejorar la experiencia universitaria."
            )
            st.balloons()

    with st.form("comentar semestre"):
        comentario = st.text_area(
            "Comentarios adicionales sobre el semestre",
            placeholder="Comparte tu experiencia general del semestre...",
        )
        send_comment = st.form_submit_button("Enviar comentario")


def evaluate_class():
    """Permite a los estudiantes evaluar una clase específica"""
    st.markdown(
        "<div class='sub-header'>📚 Evaluar una Clase</div>", unsafe_allow_html=True
    )

    if st.session_state.user_role == "invitado":
        st.warning(
            "⚠️ Los invitados no pueden realizar evaluaciones. Inicia sesión como estudiante para participar."
        )
        return

    with st.form("evaluar_clase"):
        st.markdown("### Califica una clase específica")

        # col1, col2 = st.columns(2)
        # with col1:
        asignaturas = [
            "Visualizacion de Datos",
            "Matematica Aplicada",
            "Bases de Datos",
            "Estructura de Datos y Algoritmos",
            "Probabilidades",
            "Economia Politica",
        ]

        clase = st.selectbox("Clase:", asignaturas)
        # with col2:
        #     profesores = [
        #         "Claudia A. Damiani",
        #         "Ania",
        #         "Carlos",
        #         "Raudel",
        #         "Yanetxi",
        #         "Irana",
        #     ]
        #     profesor = profesores[asignaturas.index(clase)]
        #     st.text("Profesor:")
        #     st.text(f"{profesor}")

        columns = st.columns(2)

        for index in range(len(st.session_state.vd["Categoria"])):
            with columns[index % 2]:
                vd = st.session_state.vd
                st.slider(vd["Categoria"][index], min_value=0, max_value=10, value=6)

        sugerencias = st.text_area(
            "Sugerencias de mejora",
            placeholder="¿Qué cambiarías o mejorarías de esta clase?",
        )

        submitted = st.form_submit_button("Enviar Evaluación de Clase")

        if submitted:
            # Aquí normalmente guardaríamos en una base de datos
            nueva_evaluacion = {
                "estudiante_id": st.session_state.current_user,
                "facultad": st.session_state.user_faculty,
                "clase": clase,
                "profesor": profesor,
                "sugerencias": sugerencias,
                "fecha": datetime.now().strftime("%Y-%m-%d"),
            }

            # Agregar a las evaluaciones (en memoria)
            nueva_fila = pd.DataFrame([nueva_evaluacion])
            st.success(
                "✅ ¡Gracias por evaluar esta clase! Tu feedback ayudará a mejorar la calidad de la enseñanza."
            )
            st.balloons()


def show_comments():
    """Muestra y permite agregar comentarios"""
    st.markdown(
        "<div class='sub-header'>💬 Comentarios y Experiencias</div>",
        unsafe_allow_html=True,
    )

    facultades = list(st.session_state.rating.index)
    facultades[facultades.index("GENERAL")] = "Todas"
    clases = list(set(st.session_state.classes["Asignatura"]))
    clases = [clase + " (Ciencia de Datos)" for clase in clases] + ["Todas"]
    profesores = [
        "Todos",
        "Dr. Carlos Méndez",
        "Dra. Ana García",
        "Prof. Miguel Torres",
        "Dra. Laura Rodríguez",
        "Dr. Javier López",
        "Prof. Elena Sánchez",
        "Dr. Fernando Martínez",
        "Dr. Eugenia del Río",
    ]

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_faculty = st.selectbox("Filtrar por facultad", facultades[::-1])
    with col2:
        filter_class = st.selectbox(
            "Filtrar por clase",
            clases[::-1],
        )
    with col3:
        filter_professor = st.selectbox("Filtrar por profesor", profesores)

    # Mostrar comentarios existentes
    st.markdown("### Comentarios de estudiantes")

    comments_to_show = st.session_state.comments

    if filter_faculty != "Todas":
        comments_to_show = [
            c for c in comments_to_show if c["facultad"] == filter_faculty
        ]

    if filter_class != "Todas":
        comments_to_show = [c for c in comments_to_show if c["clase"] == filter_class]

    if filter_professor != "Todos":
        comments_to_show = [
            c for c in comments_to_show if c["profesor"] == filter_professor
        ]

    if not comments_to_show:
        st.info("No hay comentarios que coincidan con los filtros seleccionados.")
    else:
        for comment in comments_to_show:
            stars = (
                "⭐" * round(comment["calificacion"] / 2)
                if comment["calificacion"] is not None
                else ""
            )
            empty_stars = (
                "☆" * (5 - round(comment["calificacion"] / 2))
                if comment["calificacion"] is not None
                else ""
            )
            stars_to_show = (
                f"{stars}{empty_stars} ({comment['calificacion']}/10)"
                if comment["calificacion"] is not None
                else "Sin calificacion"
            )

            st.markdown(
                f"""
            <div class="comment-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{comment["estudiante"]}</strong> - {comment["facultad"]}
                    </div>
                    <div>
                        <strong>{comment["clase"]}</strong> )
                    </div>
                </div>
                <div style="margin: 0.5rem 0;">
                    {stars_to_show}
                    </div>
                <div style="font-style: italic;">
                    "{comment["comentario"]}"
                </div>
                <div styile="text-align: right; font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
                    {comment["fecha"]}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Formulario para agregar nuevo comentario (solo para estudiantes)
    if (
        st.session_state.user_role != "invitado"
        and st.session_state.user_role != "administrador"
    ):
        st.markdown("### Agregar un comentario")

        with st.form("nuevo_comentario"):
            clase = st.selectbox("Clase a comentar", clases[::-1])

            comentario = st.text_area(
                "Tu comentario",
                placeholder="Comparte tu experiencia con esta clase...",
                height=100,
            )

            submitted = st.form_submit_button("Publicar Comentario")

            if submitted and comentario:
                nuevo_comentario = {
                    "estudiante": st.session_state.current_user,
                    "facultad": st.session_state.user_faculty,
                    "clase": clase,
                    "profesor": f"Profesor de la clase {clase}",
                    "calificacion": None,
                    "comentario": comentario,
                    "fecha": datetime.now().strftime("%Y-%m-%d"),
                    "semestre": st.session_state.semestre_actual,
                }

                st.session_state.comments.append(nuevo_comentario)
                st.success("✅ ¡Gracias por tu comentario! Ha sido publicado.")
                st.rerun()
    elif st.session_state.user_role == "invitado":
        st.info(
            "💡 Inicia sesión como estudiante para agregar tus propios comentarios."
        )


def show_statistics():
    """Muestra estadísticas detalladas"""
    st.markdown(
        "<div class='sub-header'>📈 Estadísticas Detalladas</div>",
        unsafe_allow_html=True,
    )

    df = st.session_state.rating

    # Filtros para estadísticas
    st.markdown("<div class='faculty-selector'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        stat_faculty = st.selectbox(
            "Seleccionar facultad para estadísticas",
            ["Todas", "Ingeniería", "Ciencias", "Humanidades"],
        )
    with col2:
        stat_semester = st.selectbox(
            "Seleccionar semestre", ["Todos", "2023-2", "2023-1", "2022-2", "2022-1"]
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Aplicar filtros
    filtered_df = df.copy()
    if stat_faculty != "Todas":
        filtered_df = filtered_df[filtered_df["facultad"] == stat_faculty]

    if stat_semester != "Todos":
        filtered_df = filtered_df[filtered_df["semestre"] == stat_semester]

    if filtered_df.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        return

    # Gráficos de estadísticas
    col1, col2 = st.columns(2)

    with col1:
        # Distribución de calificaciones
        fig1 = px.histogram(
            filtered_df,
            x="calificacion_clase",
            nbins=5,
            title="Distribución de Calificaciones de Clases",
            labels={
                "calificacion_clase": "Calificación",
                "count": "Número de Evaluaciones",
            },
            color_discrete_sequence=["#3B82F6"],
        )
        fig1.update_layout(bargap=0.1)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Calificaciones por profesor
        if not filtered_df.empty and "profesor" in filtered_df.columns:
            professor_ratings = (
                filtered_df.groupby("profesor")["calificacion_clase"]
                .mean()
                .sort_values(ascending=False)
            )
            fig2 = px.bar(
                professor_ratings,
                x=professor_ratings.values,
                y=professor_ratings.index,
                orientation="h",
                title="Calificación Promedio por Profesor",
                labels={"x": "Calificación Promedio", "y": "Profesor"},
                color=professor_ratings.values,
                color_continuous_scale="Viridis",
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

    # Comparación entre facultades
    st.markdown("### Comparación entre Facultades")

    faculty_comparison = (
        df.groupby("facultad")
        .agg(
            {
                "calificacion_clase": "mean",
                "calificacion_semestre": "mean",
                "dificultad": "mean",
                "carga_trabajo": "mean",
            }
        )
        .round(2)
    )

    st.dataframe(faculty_comparison.style.background_gradient(cmap="Blues"))

    # Evolución temporal
    st.markdown("### Evolución Temporal de Calificaciones")

    if not filtered_df.empty:
        time_series = (
            filtered_df.groupby("semestre")["calificacion_clase"].mean().reset_index()
        )
        fig3 = px.line(
            time_series,
            x="semestre",
            y="calificacion_clase",
            markers=True,
            title="Evolución de Calificaciones por Semestre",
            labels={
                "semestre": "Semestre",
                "calificacion_clase": "Calificación Promedio",
            },
        )
        fig3.update_traces(line=dict(width=3))
        st.plotly_chart(fig3, use_container_width=True)


def show_admin_panel():
    """Panel de administración (solo para administradores)"""
    st.markdown(
        "<div class='sub-header'>👨‍💼 Panel de Administración</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.user_role != "administrador":
        st.warning(
            "Acceso restringido. Solo los administradores pueden acceder a esta sección."
        )
        return

    tab1, tab2, tab3 = st.tabs(
        ["📊 Datos Completos", "📥 Exportar Datos", "⚙️ Configuración"]
    )

    with tab1:
        st.markdown("### Base de Datos de Evaluaciones")
        st.dataframe(st.session_state.rating)

        st.markdown("### Comentarios de Estudiantes")
        comments_df = pd.DataFrame(st.session_state.comments)
        st.dataframe(comments_df)

    with tab2:
        st.markdown("### Exportar Datos")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Exportar Evaluaciones a CSV"):
                csv = st.session_state.rating.to_csv(index=False)
                st.download_button(
                    label="Descargar CSV",
                    data=csv,
                    file_name="evaluaciones_universitarias.csv",
                    mime="text/csv",
                )

        with col2:
            if st.button("Exportar Comentarios a CSV"):
                comments_csv = pd.DataFrame(st.session_state.comments).to_csv(
                    index=False
                )
                st.download_button(
                    label="Descargar CSV",
                    data=comments_csv,
                    file_name="comentarios_estudiantes.csv",
                    mime="text/csv",
                )

        st.markdown("### Resumen Estadístico")
        st.write(st.session_state.rating.describe())

    with tab3:
        st.markdown("### Configuración del Sistema")

        st.info(
            "Esta sección permitiría configurar parámetros del sistema en una implementación real."
        )

        semester_name = st.text_input("Nombre del semestre actual", value="2023-2")
        evaluation_active = st.checkbox("Evaluaciones activas", value=True)

        if st.button("Guardar Configuración"):
            st.success("Configuración guardada (simulación)")


def main():
    """Función principal de la aplicación"""
    # Inicializar estado de sesión
    init_session_state()

    # Mostrar login o dashboard principal
    if not st.session_state.logged_in:
        login_section()
    else:
        main_dashboard()


if __name__ == "__main__":
    main()
