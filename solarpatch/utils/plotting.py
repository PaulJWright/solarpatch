from datetime import datetime

import matplotlib.pyplot as plt

__all__ = ["text_plotting", "package_text"]


def text_plotting(
    ax=None,
    observation_date=None,
    series_name=None,
    img_size=None,
    streamlit=True,
    show_date=False,
    **kwargs
):
    """
    Plot date and `series_name`
    """
    if observation_date is None:
        raise ValueError("Please provide an `observation_date`")

    if not show_date:
        date_obj = datetime.strptime(observation_date, "%Y.%m.%d_%H:%M:%S")
        ax.text(
            100,
            img_size - 200,
            date_obj.strftime("%d %b %Y"),
            fontsize=15,
            horizontalalignment="left",
            verticalalignment="top",
            **kwargs
        )
        ax.text(
            100,
            img_size - 100,
            date_obj.strftime("%H:%M:%S"),
            fontsize=15,
            horizontalalignment="left",
            verticalalignment="top",
            **kwargs
        )

        ax.text(3390 + 10, 4100 - 10, series_name)

    if streamlit:
        package_text(ax)


def package_text(ax):
    """
    Plotting the S*ARPS information on the plot
    """
    ax.text(
        100,
        200,
        "S*ARPS",
        fontsize=36,
        horizontalalignment="left",
        verticalalignment="bottom",
    )
    ax.text(
        110,
        100,
        "S-ARPS.github.io",
        fontsize=15,
        horizontalalignment="left",
        color="darkgray",
        verticalalignment="bottom",
    )
