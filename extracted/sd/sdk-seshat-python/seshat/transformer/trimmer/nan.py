from typing import List

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.transformer.trimmer import SFrameTrimmer


class NaNTrimmer(SFrameTrimmer):
    """
    This trimmer is used to remove rows with NaN values based on the given columns.

    Parameters
    ----------
    subset : list of str
        The list of column names to check for NaN values. If not provided, all columns are used.
    how : str
        Determines if a row is dropped when all columns are NaN ("all") or any column is NaN ("any").
    """

    def __init__(
        self, subset: List[str] = None, group_keys=None, how="all", *args, **kwargs
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.subset = subset
        self.how = how

    def calculate_complexity(self):
        return 1

    def _get_existing_subset_cols(self, default):
        if self.subset is None:
            return None
        existing_cols = [col for col in self.subset if col in default.columns]
        return existing_cols if existing_cols else None

    def trim_df(self, default: DataFrame, *args, **kwargs):
        default = default.dropna(
            subset=self._get_existing_subset_cols(default), how=self.how
        )
        return {"default": default}

    def trim_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = default.dropna(
            subset=self._get_existing_subset_cols(default), how=self.how
        )
        return {"default": default}
