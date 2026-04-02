from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F, Window

from seshat.data_class import SFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.deriver.base import SFrameDeriver


class RankDeriver(SFrameDeriver):
    """
    Derives a new column with dense rank values based on specified column.

    Parameters
    ----------
    col : str
        Column to calculate ranks from
    result_col : str
        Column to store the calculated ranks
    ascending : bool, default False
        Whether to rank in ascending order
    """

    def __init__(
        self,
        col: str,
        result_col: str,
        ascending: bool = False,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.col = col
        self.result_col = result_col
        self.ascending = ascending

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, self.col)

    def derive_df(self, default: DataFrame, *args, **kwargs):
        default[self.result_col] = (
            default[self.col].rank(ascending=self.ascending, method="dense").astype(int)
        )
        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        orderby_col = F.col(self.col)
        orderby_col = orderby_col.asc() if self.ascending else orderby_col.desc()
        window = Window.orderBy(orderby_col)
        default = default.withColumn(self.result_col, F.dense_rank().over(window))
        return {"default": default}


class RankDeriverStory(BaseTransformerStory):
    transformer = RankDeriver
    use_cases = [
        (
            "Rank entities such as users, tokens, or products based on a numeric "
            "feature (e.g., price, volume, score)"
        )
    ]
    logic_overview = (
        "Apply dense ranking to a specified column. Dense rank assigns the same "
        "rank to identical values and does not skip ranks for ties. The result "
        "is stored in a new column."
    )
    steps = [
        "Validate that the input column used for ranking exists.",
        (
            "Apply dense ranking on the specified column, in ascending or descending "
            "order."
        ),
        "Store the resulting ranks in the `result_col` column.",
        "Return the updated DataFrame.",
    ]
    tags = ["deriver", "ranking", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "RankDeriverDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
