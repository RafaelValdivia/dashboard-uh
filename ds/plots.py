# Updated plots.py - removing broken functions
from cProfile import label

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

colors = ["#f00", "#ce0", "#0a0"]
gb_cmap = mcolors.LinearSegmentedColormap.from_list("my_cmap", colors, 10)
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = [
    "Times New Roman",
    "Arial",
    "Helvetica",
    "DejaVu Sans",
]


def crplot(rows=1, cols=1, figsize=(8, 8)):
    """Create a clean plot with transparent background"""
    fig, ax = plt.subplots(rows, cols, figsize=figsize)
    fig.patch.set_facecolor("none")
    fig.patch.set_alpha(0.0)

    # Handle single axis or multiple axes
    if hasattr(ax, "__iter__"):
        for a in ax.flat:
            a.set_facecolor("none")
            a.patch.set_alpha(0.0)
            a.spines["top"].set_visible(False)
            a.spines["right"].set_visible(False)
            a.spines["bottom"].set_visible(False)
            a.spines["left"].set_visible(False)
    else:
        ax.set_facecolor("none")
        ax.patch.set_alpha(0.0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return fig, ax


def color_legend():
    """Create a color legend for ratings"""
    fig, ax = crplot(figsize=(14, 1))

    cb = mpl.colorbar.ColorbarBase(
        ax, cmap=gb_cmap, norm=mpl.colors.Normalize(0, 10), orientation="horizontal"
    )
    ax.text(-0.5, -0.5, "1", color=gb_cmap(0.0), fontsize=40)
    ax.text(10.2, -0.5, "10", color=gb_cmap(1.0), fontsize=40)
    ax.set_xticks([])
    return fig, ax


def rating_pie(rating: float, more=False):
    """Create a pie chart showing rating"""
    fig, ax = crplot()
    ax.pie(
        [rating, 10 - rating],
        colors=[gb_cmap(rating / 10), "#77777777"],
        startangle=90,
        wedgeprops={"width": 0.25},
    )
    ax.text(
        0,
        0,
        str(round(rating, 1)),
        ha="center",
        va="center",
        fontsize=50,
        color=gb_cmap(rating / 10),
        fontweight="bold",
    )
    return fig, ax


def rating_hist(Series):
    """Create a horizontal bar chart for ratings"""
    fig, ax = crplot()
    ax.set_yticks([])
    ax.set_xticks([])

    # Ensure Series has an index
    if not hasattr(Series, "index"):
        Series = pd.Series(Series)

    # Background bars
    ax.barh(
        Series.index, [10.0 for _ in range(len(Series))], color="#77777775", height=0.30
    )

    # Rating bars
    bars = ax.barh(
        Series.index,
        Series.values,
        color=[gb_cmap(value / 10) for value in Series.values],
        height=0.30,
    )

    for bar, key, value in zip(bars, Series.index, Series.values):
        width = bar.get_width()
        width = width + 0.1 if width <= 9.0 else 10.1
        ax.text(
            width,
            bar.get_y() + bar.get_height() / 2 - 0.03,
            str(round(value, 1)),
            ha="left",
            va="center",
            fontsize=16,
            color=gb_cmap(value / 10),
            fontweight="bold",
        )
        ax.text(
            0,
            bar.get_y() + bar.get_height() + 0.1,
            key,
            fontsize=20,
        )
    return fig, ax


def fac_avrg(df):
    """Create faculty average bar chart"""
    fig, ax = crplot()

    # Ensure df is a DataFrame with proper indexing
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    fac_df = df.copy()

    # Calculate average for each faculty
    if isinstance(fac_df.index, pd.RangeIndex):
        # If it's a range index, we need to set the index first
        fac_df.set_index("Facultad", inplace=True)

    # Calculate mean across columns (rating categories)
    fac_means = fac_df.mean(axis=1)

    # Sort for better visualization
    fac_means = fac_means.sort_values()

    min_lim = max(0, min(fac_means) - 1)
    max_lim = round(max(fac_means) + 0.5, 0)
    ax.set_xlim(min_lim, max_lim)

    bars = ax.barh(
        fac_means.index,
        fac_means.values,
        color=[gb_cmap(value / 10.0) for value in fac_means.values],
    )

    ax.set_yticks(list(fac_means.index))
    return fig, ax


def mark_hist(data):
    """Create a grade distribution histogram"""
    fig, ax = crplot()
    fig.set_facecolor("none")

    # Handle different input types
    if isinstance(data, pd.DataFrame):
        # DataFrame with 'Nota' and 'Count' columns
        notas = data["Nota"].astype(str).tolist()
        counts = data["Count"].tolist()
    elif isinstance(data, dict):
        # Dictionary with grade counts
        if "Nota" in data and "Count" in data:
            notas = [str(n) for n in data["Nota"]]
            counts = data["Count"]
        else:
            notas = list(data.keys())
            counts = list(data.values())
    else:
        raise ValueError("Input must be DataFrame or dict")

    bars = ax.bar(notas, counts)

    # Add labels
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.5,
            f"{count}",
            ha="center",
            va="bottom",
            fontsize=12,
        )

    ax.set_xlabel("Nota")
    ax.set_ylabel("Cantidad")
    return fig, ax


def matr_pie(data: dict, colors: list[str] = None):
    """Create a pie chart for enrollment data"""
    fig, ax = crplot()

    # Handle input types
    if isinstance(data, pd.DataFrame):
        labels = data["Brigada"].tolist()
        sizes = data["Count"].tolist()
    elif isinstance(data, dict):
        if "Brigada" in data and "Count" in data:
            labels = data["Brigada"]
            sizes = data["Count"]
        else:
            labels = list(data.keys())
            sizes = list(data.values())
    else:
        raise ValueError("Input must be DataFrame or dict")

    # Default colors if not provided
    if colors is None:
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

    ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        wedgeprops={"width": 0.35},
        textprops={"fontsize": 12, "fontweight": "bold"},
    )

    # Inner ring with counts
    ax.pie(
        sizes,
        labels=sizes,
        colors=["#ffffff00" for _ in sizes],
        radius=0.70,
        textprops={"color": "white", "fontsize": 10, "fontweight": "bold"},
    )

    ax.text(
        0,
        0,
        str(sum(sizes)),
        ha="center",
        va="center",
        fontsize=24,
        fontweight="bold",
    )
    return fig, ax


# Import pandas if needed for type checking
import pandas as pd
