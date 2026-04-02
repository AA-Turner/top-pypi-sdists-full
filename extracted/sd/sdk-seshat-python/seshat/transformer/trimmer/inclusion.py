from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.trimmer import SFrameTrimmer


class InclusionTrimmer(SFrameTrimmer):
    """
    This trimmer is used to drop rows from the default SFrame based on their presence in the other SFrame.
    If a value in the default column exists in the other column, the row will be removed.
    If `exclude` is False, only matching rows will be kept instead.

    Parameters
    ----------
    default_col : str
        The column name in the default SFrame to compare.
    other_col : str
        The column name in the other SFrame to compare.
    exclude : bool
        If True, remove matching rows from default. If False, keep only matching rows.
    """

    ONLY_GROUP = True
    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "other": configs.OTHER_SF_KEY,
    }

    def __init__(
        self,
        default_col: str = configs.CONTRACT_ADDRESS_COL,
        other_col: str = configs.CONTRACT_ADDRESS_COL,
        exclude: bool = True,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.default_col = default_col
        self.other_col = other_col
        self.exclude = exclude

    def calculate_complexity(self):
        return 1

    def trim_df(self, default: DataFrame, other: DataFrame, *args, **kwargs):
        condition = default[self.default_col].isin(other[self.other_col])
        if self.exclude:
            condition = ~condition
        default = default[condition]
        default = default.reset_index(drop=True)
        return {"default": default, "other": other}

    def trim_spf(
        self, default: PySparkDataFrame, other: PySparkDataFrame, *args, **kwargs
    ):
        values = [
            row[self.other_col]
            for row in other.select(self.other_col).distinct().collect()
        ]
        condition = F.col(self.default_col).isin(values)
        if self.exclude:
            condition = ~condition

        default = default.filter(condition)
        return {"default": default, "other": other}


class InclusionTrimmerStory(BaseTransformerStory):
    transformer = InclusionTrimmer
    use_cases = [
        "We have two sframe one contains tokens that are not popular and another contains transactions data, by using "
        "this trimmer just those tokens remain in transactions data"
    ]
    logic_overview = (
        "Keep or remove rows from the default SFrame based on whether the values in "
        "default_col also exist in other_col of the other SFrame"
    )
    steps = [
        "Extract the set of values from `other_col` in the other SFrame.",
        "Check each row in the default SFrame against this set using the `default_col`.",
        "If `exclude` is False, keep only the rows where `default_col` exists in `other_col`.",
        "If `exclude` is True, remove those rows (i.e., keep only the rows where `default_col` "
        "does not exist in `other_col`).",
    ]
    tags = ["trimmer", "multi-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "InclusionTrimmerDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
