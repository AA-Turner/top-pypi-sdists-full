from typing import List, Tuple

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F, Window

from seshat.data_class import SFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.deriver.base import SFrameDeriver


class ShiftDeriver(SFrameDeriver):
    """
    Derives new columns by applying shifts to a specified column, grouped by given keys.

    Parameters
    ----------
    sort_on : List[str]
        Columns to sort on before applying shifts
    shifts : List[Tuple[str, int]]
        List of (label, shift_value) pairs defining each shift operation
    col : str
        Column to shift values from
    group_by : str | List[str]
        Column(s) to group by when applying shifts
    ascending : bool, default True
        Sort order direction
    """

    def __init__(
        self,
        sort_on: List[str],
        shifts: List[Tuple[str, int]],
        col: str,
        group_by: str | List[str],
        ascending: bool = True,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.sort_on = sort_on
        self.ascending = ascending
        self.shifts = shifts
        self.col = col
        if isinstance(group_by, str):
            group_by = [group_by]
        self.group_by = group_by

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, self.col)
        self._validate_columns(sf, self.default_sf_key, *self.group_by)

    def derive_df(self, default: DataFrame, *args, **kwargs):
        default = default.sort_values(
            by=self.sort_on, ascending=self.ascending
        ).reset_index(drop=True)

        for label, shift in self.shifts:
            default[f"{self.col}_{label}"] = default.groupby(self.group_by)[
                self.col
            ].shift(shift)

        default = default.groupby(self.group_by)
        default = default.last()
        default = default.reset_index()

        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = default.orderBy(
            [
                F.col(c).asc() if self.ascending else F.col(c).desc()
                for c in self.sort_on
            ]
        )
        window_spec = Window.partitionBy(self.group_by).orderBy(
            [
                F.col(c).asc() if self.ascending else F.col(c).desc()
                for c in self.sort_on
            ]
        )
        for label, shift in self.shifts:
            if shift > 0:
                default = default.withColumn(
                    f"{self.col}_{label}",
                    F.lag(F.col(self.col), shift).over(window_spec),
                )
            elif shift < 0:
                default = default.withColumn(
                    f"{self.col}_{label}",
                    F.lead(F.col(self.col), abs(shift)).over(window_spec),
                )
            else:
                default = default.withColumn(f"{self.col}_{label}", F.col(self.col))

        if self.ascending:
            default = default.groupBy(self.group_by).agg(
                *[F.last(c).alias(c) for c in default.columns if c not in self.group_by]
            )
        else:
            default = default.groupBy(self.group_by).agg(
                *[F.last(c).alias(c) for c in default.columns if c not in self.group_by]
            )

        return {"default": default}


class ShiftDeriverStory(BaseTransformerStory):
    transformer = ShiftDeriver
    use_cases = [
        (
            "We have hourly transaction data and want to compare each token's price "
            "now to its price X hours ago."
        )
    ]
    logic_overview = (
        "Sort the input. For each value in `shifts`, shift the rows and label the "
        "new columns accordingly."
    )
    steps = [
        (
            "Sort the input in ascending or descending order based on the "
            "`ascending` parameter."
        ),
        (
            "For each (label, shift) pair, shift the input and add a column labeled "
            "accordingly."
        ),
        "Group the result by the `group_by` columns and return the result.",
    ]
    tags = ["deriver", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "ShiftDeriverDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
