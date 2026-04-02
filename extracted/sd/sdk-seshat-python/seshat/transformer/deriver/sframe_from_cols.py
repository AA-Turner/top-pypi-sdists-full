from typing import Dict

import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.transformer.deriver.base import SFrameDeriver


class SFrameFromColsDeriver(SFrameDeriver):
    """
    This class is used to create new sframe from specific columns of default sframes.
    If input is contained only one sframe the result is group sframe with two children.

    Parameters
    ----------
    cols : list of str
        List of columns in the default sframe to transformation must apply of them.
    result_col : str
        Column name of result values in address sframe
    """

    ONLY_GROUP = False
    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "address": configs.ADDRESS_SF_KEY,
    }

    def __init__(
        self,
        group_keys=None,
        cols=(configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL),
        result_col="extracted_value",
    ):
        super().__init__(group_keys)
        self.cols = cols
        self.result_col = result_col

    def calculate_complexity(self):
        return 1

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, *self.cols)

    def derive_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        new_df = DataFrame()

        new_df[self.result_col] = pd.unique(default[[*self.cols]].values.ravel())
        new_df[self.result_col] = new_df[self.result_col].astype(
            default[self.cols[0]].dtype
        )
        new_df.dropna(subset=[self.result_col], inplace=True)
        return {"default": default, "address": new_df}

    def derive_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        temp_spf = default.withColumn(
            self.result_col, F.explode(F.array(*[F.col(c) for c in self.cols]))
        )
        address = temp_spf.select(self.result_col).distinct()
        return {"default": default, "address": address}
