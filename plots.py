import matplotlib.pyplot as plt
import matplotlib as mpl
# import matplotlib.animation as animation
import numpy as np
import matplotlib.colors as mcolors

colors = ['#f00', '#c90', '#0a0']
gb_cmap = mcolors.LinearSegmentedColormap.from_list('my_cmap', colors)
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Times New Roman' ,'Arial', 'Helvetica', 'DejaVu Sans']


def crplot(rows = 1, cols = 1, figsize = (8,8)):
    #
    fig, ax = plt.subplots(rows, cols, figsize = figsize)
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

def color_legend():
    fig, ax = crplot(figsize=(14, 1))

    # Clean approach for standalone colorbar:

    cb = mpl.colorbar.ColorbarBase(ax, cmap=gb_cmap, 
                               norm=mpl.colors.Normalize(0, 10),
                               orientation='horizontal')
    ax.text(-.5,-.5,"1", color=gb_cmap(0.), fontsize=40)
    ax.text(10.2,-.5,"10", color=gb_cmap(1.), fontsize=40)
    ax.set_xticks([])
    return fig, ax

def animate_pie(frame):
    cur_rating = (frame/30)**2 * rating * 2
    if cur_rating <= rating:
        ax.clear()
        ax.pie([cur_rating, 10 - cur_rating],
                # colors = []
                startangle=90,
                wedgeprops={"width": 0.25}
                )

def rating_pie(rating: float, more = False):
    fig, ax = crplot()
    ax.pie([rating, 10 - rating],
                colors = [gb_cmap(rating/10), "#77777777"],
                startangle=90,
                wedgeprops={"width": 0.25}
                )
    #ax.text(0,-.4, f"Calificación\npromedio",
    #        ha="center", va="center", fontsize=20,
    #            )
    ax.text(0,0, str(round(rating,1)),
                ha="center", va="center", fontsize=50,
                color=gb_cmap(rating/10),
                fontweight="bold"
                )
    return fig, ax

def rating_hist(Series):
    fig, ax = crplot()
    ax.set_yticks([])
    ax.set_xticks([])
    ax.barh(Series.index, [10. for _ in range(len(Series))],
            color="#77777775",
            height=0.30
            )
    bars = ax.barh(Series.index, Series,
                 color=[gb_cmap(value/10) for value in Series],
                 height=0.30
                        )
    for bar, key, value in zip(bars, Series.index, Series):
        width = bar.get_width()
        width = width + 0.1 if width <= 9.0 else 10.1
        ax.text(width,
                bar.get_y() + bar.get_height()/2 - 0.03,
                str(round(value,1)), 
                ha="left", va="center",
                fontsize=16, color=gb_cmap(value/10),
                fontweight="bold"
                )
        ax.text(0, bar.get_y() + bar.get_height() + 0.1,
                key, fontsize=20,
                )
    return fig, ax

def fac_avrg(df):
    fig, ax = crplot()
    fac_df = df.copy()
    fac_df = fac_df.T.mean()
    fac_df = round(fac_df,2)
    min_lim = min(fac_df)
    min_lim = max(0, min_lim - 1)
    max_lim = round(max(fac_df) + 0.5, 0)
    ax.set_xlim(min_lim, max_lim)
    bars = ax.barh(fac_df.index, fac_df,
                color=[gb_cmap(value/10.) for value in fac_df]
                )
    
    ax.set_yticks(list(fac_df.index))
    # ax.tick_params(axis="both")
    return fig, ax