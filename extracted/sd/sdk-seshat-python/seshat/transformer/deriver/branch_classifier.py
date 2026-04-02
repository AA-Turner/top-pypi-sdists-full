from functools import reduce
from typing import List, Dict

import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver


class BranchClassifier(SFrameDeriver):
    """
    BranchClassifier takes an SFrame and generates multiple SFrames based on grouping by specified columns.

    Parameters
    ----------
    group_cols : list of str
        List of column names to group by. Each unique combination will create a separate SFrame.
    group_keys : dict, optional
        Dictionary mapping group names to their respective keys. If None, will auto-generate
        keys based on group column values.
    prefix : str, optional
        Prefix for auto-generated group keys. Defaults to "".
    keep_group_cols : bool, optional
        Whether to keep the group columns in each resulting SFrame. Defaults to False.
        When False, the group columns are removed from each grouped SFrame since they
        contain the same value for all rows in that group.
    keep_unhandled_sframes : bool, optional
        If True (default), any child SFrames of the input SFrame that are not handled by this classifier
        will be preserved in the output. If False, all unhandled child SFrames will be removed from the output,
        and only the newly generated grouped SFrames will be present.
    """

    ONLY_GROUP = False
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY}

    def __init__(
        self,
        group_cols: List[str],
        group_keys=None,
        prefix: str = "",
        keep_group_cols: bool = False,
        keep_unhandled_sframes: bool = True,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.group_cols = group_cols
        self.prefix = prefix
        self.keep_group_cols = keep_group_cols
        self.keep_unhandled_sframes = keep_unhandled_sframes

    def calculate_complexity(self):
        return len(self.group_cols)

    def execute(self, sf_input: SFrame, *args, **kwargs):
        result = self.call_handler(sf_input, *args, **kwargs)
        sf_output = sf_input.make_group(self.default_sf_key)
        if not self.keep_unhandled_sframes:
            sf_output.children.clear()

        self.set_raw(sf_output, result)
        return sf_output

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, *self.group_cols)

    def derive_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        result = {}

        # Group by columns and create separate DataFrames
        for group_values, group_df in default.groupby(self.group_cols):
            if not isinstance(group_values, tuple):
                group_values = (group_values,)

            group_key_parts = []
            for value in group_values:
                if pd.isna(value):
                    group_key_parts.append("null")
                else:
                    group_key_parts.append(str(value).replace(" ", "_"))

            group_key = self.prefix + "_".join(group_key_parts)

            clean_df = group_df.reset_index(drop=True)
            if not self.keep_group_cols:
                clean_df = clean_df.drop(columns=self.group_cols)

            result[group_key] = clean_df

        return result

    def derive_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        result = {}
        non_null_df = default.dropna(subset=self.group_cols)
        unique_groups = non_null_df.select(*self.group_cols).distinct().collect()

        for row in unique_groups:
            conditions = [F.col(col) == row[col] for col in self.group_cols]
            group_key = self.prefix + "_".join(
                str(row[col]).replace(" ", "_") for col in self.group_cols
            )

            group_df = default.filter(reduce(lambda a, b: a & b, conditions))
            if not self.keep_group_cols:
                group_df = group_df.drop(*self.group_cols)

            result[group_key] = group_df
        return result


class BranchClassifierStory(BaseTransformerStory):
    transformer = BranchClassifier
    use_cases = [
        "Split transaction data by category to analyze each category separately",
        "Group addresses by type and risk level for targeted processing",
        "Partition data based on multiple attributes for parallel analysis",
    ]
    logic_overview = (
        "Groups the default SFrame by specified columns and creates separate SFrames "
        "for each unique combination. Each group becomes a child SFrame with a key "
        "derived from the group values. Often used with Branch to apply different "
        "pipelines to each group."
    )
    steps = [
        "Validate that all specified group columns exist in the input",
        "Group the data by the specified columns",
        "For each group, generate a key from the group values",
        "Optionally remove group columns from each resulting SFrame",
        "Return a GroupSFrame with each group as a separate child",
    ]
    tags = ["deriver", "multi-sf-operation", "grouping"]

    def get_scenarios(self):
        from test.transformer.deriver.test_branch_classifier import (
            BranchClassifierDFTestCase,
        )

        return TransformerScenario.from_testcase(
            BranchClassifierDFTestCase, transformer=self.transformer
        )

    interactions = [
        (
            "Branch",
            "BranchClassifier splits data into groups, then Branch applies different pipelines to each group. "
            "The pipe_map keys in Branch must match the group keys generated by BranchClassifier. "
            "Use NestedKeyMerger after Branch to combine results. "
            "Common for processing data differently by timestamp ranges, categories, or other grouping criteria.",
        )
    ]
