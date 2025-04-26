import logging
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy
import pandas
import sqlparse

import tecton_core.tecton_pendulum as pendulum
import tecton_spark.offline_store  # noqa: TID251
from tecton_athena import odfv_helper
from tecton_athena.athena_session import get_session
from tecton_athena.data_catalog_helper import PARTITION_TYPE_DATESTR
from tecton_athena.data_catalog_helper import PARTITION_TYPE_UNIX_EPOCH_NS
from tecton_athena.data_catalog_helper import generate_sql_table_from_pandas_df
from tecton_athena.data_catalog_helper import register_feature_view_as_athena_table_if_necessary
from tecton_athena.templates_utils import load_template
from tecton_core import query_consts
from tecton_core import time_utils
from tecton_core.errors import START_TIME_NOT_BEFORE_END_TIME
from tecton_core.errors import TectonAthenaNotImplementedError
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.offline_store import window_size_seconds
from tecton_proto.common import aggregation_function__client_pb2 as afpb
from tecton_proto.data import feature_view__client_pb2 as feature_view_pb2


logger = logging.getLogger(__name__)

SECONDS_TO_NANOSECONDS = 1000 * 1000 * 1000

HISTORICAL_FEATURES_TEMPLATE = load_template("historical_features.sql")
TIME_LIMIT_TEMPLATE = load_template("time_limit.sql")
MATERIALIZATION_TILE_TEMPLATE = load_template("materialization_tile.sql")
PARTIAL_AGGREGATION_TEMPLATE = load_template("run_partial_aggregation.sql")
FULL_AGGREGATION_TEMPLATE = load_template("run_full_aggregation.sql")

# TODO: Add non-trivial aggregation types: Variance, Standard deviations and Last-N aggregations.
AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: {("SUM", "SUM")},
    afpb.AGGREGATION_FUNCTION_MIN: {("MIN", "MIN")},
    afpb.AGGREGATION_FUNCTION_MAX: {("MAX", "MAX")},
    afpb.AGGREGATION_FUNCTION_COUNT: {("COUNT", "COUNT")},
    afpb.AGGREGATION_FUNCTION_MEAN: {("COUNT", "COUNT"), ("MEAN", "AVG")},
}


@dataclass
class _FeatureSetItemInput:
    """A simplified version of FeatureSetItem which is passed to the SQL template."""

    name: str
    timestamp_key: str
    join_keys: Dict[str, str]
    features: List[str]
    sql: str
    aggregation: Optional[feature_view_pb2.TrailingTimeWindowAggregation]
    ttl_seconds: Optional[int]


def _format_sql(sql_str: str) -> str:
    return sqlparse.format(sql_str, reindent=True)


def _get_feature_selection_time_bounds_from_spine_time_range(
    feature_definition: FeatureDefinitionWrapper,
    spine_min_ts: pendulum.DateTime = None,
    spine_max_ts: pendulum.DateTime = None,
):
    feature_end_time = spine_max_ts
    feature_start_time = spine_min_ts

    if feature_definition.is_temporal:
        # We have to select at least as far back as the serving_ttl before the minimum spine time
        feature_start_time = spine_min_ts - feature_definition.serving_ttl
    elif feature_definition.is_temporal_aggregate:
        # For aggregates, we need to subtract the max aggregation time window AND an additional tile interval
        # We need to add an additional tile interval, because the spine's minimum timestamp may be inbetween two tile anchors
        feature_start_time = (
            spine_min_ts
            + time_utils.timedelta_to_duration(feature_definition.earliest_window_start)
            - feature_definition.get_tile_interval
        )

    return feature_start_time, feature_end_time


def _get_feature_selection_time_bounds(
    feature_definition: FeatureDefinitionWrapper,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    if start_time is None or (
        feature_definition.feature_start_timestamp is not None
        and start_time < feature_definition.feature_start_timestamp
    ):
        logger.warning(
            "Defaulting start_time to FeatureView's feature_start_time because start_time was either not set or smaller than FeatureView start_time"
        )
        feature_start_time = feature_definition.feature_start_timestamp
        return feature_start_time, end_time
    else:
        feature_start_time = start_time
        return feature_start_time, end_time


def get_historical_features_sql(
    spine: Optional[Union[pandas.DataFrame]],
    feature_set_config: FeatureSetConfig,
    timestamp_key: Optional[str],
    include_feature_view_timestamp_columns: bool = False,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> Tuple[str, Optional[str]]:
    feature_set_items = feature_set_config.definitions_and_configs
    input_items = []
    if spine is None:
        # Only feature view is supported when the spine is not provided.
        # Feature service should always provide the spine.
        # SDK methods should never fail this check
        assert len(feature_set_items) == 1

    # Get a list of all the join keys in the spine.
    spine_keys = {}
    for item in feature_set_items:
        fd = item.feature_definition

        if not fd.is_rtfv:
            join_keys = dict(item.join_keys)
            spine_keys.update(join_keys)

    spine_info = upload_spine(spine=spine, expected_spine_keys=list(spine_keys), expected_timestamp_key=timestamp_key)

    for item in feature_set_items:
        fd = item.feature_definition

        if fd.is_rtfv:
            continue

        offline_store_type = fd.offline_store_config.WhichOneof("store_type")

        if offline_store_type not in ("parquet", "delta"):
            msg = f"Offline store {offline_store_type} is not supported"
            raise TectonValidationError(msg)

        # Change the feature view name if it's for internal udf use.
        if item.namespace.startswith("_udf_internal"):
            name = item.namespace.upper()
        else:
            name = fd.name

        join_keys = dict(item.join_keys)
        features = [
            col_name
            for col_name in fd.view_schema.column_names()
            if col_name not in ([*list(join_keys.keys()), fd.timestamp_key])
        ]
        if len(fd.online_serving_index.join_keys) != len(fd.join_keys):
            msg = "Wildcard is not supported for Athena"
            raise TectonAthenaNotImplementedError(msg)

        if spine_info is not None:
            feature_start_time, feature_end_time = _get_feature_selection_time_bounds_from_spine_time_range(
                feature_definition=fd, spine_min_ts=spine_info.min_ts, spine_max_ts=spine_info.max_ts
            )
        else:
            feature_start_time, feature_end_time = _get_feature_selection_time_bounds(
                feature_definition=fd, start_time=start_time, end_time=end_time
            )

        if feature_start_time is not None and feature_end_time is not None and feature_start_time >= feature_end_time:
            raise START_TIME_NOT_BEFORE_END_TIME(feature_start_time, feature_end_time)

        sql_str = fetch_features_and_join_spine_sql(
            feature_definition=fd,
            feature_start_time=feature_start_time,
            feature_end_time=feature_end_time,
            spine=spine_info.spine_sql if spine_info is not None else None,
            spine_timestamp_key=timestamp_key,
        )
        input_items.append(
            _FeatureSetItemInput(
                name=name,
                timestamp_key=fd.timestamp_key,
                join_keys=join_keys,
                features=features,
                sql=sql_str,
                aggregation=(fd.trailing_time_window_aggregation() if fd.is_temporal_aggregate else None),
                ttl_seconds=(int(fd.serving_ttl.total_seconds()) if (fd.is_temporal or fd.is_feature_table) else None),
            )
        )
    if spine_info is not None:
        sql_str = HISTORICAL_FEATURES_TEMPLATE.render(
            feature_set_items=input_items,
            spine_timestamp_key=timestamp_key,
            spine_sql=spine_info.spine_sql,
            include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
            spine_keys=list(spine_keys),
            spine_contains_non_join_keys=spine_info.contains_non_join_key_columns,
        )

    return (_format_sql(sql_str), spine_info and spine_info.table)


def _timestamp_to_partition(timestamp: pendulum.DateTime, partition_size: timedelta, partition_type: str):
    if timestamp is None:
        return None

    partition_size_seconds = window_size_seconds(partition_size)

    if partition_type == PARTITION_TYPE_DATESTR:
        unix_timestamp_seconds = int(timestamp.timestamp())
        dt = pendulum.from_timestamp(time_utils.align_epoch_downwards(unix_timestamp_seconds, partition_size_seconds))
        partition_format = tecton_spark.offline_store.timestamp_formats(partition_size).python_format
        return dt.strftime(partition_format)
    elif partition_type == PARTITION_TYPE_UNIX_EPOCH_NS:
        unix_timestamp_ns = int(timestamp.timestamp() * SECONDS_TO_NANOSECONDS)
        return time_utils.align_epoch_downwards(unix_timestamp_ns, partition_size_seconds * SECONDS_TO_NANOSECONDS)
    else:
        msg = "Unexpected partition_type"
        raise Exception(msg)


def _ensure_time_is_pendulum(time):
    if time is None:
        return None

    if isinstance(time, pendulum.DateTime):
        return time

    if isinstance(time, (int, float)):
        return pendulum.from_timestamp(time)

    if isinstance(time, datetime):
        return pendulum.instance(time)

    msg = f"Unexpected Time type {type(time)}"
    raise Exception(msg)


# Todo: Refactor. Fairly ugly function
def _feature_view_select_all_sql(feature_definition: FeatureDefinitionWrapper, start_time, end_time):
    athena_table = register_feature_view_as_athena_table_if_necessary(feature_definition, session=get_session())

    source = None
    timestamp_expression = None

    start_time = _ensure_time_is_pendulum(start_time)
    end_time = _ensure_time_is_pendulum(end_time)
    partition_lower_bound = _timestamp_to_partition(
        start_time, athena_table.partition_by_interval_timedelta, athena_table.partition_type
    )
    partition_upper_bound = _timestamp_to_partition(
        end_time, athena_table.partition_by_interval_timedelta, athena_table.partition_type
    )

    select_columns = []

    # Note: It's pretty bad that the timestamp field column is handled differently between aggregates and non-aggregates
    if feature_definition.is_temporal_aggregate:
        # Let's not select _anchor_time - leads to ambiguous queries
        if query_consts.anchor_time() in athena_table.columns:
            # Note - this condition isn't always true: If the anchor time is just a partition column but not a table column. That's the case for Parquet based TWAGs
            del athena_table.columns[query_consts.anchor_time()]

        select_columns = list(athena_table.columns.keys())
        timestamp_expression = f"from_unixtime({query_consts.anchor_time()} / ({SECONDS_TO_NANOSECONDS}))"
        select_columns.append(f"{timestamp_expression} as {feature_definition.timestamp_key}")
    else:
        timestamp_expression = feature_definition.timestamp_key
        select_columns = list(athena_table.columns.keys())

    if athena_table.partition_type == PARTITION_TYPE_DATESTR:
        if partition_lower_bound:
            partition_lower_bound = f"'{partition_lower_bound}'"
        if partition_upper_bound:
            partition_upper_bound = f"'{partition_upper_bound}'"

    return TIME_LIMIT_TEMPLATE.render(
        select_columns=select_columns,
        start_time=start_time,
        end_time=end_time,
        source=athena_table.table,
        timestamp_key=timestamp_expression,
        partition_column=athena_table.partition_by,
        partition_lower_bound=partition_lower_bound,
        partition_upper_bound=partition_upper_bound,
    )


def fetch_features_and_join_spine_sql(
    feature_definition: FeatureDefinitionWrapper,
    # start is inclusive and end is exclusive
    feature_start_time: Optional[datetime] = None,
    feature_end_time: Optional[datetime] = None,
    aggregation_level: str = "full",
    # If spine is provided, it will be used to join with the output results.
    # Currently only work with full aggregation.
    spine: Optional[str] = None,
    spine_timestamp_key: Optional[str] = None,
    spine_keys: Optional[List[str]] = None,
    mock_sql_inputs: Optional[Dict[str, str]] = None,
) -> str:
    if not feature_definition.writes_to_offline_store:
        msg = f"FeatureView {feature_definition.name} does not have offline materialization enabled. Cannot proceed. Please enable offline materialization."
        raise Exception(msg)

    materialized_sql = _feature_view_select_all_sql(
        feature_definition, start_time=feature_start_time, end_time=feature_end_time
    )

    if feature_definition.is_temporal_aggregate:
        if aggregation_level == "full":
            aggregated_sql_str = FULL_AGGREGATION_TEMPLATE.render(
                source=materialized_sql,
                join_keys=feature_definition.join_keys,
                aggregation=feature_definition.trailing_time_window_aggregation(),
                timestamp_key=feature_definition.timestamp_key,
                name=feature_definition.name,
                spine=spine,
                spine_timestamp_key=spine_timestamp_key,
                spine_keys=spine_keys,
                batch_schedule=int(feature_definition.batch_materialization_schedule.total_seconds()),
            )
            return _format_sql(aggregated_sql_str)
        else:
            msg = f"Unsupported aggregation level: {aggregation_level}"
            raise ValueError(msg)

    else:
        return _format_sql(materialized_sql)


@dataclass
class _SpineInfo:
    """Information about the spine"""

    table: str
    timestamp_key: str
    min_ts: pendulum.DateTime
    max_ts: pendulum.DateTime
    spine_keys: List[str]
    contains_non_join_key_columns: bool

    @property
    def spine_sql(self):
        return f"SELECT * FROM {self.table}"


def upload_spine(
    spine: Optional[Union[pandas.DataFrame]], expected_spine_keys: List[str], expected_timestamp_key: str
) -> Optional[_SpineInfo]:
    if spine is None:
        return None

    if isinstance(spine, pandas.DataFrame):
        spine_columns = {c.lower() for c in list(spine.columns)}
        expected_spine_columns = {c.lower() for c in expected_spine_keys}
        expected_spine_columns.add(expected_timestamp_key.lower())

        non_key_columns_in_spine = spine_columns - expected_spine_columns
        missing_columns_in_spine = expected_spine_columns - spine_columns

        if len(missing_columns_in_spine) > 0:
            msg = f"Expected to find the following columns in the spine: {missing_columns_in_spine}"
            raise Exception(msg)

        spine_timestamp_type = spine.dtypes[expected_timestamp_key].type
        if spine_timestamp_type != pandas.Timestamp and spine_timestamp_type != numpy.datetime64:
            msg = f"Spine timestamp column must be of type Timestamp. It's of type {spine_timestamp_type}"
            raise Exception(msg)

        spine_min_ts = pendulum.instance(spine[expected_timestamp_key].min())
        spine_max_ts = pendulum.instance(spine[expected_timestamp_key].max())

        spine_table_name = get_session().get_spine_temp_table_name()
        generate_sql_table_from_pandas_df(df=spine, session=get_session(), table_name=spine_table_name)
        return _SpineInfo(
            table=spine_table_name,
            timestamp_key=expected_timestamp_key,
            min_ts=spine_min_ts,
            max_ts=spine_max_ts,
            spine_keys=expected_spine_keys,
            contains_non_join_key_columns=len(non_key_columns_in_spine) > 0,
        )
    else:
        msg = "Only pandas based spines are currently supported"
        raise TectonAthenaNotImplementedError(msg)


def _drop_internal_columns_from_ghf_result(data_df: pandas.DataFrame) -> pandas.DataFrame:
    internal_columns = [c for c in data_df.columns if c.startswith("_udf_internal")]
    return data_df.drop(columns=internal_columns)


def get_historical_features(
    spine: Optional[Union[pandas.DataFrame]],
    feature_set_config: FeatureSetConfig,
    timestamp_key: str,
    include_feature_view_timestamp_columns: bool = False,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> pandas.DataFrame:
    sql_str, spine_table = get_historical_features_sql(
        spine=spine,
        feature_set_config=feature_set_config,
        timestamp_key=timestamp_key,
        include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
        start_time=start_time,
        end_time=end_time,
    )

    try:
        logger.info("Getting historical features. This may take a few minutes...")

        materialized_feature_data_df = get_session().read_sql(sql_str)
        odfvs = odfv_helper.get_odfvs_from_feature_set_config(feature_set_config)
        internal_feature_data_df = odfv_helper.run_and_append_on_demand_features_to_historical_data(
            materialized_feature_data_df, odfvs
        )
        # ODFVs dependent FVs may have pulled in internal columns that need to be dropped
        final_feature_data_df = _drop_internal_columns_from_ghf_result(internal_feature_data_df)

        return final_feature_data_df
    finally:
        if spine_table:
            get_session().sql(f"DROP TABLE IF EXISTS {spine_table}")
