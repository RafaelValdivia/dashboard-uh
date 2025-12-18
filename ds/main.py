import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# Import plot utilities
import plots

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Dashboard Universitario - UH",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load CSS if exists
css_path = Path("style.css")
if css_path.exists():
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================================================================
# DATA MANAGEMENT
# ============================================================================


class DataManager:
    """Manages loading and accessing data for the dashboard"""

    @staticmethod
    def load_data():
        """Load all data files"""
        data_files = {
            "semester_ratings": "Semester_Rating.csv",
            "matcom_ratings": "MATCOM_Rating.csv",
            "matcom_classes": "MATCOM_Classes.csv",
            "subject_ratings": "VD_Rating.csv",
        }

        data = {}
        for key, filename in data_files.items():
            try:
                data[key] = pd.read_csv(filename)
            except FileNotFoundError:
                st.error(f"⚠️ Archivo no encontrado: {filename}")
                # Create empty DataFrame
                data[key] = pd.DataFrame()

        return data

    @staticmethod
    def get_faculties():
        """Get list of all faculties"""
        try:
            df = pd.read_csv("Semester_Rating.csv")
            faculties = df["Facultad"].tolist()
            # Remove "GENERAL" from the list for selection purposes
            return [f for f in faculties if f != "GENERAL"]
        except:
            # Return default list if file not found
            return [
                "MATCOM",
                "FF",
                "FQ",
                "FBIOM",
                "FHS",
                "INSTEC",
                "FTUR",
                "FCOM",
                "LEX",
                "PSICO",
                "CSGH",
            ]

    @staticmethod
    def get_careers(faculty="MATCOM"):
        """Get careers for a specific faculty"""
        careers_by_faculty = {
            "MATCOM": ["Matemática", "Ciencias de la Computación", "Ciencia de Datos"],
            "FF": ["Física", "Física Médica", "Geofísica"],
            "FQ": ["Química", "Bioquímica", "Química Farmacéutica"],
            "FBIOM": ["Biología", "Microbiología", "Biotecnología"],
            "FHS": ["Historia", "Sociología", "Filosofía"],
            "INSTEC": ["Ingeniería en Telecomunicaciones", "Ingeniería Eléctrica"],
        }
        return careers_by_faculty.get(faculty, ["Carrera Principal"])


# ============================================================================
# AUTHENTICATION
# ============================================================================


class AuthenticationManager:
    """Handles user authentication"""

    USER_DATABASE = {
        "estudiante1": {
            "password": "1234",
            "nombre": "Juan Pérez",
            "facultad": "MATCOM",
            "carrera": "Ciencia de Datos",
            "role": "estudiante",
        },
        "estudiante2": {
            "password": "1234",
            "nombre": "Ana Gómez",
            "facultad": "FF",
            "carrera": "Física",
            "role": "estudiante",
        },
        "admin": {
            "password": "admin123",
            "nombre": "Administrador",
            "facultad": "Todas",
            "carrera": "Todas",
            "role": "administrador",
        },
    }

    @staticmethod
    def authenticate(username, password):
        """Authenticate a user"""
        if username in AuthenticationManager.USER_DATABASE:
            user_data = AuthenticationManager.USER_DATABASE[username]
            if password == user_data["password"]:
                return True, user_data
        return False, None

    @staticmethod
    def init_session_state():
        """Initialize session state variables"""
        default_state = {
            "logged_in": False,
            "current_user": None,
            "user_role": None,
            "user_faculty": None,
            "user_career": None,
            "current_page": "📊 Dashboard Principal",
            "data": {},
            "comments": AuthenticationManager.load_sample_comments(),
        }

        for key, value in default_state.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def load_sample_comments():
        """Load sample comments"""
        return [
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
                "facultad": "FBIOM",
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
        ]


# ============================================================================
# PAGE COMPONENTS
# ============================================================================


class DashboardComponents:
    """Reusable components for the dashboard"""

    @staticmethod
    def create_header(title, icon="🎓"):
        """Create a styled header"""
        st.markdown(
            f"""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                     border-radius: 10px; margin-bottom: 2rem;'>
                <h1 style='color: white; margin: 0;'>{icon} {title}</h1>
                <p style='color: rgba(255,255,255,0.8); margin: 0;'>Universidad de La Habana</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def create_metric_card(title, value, change=None, icon="📊"):
        """Create a metric card"""
        change_html = ""
        if change:
            change_color = "green" if change > 0 else "red"
            change_html = f"<div style='color: {change_color}; font-size: 0.9rem;'>▲ {change}%</div>"

        return f"""
            <div style='background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.5rem;'>{icon}</span>
                    <span style='font-weight: bold; color: #666;'>{title}</span>
                </div>
                <div style='font-size: 2rem; font-weight: bold;'>{value}</div>
                {change_html}
            </div>
        """

    @staticmethod
    def create_filter_bar():
        """Create a filter bar for dashboards"""
        col1, col2, col3 = st.columns(3)
        with col1:
            faculty = st.selectbox("Facultad", DataManager.get_faculties())
        with col2:
            career = st.selectbox("Carrera", DataManager.get_careers(faculty))
        with col3:
            semester = st.selectbox(
                "Semestre", ["2023-2", "2023-1", "2022-2", "2022-1"]
            )
        return faculty, career, semester


# ============================================================================
# PAGE VIEWS
# ============================================================================


class LoginView:
    """Login page view"""

    @staticmethod
    def render():
        st.markdown(
            """
            <style>
            .login-container {
                max-width: 500px;
                margin: 0 auto;
                padding: 2rem;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='login-container'>", unsafe_allow_html=True)

        DashboardComponents.create_header("Sistema de Evaluación", "🔐")

        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")

            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button(
                    "Iniciar Sesión", use_container_width=True
                )
            with col2:
                guest_btn = st.form_submit_button(
                    "Modo Invitado", use_container_width=True
                )

            if login_btn:
                authenticated, user_data = AuthenticationManager.authenticate(
                    username, password
                )
                if authenticated:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_data["nombre"]
                    st.session_state.user_role = user_data["role"]
                    st.session_state.user_faculty = user_data["facultad"]
                    st.session_state.user_career = user_data["carrera"]
                    st.success(f"¡Bienvenido(a), {user_data['nombre']}!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")

            if guest_btn:
                st.session_state.logged_in = True
                st.session_state.current_user = "Invitado"
                st.session_state.user_role = "invitado"
                st.session_state.user_faculty = "General"
                st.session_state.user_career = "General"
                st.success("Has ingresado como invitado.")
                st.rerun()

        st.markdown("---")
        st.markdown("### Credenciales de Prueba")
        st.markdown("""
        - **Estudiante:** `estudiante1` / `1234`
        - **Administrador:** `admin` / `admin123`
        """)

        st.markdown("</div>", unsafe_allow_html=True)


class MainDashboardView:
    """Main dashboard view"""

    @staticmethod
    def render():
        DashboardComponents.create_header("Dashboard Principal")

        # Load data
        data = DataManager.load_data()

        if not data["semester_ratings"].empty:
            # Overall metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                avg_rating = data["semester_ratings"].iloc[:, 1:].mean().mean()
                st.markdown(
                    DashboardComponents.create_metric_card(
                        "Calificación Promedio", f"{avg_rating:.1f}/10", icon="⭐"
                    ),
                    unsafe_allow_html=True,
                )

            with col2:
                total_faculties = len(data["semester_ratings"]) - 1  # Exclude GENERAL
                st.markdown(
                    DashboardComponents.create_metric_card(
                        "Facultades", total_faculties, icon="🏛️"
                    ),
                    unsafe_allow_html=True,
                )

            with col3:
                total_students = (
                    data["matcom_ratings"]["ID"].nunique()
                    if not data["matcom_ratings"].empty
                    else 0
                )
                st.markdown(
                    DashboardComponents.create_metric_card(
                        "Estudiantes", total_students, icon="👥"
                    ),
                    unsafe_allow_html=True,
                )

            with col4:
                avg_grade = (
                    data["matcom_classes"]["Nota"].mean()
                    if not data["matcom_classes"].empty
                    and "Nota" in data["matcom_classes"].columns
                    else 0
                )
                st.markdown(
                    DashboardComponents.create_metric_card(
                        "Nota Promedio", f"{avg_grade:.1f}/5", icon="📝"
                    ),
                    unsafe_allow_html=True,
                )

            st.divider()

            # Semester Rating Section
            st.subheader("📈 Calificación del Semestre")

            col1, col2 = st.columns([1, 2])
            with col1:
                st.pyplot(plots.rating_pie(avg_rating)[0])

            with col2:
                avg_by_category = data["semester_ratings"].iloc[:, 1:].mean()
                st.pyplot(plots.rating_hist(avg_by_category)[0])

            # Color legend
            st.pyplot(plots.color_legend()[0])

            # Faculty Averages
            with st.expander("📊 Ver Calificaciones por Facultad"):
                st.pyplot(
                    plots.fac_avrg(data["semester_ratings"].set_index("Facultad"))[0]
                )

            st.divider()

            # Faculty Gallery
            st.subheader("🏛️ Galería de Facultades")
            faculties = DataManager.get_faculties()
            cols = st.columns(4)

            for idx, faculty in enumerate(faculties[:8]):  # Show first 8
                with cols[idx % 4]:
                    # Try to load logo, fallback to placeholder
                    logo_path = f"logos/{faculty}.png"
                    if os.path.exists(logo_path):
                        st.image(logo_path, use_column_width=True)
                    else:
                        st.markdown(
                            f"""
                            <div style='background: #f0f2f6; padding: 2rem; text-align: center; border-radius: 10px;'>
                                <div style='font-size: 3rem;'>🏛️</div>
                                <div style='font-weight: bold;'>{faculty}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    st.caption(faculty)


class FacultyDashboardView:
    """Faculty-specific dashboard"""

    @staticmethod
    def render():
        faculty, career, semester = DashboardComponents.create_filter_bar()
        DashboardComponents.create_header(f"Dashboard de {faculty}", "🏛️")

        # Load data
        data = DataManager.load_data()

        if not data["semester_ratings"].empty:
            # Faculty info and rating
            col1, col2 = st.columns([1, 1])

            with col1:
                # Faculty rating
                faculty_ratings = data["semester_ratings"][
                    data["semester_ratings"]["Facultad"] == faculty
                ]
                if not faculty_ratings.empty:
                    faculty_avg = faculty_ratings.iloc[:, 1:].mean(axis=1).values[0]
                    st.pyplot(plots.rating_pie(faculty_avg)[0])

                    # Faculty metrics
                    st.metric("Calificación General", f"{faculty_avg:.1f}/10")
                    st.metric("Posición Ranking", "5/19")
                    st.metric("Tendencia", "+0.2%", delta="0.2 puntos")

            with col2:
                # Detailed ratings
                if not faculty_ratings.empty:
                    ratings = faculty_ratings.iloc[:, 1:].T
                    ratings.columns = ["Calificación"]
                    st.dataframe(
                        ratings.style.format("{:.1f}"), use_container_width=True
                    )

                    # Bar chart of ratings
                    st.pyplot(plots.rating_hist(ratings["Calificación"])[0])

        st.divider()

        # Careers in this faculty
        st.subheader("🎓 Carreras")
        careers = DataManager.get_careers(faculty)

        cols = st.columns(min(3, len(careers)))
        for idx, career_name in enumerate(careers):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div style='background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <h4>{career_name}</h4>
                        <p>📚 <strong>Estudiantes:</strong> 150</p>
                        <p>⭐ <strong>Promedio:</strong> 4.2/5</p>
                        <p>📈 <strong>Tasa Graduación:</strong> 85%</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )


class EvaluationView:
    """Semester and class evaluation views"""

    @staticmethod
    def render_semester_evaluation():
        DashboardComponents.create_header("Evaluar Semestre", "⭐")

        if st.session_state.user_role == "invitado":
            st.warning(
                "Los invitados no pueden realizar evaluaciones. Inicia sesión como estudiante."
            )
            return

        with st.form("semester_evaluation"):
            st.subheader("Califica tu semestre")

            # Dynamic categories from data
            data = DataManager.load_data()
            if not data["semester_ratings"].empty:
                categories = data["semester_ratings"].columns[1:].tolist()
            else:
                categories = [
                    "Respeto a los horarios",
                    "Disponibilidad de aulas",
                    "Facilidad para el E.I.",
                    "Bibliografía/Internet",
                    "Carga de trabajo",
                    "Ocio",
                ]

            ratings = {}
            cols = st.columns(2)
            for idx, category in enumerate(categories):
                with cols[idx % 2]:
                    ratings[category] = st.slider(
                        category,
                        min_value=1,
                        max_value=10,
                        value=6,
                        help=f"Califica: {category}",
                    )

            comment = st.text_area(
                "Comentarios adicionales",
                placeholder="Comparte tu experiencia general del semestre...",
            )

            submitted = st.form_submit_button("Enviar Evaluación")
            if submitted:
                st.success("✅ ¡Gracias por evaluar tu semestre!")
                st.balloons()

    @staticmethod
    def render_class_evaluation():
        DashboardComponents.create_header("Evaluar Clase", "📚")

        if st.session_state.user_role == "invitado":
            st.warning(
                "Los invitados no pueden realizar evaluaciones. Inicia sesión como estudiante."
            )
            return

        with st.form("class_evaluation"):
            # Class selection
            col1, col2 = st.columns(2)
            with col1:
                classes = [
                    "Visualización de Datos",
                    "Análisis Matemático I",
                    "Programación",
                    "Bases de Datos",
                    "Aprendizaje Automático",
                ]
                selected_class = st.selectbox("Selecciona la clase", classes)

            with col2:
                professors = [
                    "Dr. Carlos Méndez",
                    "Dra. Ana García",
                    "Prof. Miguel Torres",
                ]
                selected_professor = st.selectbox("Profesor", professors)

            # Rating categories
            st.subheader("Categorías de Evaluación")

            data = DataManager.load_data()
            if not data["subject_ratings"].empty:
                categories = data["subject_ratings"]["Categoria"].tolist()
            else:
                categories = [
                    "Calidad del profesor",
                    "Recursos didácticos",
                    "Carga de trabajo",
                    "Justicia en la evaluación",
                    "Utilidad de los contenidos",
                ]

            class_ratings = {}
            cols = st.columns(2)
            for idx, category in enumerate(categories):
                with cols[idx % 2]:
                    class_ratings[category] = st.slider(
                        category, min_value=1, max_value=10, value=6
                    )

            suggestions = st.text_area(
                "Sugerencias de mejora", placeholder="¿Qué mejorarías de esta clase?"
            )

            submitted = st.form_submit_button("Enviar Evaluación")
            if submitted:
                st.success("✅ ¡Gracias por evaluar esta clase!")
                st.balloons()


class CommentsView:
    """Comments and feedback view"""

    @staticmethod
    def render():
        DashboardComponents.create_header("Comentarios", "💬")

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_faculty = st.selectbox(
                "Facultad", ["Todas"] + DataManager.get_faculties()
            )
        with col2:
            filter_type = st.selectbox(
                "Tipo", ["Todos", "Semestre", "Clase", "Profesor"]
            )
        with col3:
            filter_sort = st.selectbox(
                "Ordenar por", ["Más recientes", "Mejor calificados", "Más útiles"]
            )

        # Comments list
        st.subheader("Comentarios de Estudiantes")

        for comment in st.session_state.comments:
            # Apply filters
            if filter_faculty != "Todas" and comment["facultad"] != filter_faculty:
                continue

            # Display comment card
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{comment['estudiante']}** - {comment['facultad']}")
                    st.markdown(f"*{comment['clase']}* con {comment['profesor']}")
                    st.markdown(f"> {comment['comentario']}")
                with col2:
                    if comment["calificacion"]:
                        st.metric("Calificación", f"{comment['calificacion']}/10")
                    st.caption(comment["fecha"])

            st.divider()

        # Add new comment
        if st.session_state.user_role not in ["invitado", "administrador"]:
            with st.expander("➕ Agregar Comentario"):
                with st.form("new_comment"):
                    comment_class = st.selectbox(
                        "Clase",
                        [
                            "Visualización de Datos",
                            "Programación",
                            "Matemáticas",
                            "Estadística",
                        ],
                    )
                    comment_text = st.text_area("Tu comentario", height=100)
                    rating = st.slider("Calificación (opcional)", 1, 10, 6)

                    submitted = st.form_submit_button("Publicar")
                    if submitted and comment_text:
                        new_comment = {
                            "estudiante": st.session_state.current_user,
                            "facultad": st.session_state.user_faculty,
                            "clase": comment_class,
                            "profesor": "Por definir",
                            "comentario": comment_text,
                            "calificacion": rating,
                            "fecha": datetime.now().strftime("%Y-%m-%d"),
                        }
                        st.session_state.comments.insert(0, new_comment)
                        st.success("Comentario publicado")
                        st.rerun()


# ============================================================================
# MAIN APPLICATION
# ============================================================================


class UniversityDashboard:
    """Main application controller"""

    def __init__(self):
        self.pages = {
            "📊 Dashboard Principal": MainDashboardView.render,
            "🏛️ Dashboard Facultad": FacultyDashboardView.render,
            "⭐ Evaluar Semestre": EvaluationView.render_semester_evaluation,
            "📚 Evaluar Clase": EvaluationView.render_class_evaluation,
            "💬 Comentarios": CommentsView.render,
        }

    def render_sidebar(self):
        """Render the application sidebar"""
        with st.sidebar:
            # User info
            if st.session_state.logged_in:
                st.markdown(
                    f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                             padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                        <h3 style='margin: 0;'>{st.session_state.current_user}</h3>
                        <p style='margin: 0; opacity: 0.8;'>{st.session_state.user_role.capitalize()}</p>
                        <p style='margin: 0; opacity: 0.8;'>{st.session_state.user_faculty}</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            # Navigation
            st.markdown("### Navegación")
            selected_page = st.radio(
                "Seleccionar página:",
                options=list(self.pages.keys()),
                label_visibility="collapsed",
            )

            st.session_state.current_page = selected_page

            st.divider()

            # Quick stats
            st.markdown("### 📈 Datos Rápidos")
            try:
                data = pd.read_csv("Semester_Rating.csv")
                avg_rating = data.iloc[:, 1:].mean().mean()
                st.metric("Calificación General", f"{avg_rating:.1f}/10")
                st.metric("Total Facultades", len(data) - 1)
            except:
                st.metric("Calificación General", "4.2/10")
                st.metric("Total Facultades", 19)

            st.divider()

            # Logout button
            if st.session_state.logged_in and st.button(
                "🚪 Cerrar Sesión", use_container_width=True
            ):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    def run(self):
        """Run the main application"""
        # Initialize session state
        AuthenticationManager.init_session_state()

        # Load data
        if not st.session_state.get("data"):
            st.session_state.data = DataManager.load_data()

        # Show login or main app
        if not st.session_state.logged_in:
            LoginView.render()
        else:
            self.render_sidebar()

            # Render selected page
            page_func = self.pages.get(st.session_state.current_page)
            if page_func:
                page_func()
            else:
                st.warning("Página no encontrada")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app = UniversityDashboard()
    app.run()
