import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plots import *
import os

st.title("Semestre UH 25")
# cambiar nombre semestre

tabs = st.tabs(["Calificación", "Facultad",
                "Carrera", "Asignatura"])

with tabs[0]:
    st.header("Calificación del Semestre 25")
    col1, col2 = st.columns([0.75,1])
    with col1:
        st.pyplot(rtng_pie(sem_rtng)[0])
    with col2:
        st.pyplot(rtng_hist (sem_data)[0])
    with st.expander("Calificación por facultad"):
        st.pyplot(avrg_hist(fac_avrg)[0])
    st.divider()
    cols = st.columns([1,1])
    j = 0
    for i in os.listdir("images"):
        try:
            with cols[j%2]:
                st.image(f"images/{i}", width=300 )
            j+=1
        except Exception as e:
            pass
    st.subheader("Histograma de notas del semestre")
    mark_colors = ["#b00", "#bb0", "#0b0", "#0fb"]
    st.pyplot(mark_hist({"2": 64, "3": 203, "4": 34, "5": 18},
             mark_colors)[0]
              )
    st.divider()
    st.subheader("Comentarios de los estudiantes")
    st.image("comments.jpg", width=900)
    st.divider()

with tabs[1]:
    faculty = "MATCOM"
    st.header(faculty)
    col1, col2 = st.columns([0.75, 1])
    st.divider()
    st.header(f"Calificación del semestre de {faculty}")
    col3, col4 = st.columns([0.75, 1])
    with col1: 
        st.image("images/matcom.png")
    with col2:
        st.text("""Facultad de Matemática y Computación. Fundada en el año de la corneta por un tipo que no conozco. Al principio tenia una sola carrera (Matemática) pero con el avance de la tecnología y la computación en el siglo XX se añadió la carrera de Ciencias de la Computación. Más recientemente se fundó la carrera de Ciencias de Datos por Yudivian "La Amenaza", Fiad y Fuilan. (Aqui es donde va la descripcion de la facultad)
                """)
    with col3:
        st.pyplot(rtng_pie(fac_avrg[faculty])[0])
    with col4:
        st.pyplot(rtng_hist(fac_data[faculty])[0])
    st.divider()
    st.header("Carreras:")
    st.markdown("## [Matematica](www.google.com)")
    st.markdown("## [Ciencias de la Computación](www.google.com)")
    st.markdown("## [Ciencias de Datos](www.google.com)")
    st.divider()
    colors=["#0a0","#a0a", "#09b", "#f92"]
    st.header("Matrícula")
    st.pyplot(matr_pie(matr_MATCOM, colors[:-1])[0])
    st.header("Rendimiento Académico")
    st.markdown("### Promedio: 3.5")
    st.pyplot(mark_hist(notas_MATCOM,colors[:-1])[0])
    st.header("Frecuencia absoluta de las notas")
    st.pyplot(mark_hist({
        "2": 67, "3": 105, "4": 32, "5": 6
        }, mark_colors)[0]
              )

with tabs[2]:
    st.markdown("# Ciencias de Datos")
    st.subheader("Matrícula:")
    st.pyplot(matr_pie(matr_CD, colors)[0])
    col1, col2 = st.columns([1,1])
    with col1: 
        pass
    def gen_class(n:int, col1, col2) -> None:
        with col1:
            for i in range(n,8+n,2):
                st.markdown(f"## [Asignatura {i}](google.com)")
        with col2:
            for i in range(1+n,9+n,2):
                st.markdown(f"## [Asignatura {i}](google.com)")
    st.header("Rendimiento Académico")
    st.markdown("### Promedio: 3.9")
    st.pyplot(mark_hist({
        "Primer Año": 2.8,
        "Segundo Año": 3.4,
        "Tercer Año": 3.8,
        "Cuarto Año": 3.9
        },colors[:])[0])
    st.header("Frecuencia absoluta de las notas")
    st.pyplot(mark_hist({
        "2": 18, "3": 42, "4": 12, "5": 3
        }, mark_colors)[0]
              )
    for year in range(1,5):
        st.header(f"Año {year}")
        col1, col2 = st.columns([1,1])
        gen_class(1, col1, col2)
        st.divider()

with tabs[3]:
    st.header("Visualización de Datos")
    st.text("Descripcion de la asignatura "*10)
    col1, col2 = st.columns([0.75, 1])
    vd_rtng = sum(asig_VD.values())/len(asig_VD)
    with col1:
        st.pyplot(rtng_pie(vd_rtng)[0])
    with col2:
        st.pyplot(rtng_hist(asig_VD)[0])
    st.subheader("Rendimiento Académico")
    st.markdown("### Promedio: 3.9")
    st.pyplot(mark_hist(vd_notas, mark_colors)[0])
