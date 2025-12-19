import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

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

try:
    with open("style.css", "r") as style:
        st.markdown(
            f"""
            <style>
            {style.read()}
            </style>
            """,
            unsafe_allow_html=True,
        )
except:
    pass

# Minimal CSS for pointer cursor only
st.markdown(
    """
<style>
/* style.css - Enhanced version */
/* Custom styles for the University Dashboard */

/* Cursor pointers for interactive elements */
button, .stButton > button, .stSelectbox, .stSlider,
.stCheckbox, .stRadio, .stFormSubmitButton {
    cursor: pointer !important;
}

/* Consistent column heights */
[data-testid="column"] {
    min-height: 100px;
}

/* Faculty card styling */
.faculty-card {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    height: 280px !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.faculty-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

/* Consistent button heights */
.stButton > button {
    min-height: 40px !important;
    height: 40px !important;
    white-space: normal !important;
    word-wrap: break-word !important;
    line-height: 1.2 !important;
    padding: 8px 16px !important;
    margin: 0 !important;
}

/* Form element styling */
.stSelectbox > div > div {
    cursor: pointer !important;
}

.stSlider > div > div {
    cursor: pointer !important;
}

/* Dataframe hiding */
[data-testid="stDataFrame"] {
    display: none;
}

/* Consistent metric cards */
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* Chart container styling */
.chart-container {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Consistent spacing */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 10px 16px;
}
    /* Pointer cursors for interactive elements */
    button,
    .stButton > button,
    .stSelectbox > div,
    .stSlider > div,
    .stCheckbox > div,
    .stRadio > div,
    .stFormSubmitButton,
    .stTextInput > div,
    .stTextArea > div,
    .stNumberInput > div,
    .stDateInput > div,
    .stTimeInput > div,
    .stFileUploader > div,
    .stMultiSelect > div,
    .stColorPicker > div {
        cursor: pointer !important;
    }

    /* Slider handles */
    .stSlider > div > div > div > div {
        cursor: pointer !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# DATA MANAGEMENT
# ============================================================================


class DataManager:
    """Manages loading and accessing data for the dashboard"""

    # Faculty full names mapping
    FACULTY_FULL_NAMES = {
        "MATCOM": "Matemática y Computación",
        "FF": "Física",
        "FQ": "Química",
        "FBIO": "Biología",
        "FHS": "Historia y Sociología",
        "INSTEC": "Tecnologías y Ciencias Aplicadas",
        "FTUR": "Turismo",
        "FCOM": "Comunicación",
        "LEX": "Derecho",
        "PSICO": "Psicología",
        "FAYL": "Artes y Letras",
        "IFAL": "Farmacia y Alimentos",
        "ISDI": "Diseño Industrial",
        "CSGH": "Gestión Habana",
        "CONFIN": "Contabilidad y Finanzas",
        "EKO": "Economía",
        "GEO": "Geografía",
    }

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
                data[key] = pd.DataFrame()

        return data

    @staticmethod
    def get_faculties():
        """Get list of all faculties"""
        try:
            df = pd.read_csv("Semester_Rating.csv")
            faculties = df["Facultad"].tolist()
            return [f for f in faculties if f != "GENERAL"]
        except:
            return list(DataManager.FACULTY_FULL_NAMES.keys())

    @staticmethod
    def get_faculty_full_name(acronym):
        """Get full name of a faculty from its acronym"""
        return DataManager.FACULTY_FULL_NAMES.get(acronym, acronym)

    @staticmethod
    def get_careers(faculty="MATCOM"):
        """Get careers for a specific faculty"""
        careers_by_faculty = {
            "MATCOM": ["Matemática", "Ciencias de la Computación", "Ciencia de Datos"],
            "FF": ["Licenciatura en Física", "Ingeniería Física"],
            "FQ": ["Licenciatura en Química", "Ingeniería Química"],
            "FBIO": ["Licenciatura en Biología", "Microbiología", "Bioquímica"],
            "FHS": ["Licenciatura en Historia", "Sociología", "Filosofía"],
            "INSTEC": ["Fisica Nuclear", "Radioquimica", "Meteorologia"],
            "FTUR": ["Licenciatura en Turismo"],
            "FCOM": ["Comunicación Social", "Periodismo"],
            "LEX": ["Derecho"],
            "PSICO": ["Licenciatura en Psicología"],
            "FAYL": ["Licenciatura en Letras", "Historia del Arte"],
            "IFAL": ["Licenciatura en Farmacia", "Ciencia de los Alimentos"],
            "ISDI": ["Diseño Industrial", "Diseño de Comunicación Visual"],
            "CSGH": ["Gestión del Patrimonio Cultural"],
            "CONFIN": ["Licenciatura en Contabilidad y Finanzas"],
            "EKO": ["Licenciatura en Economía"],
            "GEO": ["Licenciatura en Geografía"],
        }
        return careers_by_faculty.get(faculty, ["Carrera Principal"])

    @staticmethod
    def get_faculty_rating(faculty):
        """Get rating data for a specific faculty"""
        try:
            df = pd.read_csv("Semester_Rating.csv")
            faculty_data = df[df["Facultad"] == faculty]
            if not faculty_data.empty:
                rating_columns = [
                    col for col in faculty_data.columns if col != "Facultad"
                ]
                avg_rating = faculty_data[rating_columns].mean(axis=1).values[0]
                return avg_rating, faculty_data[rating_columns].iloc[0].to_dict()
            return 0.0, {}
        except:
            return round(np.random.uniform(3, 9), 1), {}

    @staticmethod
    def get_career_rating(faculty):
        """Get rating data for a specific faculty"""
        try:
            df = pd.read_csv("")
            faculty_data = df[df["Facultad"] == faculty]
            if not faculty_data.empty:
                rating_columns = [
                    col for col in faculty_data.columns if col != "Facultad"
                ]
                avg_rating = faculty_data[rating_columns].mean(axis=1).values[0]
                return avg_rating, faculty_data[rating_columns].iloc[0].to_dict()
            return 0.0, {}
        except:
            return round(np.random.uniform(3, 9), 1), {}


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
            "selected_faculty": "MATCOM",
            "data": {},
            "comments": AuthenticationManager.load_sample_comments(),
            "semester_form_data": {"ratings": {}, "comment": ""},
            "class_form_data": {
                "class": "Visualización de Datos",
                "professor": "Dr. Carlos Méndez",
                "ratings": {},
                "suggestions": "",
            },
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
    def create_metric_card(title, value, icon="📊", color="#667eea"):
        """Create a metric card"""
        return f"""
            <div style='background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid {color};'>
                <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.5rem;'>{icon}</span>
                    <span style='font-weight: bold; color: #666;'>{title}</span>
                </div>
                <div style='font-size: 2rem; font-weight: bold; color: #333;'>{value}</div>
            </div>
        """

    @staticmethod
    def create_faculty_card(faculty_acronym, index):
        """Create a consistent faculty card with full name"""
        full_name = DataManager.get_faculty_full_name(faculty_acronym)

        # Truncate long names
        display_name = full_name
        if len(full_name) > 40:
            display_name = full_name[:37] + "..."

        # Create card in fixed height container
        with st.container():
            # Faculty icon and acronym
            found = False
            for element in os.listdir("logos"):
                if faculty_acronym.lower() in element:
                    found = True
                    with st.container():
                        img = Image.open("logos/" + element)
                        img = img.resize((300, 300))
                        st.image(img)
                        break
            if not found:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(
                            f"<div style='text-align: center; font-size: 2rem;'>🏛️</div>",
                            unsafe_allow_html=True,
                        )
                    with col2:
                        st.markdown(
                            f"<h3 style='margin: 0;'>{faculty_acronym}</h3>",
                            unsafe_allow_html=True,
                        )
            with st.container(height=100):
                # Full name
                st.markdown(
                    f"<div style='text-align: center; padding: 10px 0; font-size: 0.9rem; color: #666;'>{display_name}</div>",
                    unsafe_allow_html=True,
                )

            # Spacing
            # st.write("")
            # st.write("")

            # Explore button at bottom
            if st.button(
                "Explorar",
                key=f"faculty_btn_{faculty_acronym}_{index}",
                use_container_width=True,
            ):
                st.session_state.current_page = "🏛️ Dashboard Facultad"
                st.session_state.selected_faculty = faculty_acronym
                st.rerun()

    @staticmethod
    def create_student_distribution_chart():
        """Create a student distribution by year chart"""
        years_data = {
            "1er Año": np.random.randint(80, 120),
            "2do Año": np.random.randint(70, 110),
            "3er Año": np.random.randint(60, 100),
            "4to Año": np.random.randint(50, 90),
            "5to Año": np.random.randint(40, 80),
        }

        fig, ax = plt.subplots(figsize=(10, 6))

        colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(years_data)))

        bars = ax.bar(years_data.keys(), years_data.values(), color=colors)
        ax.set_xlabel("Año Académico", fontsize=12)
        ax.set_ylabel("Cantidad de Estudiantes", fontsize=12)
        ax.set_title(
            "Distribución de Estudiantes por Año", fontsize=14, fontweight="bold"
        )

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.5,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        return fig

    @staticmethod
    def create_career_comparison_chart(faculty):
        """Create a bar chart comparing careers by average grade"""
        careers = DataManager.get_careers(faculty)
        avg_grades = {
            career: round(np.random.uniform(3.5, 4.5), 2) for career in careers
        }

        fig, ax = plt.subplots(figsize=(12, 6))

        colors = plt.cm.viridis(np.linspace(0.3, 0.7, len(careers)))

        display_names = [
            name[:25] + "..." if len(name) > 25 else name for name in careers
        ]

        bars = ax.bar(display_names, avg_grades.values(), color=colors)
        ax.set_xlabel("Carrera", fontsize=12)
        ax.set_ylabel("Calificación Promedio (1-5)", fontsize=12)
        ax.set_title(
            f"Calificaciones Promedio por Carrera", fontsize=14, fontweight="bold"
        )
        ax.set_ylim(3.0, 5.0)

        # Add value labels
        for bar, grade in zip(bars, avg_grades.values()):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.02,
                f"{grade:.2f}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        return fig

    @staticmethod
    def create_grade_distribution_chart():
        """Create a grade distribution chart"""
        grades_data = {
            "2": np.random.randint(5, 15),
            "3": np.random.randint(20, 40),
            "4": np.random.randint(30, 50),
            "5": np.random.randint(10, 20),
        }

        fig, ax = plt.subplots(figsize=(8, 6))

        colors = ["#6baed6", "#4292c6", "#2171b5", "#084594"]

        bars = ax.bar(grades_data.keys(), grades_data.values(), color=colors)
        ax.set_xlabel("Nota", fontsize=12)
        ax.set_ylabel("Cantidad de Estudiantes", fontsize=12)
        ax.set_title("Distribución de Calificaciones", fontsize=14, fontweight="bold")

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.1,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        return fig


# ============================================================================
# PAGE VIEWS
# ============================================================================


class LoginView:
    """Login page view"""

    @staticmethod
    def render():
        DashboardComponents.create_header("Sistema de Evaluación", "🎓")

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


class MainDashboardView:
    """Main dashboard view"""

    @staticmethod
    def render():
        DashboardComponents.create_header("Dashboard Principal")

        # Load data
        data = DataManager.load_data()

        if not data["semester_ratings"].empty:
            # Overall metrics with equal columns
            col2, col3, col4 = st.columns(3)

            avg_rating = data["semester_ratings"].iloc[:, 1:].mean().mean()
            # with col1:
            # avg_rating = data["semester_ratings"].iloc[:, 1:].mean().mean()
            #     st.markdown(
            #         DashboardComponents.create_metric_card(
            #             "Calificación Promedio", f"{avg_rating:.1f}/10", icon="⭐"
            #         ),
            #         unsafe_allow_html=True,
            #     )

            with col2:
                total_faculties = len(data["semester_ratings"]) - 1
                st.markdown(
                    DashboardComponents.create_metric_card(
                        "Facultades", total_faculties, icon="🏛️"
                    ),
                    unsafe_allow_html=True,
                )

            with col3:
                # total_students = (
                #     data["matcom_ratings"]["ID"].nunique()
                #     if not data["matcom_ratings"].empty
                #     else 0
                # )
                total_students = 1429
                st.markdown(
                    DashboardComponents.create_metric_card(
                        "Estudiantes", f"{total_students:,}", icon="👥"
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
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(plots.color_legend()[0])
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(plots.rating_pie(avg_rating)[0])
            with col2:
                avg_by_category = data["semester_ratings"].iloc[:, 1:].mean()
                st.pyplot(plots.rating_hist(avg_by_category)[0])

            # Color legend

            # Faculty Averages
            with st.expander("📊 Ver Calificaciones por Facultad"):
                st.pyplot(
                    plots.fac_avrg(data["semester_ratings"].set_index("Facultad"))[0]
                )

            st.divider()

            # Faculty Gallery
            st.subheader("🏛️ Facultades de la Universidad")
            faculties = DataManager.get_faculties()

            # Create 4 equal columns
            cols = st.columns(4)

            for idx, faculty in enumerate(faculties):
                col_idx = idx % 4
                with cols[col_idx]:
                    DashboardComponents.create_faculty_card(faculty, idx)


class FacultyDashboardView:
    """Faculty-specific dashboard with integrated career information"""

    @staticmethod
    def render():
        # Get selected faculty from session state
        selected_faculty = st.session_state.get("selected_faculty", "MATCOM")

        # Faculty selector
        col1, col2 = st.columns([4, 1])
        with col1:
            selected_faculty = st.selectbox(
                "Selecciona una facultad",
                DataManager.get_faculties(),
                index=DataManager.get_faculties().index(selected_faculty)
                if selected_faculty in DataManager.get_faculties()
                else 0,
                key="faculty_selector",
            )

        # Store current faculty in session state
        st.session_state.selected_faculty = selected_faculty

        with col2:
            st.markdown("")
            st.markdown("")
            if st.button("⬅️ Volver", use_container_width=True):
                st.session_state.current_page = "📊 Dashboard Principal"
                st.rerun()

        DashboardComponents.create_header(f"Dashboard de {selected_faculty}", "🏛️")

        # Create tabs
        tab1, tab2, tab3 = st.tabs(
            ["📊 Información General", "🎓 Carreras", "📈 Rendimiento"]
        )

        with tab1:
            FacultyDashboardView.render_general_info(selected_faculty)

        with tab2:
            FacultyDashboardView.render_careers_section(selected_faculty)

        with tab3:
            FacultyDashboardView.render_performance_section(selected_faculty)

    @staticmethod
    def render_general_info(faculty):
        """Render general information about the faculty"""
        col1, col2 = st.columns([1, 1])

        with col1:
            descriptions = {
                "MATCOM": "La Facultad de Matemática y Computación (MATCOM) es el centro rector para la formación de profesionales en Matemática, Ciencias de la Computación y Ciencia de Datos en Cuba. Fundada en 1976, combina tradición matemática con innovación tecnológica.",
                "FF": "La Facultad de Física forma profesionales con sólida formación científica para la docencia, investigación e innovación tecnológica en diversas áreas de la física pura y aplicada.",
                "FQ": "Facultad de Química, centro de excelencia en la formación de químicos con capacidad para la investigación, producción y control de calidad en la industria química y farmacéutica.",
                "FBIO": "Facultad de Biología dedicada al estudio de los seres vivos, formando biólogos, microbiólogos y bioquímicos para la investigación y aplicación en ciencias de la vida.",
                "FHS": "Facultad de Historia y Sociología que estudia el desarrollo de las sociedades humanas, formando historiadores y sociólogos con visión crítica y analítica.",
                "INSTEC": "Instituto Superior de Tecnologías y Ciencias Aplicadas, centro de excelencia en ingenierías avanzadas y tecnologías de punta.",
                "FTUR": "Facultad de Turismo dedicada a la formación de profesionales para la gestión y desarrollo del sector turístico.",
                "FCOM": "Facultad de Comunicación Social que forma comunicadores y periodistas para los medios de comunicación y relaciones públicas.",
                "LEX": "Facultad de Derecho, formando juristas con sólidos conocimientos en ciencias jurídicas y sociales.",
                "PSICO": "Facultad de Psicología dedicada al estudio del comportamiento humano y la formación de psicólogos clínicos, educativos y organizacionales.",
                "FAYL": "Facultad de Artes y Letras, centro de formación en literatura, arte y cultura con tradición humanística.",
                "IFAL": "Instituto de Farmacia y Alimentos, especializado en ciencias farmacéuticas y tecnología de alimentos.",
                "ISDI": "Instituto Superior de Diseño Industrial, formando diseñadores para la industria y la comunicación visual.",
                "CSGH": "Centro de Estudios de Gestión Habana, especializado en administración, economía y negocios.",
            }

            st.markdown(f"""
                ### Sobre la Facultad
                {descriptions.get(faculty, "Facultad de la Universidad de La Habana con larga tradición académica y excelencia en la formación profesional.")}
            """)
        with col1:
            st.markdown("### 📋 Información Clave")
            info_data = {
                "📅 Año de fundación": FacultyDashboardView.get_founding_year(faculty),
                "👨‍🏫 Decano/Director": FacultyDashboardView.get_dean(faculty),
                "👥 Estudiantes activos": FacultyDashboardView.get_student_count(
                    faculty
                ),
                "📚 Programas académicos": len(DataManager.get_careers(faculty)),
                "🏫 Ubicación": "Universidad de La Habana, Vedado",
            }

            for label, value in info_data.items():
                st.markdown(f"**{label}:** {value}")

        with col2:
            logo_path = f"logos/{faculty}.png"
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
            else:
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                             border-radius: 10px; color: white;'>
                        <div style='font-size: 3rem;'>🏛️</div>
                        <h3 style='margin: 0.5rem 0;'>{faculty}</h3>
                        <p style='margin: 0; font-size: 0.9rem;'>{DataManager.get_faculty_full_name(faculty)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("### 📊 Estadísticas Rápidas")
            stats = FacultyDashboardView.get_faculty_stats(faculty)
            columns = st.columns(len(stats))
            for index, (stat, value) in enumerate(stats.items()):
                with columns[index]:
                    st.metric(stat, value)

        avg_rating, rating_details = DataManager.get_faculty_rating(faculty)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Calificación del Semestre")
            fig, ax = plots.rating_pie(avg_rating)
            st.pyplot(fig, use_container_width=True)

        with col2:
            if rating_details:
                st.markdown("### Calificación por Categoría")
                ratings_series = pd.Series(rating_details)
                fig, ax = plots.rating_hist(ratings_series)
                st.pyplot(fig, use_container_width=True)
            else:
                st.info("No hay datos de calificación disponibles por categoría")

    @staticmethod
    def render_careers_section(faculty):
        """Render detailed career information for the faculty"""
        st.header("🎓 Carreras Ofrecidas")
        # Career details
        careers = DataManager.get_careers(faculty)

        if not careers:
            st.info("No hay información de carreras disponible para esta facultad.")
            return

        selected_career = st.selectbox(
            "Selecciona una carrera para ver detalles",
            careers,
            key=f"career_select_{faculty}",
        )

        # Get faculty rating
        # avg_rating, rating_details = DataManager.get_faculty_rating(faculty)

        # # Two equal columns for rating charts
        # col1, col2 = st.columns(2)

        # with col1:
        #     st.markdown("### Calificación del Semestre")
        #     fig, ax = plots.rating_pie(avg_rating)
        #     st.pyplot(fig, use_container_width=True)

        # with col2:
        #     if rating_details:
        #         st.markdown("### Calificación por Categoría")
        #         ratings_series = pd.Series(rating_details)
        #         fig, ax = plots.rating_hist(ratings_series)
        #         st.pyplot(fig, use_container_width=True)
        #     else:
        #         st.info("No hay datos de calificación disponibles por categoría")

        st.divider()

        col1, col2 = st.columns([1, 1])

        with col1:
            career_info = FacultyDashboardView.get_career_info(faculty, selected_career)

            st.markdown(f"### {selected_career}")
            st.markdown(f"**Descripción:** {career_info['description']}")
            st.markdown(f"**Duración:** {career_info['duration']} años")
            st.markdown(f"**Título:** {career_info['degree']}")
            st.markdown(f"**Modalidad:** {career_info['modality']}")

            with st.expander("📚 Plan de Estudios"):
                subjects = FacultyDashboardView.get_career_subjects(
                    faculty, selected_career
                )
                for subject in subjects:
                    st.markdown(f"• {subject}")

        with col2:
            st.markdown("### 📈 Estadísticas")
            stats = FacultyDashboardView.get_career_stats(faculty, selected_career)
            columns = st.columns(len(stats) // 2)
            for index, (stat, value) in enumerate(stats.items()):
                with columns[index % 2]:
                    st.metric(stat, value)
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            with st.expander("🎯 Perfil del Graduado"):
                profile_points = FacultyDashboardView.get_graduate_profile(
                    faculty, selected_career
                )
                for point in profile_points:
                    st.markdown(f"✓ {point}")

    @staticmethod
    def render_performance_section(faculty):
        """Render academic performance data for the faculty"""
        st.header("📈 Rendimiento Académico")

        # Top metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_rating, _ = DataManager.get_faculty_rating(faculty)
            st.metric("Calificación General", f"{avg_rating:.1f}/10")

        with col2:
            student_count = FacultyDashboardView.get_student_count(faculty)
            st.metric("Estudiantes", student_count)

        with col3:
            avg_grade = FacultyDashboardView.get_average_grade(faculty)
            st.metric("Promedio Estudiantes", f"{avg_grade:.2f}")

        with col4:
            grad_rate = np.random.randint(75, 95)
            st.metric("Tasa Graduación", f"{grad_rate}%")

        st.divider()

        # Main charts - 2x2 grid
        st.subheader("📊 Visualizaciones")

        # First row
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 👥 Estudiantes por Año")
            enrollment_data = pd.DataFrame(
                {
                    "Brigada": ["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"],
                    "Count": [
                        np.random.randint(80, 120),
                        np.random.randint(70, 110),
                        np.random.randint(60, 100),
                        np.random.randint(50, 90),
                        np.random.randint(40, 80),
                    ],
                }
            )

            colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974"]
            fig, ax = plots.matr_pie(enrollment_data, colors)
            fig.set_size_inches(8, 6)
            plt.rcParams.update({"font.size": 12})
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.markdown("##### 📝 Distribución de Calificaciones")
            fig = FacultyDashboardView.create_grade_distribution_chart()
            st.pyplot(fig, use_container_width=True)

        # Second row
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("##### 📊 Promedio por Carrera")
            fig = FacultyDashboardView.create_career_average_chart(faculty)
            st.pyplot(fig, use_container_width=True)

        with col4:
            st.markdown("##### 📈 Evolución del Rendimiento")
            fig = FacultyDashboardView.create_performance_trend_chart(faculty)
            st.pyplot(fig, use_container_width=True)

    @staticmethod
    def create_grade_distribution_chart():
        """Create a clean grade distribution chart"""
        grades_data = {
            "2": np.random.randint(5, 15),
            "3": np.random.randint(20, 40),
            "4": np.random.randint(30, 50),
            "5": np.random.randint(10, 20),
        }

        fig, ax = plt.subplots(figsize=(10, 9))
        colors = ["#3182bd", "#4292c6", "#2171b5", "#084594"]

        bars = ax.bar(grades_data.keys(), grades_data.values(), color=colors)
        ax.set_xlabel("Nota", fontsize=14)
        ax.set_ylabel("Cantidad de Estudiantes", fontsize=14)
        ax.set_title(
            "Distribución de Calificaciones", fontsize=16, fontweight="bold", pad=20
        )

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.5,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold",
            )

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        return fig

    @staticmethod
    def create_career_average_chart(faculty):
        """Create career average grades chart"""
        careers = DataManager.get_careers(faculty)
        avg_grades = {
            career: round(np.random.uniform(3.5, 4.5), 2) for career in careers
        }

        fig, ax = plt.subplots(figsize=(10, 10))
        colors = plt.cm.viridis(np.linspace(0.3, 0.7, len(careers)))

        display_names = [
            name[:20] + "..." if len(name) > 20 else name for name in careers
        ]

        bars = ax.bar(display_names, avg_grades.values(), color=colors)
        ax.set_ylabel("Calificación Promedio (1-5)", fontsize=14)
        ax.set_ylim(3.0, 5.0)
        ax.set_title(
            "Calificaciones Promedio por Carrera",
            fontsize=16,
            fontweight="bold",
            pad=20,
        )

        for bar, grade in zip(bars, avg_grades.values()):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.02,
                f"{grade:.2f}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold",
            )

        plt.xticks(rotation=45, ha="right", fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        return fig

    @staticmethod
    def create_performance_trend_chart(faculty):
        """Create performance trend chart"""
        years = ["2019", "2020", "2021", "2022", "2023"]
        performance = [round(np.random.uniform(3.3, 4.7), 2) for _ in years]

        fig, ax = plt.subplots(figsize=(10, 9))
        ax.plot(
            years, performance, marker="o", linewidth=3, markersize=10, color="#3182bd"
        )
        ax.set_xlabel("Año", fontsize=14)
        ax.set_ylabel("Calificación Promedio", fontsize=14)
        ax.set_title(
            "Evolución del Rendimiento", fontsize=16, fontweight="bold", pad=20
        )
        ax.set_ylim(3.0, 5.0)
        ax.grid(True, alpha=0.3)

        for i, (year, perf) in enumerate(zip(years, performance)):
            ax.text(
                i,
                perf + 0.05,
                f"{perf:.2f}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold",
                bbox=dict(facecolor="white", alpha=0.8),
            )

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        return fig

    @staticmethod
    def get_founding_year(faculty):
        """Get founding year for a faculty"""
        founding_years = {
            "MATCOM": "1976",
            "FF": "1962",
            "FQ": "1963",
            "FBIO": "1964",
            "FHS": "1962",
            "INSTEC": "1980",
            "FTUR": "1995",
            "FCOM": "1990",
            "LEX": "1900",
            "PSICO": "1970",
            "FAYL": "1962",
            "IFAL": "1975",
            "ISDI": "1985",
            "CSGH": "1998",
        }
        return founding_years.get(faculty, "1960")

    @staticmethod
    def get_dean(faculty):
        """Get dean/director for a faculty"""
        deans = {
            "MATCOM": "Dr. Carlos Martínez",
            "FF": "Dr. Arbelio Pentón Madrigal",
            "FQ": "Dra. Marta Álvarez",
            "FBIO": "Dr. Pedro Pablo García",
            "FHS": "Dra. Mayra Mena",
            "INSTEC": "Dr. Roberto González",
            "FTUR": "MSc. Ana López",
            "FCOM": "Dr. Julio García",
            "LEX": "Dr. Fernando Martínez",
            "PSICO": "Dra. Laura Rodríguez",
            "FAYL": "Dr. Jorge Pérez",
            "IFAL": "Dra. Carmen Ruiz",
            "ISDI": "MSc. Alejandro Díaz",
            "CSGH": "Dr. Ricardo Fernández",
        }
        return deans.get(faculty, "Por definir")

    @staticmethod
    def get_student_count(faculty):
        """Get student count for a faculty"""
        student_counts = {
            "MATCOM": "550",
            "FF": "420",
            "FQ": "380",
            "FBIO": "450",
            "FHS": "320",
            "INSTEC": "280",
            "FTUR": "200",
            "FCOM": "250",
            "LEX": "600",
            "PSICO": "350",
            "FAYL": "280",
            "IFAL": "220",
            "ISDI": "180",
            "CSGH": "150",
        }
        return student_counts.get(faculty, "300")

    @staticmethod
    def get_faculty_stats(faculty):
        """Get various statistics for a faculty"""
        return {
            "Profesores": str(np.random.randint(40, 100)),
            "Laboratorios": str(np.random.randint(5, 20)),
            "Proyectos activos": str(np.random.randint(10, 50)),
        }

    @staticmethod
    def get_average_grade(faculty):
        """Get average student grade for the faculty"""
        return round(np.random.uniform(3.5, 4.5), 2)

    @staticmethod
    def get_career_info(faculty, career):
        """Get detailed information about a specific career"""
        durations = {
            "Matemática": 5,
            "Ciencias de la Computación": 5,
            "Ciencia de Datos": 4,
            "Licenciatura en Física": 5,
            "Ingeniería Física": 5,
            "Licenciatura en Química": 5,
            "Licenciatura en Biología": 5,
            "Licenciatura en Microbiología": 5,
            "Licenciatura en Bioquímica y Biología Molecular": 5,
            "Licenciatura en Historia": 5,
            "Licenciatura en Sociología": 5,
            "Licenciatura en Filosofía": 5,
            "Ingeniería en Telecomunicaciones": 5,
            "Ingeniería Eléctrica": 5,
            "Ingeniería en Ciencias Aplicadas": 5,
            "Licenciatura en Turismo": 5,
            "Comunicación Social": 5,
            "Periodismo": 5,
            "Derecho": 5,
            "Licenciatura en Psicología": 5,
            "Licenciatura en Lenguas Extranjeras": 5,
            "Licenciatura en Letras": 5,
            "Licenciatura en Historia del Arte": 5,
            "Licenciatura en Geografía": 5,
            "Licenciatura en Farmacia": 5,
            "Licenciatura en Ciencia de los Alimentos": 5,
            "Diseño Industrial": 5,
            "Diseño de Comunicación Visual": 5,
            "Preservación y Gestión del Patrimonio Cultural": 5,
            "Licenciatura en Economía": 5,
            "Licenciatura en Administración de Empresas": 5,
            "Licenciatura en Contabilidad y Finanzas": 5,
        }

        descriptions = {
            "Matemática": "Formación sólida en matemáticas puras y aplicadas, preparando para investigación y aplicación en diversas áreas científicas y tecnológicas.",
            "Ciencias de la Computación": "Formación en fundamentos teóricos y prácticos de la computación, algoritmos, sistemas y desarrollo de software.",
            "Ciencia de Datos": "Formación interdisciplinaria en matemáticas, estadística y computación para extraer conocimiento de datos complejos.",
            "Licenciatura en Física": "Formación en leyes fundamentales de la naturaleza, métodos experimentales y aplicaciones tecnológicas.",
            "Ingeniería Física": "Aplicación de principios físicos al diseño y desarrollo de tecnologías y sistemas innovadores.",
            "Licenciatura en Química": "Estudio de la composición, propiedades y transformaciones de la materia, con aplicaciones industriales y ambientales.",
        }

        default_desc = f"Carrera de {career} en la facultad de {faculty}, formando profesionales con excelencia académica y preparación integral."

        return {
            "description": descriptions.get(career, default_desc),
            "duration": durations.get(career, 5),
            "degree": "Licenciado/a"
            if "Licenciatura" in career
            else "Ingeniero/a"
            if "Ingeniería" in career
            else "Profesional",
            "modality": "Presencial",
        }

    @staticmethod
    def get_career_stats(faculty, career):
        """Get statistics for a specific career"""
        return {
            "Estudiantes": str(np.random.randint(50, 300)),
            "Tasa graduación": f"{np.random.randint(75, 95)}%",
            "Demanda": np.random.choice(["Alta", "Media", "Baja"], p=[0.6, 0.3, 0.1]),
            "Empleabilidad": f"{np.random.randint(80, 98)}%",
        }

    @staticmethod
    def get_career_subjects(faculty, career):
        """Get main subjects for a career"""
        subjects_by_career = {
            "Matemática": [
                "Análisis Matemático I-IV",
                "Álgebra Lineal y Abstracta",
                "Geometría Diferencial",
                "Ecuaciones Diferenciales",
                "Análisis Numérico",
                "Topología",
            ],
            "Ciencias de la Computación": [
                "Algoritmos y Estructuras de Datos",
                "Bases de Datos Avanzadas",
                "Sistemas Operativos",
                "Redes de Computadoras",
                "Inteligencia Artificial",
                "Ingeniería de Software",
            ],
            "Ciencia de Datos": [
                "Estadística Matemática",
                "Machine Learning",
                "Visualización de Datos",
                "Big Data y Cloud Computing",
                "Minería de Datos",
                "Procesamiento de Lenguaje Natural",
            ],
            "Licenciatura en Física": [
                "Mecánica Clásica",
                "Electromagnetismo",
                "Termodinámica y Mecánica Estadística",
                "Mecánica Cuántica",
                "Física del Estado Sólido",
                "Óptica y Fotónica",
            ],
        }

        default_subjects = [
            "Fundamentos de la Carrera",
            "Metodología de la Investigación",
            "Taller de Integración Profesional",
            "Práctica Profesional Supervisada",
            "Trabajo de Diploma o Tesis",
        ]

        return subjects_by_career.get(career, default_subjects)

    @staticmethod
    def get_graduate_profile(faculty, career):
        """Get graduate profile points for a career"""
        profiles = {
            "Matemática": [
                "Capacidad para modelar y resolver problemas matemáticos complejos en diversos contextos",
                "Habilidades avanzadas en análisis matemático, álgebra y geometría",
                "Competencia en métodos matemáticos aplicados a ciencias, ingeniería y tecnología",
                "Capacidad para investigación matemática pura y aplicada de alto nivel",
                "Habilidades para la docencia y transferencia de conocimiento matemático",
            ],
            "Ciencias de la Computación": [
                "Desarrollo de software robusto, escalable y de alta calidad",
                "Diseño y análisis de algoritmos eficientes para problemas complejos",
                "Administración y configuración de sistemas computacionales y redes",
                "Implementación y gestión de bases de datos seguras y eficientes",
                "Gestión de proyectos de desarrollo tecnológico e innovación",
            ],
            "Ciencia de Datos": [
                "Extracción de insights valiosos y conocimiento de datos complejos y masivos",
                "Implementación de modelos de machine learning y aprendizaje automático",
                "Visualización efectiva y comunicativa de información y resultados",
                "Gestión integral de proyectos de análisis de datos y business intelligence",
                "Comunicación de resultados técnicos a audiencias técnicas y no técnicas",
            ],
        }

        default_profile = [
            "Formación integral en los fundamentos teóricos y prácticos de la disciplina",
            "Capacidad para investigación científica básica y aplicada de calidad",
            "Habilidades para el trabajo en equipo multidisciplinario y colaborativo",
            "Competencia para la identificación y resolución de problemas complejos",
            "Compromiso ético, responsabilidad social y profesionalismo",
        ]

        return profiles.get(career, default_profile)


class EvaluationView:
    """Semester and class evaluation views"""

    @staticmethod
    def render_semester_evaluation():
        DashboardComponents.create_header("Evaluar Semestre", "⭐")

        if st.session_state.user_role in ["invitado", "administrador"]:
            user_role = (
                "invitados"
                if st.session_state.user_role == "invitado"
                else "administradores"
            )
            st.warning(f"Los {user_role} no pueden realizar evaluaciones.")
            return

        # Categories with detailed tooltips
        categories = [
            "Respeto a los horarios",
            "Disponibilidad de aulas",
            "Facilidad para el E.I.",
            "Bibliografía/Internet",
            "Carga de trabajo",
            "Ocio",
        ]

        tooltips = {
            "Respeto a los horarios": "¿Se respetan los horarios de clases y actividades programadas?",
            "Disponibilidad de aulas": "¿Hay suficientes aulas disponibles y están en buen estado?",
            "Facilidad para el E.I.": "¿Es fácil acceder a la enseñanza individualizada cuando se necesita?",
            "Bibliografía/Internet": "¿Hay suficiente material bibliográfico y acceso a Internet para estudiar?",
            "Carga de trabajo": "¿Es adecuada y equilibrada la carga de trabajo del semestre?",
            "Ocio": "¿Hay suficiente tiempo y espacios para actividades recreativas y deportivas?",
        }

        with st.form("semester_evaluation", clear_on_submit=False):
            st.subheader("Califica tu semestre (1-10)")

            # Ratings in two columns
            ratings = {}
            cols = st.columns(2)

            for idx, category in enumerate(categories):
                with cols[idx % 2]:
                    # Get saved value or default to 6
                    saved_value = st.session_state.semester_form_data["ratings"].get(
                        category, 6
                    )
                    ratings[category] = st.slider(
                        label=category,
                        min_value=1,
                        max_value=10,
                        value=saved_value,
                        help=tooltips.get(category, ""),
                        key=f"slider_{category}",
                    )

            comment = st.text_area(
                "Comentarios adicionales",
                value=st.session_state.semester_form_data.get("comment", ""),
                placeholder="Comparte tu experiencia general del semestre...",
                height=100,
            )

            submitted = st.form_submit_button(
                "📤 Enviar Evaluación", use_container_width=True
            )
            # Form buttons
            # col1, col2 = st.columns(2)
            # with col1:
            #     submitted = st.form_submit_button(
            #         "📤 Enviar Evaluación", use_container_width=True
            #     )
            # with col2:
            #     reset_clicked = st.form_submit_button(
            #         "🔄 Limpiar Formulario", use_container_width=True
            #     )

            # if reset_clicked:
            #     # Clear all form data
            #     st.session_state.semester_form_data = {"ratings": {}, "comment": ""}

            #     # Clear slider values by re-rendering
            #     for category in categories:
            #         if f"slider_{category}" in st.session_state:
            #             del st.session_state[f"slider_{category}"]

            #     st.success("¡Formulario limpiado!")
            #     st.rerun()

            if submitted:
                # Save form data
                st.session_state.semester_form_data = {
                    "ratings": ratings,
                    "comment": comment,
                }

                # Calculate average
                avg_rating = sum(ratings.values()) / len(ratings)

                # Show success message with summary
                st.success("✅ ¡Gracias por evaluar tu semestre!")

                # Display summary
                with st.expander("📋 Ver Resumen de tu Evaluación"):
                    st.metric("Calificación Promedio", f"{avg_rating:.1f}/10")
                    st.write("**Detalle por categoría:**")
                    for category, rating in ratings.items():
                        st.write(f"• {category}: {rating}/10")

                    if comment.strip():
                        st.write("**Tu comentario:**")
                        st.write(f"> {comment}")

                st.balloons()

    @staticmethod
    def render_class_evaluation():
        DashboardComponents.create_header("Evaluar Clase", "📚")

        if st.session_state.user_role in ["invitado", "administrador"]:
            user_role = (
                "invitados"
                if st.session_state.user_role == "invitado"
                else "administradores"
            )
            st.warning(f"Los {user_role} no pueden realizar evaluaciones.")
            return

        with st.form("class_evaluation", clear_on_submit=False):
            # Class selection
            # col1, col2 = st.columns(2)
            # with col1:
            #     classes = [
            #         "Visualización de Datos",
            #         "Análisis Matemático I",
            #         "Programación",
            #         "Bases de Datos",
            #         "Aprendizaje Automático",
            #     ]
            #     selected_class = st.selectbox(
            #         "Selecciona la clase",
            #         classes,
            #         index=classes.index(
            #             st.session_state.class_form_data.get(
            #                 "class", "Visualización de Datos"
            #             )
            #         ),
            #     )

            # with col2:
            #     professors = [
            #         "Dr. Carlos Méndez",
            #         "Dra. Ana García",
            #         "Prof. Miguel Torres",
            #         "Dra. Laura Rodríguez",
            #         "Dr. Javier López",
            #     ]
            #     selected_professor = st.selectbox(
            #         "Profesor",
            #         professors,
            #         index=professors.index(
            #             st.session_state.class_form_data.get(
            #                 "professor", "Dr. Carlos Méndez"
            #             )
            #         ),
            #     )

            classes = [
                "Visualización de Datos",
                "Análisis Matemático I",
                "Programación",
                "Bases de Datos",
                "Aprendizaje Automático",
            ]
            selected_class = st.selectbox(
                "Selecciona la clase",
                classes,
                index=classes.index(
                    st.session_state.class_form_data.get(
                        "class", "Visualización de Datos"
                    )
                ),
            )
            # Rating categories with tooltips
            st.subheader("Categorías de Evaluación (1-10)")

            categories = [
                "Calidad del profesor",
                "Recursos didácticos",
                "Carga de trabajo",
                "Justicia en la evaluación",
                "Utilidad de los contenidos",
            ]

            class_tooltips = {
                "Calidad del profesor": "¿El profesor explica claramente y motiva el aprendizaje?",
                "Recursos didácticos": "¿Los materiales y recursos de enseñanza son adecuados?",
                "Carga de trabajo": "¿Es apropiada la cantidad de trabajo para esta clase?",
                "Justicia en la evaluación": "¿Las evaluaciones son justas y transparentes?",
                "Utilidad de los contenidos": "¿Los contenidos son relevantes para tu formación profesional?",
            }

            class_ratings = {}
            cols = st.columns(2)
            for idx, category in enumerate(categories):
                with cols[idx % 2]:
                    saved_value = st.session_state.class_form_data["ratings"].get(
                        category, 6
                    )
                    class_ratings[category] = st.slider(
                        category,
                        min_value=1,
                        max_value=10,
                        value=saved_value,
                        help=class_tooltips.get(category, ""),
                        key=f"class_slider_{category}",
                    )

            suggestions = st.text_area(
                "Sugerencias de mejora",
                value=st.session_state.class_form_data.get("suggestions", ""),
                placeholder="¿Qué mejorarías de esta clase?",
                height=100,
            )

            submitted = st.form_submit_button(
                "📤 Enviar Evaluación", use_container_width=True
            )
            # Form buttons
            # col1, col2 = st.columns(2)
            # with col1:
            #     submitted = st.form_submit_button(
            #         "📤 Enviar Evaluación", use_container_width=True
            #     )
            # with col2:
            #     reset_clicked = st.form_submit_button(
            #         "🔄 Limpiar Formulario", use_container_width=True
            #     )

            # if reset_clicked:
            #     # Clear all form data
            #     st.session_state.class_form_data = {
            #         "class": "Visualización de Datos",
            #         "professor": "Dr. Carlos Méndez",
            #         "ratings": {},
            #         "suggestions": "",
            #     }

            #     # Clear slider values
            #     for category in categories:
            #         if f"class_slider_{category}" in st.session_state:
            #             del st.session_state[f"class_slider_{category}"]

            #     st.success("¡Formulario limpiado!")
            #     st.rerun()

            if submitted:
                # Save form data
                st.session_state.class_form_data = {
                    "class": selected_class,
                    # "professor": selected_professor,
                    "ratings": class_ratings,
                    "suggestions": suggestions,
                }

                # Calculate average
                avg_rating = sum(class_ratings.values()) / len(class_ratings)

                # Show success message
                st.success(f"✅ ¡Gracias por evaluar {selected_class}!")

                # Display summary
                with st.expander("📋 Ver Resumen de tu Evaluación"):
                    st.metric("Calificación Promedio", f"{avg_rating:.1f}/10")
                    st.write(f"**Clase:** {selected_class}")
                    # st.write(f"**Profesor:** {selected_professor}")
                    st.write("**Detalle por categoría:**")
                    for category, rating in class_ratings.items():
                        st.write(f"• {category}: {rating}/10")

                    if suggestions.strip():
                        st.write("**Tus sugerencias:**")
                        st.write(f"> {suggestions}")

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
                    # rating = st.slider("Calificación (opcional)", 1, 10, 6)

                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button(
                            "📤 Publicar", use_container_width=True
                        )
                    with col2:
                        if st.form_submit_button(
                            "❌ Cancelar", use_container_width=True
                        ):
                            st.rerun()

                    if submitted and comment_text:
                        new_comment = {
                            "estudiante": st.session_state.current_user,
                            "facultad": st.session_state.user_faculty,
                            "carrera": st.session_state.user_career,
                            "clase": comment_class,
                            "profesor": "Dr. Marlon Castro",
                            "comentario": comment_text,
                            "calificacion": None,
                            "fecha": datetime.now().strftime("%Y-%m-%d"),
                        }
                        st.session_state.comments.insert(0, new_comment)
                        st.success("✅ Comentario publicado")
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
            # User info with career
            if st.session_state.logged_in:
                st.markdown(
                    f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                             padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                        <h3 style='margin: 0;'>{st.session_state.current_user}</h3>
                        <p style='margin: 5px 0; opacity: 0.9;'>
                            <strong>Rol:</strong> {st.session_state.user_role.capitalize()}
                        </p>
                        <p style='margin: 5px 0; opacity: 0.9;'>
                            <strong>Facultad:</strong> {st.session_state.user_faculty}
                        </p>
                        <p style='margin: 5px 0; opacity: 0.9;'>
                            <strong>Carrera:</strong> {st.session_state.user_career}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Navigation
            st.markdown("### Navegación")

            # Get current page index
            page_names = list(self.pages.keys())
            current_page = st.session_state.current_page
            current_index = (
                page_names.index(current_page) if current_page in page_names else 0
            )

            selected_page = st.radio(
                "Seleccionar página:",
                options=page_names,
                index=current_index,
                label_visibility="collapsed",
            )

            # Update session state if page changed
            if selected_page != st.session_state.current_page:
                st.session_state.current_page = selected_page
                st.rerun()

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
                st.metric("Total Facultades", len(DataManager.get_faculties()))

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
