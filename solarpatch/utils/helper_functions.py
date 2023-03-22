from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

import solarpatch.utils.default_variables as dv

__all__ = ["rotate_points"]


def rotate_points(points, origin=(0, 0), degrees: float = 180):
    """
    Rotate `points` around `origin` by `degrees`
    """
    # radian conversion
    angle = np.deg2rad(degrees)

    # 2D rotation matrix
    _ = np.array(
        [[np.cos(angle), np.sin(angle)], [-1.0 * np.sin(angle), np.cos(angle)]]
    )

    pass


def mdi_bitmap_to_hmi(patches):
    for p in patches:
        p[np.isin(p, [5, 9, 17])] = 101
        p[np.isin(p, [6, 10, 18])] = 102
        p[np.isin(p, [37, 41, 49])] = 133
        p[np.isin(p, [38, 42, 50])] = 134
        p -= 100

    return patches


def datetime_to_jsoc(dt: datetime):
    """
    jsoc string from datetime object
    """
    return dt.strftime(dv.JSOC_DATE_FORMAT)


def jsoc_to_datetime(date_string: str):
    """
    datetime object from jsoc string
    """
    return datetime.strptime(date_string, dv.JSOC_DATE_FORMAT)
