import numpy as np

from solarpatch.sun.generic_sun import GenericSun


class RealSun(GenericSun):
    def __init__(self):
        pass

    def is_real(self):
        return True
