import contextlib
import inspect
import logging
import os
import time
from datetime import datetime
from typing import Optional

import boto3
import pyarrow.fs

from tecton_core.offline_store import PartitionType


os.environ["RAY_DEDUP_LOGS"] = "0"
import ray
from google.protobuf.json_format import MessageToJson

from tecton_core import conf
from tecton_core import function_deserialization
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.dialect import Dialect
from tecton_core.query.errors import UserCodeError
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_core.secret_management import SecretResolver
from tecton_core.sink_context import SinkContext
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.common.task_params import redact_sensitive_fields_from_params
from tecton_materialization.ray.batch_materialization import run_batch_materialization
from tecton_materialization.ray.dataset_generation import run_dataset_generation
from tecton_materialization.ray.delta import DeltaWriter
from tecton_materialization.ray.feature_export import get_feature_export_qt
from tecton_materialization.ray.feature_export import get_feature_export_store_params
from tecton_materialization.ray.iceberg import IcebergWriter
from tecton_materialization.ray.ingest_materialization import ingest_pushed_df
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_delta_writer
from tecton_materialization.ray.materialization_utils import get_secret_resolver
from tecton_materialization.ray.materialization_utils import get_writer_for_fd
from tecton_materialization.ray.materialization_utils import run_online_store_copier
from tecton_proto.args import transformation__client_pb2 as transformation__args_proto
from tecton_proto.materialization.job_metadata__client_pb2 import TectonManagedStage
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.materialization.params__client_pb2 import SecretMaterializationTaskParams
from tecton_proto.offlinestore.delta import metadata__client_pb2 as metadata_pb2
from tecton_proto.online_store_writer.copier__client_pb2 import DeletionRequest
from tecton_proto.online_store_writer.copier__client_pb2 import OnlineStoreCopierRequest


logger = logging.getLogger(__name__)

FEATURE_EXPORT_TASK_TYPE = "feature_export"

_DIALECT_TO_STAGE_TYPE = {
    Dialect.PANDAS: TectonManagedStage.PYTHON,
    Dialect.DUCKDB: TectonManagedStage.PYTHON,
    Dialect.SNOWFLAKE: TectonManagedStage.SNOWFLAKE,
}

_DIALECT_TO_UI_STRING = {
    Dialect.PANDAS: "Python",
    Dialect.DUCKDB: "Python",
    Dialect.SNOWFLAKE: "Snowflake",
}


def _delete_from_online_store(
    materialization_task_params: MaterializationTaskParams, job_status_client: JobStatusClient
) -> None:
    online_stage_monitor = job_status_client.create_stage_monitor(
        "Delete keys from online store",
    )
    with online_stage_monitor() as progress_callback:
        if materialization_task_params.deletion_task_info.deletion_parameters.HasField("online_join_keys_path"):
            deletion_request = DeletionRequest(
                online_join_keys_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_path,
            )
        else:
            deletion_request = DeletionRequest(
                online_join_keys_full_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_full_path,
            )
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=materialization_task_params.online_store_writer_config,
            feature_view=materialization_task_params.feature_view,
            deletion_request=deletion_request,
        )
        run_online_store_copier(request)
    progress_callback(1.0)


def _delete_from_offline_store(params: MaterializationTaskParams, job_status_client: JobStatusClient):
    offline_uri = params.deletion_task_info.deletion_parameters.offline_join_keys_path
    fs, path = pyarrow.fs.FileSystem.from_uri(offline_uri)
    keys_table = pyarrow.dataset.dataset(source=path, filesystem=fs).to_table()
    offline_stage_monitor = job_status_client.create_stage_monitor("Delete keys from offline store")
    with offline_stage_monitor():
        writer = get_writer_for_fd(params)
        writer.delete_keys(keys_table)
        writer.commit()


def _feature_export(
    fd: FeatureDefinitionWrapper,
    task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
    secret_resolver: Optional[SecretResolver],
):
    export_params = task_params.feature_export_info.feature_export_parameters
    start_time = export_params.feature_start_time.ToDatetime()
    end_time = export_params.feature_end_time.ToDatetime()
    table_uri = export_params.export_store_path

    delta_writer = None
    if table_uri:
        store_params = get_feature_export_store_params(fd)
        delta_writer = get_delta_writer(
            task_params,
            store_params=store_params,
            table_uri=table_uri,
            join_keys=fd.join_keys,
            partition_type=PartitionType.DATE_STR,
        )

    _run_export(
        fd,
        start_time,
        end_time,
        executor,
        job_status_client,
        delta_writer,
        secret_resolver,
    )


def _run_export(
    fd: FeatureDefinitionWrapper,
    start_time: datetime,
    end_time: datetime,
    qt_executor: QueryTreeExecutor,
    job_status_client: JobStatusClient,
    delta_writer: Optional[DeltaWriter],
    secret_resolver: Optional[SecretResolver] = None,
):
    qt_monitor = job_status_client.create_stage_monitor(
        "Prepare and execute query tree",
    )
    with qt_monitor():
        qt, interval = get_feature_export_qt(fd, start_time, end_time)
        qt_output = qt_executor.exec_qt(qt)

    feature_data = qt_output.result_table
    function_args = {}
    # Write to Sink
    if fd.sink_config:
        sink_config = fd.sink_config
        secrets = {}
        if sink_config.secrets:
            if not secret_resolver:
                msg = "No secret resolver was provided, but sink_config contains secrets!"
                raise TectonValidationError(msg)
            secrets = secret_resolver.resolve_map(sink_config.secrets)

        function = function_deserialization.from_proto(sink_config.function)
        params = list(inspect.signature(function).parameters)
        if "context" in params:
            function_args["context"] = SinkContext(
                feature_view_name=fd.name,
                feature_view_id=fd.id,
                workspace=fd.workspace,
                secrets=secrets,
                start_time=start_time,
                end_time=end_time,
            )
        sink_write_monitor = job_status_client.create_stage_monitor(
            f"Write full features to sink: {sink_config.name}",
        )

        with sink_write_monitor():
            if sink_config.mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PANDAS:
                # Turn into a table.
                feature_data = feature_data.read_all()
                function_args["df"] = feature_data.to_pandas()
            elif sink_config.mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYARROW:
                function_args["df"] = feature_data
            else:
                msg = f"Invalid sink mode: ${sink_config.mode}"
                raise TectonValidationError(msg)
            try:
                function(**function_args)
            except Exception as exc:
                msg = f"Invoking Sink Config: '{sink_config.name}' failed with exception."
                raise UserCodeError(msg) from exc

    # Write to export_store_path
    if delta_writer:
        delta_write_monitor = job_status_client.create_stage_monitor(
            "Write full features to offline store.",
        )
        # Rerun query tree to get another RecordBatchReader if we used pyarrow mode for the sink
        if (
            fd.sink_config
            and fd.sink_config.mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYARROW
        ):
            qt_output = qt_executor.exec_qt(qt)
            feature_data = qt_output.result_table
        with delta_write_monitor():
            # TODO (TEC-18865): add support for is_overwrite flag for feature_export jobs
            transaction_metadata = metadata_pb2.TectonDeltaMetadata()
            transaction_metadata.feature_start_time.FromDatetime(interval.start)

            @delta_writer.transaction(transaction_metadata)
            def txn():
                delta_writer.delete_time_range(interval)
                delta_writer.write(feature_data)

            txn()


@contextlib.contextmanager
def _ray(**kwargs):
    logging.warning(f"Initializing Ray from classpath: {os.environ['CLASSPATH']}")
    jvm_options = kwargs.pop("jvm_options", [])
    ray.init(
        job_config=ray.job_config.JobConfig(
            code_search_path=os.environ["CLASSPATH"].split(":"),
            # Increasing max heap size mostly for Online Store Copier.
            # Our target Parquet file size is around 1GB (although, not guaranteed, see delta.py),
            # so to download and decode such file 2-4GB might be needed.
            # Multiplying it by 2x factor for some buffer.
            jvm_options=["-Xmx16G", *jvm_options],
        ),
        include_dashboard=False,
        **kwargs,
    )
    try:
        yield
    finally:
        ray.shutdown()


def run_materialization(
    materialization_task_params: MaterializationTaskParams,
    secret_materialization_task_params: SecretMaterializationTaskParams,
) -> None:
    json_params = MessageToJson(materialization_task_params)
    redacted_json_params = redact_sensitive_fields_from_params(json_params)
    logger.info(f"Starting materialization with params: {redacted_json_params}")

    conf.set("DUCKDB_DEBUG", "true")
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "rift")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")

    # Sometimes we see transitory credential error on EC2, so we try to detect the error and fail early
    if _is_on_ec2_instance():
        _check_ec2_credential()

    job_status_client = JobStatusClient(JobMetadataClient.for_params(materialization_task_params))
    job_status_client.set_overall_state(TectonManagedStage.State.RUNNING)
    try:
        run_ray_job(materialization_task_params, secret_materialization_task_params, job_status_client)
        job_status_client.set_overall_state(TectonManagedStage.State.SUCCESS)
    except Exception:
        job_status_client.set_current_stage_failed(TectonManagedStage.ErrorType.UNEXPECTED_ERROR)
        job_status_client.set_overall_state(TectonManagedStage.State.ERROR)
        raise


def _is_on_ec2_instance() -> bool:
    return (
        os.environ.get("AWS_DEFAULT_REGION") is not None
        and os.environ.get("MATERIALIZATION_TASK_PARAMS_S3_URL") is not None
    )


def _check_ec2_credential() -> None:
    sts_client = boto3.client("sts")
    num_retries = 3
    for i in range(num_retries):
        try:
            sts_client.get_caller_identity()
            break
        except Exception as e:
            if i + 1 < num_retries:
                time.sleep(5)
                continue
            else:
                error_msg = f"Failed to get EC2 credential with error {str(e)}"
                raise Exception(error_msg)


def _run_delta_maintenance(materialization_task_params: MaterializationTaskParams) -> None:
    delta_writer = get_writer_for_fd(materialization_task_params)
    assert isinstance(delta_writer, DeltaWriter), f"Expected DeltaWriter but got {type(delta_writer).__name__}"

    maintenance_params = materialization_task_params.delta_maintenance_task_info.delta_maintenance_parameters
    if maintenance_params.execute_sorting:
        delta_writer.run_z_order_optimization()
        if maintenance_params.entity_sample_rows > 0:
            delta_writer.collect_sample_entities(maintenance_params.entity_sample_rows)
        delta_writer.commit()
    if maintenance_params.vacuum:
        # vacuuming is not implemented
        pass


def _run_iceberg_maintenance(
    materialization_task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
) -> None:
    iceberg_writer = get_writer_for_fd(materialization_task_params)
    assert isinstance(iceberg_writer, IcebergWriter), f"Expected IcebergWriter but got {type(iceberg_writer).__name__}"

    maintenance_params = materialization_task_params.iceberg_maintenance_task_info.iceberg_maintenance_parameters
    if maintenance_params.execute_compaction:
        compact_files_monitor = job_status_client.create_stage_monitor(
            "Compact small files < 100mb in offline store",
        )
        with compact_files_monitor():
            iceberg_writer.compact_files()
            iceberg_writer.commit()


def run_ray_job(
    materialization_task_params: MaterializationTaskParams,
    secret_materialization_task_params: SecretMaterializationTaskParams,
    job_status_client: JobStatusClient,
) -> None:
    secret_resolver = get_secret_resolver(secret_materialization_task_params.secret_service_params)
    task_type = _get_task_type(materialization_task_params)
    executor = QueryTreeExecutor(monitor=job_status_client, secret_resolver=secret_resolver)

    if task_type == "deletion_task":
        _delete_from_offline_store(materialization_task_params, job_status_client)
        _delete_from_online_store(materialization_task_params, job_status_client)
    elif task_type == "delta_maintenance_task":
        _run_delta_maintenance(materialization_task_params)
    elif task_type == "iceberg_maintenance_task":
        _run_iceberg_maintenance(materialization_task_params, job_status_client)
    elif task_type == "ingest_task":
        assert materialization_task_params.feature_view.schemas.HasField("materialization_schema"), "missing schema"
        fd = feature_definition_from_task_params(materialization_task_params)
        ingest_pushed_df(materialization_task_params, fd, job_status_client, executor)
    elif task_type == FEATURE_EXPORT_TASK_TYPE:
        fd = feature_definition_from_task_params(materialization_task_params)
        _feature_export(fd, materialization_task_params, job_status_client, executor, secret_resolver)
    elif task_type == "batch_task":
        assert materialization_task_params.feature_view.schemas.HasField("materialization_schema"), "missing schema"

        run_batch_materialization(materialization_task_params, job_status_client, executor)
    elif task_type == "dataset_generation_task":
        run_dataset_generation(materialization_task_params, secret_materialization_task_params, job_status_client)
    else:
        msg = f"Task type {task_type} is not supported by Ray materialization job"
        raise ValueError(msg)


def _get_task_type(materialization_task_params: MaterializationTaskParams) -> str:
    return materialization_task_params.WhichOneof("task_info")[:-5]  # removesuffix("_info")
