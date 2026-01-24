#
# Copyright 2023-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import trafaret as t
from typing_extensions import TypedDict

from datarobot.enums import (
    AggregationFunctions,
    CategoricalStatsMethods,
    DatetimeSamplingStrategy,
    DownsamplingOperations,
    FilterOperationFunctions,
    FindAndReplaceMatchMode,
    JoinSourceType,
    JoinType,
    NumericStatsMethods,
    SamplingOperations,
    SmartDownsamplingMethod,
    WranglingOperations,
    enum_to_list,
)
from datarobot.models.api_object import APIObject
from datarobot.models.dataset import Dataset


class BaseOperation(APIObject):
    """Single base transformation unit in Data Wrangler recipe."""

    def __init__(self, directive: str, arguments: Any):
        self.directive = directive
        self.arguments = arguments


class WranglingOperation(BaseOperation):
    """Base class for data wrangling operations."""

    _converter = t.Dict({
        t.Key("directive"): t.Enum(*enum_to_list(WranglingOperations)),
        t.Key("arguments"): t.Mapping(t.String(), t.Any()),
    }).allow_extra("*")


class DownsamplingOperation(BaseOperation):
    """Base class for downsampling operations."""

    _converter = t.Dict({
        t.Key("directive"): t.Enum(*enum_to_list(DownsamplingOperations)),
        t.Key("arguments"): t.Mapping(t.String(), t.Any()),
    }).allow_extra("*")


class SamplingOperation(BaseOperation):
    """Base class for sampling operations."""

    _converter = t.Dict({
        t.Key("directive"): t.Enum(*enum_to_list(SamplingOperations)),
        t.Key("arguments"): t.Mapping(t.String(), t.Any()),
    }).allow_extra("*")


class BaseTimeAwareTask(APIObject):
    """Base class for time-aware tasks in time series operation task plan."""

    def __init__(self, name: str, arguments: Dict[str, Any]):
        self.name = name
        self.arguments = arguments


class TaskPlanElement(APIObject):
    """
    Represents a task plan element for a specific column in a time series operation.

    Parameters
    ----------
    column:
        Column name for which the task plan is defined.
    task_list:
        List of time-aware tasks to be applied to the column.
    """

    def __init__(self, column: str, task_list: List[BaseTimeAwareTask]):
        self.column = column
        self.task_list = task_list


class CategoricalStats(BaseTimeAwareTask):
    """
    Time-aware task to compute categorical statistics for a rolling window.

    Parameters
    ----------
    methods:
        List of categorical statistical methods to apply for rolling statistics.
    window_size:
        Number of rows to include in the rolling window.
    """

    def __init__(self, methods: List[CategoricalStatsMethods], window_size: int):
        super().__init__("categorical-stats", {"window_size": window_size, "methods": methods})


class NumericStats(BaseTimeAwareTask):
    """
    Time-aware task to compute numeric statistics for a rolling window.

    Parameters
    ----------
    methods:
        List of numeric statistical methods to apply for rolling statistics.
    window_size:
        Number of rows to include in the rolling window.
    """

    def __init__(self, methods: List[NumericStatsMethods], window_size: int):
        super().__init__("numeric-stats", {"window_size": window_size, "methods": methods})


class Lags(BaseTimeAwareTask):
    """
    Time-aware task to create one or more lags for a feature.

    Parameters
    ----------
    orders:
        List of lag orders to create.
    """

    def __init__(self, orders: List[int]):
        super().__init__("lags", {"orders": orders})


class LagsOperation(WranglingOperation):
    """
    Data wrangling operation to create one or more lags for a feature based off of a datetime ordering feature.
    This operation will create a new column for each lag order specified.

    Parameters
    ----------
    column:
        Column name to create lags for.
    orders:
        List of lag orders to create.
    datetime_partition_column:
        Column name used to partition the data by datetime. Used to order the data for lag creation.
    multiseries_id_column:
        Column name used to identify time series within the data. Required only for multiseries.

    Examples
    --------
    Create lags of orders 1, 5 and 30 in stock price data on opening price column "open_price", ordered by datetime
    column "date". The data contains multiple time series identified by "ticker_symbol":

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import LagsOperation
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> lags_op = LagsOperation(
        ...     column="open_price",
        ...     orders=[1, 5, 30],
        ...     datetime_partition_column="date",
        ...     multiseries_id_column="ticker_symbol",
        ... )
        >>> recipe.update(operations=[lags_op])
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
    Data wrangling operation to calculate categorical statistics for a rolling window. This operation
    will create a new column for each method specified.

    Parameters
    ----------
    column:
        Column name to create rolling statistics for.
    window_size:
        Number of rows to include in the rolling window.
    methods:
        List of methods to apply for rolling statistics. Currently only supports
        `datarobot.enums.CategoricalStatsMethods.MOST_FREQUENT`.
    datetime_partition_column:
        Column name used to partition the data by datetime. Used to order the timeseries data.
    multiseries_id_column:
        Column name used to identify each time series within the data. Required only for multiseries.
    rolling_most_frequent_udf:
        Fully qualified path to rolling most frequent user defined function. Used to optimize sql execution with
        snowflake.

    Examples
    --------
    Create rolling categorical statistics to track the most frequent product category purchased by customers based on
    their last 50 purchases:

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import WindowCategoricalStatsOperation
        >>> from datarobot.enums import CategoricalStatsMethods
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> window_cat_stats_op = WindowCategoricalStatsOperation(
        ...     column="product_category",
        ...     window_size=50,
        ...     methods=[CategoricalStatsMethods.MOST_FREQUENT],
        ...     datetime_partition_column="purchase_date",
        ...     multiseries_id_column="customer_id",
        ... )
        >>> recipe.update(operations=[window_cat_stats_op])
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
    """
    Data wrangling operation to calculate numeric statistics for a rolling window. This operation will create one
    or more new columns.

    Parameters
    ----------
    column:
        Column name to create rolling statistics for.
    window_size:
        Number of rows to include in the rolling window.
    methods:
        List of methods to apply for rolling statistics. A new column will be created for each method.
    datetime_partition_column:
        Column name used to partition the data by datetime. Used to order the timeseries data.
    multiseries_id_column:
        Column name used to identify each time series within the data. Required only for multiseries.
    rolling_median_udf:
        Fully qualified path to a rolling median user-defined function. Used to optimize SQL execution with Snowflake.

    Examples
    --------
    Create rolling numeric statistics to track the maximum, minimum, and median stock prices over the last 7 trading
    sessions:

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import WindowNumericStatsOperation
        >>> from datarobot.enums import NumericStatsMethods
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> window_num_stats_op = WindowNumericStatsOperation(
        ...     column="stock_price",
        ...     window_size=7,
        ...     methods=[
        ...         NumericStatsMethods.MAX,
        ...         NumericStatsMethods.MIN,
        ...         NumericStatsMethods.MEDIAN,
        ...     ],
        ...     datetime_partition_column="trading_date",
        ...     multiseries_id_column="ticker_symbol",
        ... )
        >>> recipe.update(operations=[window_num_stats_op])
    """

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
    """
    Data wrangling operation to generate a dataset ready for time series modeling: with forecast point, forecast
    distances, known in advance columns, etc.

    Parameters
    ----------
    target_column:
        Target column to use for generating naive baseline features during feature reduction.
    datetime_partition_column:
        Column name used to partition the data by datetime. Used to order the time series data.
    forecast_distances:
        List of forecast distances to generate features for. Each distance represents a relative position that
        determines how many rows ahead to predict.
    task_plan:
        List of task plans for each column.
    baseline_periods:
        List of integers representing the periodicities used to generate naive baseline features from the target.
        Baseline period = 1 corresponds to the naive latest baseline.
    known_in_advance_columns:
        List of columns that are known in advance at prediction time, i.e. features that do not need to be lagged.
    multiseries_id_column:
        Column name used to identify each time series within the data. Required only for multiseries.
    rolling_median_udf:
        Fully qualified path to rolling median user defined function. Used to optimize SQL execution with Snowflake.
    rolling_most_frequent_udf:
        Fully qualified path to rolling most frequent user defined function.
    forecast_point:
        To use at prediction time.

    Examples
    --------
    Create a time series operation for sales forecasting with forecast distances of 7 and 30 days, using the sale amount
    as the target column, the date of the sale for datetime ordering, and "store_id" as the multiseries identifier.
    The operation includes a task plan to compute lags of orders 1, 7, and 30 on the sales amount, and
    specifies known in advance columns "promotion" and "holiday_flag":

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import TimeSeriesOperation, TaskPlanElement, Lags
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> task_plan = [
        ...     TaskPlanElement(
        ...         column="sales_amount",
        ...         task_list=[Lags(orders=[1, 7, 30])]
        ...     )
        ... ]
        >>> time_series_op = TimeSeriesOperation(
        ...     target_column="sales_amount",
        ...     datetime_partition_column="sale_date",
        ...     forecast_distances=[7, 30],
        ...     task_plan=[task_plan],
        ...     known_in_advance_columns=["promotion", "holiday_flag"],
        ...     multiseries_id_column="store_id"
        ... )
        >>> recipe.update(operations=[time_series_op])
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
    """
    Data wrangling operation to create a new feature computed using a SQL expression.

    Parameters
    ----------
    expression:
        SQL expression to compute the new feature.
    new_feature_name:
        Name of the new feature.

    Examples
    --------
    Create a new feature "total_sales" by summing the total of "online_sales" and "in_store_sales", rounded to the
    nearest dollar:

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import ComputeNewOperation
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> compute_new_op = ComputeNewOperation(
        ...     expression="ROUND(online_sales + in_store_sales, 0)",
        ...     new_feature_name="total_sales"
        ... )
        >>> recipe.update(operations=[compute_new_op])
    """

    def __init__(self, expression: str, new_feature_name: str):
        super().__init__(
            directive=WranglingOperations.COMPUTE_NEW,
            arguments={"expression": expression, "new_feature_name": new_feature_name},
        )


class RenameColumnsOperation(WranglingOperation):
    """
    Data wrangling operation to rename one or more columns.

    Parameters
    ----------
    column_mappings:
        Mapping of original column names to new column names.

    Examples
    --------
    Rename columns "old_name1" to "new_name1" and "old_name2" to "new_name2":

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import RenameColumnsOperation
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> rename_op = RenameColumnsOperation(
        ...     column_mappings={'old_name1': 'new_name1', 'old_name2': 'new_name2'}
        ... )
        >>> recipe.update(operations=[rename_op])
    """

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
            arguments={"column_mappings": [{"original_name": k, "new_name": v} for k, v in column_mappings.items()]},
        )


class FilterCondition(TypedDict):
    """
    Condition to filter rows in a :class:`FilterOperation <datarobot.models.recipe_operation.FilterOperation>`.

    Parameters
    ----------
    column: str
        Column name to apply the condition on.
    function: :class:`FilterOperationFunctions <datarobot.enums.FilterOperationFunctions>`
        The filtering function to use.
    function_arguments: List[Union[str, int, float]]
        The list of arguments for the filtering function.

    Examples
    --------
    :class:`FilterCondition <datarobot.models.recipe_operation.FilterCondition>` to filter rows where "age" is between
    18 and 65:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import FilterCondition
        >>> from datarobot.enums import FilterOperationFunctions
        >>> condition = FilterCondition(
        ...     column="age",
        ...     function=FilterOperationFunctions.BETWEEN,
        ...     function_arguments=[18, 65]
        ... )
    """

    column: str
    function: FilterOperationFunctions
    function_arguments: List[Union[str, int, float]]


class FilterOperation(WranglingOperation):
    """
    Data wrangling operation to filter rows based on one or more conditions.

    Parameters
    ----------
    conditions:
        List of conditions to filter on.
    keep_rows:
        If matching rows should be kept or dropped.
    operator:
        Operator to use between conditions when using multiple conditions. Allowed values: [and, or].

    Examples
    --------
    Filter input to only keep users older than 18:

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import FilterOperation, FilterCondition
        >>> from datarobot.enums import FilterOperationFunctions
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> condition = FilterCondition(
        ...     column="age",
        ...     function=FilterOperationFunctions.GREATER_THAN,
        ...     function_arguments=[18]
        ... )
        >>> filter_op = FilterOperation(conditions=[condition], keep_rows=True)
        >>> recipe.update(operations=[filter_op])

    Filter input to filter out rows where "status" is either "inactive" or "banned":

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import FilterOperation, FilterCondition
        >>> from datarobot.enums import FilterOperationFunctions
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> inactive_cond = FilterCondition(
        ...     column="status",
        ...     function=FilterOperationFunctions.EQUALS,
        ...     function_arguments=["inactive"]
        ... )
        >>> banned_cond = FilterCondition(
        ...     column="status",
        ...     function=FilterOperationFunctions.EQUALS,
        ...     function_arguments=["banned"]
        ... )
        >>> filter_op = FilterOperation(
        ...     conditions=[inactive_cond, banned_cond],
        ...     keep_rows=False,
        ...     operator="or"
        ... )
        >>> recipe.update(operations=[filter_op])
    """

    def __init__(
        self,
        conditions: List[FilterCondition],
        keep_rows: Optional[bool] = True,
        operator: Optional[str] = "and",
    ):
        super().__init__(
            directive=WranglingOperations.FILTER,
            arguments={"keep_rows": keep_rows, "operator": operator, "conditions": conditions},
        )


class DropColumnsOperation(WranglingOperation):
    """
    Data wrangling operation to drop one or more columns.

    Parameters
    ----------
    columns:
        Columns to drop.

    Examples
    --------
    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import DropColumnsOperation
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> drop_op = DropColumnsOperation(columns=['col1', 'col2'])
        >>> recipe.update(operations=[drop_op])
    """

    def __init__(self, columns: List[str]):
        super().__init__(
            directive=WranglingOperations.DROP_COLUMNS,
            arguments={"columns": columns},
        )


class DedupeRowsOperation(WranglingOperation):
    """
    Data wrangling operation to remove duplicate rows. Uses values from all columns.

    Examples
    --------
    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import DedupeRowsOperation
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> dedupe_op = DedupeRowsOperation()
        >>> recipe.update(operations=[dedupe_op])
    """

    def __init__(self):  # type: ignore[no-untyped-def]
        super().__init__(
            directive=WranglingOperations.DEDUPE_ROWS,
            arguments={},
        )


class FindAndReplaceOperation(WranglingOperation):
    """
    Data wrangling operation to find and replace strings in a column.

    Parameters
    ----------
    column:
        Column name to perform find and replace on.
    find:
        String or expression to find.
    replace_with:
        String to replace with.
    match_mode:
        Match mode to use when finding strings.
    is_case_sensitive:
        Whether the find operation should be case sensitive.

    Examples
    --------
    Set Recipe operations to search for exact match of "old_value" in column "col1" and replace with "new_value":

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import FindAndReplaceOperation
        >>> from datarobot.enums importFindAndReplaceMatchMode
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> find_replace_op = FindAndReplaceOperation(
        ...     column="col1",
        ...     find="old_value",
        ...     replace_with="new_value",
        ...     match_mode=FindAndReplaceMatchMode.EXACT,
        ...     is_case_sensitive=True
        ... )
        >>> recipe.update(operations=[find_replace_op])

    Set Recipe operations to use regular expression to replace names starting with "Brand" in column "name" and replace
    with "Lyra":

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import FindAndReplaceOperation
        >>> from datarobot.enums import FindAndReplaceMatchMode
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> find_replace_op = FindAndReplaceOperation(
        ...     column="name",
        ...     find="^Brand.*",
        ...     replace_with="Lyra",
        ...     match_mode=FindAndReplaceMatchMode.REGEX
        ... )
        >>> recipe.update(operations=[find_replace_op])
    """

    def __init__(
        self,
        column: str,
        find: str,
        replace_with: str,
        match_mode: FindAndReplaceMatchMode = FindAndReplaceMatchMode.EXACT,
        is_case_sensitive: bool = False,
    ):
        super().__init__(
            directive=WranglingOperations.REPLACE,
            arguments={
                "origin": column,
                "searchFor": find,
                "replacement": replace_with,
                "matchMode": match_mode,
                "isCaseSensitive": is_case_sensitive,
            },
        )


class JoinOperation(WranglingOperation):
    """
    Data wrangling operation to join an additional data input to the current data. The additional data input is
    treated as the right side of the join. The additional data input must be added to the recipe inputs when
    updating the recipe with this operation.

    The join condition only supports equality predicates. Multiple fields are combined with AND operators
    (e.g., `JOIN A, B ON A.x = B.y AND A.z = B.z AND A.t = B.t`).

    Examples
    --------
    Join customer details with an additional dataset of credit card information using customer id:

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe import RecipeDatasetInput
        >>> from datarobot.models.recipe_operation import JoinOperation
        >>> from datarobot.enums import JoinTypes
        >>> cc_dataset = dr.Dataset.get('5f43a1e2e4b0c123456789ab')
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> inputs = [recipe.inputs[0], RecipeDatasetInput.from_dataset(cc_dataset)]
        >>> join_op = JoinOperation.join_dataset(
        ...     dataset=cc_dataset,
        ...     join_type=JoinTypes.INNER,
        ...     right_prefix='cc_',
        ...     left_keys=['customer_id'],
        ...     right_keys=['customer_id']
        ... )
        >>> recipe.update(operations=[join_op], inputs=inputs)

    Join sales data with a reference table of sales targets that applies to all stores (Cartesian join to broadcast
    targets to every sales record):

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe import JDBCTableDataSourceInput
        >>> from datarobot.models.recipe_operation import JoinOperation
        >>> from datarobot.enums import JoinTypes
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> data_source_id = "647873c5a721e5647c15bbdc"
        >>> reference_table_input = JDBCTableDataSourceInput(
        ...     input_type=RecipeInputType.DATASOURCE,
        ...     data_source_id=data_source_id,
        ...     data_store_id="6418452b8a79f972e8ffe208",
        ...     alias="targets_table"
        ... )
        >>> inputs = [recipe.inputs[0], reference_table_input]
        >>> join_op = JoinOperation.join_jdbc_data_source_table(
        ...     data_source_id=data_source_id,
        ...     join_type=JoinTypes.CARTESIAN,
        ...     right_prefix='ref_'
        ... )
        >>> recipe.update(operations=[join_op], inputs=inputs)
    """

    def __init__(
        self,
        source_type: JoinSourceType,
        join_type: JoinType,
        right_dataset_id: Optional[str] = None,
        right_dataset_version_id: Optional[str] = None,
        right_data_source_id: Optional[str] = None,
        right_prefix: Optional[str] = None,
        left_keys: Optional[List[str]] = None,
        right_keys: Optional[List[str]] = None,
    ):
        super().__init__(
            directive=WranglingOperations.JOIN,
            arguments={
                "joinType": join_type,
                "rightDataSourceId": right_data_source_id,
                "rightDatasetId": right_dataset_id,
                "rightDatasetVersionId": right_dataset_version_id,
                "leftKeys": left_keys,
                "rightKeys": right_keys,
                "rightPrefix": right_prefix,
                "source": source_type,
            },
        )

    @classmethod
    def join_dataset(
        cls,
        dataset: Dataset,
        join_type: JoinType,
        right_prefix: Optional[str] = None,
        left_keys: Optional[List[str]] = None,
        right_keys: Optional[List[str]] = None,
    ) -> JoinOperation:
        """
        Create a :class:`JoinOperation <datarobot.models.recipe_operation.JoinOperation>` to join a dataset to the
        data in the recipe.

        Parameters
        ----------
        dataset:
            Dataset to join with. This dataset must already be added to the recipe inputs.
        join_type:
            Type of join to perform.
        right_prefix:
            Optional prefix to add to all column names from the joined dataset in the join result.
        left_keys:
            List of column names to be used in the "ON" clause for the left side of the join. Required for inner
            and left joins, not used for Cartesian joins.
        right_keys:
            List of column names to be used in the "ON" clause for the right side of the join. Required for inner
            and left joins, not used for Cartesian joins.
        """
        return cls(
            source_type=JoinSourceType.DATASET,
            join_type=join_type,
            right_dataset_id=dataset.id,
            right_dataset_version_id=dataset.version_id,
            right_prefix=right_prefix,
            left_keys=left_keys,
            right_keys=right_keys,
        )

    @classmethod
    def join_jdbc_data_source_table(
        cls,
        data_source_id: str,
        join_type: JoinType,
        right_prefix: Optional[str] = None,
        left_keys: Optional[List[str]] = None,
        right_keys: Optional[List[str]] = None,
    ) -> JoinOperation:
        """
        Create a :class:`JoinOperation <datarobot.models.recipe_operation.JoinOperation>` to join a JDBC table input
        from a data source to the data in the recipe.

        Parameters
        ----------
        data_source_id:
            Data source ID for the JDBC table to join with. This data source must already be added to the recipe inputs.
        join_type:
            Type of join to perform.
        right_prefix:
            Optional prefix to add to all column names from the joined table in the join result.
        left_keys:
            List of column names to be used in the "ON" clause for the left side of the join. Required for inner
            and left joins, not used for Cartesian joins.
        right_keys:
            List of column names to be used in the "ON" clause for the right side of the join. Required for inner
            and left joins, not used for Cartesian joins.
        """
        return cls(
            source_type=JoinSourceType.TABLE,
            join_type=join_type,
            right_data_source_id=data_source_id,
            right_prefix=right_prefix,
            left_keys=left_keys,
            right_keys=right_keys,
        )


class AggregateFeature(TypedDict):
    """
    Feature to aggregate and the aggregation functions to apply in a
    :class:`AggregationOperation <datarobot.models.recipe_operation.AggregationOperation>`.

    Parameters
    ----------
    feature: str
        Feature to aggregate.
    functions: List[AggregationFunctions]
        List of aggregation functions to apply. A new column will be created for each function. Some feature types may
        not support all aggregation functions, e.g. categorical features do not support numeric aggregation functions
        like SUM or AVG.

    Examples
    --------
    :class:`AggregateFeature <datarobot.models.recipe_operation.AggregateFeature>` to compute the sum and average of
    sales:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import AggregateFeature
        >>> from datarobot.enums import AggregationFunctions
        >>> aggregate_feature = AggregateFeature(
        ...     feature="sales_amount",
        ...     functions=[AggregationFunctions.SUM, AggregationFunctions.AVG]
        ... )
    """

    feature: str
    functions: List[AggregationFunctions]


class AggregationOperation(WranglingOperation):
    """
    Data wrangling operation to compute aggregate metrics for one or more features by grouping data by one or
    more columns. This operation will retain all group by columns in the output dataset and create a new
    column for each aggregation function applied to each feature chosen for aggregation.

    Parameters
    ----------
    aggregations:
        List of features to aggregate with the aggregation functions to apply on each feature. Any features
        in the list of aggregations should not appear in the `group_by_columns` list.
    group_by_columns:
        List of columns to group by. Any column name in this list should not appear in the list of features to
        aggregate.

    Examples
    --------
    Create an aggregation operation to compute the total and average sales amounts, and total sales quantity per region.
    This will create 3 new columns `sales_amount_sum`, `sales_amount_avg`, and `sales_quantity_sum` in the output
    dataset:

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe_operation import AggregationOperation, AggregateFeature
        >>> from datarobot.enums import AggregationFunctions
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
        >>> agg_sales = AggregateFeature(
        ...     feature="sales_amount",
        ...     functions=[AggregationFunctions.SUM, AggregationFunctions.AVG]
        ... )
        >>> agg_quantity = AggregateFeature(
        ...     feature="sales_quantity",
        ...     functions=[AggregationFunctions.SUM]
        ... )
        >>> aggregation_op = AggregationOperation(
        ...     aggregations=[agg_sales, agg_quantity],
        ...     group_by_columns=["region"]
        ... )
        >>> recipe.update(operations=[aggregation_op])
    """

    def __init__(self, aggregations: List[AggregateFeature], group_by_columns: List[str]):
        super().__init__(
            directive=WranglingOperations.AGGREGATE,
            arguments={
                "aggregations": aggregations,
                "groupBy": group_by_columns,
            },
        )


class RandomSamplingOperation(SamplingOperation):
    """
    A sampling technique that randomly selects the specified number of rows from the input when generating the sample
    data for a recipe.

    Parameters
    ----------
    rows:
        The number of rows to sample.
    seed:
        The random seed to use for sampling. Optional.

    Examples
    --------
    Using the default seed:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import RandomSamplingOperation
        >>> op = RandomSamplingOperation(rows=500)

    Randomly generating a seed value:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import RandomSamplingOperation
        >>> import random
        >>> random_op = RandomSamplingOperation(rows=500, seed=random.randint(1, 10000))
    """

    def __init__(self, rows: int, seed: Optional[int] = None):
        super().__init__(
            directive=SamplingOperations.RANDOM_SAMPLE,
            arguments={"rows": rows, "seed": seed},
        )


class LimitSamplingOperation(SamplingOperation):
    """
    A sampling technique that samples the first *N* rows from the input when generating the
    sample data for a recipe.

    Parameters
    ----------
    rows:
        The number of rows to sample.

    Examples
    --------
    Using the limit sampling operation to sample the first 100 rows:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import LimitSamplingOperation
        >>> op = LimitSamplingOperation(rows=100)
    """

    def __init__(self, rows: int):
        super().__init__(
            directive=SamplingOperations.LIMIT,
            arguments={"rows": rows},
        )


class DatetimeSamplingOperation(SamplingOperation):
    """
    A sampling technique that samples `n` rows by ordering rows based on a datetime partition column and selecting
    according to the strategy specified (e.g. latest, earliest). Supports multiseries data.

    Parameters
    ----------
    datetime_partition_column:
        The datetime partition column to order by.
    rows:
        The number of rows to sample.
    strategy:
        The datetime sampling strategy to use. Optional.
    multiseries_id_column:
        Column name used to identify each time series within the input data. Required only for multiseries data.
    selected_series:
        The list of series identifiers to include when sampling multiseries data. Requires `multiseries_id_column` to
        be set.

    Examples
    --------
    Create a sampling operation to sample the latest 200 stock trades for tickers 'AAPL' and 'MSFT':

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import DatetimeSamplingOperation
        >>> from datarobot.enums import DatetimeSamplingStrategy
        >>> op = DatetimeSamplingOperation(
        ...     datetime_partition_column='trade_date',
        ...     rows=200,
        ...     strategy=DatetimeSamplingStrategy.LATEST,
        ...     multiseries_id_column='ticker',
        ...     selected_series=['AAPL', 'MSFT']
        ... )
    """

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


class TableSampleSamplingOperation(SamplingOperation):
    """
    A sampling technique that uses a table sample method to randomly select a percentage of rows from the input
    when generating the sample data for a recipe. Not supported for all data inputs.
    For data stores that support table sampling this method is generally more efficient than random sampling.

    Parameters
    ----------
    percent:
        The percentage (%) of rows to sample (0-100).
    seed:
        The random seed to use for sampling. Optional.

    Examples
    --------
    Sample using 50% of the input datasource using the default seed:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import TableSampleSamplingOperation
        >>> op = TableSampleSamplingOperation(percent=50)
    """

    def __init__(self, percent: int, seed: Optional[int] = None):
        if percent not in range(0, 101):
            raise ValueError("percent must be between 0 and 100.")
        super().__init__(
            directive=SamplingOperations.TABLE_SAMPLE,
            arguments={"percent": percent, "seed": seed},
        )


class RandomDownsamplingOperation(DownsamplingOperation):
    """
    A downsampling technique that reduces the size of the majority class using random sampling (i.e., each sample has an
    equal probability of being chosen).

    Parameters
    ----------
    max_rows:
        The maximum number of rows to downsample to.
    seed:
        The random seed to use for downsampling. Optional.

    Examples
    --------
    Using the default seed:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import RandomDownsamplingOperation
        >>> op = RandomDownsamplingOperation(max_rows=600)

    Randomly generating a seed value:

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import RandomDownsamplingOperation
        >>> import random
        >>> random_op = RandomDownsamplingOperation(max_rows=600, seed=random.randint(1, 10000))
    """

    DEFAULT_SEED = 43  # Default seed used in UI

    def __init__(self, max_rows: int, seed: int = DEFAULT_SEED):
        super().__init__(
            directive=DownsamplingOperations.RANDOM_SAMPLE,
            arguments={"rows": max_rows, "seed": seed},
        )


class SmartDownsamplingOperation(DownsamplingOperation):
    """
    A downsampling technique that relies on the distribution of target values to adjust size and specifies how much a
    specific class was sampled in a new column.

    For this technique to work, ensure the recipe has set `target` and `weightsFeature` in the recipe's settings.

    Parameters
    ----------
    max_rows:
        The maximum number of rows to downsample to.
    method:
        The downsampling method to use.
    seed:
        The random seed to use for downsampling. Optional.

    Examples
    --------
    .. code-block:: python

        >>> from datarobot.models.recipe_operation import SmartDownsamplingOperation, SmartDownsamplingMethod
        >>> op = SmartDownsamplingOperation(max_rows=1000, method=SmartDownsamplingMethod.BINARY)
    """

    DEFAULT_SEED = 43  # Default seed used in UI

    def __init__(
        self,
        max_rows: int,
        method: SmartDownsamplingMethod = SmartDownsamplingMethod.BINARY,
        seed: int = DEFAULT_SEED,
    ):
        super().__init__(
            directive=DownsamplingOperations.SMART_DOWNSAMPLING,
            arguments={"rows": max_rows, "method": method, "seed": seed},
        )
