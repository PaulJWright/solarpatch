import numpy as np

from solarpatch.sun.generic_sun import GenericSun


class SynthSun(GenericSun):
    def __init__(self, keys):
        super().__init__(keys)

    def data_gen(self, keys):
        """
        generate the data
        """
        x = np.arange(0, 4096)  # need to remove hard-coded value here...
        y = np.arange(0, 4096)
        radius = keys["RSUN_OBS"][0] / keys["CDELT1"][0]

        data = np.zeros((y.size, x.size)) * np.nan
        mask = (x[np.newaxis, :] - keys["CRPIX2"][0]) ** 2 + (
            y[:, np.newaxis] - keys["CRPIX1"][0]
        ) ** 2 < radius**2
        data[mask] = 1.0

        return data

    def is_real(self):
        return False
