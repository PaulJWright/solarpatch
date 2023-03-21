import numpy as np

from solarpatch.utils.helper_functions import rotate_points


class GenericSun:  # based on SunPy map
    def __init__(self, keys, img_size):
        # set the data
        self.data = self.data_gen(keys, img_size)

        return

    def extract_keys(self):
        pass

    def rotate(self):
        return rotate_points(self.points, self.origin, self.degrees)

    def _get_patches(self):
        """
        obtain patches for the given date
        """
        pass

    @classmethod
    def data_gen(self, keys):
        """
        data generation class

        Parameters
        ----------
        keys : Dict
            A dictionary of keys

        Returns
        -------
        data : np.array of data
        """
        pass

    @classmethod
    def is_real(self):
        raise NotImplementedError()
