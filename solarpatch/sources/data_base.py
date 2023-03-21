import copy
import datetime
import multiprocessing as mp
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

import drms
import matplotlib.patches as ptc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits
from matplotlib.colors import BoundaryNorm, ListedColormap

import solarpatch.utils.default_variables as dv
from solarpatch.sun.real_sun import RealSun
from solarpatch.sun.synth_sun import SynthSun
from solarpatch.utils.plotting import text_plotting


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

    def __init__(self, observation_date, synthetic=True):
        # set the parameters
        self._original_obs_date = observation_date
        self._synthetic = synthetic

        # get and set fulldisk data
        self._keys, self._segs = self._get_fulldisk_data(synthetic)

        # update the observation date based on the magnetogram obtained
        self._observation_date = self._keys.T_OBS[0][
            :-4
        ]  # should we be using T_OBS?
        # alert the user that we are using a different observation date

        if np.all(self._original_obs_date != self._observation_date):
            # logger.info
            print(
                f"the provided date was {self._original_obs_date}, \n"
                + f"the retrieved magnetogram is from {self._observation_date}"
            )

        # generate the data
        self._data = SynthSun(self._keys) if self._synthetic else RealSun()

        # get and set the patch data
        (
            self.patch_data,
            self.patch_keys,
            self.patch_segs,
        ) = self._get_patches_bitmap()
        self._get_bboxes()

        # rotate the data and bounding boxes
        # self._data.rotate(self._keys['CROTA1'])

    def get_patch_data(self, url):
        return fits.getdata(url)

    @property
    def observation_date(self) -> str:
        # this should be set on instantiation and then only read; shouldn't be able to change it...
        return self._observation_date

    @property
    def data(self):
        """return the data"""
        return self._data

    @abstractmethod
    def _get_fulldisk_data(self, synthetic) -> Dict:
        """
        get the fulldisk data from the data source. This should be keys-only if
        synthetic=True, else segs should also be returned.
        """
        pass

    # @abstractmethod
    # def _set_fulldisk_data(self):
    #     """ set the fulldisk data into the """
    #     pass

    # def _get_patch_data(self):
    #     pass

    # def _set_patch_data(self):
    #     self._data.set_bitmap_data(...)

    def _get_bboxes(self):
        """
        Method to get the set of bounding boxes in parallel
        """
        with ThreadPoolExecutor() as executor:
            self.bbox = executor.map(
                self._one_patch, range(self.patch_keys.shape[0])
            )

    def _get_single_bbox(
        self, i, hatch="", fill=False, snap=False, lw=1.25, **kwargs
    ):
        """
        get the dimensions of a single bounding box

        Returns
        -------
        y1, y2, x1, x2,

        matplotlib.patches.Rectangle : Rectange corresponding to the single bounding box

        """

        # extract shape of the patch
        YDIM_CCD, XDIM_CCD = self.patch_data[i].shape

        # xy values of the box boundaries
        y2 = int(
            np.rint(
                self._data.data.shape[0]
                - self._keys.CRPIX2
                - self.patch_keys.iloc[i].CRPIX2
                + YDIM_CCD
            )
        )
        y1 = int(
            np.rint(
                self._data.data.shape[0]
                - self._keys.CRPIX2
                - self.patch_keys.iloc[i].CRPIX2
            )
        )
        x2 = int(
            np.rint(
                self._data.data.shape[0]
                - self._keys.CRPIX1
                - self.patch_keys.iloc[i].CRPIX1
                + XDIM_CCD
            )
        )
        x1 = int(
            np.rint(
                self._data.data.shape[0]
                - self._keys.CRPIX1
                - self.patch_keys.iloc[i].CRPIX1
            )
        )

        return (
            y1,
            y2,
            x1,
            x2,
            ptc.Rectangle(
                (x1, y1),
                XDIM_CCD,
                YDIM_CCD,
                hatch=hatch,
                fill=fill,
                snap=snap,
                lw=lw,
                **kwargs,
            ),
        )

    def _one_patch(self, i):
        """
        obtain the bounding box and update the data for one patch
        """

        # region number
        region_number = int(self.patch_keys.iloc[i].HARPNUM)

        # get x/y values of rectangle and the rectangle object.
        y1, y2, x1, x2, rectangle = self._get_single_bbox(i)

        self._update_data_with_patch(i, y1, y2, x1, x2)

        return rectangle, region_number

    def _update_data_with_patch(self, i, y1, y2, x1, x2):
        """
        update the data based on the bitmap of one patch
        """
        # find non-zero pixels and assign them
        nonzero = np.nonzero(self.patch_data[i])

        # compare the maximum of current data in patch location to the active region patch
        # set pixels equal to patch_data[i] only if non-zero and > current values in patch location
        # this stops overlapping patches being re-written with lower bit vaLUES
        mx = np.maximum(
            self._data.data[y1:y2, x1:x2][nonzero], self.patch_data[i][nonzero]
        )

        # updates the sun object.
        self._data.data[y1:y2, x1:x2][nonzero] = mx

    # def plot(self, ax):
    #     # Plot the active regions ("patches") on the sun for this instrument and date
    #     ax.set_title(f"{self.instrument} {self.date}")
    #     # Code to plot active regions on the sun for this instrument and date

    def plot(
        self,
        magnetogram_bg: bool = False,
        transparent: bool = True,
        return_plot_object: bool = False,
        outfile: str = None,
        dpi: int = 200,
        plot_axis: bool = False,
        figsize: tuple = (15, 15),
    ) -> None:
        """
        method for plotting the Sun and the SHARP/SMARP regions

        Parameters
        ----------

        magnetogram_bg : Optional[bool]
            ``False`` by default

        ...

        ...

        ...
        """

        fig, ax = plt.subplots(1, 1, figsize=figsize)

        if not plot_axis:
            plt.axis("off")

        ticks = np.array(list(dv.BITMAP_DICT.keys()))
        bounds = (
            [0] + list(ticks[:-1] + (ticks[1:] - ticks[:-1]) / 2) + [ticks[-1]]
        )
        norm = BoundaryNorm(bounds, dv.SOLARPATCH_CMAP.N)

        # Go through the bounding boxes and plot
        for rectangle, label in self.bbox:
            """plot the rectanges and associated text"""
            ax.add_patch(rectangle)
            plt.text(
                rectangle.get_x(),
                rectangle.get_y() + rectangle.get_height() + 20,
                label,
            )  # backgroundcolor=colors[0], fontsize=6)

        # plot the image
        _ = plt.imshow(
            self._data.data, origin="lower", cmap=dv.SOLARPATCH_CMAP, norm=norm
        )  # cmap='tab10', norm=colors.Normalize(vmin=0, vmax=34), interpolation='nearest')

        # plot the legend
        legend = plt.legend(
            [
                ptc.Patch(color=dv.SOLARPATCH_CMAP(norm(b)))
                for b in reversed(bounds[:-1])
            ],
            [f"{v}" for k, v in reversed(dv.BITMAP_DICT.items())],
            edgecolor="black",
        )
        legend.get_frame().set_linewidth(1.25)

        # display the observation date, and series
        text_plotting(
            obs_date=self._observation_date,
            series_name="HARPNUM",
            img_size=self._data.data.shape[0],
            streamlit=True,
        )

        # urgh, this is stupid
        plt.text(
            self._keys["CRPIX2"][0],
            self._keys["CRPIX1"][0] + (self._data.data.shape[0] / 2),
            "S O U T H",
            horizontalalignment="center",
        )

        plt.show()
