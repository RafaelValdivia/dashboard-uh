import pandas as pd
import matplotlib.pyplot as plt
from data import *

darkmode = True
fontcolor = "#fff" if darkmode else "#000"

def color(rating: float) -> str:
    color_dict: dict[float, str] = {
            0.0: "#bb0000ff",
            2.0: "#cc6600ff",
            4.0: "#e3cc00ff",
            6.0: "#99cc00ff",
            7.0: "#00bb00ff",
            10.0: None
            } 
    previous_value: str = list(color_dict.values())[0]
    for key in color_dict:
        if key >= rating:
            return previous_value
        else:
            previous_value = color_dict[key]

def crplot():
    #
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("none")
    fig.patch.set_alpha(0.0)
    # 
    ax.set_facecolor("none")
    ax.patch.set_alpha(0.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    #
    return fig, ax

def rtng_pie(rtng: float):
    fig, ax = crplot()
    ax.pie([rtng, 10 - rtng],
                colors=[color(rtng), "#77777777"],
                startangle=90.,
                wedgeprops={"width": 0.25}
               )

    ax.text(0,0, str(round(rtng,1)),
                ha="center", va="center", fontsize=32,
                color=color(rtng)
                )
    return fig, ax
 
def rtng_hist(data: dict):
    fig, ax = crplot()
    ax.set_yticks([])
    ax.set_xticks([])
    ax.barh(data.keys(), [10. for _ in range(len(data))],
            color="#77777777",
            height=0.30
            )
    bars = ax.barh(data.keys(), data.values(),
                 color=[color(value) for value in data.values()],
                 height=0.30
                        )
    for bar, key in zip(bars, data):
        value = data[key]
        width = bar.get_width()
        width = width + 0.1 if width <= 9.0 else 10.1
        ax.text(width,
                bar.get_y() + bar.get_height()/2 - 0.03,
                str(round(value,1)), 
                ha="left", va="center",
                fontsize=16, color=color(value),
                fontweight="bold"
                )
        ax.text(0, bar.get_y() + bar.get_height() + 0.1,
                key, fontsize=20, color=fontcolor
                )
    return fig, ax

def avrg_hist(data: dict):
    fig, ax = crplot()
    min_lim = min(data.values())
    min_lim = max(0, min_lim - 1)
    max_lim = round(max(data.values()) + 0.5, 0)
    ax.set_xlim(min_lim, max_lim)
    bars = ax.barh(data.keys(), data.values(),
                color=[color(value) for value in data.values()]
                )
    ax.bar_label(bars,
                  labels=[round(value, 1) for value in data.values()],
                  color=fontcolor
                  )
    ax.set_yticks(list(data.keys()))
    ax.tick_params(axis="both", colors=fontcolor)
    return fig, ax

def mark_hist(data: dict, colors: list[str]):
    fig, ax = crplot()
    fig.set_facecolor("none")
    bars = ax.bar(data.keys(), data.values(),
           )
    ax.bar_label(bars, 
                 labels=data.values(), 
                 color=fontcolor,
                 fontsize=20                 
                 )
    ax.tick_params(axis="both", colors=fontcolor)
    return fig, ax

def matr_pie(data: dict, colors:list[str]):
    fig, ax = crplot()
    ax.pie(data.values(), labels=data.keys(),
           colors=colors,
           wedgeprops={"width":0.35},
           textprops={"color":fontcolor}
           )
    ax.pie(data.values(), labels=data.values(),
           colors=["#ffffff00" for _ in data],
           radius=0.70,
           textprops={"color":"white",
                      "fontsize":14,
                      "fontweight":"bold"
                      }
           )
    ax.text(0,0,
            sum(data.values()),
            ha="center", va="center",
            fontsize=32, fontweight="bold",
            color=fontcolor
            )
    return fig, ax
