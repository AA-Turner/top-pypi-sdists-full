from typing import List

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.trimmer import SFrameTrimmer


class DuplicateTrimmer(SFrameTrimmer):
    """
    This trimmer is used to remove duplicate rows from the data based on the given columns.

    Parameters
    ----------
    subset : list of str
        The list of column names to check for duplicates. If not provided, all columns are used.
    """

    def __init__(self, subset: List[str] = None, group_keys=None, *args, **kwargs):
        super().__init__(group_keys, *args, **kwargs)
        self.subset = subset

    def trim_df(self, default: DataFrame, *args, **kwargs):
        default = default.drop_duplicates(subset=self.subset)
        return {"default": default}

    def trim_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = default.dropDuplicates(subset=self.subset)
        return {"default": default}


class DuplicateTrimmerStory(BaseTransformerStory):
    transformer = DuplicateTrimmer
    use_cases = ["An SFrame contains duplicate rows that need to be removed."]
    logic_overview = (
        "Removes duplicate rows from the input SFrame. Duplicates are identified "
        "based on a specified subset of columns. If no subset is provided, the "
        "entire row is used for comparison."
    )
    steps = [
        "If `subset` is None, consider all columns when identifying duplicates.",
        "Otherwise, identify duplicates based only on the specified `subset` of columns.",
        "Remove duplicate rows from the SFrame accordingly.",
    ]
    tags = ["trimmer", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "DuplicateTrimmerDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
