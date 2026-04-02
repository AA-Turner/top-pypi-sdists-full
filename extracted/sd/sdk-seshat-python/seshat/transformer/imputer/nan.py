from typing import List, Dict

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.data_class import SFrame
from seshat.general.transformer_story.base import (
    TransformerScenario,
    BaseTransformerStory,
)
from seshat.transformer.imputer import SFrameImputer
from seshat.utils import pandas_func, pyspark_func


class NaNImputer(SFrameImputer):
    """
    A transformer that replaces NaN values in specified columns with a specific value.

    Parameters
    ----------
    cols : list of str, optional
        Columns that should be imputed. If None, all columns will be considered.
    value : any, optional
        The value to impute. If None, a default zero-like value based on the column's data type will be used.
    """

    def __init__(
        self, cols: List[str] = None, value=None, group_keys=None, *args, **kwargs
    ):
        super().__init__(group_keys)

        self.cols = cols
        self.value = value

    def validate(self, sf: SFrame):
        super().validate(sf)
        if self.cols:
            self._validate_columns(sf, self.default_sf_key, *self.cols)

    def impute_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        for col in self.cols or default.columns.tolist():
            value = (
                self.value
                if self.value is not None
                else pandas_func.get_zero_value(default[col])
            )
            default = default.fillna({col: value})
        return {"default": default}

    def impute_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        cols_to_impute = self.cols or default.columns
        fill_dict = {}
        for col in cols_to_impute:
            value = (
                self.value
                if self.value is not None
                else pyspark_func.get_zero_value(default, col)
            )
            fill_dict[col] = value
        default = default.fillna(fill_dict)
        return {"default": default}


class NaNImputerStory(BaseTransformerStory):
    transformer = NaNImputer
    use_cases = [
        "To fill missing (NaN) values in specified columns of an SFrame.",
        "To replace NaN values with a fixed value (e.g., 0, empty string).",
        "To replace NaN values with statistical measures like mean, median, or mode.",
    ]
    logic_overview = (
        "Replaces NaN values in specified columns of an SFrame using either a fixed value "
        "or a statistical strategy (mean, median, mode)."
    )
    steps = [
        (
            "Identify columns with NaN values to be imputed (either specified by `cols` "
            "or all numeric columns if `cols` is None)."
        ),
        "If a `value` is provided, fill NaN values in the target columns with this value.",
        (
            "If a `strategy` ('mean', 'median', 'mode') is provided, calculate the respective "
            "statistic for each target column and fill NaN values with it."
        ),
        "Ensure that only one of `value` or `strategy` is specified during initialization.",
    ]
    tags = ["imputer", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.imputer.test_nan_imputer import NaNImputerDFTestCase

        return TransformerScenario.from_testcase(
            NaNImputerDFTestCase, transformer=self.transformer
        )
