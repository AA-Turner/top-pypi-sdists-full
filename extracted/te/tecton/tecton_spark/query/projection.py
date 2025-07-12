import itertools
from datetime import timedelta
from functools import reduce
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pyspark
import pyspark.sql.window as spark_window
from pyspark.sql import functions as F
from pyspark.sql.functions import expr
from pyspark.sql.types import ArrayType
from pyspark.sql.types import LongType

import tecton_core.tecton_pendulum as pendulum
from tecton_core import time_utils as core_time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.feature_extraction_sql_builder import FeatureExtractionSqlBuilder
from tecton_core.query_consts import TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import valid_from
from tecton_core.query_consts import valid_to
from tecton_core.specs import MaterializedFeatureViewSpec
from tecton_core.specs import MaterializedFeatureViewType
from tecton_proto.common.aggregation_function__client_pb2 import AggregationFunction
from tecton_proto.data import feature_view__client_pb2 as feature_view__data_pb2
from tecton_spark.query.node import SparkExecNode
from tecton_spark.time_utils import convert_epoch_to_timestamp_column
from tecton_spark.time_utils import convert_timestamp_to_epoch


@attrs.frozen
class AddAnchorTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_store_format_version: int
    batch_schedule: int
    timestamp_field: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        anchor_time_val = convert_timestamp_to_epoch(F.col(self.timestamp_field), self.feature_store_format_version)
        df = input_df.withColumn(
            anchor_time(),
            anchor_time_val - anchor_time_val % self.batch_schedule,
        )
        return df


@attrs.frozen
class AddRetrievalAnchorTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    name: str
    feature_store_format_version: int
    batch_schedule: int
    tile_interval: int
    timestamp_field: str
    is_stream: bool
    data_delay_seconds: Optional[int] = 0

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        anchor_time_val = convert_timestamp_to_epoch(
            F.col(self.timestamp_field) - expr(f"interval {self.data_delay_seconds} seconds"),
            self.feature_store_format_version,
        )
        # tile_interval will be 0 for continuous
        if self.tile_interval == 0:
            df = input_df.withColumn(anchor_time(), anchor_time_val)
        else:
            # For stream, we use the tile interval for bucketing since the data is available as soon as
            # the aggregation interval ends.
            # For BAFV, we use the batch schedule to get the last tile written.
            if self.is_stream:
                df = input_df.withColumn(
                    anchor_time(),
                    anchor_time_val - anchor_time_val % self.tile_interval - self.tile_interval,
                )
            else:
                df = input_df.withColumn(
                    anchor_time(),
                    anchor_time_val - anchor_time_val % self.batch_schedule - self.tile_interval,
                )
        return df


@attrs.frozen
class MultiRtfvFeatureExtractionSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_definition_namespaces: List[Tuple[FeatureDefinitionWrapper, str]]
    events_df_timestamp_field: str
    use_namespace_feature_prefix: bool = True

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        sql_builder = FeatureExtractionSqlBuilder(
            self.events_df_timestamp_field,
            self.input_node.columns,
            ComputeMode.SPARK,
            self.use_namespace_feature_prefix,
        )

        feature_query_terms = []
        for fdw, namespace in self.feature_definition_namespaces:
            feature_query_terms.extend(sql_builder.extract_rtfv_features(fdw, namespace))

        # quote_char="`" is necessary to ensure column references show up as `select `column_name`` instead of `select 'column_name'`.
        feature_sql_exprs = [expr(col.get_sql(with_alias=True, quote_char="`")) for col in feature_query_terms]
        return input_df.select("*", *feature_sql_exprs)


@attrs.frozen
class RenameColsSparkNode(SparkExecNode):
    input_node: SparkExecNode
    mapping: Optional[Dict[str, Union[str, List[str]]]]
    drop: Optional[List[str]]
    keep_original_columns_from_mapping: bool = False

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        if self.mapping:
            rename_cols = []
            for old_name, new_name in self.mapping.items():
                if not new_name:
                    continue
                if isinstance(new_name, list):
                    for col in sorted(new_name):
                        rename_cols.append(F.col(old_name).alias(col))
                else:
                    rename_cols.append(F.col(old_name).alias(new_name))

                if self.keep_original_columns_from_mapping:
                    rename_cols.append(F.col(old_name))
            existing_cols = [col for col in input_df.columns if col not in self.mapping.keys()]
            input_df = input_df.select(*existing_cols, *rename_cols)

        if self.drop:
            input_df = input_df.drop(*self.drop)

        return input_df


@attrs.frozen
class ConvertEpochToTimestampSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_store_formats: Dict[str, int]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        for name, feature_store_format_version in self.feature_store_formats.items():
            input_df = input_df.withColumn(
                name,
                convert_epoch_to_timestamp_column(F.col(name), feature_store_format_version),
            )
        return input_df


@attrs.frozen
class ConvertTimestampToUTCSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_key: str
    batch_publish_timestamp: Optional[str] = None  # optionally set for Materialized Feature Views only

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        # Spark timestamps are always in UTC, hence no conversion is done
        return self.input_node.to_dataframe(spark)


@attrs.frozen
class AddAnchorTimeColumnsForSawtoothIntervalsSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_field: str
    anchor_time_column_map: Dict[str, timedelta]
    data_delay_seconds: int
    feature_store_format_version: int
    aggregation_tile_interval_column_map: Dict[str, int]
    truncate_to_recent_complete_tile: bool

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        if self.timestamp_field != anchor_time():
            anchor_time_val = convert_timestamp_to_epoch(
                F.col(self.timestamp_field) - expr(f"interval {self.data_delay_seconds} seconds"),
                self.feature_store_format_version,
            )
        else:
            anchor_time_val = F.col(self.timestamp_field)

        columns = [F.col(column) for column in self.input_node.columns]
        new_timestamp_columns = []
        for column_name, unit in self.anchor_time_column_map.items():
            interval_seconds = core_time_utils.convert_timedelta_for_version(unit, self.feature_store_format_version)
            if interval_seconds == 0:
                spark_column = anchor_time_val.alias(column_name)
            else:
                aggregation_tile_interval = (
                    self.aggregation_tile_interval_column_map[column_name]
                    if self.truncate_to_recent_complete_tile
                    else 0
                )
                spark_column = (anchor_time_val - anchor_time_val % interval_seconds - aggregation_tile_interval).alias(
                    column_name
                )
            new_timestamp_columns.append(spark_column)
        return input_df.select(*columns, *new_timestamp_columns)


@attrs.frozen
class AdjustAnchorTimeToWindowEndSparkNode(SparkExecNode):
    input_node: SparkExecNode
    anchor_time_columns: List[str]
    aggregation_tile_interval_column_map: Dict[str, int]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        output_df = self.input_node.to_dataframe(spark)
        for column in self.anchor_time_columns:
            aggregation_tile_interval = self.aggregation_tile_interval_column_map[column]
            if aggregation_tile_interval != 0:
                output_df = output_df.withColumn(column, F.col(column) + aggregation_tile_interval)
        return output_df


@attrs.frozen
class AddEffectiveTimestampSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_field: str
    effective_timestamp_name: str
    batch_schedule_seconds: int
    is_stream: bool
    data_delay_seconds: int

    # TODO(PRODENG-262): Remove use_legacy_temporal_aggregate_behavior flag once ghf is deprecated
    # use_legacy_temporal_aggregate_behavior is a flag used to preserve the behavior of deprecated function get_historical_features
    # we have not removed get_historical_features from the SDK in order to prevent upgrade friction
    use_legacy_temporal_aggregate_behavior: bool = False

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        # batch_schedule = 0 implies feature table.
        if self.batch_schedule_seconds == 0 or self.is_stream:
            effective_timestamp = F.col(self.timestamp_field)
        else:
            slide_str = f"{self.batch_schedule_seconds} seconds"
            timestamp_col = F.col(self.timestamp_field)
            if self.use_legacy_temporal_aggregate_behavior:
                timestamp_col -= expr("interval 1 microseconds")
            window_spec = F.window(timestamp_col, slide_str, slide_str)
            effective_timestamp = window_spec.end + expr(f"interval {self.data_delay_seconds} seconds")

        df = input_df.withColumn(self.effective_timestamp_name, effective_timestamp)
        return df


@attrs.frozen
class AddDurationSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_field: str
    duration: pendulum.Duration
    new_column_name: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.withColumn(
            self.new_column_name,
            F.col(self.timestamp_field) + expr(f"interval {self.duration.total_seconds()} seconds"),
        )


@attrs.frozen
class SelectDistinctSparkNode(SparkExecNode):
    input_node: SparkExecNode
    columns: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.select(self.columns).distinct()


@attrs.frozen
class AddBooleanPartitionColumnsSparkNode(SparkExecNode):
    input_node: SparkExecNode
    column_to_bool_map: Dict[str, bool]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        for column_name, value in self.column_to_bool_map.items():
            input_df = input_df.withColumn(column_name, F.lit(value))
        return input_df


@attrs.frozen
class ExplodeEventsByTimestampAndSelectDistinctSparkNode(SparkExecNode):
    """
    Explode the events in the input node and select distinct columns.
    """

    input_node: SparkExecNode
    explode_columns: List[str]
    explode_columns_to_boolean_columns: Dict[str, str]
    timestamp_column: str
    columns_to_ignore: List[str]

    def _add_identifier_columns(self, df: pyspark.sql.DataFrame, explode_column: str) -> pyspark.sql.DataFrame:
        columns_to_add = []
        for column in self.explode_columns:
            identifier = self.explode_columns_to_boolean_columns[column]
            if column == explode_column:
                columns_to_add.append(F.lit(True).alias(identifier))
            else:
                columns_to_add.append(F.lit(False).alias(identifier))
        return df.select("*", *columns_to_add)

    def _select_distinct_for_explode_column(
        self, input_df: pyspark.sql.DataFrame, explode_column: str
    ) -> pyspark.sql.DataFrame:
        new_df = self._add_identifier_columns(input_df, explode_column)
        other_columns = itertools.chain(
            self.columns_to_ignore,
            (col for col in self.explode_columns if col != explode_column),
        )
        for column in other_columns:
            new_df = new_df.withColumn(column, F.lit(None))
        return new_df.select(*self.columns).distinct()

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        union_df = self._select_distinct_for_explode_column(input_df, self.explode_columns[0])
        if len(self.explode_columns) == 1:
            return union_df

        for explode_column in self.explode_columns[1:]:
            intermediate_df = self._select_distinct_for_explode_column(input_df, explode_column)
            union_df = union_df.union(intermediate_df)
        return union_df


@attrs.frozen
class AggregationSecondaryKeyExplodeSparkNode(SparkExecNode):
    """
    This node returns all <entity, aggregation secondary key> pairs from the input node. It's used for retrieving
    secondary key aggregate features without spine.

    This node is similar to AsofSecondaryKeyExplodeSparkNode but doesn't require as-of join. It uses entities and
    anchor time to look back the max aggregation window time to find all secondary key values, and build a spine with
    all of them.
    """

    input_node: SparkExecNode
    join_keys: List[str]
    aggregation_secondary_key: str
    has_lifetime_aggregate: bool
    earliest_anchor_time_from_window_start: Optional[int]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        window_start = (
            spark_window.Window.unboundedPreceding
            if self.has_lifetime_aggregate
            else self.earliest_anchor_time_from_window_start
        )

        window_spec = (
            spark_window.Window.partitionBy(self.join_keys)
            .orderBy([anchor_time()])
            .rangeBetween(window_start, spark_window.Window.currentRow)
        )

        # Collect all secondary key values within the aggregation window, and explode them to build a spine.
        # Note the window based `collect_set` applies to every single row, so if a single join key has multiple
        # aggregation secondary keys with the same anchor time, the result dataframe will have multiple same rows for
        # that particular join key and anchor time. We select distinct here to deduplicate.
        input_df = (
            input_df.withColumn(
                TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL,
                F.collect_set(self.aggregation_secondary_key).over(window_spec),
            )
            .drop(self.aggregation_secondary_key)
            .distinct()
        )
        return input_df.withColumn(
            self.aggregation_secondary_key, F.explode(TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL)
        ).drop(TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL)


@attrs.frozen
class AddUniqueIdSparkNode(SparkExecNode):
    """
    Add a '_tecton_unique_id' column to the input node. This column is used to uniquely identify rows in the input node.

    Warning: The generated unique ID is non-deterministic on Spark, so this column may not be safe to join on.
    """

    input_node: SparkExecNode
    column_name: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.input_node.to_dataframe(spark).withColumn(self.column_name, F.monotonically_increasing_id())


def _is_count_feature(feature: feature_view__data_pb2.Aggregate) -> bool:
    return (
        feature.function == AggregationFunction.AGGREGATION_FUNCTION_COUNT
        or feature.function == AggregationFunction.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT
    )


@attrs.frozen
class DeriveValidityPeriodSparkNode(SparkExecNode):
    """
    Derives the `valid_from` and `valid_to` columns from a fully aggregated data frame
    and removes duplicates and rows with default values for all aggregation columns.
    """

    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper
    timestamp_field: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        join_keys = self.fdw.join_keys
        df = self.input_node.to_dataframe(spark)
        features = self.fdw.fv_spec.features
        window = spark_window.Window.partitionBy(*join_keys).orderBy(self.timestamp_field)

        df = df.withColumn(valid_from(), F.col(self.timestamp_field)).withColumn(
            valid_to(), F.lead(self.timestamp_field).over(window)
        )

        feature_value_update_conditions = [
            ~F.col(column).eqNullSafe(F.col(f"_tecton_prev_{column}")) for column in features
        ]
        track_changes_cols = list(features)

        if self.fdw.serving_ttl is not None:
            df = self._expire_ttl(df)

            # if `valid_from` is not equal to the previous `valid_to` (in the case of TTL expiry),
            # we should not merge the rows even though the feature values are equal
            track_changes_cols.append(valid_to())
            feature_value_update_conditions.append(~F.col(valid_from()).eqNullSafe(F.col(f"_tecton_prev_{valid_to()}")))

        previous_value_columns = [
            F.lag(column).over(window).alias(f"_tecton_prev_{column}") for column in track_changes_cols
        ]
        df = df.select("*", *previous_value_columns)

        # Check if any feature column changed in value, set is_new=1 for rows with changes
        df = df.withColumn(
            "_tecton_is_new", F.when(reduce(lambda x, y: x | y, feature_value_update_conditions), 1).otherwise(0)
        )

        # Cumulatively sum the `is_new` column to create "groups".
        # A group is a set of consecutive rows that has the same aggregated value.
        df = df.withColumn("_tecton_group", F.sum("_tecton_is_new").over(window))

        # if valid_to for a group is "null", we've reached the last event and the "max" should be null
        # since we don't know how long the value is valid
        null_check = F.max(F.when(F.col(valid_to()).isNull(), True).otherwise(False))
        df = df.groupBy(*join_keys, *features, "_tecton_group").agg(
            F.min(valid_from()).alias(valid_from()),
            F.when(null_check, F.lit(None)).otherwise(F.max(valid_to())).alias(valid_to()),
        )

        if isinstance(self.fdw.fv_spec, MaterializedFeatureViewSpec):
            if self.fdw.fv_spec.type == MaterializedFeatureViewType.TEMPORAL_AGGREGATE:
                df = self._remove_default_values(df)

        return df.drop("_tecton_group", self.timestamp_field)

    def _remove_default_values(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        """
        Removes rows with default values for all aggregation columns.
        """
        aggregate_features = self.fdw.fv_spec.aggregate_features
        is_default_value_conditions = []
        if self.fdw.aggregation_secondary_key:
            # For secondary key aggs, we remove rows that have empty rollup output lists
            column_names = [rollup_output.name for rollup_output in self.fdw.fv_spec.secondary_key_rollup_outputs]
            is_default_value_conditions.extend([F.size(F.col(column)) == 0 for column in column_names])
        else:
            for feature in aggregate_features:
                column_name = feature.output_feature_name
                if isinstance(df.schema[column_name].dataType, ArrayType):
                    all_counts_empty = F.size(F.array_except(column_name, F.array(F.lit(0)))) == 0
                    all_nulls = F.size(F.array_except(column_name, F.array(F.lit(None)))) == 0
                    if _is_count_feature(feature):
                        condition = all_counts_empty | all_nulls
                    else:
                        condition = all_nulls
                else:
                    if _is_count_feature(feature):
                        condition = F.col(column_name).isNull() | (F.col(column_name) == 0)
                    else:
                        condition = F.col(column_name).isNull()
                is_default_value_conditions.append(condition)

        return df.filter(~reduce(lambda x, y: x & y, is_default_value_conditions))

    def _expire_ttl(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        """
        Trims `valid_to` values according to TTL for non-aggregate feature views
        """
        ttl_seconds = self.fdw.serving_ttl.total_seconds()
        should_trim_valid_to = F.col(valid_to()).isNull() | (
            (F.col(valid_to()).cast(LongType()) - F.col(valid_from()).cast(LongType())) > ttl_seconds
        )
        df = df.withColumn(
            valid_to(),
            F.when(should_trim_valid_to, F.col(valid_from()) + expr(f"INTERVAL {ttl_seconds} SECONDS")).otherwise(
                F.col(valid_to())
            ),
        )

        return df
