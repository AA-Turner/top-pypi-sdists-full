import typing
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas

import tecton_core.tecton_pendulum as pendulum
from tecton._internals.mock_source_utils import validate_mock_inputs
from tecton.framework.data_frame import TectonDataFrame
from tecton_core import feature_definition_wrapper
from tecton_core import specs
from tecton_core.errors import TectonSnowflakeNotImplementedError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.materialization_context import MaterializationContext
from tecton_core.snowflake_context import SnowflakeContext
from tecton_core.time_utils import get_timezone_aware_datetime
from tecton_proto.args import feature_view__client_pb2 as feature_view__args_pb2
from tecton_proto.args import transformation__client_pb2 as transformation__args_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.common import spark_schema__client_pb2 as spark_schema_pb2
from tecton_snowflake import schema_derivation_utils
from tecton_snowflake import sql_helper


if typing.TYPE_CHECKING:
    import snowflake.snowpark


def get_historical_features(
    feature_set_config: FeatureSetConfig,
    spine: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, TectonDataFrame, str]] = None,
    timestamp_key: Optional[str] = None,
    include_feature_view_timestamp_columns: bool = False,
    from_source: Optional[bool] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    entities: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, TectonDataFrame]] = None,
    append_prefix: bool = True,  # Whether to append the prefix to the feature column name
) -> TectonDataFrame:
    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    if entities is not None:
        # Convert entities to a snowflake dataframe
        if isinstance(entities, pandas.DataFrame):
            entities = TectonDataFrame._create(entities).to_snowpark()
        elif isinstance(entities, TectonDataFrame):
            entities = entities.to_snowpark()

    return TectonDataFrame._create_with_snowflake(
        sql_helper.get_historical_features_with_snowpark(
            spine=spine,
            session=SnowflakeContext.get_instance().get_session(),
            timestamp_key=timestamp_key,
            feature_set_config=feature_set_config,
            include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            append_prefix=append_prefix,
            from_source=from_source,
        )
    )


def run_batch(
    fd: FeatureDefinitionWrapper,
    mock_inputs: Dict[str, pandas.DataFrame],
    feature_start_time: datetime,
    feature_end_time: datetime,
    aggregation_level: Optional[str],
) -> TectonDataFrame:
    validate_mock_inputs(mock_inputs, fd)
    mock_sql_inputs = None

    feature_start_time = get_timezone_aware_datetime(feature_start_time)
    feature_end_time = get_timezone_aware_datetime(feature_end_time)

    if fd.is_temporal_aggregate:
        for feature in fd.fv_spec.aggregate_features:
            aggregate_function = sql_helper.AGGREGATION_PLANS[feature.function]
            if not aggregate_function:
                msg = f"Unsupported aggregation function {feature.function} in snowflake pipeline"
                raise TectonSnowflakeNotImplementedError(msg)

    session = SnowflakeContext.get_instance().get_session()

    if mock_inputs:
        mock_sql_inputs = {
            key: sql_helper.generate_sql_table_from_pandas_df(
                df=df, session=session, table_name=f"_TT_TEMP_INPUT_{key.upper()}_TABLE"
            )
            for (key, df) in mock_inputs.items()
        }

    # Validate input start and end times. Set defaults if None.
    sql_str = sql_helper.generate_run_batch_sql(
        feature_definition=fd,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        aggregation_level=aggregation_level,
        mock_sql_inputs=mock_sql_inputs,
        materialization_context=MaterializationContext._create_internal(
            pendulum.instance(feature_start_time),
            pendulum.instance(feature_end_time),
            fd.fv_spec.batch_schedule,
        ),
        session=session,
        from_source=True,  # For run() we don't use materialized data
    )
    return TectonDataFrame._create_with_snowflake(session.sql(sql_str))


def get_dataframe_for_data_source(
    data_source: specs.DataSourceSpec,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> TectonDataFrame:
    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    session = SnowflakeContext.get_instance().get_session()
    return TectonDataFrame._create_with_snowflake(
        sql_helper.get_dataframe_for_data_source(session, data_source.batch_source, start_time, end_time)
    )


# For notebook driven development
def derive_batch_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
) -> spark_schema_pb2.SparkSchema:
    if not ds_args.HasField("snowflake_ds_config"):
        msg = f"Invalid batch source args: {ds_args}"
        raise ValueError(msg)

    connection = SnowflakeContext.get_instance().get_connection()
    return schema_derivation_utils.get_snowflake_schema(ds_args, connection)


def derive_view_schema_for_feature_view(
    feature_view_args: feature_view__args_pb2.FeatureViewArgs,
    transformation_specs: List[specs.TransformationSpec],
    data_source_specs: List[specs.DataSourceSpec],
) -> schema_pb2.Schema:
    connection = SnowflakeContext.get_instance().get_connection()
    session = SnowflakeContext.get_instance().get_session()
    return schema_derivation_utils.get_feature_view_view_schema(
        feature_view_args, transformation_specs, data_source_specs, connection, session
    )


def has_snowpark_transformation(
    feature_definition_list: List[feature_definition_wrapper.FeatureDefinitionWrapper],
) -> bool:
    for feature_definition in feature_definition_list:
        has_snowpark_transformation = any(
            transformation.transformation_mode
            == transformation__args_pb2.TransformationMode.TRANSFORMATION_MODE_SNOWPARK
            for transformation in feature_definition.transformations
        )
        if has_snowpark_transformation:
            return True
    return False
