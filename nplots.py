import pandas as pd
import matplotlib.pyplot as plt
from data import *

color_dict: dict[float, str] = {
        0.0: "#bb0000ff",
        2.0: "#bb5500ff",
        4.0: "#f3cb00ff",
        6.0: "#aaee00ff",
        8.0: "#00aa00ff",
        10.0: None
        }
def search_color(rating: float) -> str:
    previous_value: str = list(color_dict.values())[0]
    for key in color_dict:
        if key > rating:
            return previous_value
        else:
            previous_value = color_dict[key]


# Plot del grafico pie de la calificacion del semestre
fig_semester, ax_semester = plt.subplots()
radius = 2.
ax_semester.pie([1], 
       colors = ["#aaaaaa32"],
       radius = 0.970 * radius,
       wedgeprops={"width": 0.20})
ax_semester.pie([semester_rating, 10 - semester_rating], 
       colors = [search_color(semester_rating), "#aaaaaa00"],
        radius = radius,
       startangle=90., 
       wedgeprops={"width": 0.35})
ax_semester.text(0,0, f"{semester_rating}", 
        ha="center", va="center", fontsize=82,
        color=search_color(semester_rating))
# Haciendo transparente el fondo
fig_semester.patch.set_alpha(0.0)



# Plot del semestre, todas categorias
fig_semhist, ax_semhist = plt.subplots()
bar_colors = [search_color(rating) for rating in semester_data.values()]
bars = ax_semhist.barh(semester_data.keys(), semester_data.values(),
                color = bar_colors,
                height=0.35)
ax_semhist.bar_label(bars, labels=semester_data.values(), padding=2, 
             fontsize=12, color='white', fontweight='bold')
# Add labels on top of bars
for i, (bar, key) in enumerate(zip(bars, semester_data.keys())):
    width = bar.get_width()
    ax_semhist.text(0, bar.get_y() + bar.get_height()/2 + 0.5, 
            f'{key}', 
            ha='left', va='center',
            fontsize=12, color='white', fontweight='bold')

# Haciendo transparente al fondo
fig_semhist.patch.set_facecolor("none")
fig_semhist.patch.set_alpha(0.0)
ax_semhist.set_facecolor("none")
ax_semhist.patch.set_alpha(0.0)
# Remove ticks and labels completely
ax_semhist.set_xticks([])
ax_semhist.set_yticks([])
# Remove only tick labels (keep ticks)
ax_semhist.spines['top'].set_visible(False)
ax_semhist.spines['right'].set_visible(False)
ax_semhist.spines['bottom'].set_visible(False)
ax_semhist.spines['left'].set_visible(False)

# Faculties averages
fig_faculty, ax_faculty = plt.subplots()
bar_colors = [search_color(average) for average in faculty_average.values()]
bars = ax_faculty.barh(faculty_average.keys(), faculty_average.values(),
                      color = bar_colors)
