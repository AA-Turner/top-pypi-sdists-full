from collections import defaultdict
from datetime import datetime
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

import pyspark
import pyspark.sql.functions as F
from pyspark.sql import Column

from tecton_core.aggregation_utils import get_materialization_aggregation_column_prefixes
from tecton_core.aggregation_utils import get_pretty_column_prefix
from tecton_core.query import compaction_utils
from tecton_core.query_consts import aggregation_group_id
from tecton_core.query_consts import aggregation_tile_id
from tecton_core.query_consts import anchor_time
from tecton_core.schema import Schema
from tecton_proto.data.feature_view__client_pb2 import TrailingTimeWindowAggregation
from tecton_spark.aggregation_plans import AggregationPlan
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.time_utils import convert_timestamp_to_epoch
from tecton_spark.time_utils import get_timestamp_in_seconds


WINDOW_COLUMN_NAME = "window"


def _get_feature_partial_aggregations(
    aggregation_plan: AggregationPlan, feature_name: str
) -> Iterator[Tuple[str, Column]]:
    column_names = set()
    input_columns = (
        aggregation_plan.intermediate_column_names(feature_name)
        if aggregation_plan.intermediate_column_prefixes is not None
        else [feature_name]
    )

    for column_name, aggregated_column in zip(
        aggregation_plan.materialized_column_names(feature_name),
        aggregation_plan.partial_aggregation_transform(input_columns),
    ):
        if column_name in column_names:
            continue
        column_names.add(column_name)

        yield column_name, aggregated_column.alias(column_name)


def _convert_window_to_anchor_time(
    output_df: pyspark.sql.DataFrame,
    is_continuous: bool,
    time_key: str,
    version: int,
    window_start_column_name: Optional[str],
    window_end_column_name: Optional[str],
    convert_window_times_to_epoch: bool,
) -> pyspark.sql.DataFrame:
    def _add_time_column(
        df: pyspark.sql.DataFrame, input_ts_column_name: str, output_column_name: str
    ) -> pyspark.sql.DataFrame:
        col = F.col(input_ts_column_name)
        return df.withColumn(
            output_column_name, convert_timestamp_to_epoch(col, version) if convert_window_times_to_epoch else col
        )

    # For continuous aggregations this will simply be the time key.
    if is_continuous:
        return _add_time_column(output_df, time_key, anchor_time())

    # Grouping by Spark Window introduces the "window" struct with "start" and "end" columns.
    # We only need to keep the "start" column as an anchor time.
    anchor_column_name = window_start_column_name if window_start_column_name else anchor_time()
    output_df = _add_time_column(output_df, f"{WINDOW_COLUMN_NAME}.start", anchor_column_name)

    if window_end_column_name:
        output_df = _add_time_column(output_df, f"{WINDOW_COLUMN_NAME}.end", window_end_column_name)

    return output_df.drop(WINDOW_COLUMN_NAME)


def construct_partial_time_aggregation_df(
    df: pyspark.sql.DataFrame,
    group_by_columns: List[str],
    time_aggregation: TrailingTimeWindowAggregation,
    version: int,
    view_schema: Schema,
    window_start_column_name: Optional[str] = None,
    window_end_column_name: Optional[str] = None,
    convert_to_epoch: bool = True,
    aggregation_anchor_time: Optional[datetime] = None,
) -> pyspark.sql.DataFrame:
    """Constructs a dataframe that performs partial aggregations on the input dataframe.

    Also removes the default window column that is generated, and replaces it with a start time column, and optionally
    an end time column.

    If the time aggregation is continuous, no aggregations will be performed. Instead, a start time column will be added
    but will simply be the same as the timestamp column in the input dataframe.

    Args:
        df: The input dataframe.
        group_by_columns: The columns to be grouped by for the partial aggregations.
        time_aggregation: The set of partial aggregations to be performed.
        version: The feature store version.
        window_start_column_name: If specified, the name of the start time column; otherwise it will use the default value "_anchor_time".
        window_end_column_name: If specified, the end time column will be included with this name.
        convert_to_epoch: If True, the window start and end times will be converted to epoch.
        aggregation_anchor_time: If specified, the offset for the aggregation windows.
        view_schema: The schema of the dataframe the partial aggregations are being performed for.

    Returns:
        A dataframe with the partial aggregations. For example, if `user_id` is the only join key, there are two
        aggregations (min and max), `window_start_column_name` is `tile_start_time`, `window_end_column_name` is
        `tile_end_time`, and `convert_to_epoch` is `False`, then the resulting dataframe might look something like:

        +-------+------------+------------+-------------------+-------------------+
        |user_id|value_min_1d|value_max_1d|    tile_start_time|      tile_end_time|
        +-------+------------+------------+-------------------+-------------------+
        |      1|           7|           9|2022-05-15 00:00:00|2022-05-16 00:00:00|
        |      2|          10|          12|2022-05-16 00:00:00|2022-05-17 00:00:00|
        |      1|          13|          13|2022-05-16 00:00:00|2022-05-17 00:00:00|
        +-------+------------+------------+-------------------+-------------------+
    """
    output_columns = set()
    # If create_tiles is None, default to creating tiles whenever the fv is not using continuous mode
    aggregation_tile_interval = time_aggregation.aggregation_slide_period.seconds
    create_tiles = aggregation_tile_interval > 0
    if create_tiles:
        group_by_cols = [F.col(col) for col in group_by_columns]
        slide_str = f"{aggregation_tile_interval} seconds"

        anchor_time_offset_string = None
        if aggregation_anchor_time:
            # Compute the offset from the epoch such that anchor_time aligns to an interval boundary of size
            # aggregation_slide_period. i.e. `epoch + offset + (X * slide_period) = anchor_time`, where X is
            # an integer.
            anchor_time_epoch = get_timestamp_in_seconds(aggregation_anchor_time)
            slide_period_seconds = aggregation_tile_interval
            anchor_time_offset_seconds = anchor_time_epoch % slide_period_seconds
            anchor_time_offset_string = f"{anchor_time_offset_seconds} seconds"

        window_spec = F.window(time_aggregation.time_key, slide_str, slide_str, anchor_time_offset_string)
        group_by_cols = [window_spec, *group_by_cols]
        aggregations = []
        intermediate_columns_added = set()
        for feature in time_aggregation.features:
            col_datatype = view_schema.to_dict()[feature.input_feature_name]
            aggregation_plan = get_aggregation_plan(
                feature.function,
                feature.function_params,
                time_aggregation.is_continuous,
                time_aggregation.time_key,
                col_datatype,
            )

            if aggregation_plan.partial_aggregation_preprocessor is not None:
                intermediate_columns = aggregation_plan.partial_aggregation_preprocessor(feature.input_feature_name)
                intermediate_column_names = aggregation_plan.intermediate_column_names(feature.input_feature_name)
                for column, column_name in zip(intermediate_columns, intermediate_column_names):
                    if column_name not in intermediate_columns_added:
                        intermediate_columns_added.add(column_name)
                        df = df.withColumn(column_name, column)

            for name, aggregation in _get_feature_partial_aggregations(aggregation_plan, feature.input_feature_name):
                if name in output_columns:
                    continue
                output_columns.add(name)
                aggregations.append(aggregation)
        output_df = df.groupBy(*group_by_cols).agg(*aggregations)
    else:
        columns_to_drop = set()
        intermediate_columns_added = set()
        for feature in time_aggregation.features:
            col_datatype = view_schema.to_dict()[feature.input_feature_name]

            aggregation_plan = get_aggregation_plan(
                feature.function,
                feature.function_params,
                time_aggregation.is_continuous,
                time_aggregation.time_key,
                col_datatype,
            )

            if aggregation_plan.partial_aggregation_preprocessor is not None:
                intermediate_columns = aggregation_plan.partial_aggregation_preprocessor(feature.input_feature_name)
                intermediate_column_names = aggregation_plan.intermediate_column_names(feature.input_feature_name)
                for column, column_name in zip(intermediate_columns, intermediate_column_names):
                    if column_name not in intermediate_columns_added:
                        intermediate_columns_added.add(column_name)
                        df = df.withColumn(column_name, column)

            input_columns = (
                aggregation_plan.intermediate_column_names(feature.input_feature_name)
                if aggregation_plan.intermediate_column_prefixes is not None
                else [feature.input_feature_name]
            )
            continuous_columns = aggregation_plan.continuous_partial_aggregation_transform(input_columns)

            continuous_column_prefixes = get_materialization_aggregation_column_prefixes(
                feature.function, function_params=feature.function_params, is_continuous=time_aggregation.is_continuous
            )
            continuous_column_names = [
                f"{column_prefix}_{feature.input_feature_name}" for column_prefix in continuous_column_prefixes
            ]

            for column_name, column in zip(continuous_column_names, continuous_columns):
                if column_name in output_columns:
                    continue
                output_columns.add(column_name)
                df = df.withColumn(column_name, column)
            columns_to_drop.add(feature.input_feature_name)
            columns_to_drop.update(input_columns)
        # Drop the original feature columns.
        for column in columns_to_drop:
            df = df.drop(column)
        output_df = df

    output_df = _convert_window_to_anchor_time(
        output_df,
        not create_tiles,
        time_aggregation.time_key,
        version,
        window_start_column_name,
        window_end_column_name,
        convert_to_epoch,
    )
    # TOOD: TEC-12299 drop the `timestamp` column in m13n schema for continuous WAFV
    return output_df


def partial_aggregate_column_renames(
    slide_interval_string: str, trailing_time_window_aggregation: TrailingTimeWindowAggregation
) -> Dict[str, str]:
    """Rename partial aggregate columns to human readable format."""
    # Create a map from intermediate rollup column name to preferred column names.
    renaming_map = {}
    for feature in trailing_time_window_aggregation.features:
        aggregation_plan = get_aggregation_plan(
            feature.function,
            feature.function_params,
            trailing_time_window_aggregation.is_continuous,
            trailing_time_window_aggregation.time_key,
        )

        for materialized_column_prefix, materialized_column_name in zip(
            aggregation_plan.materialized_column_prefixes,
            aggregation_plan.materialized_column_names(feature.input_feature_name),
        ):
            new_prefix = get_pretty_column_prefix(materialized_column_prefix)
            renaming_map[materialized_column_name] = (
                f"{feature.input_feature_name}_{new_prefix}_{slide_interval_string}"
            )
    return renaming_map


def construct_online_partial_agg_v2_df(
    df: pyspark.sql.DataFrame,
    group_by_columns: List[str],
    aggregation_groups: Tuple[compaction_utils.AggregationGroup, ...],
    time_key: str,
    view_schema: Schema,
    is_continuous: bool = False,
) -> pyspark.sql.DataFrame:
    """Constructs a dataframe that performs partial aggregations for online materialization on the input dataframe.

    This is built to follow the pattern used for the batch-compacted online store format. It does the aggregations
    specified by the `aggregation_groups`, grouped by the `group_by_columns`. Rows in the input dataframe are already mapped
    to the appropriate aggregation_group via the `AGGREGATION_GROUP_ID` column.
    """

    group_by_cols = [F.col(col) for col in group_by_columns]

    aggregations = []

    intermediate_columns_added = set()

    for agg_group in aggregation_groups:
        sub_aggs = []
        sub_outputs = set()

        for feature in agg_group.aggregate_features:
            col_datatype = view_schema.to_dict()[feature.input_feature_name]
            aggregation_plan = get_aggregation_plan(
                feature.function, feature.function_params, is_continuous, time_key, col_datatype
            )

            # partial_aggregation_preprocessor is used by approximate count distinct
            if aggregation_plan.partial_aggregation_preprocessor is not None:
                intermediate_columns = aggregation_plan.partial_aggregation_preprocessor(feature.input_feature_name)
                intermediate_column_names = aggregation_plan.intermediate_column_names(feature.input_feature_name)
                for column, column_name in zip(intermediate_columns, intermediate_column_names):
                    if column_name not in intermediate_columns_added:
                        intermediate_columns_added.add(column_name)
                        df = df.withColumn(column_name, column)

            for name, aggregation in _get_feature_partial_aggregations(aggregation_plan, feature.input_feature_name):
                # Skip duplicated partial aggregates. This can happen if you have mean + count over the same column, since they both use a count partial aggregate.
                if name in sub_outputs:
                    continue
                sub_outputs.add(name)
                sub_aggs.append(aggregation)

        expected_columns = agg_group.schema.column_names()
        if len(sub_outputs) != len(expected_columns):
            msg = "unexpected difference between expected columns and output columns"
            raise ValueError(msg)
        if set(sub_outputs) != set(expected_columns):
            msg = "unexpected difference between expected columns and output columns"
            raise ValueError(msg)

        aggregations.append(
            F.when(
                (F.col(aggregation_group_id()) == agg_group.window_index)
                & (F.col(aggregation_tile_id()) == agg_group.tile_index),
                F.struct(*sub_aggs),
            )
            .otherwise(F.lit(None))
            .alias(agg_group.window_tile_column_name)
        )

    # Compute aggregations for each aggregation window and tile.
    output_df = df.groupBy(*group_by_cols).agg(*aggregations)
    return output_df


def construct_partial_agg_lists_for_online_df(
    df: pyspark.sql.DataFrame,
    group_by_columns: List[str],
    aggregation_groups: Tuple[compaction_utils.AggregationGroup, ...],
) -> pyspark.sql.DataFrame:
    """Takes input data containing partial aggregations and collects all partial aggregations for a given aggregation window into one list.

    This is built to follow the pattern used for the batch-compacted online store format and used for the online compaction query.
    """
    group_by_cols = [F.col(col) for col in group_by_columns]

    input_tile_columns = []
    first_agg_columns = []

    agg_window_indexes_to_agg_groups = defaultdict(list)

    for agg_group in aggregation_groups:
        agg_window_indexes_to_agg_groups[agg_group.window_index].append(agg_group)

        aggregation_column_for_tile = F.col(agg_group.window_tile_column_name)
        input_tile_columns.append(aggregation_column_for_tile)
        # Every row corresponds to only 1 agg id + tile id combination, and sets nulls for the other tile columns. Use ignorenulls=True so we only select the first (and only) non-null value for that tile.
        first_agg_columns.append(
            F.first(aggregation_column_for_tile, ignorenulls=True).alias(agg_group.window_tile_column_name)
        )

    # For each join key and aggregation window, there is only 1 non-null value in each aggregation tile column across all the rows. This is why we can use first() aggregation to get the tile agg values.
    output_df = df.select(*group_by_cols, *input_tile_columns).groupBy(*group_by_cols).agg(*first_agg_columns)

    # Collapse all tile columns into one array with the tiles sorted in ascending order. The ordering is important.
    array_agg_columns = []
    for agg_window in agg_window_indexes_to_agg_groups.keys():
        sorted_tile_column_names = compaction_utils.get_sorted_tile_column_names(
            agg_window, agg_window_indexes_to_agg_groups[agg_window]
        )
        array_agg_columns.append(
            F.array(*[F.col(col_name) for col_name in sorted_tile_column_names]).alias(str(agg_window))
        )

    return output_df.select(*group_by_cols, *array_agg_columns)
