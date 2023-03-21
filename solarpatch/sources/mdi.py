import datetime
from typing import Dict

import matplotlib.pyplot as plt

from solarpatch.sources.data_base import GenericDataSource


class HMISolarPatch(GenericDataSource):
    instrument = "HMI"

    @classmethod
    def datasource(cls, instrument: str, meta: Dict) -> bool:
        """
        Determines if ``instrument`` should lead to the instantiation
        of this child class
        """

        # probably want to do on obs_date
        return instrument.lower() == "hmi"


class MDISolarPatch(GenericDataSource):
    instrument = "MDI"

    # probably want to do on obs_date
    @classmethod
    def datasource(cls, instrument: str, meta: Dict) -> bool:
        """
        Determines if ``instrument`` should lead to the instantiation
        of this child class
        """
        return instrument.lower() == "mdi"
