import matplotlib.pyplot as plt

from solarpatch.sources.dataset_factory import DataSource

__all__ = ["SolarPatchCollection"]


class SolarPatchCollection:
    def __init__(self, date, synthetic=True):
        self.date = date
        self.solarpatches = DataSource(
            observation_date=date, synthetic=synthetic
        )

    def plot(self, instrument=None):
        # Check if the instrument is available
        if instrument and instrument not in [
            sp.instrument for sp in self.solarpatches
        ]:
            raise ValueError(
                f"{instrument} data is not available for {self.date}"
            )

        # Plot the solar patches
        if len(self.solarpatches) == 1:
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            if not instrument or self.solarpatches[0].instrument == instrument:
                self.solarpatches[0].plot(ax)
        elif len(self.solarpatches) == 2:
            fig, axes = plt.subplots(1, 2, figsize=(20, 10))
            for i, ax in enumerate(axes):
                if (
                    not instrument
                    or self.solarpatches[i].instrument == instrument
                ):
                    self.solarpatches[i].plot(ax)
        else:
            raise NotImplementedError("Cannot plot more than 2 SolarPatches")
