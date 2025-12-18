import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configure matplotlib
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Helvetica"]

# Custom color map (red-yellow-green)
COLORS = ["#f00", "#ce0", "#0a0"]
GRADE_CMAP = mcolors.LinearSegmentedColormap.from_list("grade_cmap", COLORS, 10)


class Plotter:
    """Utility class for creating consistent plots"""

    @staticmethod
    def create_clean_plot(rows=1, cols=1, figsize=(8, 8)):
        """Create a clean matplotlib plot with transparent background"""
        fig, ax = plt.subplots(rows, cols, figsize=figsize)

        # Set transparent background
        fig.patch.set_facecolor("none")
        fig.patch.set_alpha(0.0)

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

    @staticmethod
    def create_color_legend(figsize=(14, 1)):
        """Create a color legend bar showing the rating scale"""
        fig, ax = Plotter.create_clean_plot(figsize=figsize)

        # Create colorbar
        cb = mpl.colorbar.ColorbarBase(
            ax,
            cmap=GRADE_CMAP,
            norm=mpl.colors.Normalize(0, 10),
            orientation="horizontal",
        )

        # Add labels
        ax.text(-0.5, -0.5, "1", color=GRADE_CMAP(0.0), fontsize=40)
        ax.text(10.2, -0.5, "10", color=GRADE_CMAP(1.0), fontsize=40)
        ax.set_xticks([])

        return fig, ax

    @staticmethod
    def create_rating_pie(rating: float):
        """Create a pie chart showing a rating"""
        fig, ax = Plotter.create_clean_plot()

        # Create pie chart
        ax.pie(
            [rating, 10 - rating],
            colors=[GRADE_CMAP(rating / 10), "#77777777"],
            startangle=90,
            wedgeprops={"width": 0.25},
        )

        # Add rating text in center
        ax.text(
            0,
            0,
            str(round(rating, 1)),
            ha="center",
            va="center",
            fontsize=50,
            color=GRADE_CMAP(rating / 10),
            fontweight="bold",
        )

        return fig, ax

    @staticmethod
    def create_rating_barplot(ratings_series):
        """Create a horizontal bar plot for ratings"""
        fig, ax = Plotter.create_clean_plot()

        # Remove ticks
        ax.set_yticks([])
        ax.set_xticks([])

        # Background bars (full length)
        ax.barh(
            ratings_series.index,
            [10.0] * len(ratings_series),
            color="#77777775",
            height=0.30,
        )

        # Actual rating bars
        bars = ax.barh(
            ratings_series.index,
            ratings_series.values,
            color=[GRADE_CMAP(value / 10) for value in ratings_series.values],
            height=0.30,
        )

        # Add value labels
        for bar, category, value in zip(
            bars, ratings_series.index, ratings_series.values
        ):
            width = bar.get_width()
            width = width + 0.1 if width <= 9.0 else 10.1

            ax.text(
                width,
                bar.get_y() + bar.get_height() / 2 - 0.03,
                str(round(value, 1)),
                ha="left",
                va="center",
                fontsize=16,
                color=GRADE_CMAP(value / 10),
                fontweight="bold",
            )

            ax.text(
                0,
                bar.get_y() + bar.get_height() + 0.1,
                category,
                fontsize=16,
            )

        return fig, ax

    @staticmethod
    def create_faculty_average_plot(df):
        """Create a bar plot showing faculty averages"""
        fig, ax = Plotter.create_clean_plot()

        # Calculate averages
        fac_df = df.copy().T.mean().round(2)

        # Set limits
        min_lim = max(0, min(fac_df) - 1)
        max_lim = round(max(fac_df) + 0.5, 0)
        ax.set_xlim(min_lim, max_lim)

        # Create bars
        bars = ax.barh(
            fac_df.index, fac_df, color=[GRADE_CMAP(value / 10.0) for value in fac_df]
        )

        ax.set_yticks(list(fac_df.index))
        return fig, ax

    @staticmethod
    def create_grade_distribution_plot(grade_counts):
        """Create a bar plot for grade distribution"""
        fig, ax = Plotter.create_clean_plot()

        # Convert to DataFrame if needed
        if isinstance(grade_counts, dict):
            grade_counts = pd.DataFrame(
                {
                    "Nota": list(grade_counts.keys()),
                    "Count": list(grade_counts.values()),
                }
            )

        # Create bar plot
        bars = ax.bar(
            grade_counts["Nota"].astype(str),
            grade_counts["Count"],
            color=GRADE_CMAP(0.7),  # Single color for distribution
        )

        # Add labels
        for bar, count in zip(bars, grade_counts["Count"]):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.1,
                f"{count}",
                ha="center",
                va="bottom",
                fontsize=12,
            )

        ax.set_xlabel("Nota")
        ax.set_ylabel("Cantidad de Estudiantes")

        return fig, ax

    @staticmethod
    def create_enrollment_pie(enrollment_data, colors=None):
        """Create a pie chart for enrollment data"""
        fig, ax = Plotter.create_clean_plot()

        # Convert to DataFrame if needed
        if isinstance(enrollment_data, dict):
            enrollment_data = pd.DataFrame(
                {
                    "Brigada": list(enrollment_data.keys()),
                    "Count": list(enrollment_data.values()),
                }
            )

        # Default colors
        if colors is None:
            colors = plt.cm.Set3(np.linspace(0, 1, len(enrollment_data)))

        # Outer pie (categories)
        ax.pie(
            enrollment_data["Count"],
            labels=enrollment_data["Brigada"],
            colors=colors,
            wedgeprops={"width": 0.35},
            textprops={"fontsize": 12, "fontweight": "bold"},
        )

        # Inner pie (counts)
        ax.pie(
            enrollment_data["Count"],
            labels=enrollment_data["Count"],
            colors=["#ffffff00"] * len(enrollment_data),
            radius=0.70,
            textprops={"color": "white", "fontsize": 10, "fontweight": "bold"},
        )

        # Total in center
        ax.text(
            0,
            0,
            str(sum(enrollment_data["Count"])),
            ha="center",
            va="center",
            fontsize=24,
            fontweight="bold",
        )

        return fig, ax


# Legacy function names for backward compatibility
def crplot(rows=1, cols=1, figsize=(8, 8)):
    return Plotter.create_clean_plot(rows, cols, figsize)


def color_legend():
    return Plotter.create_color_legend()


def rating_pie(rating: float, more=False):
    return Plotter.create_rating_pie(rating)


def rating_hist(Series):
    return Plotter.create_rating_barplot(Series)


def fac_avrg(df):
    return Plotter.create_faculty_average_plot(df)


def mark_hist(data):
    return Plotter.create_grade_distribution_plot(data)


def matr_pie(data: dict, colors: list[str]):
    return Plotter.create_enrollment_pie(data, colors)
