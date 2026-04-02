import pandas as pd
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.utils.validation import TimeStampColumnValidator


class ChangingOverTimeDeriver(SFrameDeriver):
    """
    Calculate the relative change in a value over time for each index group.

    This deriver computes the change between the first and last values of a
    specified column (value_col), ordered by a timestamp column, for each
    unique value in the index column. The relative change is calculated as
    (last - first) / first.

    The result is returned in a new SFrame under the "result" key, which
    contains only the index_col and the result_changing_col with the computed
    values.

    Parameters
    ----------
    index_col : str
        The column used to identify unique groups (e.g., an entity ID).
    value_col : str
        The column whose change over time is to be calculated.
    result_changing_col : str
        The name of the column to store the resulting change values.
    timestamp_col : str, optional
        The column used to order the values over time. Default is configs.BLOCK_TIMESTAMP_COL.
    group_keys : dict, optional
        Group keys for the parent Transformer class.
    """

    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY, "result": "result"}

    def __init__(
        self,
        index_col: str,
        value_col: str,
        result_changing_col: str,
        timestamp_col: str = configs.BLOCK_TIMESTAMP_COL,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.index_col = index_col
        self.value_col = value_col
        self.result_changing_col = result_changing_col
        self.timestamp_col = timestamp_col

    def calculate_complexity(self):
        return 15

    def derive_df(self, default: pd.DataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)

        sorted_default = default.sort_values(self.timestamp_col, ascending=False)
        sorted_default = sorted_default[
            [self.index_col, self.value_col, self.timestamp_col]
        ]
        last = (
            sorted_default.groupby(self.index_col)
            .first()
            .reset_index()
            .rename(columns={self.value_col: "last"})
        )
        sorted_default = sorted_default.sort_values(self.timestamp_col)
        first = (
            sorted_default.groupby(self.index_col)
            .first()
            .reset_index()
            .rename(columns={self.value_col: "first"})
        )

        result = pd.merge(last, first, on=self.index_col)
        result[self.result_changing_col] = (result["last"] - result["first"]) / result[
            "first"
        ]

        result = result[[self.index_col, self.result_changing_col]]

        result = result.dropna(subset=[self.result_changing_col])

        return {"default": default, "result": result}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)
        sorted_default = default.sort(F.desc(self.timestamp_col)).select(
            self.index_col, self.value_col, self.timestamp_col
        )
        last = sorted_default.groupBy(self.index_col).agg(
            F.first(self.value_col).alias("last")
        )
        sorted_default = default.orderBy(self.timestamp_col).select(
            self.index_col, self.value_col, self.timestamp_col
        )
        first = sorted_default.groupBy(self.index_col).agg(
            F.first(self.value_col).alias("first")
        )

        result = last.join(first, on=self.index_col)
        result = result.withColumn(
            self.result_changing_col,
            (F.col("last") - F.col("first")) / F.col("first"),
        )
        result = result.select(self.index_col, self.result_changing_col)

        result = result.dropna(subset=[self.result_changing_col])
        return {"default": default, "result": result}


class ChangingOverTimeDeriverStory(BaseTransformerStory):
    transformer = ChangingOverTimeDeriver
    use_cases = [
        "Find out that the price of token in specific period of time how much changes"
    ]
    logic_overview = (
        "Find the latest and first value for each `index_col` based on "
        "`timestamp_col`, then calculate (LAST - FIRST)/LAST for each one."
    )
    steps = [
        "Validate that `timestamp_col` is datetime column",
        "Sort items based on timestamp_col",
        "Group by `index_col`, find first and last for each one",
        "For each `index_col` values, calculate (LAST-FIRST)/LAST for each one.",
    ]
    tags = ["deriver", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.deriver.test_changing_over_time import (
            ChangingOverTimeDeriverDFTestCase,
        )

        return TransformerScenario.from_testcase(
            ChangingOverTimeDeriverDFTestCase, transformer=self.transformer
        )
