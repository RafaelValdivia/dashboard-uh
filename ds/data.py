import numpy as np
import pandas as pd

# Constants for the application
SEMESTER_CATEGORIES = [
    "Respeto a los horarios",
    "Disponibilidad de aulas",
    "Facilidad para el E.I.",
    "Bibliografía/Internet",
    "Carga de trabajo",
    "Ocio",
]

SUBJECT_CATEGORIES = [
    "Calidad del profesor",
    "Recursos didácticos",
    "Carga de trabajo",
    "Justicia en la evaluación",
    "Utilidad de los contenidos impartidos",
]

FACULTIES = [
    "CONFIN",
    "EKO",
    "FTUR",
    "FBIOM",
    "INSTEC",
    "GEO",
    "IFAL",
    "MATCOM",
    "FF",
    "FQ",
    "FAYL",
    "FCOM",
    "LEX",
    "FHS",
    "ISDI",
    "FLEX",
    "PSICO",
    "CSGH",
    "FENHI",
]

DATA_SCIENCE_CLASSES = [
    ("Filosofía", 1, 1),
    ("Análisis Matemático I", 1, 1),
    ("Álgebra Lineal", 1, 1),
    ("Introducción a la Programación", 1, 1),
    ("Lógica", 1, 1),
    ("Introducción a la Ciencia de Datos", 1, 1),
    ("Educación Física", 1, 1),
    ("Historia de Cuba", 2, 1),
    ("Análisis Matemático II", 2, 1),
    ("Matemática Numérica", 2, 1),
    ("Análisis Exploratoria de Datos", 2, 1),
    ("Programación", 2, 1),
    ("Comunicación en Ciencia de Datos", 2, 1),
    ("Educación Física II", 2, 1),
    ("Práctica Profesional", 2, 1),
    ("Economía Política", 3, 2),
    ("Matemática y Aplicaciones", 3, 2),
    ("Probabilidades", 3, 2),
    ("Bases de Datos", 3, 2),
    ("Estructura de Datos", 3, 2),
    ("Visualización de Datos", 3, 2),
    ("Educación Física III", 3, 2),
    ("Análisis Estadístico I", 4, 2),
    ("Modelos de Optimización", 4, 2),
    ("Complejidad Computacional", 4, 2),
    ("Sistemas Computacionales y Redes", 4, 2),
    ("Aprendizaje Automático", 4, 2),
    ("Análisis de Redes Complejas", 4, 2),
    ("Educación Física", 4, 2),
    ("Práctica Profesional II", 4, 2),
    ("Teoría Política", 5, 3),
    ("Análisis Estadístico II", 5, 3),
    ("Muestreo y Diseño de Experimentos", 5, 3),
    ("Redes Neuronales", 5, 3),
    ("Procesamientos de Lenguaje", 5, 3),
    ("Procesamiento de Grandes Volumenes de Datos", 5, 3),
    ("Procesos Estocásticos y Series de Tiempo", 6, 3),
    ("Sistemas de Recuperación de Información", 6, 3),
    ("Simulación", 6, 3),
    ("Ingeniería de Datos", 6, 3),
    ("Procesamiento de Imágenes", 6, 3),
    ("Curso Optativo I", 6, 3),
    ("Práctica Profesional III", 6, 3),
    ("Estudias de Ciencia, Tecnología y Sociedad", 7, 4),
    ("Seguridad Nacional", 7, 4),
    ("Defensa Nacional", 7, 4),
    ("Inteligencia de Negocios", 7, 4),
    ("Elementos de Inteligencia Artificial", 7, 4),
    ("Ciberseguridad y Privacidad", 7, 4),
    ("Curso Optativo II", 7, 4),
    ("Metodología de la Investigación", 8, 4),
    ("Curso Electivo", 8, 4),
    ("Culminación de Estudios", 8, 4),
]

MATCOM_ENROLLMENT = {
    "M1": 26,
    "M2": 14,
    "M3": 12,
    "M4": 8,
    "D1": 46,
    "D2": 4,
    "D3": 5,
    "D4": 5,
    "C1": 143,
    "C2": 85,
    "C3": 60,
    "C4": 55,
}


def generate_student_ids():
    """Generate all student IDs for MATCOM"""
    return [
        (brigade, idE)
        for brigade in MATCOM_ENROLLMENT
        for idE in range(1, MATCOM_ENROLLMENT[brigade] + 1)
    ]


def generate_semester_ratings():
    """Generate semester ratings for all faculties"""
    np.random.seed(42)

    # Generate random ratings for all faculties
    semester_ratings = {}
    for faculty in FACULTIES:
        semester_ratings[faculty] = {
            category: round(np.random.uniform(3, 10), 1)
            for category in SEMESTER_CATEGORIES
        }

    # Calculate MATCOM ratings based on individual students
    student_ids = generate_student_ids()
    student_ratings = {
        student_id: {
            category: np.random.randint(3, 11) for category in SEMESTER_CATEGORIES
        }
        for student_id in student_ids
    }

    # Calculate MATCOM average
    semester_ratings["MATCOM"] = {
        category: round(
            sum(student_ratings[student_id][category] for student_id in student_ids)
            / len(student_ids),
            1,
        )
        for category in SEMESTER_CATEGORIES
    }

    return semester_ratings, student_ratings


def create_dataframes():
    """Create and save all dataframes to CSV files"""
    semester_ratings, student_ratings = generate_semester_ratings()

    # Create semester ratings dataframe
    sem_df_data = {"Facultad": []}
    for category in SEMESTER_CATEGORIES:
        sem_df_data[category] = []

    for faculty in FACULTIES:
        sem_df_data["Facultad"].append(faculty)
        for category in SEMESTER_CATEGORIES:
            sem_df_data[category].append(semester_ratings[faculty][category])

    # Add general average
    sem_df_data["Facultad"].append("GENERAL")
    for category in SEMESTER_CATEGORIES:
        values = sem_df_data[category]
        sem_df_data[category].append(round(sum(values) / len(values), 1))

    semester_df = pd.DataFrame(sem_df_data)

    # Create MATCOM student ratings dataframe
    matcom_df_data = {"Brigada": [], "ID": []}
    for category in SEMESTER_CATEGORIES:
        matcom_df_data[category] = []

    student_ids = generate_student_ids()
    for brigade, student_id in student_ids:
        matcom_df_data["Brigada"].append(brigade)
        matcom_df_data["ID"].append(student_id)
        for category in SEMESTER_CATEGORIES:
            matcom_df_data[category].append(
                student_ratings[(brigade, student_id)][category]
            )

    matcom_ratings_df = pd.DataFrame(matcom_df_data)

    # Create subject ratings dataframe
    subject_ratings_df = pd.DataFrame(
        {
            "Categoria": SUBJECT_CATEGORIES,
            "Calificacion": np.round(
                np.random.uniform(6, 10, len(SUBJECT_CATEGORIES)), 1
            ),
        }
    )

    # Create classes dataframe
    classes_data = []
    for subject_name, semester, year in DATA_SCIENCE_CLASSES:
        if semester % 2 == 1:  # Only even semesters
            continue

        for brigade, student_id in student_ids:
            # Generate realistic grades
            if brigade[0] == "D" and int(brigade[1]) == year:
                grade = np.random.choice([2, 3, 4, 5], p=[0.1, 0.4, 0.4, 0.1])
            else:
                grade = None

            classes_data.append(
                {
                    "Brigada": brigade,
                    "ID": student_id,
                    "Asignatura": subject_name,
                    "Año": year,
                    "Nota": grade,
                }
            )

    classes_df = pd.DataFrame(classes_data)

    # Save to CSV
    semester_df.to_csv("Semester_Rating.csv", index=False)
    matcom_ratings_df.to_csv("MATCOM_Rating.csv", index=False)
    subject_ratings_df.to_csv("VD_Rating.csv", index=False)
    classes_df.to_csv("MATCOM_Classes.csv", index=False)

    print("✅ Datos generados exitosamente en archivos CSV")
    return semester_df, matcom_ratings_df, subject_ratings_df, classes_df


if __name__ == "__main__":
    create_dataframes()
