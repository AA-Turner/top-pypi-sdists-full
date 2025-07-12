from tecton_proto.common import aws_credentials__client_pb2 as _aws_credentials__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import entity__client_pb2 as _entity__client_pb2
from tecton_proto.data import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.data import resource_provider__client_pb2 as _resource_provider__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.data import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from tecton_proto.dataobs import config__client_pb2 as _config__client_pb2
from tecton_proto.materialization import job_metadata__client_pb2 as _job_metadata__client_pb2
from tecton_proto.materialization import materialization_task__client_pb2 as _materialization_task__client_pb2
from tecton_proto.online_store_writer import config__client_pb2 as _config__client_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatchTaskInfo(_message.Message):
    __slots__ = ["batch_parameters", "dynamodb_json_output_path", "should_avoid_coalesce", "should_dedupe_online_store_writes"]
    BATCH_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_JSON_OUTPUT_PATH_FIELD_NUMBER: _ClassVar[int]
    SHOULD_AVOID_COALESCE_FIELD_NUMBER: _ClassVar[int]
    SHOULD_DEDUPE_ONLINE_STORE_WRITES_FIELD_NUMBER: _ClassVar[int]
    batch_parameters: _materialization_task__client_pb2.BatchMaterializationParameters
    dynamodb_json_output_path: str
    should_avoid_coalesce: bool
    should_dedupe_online_store_writes: bool
    def __init__(self, batch_parameters: _Optional[_Union[_materialization_task__client_pb2.BatchMaterializationParameters, _Mapping]] = ..., dynamodb_json_output_path: _Optional[str] = ..., should_dedupe_online_store_writes: bool = ..., should_avoid_coalesce: bool = ...) -> None: ...

class DatasetGenerationTaskInfo(_message.Message):
    __slots__ = ["dataset_generation_parameters"]
    DATASET_GENERATION_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    dataset_generation_parameters: _materialization_task__client_pb2.DatasetGenerationParameters
    def __init__(self, dataset_generation_parameters: _Optional[_Union[_materialization_task__client_pb2.DatasetGenerationParameters, _Mapping]] = ...) -> None: ...

class DeletionTaskInfo(_message.Message):
    __slots__ = ["deletion_parameters"]
    DELETION_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    deletion_parameters: _materialization_task__client_pb2.DeletionParameters
    def __init__(self, deletion_parameters: _Optional[_Union[_materialization_task__client_pb2.DeletionParameters, _Mapping]] = ...) -> None: ...

class DeltaMaintenanceTaskInfo(_message.Message):
    __slots__ = ["delta_maintenance_parameters"]
    DELTA_MAINTENANCE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    delta_maintenance_parameters: _materialization_task__client_pb2.DeltaMaintenanceParameters
    def __init__(self, delta_maintenance_parameters: _Optional[_Union[_materialization_task__client_pb2.DeltaMaintenanceParameters, _Mapping]] = ...) -> None: ...

class FeatureExportInfo(_message.Message):
    __slots__ = ["feature_export_parameters"]
    FEATURE_EXPORT_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    feature_export_parameters: _materialization_task__client_pb2.FeatureExportParameters
    def __init__(self, feature_export_parameters: _Optional[_Union[_materialization_task__client_pb2.FeatureExportParameters, _Mapping]] = ...) -> None: ...

class IcebergMaintenanceTaskInfo(_message.Message):
    __slots__ = ["iceberg_maintenance_parameters"]
    ICEBERG_MAINTENANCE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    iceberg_maintenance_parameters: _materialization_task__client_pb2.IcebergMaintenanceParameters
    def __init__(self, iceberg_maintenance_parameters: _Optional[_Union[_materialization_task__client_pb2.IcebergMaintenanceParameters, _Mapping]] = ...) -> None: ...

class IngestTaskInfo(_message.Message):
    __slots__ = ["ingest_parameters"]
    INGEST_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    ingest_parameters: _materialization_task__client_pb2.IngestMaterializationParameters
    def __init__(self, ingest_parameters: _Optional[_Union[_materialization_task__client_pb2.IngestMaterializationParameters, _Mapping]] = ...) -> None: ...

class MaterializationTaskParams(_message.Message):
    __slots__ = ["attempt_id", "batch_task_info", "canary_id", "data_observability_config", "dataset_generation_task_info", "dbfs_credentials_path", "deletion_task_info", "delta_log_table", "delta_maintenance_task_info", "dynamodb_cross_account_external_id", "dynamodb_cross_account_role", "dynamodb_cross_account_role_arn", "dynamodb_table_region", "entities", "feature_export_info", "feature_service", "feature_services", "feature_view", "feature_views", "iceberg_maintenance_task_info", "idempotence_key", "ingest_task_info", "job_metadata_table", "job_metadata_table_type", "kms_key_arn", "materialization_task_id", "offline_store_path", "online_store_writer_config", "plan_id", "resource_providers", "secret_access_api_key", "secrets_api_service_url", "spark_job_execution_table", "stream_task_info", "transformations", "use_new_consumption_metrics", "virtual_data_sources"]
    ATTEMPT_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_TASK_INFO_FIELD_NUMBER: _ClassVar[int]
    CANARY_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_GENERATION_TASK_INFO_FIELD_NUMBER: _ClassVar[int]
    DATA_OBSERVABILITY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DBFS_CREDENTIALS_PATH_FIELD_NUMBER: _ClassVar[int]
    DELETION_TASK_INFO_FIELD_NUMBER: _ClassVar[int]
    DELTA_LOG_TABLE_FIELD_NUMBER: _ClassVar[int]
    DELTA_MAINTENANCE_TASK_INFO_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_CROSS_ACCOUNT_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_CROSS_ACCOUNT_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_CROSS_ACCOUNT_ROLE_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_TABLE_REGION_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_EXPORT_INFO_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEWS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    ICEBERG_MAINTENANCE_TASK_INFO_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCE_KEY_FIELD_NUMBER: _ClassVar[int]
    INGEST_TASK_INFO_FIELD_NUMBER: _ClassVar[int]
    JOB_METADATA_TABLE_FIELD_NUMBER: _ClassVar[int]
    JOB_METADATA_TABLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    KMS_KEY_ARN_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_PATH_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_WRITER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    SECRETS_API_SERVICE_URL_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_API_KEY_FIELD_NUMBER: _ClassVar[int]
    SPARK_JOB_EXECUTION_TABLE_FIELD_NUMBER: _ClassVar[int]
    STREAM_TASK_INFO_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    USE_NEW_CONSUMPTION_METRICS_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    attempt_id: _id__client_pb2.Id
    batch_task_info: BatchTaskInfo
    canary_id: str
    data_observability_config: _config__client_pb2.DataObservabilityMaterializationConfig
    dataset_generation_task_info: DatasetGenerationTaskInfo
    dbfs_credentials_path: str
    deletion_task_info: DeletionTaskInfo
    delta_log_table: str
    delta_maintenance_task_info: DeltaMaintenanceTaskInfo
    dynamodb_cross_account_external_id: str
    dynamodb_cross_account_role: _aws_credentials__client_pb2.AwsIamRole
    dynamodb_cross_account_role_arn: str
    dynamodb_table_region: str
    entities: _containers.RepeatedCompositeFieldContainer[_entity__client_pb2.Entity]
    feature_export_info: FeatureExportInfo
    feature_service: _feature_service__client_pb2.FeatureService
    feature_services: _containers.RepeatedScalarFieldContainer[str]
    feature_view: _feature_view__client_pb2.FeatureView
    feature_views: _containers.RepeatedCompositeFieldContainer[_feature_view__client_pb2.FeatureView]
    iceberg_maintenance_task_info: IcebergMaintenanceTaskInfo
    idempotence_key: str
    ingest_task_info: IngestTaskInfo
    job_metadata_table: str
    job_metadata_table_type: _job_metadata__client_pb2.JobMetadataTableType
    kms_key_arn: str
    materialization_task_id: str
    offline_store_path: str
    online_store_writer_config: _config__client_pb2_1.OnlineStoreWriterConfiguration
    plan_id: _id__client_pb2.Id
    resource_providers: _containers.RepeatedCompositeFieldContainer[_resource_provider__client_pb2.ResourceProvider]
    secret_access_api_key: str
    secrets_api_service_url: str
    spark_job_execution_table: str
    stream_task_info: StreamTaskInfo
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2.Transformation]
    use_new_consumption_metrics: bool
    virtual_data_sources: _containers.RepeatedCompositeFieldContainer[_virtual_data_source__client_pb2.VirtualDataSource]
    def __init__(self, feature_view: _Optional[_Union[_feature_view__client_pb2.FeatureView, _Mapping]] = ..., virtual_data_sources: _Optional[_Iterable[_Union[_virtual_data_source__client_pb2.VirtualDataSource, _Mapping]]] = ..., transformations: _Optional[_Iterable[_Union[_transformation__client_pb2.Transformation, _Mapping]]] = ..., entities: _Optional[_Iterable[_Union[_entity__client_pb2.Entity, _Mapping]]] = ..., resource_providers: _Optional[_Iterable[_Union[_resource_provider__client_pb2.ResourceProvider, _Mapping]]] = ..., feature_services: _Optional[_Iterable[str]] = ..., feature_views: _Optional[_Iterable[_Union[_feature_view__client_pb2.FeatureView, _Mapping]]] = ..., feature_service: _Optional[_Union[_feature_service__client_pb2.FeatureService, _Mapping]] = ..., materialization_task_id: _Optional[str] = ..., idempotence_key: _Optional[str] = ..., attempt_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., spark_job_execution_table: _Optional[str] = ..., job_metadata_table: _Optional[str] = ..., delta_log_table: _Optional[str] = ..., job_metadata_table_type: _Optional[_Union[_job_metadata__client_pb2.JobMetadataTableType, str]] = ..., dynamodb_table_region: _Optional[str] = ..., online_store_writer_config: _Optional[_Union[_config__client_pb2_1.OnlineStoreWriterConfiguration, _Mapping]] = ..., dynamodb_cross_account_role: _Optional[_Union[_aws_credentials__client_pb2.AwsIamRole, _Mapping]] = ..., dynamodb_cross_account_role_arn: _Optional[str] = ..., dynamodb_cross_account_external_id: _Optional[str] = ..., dbfs_credentials_path: _Optional[str] = ..., offline_store_path: _Optional[str] = ..., use_new_consumption_metrics: bool = ..., canary_id: _Optional[str] = ..., data_observability_config: _Optional[_Union[_config__client_pb2.DataObservabilityMaterializationConfig, _Mapping]] = ..., batch_task_info: _Optional[_Union[BatchTaskInfo, _Mapping]] = ..., stream_task_info: _Optional[_Union[StreamTaskInfo, _Mapping]] = ..., ingest_task_info: _Optional[_Union[IngestTaskInfo, _Mapping]] = ..., deletion_task_info: _Optional[_Union[DeletionTaskInfo, _Mapping]] = ..., delta_maintenance_task_info: _Optional[_Union[DeltaMaintenanceTaskInfo, _Mapping]] = ..., feature_export_info: _Optional[_Union[FeatureExportInfo, _Mapping]] = ..., dataset_generation_task_info: _Optional[_Union[DatasetGenerationTaskInfo, _Mapping]] = ..., iceberg_maintenance_task_info: _Optional[_Union[IcebergMaintenanceTaskInfo, _Mapping]] = ..., secrets_api_service_url: _Optional[str] = ..., secret_access_api_key: _Optional[str] = ..., plan_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., kms_key_arn: _Optional[str] = ...) -> None: ...

class SecretMaterializationTaskParams(_message.Message):
    __slots__ = ["secret_service_params"]
    SECRET_SERVICE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    secret_service_params: SecretServiceParams
    def __init__(self, secret_service_params: _Optional[_Union[SecretServiceParams, _Mapping]] = ...) -> None: ...

class SecretServiceParams(_message.Message):
    __slots__ = ["secret_access_api_key", "secrets_api_service_url"]
    SECRETS_API_SERVICE_URL_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_API_KEY_FIELD_NUMBER: _ClassVar[int]
    secret_access_api_key: str
    secrets_api_service_url: str
    def __init__(self, secrets_api_service_url: _Optional[str] = ..., secret_access_api_key: _Optional[str] = ...) -> None: ...

class StreamTaskInfo(_message.Message):
    __slots__ = ["stream_parameters", "streaming_checkpoint_path", "streaming_trigger_interval_override", "streaming_trigger_realtime_mode"]
    STREAMING_CHECKPOINT_PATH_FIELD_NUMBER: _ClassVar[int]
    STREAMING_TRIGGER_INTERVAL_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    STREAMING_TRIGGER_REALTIME_MODE_FIELD_NUMBER: _ClassVar[int]
    STREAM_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    stream_parameters: _materialization_task__client_pb2.StreamMaterializationParameters
    streaming_checkpoint_path: str
    streaming_trigger_interval_override: str
    streaming_trigger_realtime_mode: bool
    def __init__(self, stream_parameters: _Optional[_Union[_materialization_task__client_pb2.StreamMaterializationParameters, _Mapping]] = ..., streaming_checkpoint_path: _Optional[str] = ..., streaming_trigger_interval_override: _Optional[str] = ..., streaming_trigger_realtime_mode: bool = ...) -> None: ...
