# Updated data.py - generating 300 students per faculty
from datetime import datetime

import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Current semester
CURRENT_SEMESTER = "2025-2"

# Categorías a través de las cuales se califica el semestre
SEMESTER_CATEGORIES = [
    "Respeto a los horarios",
    "Disponibilidad de aulas",
    "Facilidad para el E.I.",
    "Bibliografía/Internet",
    "Carga de trabajo",
    "Ocio",
]

# Categorías para calificar una asignatura
SUBJECT_CATEGORIES = [
    "Calidad del profesor",
    "Recursos didácticos",
    "Carga de trabajo",
    "Justicia en la evaluación",
    "Utilidad de los contenidos impartidos",
]

# Lista de todas las facultades con número de carreras estimadas
FACULTIES_INFO = {
    "MATCOM": {"name": "Matemática y Computación", "careers": 3, "students": 320},
    "FF": {"name": "Física", "careers": 2, "students": 280},
    "FQ": {"name": "Química", "careers": 1, "students": 310},
    "FBIOM": {"name": "Biología", "careers": 3, "students": 295},
    "FHS": {"name": "Historia y Sociología", "careers": 3, "students": 270},
    "INSTEC": {"name": "Tecnologías Aplicadas", "careers": 3, "students": 260},
    "FTUR": {"name": "Turismo", "careers": 1, "students": 240},
    "FCOM": {"name": "Comunicación", "careers": 2, "students": 230},
    "LEX": {"name": "Derecho", "careers": 1, "students": 350},
    "PSICO": {"name": "Psicología", "careers": 1, "students": 320},
    "FAYL": {"name": "Artes y Letras", "careers": 2, "students": 250},
    "IFAL": {"name": "Farmacia y Alimentos", "careers": 2, "students": 265},
    "ISDI": {"name": "Diseño Industrial", "careers": 2, "students": 220},
    "CSGH": {"name": "Gestión Habana", "careers": 1, "students": 210},
    "FENHI": {"name": "Economía", "careers": 2, "students": 290},
    "CONFIN": {"name": "Contabilidad y Finanzas", "careers": 1, "students": 275},
    "EKO": {"name": "Economía", "careers": 1, "students": 240},
    "GEO": {"name": "Geografía", "careers": 1, "students": 190},
    "FLEX": {"name": "Lenguas Extranjeras", "careers": 1, "students": 235},
}

# Carreras por facultad
CAREERS_BY_FACULTY = {
    "MATCOM": ["Matemática", "Ciencias de la Computación", "Ciencia de Datos"],
    "FF": ["Licenciatura en Física", "Ingeniería Física"],
    "FQ": ["Licenciatura en Química"],
    "FBIOM": [
        "Licenciatura en Biología",
        "Licenciatura en Microbiología",
        "Bioquímica",
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
    "FAYL": ["Licenciatura en Letras", "Licenciatura en Historia del Arte"],
    "IFAL": ["Licenciatura en Farmacia", "Licenciatura en Ciencia de los Alimentos"],
    "ISDI": ["Diseño Industrial", "Diseño de Comunicación Visual"],
    "CSGH": ["Preservación y Gestión del Patrimonio Cultural"],
    "FENHI": ["Licenciatura en Economía", "Licenciatura en Administración de Empresas"],
    "CONFIN": ["Licenciatura en Contabilidad y Finanzas"],
    "EKO": ["Licenciatura en Economía"],
    "GEO": ["Licenciatura en Geografía"],
    "FLEX": ["Licenciatura en Lenguas Extranjeras"],
}


def generate_semester_ratings():
    """Generate semester ratings for all faculties"""
    data = []

    for faculty, info in FACULTIES_INFO.items():
        row = {"Facultad": faculty}

        # Generate realistic ratings (between 5.0 and 8.5)
        for category in SEMESTER_CATEGORIES:
            # Each faculty has different strengths
            base_rating = np.random.uniform(5.0, 7.5)
            variation = np.random.uniform(-0.5, 0.5)
            rating = round(base_rating + variation, 1)
            row[category] = min(max(rating, 1.0), 10.0)

        data.append(row)

    # Add GENERAL average
    df = pd.DataFrame(data)
    general_row = {"Facultad": "GENERAL"}

    for category in SEMESTER_CATEGORIES:
        general_row[category] = round(df[category].mean(), 1)

    df = pd.concat([df, pd.DataFrame([general_row])], ignore_index=True)

    return df


def generate_student_ratings():
    """Generate student-level ratings for all faculties (approx 300 per faculty)"""
    all_students = []

    for faculty, info in FACULTIES_INFO.items():
        num_students = info["students"]
        careers = CAREERS_BY_FACULTY.get(faculty, ["Carrera Principal"])

        # Distribute students among careers
        students_per_career = num_students // len(careers)
        remainder = num_students % len(careers)

        for i, career in enumerate(careers):
            career_students = students_per_career + (1 if i < remainder else 0)

            for student_id in range(1, career_students + 1):
                student = {
                    "Facultad": faculty,
                    "Carrera": career,
                    "ID_Estudiante": f"{faculty}-{career[:3].upper()}-{student_id:04d}",
                    "Brigada": f"{faculty[:2]}{np.random.randint(1, 10)}",
                    "Semestre": CURRENT_SEMESTER,
                }

                # Generate individual ratings (more variation than faculty average)
                for category in SEMESTER_CATEGORIES:
                    # Student ratings vary more
                    base = np.random.uniform(4.0, 9.0)
                    rating = int(round(base, 0))
                    student[category] = min(max(rating, 1), 10)

                all_students.append(student)

    return pd.DataFrame(all_students)


def generate_classes_data():
    """Generate class enrollment and grade data"""
    all_classes = []

    # Common courses across all faculties
    common_courses = [
        "Idioma Inglés",
        "Educación Física",
        "Historia de Cuba",
        "Filosofía",
        "Metodología de la Investigación",
    ]

    # Faculty-specific courses
    faculty_courses = {
        "MATCOM": [
            "Cálculo",
            "Álgebra",
            "Programación",
            "Bases de Datos",
            "Estadística",
        ],
        "FF": [
            "Mecánica Clásica",
            "Electromagnetismo",
            "Termodinámica",
            "Física Moderna",
        ],
        "FQ": [
            "Química General",
            "Química Orgánica",
            "Química Inorgánica",
            "Fisicoquímica",
        ],
        "LEX": [
            "Derecho Civil",
            "Derecho Penal",
            "Derecho Constitucional",
            "Derecho Laboral",
        ],
        "PSICO": ["Psicología General", "Psicología del Desarrollo", "Psicopatología"],
    }

    student_ratings = generate_student_ratings()

    for _, student in student_ratings.iterrows():
        faculty = student["Facultad"]
        career = student["Carrera"]

        # Take 5-7 courses per student
        num_courses = np.random.randint(5, 8)

        # Select courses (mix of common and faculty-specific)
        courses = []
        if faculty in faculty_courses:
            # Take 2-3 faculty-specific courses
            spec_courses = np.random.choice(
                faculty_courses[faculty],
                min(3, len(faculty_courses[faculty])),
                replace=False,
            )
            courses.extend(spec_courses)

        # Fill remaining with common courses
        remaining = num_courses - len(courses)
        if remaining > 0:
            common_selected = np.random.choice(
                common_courses, min(remaining, len(common_courses)), replace=False
            )
            courses.extend(common_selected)

        # Create class records
        for course in courses:
            # Generate grade (with realistic distribution)
            rand = np.random.random()
            if rand < 0.1:  # 10% fail
                grade = 2
            elif rand < 0.4:  # 30% 3
                grade = 3
            elif rand < 0.8:  # 40% 4
                grade = 4
            else:  # 20% 5
                grade = 5

            class_record = {
                "Facultad": faculty,
                "Carrera": career,
                "ID_Estudiante": student["ID_Estudiante"],
                "Asignatura": course,
                "Semestre": CURRENT_SEMESTER,
                "Nota": grade,
                "Créditos": np.random.choice([2, 3, 4]),
                "Profesor": f"Prof. {np.random.choice(['González', 'Rodríguez', 'Pérez', 'Martínez', 'García'])}",
            }

            all_classes.append(class_record)

    return pd.DataFrame(all_classes)


def generate_subject_ratings():
    """Generate ratings for specific subjects"""
    courses = [
        "Visualización de Datos",
        "Programación I",
        "Cálculo I",
        "Química General",
        "Derecho Civil",
        "Psicología General",
        "Historia de Cuba",
        "Inglés I",
        "Educación Física",
    ]

    data = []
    for course in courses:
        for category in SUBJECT_CATEGORIES:
            rating = round(np.random.uniform(6.0, 9.0), 1)
            data.append(
                {
                    "Asignatura": course,
                    "Categoria": category,
                    "Calificacion": rating,
                    "Semestre": CURRENT_SEMESTER,
                }
            )

    return pd.DataFrame(data)


def generate_all_data():
    """Generate all data files"""
    print("Generando datos para el semestre:", CURRENT_SEMESTER)

    # Generate data
    semester_ratings = generate_semester_ratings()
    student_ratings = generate_student_ratings()
    classes_data = generate_classes_data()
    subject_ratings = generate_subject_ratings()

    # Save to CSV
    semester_ratings.to_csv("Semester_Rating.csv", index=False)
    student_ratings.to_csv("Student_Ratings.csv", index=False)
    classes_data.to_csv("Classes_Data.csv", index=False)
    subject_ratings.to_csv("Subject_Ratings.csv", index=False)

    print(f"✅ Datos generados exitosamente:")
    print(f"   - {len(semester_ratings) - 1} facultades")
    print(f"   - {len(student_ratings)} estudiantes total")
    print(f"   - {len(classes_data)} registros de clases")
    print(f"   - {len(subject_ratings)} calificaciones de asignaturas")

    # Calculate average students per faculty
    avg_students = len(student_ratings) / (len(semester_ratings) - 1)
    print(f"   - Promedio: {avg_students:.0f} estudiantes por facultad")

    return semester_ratings, student_ratings, classes_data, subject_ratings


if __name__ == "__main__":
    generate_all_data()
