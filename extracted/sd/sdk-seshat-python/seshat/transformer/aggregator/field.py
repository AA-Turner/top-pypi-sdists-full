from typing import Dict, Tuple, Callable, Optional, List

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, functions as F

from seshat.data_class import SFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.aggregator import Aggregator


class FieldAggregator(Aggregator):
    """
    This class is used to perform aggregations on dataframes, supporting both grouped
    and global aggregations. When no group_by is specified, aggregations are added
    as new columns to all rows.

    Parameters
    ----------
    agg : dict
        Dictionary mapping result column names to aggregation specifications.
        Each value can be either:
        - A tuple of (source_column, aggregation_function) for standard aggregations
        - A callable function that takes a DataFrame and returns an aggregated value
    group_by : list of str, optional
        List of column names to group by. If None or empty, performs
        global aggregations across the entire dataset.
    """

    def __init__(
        self,
        agg: Dict[str, Tuple[str, str] | Callable],
        group_by: Optional[List[str]] = None,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.group_on = group_by or []
        self.agg = agg

    def calculate_complexity(self):
        return 10

    def validate(self, sf: SFrame):
        super().validate(sf)

        columns = []
        for _, agg_info in self.agg.items():
            if isinstance(agg_info, tuple):
                source_col, _ = agg_info
                columns.append(source_col)
        self._validate_columns(sf, self.default_sf_key, *columns)

    def aggregate_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        if self.group_on:
            to_agg_df = default.groupby(self.group_on)
            result_df = (
                default[self.group_on]
                .drop_duplicates()
                .sort_values(self.group_on)
                .reset_index(drop=True)
            )
        else:
            to_agg_df = default
            result_df = default

        # Find the aggregations
        for result_col, agg_info in self.agg.items():
            if isinstance(agg_info, tuple):
                source_col, agg_func = agg_info
                res = getattr(to_agg_df[source_col], agg_func)()
                if self.group_on:
                    res = res.values
                result_df[result_col] = res
            else:
                result_df[result_col] = (
                    to_agg_df.apply(agg_info).values
                    if self.group_on
                    else agg_info(default)
                )

        return {"default": result_df}

    def aggregate_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        if any(not isinstance(agg_info, tuple) for agg_info in self.agg.values()):
            return self._fallback_to_pandas(default, *args, **kwargs)

        spark_agg_funcs = {
            "first": F.first,
            "last": F.last,
            "sum": F.sum,
            "mean": F.avg,
            "avg": F.avg,
            "min": F.min,
            "max": F.max,
            "count": F.count,
            "std": F.stddev,
            "var": F.variance,
            "nunique": F.countDistinct,
        }

        # Prepare aggregations
        standard_aggs = []
        for result_col, agg_info in self.agg.items():
            if isinstance(agg_info, tuple) and len(agg_info) == 2:
                source_col, agg_func = agg_info
                if agg_func in spark_agg_funcs:
                    standard_aggs.append(
                        spark_agg_funcs[agg_func](source_col).alias(result_col)
                    )
                else:
                    return self._fallback_to_pandas(default, *args, **kwargs)
            else:
                return self._fallback_to_pandas(default, *args, **kwargs)

        if not self.group_on:
            if standard_aggs:
                agg_result = default.agg(*standard_aggs)
                agg_row = agg_result.collect()[0]

                result_df = default
                for result_col in self.agg.keys():
                    result_df = result_df.withColumn(
                        result_col, F.lit(agg_row[result_col])
                    )
            else:
                result_df = default
        else:
            if isinstance(self.group_on, str):
                group_cols = [self.group_on]
            else:
                group_cols = list(self.group_on)

            result_df = default.groupBy(*group_cols).agg(*standard_aggs)

            final_cols = group_cols + list(self.agg.keys())
            result_df = result_df.select(*final_cols)

        return {"default": result_df}

    def _fallback_to_pandas(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        pandas_df = default.toPandas()
        result_dict = self.aggregate_df(pandas_df, *args, **kwargs)
        spark = default.sparkSession
        result_df = spark.createDataFrame(
            result_dict[self.DEFAULT_GROUP_KEYS["default"]]
        )
        return {"default": result_df}


class FieldAggregatorStory(BaseTransformerStory):
    transformer = FieldAggregator
    use_cases = [
        "Aggregate data by one or more columns, computing sums, means, counts, or custom aggregations for each group.",
        "Summarize transaction or token data by grouping and applying standard or custom aggregation functions.",
    ]
    logic_overview = (
        "FieldAggregation groups the input data by specified columns and computes one or more aggregation functions "
        "(such as sum, mean, min, max, count, or user-defined functions) for each group. "
        "It supports both standard aggregations and custom Python callables, "
        "and works with both pandas and Spark backends."
    )
    steps = [
        "Initialize the transformer with a list of columns to group by and a dictionary of aggregations.",
        "Validate that all required columns exist in the input data.",
        "Group the data by the specified columns.",
        "For each aggregation, apply the function (standard or custom) to each group.",
        "Return a new SFrame with one row per group and the computed aggregation columns.",
    ]
    tags = ["aggregator", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.aggregator import TestFieldAggregator

        return TransformerScenario.from_testcase(
            TestFieldAggregator, transformer=self.transformer
        )

    find_outputs = False
