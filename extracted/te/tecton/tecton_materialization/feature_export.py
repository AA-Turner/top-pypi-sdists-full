import datetime
import inspect
import logging

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

import tecton_core.tecton_pendulum as pendulum
from tecton_core import function_deserialization
from tecton_core import specs
from tecton_core.errors import TectonValidationError
from tecton_core.fco_container import FcoContainer
from tecton_core.fco_container import create_fco_container
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.id_helper import IdHelper
from tecton_core.offline_store import PartitionType
from tecton_core.query.errors import UserCodeError
from tecton_core.query_consts import valid_from
from tecton_core.sink_context import SinkContext
from tecton_core.time_utils import convert_to_effective_timestamp
from tecton_materialization.batch_materialization import DEFAULT_COALESCE_FOR_S3
from tecton_materialization.materialization_utils import get_secret_resolver
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.materialization.params__client_pb2 import SecretMaterializationTaskParams
from tecton_spark.offline_store import DeltaWriter
from tecton_spark.offline_store import OfflineStoreWriterParams


logger = logging.getLogger(__name__)


def feature_export_from_params(
    spark: SparkSession, task_params: MaterializationTaskParams, secret_params: SecretMaterializationTaskParams
):
    export_params = task_params.feature_export_info.feature_export_parameters
    start_time = export_params.feature_start_time.ToDatetime()
    end_time = export_params.feature_end_time.ToDatetime()
    feature_view_id_str = IdHelper.to_string(task_params.feature_view.feature_view_id)
    parent_materialization_id_str = IdHelper.to_string(export_params.parent_materialization_task_id)

    logger.info(
        f"Starting feature export {task_params.materialization_task_id} job for feature view: {feature_view_id_str}, parent_materialization_task_id: {parent_materialization_id_str} for time range {start_time} to {end_time}"
    )
    fco_container = create_fco_container(
        list(task_params.virtual_data_sources) + list(task_params.transformations) + list(task_params.entities),
        include_main_variables_in_scope=True,
    )
    fv_spec = specs.create_feature_view_spec_from_data_proto(task_params.feature_view)
    fd = FeatureDefinitionWrapper(fv_spec, fco_container)

    spark_df, effective_tile = _get_features_in_range(fv_spec, fco_container, start_time, end_time)

    if spark_df.rdd.isEmpty():
        logging.info(
            f"No features found for materialization time range {start_time} to {end_time} and effective time range {effective_tile.start} to {effective_tile.end}"
        )
        return

    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"featureStartTime":"{export_params.feature_start_time.ToJsonString()}", "featureEndTime": "{export_params.feature_end_time.ToJsonString()}"}}',
    )
    is_write_optimized = spark.conf.get("spark.databricks.delta.optimizeWrite.enabled", None) == "true"
    df_to_write = spark_df if is_write_optimized else spark_df.coalesce(DEFAULT_COALESCE_FOR_S3)

    table_location = export_params.export_store_path

    if table_location:
        partition_size = datetime.timedelta(days=1)
        version = fd.get_feature_store_format_version
        logging.info(
            f"Writing features to {table_location} for materialization time range {start_time} to {end_time} and effective time range {effective_tile.start} to {effective_tile.end} with partition size={partition_size}"
        )

        export_store_params = OfflineStoreWriterParams(
            s3_path=table_location,
            always_store_anchor_column=True,
            time_column=valid_from(),
            join_key_columns=fd.join_keys,
            is_continuous=fd.is_continuous,
            upsert_by_batch_publish_timestamp=False,
        )

        writer = DeltaWriter(export_store_params, spark, version, partition_size, PartitionType.DATE_STR)
        writer.overwrite_dataframe_in_tile(df_to_write, effective_tile)

    # Write to Sink
    if fd.sink_config:
        sink_config = fd.sink_config
        secrets = {}
        secret_resolver = get_secret_resolver(secret_params.secret_service_params) if secret_params else None
        if sink_config.secrets:
            if not secret_resolver:
                msg = "No secret resolver was provided, but sink_config contains secrets!"
                raise TectonValidationError(msg)
            secrets = secret_resolver.resolve_map(sink_config.secrets)

        function = function_deserialization.from_proto(sink_config.function)
        function_args = {"df": df_to_write}
        params = list(inspect.signature(function).parameters)
        if "context" in params:
            function_args["context"] = SinkContext(
                feature_view_name=fd.name,
                feature_view_id=fd.id,
                workspace=fd.workspace,
                start_time=start_time,
                end_time=end_time,
                secrets=secrets,
            )

        try:
            function(**function_args)
        except Exception as exc:
            msg = f"Invoking Sink Config: '{sink_config.name}' failed with exception."
            raise UserCodeError(msg) from exc


def _get_features_in_range(
    fv_spec: specs.FeatureViewSpec,
    fco_container: FcoContainer,
    materialization_start_time: datetime.datetime,
    materialization_end_time: datetime.datetime,
) -> (DataFrame, pendulum.Period):
    from tecton.framework.feature_view import feature_view_from_spec

    fdw = FeatureDefinitionWrapper(fv_spec, fco_container)
    fv = feature_view_from_spec(fv_spec, fco_container)

    # get_features_in_range queries features based on their effective timestamp
    batch_schedule_seconds = fdw.batch_materialization_schedule.in_seconds()
    data_delay = fdw.online_store_data_delay_seconds
    effective_start_time = datetime.datetime.fromtimestamp(
        convert_to_effective_timestamp(int(materialization_start_time.timestamp()), batch_schedule_seconds, data_delay)
    )
    effective_end_time = datetime.datetime.fromtimestamp(
        convert_to_effective_timestamp(int(materialization_end_time.timestamp()), batch_schedule_seconds, data_delay)
    )

    tecton_df = fv.get_features_in_range(
        start_time=effective_start_time, end_time=effective_end_time, from_source=False
    )

    try:
        df = tecton_df.to_spark()
    except AnalysisException as e:
        # TODO: handle empty stores better instead of relying on string matching on an error
        if "Unable to infer schema for Parquet. It must be specified manually." in str(e):
            logger.warning("Unable to infer Parquet schema; assuming staging offline store is empty")
            return
        else:
            raise

    return df, pendulum.period(effective_start_time, effective_end_time)
