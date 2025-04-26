import datetime
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs

import tecton_core.tecton_pendulum as pendulum
from tecton_core import feature_definition_wrapper
from tecton_core import query_consts
from tecton_core import schema
from tecton_core import time_utils
from tecton_core.specs import LifetimeWindowSpec
from tecton_core.specs import OnlineBatchTablePart as SpecOnlineBatchTablePart
from tecton_core.specs import OnlineBatchTablePartTile as SpecOnlineBatchTablePartTile
from tecton_core.specs import TimeWindowSpec
from tecton_core.specs import create_time_window_spec_from_data_proto
from tecton_proto.data import feature_view__client_pb2 as feature_view__data_pb2


@attrs.frozen
class AggregationGroup:
    """AggregationGroup represents a group of aggregate features to compute with a corresponding start/end.

    The typical usage of this will be in compaction jobs, where we will use the start/end time to determine
    eligible rows for each individual aggregate. The tile index and start/end time correspond to an OnlineBatchTablePartTile for this aggregation window group. Each tile may represent a smaller time window, within the larger aggregation window, to compute futures for.
    """

    window_index: int
    inclusive_start_time: Optional[datetime.datetime]
    exclusive_end_time: datetime.datetime
    aggregate_features: Tuple[feature_view__data_pb2.Aggregate, ...]
    schema: schema.Schema
    tile_index: int
    window_tile_column_name: str  # 0_0 for example


def _get_inclusive_start_time_for_window(
    exclusive_end_time: datetime.datetime,
    aggregation_window: TimeWindowSpec,
    tile_window: Optional[SpecOnlineBatchTablePartTile] = None,
) -> Optional[datetime.datetime]:
    if isinstance(aggregation_window, LifetimeWindowSpec):
        return None
    window_start_time = (
        tile_window.relative_start_time_inclusive if tile_window is not None else aggregation_window.window_start
    )
    return time_utils.get_timezone_aware_datetime(exclusive_end_time + window_start_time)


def _get_exclusive_end_time_for_window(
    exclusive_end_time: datetime.datetime,
    aggregation_window: TimeWindowSpec,
    tile_window: Optional[SpecOnlineBatchTablePartTile] = None,
) -> datetime.datetime:
    if isinstance(aggregation_window, LifetimeWindowSpec):
        return time_utils.get_timezone_aware_datetime(exclusive_end_time)
    window_end_time = (
        tile_window.relative_end_time_exclusive if tile_window is not None else aggregation_window.window_end
    )
    return time_utils.get_timezone_aware_datetime(exclusive_end_time + window_end_time)


def _get_groups_for_aggregation_part(
    agg_part: SpecOnlineBatchTablePart, exclusive_end_time: datetime.datetime, aggregation_map: Dict
) -> List[AggregationGroup]:
    """Create one aggregation group for each tile in each aggregation part.

    Stream FVs with non-lifetime windows use sawtooths and have multiple tiles per part.
    Batch feature views with non-lifetime windows have one tile set per part.
    Lifetime windows do not have tiles set in their OnlineBatchTablePart, but we still add 1 agg group per part.
    """
    tiles = agg_part.tiles or [None]
    agg_group_tiles = []
    for i, tile in enumerate(tiles):
        agg_group_tiles.append(
            AggregationGroup(
                window_index=agg_part.window_index,
                inclusive_start_time=_get_inclusive_start_time_for_window(
                    exclusive_end_time, agg_part.time_window, tile
                ),
                exclusive_end_time=_get_exclusive_end_time_for_window(exclusive_end_time, agg_part.time_window, tile),
                aggregate_features=tuple(aggregation_map[agg_part.time_window]),
                schema=agg_part.schema,
                tile_index=i,
                window_tile_column_name=f"{agg_part.window_index}_{i}",
            )
        )
    return agg_group_tiles


def aggregation_groups(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    exclusive_end_time: datetime.datetime,
) -> Tuple[AggregationGroup, ...]:
    aggregation_map = defaultdict(list)
    for aggregation in fdw.trailing_time_window_aggregation().features:
        aggregation_map[create_time_window_spec_from_data_proto(aggregation.time_window)].append(aggregation)

    aggregation_parts = fdw.fv_spec.online_batch_table_format.online_batch_table_parts

    if len(aggregation_parts) != len(aggregation_map):
        msg = "unexpected difference in length of the spec's online_batch_table_format and trailing_time_window_aggregation"
        raise ValueError(msg)

    agg_groups = []
    for agg_part in aggregation_parts:
        agg_groups += _get_groups_for_aggregation_part(agg_part, exclusive_end_time, aggregation_map)

    return tuple(agg_groups)


def _get_min_window_start_time(
    aggregation_groups: Tuple[AggregationGroup, ...], fdw: feature_definition_wrapper.FeatureDefinitionWrapper
) -> Optional[pendulum.DateTime]:
    contains_lifetime_agg = any(group.inclusive_start_time is None for group in aggregation_groups)
    if contains_lifetime_agg:
        return fdw.materialization_start_timestamp
    min_window_time = min(group.inclusive_start_time for group in aggregation_groups)
    return pendulum.instance(min_window_time)


def _get_max_window_end_time(aggregation_groups: Tuple[AggregationGroup, ...]) -> pendulum.DateTime:
    max_window_time = max(group.exclusive_end_time for group in aggregation_groups)
    return pendulum.instance(max_window_time)


def get_data_time_limits_for_compaction(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, compaction_job_end_time: datetime.datetime
) -> Optional[pendulum.Period]:
    """Compute the time filter to be used for online compaction jobs.

    This determines how much data to read from the offline store.
    For aggregate fvs,
        start_time=earliest agg window start
        end_time=latest agg window end
    For non agg fvs,
        start_time=max(feature start time, compaction_job_end_time - ttl)
        end_time=compaction_job_end_time"""
    if fdw.materialization_start_timestamp is None:
        return None

    if fdw.is_temporal_aggregate:
        agg_groups = aggregation_groups(fdw=fdw, exclusive_end_time=compaction_job_end_time)
        start_time = _get_min_window_start_time(agg_groups, fdw)
        end_time = _get_max_window_end_time(agg_groups)
        return pendulum.Period(start_time, end_time)

    if not fdw.is_temporal:
        msg = "Expected fv to be of type temporal or temporal aggregate."
        raise Exception(msg)

    # respect ttl and feature start time for temporal fvs
    end_time = pendulum.instance(compaction_job_end_time)
    if fdw.serving_ttl:
        if not fdw.feature_start_timestamp:
            msg = "Expected feature start time to be set for temporal fvs when ttl is set."
            raise Exception(msg)
        job_time_minus_ttl = end_time - fdw.serving_ttl
        start_time = max(fdw.feature_start_timestamp, job_time_minus_ttl)
    elif fdw.feature_start_timestamp:
        start_time = fdw.feature_start_timestamp
    else:
        msg = "Expected ttl or feature start time to be set for temporal fvs."
        raise Exception(msg)
    return pendulum.Period(start_time, end_time)


def get_sorted_tile_column_names(agg_window_index: int, agg_groups: List[AggregationGroup]) -> List[str]:
    """Calculate the list of window_tile_column_names in ascending order for a given aggregation window index."""
    assert all(
        agg_window_index == agg_group.window_index for agg_group in agg_groups
    ), "All aggregation groups must have the same window index."
    expected_tile_indexes = set(range(len(agg_groups)))
    assert {
        agg_group.tile_index for agg_group in agg_groups
    } == expected_tile_indexes, "All aggregation groups must have unique tile indexes."

    sorted_tiles = sorted(
        agg_groups,
        key=lambda agg_group: agg_group.tile_index,
    )
    return [tile.window_tile_column_name for tile in sorted_tiles]


def _get_anchor_time_column_for_sawtooth_size(sawtooth_size: Optional[pendulum.Duration]) -> str:
    if sawtooth_size == pendulum.Duration(days=1):
        return query_consts.anchor_time_for_day_sawtooth()
    elif sawtooth_size == pendulum.Duration(hours=1):
        return query_consts.anchor_time_for_hour_sawtooth()
    elif sawtooth_size is None or sawtooth_size < pendulum.Duration(hours=1):
        return query_consts.anchor_time_for_non_sawtooth()

    msg = f"Invalid sawtooth size: {sawtooth_size}"
    raise ValueError(msg)


def _get_boolean_partition_column_for_sawtooth_size(
    sawtooth_size: Optional[pendulum.Duration],
) -> str:
    if sawtooth_size == pendulum.Duration(days=1):
        return query_consts.is_day_sawtooth()
    elif sawtooth_size == pendulum.Duration(hours=1):
        return query_consts.is_hour_sawtooth()
    elif sawtooth_size is None or sawtooth_size < pendulum.Duration(hours=1):
        return query_consts.is_non_sawtooth()

    msg = f"Invalid sawtooth size: {sawtooth_size}"
    raise ValueError(msg)


def _get_time_partition_column_for_sawtooth_size(sawtooth_size: Optional[pendulum.Duration]) -> Optional[str]:
    if sawtooth_size is None:
        return None
    elif sawtooth_size == pendulum.Duration(days=1):
        return query_consts.time_partition_column_for_date()
    elif sawtooth_size == pendulum.Duration(hours=1):
        return query_consts.time_partition_column_for_hour()
    elif sawtooth_size < pendulum.Duration(hours=1):
        # Either 5 minutes or one minute.
        return query_consts.time_partition_column_for_minute()

    msg = f"Invalid sawtooth size: {sawtooth_size}"
    raise ValueError(msg)


@attrs.frozen
class SawtoothAggregateFeatureBase:
    """Base class for SawtoothAggregateFeature and SecondaryKeySawtoothAggregateFeature.

    anchor_time_column: The anchor time column to use for aggregating.
    identifier_partition_column: A column to partition the data by when aggregating. This column represents which sawtooth size to use for the aggregation time window.
    use_continuous_range_query: Whether to use a continuous range query for the aggregation instead of the sawtooth aggregation plan. Only true for <2 day continuous time windows.
    time_partition_column: A column to partition the data by when aggregating. This column represents the date/hour/5min/1min interval the anchor time column falls into.
    """

    anchor_time_column: str
    identifier_partition_column: str
    use_continuous_range_query: bool
    time_partition_column: Optional[str]


@attrs.frozen
class SawtoothAggregateFeature(SawtoothAggregateFeatureBase):
    """SawtoothAggregateFeature represents a single aggregate feature and its metadata.

    The typical usage of this will be in offline retrieval for Feature Views that use sawtooth aggregations (i.e. Stream Fvs with compaction enabled and non lifetime windows).
    """

    aggregate_feature: feature_view__data_pb2.Aggregate
    batch_sawtooth_tile_size: Optional[pendulum.Duration]


@attrs.frozen
class SecondaryKeySawtoothAggregateFeature(SawtoothAggregateFeatureBase):
    """SecondaryKeySawtoothAggregateFeature represents a single SecondaryKeyOutputColumn and its metadata.

    The typical usage of this will be in offline retrieval for Feature Views that use sawtooth aggregations and secondary key aggregations.(i.e. Stream Fvs with compaction enabled and non lifetime windows).
    """

    name: str


@attrs.frozen
class SawtoothAggregationData:
    """SawtoothAggregationData represents a collection of sawtooth aggregate features and their metadata.

    The typical usage of this will be in offline retrieval for Feature Views that use sawtooth aggregations (i.e. Stream Fvs with compaction enabled and non lifetime windows).
    """

    aggregations: Dict[str, SawtoothAggregateFeature]
    unique_batch_sawtooth_tile_sizes: List[pendulum.Duration]
    _secondary_key_aggregations: Dict[str, SecondaryKeySawtoothAggregateFeature]
    stream_tile_size: Optional[pendulum.Duration] = None

    @classmethod
    def from_aggregate_features(
        cls, fdw: feature_definition_wrapper.FeatureDefinitionWrapper
    ) -> "SawtoothAggregationData":
        sawtooth_aggregations = {}
        for agg in fdw.trailing_time_window_aggregation().features:
            batch_sawtooth_tile_size = (
                time_utils.proto_to_duration(agg.batch_sawtooth_tile_size)
                if agg.HasField("batch_sawtooth_tile_size")
                else None
            )
            batch_sawtooth_tile_size_for_retrieval = batch_sawtooth_tile_size
            if batch_sawtooth_tile_size is None:
                if agg.time_window.HasField("lifetime_window"):
                    # Lifetime windows do not use sawtooths online, but should mimic day sawtoothing behavior offline.
                    batch_sawtooth_tile_size_for_retrieval = pendulum.Duration(days=1)
                elif fdw.stream_tiling_enabled:
                    # For time windows < 2d, we use the stream tile size as the sawtooth size.
                    batch_sawtooth_tile_size_for_retrieval = fdw.stream_tile_size

            # If we support custom sawtooth sizes, we should move away from using hardcoded column names here.
            anchor_time_column = _get_anchor_time_column_for_sawtooth_size(batch_sawtooth_tile_size_for_retrieval)
            boolean_partition_column = _get_boolean_partition_column_for_sawtooth_size(
                batch_sawtooth_tile_size_for_retrieval
            )
            time_partition_column = _get_time_partition_column_for_sawtooth_size(batch_sawtooth_tile_size_for_retrieval)
            sawtooth_agg = SawtoothAggregateFeature(
                aggregate_feature=agg,
                batch_sawtooth_tile_size=batch_sawtooth_tile_size_for_retrieval,
                anchor_time_column=anchor_time_column,
                identifier_partition_column=boolean_partition_column,
                time_partition_column=time_partition_column,
                use_continuous_range_query=batch_sawtooth_tile_size_for_retrieval is None,
            )
            sawtooth_aggregations[agg.output_feature_name] = sawtooth_agg

        secondary_key_aggregations = {}
        if fdw.aggregation_secondary_key:
            for secondary_key_output in fdw.materialized_fv_spec.secondary_key_rollup_outputs:
                matching_agg_list = [
                    sawtooth_agg
                    for sawtooth_agg in sawtooth_aggregations.values()
                    if create_time_window_spec_from_data_proto(sawtooth_agg.aggregate_feature.time_window)
                    == secondary_key_output.time_window
                ]
                if len(matching_agg_list) == 0:
                    msg = f"Could not find an aggregation matching the time window for secondary key output {secondary_key_output.name}"
                    raise ValueError(msg)
                matching_agg = matching_agg_list[0]
                secondary_sawtooth_agg = SecondaryKeySawtoothAggregateFeature(
                    name=secondary_key_output.name,
                    anchor_time_column=matching_agg.anchor_time_column,
                    identifier_partition_column=matching_agg.identifier_partition_column,
                    time_partition_column=matching_agg.time_partition_column,
                    use_continuous_range_query=matching_agg.use_continuous_range_query,
                )
                secondary_key_aggregations[secondary_key_output.name] = secondary_sawtooth_agg

        return cls(
            aggregations=sawtooth_aggregations,
            unique_batch_sawtooth_tile_sizes=list(
                {agg.batch_sawtooth_tile_size for agg in sawtooth_aggregations.values()}
            ),
            stream_tile_size=fdw.stream_tile_size,
            secondary_key_aggregations=secondary_key_aggregations,
        )

    def get_sawtooth_aggregation_for_output_feature_name(self, output_feature_name: str) -> SawtoothAggregateFeature:
        if output_feature_name not in self.aggregations:
            msg = f"Feature output name {output_feature_name} not found in sawtooth aggregations."
            raise ValueError(msg)
        return self.aggregations[output_feature_name]

    def get_sawtooth_aggregate_feature_or_secondary_key_feature(
        self, name: str
    ) -> Union[SawtoothAggregateFeature, SecondaryKeySawtoothAggregateFeature]:
        if name in self.aggregations:
            return self.aggregations[name]
        elif name in self._secondary_key_aggregations:
            return self._secondary_key_aggregations[name]
        else:
            msg = f"Feature name {name} not found in sawtooth aggregations or secondary key sawtooth aggregations."
            raise ValueError(msg)

    def contains_day_sawtooths(self) -> bool:
        return any(tile_size == pendulum.Duration(days=1) for tile_size in self.unique_batch_sawtooth_tile_sizes)

    def contains_hour_sawtooths(self) -> bool:
        return any(tile_size == pendulum.Duration(hours=1) for tile_size in self.unique_batch_sawtooth_tile_sizes)

    def contains_non_sawtooth_aggregations(self) -> bool:
        # Aggregations < 2 days. Exception is  <2 day aggregations that have a 1hr stream tile size.
        return any(
            tile_size is None or tile_size < pendulum.Duration(hours=1)
            for tile_size in self.unique_batch_sawtooth_tile_sizes
        )

    def contains_continuous_non_sawtooth_aggregations(self) -> bool:
        return self.stream_tile_size is None and self.contains_non_sawtooth_aggregations()

    def contains_tiled_non_sawtooth_aggregations(self) -> bool:
        return self.stream_tile_size is not None and self.contains_non_sawtooth_aggregations()

    def get_anchor_time_columns(self, include_non_sawtooths: bool = True) -> List[str]:
        column_set = {
            agg.anchor_time_column
            for agg in self.aggregations.values()
            if include_non_sawtooths or agg.anchor_time_column != query_consts.anchor_time_for_non_sawtooth()
        }
        return list(column_set)

    def get_identifier_partition_columns(self) -> List[str]:
        column_set = {agg.identifier_partition_column for agg in self.aggregations.values()}
        return list(column_set)

    def get_truncated_timestamp_partition_columns(self) -> List[str]:
        column_set = {
            agg.time_partition_column for agg in self.aggregations.values() if agg.time_partition_column is not None
        }
        return list(column_set)

    def get_partition_column_to_bool_map(
        self, sawtooth_bool_value: bool = True, non_sawtooth_bool_value: bool = True
    ) -> Dict[str, bool]:
        # Map the new partition column names to the boolean constant the column should contain.
        partition_column_to_bool_map = {}
        if self.contains_day_sawtooths():
            partition_column_to_bool_map[query_consts.is_day_sawtooth()] = sawtooth_bool_value
        if self.contains_hour_sawtooths():
            partition_column_to_bool_map[query_consts.is_hour_sawtooth()] = sawtooth_bool_value
        if self.contains_non_sawtooth_aggregations():
            partition_column_to_bool_map[query_consts.is_non_sawtooth()] = non_sawtooth_bool_value
        return partition_column_to_bool_map

    def get_anchor_time_to_partition_columns_map(self, include_non_sawtooths: bool = True) -> Dict[str, str]:
        # Map the anchor time column used for aggregations to the column to partition by.
        anchor_time_to_identifier_map = {}
        if self.contains_day_sawtooths():
            anchor_time_to_identifier_map[query_consts.anchor_time_for_day_sawtooth()] = query_consts.is_day_sawtooth()
        if self.contains_hour_sawtooths():
            anchor_time_to_identifier_map[query_consts.anchor_time_for_hour_sawtooth()] = (
                query_consts.is_hour_sawtooth()
            )
        if include_non_sawtooths and self.contains_non_sawtooth_aggregations():
            anchor_time_to_identifier_map[query_consts.anchor_time_for_non_sawtooth()] = query_consts.is_non_sawtooth()
        return anchor_time_to_identifier_map

    def get_anchor_time_to_timedelta_map(self, use_zero_timedelta: bool = False) -> Dict[str, datetime.timedelta]:
        # Map the new anchor time column names to the duration of time the timestamp is rounded to.
        anchor_time_to_timedelta_map = {}
        if self.contains_day_sawtooths():
            day_duration = datetime.timedelta(seconds=0) if use_zero_timedelta else datetime.timedelta(days=1)
            anchor_time_to_timedelta_map[query_consts.anchor_time_for_day_sawtooth()] = day_duration
        if self.contains_hour_sawtooths():
            hour_duration = datetime.timedelta(seconds=0) if use_zero_timedelta else datetime.timedelta(hours=1)
            anchor_time_to_timedelta_map[query_consts.anchor_time_for_hour_sawtooth()] = hour_duration
        if self.contains_non_sawtooth_aggregations():
            if self.stream_tile_size:
                stream_tile_size_duration = (
                    datetime.timedelta(seconds=0) if use_zero_timedelta else self.stream_tile_size
                )
                anchor_time_to_timedelta_map[query_consts.anchor_time_for_non_sawtooth()] = stream_tile_size_duration
            else:
                anchor_time_to_timedelta_map[query_consts.anchor_time_for_non_sawtooth()] = datetime.timedelta(
                    seconds=0
                )
        return anchor_time_to_timedelta_map

    def get_anchor_time_to_aggregation_interval_map(
        self, aggregation_tile_interval: int, feature_store_format_version: int
    ) -> Dict[str, int]:
        # Map the new anchor time column names to aggregation tile interval the relevant partial tiles use.
        anchor_time_to_tile_interval_map = {}
        if self.contains_day_sawtooths():
            anchor_time_to_tile_interval_map[query_consts.anchor_time_for_day_sawtooth()] = aggregation_tile_interval
        if self.contains_hour_sawtooths():
            anchor_time_to_tile_interval_map[query_consts.anchor_time_for_hour_sawtooth()] = aggregation_tile_interval
        if self.contains_non_sawtooth_aggregations():
            if self.stream_tile_size:
                tile_interval = time_utils.convert_timedelta_for_version(
                    self.stream_tile_size, feature_store_format_version
                )
            else:
                tile_interval = 0
            anchor_time_to_tile_interval_map[query_consts.anchor_time_for_non_sawtooth()] = tile_interval
        return anchor_time_to_tile_interval_map
