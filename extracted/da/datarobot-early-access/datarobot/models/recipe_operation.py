#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import trafaret as t
from typing_extensions import TypedDict

from datarobot.enums import (
    CategoricalStatsMethods,
    DatetimeSamplingStrategy,
    DownsamplingOperations,
    enum_to_list,
    FilterOperationFunctions,
    NumericStatsMethods,
    SamplingOperations,
    WranglingOperations,
)
from datarobot.models.api_object import APIObject


class BaseOperation(APIObject):
    """Single base transformation unit in Data Wrangler recipe."""

    def __init__(self, directive: str, arguments: Any):
        self.directive = directive
        self.arguments = arguments


class WranglingOperation(BaseOperation):
    _converter = t.Dict(
        {
            t.Key("directive"): t.Enum(*enum_to_list(WranglingOperations)),
            t.Key("arguments"): t.Mapping(t.String(), t.Any()),
        }
    ).allow_extra("*")


class DownsamplingOperation(BaseOperation):
    _converter = t.Dict(
        {
            t.Key("directive"): t.Enum(*enum_to_list(DownsamplingOperations)),
            t.Key("arguments"): t.Mapping(t.String(), t.Any()),
        }
    ).allow_extra("*")


class SamplingOperation(BaseOperation):
    _converter = t.Dict(
        {
            t.Key("directive"): t.Enum(*enum_to_list(SamplingOperations)),
            t.Key("arguments"): t.Mapping(t.String(), t.Any()),
        }
    ).allow_extra("*")


class BaseTimeAwareTask(APIObject):
    def __init__(self, name: str, arguments: Dict[str, Any]):
        self.name = name
        self.arguments = arguments


class TaskPlanElement(APIObject):
    def __init__(self, column: str, task_list: List[BaseTimeAwareTask]):
        self.column = column
        self.task_list = task_list


class CategoricalStats(BaseTimeAwareTask):
    def __init__(self, methods: List[CategoricalStatsMethods], window_size: int):
        super().__init__("categorical-stats", {"window_size": window_size, "methods": methods})


class NumericStats(BaseTimeAwareTask):
    def __init__(self, methods: List[NumericStatsMethods], window_size: int):
        super().__init__("numeric-stats", {"window_size": window_size, "methods": methods})


class Lags(BaseTimeAwareTask):
    def __init__(self, orders: List[int]):
        super().__init__("lags", {"orders": orders})


class LagsOperation(WranglingOperation):
    """
    Generate lags in a window.
    """

    def __init__(
        self,
        column: str,
        orders: List[int],
        datetime_partition_column: str,
        multiseries_id_column: Optional[str] = None,
    ):
        super().__init__(
            directive=WranglingOperations.LAGS,
            arguments={
                "column": column,
                "orders": orders,
                "datetime_partition_column": datetime_partition_column,
                "multiseries_id_column": multiseries_id_column,
            },
        )


class WindowCategoricalStatsOperation(WranglingOperation):
    """
    Generate rolling statistics in a window for categorical features.
    """

    def __init__(
        self,
        column: str,
        window_size: int,
        methods: List[CategoricalStatsMethods],
        datetime_partition_column: str,
        multiseries_id_column: Optional[str] = None,
        rolling_most_frequent_udf: Optional[str] = None,
    ):
        super().__init__(
            directive=WranglingOperations.WINDOW_CATEGORICAL_STATS,
            arguments={
                "column": column,
                "window_size": window_size,
                "methods": methods,
                "datetime_partition_column": datetime_partition_column,
                "multiseries_id_column": multiseries_id_column,
                "rolling_most_frequent_user_defined_function": rolling_most_frequent_udf,
            },
        )


class WindowNumericStatsOperation(WranglingOperation):
    """Generate various rolling numeric statistics in a window. Output could be a several columns."""

    def __init__(
        self,
        column: str,
        window_size: int,
        methods: List[NumericStatsMethods],
        datetime_partition_column: str,
        multiseries_id_column: Optional[str] = None,
        rolling_median_udf: Optional[str] = None,
    ):
        super().__init__(
            directive=WranglingOperations.WINDOW_NUMERIC_STATS,
            arguments={
                "column": column,
                "window_size": window_size,
                "methods": methods,
                "datetime_partition_column": datetime_partition_column,
                "multiseries_id_column": multiseries_id_column,
                "rolling_median_user_defined_function": rolling_median_udf,
            },
        )


class TimeSeriesOperation(WranglingOperation):
    """Operation to generate a dataset ready for time series modeling: with forecast point, forecast distances,
    known in advance columns, etc.
    """

    def __init__(
        self,
        target_column: str,
        datetime_partition_column: str,
        forecast_distances: List[int],
        task_plan: List[TaskPlanElement],
        baseline_periods: Optional[List[int]] = None,
        known_in_advance_columns: Optional[List[str]] = None,
        multiseries_id_column: Optional[str] = None,
        rolling_median_udf: Optional[str] = None,
        rolling_most_frequent_udf: Optional[str] = None,
        forecast_point: Optional[datetime] = None,
    ):
        """

        Parameters
        ----------
        target_column
        datetime_partition_column
        forecast_distances
        task_plan:
            contains a task list for each column
        baseline_periods:
            generates naive features from the target. For example: baseline period = 1 corresponds to the naive
            latest baseline.
        known_in_advance_columns
        multiseries_id_column
        rolling_median_udf:
            Fully qualified path to rolling median user defined function. Used to optimize sql execution with snowflake.
        rolling_most_frequent_udf:
            Fully qualified path to rolling most frequent user defined function.
        forecast_point:
             To use at prediction time.
        """
        arguments = {
            "target_column": target_column,
            "datetime_partition_column": datetime_partition_column,
            "forecast_distances": forecast_distances,
            "task_plan": task_plan,
            "multiseries_id_column": multiseries_id_column,
            "known_in_advance_columns": known_in_advance_columns,
            "baseline_periods": baseline_periods,
            "rolling_median_user_defined_function": rolling_median_udf,
            "rolling_most_frequent_user_defined_function": rolling_most_frequent_udf,
            "forecast_point": forecast_point,
        }
        super().__init__(directive=WranglingOperations.TIME_SERIES, arguments=arguments)


class ComputeNewOperation(WranglingOperation):
    def __init__(self, expression: str, new_feature_name: str):
        super().__init__(
            directive=WranglingOperations.COMPUTE_NEW,
            arguments={"expression": expression, "new_feature_name": new_feature_name},
        )


class RenameColumnsOperation(WranglingOperation):
    def __init__(self, column_mappings: Dict[str, str]):
        """
        column_mapping: dict, where
            key:  str
                Original name
            value: str
                New name
        """
        super().__init__(
            directive=WranglingOperations.RENAME_COLUMNS,
            arguments={
                "column_mappings": [
                    {"original_name": k, "new_name": v} for k, v in column_mappings.items()
                ]
            },
        )


class FilterCondition(TypedDict):
    column: str
    function: FilterOperationFunctions
    function_arguments: List[Union[str, int, float]]


class FilterOperation(WranglingOperation):
    """Filter rows."""

    def __init__(
        self,
        conditions: List[FilterCondition],
        keep_rows: Optional[bool] = True,
        operator: Optional[str] = "and",
    ):
        """
        keep_rows: bool
            If matching rows should be kept or dropped
        operator: str
            "and" or "or"
        conditions: list of FilterCondition

        """
        super().__init__(
            directive=WranglingOperations.FILTER,
            arguments={"keep_rows": keep_rows, "operator": operator, "conditions": conditions},
        )


class DropColumnsOperation(WranglingOperation):
    def __init__(self, columns: List[str]):
        """
        columns:
            Columns to delete
        """
        super().__init__(
            directive=WranglingOperations.DROP_COLUMNS,
            arguments={"columns": columns},
        )


class RandomSamplingOperation(SamplingOperation):
    def __init__(self, rows: int, seed: Optional[int] = None):
        super().__init__(
            directive=SamplingOperations.RANDOM_SAMPLE,
            arguments={"rows": rows, "seed": seed},
        )


class DatetimeSamplingOperation(SamplingOperation):
    def __init__(
        self,
        datetime_partition_column: str,
        rows: int,
        strategy: Optional[Union[str, DatetimeSamplingStrategy]] = None,
        multiseries_id_column: Optional[str] = None,
        selected_series: Optional[List[str]] = None,
    ):
        super().__init__(
            directive=SamplingOperations.DATETIME_SAMPLE,
            arguments={
                "rows": rows,
                "strategy": strategy,
                "datetime_partition_column": datetime_partition_column,
                "multiseries_id_column": multiseries_id_column,
                "selected_series": selected_series,
            },
        )
