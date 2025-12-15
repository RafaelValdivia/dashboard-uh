from random import uniform as rand

import pandas as pd

# Categorias a traves de las cuales se califica el semestre
sem_cat: list[str] = [
    "Respeto a los horarios",
    "Disponibilidad de aulas",
    "Facilidad para el E.I.",
    "Bibliografía/Internet",
    "Carga de trabajo",
    "Ocio",
]

# Categorias para calificar una asignatura
asig_cat = {
    "Calidad del profesor",
    "Recursos didácticos",
    "Carga de trabajo",
    "Justicia en la evaluación",
    "Utilidad de los contenidos impartidos",
}

# Lista de todas las facultades
faculties: list[str] = [
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


# Asignaturas de la carrera de Ciencia de Datos
# Nombre, semestre, año
classes: list[tuple[str, int, int]] = [
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

# Matricula de todas las carreras de MATCOM
matricula: dict[str, int] = {
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

# ID de todos los estudiantes de MATCOM
ID_Estudiantes = [
    (brigada, idE) for brigada in matricula for idE in range(1, matricula[brigada] + 1)
]

MATCOM_Rtng = {
    idE: {cat: int(rand(3, 10)) for cat in sem_cat} for idE in ID_Estudiantes
}

# Calificacion del Semestre de todas las facultades
Sem_Rtng = {
    faculty: {cat: round(rand(3, 10), 1) for cat in sem_cat} for faculty in faculties
}

# Reemplazando el calculo de la calificacion del semestre de MATCOM
Sem_Rtng["MATCOM"] = {
    category: round(
        sum(MATCOM_Rtng[idE][category] for idE in ID_Estudiantes) / len(ID_Estudiantes),
        1,
    )
    for category in sem_cat
}
# Exportando todas los datos a csv
#
Sem_Rtng_df = {
    "Facultad": [],
}

MATCOM_Rtng_df = {
    "Brigada": [],
    "ID": [],
}

VD_Rating_df = {
    "Categoria": [key for key in asig_cat],
    "Calificacion": [0.0 for key in asig_cat],
}

for category in sem_cat:
    Sem_Rtng_df[category] = []
    MATCOM_Rtng_df[category] = []

for i in range(len(VD_Rating_df["Calificacion"])):
    VD_Rating_df["Calificacion"][i] = rand(6, 10)

# Calificacion deL semestre por facultad
for faculty in faculties:
    Sem_Rtng_df["Facultad"].append(faculty)
    for category in sem_cat:
        Sem_Rtng_df[category].append(Sem_Rtng[faculty][category])

for idE in ID_Estudiantes:
    MATCOM_Rtng_df["Brigada"].append(idE[0])
    MATCOM_Rtng_df["ID"].append(idE[1])
    for category in sem_cat:
        MATCOM_Rtng_df[category].append(MATCOM_Rtng[idE][category])

Sem_Rtng_df["Facultad"].append("GENERAL")
for category in sem_cat:
    Sem_Rtng_df[category].append(
        round(sum(Sem_Rtng_df[category]) / len(Sem_Rtng_df[category]), 1)
    )

# Calificacion del semestre de todos los estudiantes de MATCOM y sus notass
MATCOM_df = {
    "Brigada": [],
    "ID": [],
    "Asignatura": [],
    # "Semestre": [],
    "Año": [],
    "Nota": [],
}
for asignatura in classes:
    if asignatura[1] % 2 == 1:
        continue
    for idE in ID_Estudiantes:
        MATCOM_df["Brigada"].append(idE[0])
        MATCOM_df["ID"].append(idE[1])
        MATCOM_df["Asignatura"].append(asignatura[0])
        # MATCOM_df["Semestre"].append(asignatura[1])
        MATCOM_df["Año"].append(asignatura[2])
        MATCOM_df["Nota"].append(
            int(rand(2, 6))
            if idE[0][0] == "D" and int(idE[0][1]) == asignatura[2]
            else None
        )


Sem_Rtng_df = pd.DataFrame(Sem_Rtng_df).reset_index(drop=True)
MATCOM_Rtng_df = pd.DataFrame(MATCOM_Rtng_df).reset_index(drop=True)
MATCOM_df = pd.DataFrame(MATCOM_df).reset_index(drop=True)
VD_Rating_df = pd.DataFrame(VD_Rating_df).reset_index(drop=True)

Sem_Rtng_df.to_csv("Semester_Rating.csv", index=False)
MATCOM_Rtng_df.to_csv("MATCOM_Rating.csv", index=False)
MATCOM_df.to_csv("MATCOM_Classes.csv", index=False)
VD_Rating_df.to_csv("VD_Rating.csv", index=False)
# print("CALIFICACION DEL SEMESTRE POR FACULTAD")
# print(Sem_Rtng_df)
