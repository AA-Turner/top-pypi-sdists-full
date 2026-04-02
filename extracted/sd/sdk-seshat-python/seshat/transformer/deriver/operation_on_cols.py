from typing import Callable

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.utils import pyspark_func
from seshat.utils.validation import NumericColumnValidator


class OperationOnColsDeriver(SFrameDeriver):
    """
    This deriver does some operation on two different columns of default sframe


    Parameters
    ----------
    cols: list of str
        List of column names that operation must be applied on them
    result_col: str
        Column name of result column
    agg_func: str
        Aggregation function name that operates on specified columns.

    """

    ONLY_GROUP = False
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY}

    def __init__(
        self,
        group_keys=None,
        cols=(configs.AMOUNT_COL,),
        result_col="interacted_value",
        agg_func: str | Callable = "mean",
        is_numeric=False,
    ):
        super().__init__(group_keys)
        self.cols = cols
        self.result_col = result_col
        self.agg_func = agg_func
        self.is_numeric = is_numeric

    def calculate_complexity(self):
        return 15

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, *self.cols)

    def derive_df(self, default: DataFrame, *args, **kwargs):
        if self.is_numeric:
            for col in self.cols:
                default = NumericColumnValidator().validate(default, col)
        if isinstance(self.agg_func, str):
            default[self.result_col] = default[[col for col in self.cols]].agg(
                self.agg_func, axis=1
            )
        else:
            default[self.result_col] = default[self.cols].apply(self.agg_func, axis=1)

        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        if self.is_numeric:
            for col in self.cols:
                default = NumericColumnValidator().validate(default, col)
        if isinstance(self.agg_func, str):
            try:
                func = pyspark_func.func_maps[self.agg_func]
            except KeyError:
                raise KeyError(
                    "func %s not available for pyspark dataframe" % self.agg_func
                )
        else:
            func = self.agg_func
        func_udf = F.udf(func)
        default = default.withColumn(
            self.result_col, func_udf(*[F.col(col) for col in self.cols])
        )
        if self.is_numeric:
            default = NumericColumnValidator().validate(default, self.result_col)
        return {"default": default}


class OperationOnColsDeriverStory(BaseTransformerStory):
    transformer = OperationOnColsDeriver
    tags = ["deriver", "single-sf-operation"]
    outputs = [
        "default sframe with new column `result_col` containing aggregated result"
    ]
    use_cases = [
        "Compute total on-chain volume per address by summing `sent_amount` and `received_amount`.",
        "Generate an average metric from two numeric features, e.g. `(score_1 + score_2) / 2`.",
        "Apply custom set operations on token arrays via a lambda: `lambda x: set(x[0]) | set(x[1])` to "
        "get all interacted tokens.",
    ]
    logic_overview = (
        "Combines two or more columns into a single feature by applying a specified operation to "
        "the values that appear in the same row."
    )
    steps = [
        "Confirm that every listed column exists in the default SFrame and, if `is_numeric` is enabled, contains "
        "values that can be interpreted as numbers.",
        (
            "Choose the aggregation rule: a recognised keyword such as 'sum', 'mean', "
            "'max', or any user‑supplied callable that accepts all selected columns "
            "for one row and returns a single value."
        ),
        "For each row, feed the current values from the selected columns into the aggregation rule to obtain "
        "one consolidated result.",
        (
            "Store that result in the column named by `result_col`, thereby enriching "
            "the default SFrame with a new derived feature."
        ),
        "Return the updated SFrame so subsequent transformers or models can make use of the freshly created column.",
    ]

    def get_scenarios(self):
        from test.transformer.deriver.test_operation_on_numeric_cols import (
            OperationOnNumericColsDFTestCase,
        )

        return TransformerScenario.from_testcase(
            OperationOnNumericColsDFTestCase, transformer=self.transformer
        )
