from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

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
