import copy
import multiprocessing as mp
from typing import List, Optional, Tuple

import drms
import numpy as np

import solarpatch.utils.default_variables as dv
from solarpatch.sources.data_base import GenericDataSource

__all__ = ["HMISolarPatch"]


class HMISolarPatch(GenericDataSource):
    """
    HMI

    This class extracts and sets the HMI-specific keys before obtaining the
    HMI full-disk data and SHARP patches.

    Parameters
    ----------
    observation_date : str
        The date of the observation in the format "YYYY.MM.DD_HH:MM:SS".

    synthetic : bool
        Whether to use synthetic data.

    **kwargs :
        Additional keyword arguments to be passed to the base class constructor.

    Attributes
    ----------
    instrument : str
        The name of the instrument.

    _mag_keys_required : List[str]
        A list of keys required for the HMI magnetogram.

    series_name : str
        The series name of the HMI data.

    image_size : int
        The size of the HMI image.

    _patch_keys_required : List[str]
        A list of keys required for the SHARP patches.

    _jsoc_email : str
        The email address used to access the JSOC data.

    _c : drms.Client
        The DRMS client instance.

    _original_observation_date : str
        The original observation date.

    _synthetic : bool
        Whether to use synthetic data.

    _keys : dict
        A dictionary of keys (metadata for the HMI image).

    _segs : dict or None
        A dictionary of segments for the HMI image if synthetic is False.

    _observation_date : str
        The observation date.

    _data : SynthSun or RealSun
        An instance of SynthSun or RealSun, depending on the value of _synthetic.

    Methods
    -------
    _get_fulldisk_data() -> Tuple[dict, Optional[dict]]
        Get the fulldisk HMI data.

    _get_patches_bitmap() -> Tuple[List[np.ndarray], dict, dict]
        Get the bitmap SHARP patches.

    datasource(observation_date: str, synthetic: bool) -> bool
        Determines if ``instrument`` and ``observation_date`` should lead to
        the instantiation of this child class.

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
    def _get_fulldisk_data(self) -> Tuple[dict, Optional[dict]]:
        """
        Get the fulldisk HMI data.

        Parameters
        ----------
        synthetic : bool, optional
            Whether to use synthetic data, by default True.

        Returns
        -------
        Tuple[dict, Optional[dict]]
            A tuple containing a dictionary of keys (metadata for the HMI image)
            and optionally a list of segments if synthetic is False.
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
            raise ValueError(
                f"{self._original_observation_date} returns no results!"
            )

        # check output types
        return keys, segs

    # HMI-specific methods for getting the data
    def _get_patches_bitmap(self) -> Tuple[List[np.ndarray], dict, dict]:
        """
        Get the bitmap SHARP patches.

        Returns
        -------
        Tuple[List[np.ndarray], dict, dict]
            A tuple containing a list of numpy arrays containing the patches,
            a dictionary of keys (metadata for the SHARP patches), and a
            dictionary of segments for the SHARP patches.
        """

        patch_keys, patch_segs = self._c.query(
            f"hmi.sharp_720s[][{self._observation_date}]",
            key=self._patch_keys_required,
            seg="bitmap",
        )

        urls = dv.JSOC_BASE_URL + patch_segs.bitmap

        with mp.Pool(processes=4) as pool:  # create a pool of 4 processes
            patch_data = pool.map(self.get_patch_data, urls)

        # check output types
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

        # might want to do this here so only instantiate if we find a HMI image

        statement = (
            dv.HMI_DATES["start_time"]
            <= observation_date
            <= dv.HMI_DATES["end_time"]
        )

        if statement:
            k = drms.Client(
                debug=False, verbose=False, email=dv.JSOC_EMAIL
            ).query(f"hmi.M_720s[{observation_date}]", key=["CDELT1"])
            return len(k) != 0
        else:
            return False
