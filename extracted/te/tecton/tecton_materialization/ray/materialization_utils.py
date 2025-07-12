import urllib
from typing import List
from typing import Optional

import ray
from google.protobuf import timestamp_pb2

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.offline_store import PartitionType
from tecton_core.offline_store import partition_type_for_delta
from tecton_core.secret_management import SecretResolver
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.mds_secrets import MDSSecretResolver
from tecton_materialization.ray.delta import DeltaWriter
from tecton_materialization.ray.delta import OfflineStoreParams
from tecton_materialization.ray.iceberg import IcebergWriter
from tecton_materialization.ray.offline_store_writer import OfflineStoreWriter
from tecton_proto.data.feature_view__client_pb2 import FeatureView
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams
from tecton_proto.materialization.params__client_pb2 import SecretServiceParams
from tecton_proto.online_store_writer.config__client_pb2 import OnlineStoreWriterConfiguration
from tecton_proto.online_store_writer.copier__client_pb2 import GCSStage
from tecton_proto.online_store_writer.copier__client_pb2 import LocalFileStage
from tecton_proto.online_store_writer.copier__client_pb2 import ObjectCopyRequest
from tecton_proto.online_store_writer.copier__client_pb2 import OnlineStoreCopierRequest
from tecton_proto.online_store_writer.copier__client_pb2 import S3Stage
from tecton_proto.online_store_writer.copier__client_pb2 import StatusUpdateRequest
from tecton_proto.online_store_writer.copier__client_pb2 import TimestampUnit


def run_online_store_copier(request):
    request_bytes = request.SerializeToString()
    runner_function = ray.cross_language.java_function(
        "com.tecton.onlinestorewriter.OnlineStoreCopier", "runFromSerializedRequest"
    )
    job = runner_function.remote(request_bytes, None)
    ray.get(job)


def write_to_online_store(
    online_store_writer_config: OnlineStoreWriterConfiguration,
    feature_view: FeatureView,
    feature_end_timestamp: timestamp_pb2.Timestamp,
    fd: FeatureDefinitionWrapper,
    stage_uri_str: str,
) -> None:
    stage_uri = urllib.parse.urlparse(stage_uri_str)
    if stage_uri.scheme in ("file", ""):
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=online_store_writer_config,
            feature_view=feature_view,
            object_copy_request=ObjectCopyRequest(
                local_file_stage=LocalFileStage(location=stage_uri.path), timestamp_units=TimestampUnit.MICROS
            ),
        )
    elif stage_uri.scheme == "s3":
        key = stage_uri.path
        if key.startswith("/"):
            key = key[1:]
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=online_store_writer_config,
            feature_view=feature_view,
            object_copy_request=ObjectCopyRequest(
                s3_stage=S3Stage(
                    bucket=stage_uri.netloc,
                    key=key,
                ),
                timestamp_units=TimestampUnit.MICROS,
            ),
        )
    elif stage_uri.scheme == "gs":
        blob = stage_uri.path
        if blob.startswith("/"):
            blob = blob[1:]
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=online_store_writer_config,
            feature_view=feature_view,
            object_copy_request=ObjectCopyRequest(
                gcs_stage=GCSStage(
                    bucket=stage_uri.netloc,
                    blob=blob,
                ),
                timestamp_units=TimestampUnit.MICROS,
            ),
        )
    else:
        msg = f"Unexpected staging uri scheme: {stage_uri.scheme}"
        raise NotImplementedError(msg)
    run_online_store_copier(request)

    update_status_table(online_store_writer_config, feature_view, fd, feature_end_timestamp)


def update_status_table(
    online_store_writer_config: OnlineStoreWriterConfiguration,
    feature_view: FeatureView,
    fd: FeatureDefinitionWrapper,
    feature_end_timestamp: timestamp_pb2.Timestamp,
):
    # Issue status update
    if fd.is_temporal_aggregate and not fd.is_continuous:
        anchor_time = feature_end_timestamp.ToDatetime() - fd.aggregate_slide_interval.ToTimedelta()
        anchor_time_pb = timestamp_pb2.Timestamp()
        anchor_time_pb.FromDatetime(anchor_time)
        status_update = StatusUpdateRequest(anchor_time=anchor_time_pb)
    else:
        status_update = StatusUpdateRequest(materialized_raw_data_end_time=feature_end_timestamp)

    status_request = OnlineStoreCopierRequest(
        online_store_writer_configuration=online_store_writer_config,
        feature_view=feature_view,
        status_update_request=status_update,
    )
    run_online_store_copier(status_request)


def get_writer_for_fd(
    params: MaterializationTaskParams,
) -> OfflineStoreWriter:
    role = params.dynamodb_cross_account_role if params.HasField("dynamodb_cross_account_role") else None
    kms_key_arn = params.kms_key_arn if params.HasField("kms_key_arn") else None
    fd = feature_definition_from_task_params(params)
    if fd.has_delta_offline_store:
        return DeltaWriter(
            store_params=OfflineStoreParams.for_feature_definition(fd),
            table_uri=params.offline_store_path,
            join_keys=fd.join_keys,
            dynamodb_log_table_name=params.delta_log_table,
            dynamodb_log_table_region=params.dynamodb_table_region,
            dynamodb_cross_account_role=role,
            kms_key_arn=kms_key_arn,
            partition_type=partition_type_for_delta(fd.offline_store_params),
        )
    elif fd.has_iceberg_offline_store:
        return IcebergWriter(
            store_params=OfflineStoreParams.for_feature_definition(fd),
            table_uri=params.offline_store_path,
            join_keys=fd.join_keys,
        )
    else:
        offline_store_type = fd.offline_store_config.WhichOneof("store_type")
        msg = f"{offline_store_type} is not supported."
        raise ValueError(msg)


def get_delta_writer(
    params: MaterializationTaskParams,
    store_params: OfflineStoreParams,
    table_uri: str,
    join_keys: List[str],
    partition_type: PartitionType,
) -> DeltaWriter:
    role = params.dynamodb_cross_account_role if params.HasField("dynamodb_cross_account_role") else None
    kms_key_arn = params.kms_key_arn if params.HasField("kms_key_arn") else None

    return DeltaWriter(
        store_params=store_params,
        table_uri=table_uri,
        join_keys=join_keys,
        dynamodb_log_table_name=params.delta_log_table,
        dynamodb_log_table_region=params.dynamodb_table_region,
        dynamodb_cross_account_role=role,
        kms_key_arn=kms_key_arn,
        partition_type=partition_type,
    )


def get_secret_resolver(
    secret_service_params: SecretServiceParams,
) -> Optional[SecretResolver]:
    if not secret_service_params.secrets_api_service_url:
        return None

    assert secret_service_params.secret_access_api_key, "Secret access key is required when using secret service"
    return MDSSecretResolver(
        secret_service_params.secrets_api_service_url,
        secret_service_params.secret_access_api_key,
    )
