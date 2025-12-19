import numpy as np
import pandas as pd

# ... (previous constants: SEMESTER_CATEGORIES, SUBJECT_CATEGORIES, FACULTIES, etc.) ...

# Mapping of faculty acronyms to their official Spanish names
FACULTY_NAMES = {
    "CONFIN": "Facultad de Contabilidad y Finanzas",
    "EKO": "Facultad de Economía",
    "FTUR": "Facultad de Turismo",
    "FBIOM": "Facultad de Biología",
    "FF": "Facultad de Física",
    "GEO": "Facultad de Geografía",
    "IFAL": "Instituto de Farmacia y Alimentos",
    "MATCOM": "Facultad de Matemática y Computación",
    "FQ": "Facultad de Química",
    "FAYL": "Facultad de Artes y Letras",
    "FCOM": "Facultad de Comunicación",
    "LEX": "Facultad de Derecho",
    "FHS": "Facultad de Filosofía e Historia",
    "ISDI": "Instituto Superior de Diseño",
    "FLEX": "Facultad de Lenguas Extranjeras",
    "PSICO": "Facultad de Psicología",
    "CSGH": "Colegio de San Gerónimo de La Habana",
    "INSTEC": "Instituto Superior de Tecnologías y Ciencias Aplicadas",
}

# Official careers for each faculty (sourced from UH website)
FACULTY_CAREERS = {
    "CONFIN": ["Licenciatura en Contabilidad y Finanzas"],
    "EKO": ["Licenciatura en Economía"],
    "FTUR": ["Licenciatura en Turismo"],
    "FBIOM": [
        "Licenciatura en Biología",
        "Licenciatura en Microbiología",
        "Licenciatura en Bioquímica",
    ],
    "FF": ["Ingeniería Física", "Licenciatura en Física"],
    "GEO": ["Licenciatura en Geografía"],
    "IFAL": ["Farmacia", "Alimentos"],
    "MATCOM": ["Matemática", "Ciencias de la Computación", "Ciencia de Datos"],
    "FQ": ["Licenciatura en Química"],
    "FAYL": ["Letras", "Historia del Arte"],
    "FCOM": ["Comunicación Social"],
    "LEX": ["Derecho"],
    "FHS": ["Filosofía", "Historia"],
    "ISDI": ["Diseño Industrial", "Diseño de Comunicación Visual"],
    "FLEX": ["Lenguas Extranjeras"],
    "PSICO": ["Psicología"],
    "CSGH": ["Preservación y Gestión del Patrimonio Cultural"],
    "INSTEC": ["Ingeniería en Telecomunicaciones", "Ingeniería Eléctrica"],
}


def generate_career_ratings(faculty_ratings):
    """Generate simulated ratings for each career within a faculty."""
    career_ratings = {}
    for faculty, ratings in faculty_ratings.items():
        if faculty not in FACULTY_CAREERS:
            continue
        careers = FACULTY_CAREERS[faculty]
        for career in careers:
            # Add small variation to faculty base rating
            variation = np.random.uniform(-0.5, 0.5, len(SEMESTER_CATEGORIES))
            career_rating = {
                cat: max(1, min(10, round(ratings[cat] + var, 1)))
                for cat, var in zip(SEMESTER_CATEGORIES, variation)
            }
            career_ratings[(faculty, career)] = career_rating
    return career_ratings


def create_dataframes():
    """Create and save all dataframes to CSV files."""
    # ... (existing data generation logic) ...

    # Generate career-level ratings
    career_ratings = generate_career_ratings(semester_ratings)

    # Create career ratings dataframe
    career_data = []
    for (faculty, career), ratings in career_ratings.items():
        row = {"Facultad": faculty, "Carrera": career}
        row.update(ratings)
        career_data.append(row)

    career_ratings_df = pd.DataFrame(career_data)

    # Save to CSV
    career_ratings_df.to_csv("Career_Ratings.csv", index=False)
    # ... (save other dataframes as before) ...

    print("✅ Datos generados exitosamente (incluye datos por carrera)")
    return (
        semester_df,
        matcom_ratings_df,
        subject_ratings_df,
        classes_df,
        career_ratings_df,
    )


if __name__ == "__main__":
    create_dataframes()
