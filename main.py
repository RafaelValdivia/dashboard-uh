import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plots import *


st.title("Semestre UH 25")

tabs = st.tabs(["Calificación", "Facultad",
                "Carrera", "Asignatura", "Profesor"])

with tabs[0]:
    st.header("Calificación del Semestre 25")
    col1, col2 = st.columns([0.75,1])
    with st.expander("Calificación por facultad"):
        st.pyplot(avrg_hist(fac_avrg)[0])
    with col1:
        st.pyplot(rtng_pie("SEMESTER")[0])
    with col2:
        st.pyplot(rtng_hist ("SEMESTER")[0])
    st.divider()
    st.header("imagenes_facultades")
    st.divider()
    st.subheader("Comentarios de los estudiantes")
    st.divider()
    st.subheader("Histograma de notas del semestre")
    st.pyplot(mark_hist({"2": 64, "3": 203, "4": 34, "5": 18},
              ["#b00", "#bb0", "#0b0", "#0fb"])[0]
              )

with tabs[1]:
    faculty = "MATCOM"
    st.header(faculty)
    col1, col2 = st.columns([0.75, 1])
    st.divider()
    st.header(f"Calificación del semestre de {faculty}")
    col3, col4 = st.columns([0.75, 1])
    with col1: 
        st.image("../html/images/matcom.png")
    with col2:
        st.text("""Facultad de Matemática y Computación. Fundada en el año de la corneta por un tipo que no conozco. Al principio tenia una sola carrera (Matemática) pero con el avance de la tecnología y la computación en el siglo XX se añadió la carrera de Ciencias de la Computación. Más recientemente se fundó la carrera de Ciencias de Datos por Yudivian "La Amenaza", Fiad y Fuilan. (Aqui es donde va la descripcion de la facultad)
                """)
    with col3:
        st.pyplot(rtng_pie(faculty)[0])
    with col4:
        st.pyplot(rtng_hist(faculty)[0])
    st.divider()
    st.header("Carreras:")
    st.markdown("## [Matematica](www.google.com)")
    st.markdown("## [Ciencias de la Computación](www.google.com)")
    st.markdown("## [Ciencias de Datos](www.google.com)")
    st.divider()
    colors=["#0a0","#a0a", "#09b"]
    st.header("Matrícula")
    st.pyplot(matr_pie(matr_MATCOM, colors)[0])
    st.subheader("Rendimiento Académico")
    st.pyplot(mark_hist(notas_MATCOM,colors)[0])

with tabs[2]:
    def gen_class(n:int, col1, col2) -> None:
        with col1:
            for i in range(n,8+n,2):
                st.markdown(f"## [Asignatura {i}](google.com)")
        with col2:
            for i in range(1+n,9+n,2):
                st.markdown(f"## [Asignatura {i}](google.com)")
    st.markdown("# Ciencias de Datos")
    for year in range(1,6):
        st.header(f"Año {year}")
        col1, col2 = st.columns([1,1])
        gen_class(1, col1, col2)
        st.divider()

