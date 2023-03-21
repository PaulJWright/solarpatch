import datetime
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt


class GenericDataSource(ABC):
    # initialise the ``_registry`` with an empty dict()
    _registry = dict()

    def __init_subclass__(cls, **kwargs):
        """
        This hook initialises the subclasses of the GenericDataSource class.
        This block of code is called for each subclass, and is used to register
        each subclass in a dict that has the ``datasource`` attribute.
        This is passed into the DataSource Factory for registration.
        """
        super().__init_subclass__(**kwargs)

        if hasattr(cls, "datasource"):
            cls._registry[cls] = cls.datasource

    def __init__(self, date):
        # self._instrument = instrument
        # self._meta = meta
        self.date = date
        # Initialize data for this instrument and date

    def plot(self, ax):
        # Plot the active regions ("patches") on the sun for this instrument and date
        ax.set_title(f"{self.instrument} {self.date}")
        # Code to plot active regions on the sun for this instrument and date
