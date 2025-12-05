import pandas as pd
from random import uniform as rand

sem_cat = [
 "Respeto a los horarios",
 "Disponibilidad de aulas",
 "Facilidad para el E.I.",
 "Bibliografía/Internet",
 "Carga de trabajo",
 "Ocio"
 ]
faculties = [
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
        "FENHI"
        ]

fac_data = dict.fromkeys(faculties, 0)
fac_avrg = dict.fromkeys(faculties, 0) 
sem_data = dict.fromkeys(sem_cat[::-1], 0)
sem_rtng = 0.
for faculty in fac_data:
    fac_data[faculty] = dict.fromkeys(sem_cat, 0)
    for category in sem_cat:
        value = rand(2,10)
        fac_data[faculty][category] = value
        fac_avrg[faculty] += value/len(sem_cat)
        sem_data[category] += value/len(faculties)
        sem_rtng += value/(len(faculties)*len(sem_cat))

matr_MATCOM = {
        "Ciencias de la\nComputación": 102,
        "Ciencias\nde Datos": 50,
        "Matemática": 33
        }

matr_CD = {
           "Primer Año": 40,
           "Segundo Año": 4,
           "Tercer Año": 5,
           "Cuarto Año":4
           }
notas_MATCOM = {
        "Ciencias\nde la Computación":3.4,
        "Ciencias\nde Datos": 3.6,
        "Matemática":3.82,
        }
asig_VD = {
        "Calidad del profesor": 10.,
        "Recursos didácticos": 7.9,
        "Carga de trabajo": 6.5,
        "Justicia en la evaluación": 8.4,
        "Utilidad de los contenidos impartidos": 9.3
        }

vd_notas = {
        "2": 0, "3": 1, "4": 3, "5": 0
        }
