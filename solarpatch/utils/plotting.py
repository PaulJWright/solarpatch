from datetime import datetime

import matplotlib.pyplot as plt

__all__ = ["text_plotting", "package_text"]


def text_plotting(
    observation_date=None,
    series_name=None,
    img_size=None,
    streamlit=True,
    **kwargs
):
    """
    Plot date and `series_name`
    """
    if observation_date is None:
        raise ValueError("Please provide an `observation_date`")

    date_obj = datetime.strptime(observation_date, "%Y.%m.%d_%H:%M:%S")
    plt.text(
        100,
        img_size - 200,
        date_obj.strftime("%d %b %Y"),
        fontsize=15,
        horizontalalignment="left",
        verticalalignment="top",
        **kwargs
    )
    plt.text(
        100,
        img_size - 100,
        date_obj.strftime("%H:%M:%S"),
        fontsize=15,
        horizontalalignment="left",
        verticalalignment="top",
        **kwargs
    )

    plt.text(3390 + 10, 4100 - 10, series_name)

    if streamlit:
        package_text()


def package_text():
    """
    Plotting the S*ARPS information on the plot
    """
    plt.text(
        100,
        200,
        "S*ARPS",
        fontsize=36,
        horizontalalignment="left",
        verticalalignment="bottom",
    )
    plt.text(
        110,
        100,
        "S-ARPS.github.io",
        fontsize=15,
        horizontalalignment="left",
        color="darkgray",
        verticalalignment="bottom",
    )
