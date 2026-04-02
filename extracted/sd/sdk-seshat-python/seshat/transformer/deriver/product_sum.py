from functools import reduce
from typing import List, Tuple

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.deriver.base import SFrameDeriver


class ProductSumDeriver(SFrameDeriver):
    """
    Calculates weighted sum of multiple columns and stores result in a new column.

    Parameters
    ----------
    feature_weights : List[Tuple[str, float | int]]
        List of (column_name, weight) pairs for weighted sum calculation
    result_col : str
        Name of the column to store the weighted sum result
    """

    def __init__(
        self,
        feature_weights: List[Tuple[str, float | int]],
        result_col: str,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.feature_weights = feature_weights
        self.result_col = result_col

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(
            sf, self.default_sf_key, *[c for c, _ in self.feature_weights]
        )

    def derive_df(self, default: DataFrame, *args, **kwargs):
        default[self.result_col] = sum(
            [weight * default[col] for col, weight in self.feature_weights]
        )
        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        weighted_cols = [
            F.lit(weight) * F.col(col_name) for col_name, weight in self.feature_weights
        ]
        default = default.withColumn(
            self.result_col, reduce(lambda x, y: x + y, weighted_cols)
        )
        return {"default": default}


class ProductSumDeriverStory(BaseTransformerStory):
    transformer = ProductSumDeriver
    use_cases = [
        (
            "Calculate a profitability score by computing a weighted sum of multiple "
            "features such as buy/sell volume ratio,"
        ),
        " trade count, and price change percentage with different weights.",
    ]
    logic_overview = (
        "For each row, compute a weighted sum of selected feature columns using "
        "the specified weights, and store the result in a new column defined by "
        "`result_col`."
    )
    steps = [
        "Validate that all feature columns exist in the input data.",
        "Multiply each feature column by its corresponding weight.",
        "Sum the weighted values row-wise.",
        "Store the result in a new column specified by `result_col`.",
    ]
    tags = ["deriver", "feature-engineering", "weighted-sum"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "ProductSumDeriverDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
