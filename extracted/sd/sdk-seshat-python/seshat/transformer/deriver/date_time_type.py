import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.transformer.deriver.base import SFrameDeriver


class DateTimeTypeDeriver(SFrameDeriver):
    """
    DateTime Type Deriver will change the type of an object column to a datetime column.
    """

    def __init__(self, group_keys=None, columns=None):
        super().__init__(group_keys)

        self.columns = columns

    def derive_df(self, default: DataFrame, *args, **kwargs):
        if self.columns is not None:
            for column in self.columns:
                default[column] = pd.to_datetime(default[column])

        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
