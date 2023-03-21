import copy
import multiprocessing as mp

import drms

import solarpatch.utils.default_variables as dv
from solarpatch.sources.data_base import GenericDataSource

__all__ = ["HMISolarPatch"]


class HMISolarPatch(GenericDataSource):
    """
    HMI

    This class will extract and set the HMI-specific keys  before
    obtaining the HMI full-disk data, and SHARP patches.
    """

    def __init__(self, observation_date, synthetic, **kwargs):
        """
        Parameters
        ----------
        """
        self.instrument = "HMI"
        self._mag_keys_required = [
            "CRPIX1",
            "CRPIX2",
            "RSUN_OBS",
            "T_OBS",
            "CDELT1",
        ]
        self.series_name = "HARPNUM"
        self.image_size = 4096

        self._patch_keys_required = ["CRPIX1", "CRPIX2", "HARPNUM"]

        self._jsoc_email = dv.JSOC_EMAIL
        self._c = drms.Client(
            debug=False, verbose=False, email=self._jsoc_email
        )

        super().__init__(observation_date, synthetic, **kwargs)
        # this will set the:
        #   - self._original_observation_date
        #   - self._synthetic (Bool)

        #   - self._keys, self._segs (results of self._get_fulldisk_data)
        #   - self._observation_date (from self._keys)

        #   - self._data (SynthSun or RealSun)
        #   - self._get_patch_data()
        #   - self._data.rotate()

    # HMI-specific methods for getting the data
    def _get_fulldisk_data(self, synthetic=True):
        """
        get the fulldisk HMI data

        Parameters
        ----------

        self : ...

        Returns
        -------

        keys : Dict
            a dictionary of keys (metadata for the HMI image)

        segs : Optional = None:
            segments returned if Synthetic is False

        """

        # check if the magnetogram requested is hmi or mdi
        magnetogram_string = f"hmi.M_720s[{self._original_observation_date}]"

        # if synthetic, only return keys
        if self._synthetic:
            keys = self._c.query(
                magnetogram_string, key=self._mag_keys_required
            )
            segs = None
        else:
            keys, segs = self._c.query(
                magnetogram_string,
                key=self._mag_keys_required,
                segs="magnetogram",
            )

        # raise error if there are no keys returned
        if len(keys) == 0:
            raise ValueError(f"{self._date_time} returns no results!")

        return keys, segs

    # HMI-specific methods for getting the data
    def _get_patches_bitmap(self):
        """
        get the bitmap SHARP patches

        Returns
        -------
        patch_data : List[np.array]
            a list containing the patches for HMI

        """

        patch_keys, patch_segs = self._c.query(
            f"hmi.sharp_720s[][{self._observation_date}]",
            key=self._patch_keys_required,
            seg="bitmap",
        )

        urls = dv.BASE_URL + patch_segs.bitmap

        with mp.Pool(processes=4) as pool:  # create a pool of 4 processes
            patch_data = pool.map(self.get_patch_data, urls)

        return patch_data, patch_keys, patch_segs

    @classmethod
    def datasource(cls, observation_date, synthetic) -> bool:
        """
        Determines if ``instrument`` should lead to the instantiation
        of this child class
        """

        return (
            observation_date == "2010.07.14_11:00:08"
            and synthetic == synthetic
        )
