from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.transformer.trimmer import SFrameTrimmer


class ChangeColumnNameTrimmer(SFrameTrimmer):
    """
    Change Column Name Trimmer will change the name of columns.
    """

    def __init__(self, group_keys=None, columns_map=None):
        super().__init__(group_keys)

        self.columns_map = columns_map

    def trim_df(self, default: DataFrame, *args, **kwargs):
        if self.columns_map is not None:
            default = default.rename(columns=self.columns_map)

        return {"default": default}

    def trim_spf(self, default: PySparkDataFrame, *args, **kwargs):
        # ToDo: add spf
        return {"default": default}
