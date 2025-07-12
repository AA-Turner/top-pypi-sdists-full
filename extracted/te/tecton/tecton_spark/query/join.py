import logging
import operator
from datetime import timedelta
from functools import reduce
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple

import attrs
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.window as spark_window

import tecton_core.tecton_pendulum as pendulum
from tecton_core import time_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query import compaction_utils
from tecton_core.query_consts import aggregation_group_id
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import effective_timestamp
from tecton_core.query_consts import tecton_secondary_key_aggregation_indicator_col
from tecton_core.query_consts import temp_indictor_column_name
from tecton_core.query_consts import temp_intermediate_partial_aggregate_column_name
from tecton_core.query_consts import temp_struct_column_name
from tecton_core.schema import Schema
from tecton_core.specs.feature_view_spec import OnlineBatchTablePart
from tecton_core.specs.time_window_spec import LifetimeWindowSpec
from tecton_core.specs.time_window_spec import RelativeTimeWindowSpec
from tecton_core.specs.time_window_spec import TimeWindowSeriesSpec
from tecton_core.specs.time_window_spec import TimeWindowSpec
from tecton_core.specs.time_window_spec import create_time_window_spec_from_data_proto
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_core.time_utils import convert_timestamp_for_version
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.query.node import SparkExecNode


logger = logging.getLogger(__name__)


@attrs.frozen
class JoinSparkNode(SparkExecNode):
    """
    A basic left join on 2 inputs
    """

    left: SparkExecNode
    right: SparkExecNode
    join_cols: List[str]
    how: str
    allow_nulls: bool = False

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        # NOTE: the aliases are added because on Databricks the usage of this node in a
        # FeatureService join errors when going through the allow nulls codepath.
        # The error claimed an ambiguous self-join, when the spine events are the same data source as a feature view's events.
        left_df = self.left.to_dataframe(spark).alias("left_join_df")
        right_df = self.right.to_dataframe(spark).alias("right_join_df")
        if self.allow_nulls:
            join_condition = reduce(operator.and_, [left_df[col].eqNullSafe(right_df[col]) for col in self.join_cols])
            right_nonjoin_cols = set(self.right.columns) - set(self.join_cols)
            # We need to quote the column names because we use dots in the column names to separate feature view name and feature name.
            return left_df.join(right_df, how=self.how, on=join_condition).select(
                *[left_df[f"`{col}`"] for col in self.left.columns],
                *[right_df[f"`{col}`"] for col in right_nonjoin_cols],
            )
        else:
            return left_df.join(right_df, how=self.how, on=self.join_cols)


@attrs.frozen
class WildcardJoinSparkNode(SparkExecNode):
    left: SparkExecNode
    right: SparkExecNode
    join_cols: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)

        left_columns = [getattr(left_df, col) for col in left_df.columns if col not in self.join_cols]
        right_columns = [getattr(right_df, col) for col in right_df.columns if col not in self.join_cols]

        left_df = left_df.withColumn("_tecton_join_cols", F.struct(self.join_cols))
        right_df = right_df.withColumn("_tecton_join_cols", F.struct(self.join_cols))

        return left_df.join(right_df, how="outer", on=["_tecton_join_cols"]).select(
            "_tecton_join_cols.*", *left_columns, *right_columns
        )


@attrs.frozen
class AsofJoinInputSparkContainer:
    node: SparkExecNode
    timestamp_field: str  # spine or feature timestamp
    effective_timestamp_field: Optional[str]
    prefix: Optional[str]
    schema: Optional[Schema]


@attrs.frozen
class _AsofJoinerAndWindowAggregator:
    """
    Implements an asof join + window aggregate, with the left side being the
    'spine' and the right side being used for the aggregate value.

    There are a few ways this behavior can be implemented, but by test the best
    performing method has been to union the two inputs and use a window
    function over the unioned DataFrame to do the calculation.

    This can be used for a traditional asof join by using a `last` window func on the unioned dataframe:
        last(col) OVER (PARTITION BY partition_cols ORDER BY timestamp_cols RANGE BETWEEN unbounded preceding AND current row)

    This is also used by the full aggregate rollup (which uses more complicated set of window specs and rollup functions). Example 1h count rollup:
        sum(count_col) OVER (PARTITION BY partition_cols ORDER BY timestamp_cols RANGE BETWEEN 3600 AND current row)
    """

    _left_df: pyspark.sql.DataFrame
    _right_df: pyspark.sql.DataFrame
    timestamp_cols: Tuple[str, ...]
    common_partition_cols: Tuple[str, ...]  # partition columns used by all aggregations.
    _extra_partition_cols: Tuple[str, ...]  # partition columns not shared by every aggregation.
    _left_ts_cols: Tuple[str, ...]
    _use_window_range_between_value: bool
    _tecton_window_range_between_order_columns: Tuple[str, ...]

    _timestamp_prefix: ClassVar[str] = "_tecton_asof_join_timestamp"
    _left_prefix: ClassVar[str] = "_tecton_left"
    _is_left_column_name: ClassVar[str] = "IS_LEFT"
    _tecton_window_range_between_order_col_name: ClassVar[str] = "_tecton_window_range_between_order_col"

    @classmethod
    def create(
        cls,
        left_df: pyspark.sql.DataFrame,
        right_df: pyspark.sql.DataFrame,
        left_ts_cols: Sequence[str],
        right_ts_cols: Sequence[str],
        partition_cols: Sequence[str],
        use_window_range_between_value: bool,
        extra_partition_cols: Sequence[str] = [],
    ) -> "_AsofJoinerAndWindowAggregator":
        if len(left_ts_cols) != len(right_ts_cols):
            msg = f"Timestamp columns are not equal length: left({left_ts_cols}), right({right_ts_cols})"
            raise RuntimeError(msg)

        timestamp_cols = [f"{cls._timestamp_prefix}_{i}" for i in range(len(left_ts_cols))]
        window_range_between_order_cols = [
            f"{cls._tecton_window_range_between_order_col_name}_{i}" for i in range(len(timestamp_cols))
        ]

        left_df_cols = [F.col(old_col).alias(new_col) for new_col, old_col in zip(timestamp_cols, left_ts_cols)]
        left_df = left_df.select("*", *left_df_cols)

        right_df_cols = [F.col(old_col).alias(new_col) for new_col, old_col in zip(timestamp_cols, right_ts_cols)]
        right_df = right_df.select("*", *right_df_cols)

        return cls(
            left_df=left_df,
            right_df=right_df,
            timestamp_cols=tuple(timestamp_cols),
            left_ts_cols=tuple(left_ts_cols),
            common_partition_cols=tuple(partition_cols),
            extra_partition_cols=tuple(extra_partition_cols),
            use_window_range_between_value=use_window_range_between_value,
            tecton_window_range_between_order_columns=tuple(window_range_between_order_cols),
        )

    @property
    def common_cols(self) -> List[str]:
        return list(self.timestamp_cols) + list(self.all_partition_columns)

    @property
    def all_partition_columns(self) -> List[str]:
        return list(self.common_partition_cols) + list(self._extra_partition_cols)

    @property
    def left_nonjoin_cols(self) -> List[str]:
        return [c for c in self._left_df.columns if c not in set(self.common_cols)]

    @property
    def _right_nonjoin_cols(self) -> List[str]:
        return [c for c in self._right_df.columns if c not in set(self.common_cols)]

    def _union(self) -> pyspark.sql.DataFrame:
        # schemas have to match exactly so that the 2 dataframes can be unioned together.
        left_full_cols = (
            [F.lit(True).alias(self._is_left_column_name)]
            + [F.col(x) for x in self.common_cols]
            + [F.col(x).alias(f"{self._left_prefix}_{x}") for x in self.left_nonjoin_cols]
            + [F.lit(None).alias(x) for x in self._right_nonjoin_cols]
        )
        right_full_cols = (
            [F.lit(False).alias(self._is_left_column_name)]
            + [F.col(x) for x in self.common_cols]
            + [F.lit(None).alias(f"{self._left_prefix}_{x}") for x in self.left_nonjoin_cols]
            + [F.col(x) for x in self._right_nonjoin_cols]
        )

        if self._use_window_range_between_value:
            # we want left rows to be sorted after right rows if timestamps are the same. But when using "window range between"
            # only 1 column can be used for sorting. As a workaround, we multiply the left rows by * 2 and then add 1. The right
            # rows will be multiplied by 2 only. This will ensure the left rows will be sorted after the right rows.
            for index, timestamp_col in enumerate(self.timestamp_cols):
                order_by_col = self._tecton_window_range_between_order_columns[index]
                left_full_cols.append((F.col(timestamp_col).cast("long") * 2 + 1).alias(order_by_col))
                right_full_cols.append((F.col(timestamp_col).cast("long") * 2).alias(order_by_col))

        left_df = self._left_df.select(left_full_cols)
        right_df = self._right_df.select(right_full_cols)
        return left_df.union(right_df)

    def join_and_aggregate(self, aggregations: List[pyspark.sql.Column]) -> pyspark.sql.DataFrame:
        union = self._union()
        # We use the right side of asof join to calculate the aggregate values to augment to the rows from the left side.
        # Then, we drop the right side's rows.
        output_columns = (
            self.common_cols
            + [F.col(f"{self._left_prefix}_{x}").alias(x) for x in self.left_nonjoin_cols]
            + aggregations
            + [self._is_left_column_name]
        )
        selected = union.select(output_columns)
        return selected.filter(self._is_left_column_name).drop(self._is_left_column_name, *self.timestamp_cols)

    def get_range_between_window_spec(
        self,
        range_between_start: spark_window.Window,
        range_between_end: spark_window.Window,
        timestamp_col: Optional[str] = None,
        extra_partition_cols: List[str] = [],
    ) -> spark_window.WindowSpec:
        assert len(extra_partition_cols) == 0 or all(
            col in self._extra_partition_cols for col in extra_partition_cols
        ), f"Expected extra_partition_cols {extra_partition_cols} in {self._extra_partition_cols}."
        assert timestamp_col is None or timestamp_col in self._left_ts_cols, (
            f"Expected timestamp_col {timestamp_col} in {self._left_ts_cols}."
        )

        if range_between_start == spark_window.Window.unboundedPreceding:
            if timestamp_col:
                order_column_index = self._left_ts_cols.index(timestamp_col)
                order_by_cols = [self.timestamp_cols[order_column_index], self._is_left_column_name]
            else:
                order_by_cols = [*self.timestamp_cols, self._is_left_column_name]
        else:
            if timestamp_col:
                order_column_index = self._left_ts_cols.index(timestamp_col)
            else:
                order_column_index = 0
            order_by_col = self._tecton_window_range_between_order_columns[order_column_index]
            order_by_cols = [order_by_col]
        window_spec = (
            spark_window.Window.partitionBy(list(self.common_partition_cols) + extra_partition_cols)
            .orderBy([F.col(c).asc() for c in order_by_cols])
            .rangeBetween(range_between_start, range_between_end)
        )
        return window_spec


@attrs.frozen
class AsofJoinSparkNode(SparkExecNode):
    """
    A "basic" asof join on 2 inputs.
    LEFT asof_join RIGHT has the following behavior:
        For each row on the left side, find the latest (but <= in time) matching (by join key) row on the right side, and associate the right side's columns to that row.
    The result is a dataframe with the same number of rows as LEFT, with additional columns. These additional columns are prefixed with f"{right_prefix}_". This is the built-in behavior of the tempo library.

    """

    left_container: AsofJoinInputSparkContainer
    right_container: AsofJoinInputSparkContainer
    join_cols: List[str]

    _right_struct_col: ClassVar[str] = "_right_values_struct"

    def _structify_right(self, right_df: pyspark.sql.DataFrame, struct_col_name: str) -> pyspark.sql.DataFrame:
        # we additionally include the right time field though we join on the left's time field.
        # This is so we can see how old the row we joined against is and later determine whether to exclude on basis of ttl
        right_nonjoin_cols = list(set(right_df.columns) - set(self.join_cols))
        # wrap fields on the right in a struct. This is to work around null feature values and ignorenulls
        # used during joining/window function.
        cols_to_wrap = [F.col(c).alias(f"{self.right_container.prefix}_{c}") for c in right_nonjoin_cols]
        right_df = right_df.withColumn(struct_col_name, F.struct(*cols_to_wrap))
        return right_df

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left_container.node.to_dataframe(spark)
        right_df = self.right_container.node.to_dataframe(spark)

        right_df = self._structify_right(right_df, self._right_struct_col)

        # The left and right dataframes are unioned together and sorted using 2 columns.
        # The spine will use the spine timestamp and the features will be ordered by their
        # (effective_timestamp, feature_timestamp) because multiple features can have the same effective
        # timestamp. We want to return the closest feature to the spine timestamp that also satisfies
        # the condition => effective timestamp <= spine timestamp.
        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=left_df,
            right_df=right_df,
            left_ts_cols=[self.left_container.timestamp_field, self.left_container.timestamp_field],
            right_ts_cols=[self.right_container.effective_timestamp_field, self.right_container.timestamp_field],
            partition_cols=self.join_cols,
            use_window_range_between_value=False,
        )
        window_spec = join_spec.get_range_between_window_spec(
            spark_window.Window.unboundedPreceding, spark_window.Window.currentRow
        )
        aggregations = [
            F.last(F.col(self._right_struct_col), ignorenulls=True).over(window_spec).alias(self._right_struct_col)
        ]
        spine_with_features_df = join_spec.join_and_aggregate(aggregations)

        # unwrap the struct to return the fields
        final_df = spine_with_features_df.select(
            self.join_cols + join_spec.left_nonjoin_cols + [f"{self._right_struct_col}.*"]
        )
        return final_df


@attrs.frozen
class AsofJoinFullAggSparkNode(SparkExecNode):
    """
    An asof join very similar to AsofJoinNode, but with a change where it does
    the full aggregation rollup (rather than a last).

    NOTE: This should only be used for window aggregates.

    LEFT asof_join RIGHT has the following behavior:
        For each row in the spine, find the matching partial aggregates (by time range)
        and run the appropriate full aggregate over those rows.

    The result is a dataframe with the same number of rows as the spine, with
    additional columns of the fully aggregated features (or null).

    There are a few ways this behavior can be implemented, but by test the best
    performing method has been to union the two inputs and use a window
    function for the aggregates.
    """

    spine: SparkExecNode
    partial_agg_node: SparkExecNode
    fdw: FeatureDefinitionWrapper
    TECTON_AGG_WINDOW_ORDER_COL: ClassVar[str] = "_tecton_agg_window_order_col"

    def _get_aggregations(self, join_spec: _AsofJoinerAndWindowAggregator) -> List[pyspark.sql.Column]:
        time_aggregation = self.fdw.trailing_time_window_aggregation()
        aggregations = []
        for feature in time_aggregation.features:
            col_datatype = self.fdw.view_schema.to_dict()[feature.input_feature_name]
            aggregation_plan = get_aggregation_plan(
                feature.function,
                feature.function_params,
                time_aggregation.is_continuous,
                time_aggregation.time_key,
                col_datatype,
            )
            names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            time_window = create_time_window_spec_from_data_proto(feature.time_window)

            if isinstance(time_window, TimeWindowSeriesSpec):
                window_aggs = []
                for relative_time_window in time_window.time_windows:
                    window_aggs.append(
                        aggregation_plan.full_aggregation_transform(
                            names,
                            self._generate_aggregation_window_spec(
                                RelativeTimeWindowSpec(
                                    window_start=relative_time_window.window_start,
                                    window_end=relative_time_window.window_end,
                                ),
                                join_spec,
                            ),
                        )
                    )
                agg = F.array(window_aggs)
            else:
                agg = aggregation_plan.full_aggregation_transform(
                    names,
                    self._generate_aggregation_window_spec(
                        time_window,
                        join_spec,
                    ),
                )
            aggregations.append(agg.alias(feature.output_feature_name))

        # If the aggregation secondary key appears, we run a window based aggregation on the secondary key
        # indicator column to identify if the secondary appears in each distinct window. `sum` function is arbitrary
        # here, and we just need a function to return `null` value if the secondary key does not appear in the window.
        if self.fdw.aggregation_secondary_key:
            for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
                aggregations.append(
                    F.sum(tecton_secondary_key_aggregation_indicator_col())
                    .over(
                        self._generate_aggregation_window_spec(
                            secondary_key_output.time_window,
                            join_spec,
                        )
                    )
                    .alias(
                        f"{tecton_secondary_key_aggregation_indicator_col()}_{secondary_key_output.time_window.to_string()}"
                    )
                )
        return aggregations

    def _generate_aggregation_window_spec(
        self,
        time_window: TimeWindowSpec,
        join_spec: _AsofJoinerAndWindowAggregator,
    ) -> spark_window.WindowSpec:
        # Since the spine and feature rows are unioned together, the spine rows must be ordered after the feature rows
        # when they have the same timestamp for window aggregation to be correct. Window aggregation does not allow
        # ordering using two columns when range between is used. As a workaround, we multiply the left rows by (* 2 + 1).
        # The right rows by * 2. This will ensure the left rows will be sorted after the right rows.
        # We need to make an adjustment here to earliest_anchor_time due to these changes.
        if isinstance(time_window, RelativeTimeWindowSpec):
            start, end = self.fdw.time_range_for_relative_time_window(time_window)
            return join_spec.get_range_between_window_spec(
                start * 2 - 1,
                end * 2 - 1,
            )
        elif isinstance(time_window, LifetimeWindowSpec):
            return join_spec.get_range_between_window_spec(
                spark_window.Window.unboundedPreceding,
                spark_window.Window.currentRow,
            )
        elif isinstance(time_window, TimeWindowSeriesSpec):
            start, end = self.fdw.time_range_for_relative_time_window(
                RelativeTimeWindowSpec(time_window.window_series_start, time_window.window_series_end)
            )
            return join_spec.get_range_between_window_spec(start * 2 - 1, end * 2 - 1)
        else:
            msg = f"Invalid time_window type: {type(time_window)}"
            raise TypeError(msg)

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.spine.to_dataframe(spark)
        right_df = self.partial_agg_node.to_dataframe(spark)

        partition_columns = self.fdw.join_keys

        if self.fdw.aggregation_secondary_key:
            partition_columns.append(self.fdw.aggregation_secondary_key)

            # If the aggregation secondary key appears, we add an indicator column to the partial aggregation result to
            # help identify all secondary keys that are present in each distinct time window.
            right_df = right_df.withColumn(tecton_secondary_key_aggregation_indicator_col(), F.lit(1))

        timestamp_cols = [anchor_time()]
        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=left_df,
            right_df=right_df,
            left_ts_cols=timestamp_cols,
            right_ts_cols=timestamp_cols,
            partition_cols=partition_columns,
            use_window_range_between_value=True,
        )
        aggregations = self._get_aggregations(join_spec)
        return join_spec.join_and_aggregate(aggregations)


@attrs.frozen
class AsofBitemporalJoinFullAggSparkNode(AsofJoinFullAggSparkNode):
    """
    AsofBitemporalJoinFullAggSparkNode is used only to handle late-arriving data (batch_publish_timestamp is not null) where simulate_events_published_on_time=False.
    """

    _SPINE_DF_ALIAS = "spine_df"
    _PARTIAL_AGG_DF_ALIAS = "partial_agg_df"

    def _generate_aggregation_window_spec(
        self,
        time_window: TimeWindowSpec,
        join_spec: _AsofJoinerAndWindowAggregator,
    ) -> spark_window.WindowSpec:
        # This is nearly identical to _generate_aggregation_window_spec for AsofJoinFullAggSparkNode, except:
        # 1. get_range_between_window_spec has extra_partition_cols set (very important)
        # 2. TimeWindowSeriesSpec is not supported - TimeWindowSeriesSpec is also not supported for compaction which is a prerequisite for late-arriving data.
        if isinstance(time_window, RelativeTimeWindowSpec):
            start, end = self.fdw.time_range_for_relative_time_window(time_window)
            return join_spec.get_range_between_window_spec(
                start * 2 - 1, end * 2 - 1, extra_partition_cols=[self.fdw.timestamp_key]
            )
        elif isinstance(time_window, LifetimeWindowSpec):
            return join_spec.get_range_between_window_spec(
                spark_window.Window.unboundedPreceding,
                spark_window.Window.currentRow,
                extra_partition_cols=[self.fdw.timestamp_key],
            )
        elif isinstance(time_window, TimeWindowSeriesSpec):
            msg = "TimeWindowSeriesSpec is not supported for joins with late-arriving data."
            raise ValueError(msg)
        else:
            msg = f"Invalid time_window type: {type(time_window)}"
            raise TypeError(msg)

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        """
        The query plan is:
        1. Join the spine and partial aggregation dataframes on the join keys AND spine.anchor_time >= partial_agg.anchor_time AND spine.timestamp_key >= partial_agg.effective_timestamp
        The spine.timestamp_key >= partial_agg.effective_timestamp condition ensures only events that were "effective" at the spine timestamp are captured (this is the bitemporal join part). The step will produce a dataframe with duplicate rows for each spine event that matches multiple partial aggregation events.

        2. Union the output of (1) with the spine and partition by join_keys AND spine_df.timestamp

        Aliases (spine_df and partial_agg_df) are used to avoid ambiguous self-join errors when using a pyspark dataframe.
        """

        # Alias with the same names as variables
        spine_df = self.spine.to_dataframe(spark).alias(self._SPINE_DF_ALIAS)
        partial_agg_df = self.partial_agg_node.to_dataframe(spark).alias(self._PARTIAL_AGG_DF_ALIAS)

        # Join key conditions with qualified names
        join_key_conditions = [
            F.col(f"{self._SPINE_DF_ALIAS}.{key}") == F.col(f"{self._PARTIAL_AGG_DF_ALIAS}.{key}")
            for key in self.fdw.join_keys
        ]

        # Bitemporal join conditions
        bitemporal_join_conditions = [
            F.col(f"{self._SPINE_DF_ALIAS}.{self.fdw.timestamp_key}")
            >= F.col(f"{self._PARTIAL_AGG_DF_ALIAS}.{effective_timestamp()}"),
            F.col(f"{self._SPINE_DF_ALIAS}.{anchor_time()}") >= F.col(f"{self._PARTIAL_AGG_DF_ALIAS}.{anchor_time()}"),
        ]
        if not self.fdw.has_lifetime_aggregate:
            max_aggregation_window = -convert_timedelta_for_version(
                self.fdw.earliest_window_start, self.fdw.get_feature_store_format_version
            )
            bitemporal_join_conditions.append(
                F.col(f"{self._SPINE_DF_ALIAS}.{anchor_time()}") - max_aggregation_window
                <= F.col(f"{self._PARTIAL_AGG_DF_ALIAS}.{anchor_time()}")
            )

        # Columns to keep from partial_agg_df
        partial_agg_column_names_to_keep = (
            set(partial_agg_df.columns) - set(self.fdw.join_keys) - {effective_timestamp()}
        )
        partial_agg_columns_to_keep = [
            F.col(f"{self._PARTIAL_AGG_DF_ALIAS}.{col}") for col in partial_agg_column_names_to_keep
        ]

        # Columns to keep from spine_df
        join_key_columns = [F.col(f"{self._SPINE_DF_ALIAS}.{key}") for key in self.fdw.join_keys]
        cols_to_keep = [
            *join_key_columns,
            F.col(f"{self._SPINE_DF_ALIAS}.{self.fdw.timestamp_key}"),
            *partial_agg_columns_to_keep,
        ]

        # Perform the join and select
        joined_df = partial_agg_df.join(
            spine_df, on=join_key_conditions + bitemporal_join_conditions, how="inner"
        ).select(*cols_to_keep)

        partition_columns = self.fdw.join_keys
        if self.fdw.aggregation_secondary_key:
            partition_columns.append(self.fdw.aggregation_secondary_key)

            # If the aggregation secondary key appears, we add an indicator column to the partial aggregation result to
            # help identify all secondary keys that are present in each distinct time window.
            joined_df = joined_df.withColumn(tecton_secondary_key_aggregation_indicator_col(), F.lit(1))

        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=spine_df,
            right_df=joined_df,
            left_ts_cols=[anchor_time()],
            right_ts_cols=[anchor_time()],
            partition_cols=self.fdw.join_keys,
            # different from AsofJoinFullAggSparkNode
            # TODO(BAT-15413): This may break for cases where the spine has duplicate timestamps
            # investigate behavior for cases where spine has duplicate timestamps
            extra_partition_cols=[self.fdw.timestamp_key],
            use_window_range_between_value=True,
        )
        aggregations = self._get_aggregations(join_spec)
        return join_spec.join_and_aggregate(aggregations)


@attrs.frozen
class AsofSecondaryKeyExplodeSparkNode(SparkExecNode):
    """
    This node explodes a spine that misses the secondary key, into a spine that has the secondary key. This
    explosion is needed in two scenarios:
        1. A Feature View with an aggregation_secondary_key. An aggregation_secondary_key is never in the spine,
        so we always need to explode the spine for it.
        2. A Feature View with a wild card join key. A wild card join key is optional in the spine, so we need to
        explode the spine if and only if the wild card join key is not present.

    This node looks back the max aggregation interval or TTL of the feature view to find the secondary key values by
    using a window based `collect_set` function with an as-of join between left and right dataframes. Using the max
    aggregation interval can help us find all the secondary key values in all windows with a single window based
    `collect_set` function.

    E.g. Let's say a FV has fully bound join_key `A` and a secondary key `C`.
    For every row `[a_0, anchor_0]` from the spine, we will have the following rows in the
    returned dataframe:
       [a_0  c_1  anchor_0]
       [a_0  c_2  anchor_0]
        .    .    .
       [a_0  c_k  anchor_0]
    where (`c_1`, ..., `c_k`) represent all the secondary key values such that, the following row is
    present inside `right`:
        [a_0, c_i, anchor_i]
    and:
        anchor_0 - max_feature_agg_period (or ttl) < anchor_i <= anchor_0.

    Attributes:
         left: The spine node that misses the secondary key.
         left_ts: The timestamp column of the spine node.
         right: The feature value node that contains the secondary key.
         right_ts: The timestamp column of the feature value node.

    """

    left: SparkExecNode
    left_ts: str
    right: SparkExecNode
    right_ts: str
    fdw: FeatureDefinitionWrapper
    TECTON_INTERNAL_SECONDARY_KEY_SET_COL: ClassVar[str] = "_tecton_internal_secondary_key_set"

    @property
    def secondary_key(self) -> str:
        if self.fdw.is_temporal_aggregate:
            return self.fdw.aggregation_secondary_key or self.fdw.wildcard_join_key
        return self.fdw.wildcard_join_key

    @property
    def partition_cols(self) -> List[str]:
        # If the secondary key is an aggregation secondary key, we simply use the join keys as the partition columns.
        # If the secondary key is a wildcard join key, we use all join keys except the wildcard join key as the
        # partition columns.
        if self.fdw.wildcard_join_key:
            return [col for col in self.fdw.join_keys if col != self.fdw.wildcard_join_key]
        elif self.fdw.is_temporal_aggregate and self.fdw.aggregation_secondary_key:
            return self.fdw.join_keys
        else:
            msg = "AsofSecondaryKeyExplodeSparkNode requires either a wildcard join key or an aggregation secondary key"
            raise ValueError(msg)

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)

        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=left_df,
            right_df=right_df,
            left_ts_cols=[self.left_ts],
            right_ts_cols=[self.right_ts],
            partition_cols=self.partition_cols,
            use_window_range_between_value=True,
        )

        if self.fdw.is_temporal_aggregate and self.fdw.has_lifetime_aggregate:
            earliest_anchor_time = spark_window.Window.unboundedPreceding
        elif self.fdw.is_temporal_aggregate and self.fdw.get_max_batch_sawtooth_tile_size() is not None:
            # Since fdw.earliest_window_start corresponds to the largest aggregation window, we can correctly assume it uses the largest batch sawtooth tile size.
            interval_seconds = time_utils.convert_timedelta_for_version(
                self.fdw.get_max_batch_sawtooth_tile_size(), self.fdw.get_feature_store_format_version
            )
            earliest_anchor_time = self.fdw.earliest_anchor_time_from_window_start(
                self.fdw.earliest_window_start, aggregation_tile_interval_override=interval_seconds
            )
        else:
            if self.fdw.is_temporal_aggregate:
                earliest_anchor_time = self.fdw.earliest_anchor_time_from_window_start(self.fdw.earliest_window_start)
            else:
                # Add 1 since we expire at `ttl` time
                max_aggregation_window = int(self.fdw.serving_ttl.total_seconds())
                earliest_anchor_time = -max_aggregation_window + 1

            # Since the spine and feature rows are unioned together, the spine rows must be ordered after the feature rows
            # when they have the same timestamp for window aggregation to be correct. Window aggregation does not allow
            # ordering using two columns when range between is used. As a workaround, we multiply the left rows by (* 2 + 1).
            # The right rows by * 2. This will ensure the left rows will be sorted after the right rows.
            # We need to make an adjustment here to earliest_anchor_time due to these changes.
            earliest_anchor_time = earliest_anchor_time * 2 - 1

        window_spec = join_spec.get_range_between_window_spec(earliest_anchor_time, spark_window.Window.currentRow)
        aggregations = [
            F.collect_set(F.col(self.secondary_key)).over(window_spec).alias(self.TECTON_INTERNAL_SECONDARY_KEY_SET_COL)
        ]
        df = join_spec.join_and_aggregate(aggregations)
        res = df.withColumn(
            self.secondary_key, F.explode_outer(F.col(self.TECTON_INTERNAL_SECONDARY_KEY_SET_COL))
        ).drop(self.TECTON_INTERNAL_SECONDARY_KEY_SET_COL)

        return res


@attrs.frozen
class AggregationSecondaryKeyRollupSparkNode(SparkExecNode):
    """
    Rollup aggregation secondary key and corresponding feature values for each distinct window.

    The input node is a full aggregation node, which includes join keys and a secondary key. This node will:
        1. Group aggregation features by windows and put them into a temporary struct column for each distinct window.
        2. Rollup the temporal struct into a list by grouping on join keys and anchor time.
        3. Filter out secondary keys that do not appear in a particular window, and sort the list by secondary key.
        4. Transform each field in the temporal struct columns into its own column.

    E.g. Let's say a FV has a join_key `user_id` and a secondary key `ad_id` and the full aggregation node is like:
        | user_id | ad_id | value_max_1d     | value_max_3d     |  anchor_time | indicator_1d | indicator_3d |
        |---------|-------|------------------|------------------|--------------|--------------|--------------|
        | a       | 1     | 1                | 11               | 1            | 1            | 1            |
        | a       | 2     | 2                | 12               | 1            | 1            | 1            |
        | a       | 3     | None             | 13               | 1            | None         | 1            |
        | a       | 1     | 1                | 21               | 2            | 1            | 1            |
        | a       | 2     | 2                | 22               | 2            | 1            | 1            |

        The output of this node will be:
        | user_id | ad_id_1d    | ad_id_3d    | value_max_1d | value_max_3d | anchor_time |
        |---------|-------------|-------------|--------------|--------------|-------------|
        | a       | [1, 2]      | [1, 2, 3]   | [1, 2]       | [11, 12, 13] | 1           |
        | a       | [1, 2]      | [1, 2]      | [1, 2]       | [21, 22]     | 2           |

    Attributes:
        full_aggregation_node: The input node, which is always a full aggregation node.
        fdw: The feature definition wrapper that contains the useful metadata.
        group_by_columns: The columns to group by when rolling up the secondary key and its corresponding feature values.
    """

    full_aggregation_node: SparkExecNode
    fdw: FeatureDefinitionWrapper
    group_by_columns: Tuple[str, ...]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = self.full_aggregation_node.to_dataframe(spark)

        window_to_features = self.fdw.window_to_features_map_for_secondary_keys
        # Put all columns in each distinct window into a struct column with name "_struct_{window}", and then collect
        # all struct values in each column into a list by grouping on join keys and anchor time.
        temp_struct_columns = [
            F.struct(*cols).alias(temp_struct_column_name(window)) for window, cols in window_to_features.items()
        ]
        temp_struct_column_names = [temp_struct_column_name(window) for window in window_to_features.keys()]

        # Rollup aggregation secondary keys and corresponding feature values by collecting struct values into a list so
        # that for each unique join keys and anchor time pair, we have a list of seoncdary keys and features for each
        # distinct window.
        df = (
            df.select(*df.columns, *temp_struct_columns)
            .groupBy(*self.group_by_columns)
            .agg(*[F.collect_list(c).alias(c) for c in temp_struct_column_names])
        )
        return self._transform_temp_struct_to_feature_columns(df)

    def _transform_temp_struct_to_feature_columns(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
            time_window = secondary_key_output.time_window
            temp_struct_column = temp_struct_column_name(time_window)

            # Filter out secondary keys that don't appear in a given window
            df = self._filter_aggregation_secondary_key_by_indicator(df, time_window, temp_struct_column)

            # Sort the secondary key values in ascending order.
            sort_function = f"(left, right) -> case when left.{self.fdw.aggregation_secondary_key} < right.{self.fdw.aggregation_secondary_key} then -1 when left.{self.fdw.aggregation_secondary_key} > right.{self.fdw.aggregation_secondary_key} then 1 else 0 end"
            df = df.withColumn(temp_struct_column, F.expr(f"array_sort({temp_struct_column}, {sort_function})"))

            # Extract each feature value in the struct into its own column.
            df = self._extract_features_columns_from_struct_columns(df, time_window, temp_struct_column)

            # Extract the secondary key values in the struct into its own column.
            df = df.withColumn(
                secondary_key_output.name,
                F.expr(f"transform({temp_struct_column}, x -> x.{self.fdw.aggregation_secondary_key})"),
            )

            df = df.drop(temp_struct_column)
        return df

    def _filter_aggregation_secondary_key_by_indicator(
        self, df: pyspark.sql.DataFrame, window: TimeWindowSpec, temp_struct_column_name: str
    ) -> pyspark.sql.DataFrame:
        # Filter out those secondary keys with their corresponding feature values in this time window if the
        # indicator column is `null`. We use a window based `sum` on the aggregation secondary key in
        # `AsofJoinFullAggNode` so that the indicator column is `null` for those secondary keys that are not present.
        return df.withColumn(
            temp_struct_column_name,
            F.filter(
                temp_struct_column_name,
                lambda x: x.getField(temp_indictor_column_name(window)).isNotNull(),
            ),
        )

    def _extract_features_columns_from_struct_columns(
        self, df: pyspark.sql.DataFrame, window: TimeWindowSpec, temp_struct_column_name: str
    ) -> pyspark.sql.DataFrame:
        for agg_feature in self.fdw.trailing_time_window_aggregation().features:
            if create_time_window_spec_from_data_proto(agg_feature.time_window) == window:
                df = df.withColumn(
                    agg_feature.output_feature_name,
                    F.expr(f"transform({temp_struct_column_name}, x -> x.{agg_feature.output_feature_name})"),
                )
        return df


@attrs.frozen
class InnerJoinOnRangeSparkNode(SparkExecNode):
    """Joins the left against the right, using the right columns as the conditional.

    In pseudo-sql it is:
        SELECT
            left.*
            right.*
        FROM
            left INNER JOIN right
            ON (right.right_inclusive_start_column IS null OR left.left_join_condition_column >= right.right_inclusive_start_column)
                AND left.left_join_condition_column < right.right_exclusive_end_column)
    """

    left: SparkExecNode
    right: SparkExecNode
    left_join_condition_column: str
    right_inclusive_start_column: str
    right_exclusive_end_column: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark).alias("left_join_df")
        right_df = self.right.to_dataframe(spark).alias("right_join_df")

        join_condition = (
            # If start_time is not null, use the regular condition
            (
                F.isnull(right_df[self.right_inclusive_start_column])
                | (left_df[self.left_join_condition_column] >= right_df[self.right_inclusive_start_column])
            )
            & (left_df[self.left_join_condition_column] < right_df[self.right_exclusive_end_column])
        )

        # NOTE: the broadcast is important since the Spark query optimizer is not able to infer it on DataFrames defined in memory (as of Spark 3.2).
        return left_df.join(F.broadcast(right_df), join_condition, "inner")


@attrs.frozen
class TakeLastRowSparkNode(SparkExecNode):
    input_node: SparkExecNode
    partition_by_columns: Tuple[str, ...]
    order_by_column: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark).alias("input_node_df")
        window = spark_window.Window.partitionBy(*self.partition_by_columns).orderBy(F.col(self.order_by_column).desc())
        row_number_col = "__tecton_row_num"
        assert row_number_col not in input_df.columns
        df = input_df.withColumn(row_number_col, F.row_number().over(window))
        df = df.filter(F.col(row_number_col) == 1).drop(row_number_col)
        return df


@attrs.frozen
class TemporalBatchTableFormatSparkNode(SparkExecNode):
    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper = attrs.field()
    online_batch_table_part: OnlineBatchTablePart

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark).alias("input_node_df")
        df = input_df.select(
            *self.fdw.join_keys,
            F.lit(self.online_batch_table_part.window_index)
            .cast("long")
            .alias(aggregation_group_id()),  # Cast for equivalence with aggregate QT.
            F.array(F.struct(*self.online_batch_table_part.schema.column_names())).alias(
                str(self.online_batch_table_part.window_index)
            ),
        )
        return df


@attrs.frozen
class ExplodeTimestampByTimeWindowsSparkNode(SparkExecNode):
    """
    Explodes each timestamp in 'column_name' into multiple rows, each with a new timestamp
    that is the sum of the time and the time window.
    """

    input_node: SparkExecNode
    timestamp_field: str
    fdw: FeatureDefinitionWrapper
    time_filter: pendulum.Period
    sawtooth_aggregation_data: Optional[compaction_utils.SawtoothAggregationData]
    include_original_anchor_time: bool

    def _get_time_deltas_for_sawtooth_anchor_time_cols(self) -> Dict[str, Set[int]]:
        """Calculate the aggregation tine windows to add to the anchor_time_for_X_sawtooth columns by.

        For sawtooth aggregations, datapoints are included in the aggregation window immediately and do not expire out of the aggregation window until the sawtooth tile on the trailing edge is dropped.
        For this reason, we calculate the time delta where the data is dropped as _anchor_time_for_sawtooth_tile + sawtooth_tile_size + aggregation_window_size.
        See https://www.notion.so/tecton/Get-Features-in-Range-For-Sawtooths-e1909b18f0ce427094d73cc946637734 for more information.

        Take a 10d agg which has 1d sawtooth tiles for example, if a datapoint occurs on 12/20/2024 12:03:15:
            - it will be included in the aggregation window at 12/20/2024 12:03:15
            - it will be dropped from aggregation window at 12/31/2024 00:00:00
        Each sawtooth tile size has a corresponding anchor_time column, such as _anchor_time_for_day_sawtooth.
        For our above example this looks like:
            - _anchor_time = 12/20/2024 12:03:15
            - _anchor_time_for_day_sawtooth = 12/20/2024 00:00:00
            - sawtooth_tile_size = 1 day
        Then we add _anchor_time_for_day_sawtooth + sawtooth_tile_size + aggregation_window_size and get 12/31/2024 00:00:00!
            - 12/20/2024 00:00:00 + 1d + 10d = 12/31/2024 00:00:00

        """
        assert self.sawtooth_aggregation_data is not None, "Sawtooth aggregation data must be provided"

        anchor_time_columns = self.sawtooth_aggregation_data.get_anchor_time_columns()
        column_to_time_deltas = {anchor_time_col: set() for anchor_time_col in anchor_time_columns}
        for feature in self.fdw.materialized_fv_spec.aggregate_features:
            time_window = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(time_window, RelativeTimeWindowSpec):
                sawtooth_aggregate_feature = self.sawtooth_aggregation_data.aggregations[feature.output_feature_name]
                # For non sawtooth continuous features, we need to subtract 1 second since the both bounds of the aggregation window are inclusive. This is different than normal continuous features.
                window_start = time_window.window_start - (
                    sawtooth_aggregate_feature.batch_sawtooth_tile_size or timedelta(seconds=1)
                )
                window_start_abs = convert_timedelta_for_version(
                    abs(window_start), self.fdw.get_feature_store_format_version
                )
                column_to_time_deltas[sawtooth_aggregate_feature.anchor_time_column].add(window_start_abs)
        return column_to_time_deltas

    def _get_time_deltas_for_anchor_time_col(self) -> List[int]:
        """Calculate the aggregation time windows to add to the anchor_time column by."""
        time_deltas = set()
        for feature in self.fdw.materialized_fv_spec.aggregate_features:
            time_window = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(time_window, LifetimeWindowSpec):
                time_deltas.add(timedelta(0))

            elif isinstance(time_window, TimeWindowSeriesSpec):
                for time_window in time_window.time_windows:
                    if self.include_original_anchor_time:
                        time_deltas.update((time_window.window_start, time_window.window_end))
                    else:
                        time_deltas.add(time_window.window_start)

            elif isinstance(time_window, RelativeTimeWindowSpec):
                if self.sawtooth_aggregation_data:
                    # For sawtooth features, the window start is added to sawtooth time columns in _get_time_deltas_for_sawtooth_anchor_time_cols.
                    time_deltas.add(time_window.window_end)
                else:
                    if self.include_original_anchor_time:
                        time_deltas.update((time_window.window_start, time_window.window_end))
                    else:
                        time_deltas.add(time_window.window_start)

            else:
                msg = f"Invalid time_window type: {type(time_window)}"
                raise ValueError(msg)

        time_deltas_ns = [
            convert_timedelta_for_version(abs(td), self.fdw.get_feature_store_format_version) for td in time_deltas
        ]
        return time_deltas_ns

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        spine_df = self.input_node.to_dataframe(spark)

        tds_for_anchor_time_col = self._get_time_deltas_for_anchor_time_col()
        new_anchor_times = [F.col(anchor_time()) + F.lit(td) for td in tds_for_anchor_time_col]
        if self.sawtooth_aggregation_data:
            # For sawtooth aggregations, we need to add the aggregation window to the sawtooth anchor time columns, not `anchor_time`.
            sawtooth_column_to_tds = self._get_time_deltas_for_sawtooth_anchor_time_cols()
            for anchor_time_col, time_deltas in sawtooth_column_to_tds.items():
                new_anchor_times += [F.col(anchor_time_col) + F.lit(td) for td in list(time_deltas)]

        new_anchor_time_array_col = F.array(*new_anchor_times)
        df_exploded = spine_df.withColumn(anchor_time(), F.explode(new_anchor_time_array_col))

        start_time_ns = convert_timestamp_for_version(self.time_filter.start, self.fdw.get_feature_store_format_version)
        df_exploded = df_exploded.withColumn(
            anchor_time(),
            F.when(
                (F.col(anchor_time()) <= start_time_ns),
                F.lit(start_time_ns),
            ).otherwise(F.col(anchor_time())),
        )

        end_time_ns = convert_timestamp_for_version(self.time_filter.end, self.fdw.get_feature_store_format_version)
        df_exploded = df_exploded.filter(df_exploded[anchor_time()] < end_time_ns)

        return df_exploded.dropDuplicates()


@attrs.frozen
class _UnionImplSparkNode:
    """
    A node that unions two dataframes together.
    """

    left: pyspark.sql.DataFrame
    right: pyspark.sql.DataFrame

    def union(self) -> pyspark.sql.DataFrame:
        common_cols = set(self.left.columns) & set(self.right.columns)
        left_only_columns = set(self.left.columns) - common_cols
        right_only_columns = set(self.right.columns) - common_cols

        left_full_cols = (
            [F.col(x) for x in common_cols]
            + [F.col(x) for x in left_only_columns]
            + [F.lit(None).alias(x) for x in right_only_columns]
        )
        right_full_cols = (
            [F.col(x) for x in common_cols]
            + [F.lit(None).alias(x) for x in left_only_columns]
            + [F.col(x) for x in right_only_columns]
        )
        left_df = self.left.select(left_full_cols)
        right_df = self.right.select(right_full_cols)
        return left_df.union(right_df)


@attrs.frozen
class AsofJoinSawtoothAggSparkNode(SparkExecNode):
    batch_input_node: SparkExecNode
    stream_input_node: SparkExecNode
    spine_input_node: SparkExecNode
    sawtooth_aggregation_data: compaction_utils.SawtoothAggregationData
    fdw: FeatureDefinitionWrapper

    def _add_output_feature_name_cols(self, stream_df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        # Match the schema of the batch input node which has a column for each partial aggregate column x time window.
        time_aggregation = self.fdw.trailing_time_window_aggregation()
        new_columns = []
        new_column_names = set()
        cols_to_drop = set()
        for feature in time_aggregation.features:
            # TODO(samantha): verify col_datatype is correct for last/first n aggregations
            col_datatype = self.fdw.view_schema.to_dict()[feature.input_feature_name]
            time_window = create_time_window_spec_from_data_proto(feature.time_window)
            aggregation_plan = get_aggregation_plan(
                feature.function,
                feature.function_params,
                time_aggregation.is_continuous,
                time_aggregation.time_key,
                col_datatype,
            )
            partial_aggregate_column_names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            intermediate_partial_aggregate_column_names = [
                temp_intermediate_partial_aggregate_column_name(name, time_window)
                for name in partial_aggregate_column_names
            ]
            for input_name, output_name in zip(
                partial_aggregate_column_names, intermediate_partial_aggregate_column_names
            ):
                if output_name in new_column_names:
                    continue
                new_column_names.add(output_name)
                new_columns.append(F.col(input_name).alias(output_name))
            cols_to_drop.update(partial_aggregate_column_names)

        columns_to_keep = [col for col in stream_df.columns if col not in cols_to_drop]
        return stream_df.select(*columns_to_keep, *new_columns)

    def _add_time_partition_columns(self, input_df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        output_df = input_df
        seen_partition_columns = set()
        for agg in self.sawtooth_aggregation_data.aggregations.values():
            partition_col = agg.time_partition_column
            # Aggregations can share the same partition and anchor time columns.
            if partition_col is None or partition_col in seen_partition_columns:
                continue
            anchor_time_column = agg.anchor_time_column
            interval_seconds = time_utils.convert_timedelta_for_version(
                agg.batch_sawtooth_tile_size, self.fdw.get_feature_store_format_version
            )
            output_df = output_df.withColumn(
                partition_col, F.col(anchor_time_column) - F.col(anchor_time_column) % interval_seconds
            )
        return output_df

    def _drop_time_partition_columns(self, input_df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        output_df = input_df
        for partition_col in self.sawtooth_aggregation_data.get_truncated_timestamp_partition_columns():
            output_df = output_df.drop(partition_col)
        return output_df

    def _get_aggregations(self, join_spec: _AsofJoinerAndWindowAggregator) -> List[pyspark.sql.Column]:
        time_aggregation = self.fdw.trailing_time_window_aggregation()
        aggregations = []
        for feature in time_aggregation.features:
            col_datatype = self.fdw.view_schema.to_dict()[feature.input_feature_name]
            aggregation_plan = get_aggregation_plan(
                feature.function,
                feature.function_params,
                time_aggregation.is_continuous,
                time_aggregation.time_key,
                col_datatype,
            )
            time_window = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(time_window, TimeWindowSeriesSpec):
                msg = "TimeWindowSeriesSpec is not supported for sawtooth aggregation"
                raise ValueError(msg)

            sawtooth_agg_feature = self.sawtooth_aggregation_data.get_sawtooth_aggregation_for_output_feature_name(
                feature.output_feature_name
            )
            if sawtooth_agg_feature.use_continuous_range_query:
                # Use range query for continuous aggregations < 2 days. Note, we override the tile interval to 0 so the time range is [start, end]. This is different than the default behavior of continuous feature views which is (start, end].
                start, end = self.fdw.time_range_for_relative_time_window(
                    time_window, aggregation_tile_interval_override=0
                )
                window_spec = join_spec.get_range_between_window_spec(
                    start * 2 - 1,
                    end * 2 - 1,
                    timestamp_col=sawtooth_agg_feature.anchor_time_column,
                    extra_partition_cols=[sawtooth_agg_feature.identifier_partition_column],
                )
            else:
                window_spec = join_spec.get_range_between_window_spec(
                    spark_window.Window.unboundedPreceding,
                    spark_window.Window.currentRow,
                    timestamp_col=sawtooth_agg_feature.anchor_time_column,
                    extra_partition_cols=[
                        sawtooth_agg_feature.time_partition_column,
                        sawtooth_agg_feature.identifier_partition_column,
                    ],
                )
            partial_aggregate_column_names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            intermediate_partial_aggregate_column_names = [
                temp_intermediate_partial_aggregate_column_name(name, time_window)
                for name in partial_aggregate_column_names
            ]
            agg = aggregation_plan.full_aggregation_transform(intermediate_partial_aggregate_column_names, window_spec)
            aggregations.append(agg.alias(feature.output_feature_name))

        # If the aggregation secondary key appears, we run a window based aggregation on the secondary key
        # indicator column to identify if the secondary appears in each distinct window. `sum` function is arbitrary
        # here, and we just need a function to return `null` value if the secondary key does not appear in the window.
        if self.fdw.aggregation_secondary_key:
            for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
                secondary_sawtooth_agg_feature = (
                    self.sawtooth_aggregation_data.get_sawtooth_aggregate_feature_or_secondary_key_feature(
                        secondary_key_output.name
                    )
                )
                indicator_column_name = temp_indictor_column_name(secondary_key_output.time_window)

                extra_partition_cols = [
                    secondary_sawtooth_agg_feature.identifier_partition_column,
                ]
                if secondary_sawtooth_agg_feature.time_partition_column is not None:
                    extra_partition_cols.append(secondary_sawtooth_agg_feature.time_partition_column)

                if secondary_sawtooth_agg_feature.use_continuous_range_query:
                    start, end = self.fdw.time_range_for_relative_time_window(
                        secondary_key_output.time_window, aggregation_tile_interval_override=0
                    )
                    secondary_window_spec = join_spec.get_range_between_window_spec(
                        start * 2 - 1,
                        end * 2 - 1,
                        timestamp_col=secondary_sawtooth_agg_feature.anchor_time_column,
                        extra_partition_cols=extra_partition_cols,
                    )
                else:
                    secondary_window_spec = join_spec.get_range_between_window_spec(
                        spark_window.Window.unboundedPreceding,
                        spark_window.Window.currentRow,
                        timestamp_col=secondary_sawtooth_agg_feature.anchor_time_column,
                        extra_partition_cols=extra_partition_cols,
                    )
                aggregations.append(
                    F.sum(indicator_column_name).over(secondary_window_spec).alias(indicator_column_name)
                )
        return aggregations

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        batch_input_df = self.batch_input_node.to_dataframe(spark)
        stream_input_df = self.stream_input_node.to_dataframe(spark)
        stream_input_df = self._add_output_feature_name_cols(stream_input_df)
        partition_columns = self.fdw.join_keys
        if self.fdw.aggregation_secondary_key:
            partition_columns.append(self.fdw.aggregation_secondary_key)

            # If the aggregation secondary key appears, we add indicator columns to the partial aggregation result to
            # help identify all secondary keys that are present in each distinct time window. These columns already exists for the batch_input.
            for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
                stream_input_df = stream_input_df.withColumn(
                    temp_indictor_column_name(secondary_key_output.time_window), F.lit(1)
                )

        events_df = _UnionImplSparkNode(left=batch_input_df, right=stream_input_df).union()
        events_df = self._add_time_partition_columns(events_df)

        timestamp_cols = self.sawtooth_aggregation_data.get_anchor_time_columns()
        agg_specific_partition_columns = (
            self.sawtooth_aggregation_data.get_identifier_partition_columns()
            + self.sawtooth_aggregation_data.get_truncated_timestamp_partition_columns()
        )

        spine_df = self._add_time_partition_columns(self.spine_input_node.to_dataframe(spark))
        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=spine_df,
            right_df=events_df,
            left_ts_cols=timestamp_cols,
            right_ts_cols=timestamp_cols,
            partition_cols=partition_columns,
            extra_partition_cols=agg_specific_partition_columns,
            use_window_range_between_value=self.sawtooth_aggregation_data.contains_continuous_non_sawtooth_aggregations(),
        )
        aggregations = self._get_aggregations(join_spec)
        result_df = join_spec.join_and_aggregate(aggregations)
        return self._drop_time_partition_columns(result_df)


@attrs.frozen
class UnionSparkNode(SparkExecNode):
    left: SparkExecNode
    right: SparkExecNode

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)
        return _UnionImplSparkNode(left=left_df, right=right_df).union()


@attrs.frozen
class AsofJoinReducePartialAggSparkNode(SparkExecNode):
    """
    An asof join very similar to AsofJoinFullAggNode, but with a change where it does
    a partial aggregation rollup (rather than a full).

    NOTE: This should only be used for window aggregates.

    LEFT asof_join RIGHT has the following behavior:
        For each row in the spine, find the matching partial aggregates (by time range)
        and run the appropriate intermediate partial aggregate over those rows.

    The result is a dataframe with the same number of rows as the spine, with
    additional columns of the partially aggregated features (or null) for each aggregation time window.

    There are a few ways this behavior can be implemented, but by test the best
    performing method has been to union the two inputs and use a window
    function for the aggregates.
    """

    spine: SparkExecNode
    partial_agg_node: SparkExecNode
    fdw: FeatureDefinitionWrapper
    sawtooth_aggregation_data: compaction_utils.SawtoothAggregationData
    TECTON_AGG_WINDOW_ORDER_COL: ClassVar[str] = "_tecton_agg_window_order_col"

    def _generate_aggregation_window_spec(
        self,
        time_window: TimeWindowSpec,
        join_spec: _AsofJoinerAndWindowAggregator,
        feature_name: str,
    ) -> spark_window.WindowSpec:
        # Since the spine and feature rows are unioned together, the spine rows must be ordered after the feature rows
        # when they have the same timestamp for window aggregation to be correct. Window aggregation does not allow
        # ordering using two columns when range between is used. As a workaround, we multiply the left rows by (* 2 + 1).
        # The right rows by * 2. This will ensure the left rows will be sorted after the right rows.
        # We need to make an adjustment here to earliest_anchor_time due to these changes.
        if isinstance(time_window, RelativeTimeWindowSpec):
            sawtooth_agg_feature = (
                self.sawtooth_aggregation_data.get_sawtooth_aggregate_feature_or_secondary_key_feature(feature_name)
            )
            timestamp_col = sawtooth_agg_feature.anchor_time_column
            extra_partition_columns = [sawtooth_agg_feature.identifier_partition_column]
            aggregation_tile_interval_map = self.sawtooth_aggregation_data.get_anchor_time_to_aggregation_interval_map(
                self.fdw.get_tile_interval_for_sawtooths, self.fdw.get_feature_store_format_version
            )
            start, end = self.fdw.time_range_for_relative_time_window(
                time_window, aggregation_tile_interval_override=aggregation_tile_interval_map[timestamp_col]
            )

            return join_spec.get_range_between_window_spec(
                start * 2 - 1,
                end * 2 - 1,
                timestamp_col=timestamp_col,
                extra_partition_cols=extra_partition_columns,
            )
        elif isinstance(time_window, LifetimeWindowSpec):
            sawtooth_agg_feature = (
                self.sawtooth_aggregation_data.get_sawtooth_aggregate_feature_or_secondary_key_feature(feature_name)
            )
            timestamp_col = sawtooth_agg_feature.anchor_time_column
            extra_partition_columns = [sawtooth_agg_feature.identifier_partition_column]

            return join_spec.get_range_between_window_spec(
                spark_window.Window.unboundedPreceding,
                spark_window.Window.currentRow,
                timestamp_col=timestamp_col,
                extra_partition_cols=extra_partition_columns,
            )
        else:
            msg = f"Invalid time_window type: {type(time_window)}"
            raise TypeError(msg)

    def _get_aggregations(self, join_spec: _AsofJoinerAndWindowAggregator) -> List[pyspark.sql.Column]:
        time_aggregation = self.fdw.trailing_time_window_aggregation()
        aggregations = []
        seen_output_partial_aggregate_column_names = set()
        for feature in time_aggregation.features:
            col_datatype = self.fdw.view_schema.to_dict()[feature.input_feature_name]
            aggregation_plan = get_aggregation_plan(
                feature.function,
                feature.function_params,
                time_aggregation.is_continuous,
                time_aggregation.time_key,
                col_datatype,
            )
            time_window = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(time_window, TimeWindowSeriesSpec):
                msg = "TimeWindowSeriesSpec is not supported for sawtooth aggregation"
                raise NotImplementedError(msg)

            sawtooth_agg_feature = self.sawtooth_aggregation_data.get_sawtooth_aggregation_for_output_feature_name(
                feature.output_feature_name
            )
            materialized_column_names = aggregation_plan.materialized_column_names(
                feature.input_feature_name
            )  # output of partial agg node
            output_partial_aggregate_column_names = [
                temp_intermediate_partial_aggregate_column_name(name, time_window) for name in materialized_column_names
            ]

            if sawtooth_agg_feature.use_continuous_range_query:
                # This fv contains sawtooth aggregations, but this particular aggregation does not use sawtoothing.
                # Do not do the full agg rollup here, since we will do it in AsofJoinSawtoothAggNode.
                aggs_to_add = [
                    F.lit(None).alias(output_name)
                    for output_name in output_partial_aggregate_column_names
                    if output_name not in seen_output_partial_aggregate_column_names
                ]
            else:
                window_spec = self._generate_aggregation_window_spec(
                    time_window, join_spec, feature.output_feature_name
                )
                partial_aggregations = aggregation_plan.reduce_partial_aggregation_transform(
                    materialized_column_names, window_spec
                )
                aggs_to_add = [
                    partial_agg_column.alias(output_name)
                    for partial_agg_column, output_name in zip(
                        partial_aggregations, output_partial_aggregate_column_names
                    )
                    if output_name not in seen_output_partial_aggregate_column_names
                ]
            aggregations += aggs_to_add
            seen_output_partial_aggregate_column_names.update(output_partial_aggregate_column_names)

        # If the aggregation secondary key appears, we run a window based aggregation on the secondary key
        # indicator column to identify if the secondary appears in each distinct window. `sum` function is arbitrary
        # here, and we just need a function to return `null` value if the secondary key does not appear in the window.
        if self.fdw.aggregation_secondary_key:
            for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
                secondary_sawtooth_agg_feature = (
                    self.sawtooth_aggregation_data.get_sawtooth_aggregate_feature_or_secondary_key_feature(
                        secondary_key_output.name
                    )
                )
                output_secondary_column_name = (
                    f"{tecton_secondary_key_aggregation_indicator_col()}_{secondary_key_output.time_window.to_string()}"
                )
                if secondary_sawtooth_agg_feature.use_continuous_range_query:
                    aggregations.append(F.lit(None).alias(output_secondary_column_name))
                else:
                    aggregations.append(
                        F.sum(tecton_secondary_key_aggregation_indicator_col())
                        .over(
                            self._generate_aggregation_window_spec(
                                secondary_key_output.time_window,
                                join_spec,
                                secondary_sawtooth_agg_feature.name,
                            )
                        )
                        .alias(output_secondary_column_name)
                    )
        return aggregations

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.spine.to_dataframe(spark)
        right_df = self.partial_agg_node.to_dataframe(spark)

        partition_columns = self.fdw.join_keys
        agg_specific_partition_columns = self.sawtooth_aggregation_data.get_identifier_partition_columns()
        if self.fdw.aggregation_secondary_key:
            partition_columns.append(self.fdw.aggregation_secondary_key)

            # If the aggregation secondary key appears, we add an indicator column to the partial aggregation result to
            # help identify all secondary keys that are present in each distinct time window.
            right_df = right_df.withColumn(tecton_secondary_key_aggregation_indicator_col(), F.lit(1))

        timestamp_cols = self.sawtooth_aggregation_data.get_anchor_time_columns()
        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=left_df,
            right_df=right_df,
            left_ts_cols=timestamp_cols,
            right_ts_cols=timestamp_cols,
            partition_cols=partition_columns,
            extra_partition_cols=agg_specific_partition_columns,
            use_window_range_between_value=True,
        )
        aggregations = self._get_aggregations(join_spec)
        return join_spec.join_and_aggregate(aggregations)
