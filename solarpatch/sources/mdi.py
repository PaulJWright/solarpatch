import multiprocessing as mp

import drms
import numpy as np

import solarpatch.utils.default_variables as dv
from solarpatch.sources.data_base import GenericDataSource
from solarpatch.utils.helper_functions import mdi_bitmap_to_hmi

__all__ = ["MDISolarPatch"]


class MDISolarPatch(GenericDataSource):
    """
    MDI

    This class will extract and set the MDI-specific keys  before
    obtaining the MDI full-disk data, and SHARP patches.
    """

    def __init__(self, observation_date, synthetic, **kwargs):
        """
        Parameters
        ----------
        """

        self.instrument = "MDI"
        self._mag_keys_required = [
            "CRPIX1",
            "CRPIX2",
            "RSUN_OBS",
            "T_OBS",
            "CDELT1",
        ]
        self._patch_keys_required = ["CRPIX1", "CRPIX2", "TARPNUM"]
        self.series_name = "TARPNUM"
        self.image_size = 1024
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

    # MDI-specific methods for getting the data
    def _get_fulldisk_data(self):
        """
        get the fulldisk MDI data

        Parameters
        ----------

        self : ...

        Returns
        -------

        keys : Dict
            a dictionary of keys (metadata for the MDI image)

        segs : Optional = None:
            segments returned if Synthetic is False

        """

        # check if the magnetogram requested is MDI or mdi
        magnetogram_string = (
            f"mdi.fd_M_96m_lev182[{self._original_observation_date}]"
        )

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

    # MDI-specific methods for getting the data
    def _get_patches_bitmap(self):
        """
        get the bitmap SHARP patches

        Returns
        -------
        patch_data : List[np.array]
            a list containing the patches for MDI

        """

        patch_keys, patch_segs = self._c.query(
            f"mdi.smarp_96m[][{self._observation_date}]",
            key=self._patch_keys_required,
            seg="bitmap",  # can also have magnetogram here...
        )

        urls = dv.JSOC_BASE_URL + patch_segs.bitmap

        with mp.Pool(processes=4) as pool:  # create a pool of 4 processes
            patch_data = pool.map(self.get_patch_data, urls)

        # convert MDI bitmap to HMI-like data.
        patch_data = mdi_bitmap_to_hmi(patch_data)

        return patch_data, patch_keys, patch_segs

    @classmethod
    def datasource(cls, observation_date: str, synthetic: bool) -> bool:
        """
        Determines if the ``observation_date`` should lead to
        the instantiation of this child class.

        Parameters
        ----------
        observation_date : str
            The date of the observation in the format "YYYY.MM.DD_HH:MM:SS".

        synthetic : bool
            Whether to use synthetic data.

        Returns
        -------
        bool
            True if this child class should be instantiated, False otherwise.
        """
        # return (
        #     dv.MDI_DATES['start_time'] <= observation_date <= dv.MDI_DATES['end_time']
        # )
        statement = (
            dv.MDI_DATES["start_time"]
            <= observation_date
            <= dv.MDI_DATES["end_time"]
        )

        # Might be more efficient to return the whole query...
        if statement:
            k = drms.Client(
                debug=False, verbose=False, email=dv.JSOC_EMAIL
            ).query(f"mdi.fd_M_96m_lev182[{observation_date}]", key=["CDELT1"])
            return len(k) != 0
        else:
            return False
