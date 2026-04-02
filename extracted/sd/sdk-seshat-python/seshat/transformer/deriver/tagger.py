from typing import List, Tuple, Dict

import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver
from seshat.transformer.trimmer import FilterTrimmer


class Tagger(SFrameDeriver):
    """
    This class is used to apply multiple filters to data and attach labels to rows
    that pass each filter. A row can have multiple labels if it passes multiple filters.

    Parameters
    ----------
    filters_and_labels : list of tuple
        List of tuples containing (FilterTrimmer, label) pairs. Each FilterTrimmer
        will be applied and rows that pass the filter will get the corresponding label.
    result_col : str, default "labels"
        Name of the column to store the list of labels for each row.
    """

    def __init__(
        self,
        filters_and_labels: List[Tuple[FilterTrimmer, str]],
        result_col: str = "labels",
        group_keys=None,
    ):
        super().__init__(group_keys)
        self.filters_and_labels = filters_and_labels
        self.result_col = result_col

    def calculate_complexity(self):
        return len(self.filters_and_labels) * 5

    def validate(self, sf: SFrame):
        super().validate(sf)
        # Validate that all filters can work with the input data
        for filter_trimmer, _ in self.filters_and_labels:
            filter_trimmer.validate(sf)

    def derive_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        results = []
        for filter_trimmer, label in self.filters_and_labels:
            trimmed_result = filter_trimmer.trim_df(default, *args, **kwargs)
            res = trimmed_result["default"].copy()
            res.loc[:, self.result_col] = label
            results.append(res)

        result = pd.concat(results)

        without_label = result[
            [col for col in result.columns if col != self.result_col]
        ]
        unlabeled = pd.concat([default, without_label]).drop_duplicates(keep=False)

        result = pd.concat([result, unlabeled])

        return {"default": result}

    def derive_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        results = []

        for filter_trimmer, label in self.filters_and_labels:
            filtered_result = filter_trimmer.trim_spf(default, *args, **kwargs)
            res = filtered_result["default"]

            res = res.withColumn(self.result_col, F.lit(label))
            results.append(res)

        if results:
            result = results[0]
            for df in results[1:]:
                result = result.union(df)
        else:
            result = default.withColumn(self.result_col, F.lit(None).cast("string"))

        # Find unlabeled rows
        other_columns = [col for col in default.columns if col != self.result_col]
        without_label = result.select(*other_columns)
        unlabeled = default.join(without_label, on=other_columns, how="left_anti")
        unlabeled = unlabeled.withColumn(self.result_col, F.lit(None).cast("string"))
        final_result = result.union(unlabeled)

        return {"default": final_result}


class TaggerStory(BaseTransformerStory):
    transformer = Tagger
    use_cases = [
        "Label transactions based on multiple criteria such as value thresholds",
        "Tag addresses with risk indicators using different filters",
        "Apply multiple classification rules to data simultaneously",
    ]
    logic_overview = (
        "Applies multiple filters to the data and attaches labels to rows that pass "
        "each filter. Rows can receive multiple labels if they match multiple filters."
    )
    steps = [
        "Validate that all filters can work with the input data",
        "For each filter, apply it and collect matching rows",
        "Attach the corresponding label to each set of matching rows",
        "Combine all labeled rows and preserve unlabeled rows",
        "Return the data with a new labels column",
    ]
    tags = ["deriver", "single-sf-operation", "labeling"]

    def get_scenarios(self):
        from test.transformer.deriver import TaggerDFTestCase

        return TransformerScenario.from_testcase(
            TaggerDFTestCase, transformer=self.transformer
        )
