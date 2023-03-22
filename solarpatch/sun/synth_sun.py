import numpy as np

from solarpatch.sun.generic_sun import GenericSun


class SynthSun(GenericSun):
    def __init__(self, keys, img_size):
        super().__init__(keys, img_size)

    def data_gen(self, keys, img_size):
        """
        generate the blank map of the Sun:
            * 1.0 on disk
            * nan off disk
        """
        # setting up the data
        x, y = np.arange(0, img_size), np.arange(0, img_size)
        data = np.zeros((y.size, x.size)) * np.nan

        # get solar radius
        radius = keys["RSUN_OBS"][0] / keys["CDELT1"][0]

        # set all values within the radius as 1.0 (nan outside)
        mask = (x[np.newaxis, :] - keys["CRPIX2"][0]) ** 2 + (
            y[:, np.newaxis] - keys["CRPIX1"][0]
        ) ** 2 < radius**2

        data[mask] = 1.0

        return data

    def is_real(self):
        return False
