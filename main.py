import os
from datetime import datetime
from itertools import dropwhile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plots
from PIL import Image

import streamlit as st


def trigger_reset():
    st.session_state.trigger_reset = True


with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Dashboard Universitario",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.config.set_option("theme.base", "light")


def dd(dic, keys, values):
    return pd.DataFrame({keys: list(dic.keys()), values: list(dic.values())})


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

    # Initialize new data structures from original dashboard
    if "sem_data" not in st.session_state:
        # Create sample semester data for visualizations
        st.session_state.sem_data = {
            "Rating 1": 4.2,
            "Rating 2": 3.8,
            "Rating 3": 4.5,
            "Rating 4": 3.9,
            "Rating 5": 4.1,
        }

    if "fac_avrg" not in st.session_state:
        # Create faculty averages
        st.session_state.fac_avrg = {
            "MATCOM": 4.0,
            "FF": 3.8,
            "FQ": 4.1,
            "FBIO": 3.9,
            "FHS": 4.2,
            "INSTEC": 4.0,
        }

    # if "fac_data" not in st.session_state:
    #     # Create faculty data for histograms
    #     st.session_state.fac_data = {
    #         "MATCOM": {"Excelente": 45, "Bueno": 120, "Regular": 35, "Malo": 15},
    #         "FF": {"Excelente": 60, "Bueno": 140, "Regular": 40, "Malo": 10},
    #     }

    if "sem_rtng" not in st.session_state:
        # Semester rating for pie chart
        st.session_state.sem_rtng = 4.1

    if "mark_colors" not in st.session_state:
        # Color scheme for grade histograms
        st.session_state.mark_colors = ["#b00", "#bb0", "#0b0", "#0fb"]

    if "matr_MATCOM" not in st.session_state:
        # MATCOM enrollment data
        st.session_state.matr_MATCOM = pd.DataFrame(
            {
                "Brigada": [
                    "Matemática",
                    "Ciencias de\n la Computación",
                    "Ciencias de\n Datos",
                ],
                "Count": [100, 220, 150],
            },
        ).reset_index(drop=True)

    if "notas_MATCOM" not in st.session_state:
        # MATCOM grade distribution
        st.session_state.notas_MATCOM = {"2": 67, "3": 105, "4": 32, "5": 6}
        st.session_state.notas_MATCOM = dd(
            st.session_state.notas_MATCOM, "Nota", "Count"
        )

    if "matr_CD" not in st.session_state:
        # Ciencias de Datos enrollment data
        st.session_state.matr_CD = pd.DataFrame(
            {
                "Brigada": ["Primer Año", "Segundo Año", "Tercer Año", "Cuarto Año"],
                "Count": [120, 85, 60, 40],
            }
        ).reset_index(drop=True)

    if "asig_VD" not in st.session_state:
        # Visualización de Datos course ratings
        st.session_state.asig_VD = {
            "Claridad": 4.2,
            "Dificultad": 3.8,
            "Utilidad": 4.5,
            "Organización": 4.0,
            "Evaluación": 4.1,
        }

    if "vd_notas" not in st.session_state:
        # Visualización de Datos grade distribution
        st.session_state.vd_notas = {"2": 8, "3": 25, "4": 15, "5": 12}

    if "colors" not in st.session_state:
        # Color scheme for various charts
        st.session_state.colors = ["#0a0", "#a0a", "#09b", "#f92"]


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
            "🎓 Dashboard Carrera",
            "🎓 Dashboard Asignatura",
            "⭐ Evaluar Semestre",
            "📚 Evaluar Clase",
            "💬 Comentarios",
            "Guion del video",
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
    elif selected_page == "Guion del video":
        with open("guion.md", "r") as guion:
            st.markdown(guion.read())
    elif selected_page == "🎓 Dashboard Facultad":
        show_faculty_dashboard()
    elif selected_page == "🎓 Dashboard Carrera":
        show_degree_dashboard()
    elif selected_page == "🎓 Dashboard Asignatura":
        show_course_dashboard()
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

    # Métricas principales - Added from original dashboard
    st.markdown(
        "<div class='sub-header'>📈 Calificación del Semestre 25</div>",
        unsafe_allow_html=True,
    )

    df = st.session_state.rating
    col1, col2 = st.columns([1, 1])

    with col1:
        st.pyplot(plots.rating_pie(st.session_state.rating.mean().mean())[0])

    with col2:
        st.pyplot(plots.rating_hist(st.session_state.rating.mean())[0])

    # Faculty averages expander - Added from original dashboard
    with st.expander("Calificación por facultad"):
        st.pyplot(plots.fac_avrg(st.session_state.rating)[0])

    st.divider()

    # Image gallery - Added from original dashboard
    st.markdown(
        "<div class='sub-header'>📸 Galería de Facultades</div>", unsafe_allow_html=True
    )
    img_names = [i for i in os.listdir("logos/") if "png" in i]
    cols = st.columns(3)

    for index, img_name in enumerate(img_names):
        with cols[index % 3]:
            with st.container(height=300):
                st.image(f"logos/{img_name}", width=250)
            st.button(
                f"Ir a la página de {img_name.upper().replace('.PNG', '')}",
                key=f"faculty_btn_{index}",
            )

    st.divider()

    # Semester grade histogram - Added from original dashboard
    st.subheader("Histograma de notas del semestre")
    st.pyplot(
        plots.mark_hist(dd({"2": 64, "3": 203, "4": 34, "5": 18}, "Nota", "Count"))[0]
    )

    # st.divider()

    # Student comments section - Added from original dashboard
    # st.subheader("Comentarios de los estudiantes")
    # st.image("comments.jpg", width=900, caption="Resumen de comentarios del semestre")
    # st.divider()


def show_faculty_dashboard():
    """Muestra el dashboard de facultad con métricas detalladas"""
    faculty = "MATCOM"

    st.markdown(
        f"<h1 class='main-header'>Dashboard de {faculty}</h1>",
        unsafe_allow_html=True,
    )

    # Header with image and description
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("logos/matcom.png", width=300)

    with col2:
        st.markdown("""
        ### Facultad de Matemática y Computación
        Fundada en el año 1976 por el Dr. Carlos Martínez. Al principio tenía una sola carrera (Matemática)
        pero con el avance de la tecnología y la computación en el siglo XX se añadió la carrera de Ciencias
        de la Computación. Más recientemente se fundó la carrera de Ciencias de Datos.

        **Directora:** Dra. Ana María González
        **Estudiantes activos:** 550
        **Profesores:** 45
        """)

    st.divider()

    # Faculty ratings section
    st.header(f"Calificación del semestre de {faculty}")
    col3, col4 = st.columns([1, 1])

    with col3:
        st.pyplot(plots.rating_pie(st.session_state.sem_rtng)[0])

    with col4:
        st.pyplot(plots.rating_hist(st.session_state.rating.mean())[0])

    st.divider()

    # Degree programs list - Added from original dashboard
    st.header("Carreras:")
    col5, col6, col7 = st.columns(3)

    with col5:
        st.markdown("### [Matemática](/#)")
        st.markdown("**Estudiantes:** 180")
        st.markdown("**Promedio:** 3.8")

    with col6:
        st.markdown("### [Ciencias de la Computación](/#)")
        st.markdown("**Estudiantes:** 220")
        st.markdown("**Promedio:** 4.0")

    with col7:
        st.markdown("### [Ciencias de Datos](/#)")
        st.markdown("**Estudiantes:** 150")
        st.markdown("**Promedio:** 4.2")

    st.divider()

    # Enrollment and academic performance - Added from original dashboard
    colors = ["#ab9", "#a0a", "#09b"]

    st.header("Matrícula por Carrera")
    st.markdown("### Matrícula por Carrera: ")
    st.pyplot(plots.matr_pie(st.session_state.matr_MATCOM, colors)[0])

    st.header("Rendimiento Académico")
    st.markdown("### Promedio General: 3.9")
    careers
    st.pyplot()[0])

    st.header("Frecuencia absoluta de las notas")
    st.pyplot(
        plots.mark_hist(dd({"2": 47, "3": 85, "4": 22, "5": 6}, "Nota", "Count"))[0]
    )


def show_degree_dashboard():
    """Muestra el dashboard de carrera específica"""
    st.markdown(
        "<h1 class='main-header'>🎓 Ciencias de Datos</h1>",
        unsafe_allow_html=True,
    )

    st.markdown("""
    ### Descripción de la Carrera
    La carrera de Ciencias de Datos forma profesionales capaces de extraer conocimiento y insights valiosos
    a partir de grandes volúmenes de datos. Combina fundamentos matemáticos, estadísticos y computacionales
    para resolver problemas complejos en diversos campos.
    """)

    # Enrollment chart - Added from original dashboard
    st.subheader("Matrícula por Año Académico:")
    st.pyplot(plots.matr_pie(st.session_state.matr_CD, st.session_state.colors)[0])

    st.divider()

    # Dynamic subject listing by year - Added from original dashboard
    def gen_class(n: int, col1, col2) -> None:
        with col1:
            for i in range(n, 8 + n, 2):
                st.markdown(f"### [Asignatura {i}](/#)")
                st.markdown(f"**Créditos:** {4 if i % 2 == 0 else 3}")
                st.markdown(f"**Profesor:** Dr. {'A' if i % 2 == 0 else 'B'}")

        with col2:
            for i in range(1 + n, 9 + n, 2):
                st.markdown(f"### [Asignatura {i}](/#)")
                st.markdown(f"**Créditos:** {4 if i % 2 == 1 else 3}")
                st.markdown(f"**Profesor:** Dr. {'C' if i % 2 == 1 else 'D'}")

    # Academic performance by year - Added from original dashboard
    st.header("Rendimiento Académico por Año")
    st.markdown("### Promedio General: 3.9")
    st.pyplot(
        plots.mark_hist(
            {
                "Primer Año": 2.8,
                "Segundo Año": 3.4,
                "Tercer Año": 3.8,
                "Cuarto Año": 3.9,
            }
        )[0]
    )

    st.header("Frecuencia absoluta de las notas")
    st.pyplot(
        plots.mark_hist(
            dd({"2": 18, "3": 42, "4": 12, "5": 3}, "Nota", "Count2"),
            st.session_state.mark_colors,
        )[0]
    )

    st.divider()

    # Subjects by year - Added from original dashboard
    for year in range(1, 5):
        st.header(f"Año {year}")
        col1, col2 = st.columns([1, 1])
        gen_class((year - 1) * 8, col1, col2)
        st.divider()


def show_course_dashboard():
    """Muestra el dashboard de asignatura específica"""
    st.markdown(
        "<h1 class='main-header'>📊 Visualización de Datos</h1>",
        unsafe_allow_html=True,
    )

    # Course ratings - Added from original dashboard
    col1, col2 = st.columns([0.75, 1])
    vd_rtng = sum(st.session_state.asig_VD.values()) / len(st.session_state.asig_VD)
    st.markdown("### Descripción de la Asignatura")
    with col1:
        with st.container(height=200):
            st.markdown("""
            Esta asignatura introduce los principios fundamentales de la visualización de datos,
            técnicas para comunicar información de manera efectiva mediante representaciones gráficas,
            y el uso de herramientas modernas para crear visualizaciones interactivas y estáticas.
            """)
        with st.container(height=600):
            st.pyplot(plots.rating_pie(vd_rtng)[0])

    with col2:
        with st.container(height=200):
            st.markdown("""
            **Créditos:** 4\n
            **Semestre:** 4to\n
            **Prerrequisitos:** Programación I, Estadística\n
            **Profesor:** Dr. Carlos Méndez
            """)
        with st.container(height=600):
            st.pyplot(plots.rating_hist(st.session_state.asig_VD)[0])

    st.divider()

    # Academic performance for the course - Added from original dashboard
    st.subheader("Rendimiento Académico en la Asignatura")
    st.markdown("### Promedio: 3.9")
    st.pyplot(
        plots.mark_hist(st.session_state.vd_notas, st.session_state.mark_colors)[0]
    )

    st.divider()

    # Course breakdown
    st.header("Detalles de Evaluación")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Distribución de Notas")
        grades_df = pd.DataFrame(
            {
                "Rango": ["2-2.4", "2.5-2.9", "3-3.4", "3.5-3.9", "4-4.4", "4.5-5"],
                "Estudiantes": [8, 15, 22, 18, 12, 5],
            }
        )
        st.bar_chart(grades_df.set_index("Rango"))

    with col4:
        st.markdown("### Componentes de Evaluación")
        eval_data = pd.DataFrame(
            {
                "Componente": ["Proyecto Final", "Exámenes", "Tareas", "Participación"],
                "Porcentaje": [40, 30, 20, 10],
            }
        )
        fig = px.pie(eval_data, values="Porcentaje", names="Componente")
        st.plotly_chart(fig, use_container_width=True)


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
        if send_comment:
            # Aquí normalmente guardaríamos en una base de datos
            nueva_evaluacion = {
                "estudiante_id": st.session_state.current_user,
                "facultad": st.session_state.user_faculty,
                "fecha": datetime.now().strftime("%Y-%m-%d"),
            }

            st.success("Gracias por enviar su comentario.")
            st.balloons()


def evaluate_class():
    """Permite a los estudiantes evaluar una clase específica"""
    st.markdown(
        "<div class='sub-header'>📚 Evaluar una Clase</div>", unsafe_allow_html=True
    )

    if st.session_state.user_role == "invitado":
        st.warning("⚠️ Los invitados no pueden realizar evaluaciones")
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
