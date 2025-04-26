import re
import typing
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Union

import pandas
from google.protobuf import duration_pb2

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import data_types
from tecton_core import errors
from tecton_core import specs
from tecton_core.errors import INVALID_SPINE_SQL
from tecton_core.errors import START_TIME_NOT_BEFORE_END_TIME
from tecton_core.errors import TectonSnowflakeNotImplementedError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.materialization_context import MaterializationContext
from tecton_core.query_consts import udf_internal
from tecton_core.time_utils import convert_pandas_df_for_snowflake_upload
from tecton_proto.common import aggregation_function__client_pb2 as afpb
from tecton_proto.data import feature_view__client_pb2 as feature_view_pb2
from tecton_snowflake.pipeline_helper import pipeline_to_df_with_input
from tecton_snowflake.pipeline_helper import pipeline_to_sql_string
from tecton_snowflake.templates_utils import load_template
from tecton_snowflake.utils import format_sql
from tecton_snowflake.utils import generate_random_name


if typing.TYPE_CHECKING:
    import snowflake.connector
    import snowflake.snowpark


TEMP_SPINE_TABLE_NAME_FROM_DF = "_TEMP_SPINE_TABLE_FROM_DF"
TEMP_SPINE_TABLE_NAME_PREFIX = "_TT_SPINE_TABLE"

FULL_AGGREGATION_TEMPLATE = load_template("run_full_aggregation.sql")
HISTORICAL_FEATURES_TEMPLATE = load_template("historical_features.sql")
MATERIALIZATION_TILE_TEMPLATE = load_template("materialization_tile.sql")
MATERIALIZED_FEATURE_VIEW_TEMPLATE = load_template("materialized_feature_view.sql")
ONLINE_STORE_COPIER_TEMPLATE = load_template("online_store_copier.sql")
PARTIAL_AGGREGATION_TEMPLATE = load_template("run_partial_aggregation.sql")
TIME_LIMIT_TEMPLATE = load_template("time_limit.sql")
DELETE_STAGED_FILES_TEMPLATE = load_template("delete_staged_files.sql")
CREATE_TEMP_TABLE_BFV_TEMPLATE = load_template("create_temp_table_for_bfv.sql")
CREATE_TEMP_TABLE_BWAFV_TEMPLATE = load_template("create_temp_table_for_bwafv.sql")
DELETE_ORPHANED_SCHEMAS_TEMPLATE = load_template("delete_orphaned_schemas.sql")

# TODO(TEC-6204): Last and LastN are not currently supported
#
# Map of proto function type -> set of (output column prefix, snowflake function name)
AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: lambda: {("SUM", "SUM")},
    afpb.AGGREGATION_FUNCTION_MIN: lambda: {("MIN", "MIN")},
    afpb.AGGREGATION_FUNCTION_MAX: lambda: {("MAX", "MAX")},
    afpb.AGGREGATION_FUNCTION_COUNT: lambda: {("COUNT", "COUNT")},
    afpb.AGGREGATION_FUNCTION_MEAN: lambda: {("COUNT", "COUNT"), ("MEAN", "AVG")},
    # sample variation equation: (Σ(x^2) - (Σ(x)^2)/N)/N-1
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: lambda: {
        ("SUM", "SUM"),
        ("COUNT", "COUNT"),
        ("SUM_OF_SQUARES", "SUM_OF_SQUARES"),
    },
    # population variation equation: Σ(x^2)/n - μ^2
    afpb.AGGREGATION_FUNCTION_VAR_POP: lambda: {
        ("SUM", "SUM"),
        ("COUNT", "COUNT"),
        ("SUM_OF_SQUARES", "SUM_OF_SQUARES"),
    },
    # sample standard deviation equation: √ ((Σ(x^2) - (Σ(x)^2)/N)/N-1)
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: lambda: {
        ("SUM", "SUM"),
        ("COUNT", "COUNT"),
        ("SUM_OF_SQUARES", "SUM_OF_SQUARES"),
    },
    # population standard deviation equation: √ (Σ(x^2)/n - μ^2)
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: lambda: {
        ("SUM", "SUM"),
        ("COUNT", "COUNT"),
        ("SUM_OF_SQUARES", "SUM_OF_SQUARES"),
    },
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: lambda n, is_continuous: {
        ("LAST_NON_DISTINCT_N" + (str(n) if not is_continuous else ""), n),
    },
    afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: lambda n, is_continuous: {
        ("FIRST_NON_DISTINCT_N" + (str(n) if not is_continuous else ""), n),
    },
}


@dataclass
class _FeatureSetItemInput:
    """A simplified version of FeatureSetItem which is passed to the SQL template."""

    name: str
    namespace: str
    timestamp_key: str
    join_keys: Dict[str, str]
    features: List[str]
    sql: str
    aggregation: Optional[feature_view_pb2.TrailingTimeWindowAggregation]
    ttl_seconds: Optional[int]
    append_prefix: bool
    batch_schedule: int
    data_delay: int


def get_historical_features_sql(
    spine_sql: Optional[str],
    feature_set_config: FeatureSetConfig,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
    include_feature_view_timestamp_columns: bool = False,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    session: "snowflake.snowpark.Session" = None,
    append_prefix: bool = True,  # Whether to append the prefix to the feature column name
) -> List[str]:
    suffix = generate_random_name()
    spine_table_name = f"{TEMP_SPINE_TABLE_NAME_PREFIX}_{suffix}"
    # Whether to register temp views with the session, or use a giant query
    use_short_sql = conf.get_bool("SNOWFLAKE_SHORT_SQL_ENABLED")
    use_temp_table = conf.get_bool("SNOWFLAKE_TEMP_TABLE_ENABLED")
    feature_set_items = feature_set_config.definitions_and_configs
    input_items = []
    if spine_sql is None:
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

    for item in feature_set_items:
        fd = item.feature_definition
        # Change the feature view name if it's for internal udf use.
        is_internal_udf_feature = item.namespace.startswith(udf_internal())
        if is_internal_udf_feature:
            name = item.namespace.upper()
        else:
            name = fd.name

        if not fd.is_rtfv:
            join_keys = dict(item.join_keys)
            features = [
                col_name
                for col_name in fd.view_schema.column_names()
                if col_name not in ([*list(join_keys.keys()), fd.timestamp_key])
            ]
            if len(fd.online_serving_index.join_keys) != len(fd.join_keys):
                msg = "Wildcard is not supported for Snowflake"
                raise TectonSnowflakeNotImplementedError(msg)
            if fd.is_incremental_backfill and from_source:
                raise errors.FV_BFC_SINGLE_FROM_SOURCE
            if start_time is None or (
                fd.feature_start_timestamp is not None and start_time < fd.feature_start_timestamp
            ):
                raw_data_start_time = fd.feature_start_timestamp
            else:
                raw_data_start_time = start_time

            raw_data_end_time = end_time
            if fd.is_temporal_aggregate and raw_data_start_time is not None:
                # Account for final aggregation needing aggregation window prior to earliest timestamp
                raw_data_start_time = raw_data_start_time + fd.earliest_window_start

            sql_str = generate_run_batch_sql(
                feature_definition=fd,
                feature_start_time=raw_data_start_time,
                feature_end_time=raw_data_end_time,
                # If the spine sql has undetermined results(LIMIT X etc.), we don't want
                # to run it twice. So we use the subquery we defined here directly.
                spine=spine_table_name if spine_sql is not None else None,
                spine_timestamp_key=timestamp_key,
                session=session,
                from_source=from_source,
                data_delay=fd.max_source_data_delay,
            )
            input_items.append(
                _FeatureSetItemInput(
                    name=name,
                    namespace=item.namespace or name,
                    timestamp_key=fd.timestamp_key,
                    join_keys=join_keys,
                    features=features,
                    sql=sql_str,
                    aggregation=(fd.trailing_time_window_aggregation() if fd.is_temporal_aggregate else None),
                    ttl_seconds=(int(fd.serving_ttl.total_seconds()) if fd.is_temporal else None),
                    append_prefix=append_prefix or is_internal_udf_feature,
                    batch_schedule=0
                    if fd.min_scheduling_interval is None
                    else int(fd.min_scheduling_interval.total_seconds()),
                    data_delay=fd.max_source_data_delay.total_seconds(),
                )
            )
    queries = []

    if spine_sql is not None:
        if use_short_sql or use_temp_table:
            view_or_table = "TABLE" if use_temp_table else "VIEW"
            queries.append(f"CREATE TEMPORARY {view_or_table} {spine_table_name} AS ({spine_sql})")
            for item in input_items:
                if item.aggregation is not None:
                    queries.append(
                        format_sql(
                            CREATE_TEMP_TABLE_BWAFV_TEMPLATE.render(
                                item=item,
                                spine_table_name=spine_table_name,
                                spine_keys=list(spine_keys),
                                spine_timestamp_key=timestamp_key,
                                suffix=suffix,
                                view_or_table=view_or_table,
                            )
                        )
                    )
                else:
                    queries.append(
                        format_sql(
                            CREATE_TEMP_TABLE_BFV_TEMPLATE.render(
                                item=item,
                                spine_table_name=spine_table_name,
                                spine_keys=list(spine_keys),
                                spine_timestamp_key=timestamp_key,
                                include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
                                suffix=suffix,
                                view_or_table=view_or_table,
                            )
                        )
                    )
        sql_str = HISTORICAL_FEATURES_TEMPLATE.render(
            feature_set_items=input_items,
            spine_timestamp_key=timestamp_key,
            spine_sql=spine_sql,
            include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
            spine_keys=list(spine_keys),
            use_temp_tables=use_short_sql or use_temp_table,
            spine_table_name=spine_table_name,
            suffix=suffix,
        )
    if start_time is not None or end_time is not None:
        timestamp = timestamp_key if spine_sql is not None else fd.timestamp_key
        sql_str = TIME_LIMIT_TEMPLATE.render(
            source=sql_str, timestamp_key=timestamp, start_time=start_time, end_time=end_time
        )
    queries.append(format_sql(sql_str))
    if conf.get_bool("SNOWFLAKE_DEBUG"):
        print(f"Generated {len(queries)} Snowflake SQL for get_historical_features, this does not include ODFV:")
        for query in queries:
            print(query)
    return queries


def get_historical_features(
    spine: Optional[Union[pandas.DataFrame, str]],
    connection: "snowflake.connector.Connection",
    feature_set_config: FeatureSetConfig,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
    include_feature_view_timestamp_columns: bool = False,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    append_prefix: bool = True,  # Whether to append the prefix to the feature column name
) -> pandas.DataFrame:
    cur = connection.cursor()
    spine_sql = None
    if isinstance(spine, str):
        spine_sql = spine
    elif isinstance(spine, pandas.DataFrame):
        spine_sql = generate_sql_table_from_pandas_df(
            df=spine, table_name=TEMP_SPINE_TABLE_NAME_FROM_DF, connection=connection
        )

    sql_strs = get_historical_features_sql(
        spine_sql=spine_sql,
        feature_set_config=feature_set_config,
        timestamp_key=timestamp_key,
        include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
        start_time=start_time,
        end_time=end_time,
        append_prefix=append_prefix,
        from_source=from_source,
    )
    for sql_str in sql_strs:
        cur.execute(sql_str, _statement_params={"SF_PARTNER": "tecton-ai"})
    return cur.fetch_pandas_all()


def generate_sql_table_from_pandas_df(
    df: pandas.DataFrame,
    table_name: str,
    session: "snowflake.snowpark.Session" = None,
    connection: "snowflake.connector.Connection" = None,
) -> str:
    """Generate a TABLE from pandas.DataFrame. Returns the sql query to select * from the table"""
    if session is None and connection is None:
        msg = "Either session or connection must be provided"
        raise ValueError(msg)

    if session is not None:
        session.sql(f"DROP TABLE IF EXISTS {table_name}").collect(statement_params={"SF_PARTNER": "tecton-ai"})
        convert_pandas_df_for_snowflake_upload(df)
        session.write_pandas(df, table_name, auto_create_table=True, table_type="temporary", use_logical_type=True)
        return f"SELECT * FROM {table_name}"

    if connection is not None:
        from snowflake.connector.pandas_tools import write_pandas

        # Get the SQL that would be generated by the create table statement
        create_table_sql = pandas.io.sql.get_schema(df, table_name)

        # Replace the `CREATE TABLE` with `CREATE OR REPLACE TEMPORARY TABLE`
        create_tmp_table_sql = re.sub("^(CREATE TABLE)?", "CREATE OR REPLACE TEMPORARY TABLE", create_table_sql)
        cur = connection.cursor()
        cur.execute(create_tmp_table_sql, _statement_params={"SF_PARTNER": "tecton-ai"})
        write_pandas(conn=connection, df=df, table_name=table_name, use_logical_type=True)
        return f"SELECT * FROM {table_name}"


def validate_spine_dataframe(
    spine_df: "snowflake.snowpark.DataFrame",
    timestamp_key: str,
    join_keys: List[str],
    request_context_keys: List[str] = [],
):
    from snowflake.snowpark import types

    if timestamp_key not in spine_df.columns:
        msg = f"Expected to find '{timestamp_key}' among available spine columns: '{', '.join(spine_df.columns)}'."
        raise errors.TectonValidationError(msg)
    for field in spine_df.schema.fields:
        if field.name == timestamp_key and not isinstance(field.datatype, types.TimestampType):
            msg = f"Invalid type of timestamp_key column in the given spine. Expected Timestamp, got {field.datatype}"
            raise errors.TectonValidationError(msg)
    for key in join_keys + request_context_keys:
        if key not in spine_df.columns:
            msg = f"Expected to find '{key}' among available spine columns: '{', '.join(spine_df.columns)}'."
            raise errors.TectonValidationError(msg)


def get_historical_features_with_snowpark(
    spine: Union[pandas.DataFrame, str, "snowflake.snowpark.DataFrame"],
    session: "snowflake.snowpark.Session",
    feature_set_config: FeatureSetConfig,
    timestamp_key: Optional[str],
    from_source: Optional[bool],
    include_feature_view_timestamp_columns: bool = False,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    entities: "snowflake.snowpark.DataFrame" = None,
    append_prefix: bool = True,  # Whether to append the prefix to the feature column name
) -> "snowflake.snowpark.DataFrame":
    from snowflake.snowpark import DataFrame
    from snowflake.snowpark import types

    spine_sql = None
    if isinstance(spine, str):
        spine_sql = spine
    elif isinstance(spine, DataFrame):
        spine.write.save_as_table(TEMP_SPINE_TABLE_NAME_FROM_DF, mode="overwrite", table_type="temporary")
        spine_sql = f"SELECT * FROM {TEMP_SPINE_TABLE_NAME_FROM_DF}"
    elif isinstance(spine, pandas.DataFrame):
        spine_sql = generate_sql_table_from_pandas_df(
            df=spine, table_name=TEMP_SPINE_TABLE_NAME_FROM_DF, session=session
        )

    if spine is not None:
        # validate spine sql
        try:
            spine_df = session.sql(spine_sql)
            spine_schema = spine_df.schema
        except Exception as e:
            raise INVALID_SPINE_SQL(e)
        if timestamp_key is None:
            schema = spine_schema
            timestamp_cols = [field.name for field in schema.fields if isinstance(field.datatype, types.TimestampType)]

            if len(timestamp_cols) > 1 or len(timestamp_cols) == 0:
                msg = f"Could not infer timestamp keys from {schema}; please specify explicitly"
                raise errors.TectonValidationError(msg)
            timestamp_key = timestamp_cols[0]

        join_keys = [join_key for fd in feature_set_config.feature_definitions for join_key in fd.join_keys]
        request_context_keys = [key for fd in feature_set_config.feature_definitions for key in fd.request_context_keys]
        validate_spine_dataframe(
            spine_df, timestamp_key, join_keys=join_keys, request_context_keys=request_context_keys
        )

    sql_strs = get_historical_features_sql(
        spine_sql=spine_sql,
        feature_set_config=feature_set_config,
        timestamp_key=timestamp_key,
        include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
        start_time=start_time,
        end_time=end_time,
        session=session,
        append_prefix=append_prefix,
        from_source=from_source,
    )
    for sql_str in sql_strs[:-1]:
        session.sql(sql_str).collect(statement_params={"SF_PARTNER": "tecton-ai"})
    output_df = session.sql(sql_strs[-1])

    # Apply ODFV to the spine.
    for item in feature_set_config.definitions_and_configs:
        fd = item.feature_definition
        if fd.is_rtfv:
            schema_dict = fd.view_schema.to_dict()
            output_df = pipeline_to_df_with_input(
                session=session,
                input_df=output_df,
                pipeline=fd.pipeline,
                transformations=fd.transformations,
                output_schema=schema_dict,
                name=fd.name,
                fv_id=fd.id,
                namespace=item.namespace or fd.name,
                append_prefix=append_prefix,
            )
    columns_to_drop = [column for column in output_df.columns if "_UDF_INTERNAL_" in column]
    if len(columns_to_drop) > 0:
        output_df = output_df.drop(*columns_to_drop)
    if entities is not None:
        column_names = [field.name for field in entities.schema.fields]
        # Do an inner join on the entities to filter out rows that don't have a matching entity
        output_df = entities.join(right=output_df, using_columns=column_names, join_type="inner")
    return output_df


def generate_run_batch_sql(
    feature_definition: FeatureDefinitionWrapper,
    from_source: Optional[bool],
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
    materialization_context: Optional[MaterializationContext] = None,
    session: "snowflake.snowpark.Session" = None,
    data_delay: Optional[pendulum.Duration] = None,
) -> str:
    # Set a default materilization_context if not provided.
    # This is following the same logic as spark.
    if materialization_context is None:
        materialization_feature_start_time = feature_start_time or pendulum.from_timestamp(0, pendulum.tz.UTC)
        materialization_feature_end_time = feature_end_time or pendulum.datetime(2100, 1, 1)
        if not materialization_feature_start_time < materialization_feature_end_time:
            raise START_TIME_NOT_BEFORE_END_TIME(materialization_feature_start_time, materialization_feature_end_time)

        materialization_context = MaterializationContext._create_internal(
            materialization_feature_start_time,
            materialization_feature_end_time,
            feature_definition.fv_spec.batch_schedule,
        )

    if from_source is None:
        from_source = not feature_definition.materialization_enabled or not feature_definition.writes_to_offline_store

    if from_source is False:
        if not feature_definition.materialization_enabled or not feature_definition.writes_to_offline_store:
            raise errors.FV_NEEDS_TO_BE_MATERIALIZED(feature_definition.name)

    if from_source:
        pipeline_sql = pipeline_to_sql_string(
            pipeline=feature_definition.pipeline,
            data_sources=feature_definition.data_sources,
            transformations=feature_definition.transformations,
            materialization_context=materialization_context,
            mock_sql_inputs=mock_sql_inputs,
            session=session,
        )
        materialized_sql = get_materialization_query(
            feature_definition=feature_definition,
            feature_start_time=feature_start_time,
            feature_end_time=feature_end_time,
            source=pipeline_sql,
            offline_materialization=True,
        )
    else:
        materialized_sql = TIME_LIMIT_TEMPLATE.render(
            source=f"SELECT * FROM {feature_definition.fv_spec.snowflake_view_name}",
            timestamp_key=feature_definition.time_key,
            start_time=feature_start_time,
            end_time=feature_end_time,
        )
    if feature_definition.is_temporal_aggregate:
        if aggregation_level == "full":
            aggregated_sql_str = FULL_AGGREGATION_TEMPLATE.render(
                source=materialized_sql,
                join_keys=feature_definition.join_keys,
                aggregation=feature_definition.trailing_time_window_aggregation(),
                timestamp_key=feature_definition.time_key,
                name=feature_definition.name,
                spine=spine,
                spine_timestamp_key=spine_timestamp_key,
                spine_keys=spine_keys,
                batch_schedule=int(materialization_context.batch_schedule.total_seconds()),
                data_delay=int(data_delay.total_seconds()) if data_delay else 0,
                continuous=feature_definition.is_continuous,
                offline_materialization=True,
                is_continuous=feature_definition.is_continuous,
            )
            return format_sql(aggregated_sql_str)
        elif aggregation_level == "partial":
            # Rename the output columns, and add tile start/end time columns
            partial_aggregated_sql_str = PARTIAL_AGGREGATION_TEMPLATE.render(
                source=materialized_sql,
                join_keys=feature_definition.join_keys,
                aggregations=_get_feature_view_aggregations(feature_definition),
                slide_interval=feature_definition.aggregate_slide_interval,
                slide_interval_string=feature_definition.get_aggregate_slide_interval_string,
                timestamp_key=feature_definition.time_key,
            )
            return format_sql(partial_aggregated_sql_str)
        elif aggregation_level == "disabled":
            sql_str = TIME_LIMIT_TEMPLATE.render(
                source=pipeline_sql,
                timestamp_key=feature_definition.time_key,
                start_time=feature_start_time,
                end_time=feature_end_time,
            )
            return format_sql(sql_str)
        else:
            msg = f"Unsupported aggregation level: {aggregation_level}"
            raise ValueError(msg)

    else:
        return format_sql(materialized_sql)


# By default Snowflake unloads numerical types as byte arrays because they have higher precision than available Parquet
# types. We could decode these in the OnlineStoreCopier, but since we will be downcasting them to the precision of
# Parquet types we might as well do it now.
#
# Snowflake docs for how casting interacts with Parquet types:
# https://docs.snowflake.com/en/user-guide/data-unload-considerations.html#explicitly-converting-numeric-columns-to-parquet-data-types
COPY_CASTS = {
    data_types.Int64Type(): "BIGINT",
    data_types.Float64Type(): "DOUBLE",
}


def get_materialization_query(
    feature_definition: FeatureDefinitionWrapper,
    source: str,
    # start is inclusive and end is exclusive
    feature_start_time: Optional[datetime] = None,
    feature_end_time: Optional[datetime] = None,
    # Whether we are building offline materialization query. If we are building an materialization query, in continuous
    # mode, we will have to hardcode the schedule interval to 1 day
    offline_materialization: bool = False,
):
    """Returns a SQL query for time-limited materialization.

    Does not include a terminating `;` or any COPY or INSERT statements."""

    if feature_definition.is_temporal_aggregate:
        source = MATERIALIZATION_TILE_TEMPLATE.render(
            source=source,
            join_keys=feature_definition.join_keys,
            aggregations=_get_feature_view_aggregations(feature_definition),
            slide_interval=feature_definition.aggregate_slide_interval,
            timestamp_key=feature_definition.time_key,
            continuous=feature_definition.is_continuous,
            offline_materialization=offline_materialization,
        )
    return format_sql(
        TIME_LIMIT_TEMPLATE.render(
            source=source,
            timestamp_key=feature_definition.time_key,
            start_time=feature_start_time,
            end_time=feature_end_time,
        )
    )


def get_delete_staged_files_sql(destination_stage: str, days: int):
    # Note the double quotes around destination_stage are required for the SQL to format properly
    script_sql = DELETE_STAGED_FILES_TEMPLATE.render(
        destination_stage=f"'{destination_stage}'",
        days=days,
    )
    sql = "\n".join(("EXECUTE IMMEDIATE", "$$", format_sql(script_sql), "$$;"))
    return format_sql(sql)


def get_delete_orphaned_schemas_sql(snowflake_database: str):
    script_sql = DELETE_ORPHANED_SCHEMAS_TEMPLATE.render(
        snowflake_database=snowflake_database,
    )
    sql = "\n".join(("EXECUTE IMMEDIATE", "$$", format_sql(script_sql), "$$;"))
    return format_sql(sql)


def get_materialization_copy_sql(
    feature_definition: FeatureDefinitionWrapper,
    # start is inclusive and end is exclusive
    time_limits: pendulum.Period,
    destination_stage: Optional[str],
    destination_table: Optional[str],
    # this is materialization task id; it's probably being used incorrectly because
    # different attempts can share the same task id.
    materialization_id: str,
    session: "snowflake.snowpark.Session" = None,
    # If provided, this query will be used instead of the feature_definition
    materialization_query: Optional[str] = None,
):
    """
    TODO(TEC-16752): Deprecate this once snowpark support is fully removed.
    Returns a SQL query for a COPY INTO an destination_stage for materialization.
    Additionally INSERTs into destination_table for manually-materialized FeatureViews.
    """

    materialization_context = MaterializationContext._create_internal(
        time_limits.start, time_limits.end, feature_definition.fv_spec.batch_schedule
    )
    materialize_online = destination_stage is not None
    materialize_offline = destination_table is not None
    if materialization_query is None:
        source = pipeline_to_sql_string(
            pipeline=feature_definition.pipeline,
            data_sources=feature_definition.data_sources,
            transformations=feature_definition.transformations,
            materialization_context=materialization_context,
            session=session,
        )

        materialization_query = get_materialization_query(
            source=source,
            feature_definition=feature_definition,
            feature_start_time=time_limits.start,
            feature_end_time=time_limits.end,
            offline_materialization=materialize_offline,
        )
    common_context = {
        "source": materialization_query,
        "materialize_online": materialize_online,
        "materialize_offline": materialize_offline,
        "destination_stage": destination_stage,
        "materialization_schema": feature_definition.materialization_schema.to_proto(),
        "materialization_id": materialization_id,
        "cast_types": COPY_CASTS,
    }
    if materialize_offline:
        view_name = feature_definition.fv_spec.snowflake_view_name
        database, schema, view = view_name.split(".")
        script_sql = MATERIALIZED_FEATURE_VIEW_TEMPLATE.render(
            destination_table=destination_table,
            workspace=f"{database}.{schema}",
            destination_view=view_name,
            start_time=time_limits.start,
            end_time=time_limits.end,
            continuous=feature_definition.is_continuous,
            timestamp_field=feature_definition.time_key,
            is_aggregate=feature_definition.is_temporal_aggregate,
            slide_interval=feature_definition.aggregate_slide_interval
            if feature_definition.is_temporal_aggregate
            else duration_pb2.Duration(),
            **common_context,
        )
        sql = "\n".join(("EXECUTE IMMEDIATE", "$$", format_sql(script_sql), "$$;"))
    else:
        sql = ONLINE_STORE_COPIER_TEMPLATE.render(**common_context)
    return format_sql(sql)


def get_dataframe_for_data_source(
    session: "snowflake.snowpark.Session",
    data_source: specs.BatchSourceSpec,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> "snowflake.snowpark.DataFrame":
    assert isinstance(
        data_source, specs.SnowflakeSourceSpec
    ), f"Snowflake compute only supports Snowflake data sources. Got: {data_source}."

    if data_source.query:
        source = data_source.query
    else:
        source = f"{data_source.database}.{data_source.schema}.{data_source.table}"

    if (start_time is not None or end_time is not None) and data_source.timestamp_field is None:
        msg = "Filtering by start_time or end_time requires the timestamp_field parameter to be set on this data source"
        raise ValueError(msg)
    sql_str = TIME_LIMIT_TEMPLATE.render(
        source=source,
        timestamp_key=data_source.timestamp_field,
        start_time=start_time,
        end_time=end_time,
    )
    return session.sql(sql_str)


def _get_feature_view_aggregations(feature_definition: FeatureDefinitionWrapper) -> Dict[str, Set[str]]:
    aggregations = defaultdict(set)
    is_continuous = feature_definition.is_continuous
    # For continuous features, we only keep one aggregation function for first/last non distinct n for each input feature
    if is_continuous:
        max_first_distinct_n_aggs = defaultdict(int)
        max_last_distinct_n_aggs = defaultdict(int)

    for feature in feature_definition.fv_spec.aggregate_features:
        aggregate_function_lambda = AGGREGATION_PLANS[feature.function]
        if not aggregate_function_lambda:
            msg = f"Unsupported aggregation function {feature.function} in snowflake pipeline"
            raise TectonSnowflakeNotImplementedError(msg)
        if feature.function == afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N:
            if is_continuous:
                max_last_distinct_n_aggs[feature.input_feature_name] = max(
                    max_last_distinct_n_aggs[feature.input_feature_name], feature.function_params.last_n.n
                )
                continue
            aggregate_function = aggregate_function_lambda(feature.function_params.last_n.n, is_continuous)
        elif feature.function == afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N:
            if is_continuous:
                max_first_distinct_n_aggs[feature.input_feature_name] = max(
                    max_first_distinct_n_aggs[feature.input_feature_name], feature.function_params.first_n.n
                )
                continue
            aggregate_function = aggregate_function_lambda(feature.function_params.first_n.n, is_continuous)
        else:
            aggregate_function = aggregate_function_lambda()
        aggregations[feature.input_feature_name].update(aggregate_function)

    if is_continuous:
        for feature_name, max_last_n in max_last_distinct_n_aggs.items():
            aggregations[feature_name].update(
                AGGREGATION_PLANS[afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N](max_last_n, is_continuous)
            )
        for feature_name, max_first_n in max_first_distinct_n_aggs.items():
            aggregations[feature_name].update(
                AGGREGATION_PLANS[afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N](max_first_n, is_continuous)
            )

    # Need to order the functions for deterministic results.
    for key, value in aggregations.items():
        aggregations[key] = sorted(value)

    return aggregations
