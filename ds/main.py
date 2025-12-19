import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import plot utilities
import plots

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Dashboard Universitario - UH",
    page_icon="🎓",
    layout="centered",
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
        """Get careers for a specific faculty with real data from University of Havana"""
        careers_by_faculty = {
            "MATCOM": ["Matemática", "Ciencias de la Computación", "Ciencia de Datos"],
            "FF": ["Licenciatura en Física", "Ingeniería Física"],
            "FQ": ["Licenciatura en Química"],
            "FBIOM": [
                "Licenciatura en Biología",
                "Licenciatura en Microbiología",
                "Licenciatura en Bioquímica y Biología Molecular",
            ],
            "FHS": [
                "Licenciatura en Historia",
                "Licenciatura en Sociología",
                "Licenciatura en Filosofía",
            ],
            "INSTEC": [
                "Ingeniería en Telecomunicaciones",
                "Ingeniería Eléctrica",
                "Ingeniería en Ciencias Aplicadas",
            ],
            "FTUR": ["Licenciatura en Turismo"],
            "FCOM": ["Comunicación Social", "Periodismo"],
            "LEX": ["Derecho"],
            "PSICO": ["Licenciatura en Psicología"],
            "FLEX": ["Licenciatura en Lenguas Extranjeras"],
            "FAYL": ["Licenciatura en Letras", "Licenciatura en Historia del Arte"],
            "GEO": ["Licenciatura en Geografía"],
            "IFAL": [
                "Licenciatura en Farmacia",
                "Licenciatura en Ciencia de los Alimentos",
            ],
            "ISDI": ["Diseño Industrial", "Diseño de Comunicación Visual"],
            "CSGH": ["Preservación y Gestión del Patrimonio Cultural"],
            "FENHI": [
                "Licenciatura en Economía",
                "Licenciatura en Administración de Empresas",
            ],
            "CONFIN": ["Licenciatura en Contabilidad y Finanzas"],
            "EKO": ["Licenciatura en Economía"],
            "FDER": ["Derecho"],
            "FARQ": ["Arquitectura"],
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

            st.subheader("🏛️ Galería de Facultades")
            faculties = DataManager.get_faculties()
            cols = st.columns(4)

            for idx, faculty in enumerate(faculties[:8]):  # Show first 8 faculties
                with cols[idx % 4]:
                    # Display faculty card
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

                    # Navigation button with onclick functionality
                    if st.button(
                        f"Explorar {faculty}",
                        key=f"faculty_btn_{idx}",
                        use_container_width=True,
                    ):
                        # Update session state for navigation
                        st.session_state.current_page = "🏛️ Dashboard Facultad"
                        st.session_state.selected_faculty = faculty
                        st.session_state.show_faculty_filter = (
                            False  # Hide filter initially
                        )
                        st.rerun()

            # Show more faculties button if there are more
            if len(faculties) > 8:
                if st.button("Ver todas las facultades", use_container_width=True):
                    st.session_state.show_all_faculties = True
                    st.rerun()

            if st.session_state.get("show_all_faculties", False):
                st.subheader("Todas las Facultades")
                all_cols = st.columns(4)
                for idx, faculty in enumerate(faculties[8:]):
                    with all_cols[idx % 4]:
                        st.markdown(f"**{faculty}**")
                        if st.button(f"Ir a {faculty}", key=f"all_faculty_btn_{idx}"):
                            st.session_state.current_page = "🏛️ Dashboard Facultad"
                            st.session_state.selected_faculty = faculty
                            st.rerun()


# Updated FacultyDashboardView class with integrated career dashboard
class FacultyDashboardView:
    """Faculty-specific dashboard with integrated career information"""

    @staticmethod
    def render():
        # Get selected faculty from session state or use selectbox
        if "selected_faculty_from_main" in st.session_state:
            selected_faculty = st.session_state.selected_faculty_from_main
            # Clear the flag so it doesn't persist
            del st.session_state.selected_faculty_from_main
        else:
            selected_faculty = st.selectbox(
                "Selecciona una facultad",
                DataManager.get_faculties(),
                index=DataManager.get_faculties().index(
                    st.session_state.get("current_faculty", "MATCOM")
                ),
            )

        # Store current faculty in session state
        st.session_state.current_faculty = selected_faculty

        DashboardComponents.create_header(f"Dashboard de {selected_faculty}", "🏛️")

        # Back button to main dashboard
        if st.button("⬅️ Volver al Dashboard Principal", use_container_width=True):
            st.session_state.current_page = "📊 Dashboard Principal"
            st.rerun()

        # Create tabs for different sections
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
        col1, col2 = st.columns([2, 1])

        with col1:
            # Faculty description
            descriptions = {
                "MATCOM": "La Facultad de Matemática y Computación (MATCOM) es el centro rector para la formación de profesionales en Matemática, Ciencias de la Computación y Ciencia de Datos en Cuba. Fundada en 1976, combina tradición matemática con innovación tecnológica.",
                "FF": "La Facultad de Física forma profesionales con sólida formación científica para la docencia, investigación e innovación tecnológica en diversas áreas de la física pura y aplicada.",
                "FQ": "Facultad de Química, centro de excelencia en la formación de químicos con capacidad para la investigación, producción y control de calidad en la industria química y farmacéutica.",
                "FBIOM": "Facultad de Biología dedicada al estudio de los seres vivos, formando biólogos, microbiólogos y bioquímicos para la investigación y aplicación en ciencias de la vida.",
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

            # Key information
            st.markdown("### 📋 Información Clave")
            info_data = {
                "📅 Año de fundación": FacultyDashboardView.get_founding_year(faculty),
                "👨‍🏫 Decano/Director": FacultyDashboardView.get_dean(faculty),
                "👥 Estudiantes activos": FacultyDashboardView.get_student_count(
                    faculty
                ),
                "📚 Programas académicos": len(DataManager.get_careers(faculty)),
                "🏫 Ubicación": "Universidad de La Habana, Vedado",
                "🌐 Sitio web": f"www.uh.cu/facultades/{faculty.lower()}",
            }

            for label, value in info_data.items():
                st.markdown(f"**{label}:** {value}")

        with col2:
            # Display faculty logo or placeholder
            logo_path = f"logos/{faculty}.png"
            if os.path.exists(logo_path):
                st.image(logo_path, use_column_width=True)
            else:
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                             border-radius: 10px; color: white;'>
                        <div style='font-size: 4rem;'>🏛️</div>
                        <h3>{faculty}</h3>
                        <p>Universidad de La Habana</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            # Quick stats
            st.markdown("### 📊 Estadísticas Rápidas")
            stats = FacultyDashboardView.get_faculty_stats(faculty)

            for stat, value in stats.items():
                st.metric(stat, value)

    @staticmethod
    def render_careers_section(faculty):
        """Render detailed career information for the faculty"""
        st.header("🎓 Carreras Ofrecidas")

        careers = DataManager.get_careers(faculty)

        if not careers:
            st.info("No hay información de carreras disponible para esta facultad.")
            return

        # Career selector
        selected_career = st.selectbox(
            "Selecciona una carrera para ver detalles",
            careers,
            key=f"career_select_{faculty}",
        )

        st.divider()

        # Career details
        col1, col2 = st.columns([2, 1])

        with col1:
            # Career description
            career_info = FacultyDashboardView.get_career_info(faculty, selected_career)

            st.markdown(f"### {selected_career}")
            st.markdown(f"**Descripción:** {career_info['description']}")
            st.markdown(f"**Duración:** {career_info['duration']} años")
            st.markdown(f"**Título que otorga:** {career_info['degree']}")
            st.markdown(f"**Modalidad:** {career_info['modality']}")
            st.markdown(f"**Coordinador:** {career_info['coordinator']}")

            # Curriculum highlights
            with st.expander("📚 Plan de Estudios (Materias Principales)"):
                subjects = FacultyDashboardView.get_career_subjects(
                    faculty, selected_career
                )
                for subject in subjects:
                    st.markdown(f"- {subject}")

        with col2:
            # Career statistics
            st.markdown("### 📈 Estadísticas")

            stats = FacultyDashboardView.get_career_stats(faculty, selected_career)
            for stat, value in stats.items():
                st.metric(stat, value)

            # Graduate profile
            st.markdown("### 🎯 Perfil del Graduado")
            profile_points = FacultyDashboardView.get_graduate_profile(
                faculty, selected_career
            )
            for point in profile_points[:3]:  # Show first 3 points
                st.markdown(f"✓ {point}")

            if len(profile_points) > 3:
                with st.expander("Ver perfil completo"):
                    for point in profile_points[3:]:
                        st.markdown(f"✓ {point}")

        st.divider()

        # All careers overview
        st.subheader("📋 Resumen de Todas las Carreras")

        careers_data = []
        for career in careers:
            info = FacultyDashboardView.get_career_info(faculty, career)
            stats = FacultyDashboardView.get_career_stats(faculty, career)

            careers_data.append(
                {
                    "Carrera": career,
                    "Duración": info["duration"],
                    "Estudiantes": stats.get("Estudiantes", "N/A"),
                    "Promedio": stats.get("Promedio", "N/A"),
                    "Demanda": stats.get("Demanda", "Media"),
                }
            )

        if careers_data:
            careers_df = pd.DataFrame(careers_data)
            st.dataframe(
                careers_df,
                use_container_width=True,
                column_config={
                    "Carrera": st.column_config.TextColumn("Carrera", width="large"),
                    "Duración": st.column_config.NumberColumn(
                        "Duración (años)", format="%d"
                    ),
                    "Estudiantes": st.column_config.NumberColumn("Estudiantes"),
                    "Promedio": st.column_config.NumberColumn(
                        "Promedio", format="%.1f"
                    ),
                    "Demanda": st.column_config.TextColumn("Demanda"),
                },
            )

    @staticmethod
    def render_performance_section(faculty):
        """Render academic performance data for the faculty"""
        st.header("📈 Rendimiento Académico")

        # Load faculty-specific data if available
        data = DataManager.load_data()

        if (
            not data["semester_ratings"].empty
            and faculty in data["semester_ratings"]["Facultad"].values
        ):
            faculty_data = data["semester_ratings"][
                data["semester_ratings"]["Facultad"] == faculty
            ]

            if not faculty_data.empty:
                # Faculty rating metrics
                col1, col2, col3 = st.columns(3)

                with col1:
                    avg_rating = faculty_data.iloc[:, 1:].mean(axis=1).values[0]
                    st.metric("Calificación General", f"{avg_rating:.1f}/10")

                with col2:
                    # Calculate trend (simulated)
                    trend = np.random.uniform(-0.5, 0.5)
                    st.metric(
                        "Tendencia", f"{trend:+.1f}", delta=f"{trend:+.1f} puntos"
                    )

                with col3:
                    rank = np.random.randint(1, 20)
                    st.metric("Ranking Facultades", f"#{rank}/19")

                # Detailed ratings chart
                st.subheader("Calificaciones por Categoría")

                ratings = faculty_data.iloc[:, 1:].T
                ratings.columns = ["Calificación"]

                # FIXED: Use rating_hist instead of create_rating_barplot
                fig, ax = plots.rating_hist(ratings["Calificación"])
                st.pyplot(fig)

        # Additional performance metrics
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            # Student distribution by year
            st.subheader("Distribución por Año")
            years_data = {
                "Primer año": np.random.randint(80, 120),
                "Segundo año": np.random.randint(70, 110),
                "Tercer año": np.random.randint(60, 100),
                "Cuarto año": np.random.randint(50, 90),
                "Quinto año": np.random.randint(40, 80),
            }

            fig, ax = plt.subplots()
            ax.pie(years_data.values(), labels=years_data.keys(), autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)

        with col2:
            # Grade distribution
            st.subheader("Distribución de Notas")
            grades_data = {
                "2": np.random.randint(5, 15),
                "3": np.random.randint(20, 40),
                "4": np.random.randint(30, 50),
                "5": np.random.randint(10, 20),
            }

            fig, ax = plt.subplots()
            bars = ax.bar(
                grades_data.keys(),
                grades_data.values(),
                color=["#e74c3c", "#f39c12", "#3498db", "#27ae60"],
            )
            ax.set_xlabel("Nota")
            ax.set_ylabel("Cantidad de Estudiantes")

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 0.1,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                )

            st.pyplot(fig)
        # Additional performance metrics
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            # Student distribution by year
            st.subheader("Distribución por Año")
            years_data = {
                "Primer año": np.random.randint(80, 120),
                "Segundo año": np.random.randint(70, 110),
                "Tercer año": np.random.randint(60, 100),
                "Cuarto año": np.random.randint(50, 90),
                "Quinto año": np.random.randint(40, 80),
            }

            fig, ax = plt.subplots()
            ax.pie(years_data.values(), labels=years_data.keys(), autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)

        with col2:
            # Grade distribution
            st.subheader("Distribución de Notas")
            grades_data = {
                "2": np.random.randint(5, 15),
                "3": np.random.randint(20, 40),
                "4": np.random.randint(30, 50),
                "5": np.random.randint(10, 20),
            }

            fig, ax = plt.subplots()
            bars = ax.bar(
                grades_data.keys(),
                grades_data.values(),
                color=["#e74c3c", "#f39c12", "#3498db", "#27ae60"],
            )
            ax.set_xlabel("Nota")
            ax.set_ylabel("Cantidad de Estudiantes")

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 0.1,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                )

            st.pyplot(fig)

    @staticmethod
    def get_founding_year(faculty):
        """Get founding year for a faculty"""
        founding_years = {
            "MATCOM": "1976",
            "FF": "1962",
            "FQ": "1963",
            "FBIOM": "1964",
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
            "FBIOM": "Dr. Pedro Pablo García",
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
            "FBIOM": "450",
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
            "Egresados/año": str(np.random.randint(50, 150)),
            "Laboratorios": str(np.random.randint(5, 20)),
            "Proyectos de investigación": str(np.random.randint(10, 50)),
        }

    @staticmethod
    def get_career_info(faculty, career):
        """Get detailed information about a specific career"""
        # This would ideally come from a database
        # For now, return simulated data

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
            "Arquitectura": 6,
            "Ingeniería Civil": 6,
            "Ingeniería Hidráulica": 6,
        }

        descriptions = {
            "Matemática": "Formación sólida en matemáticas puras y aplicadas, preparando para investigación y aplicación en diversas áreas científicas y tecnológicas.",
            "Ciencias de la Computación": "Formación en fundamentos teóricos y prácticos de la computación, algoritmos, sistemas y desarrollo de software.",
            "Ciencia de Datos": "Formación interdisciplinaria en matemáticas, estadística y computación para extraer conocimiento de datos complejos.",
            "Licenciatura en Física": "Formación en leyes fundamentales de la naturaleza, métodos experimentales y aplicaciones tecnológicas.",
            "Ingeniería Física": "Aplicación de principios físicos al diseño y desarrollo de tecnologías y sistemas innovadores.",
            "Licenciatura en Química": "Estudio de la composición, propiedades y transformaciones de la materia, con aplicaciones industriales y ambientales.",
        }

        # Default description if not found
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
            "coordinator": f"Dr./Dra. {np.random.choice(['González', 'Rodríguez', 'Pérez', 'Martínez', 'García'])}",
        }

    @staticmethod
    def get_career_stats(faculty, career):
        """Get statistics for a specific career"""
        return {
            "Estudiantes": str(np.random.randint(50, 300)),
            "Promedio": f"{np.random.uniform(3.5, 4.5):.1f}",
            "Tasa graduación": f"{np.random.randint(75, 95)}%",
            "Demanda": np.random.choice(["Alta", "Media", "Baja"]),
            "Empleabilidad": f"{np.random.randint(80, 98)}%",
        }

    @staticmethod
    def get_career_subjects(faculty, career):
        """Get main subjects for a career"""
        subjects_by_career = {
            "Matemática": [
                "Análisis Matemático",
                "Álgebra",
                "Geometría",
                "Topología",
                "Ecuaciones Diferenciales",
                "Análisis Numérico",
            ],
            "Ciencias de la Computación": [
                "Algoritmos",
                "Estructuras de Datos",
                "Bases de Datos",
                "Inteligencia Artificial",
                "Sistemas Operativos",
                "Redes",
            ],
            "Ciencia de Datos": [
                "Estadística",
                "Machine Learning",
                "Visualización de Datos",
                "Big Data",
                "Minería de Datos",
                "Procesamiento de Lenguaje Natural",
            ],
            "Licenciatura en Física": [
                "Mecánica Clásica",
                "Electromagnetismo",
                "Termodinámica",
                "Mecánica Cuántica",
                "Física Estadística",
                "Óptica",
            ],
            "Ingeniería Física": [
                "Mecánica de Sólidos",
                "Electrónica",
                "Materiales",
                "Instrumentación",
                "Control Automático",
                "Energías Renovables",
            ],
            "Licenciatura en Química": [
                "Química General",
                "Química Orgánica",
                "Química Inorgánica",
                "Fisicoquímica",
                "Química Analítica",
                "Bioquímica",
            ],
            "Derecho": [
                "Derecho Civil",
                "Derecho Penal",
                "Derecho Constitucional",
                "Derecho Administrativo",
                "Derecho Internacional",
                "Teoría del Estado",
            ],
            "Psicología": [
                "Psicología General",
                "Psicología del Desarrollo",
                "Psicopatología",
                "Psicometría",
                "Neuropsicología",
                "Psicoterapia",
            ],
        }

        default_subjects = [
            "Fundamentos de la Carrera",
            "Metodología de la Investigación",
            "Taller de Integración",
            "Práctica Profesional",
            "Trabajo de Diploma",
        ]

        return subjects_by_career.get(career, default_subjects)

    @staticmethod
    def get_graduate_profile(faculty, career):
        """Get graduate profile points for a career"""
        profiles = {
            "Matemática": [
                "Capacidad para modelar y resolver problemas matemáticos complejos",
                "Habilidades en análisis matemático y razonamiento lógico",
                "Competencia en métodos matemáticos aplicados a diversas áreas",
                "Capacidad para la investigación matemática pura y aplicada",
                "Habilidades para la docencia y transferencia de conocimiento",
            ],
            "Ciencias de la Computación": [
                "Desarrollo de software robusto y escalable",
                "Diseño y análisis de algoritmos eficientes",
                "Administración de sistemas computacionales y redes",
                "Implementación de bases de datos seguras y eficientes",
                "Gestión de proyectos de desarrollo tecnológico",
            ],
            "Ciencia de Datos": [
                "Extracción de insights valiosos de datos complejos",
                "Implementación de modelos de machine learning",
                "Visualización efectiva de información",
                "Gestión de proyectos de análisis de datos",
                "Comunicación de resultados técnicos a diferentes audiencias",
            ],
            "Licenciatura en Física": [
                "Comprensión profunda de leyes físicas fundamentales",
                "Habilidades experimentales y de laboratorio",
                "Modelación matemática de fenómenos físicos",
                "Capacidad para investigación científica",
                "Aplicación de principios físicos en soluciones tecnológicas",
            ],
        }

        default_profile = [
            "Formación integral en los fundamentos de la disciplina",
            "Capacidad para investigación científica y aplicada",
            "Habilidades para el trabajo en equipo multidisciplinario",
            "Competencia para la resolución de problemas complejos",
            "Compromiso ético y responsabilidad social profesional",
        ]

        return profiles.get(career, default_profile)


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
