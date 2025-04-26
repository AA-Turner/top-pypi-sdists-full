import logging
from datetime import timedelta

import pandas

import tecton_core.tecton_pendulum as pendulum
from tecton_athena.athena_session import PARTITION_TYPE_DATESTR
from tecton_athena.athena_session import PARTITION_TYPE_UNIX_EPOCH_NS
from tecton_athena.athena_session import AthenaSession
from tecton_athena.athena_session import AthenaTableCreationSpec
from tecton_core import conf
from tecton_core import query_consts
from tecton_core.data_types import ArrayType
from tecton_core.data_types import BoolType
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.data_types import TimestampType
from tecton_core.errors import TectonAthenaNotImplementedError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.offline_store import get_offline_store_partition_params
from tecton_core.offline_store import timestamp_to_partition_epoch
from tecton_proto.data.feature_store__client_pb2 import FeatureStoreFormatVersion


logger = logging.getLogger(__name__)

SECONDS_TO_NANOSECONDS = 1000 * 1000 * 1000

TECTON_DATA_TYPE_TO_HIVE_TYPES = {
    StringType(): "string",
    Float64Type(): "double",
    Int32Type(): "integer",
    Int64Type(): "bigint",
    TimestampType(): "timestamp",
    BoolType(): "boolean",
    ArrayType(Int64Type()): "array<bigint>",
    ArrayType(Int32Type()): "array<integer>",
    ArrayType(Float64Type()): "array<double>",
    ArrayType(StringType()): "array<string>",
    ArrayType(BoolType()): "array<boolean>",
}


# Todo: Refactor. Fairly ugly function
def register_feature_view_as_athena_table_if_necessary(
    feature_definition: FeatureDefinitionWrapper, session: AthenaSession
) -> AthenaTableCreationSpec:
    # Examples of how our offline store is partitioned - quite the madness:
    # BWAFV on Delta
    # Partition Column: time_partition
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]

    # Continuous SWAFV on Parquet
    # Partition Column: time_partition
    # Materialized Columns: timestamp, _anchor_time, [join_keys], [feature_columns]
    # Note: Very weird that we have a timestamp parquet column here - redundant with _anchor_time

    # BWAFV on Parquet
    # Partition Column: _anchor_time
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]
    # !! In this case we need to drop the partition column from the top level columns

    # BFV on Parquet
    # Partition Column: _anchor_time
    # Materialized Columns: ts, [join_keys], [feature_columns]

    s3_path = feature_definition.materialized_data_path
    # Tecton allows '-' in a workspace name, while Athena does not allow it in the
    # table/view names.
    # To also match a behavior with Snowflake, we replace '-' with '_'.
    # TODO(TEC-11222): deal with Athena table name collision across workspaces.
    workspace_prefix = feature_definition.workspace.replace("-", "_")
    table_name = workspace_prefix + "__" + feature_definition.name

    partition_type = None
    partition_by_interval_timedelta = None
    partition_by = None
    partition_by_type = None
    partition_by_format = None
    partition_by_range_from = None
    partition_by_range_to = None
    partition_by_interval = None

    offline_store_config = feature_definition.offline_store_config
    store_type = offline_store_config.WhichOneof("store_type")

    # We only support nanosecond based partitions now
    assert (
        feature_definition.get_feature_store_format_version
        >= FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS
    )

    # TODO: use partition_type from partition_params here
    partition_params = get_offline_store_partition_params(feature_definition)
    if store_type == "delta":
        partition_by = partition_params.partition_by

        partition_by_interval_timedelta = partition_params.partition_interval.as_timedelta()
        if partition_by_interval_timedelta % timedelta(days=1) != timedelta(0):
            # We only support daily partitions now
            msg = "Athena reader currently only supports daily delta partitions"
            raise TectonAthenaNotImplementedError(msg)

        # we do not set partition_by_interval, because this is used by
        # projection in AthenaCreateTableSpec. The default value is "1"
        # , because the default unit is in days because we use "date" type

        partition_type = PARTITION_TYPE_DATESTR
        partition_by_type = "date"
        partition_by_format = "yyyy-MM-dd"
        # TODO(TEC-16481): match the Parquet logic and use timestamp_to_partition_date_str. The current logic may break for fvs with large batch schedules.
        partition_by_range_from = (
            pendulum.instance(feature_definition.materialization_start_timestamp).start_of("day").format("YYYY-MM-DD")
        )
        # Let's register the table with partitions up until 1 year from now. Will break if the table is registered and used for more than 1 year
        partition_by_range_to = pendulum.now("utc").add(years=1).end_of("year").format("YYYY-MM-DD")

    elif store_type == "parquet":
        partition_by = partition_params.partition_by
        partition_by_type = "integer"
        partition_type = PARTITION_TYPE_UNIX_EPOCH_NS
        partition_by_interval_timedelta = partition_params.partition_interval.as_timedelta()

        partition_by_range_from = timestamp_to_partition_epoch(
            feature_definition.materialization_start_timestamp,
            partition_params,
            feature_definition.get_feature_store_format_version,
        )
        partition_by_range_to = timestamp_to_partition_epoch(
            pendulum.now("utc").add(years=1).end_of("year"),
            partition_params,
            feature_definition.get_feature_store_format_version,
        )
        # The partition size should really be configured explicitly in the proto offline store config
        partition_by_interval = int(partition_by_interval_timedelta.total_seconds() * SECONDS_TO_NANOSECONDS)
    else:
        msg = "Unexpected offline store config"
        raise Exception(msg)

    materialization_schema = feature_definition.materialization_schema
    hive_columns = {}
    for col, data_type in materialization_schema.column_name_and_data_types():
        assert data_type in TECTON_DATA_TYPE_TO_HIVE_TYPES, f"Unexpected data type {data_type}"
        hive_columns[col] = TECTON_DATA_TYPE_TO_HIVE_TYPES[data_type]

    if feature_definition.is_temporal_aggregate:
        if query_consts.anchor_time() not in hive_columns:
            msg = "Expected to find _anchor_time in materialized FeatureView schema"
            raise Exception(msg)
        # TODO(sanika): Clean this up. We have a bug somewhere - the materialization_schema indicates that the spark type for anchor_time is 4-byte integer. But we need 8 bytes.
        hive_columns[query_consts.anchor_time()] = "bigint"

    # Athena querytree expects the registered table to match the materialization schema.
    # We can remove this special handling when non QT is removed.
    if feature_definition.is_continuous and conf.get_bool("USE_DEPRECATED_ATHENA_RETRIEVAL"):
        if "timestamp" in hive_columns:
            # Special madness about continuous aggregates
            # The parquet files contain both a `timestamp` and an `_anchor_time` field. Same value in both, just a different type
            del hive_columns["timestamp"]

    if partition_by in hive_columns:
        del hive_columns[partition_by]

    athena_database = session.get_database()
    athena_table_spec = AthenaTableCreationSpec(
        database=athena_database,
        table=table_name,
        s3_location=s3_path,
        data_format=store_type,
        columns=hive_columns,
        partition_by=partition_by,
        partition_by_type=partition_by_type,
        partition_by_format=partition_by_format,
        partition_by_range_from=str(partition_by_range_from),
        partition_by_range_to=str(partition_by_range_to),
        partition_by_interval=partition_by_interval,
        partition_by_interval_timedelta=partition_by_interval_timedelta,
        partition_type=partition_type,
    )

    session.create_table_if_necessary(athena_table_spec)

    return athena_table_spec


def generate_sql_table_from_pandas_df(df: pandas.DataFrame, table_name: str, session: AthenaSession) -> str:
    """Generate a TABLE from pandas.DataFrame. Returns the sql query to select * from the table"""
    if session is None:
        msg = "Session must be provided"
        raise ValueError(msg)

    session.sql(f"DROP TABLE IF EXISTS {table_name}")
    table_expr = session.write_pandas(df, table_name)
    return f"SELECT * FROM {table_expr}"
