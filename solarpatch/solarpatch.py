from datetime import datetime
from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

import solarpatch.utils.default_variables as dv
from solarpatch.sources.dataset_factory import DataSource

__all__ = ["SolarPatch"]


class SolarPatch:
    """
    A class to hold and display solar patches.
    """

    def __init__(
        self,
        observation_date: datetime = dv.COTEMPORAL_DATE,
        synthetic: bool = True,
    ) -> None:
        """
        Constructs a SolarPatch object

        Parameters:
        -----------
        observation_date : datetime, optional
            The date and time of the solar patch observation.
            Default is defined in `solarpath.utils.default_varaibles`
            as `dv.COTEMPORAL_TIME`

        synthetic : bool, optional
            Whether the background data is synthetic or not. Default is True.

        Raises:
        -------
        TypeError:
            If the `observation_date` parameter is not an instance of `datetime`.

        NotImplementedError:
            If the `synthetic` parameter is False.

        """

        if not isinstance(observation_date, datetime):
            raise TypeError(
                "The 'observation_date' parameter must be an instance of 'datetime'."
            )

        if not synthetic:
            raise NotImplementedError("`synthetic = False` is not implemented")

        self._observation_date = observation_date
        self._solarpatches = DataSource(
            observation_date=self._observation_date, synthetic=synthetic
        )

    def plot(self, **kwargs):
        if len(self.solarpatches) == 1:
            fig, ax = plt.subplots()
            self.solarpatches[0].plot(ax=ax)
            plt.show()
        elif len(self.solarpatches) == 2:
            fig, axs = plt.subplots(nrows=1, ncols=2)
            for i in range(len(self.solarpatches)):
                ax = axs[i]
                sp = self.solarpatches[i]
                sp.plot(ax=ax, legend=False, plot_axis=True, **kwargs)
            plt.show()
        else:
            raise NotImplementedError("Cannot plot more than 2 SolarPatches")

    @property
    def solarpatches(self) -> List[DataSource]:
        """
        Returns the DataSource objects representing the solar patch data.

        Returns:
        --------
        List[DataSource]:
            A list of DataSource objects representing the solar patch data.

        """

        return self._solarpatches
