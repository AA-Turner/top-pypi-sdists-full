from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.common import compute_identity__client_pb2 as _compute_identity__client_pb2
from tecton_proto.common import compute_mode__client_pb2 as _compute_mode__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.materialization import spark_cluster__client_pb2 as _spark_cluster__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
TEST_ONLY_MATERIALIZATION_JOB_TYPE_BATCH: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_DATASET_GENERATION: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_ICEBERG_MAINTENANCE: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_INGEST: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_MAINTENANCE: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_STREAM: TestOnlyMaterializationJobType
TEST_ONLY_MATERIALIZATION_JOB_TYPE_UNSPECIFIED: TestOnlyMaterializationJobType

class CancelDatasetJobRequest(_message.Message):
    __slots__ = ["job_id", "saved_feature_data_frame", "workspace"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    SAVED_FEATURE_DATA_FRAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    saved_feature_data_frame: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., saved_feature_data_frame: _Optional[str] = ..., job_id: _Optional[str] = ...) -> None: ...

class CancelDatasetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: _Optional[_Union[MaterializationJob, _Mapping]] = ...) -> None: ...

class CancelJobRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "job_id", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_service: str
    feature_view: str
    job_id: str
    workspace: str
    def __init__(self, job_id: _Optional[str] = ..., workspace: _Optional[str] = ..., feature_view: _Optional[str] = ..., feature_service: _Optional[str] = ...) -> None: ...

class CancelJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: _Optional[_Union[MaterializationJob, _Mapping]] = ...) -> None: ...

class CompleteDataframeUploadRequest(_message.Message):
    __slots__ = ["key", "part_etags", "upload_id", "workspace"]
    class PartEtagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    KEY_FIELD_NUMBER: _ClassVar[int]
    PART_ETAGS_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    key: str
    part_etags: _containers.ScalarMap[int, str]
    upload_id: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., key: _Optional[str] = ..., upload_id: _Optional[str] = ..., part_etags: _Optional[_Mapping[int, str]] = ...) -> None: ...

class CompleteDataframeUploadResponse(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class GetDataframeInfoRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "task_type", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_service: str
    feature_view: str
    task_type: _spark_cluster__client_pb2.TaskType
    workspace: str
    def __init__(self, feature_view: _Optional[str] = ..., feature_service: _Optional[str] = ..., workspace: _Optional[str] = ..., task_type: _Optional[_Union[_spark_cluster__client_pb2.TaskType, str]] = ...) -> None: ...

class GetDataframeInfoResponse(_message.Message):
    __slots__ = ["df_path", "signed_url_for_df_upload"]
    DF_PATH_FIELD_NUMBER: _ClassVar[int]
    SIGNED_URL_FOR_DF_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    df_path: str
    signed_url_for_df_upload: str
    def __init__(self, df_path: _Optional[str] = ..., signed_url_for_df_upload: _Optional[str] = ...) -> None: ...

class GetDataframeUploadUrlRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "task_type", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_service: str
    feature_view: str
    task_type: _spark_cluster__client_pb2.TaskType
    workspace: str
    def __init__(self, feature_view: _Optional[str] = ..., feature_service: _Optional[str] = ..., workspace: _Optional[str] = ..., task_type: _Optional[_Union[_spark_cluster__client_pb2.TaskType, str]] = ...) -> None: ...

class GetDataframeUploadUrlResponse(_message.Message):
    __slots__ = ["key", "upload_id"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    key: str
    upload_id: str
    def __init__(self, key: _Optional[str] = ..., upload_id: _Optional[str] = ...) -> None: ...

class GetDatasetJobRequest(_message.Message):
    __slots__ = ["job_id", "saved_feature_data_frame", "workspace"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    SAVED_FEATURE_DATA_FRAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    saved_feature_data_frame: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., saved_feature_data_frame: _Optional[str] = ..., job_id: _Optional[str] = ...) -> None: ...

class GetDatasetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: _Optional[_Union[MaterializationJob, _Mapping]] = ...) -> None: ...

class GetJobRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "job_id", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_service: str
    feature_view: str
    job_id: str
    workspace: str
    def __init__(self, job_id: _Optional[str] = ..., workspace: _Optional[str] = ..., feature_view: _Optional[str] = ..., feature_service: _Optional[str] = ...) -> None: ...

class GetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: _Optional[_Union[MaterializationJob, _Mapping]] = ...) -> None: ...

class GetLatestReadyTimeRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_service: str
    feature_view: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., feature_view: _Optional[str] = ..., feature_service: _Optional[str] = ...) -> None: ...

class GetLatestReadyTimeResponse(_message.Message):
    __slots__ = ["offline_latest_ready_time", "online_latest_ready_time"]
    OFFLINE_LATEST_READY_TIME_FIELD_NUMBER: _ClassVar[int]
    ONLINE_LATEST_READY_TIME_FIELD_NUMBER: _ClassVar[int]
    offline_latest_ready_time: _timestamp_pb2.Timestamp
    online_latest_ready_time: _timestamp_pb2.Timestamp
    def __init__(self, online_latest_ready_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., offline_latest_ready_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IngestDataframeFromS3Request(_message.Message):
    __slots__ = ["df_path", "feature_view", "use_tecton_managed_retries", "workspace"]
    DF_PATH_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    USE_TECTON_MANAGED_RETRIES_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    df_path: str
    feature_view: str
    use_tecton_managed_retries: bool
    workspace: str
    def __init__(self, feature_view: _Optional[str] = ..., df_path: _Optional[str] = ..., workspace: _Optional[str] = ..., use_tecton_managed_retries: bool = ...) -> None: ...

class IngestDataframeFromS3Response(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: _Optional[_Union[MaterializationJob, _Mapping]] = ...) -> None: ...

class JobAttempt(_message.Message):
    __slots__ = ["compute_identity", "created_at", "id", "run_url", "state", "updated_at"]
    COMPUTE_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RUN_URL_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    compute_identity: _compute_identity__client_pb2.ComputeIdentity
    created_at: _timestamp_pb2.Timestamp
    id: str
    run_url: str
    state: str
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[str] = ..., run_url: _Optional[str] = ..., compute_identity: _Optional[_Union[_compute_identity__client_pb2.ComputeIdentity, _Mapping]] = ...) -> None: ...

class ListJobsRequest(_message.Message):
    __slots__ = ["feature_service", "feature_view", "workspace"]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_service: str
    feature_view: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., feature_view: _Optional[str] = ..., feature_service: _Optional[str] = ...) -> None: ...

class ListJobsResponse(_message.Message):
    __slots__ = ["jobs"]
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[MaterializationJob]
    def __init__(self, jobs: _Optional[_Iterable[_Union[MaterializationJob, _Mapping]]] = ...) -> None: ...

class MaterializationJob(_message.Message):
    __slots__ = ["attempts", "created_at", "end_time", "feature_service", "feature_view", "id", "ingest_path", "job_type", "next_attempt_at", "offline", "online", "saved_feature_data_frame", "start_time", "state", "updated_at", "workspace"]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INGEST_PATH_FIELD_NUMBER: _ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: _ClassVar[int]
    NEXT_ATTEMPT_AT_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    SAVED_FEATURE_DATA_FRAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    attempts: _containers.RepeatedCompositeFieldContainer[JobAttempt]
    created_at: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    feature_service: str
    feature_view: str
    id: str
    ingest_path: str
    job_type: str
    next_attempt_at: _timestamp_pb2.Timestamp
    offline: bool
    online: bool
    saved_feature_data_frame: str
    start_time: _timestamp_pb2.Timestamp
    state: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, id: _Optional[str] = ..., workspace: _Optional[str] = ..., feature_view: _Optional[str] = ..., feature_service: _Optional[str] = ..., saved_feature_data_frame: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[str] = ..., attempts: _Optional[_Iterable[_Union[JobAttempt, _Mapping]]] = ..., next_attempt_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., online: bool = ..., offline: bool = ..., job_type: _Optional[str] = ..., ingest_path: _Optional[str] = ...) -> None: ...

class MaterializationJobRequest(_message.Message):
    __slots__ = ["end_time", "feature_view", "offline", "online", "overwrite", "start_time", "use_tecton_managed_retries", "workspace"]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    USE_TECTON_MANAGED_RETRIES_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    end_time: _timestamp_pb2.Timestamp
    feature_view: str
    offline: bool
    online: bool
    overwrite: bool
    start_time: _timestamp_pb2.Timestamp
    use_tecton_managed_retries: bool
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., feature_view: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., online: bool = ..., offline: bool = ..., use_tecton_managed_retries: bool = ..., overwrite: bool = ...) -> None: ...

class MaterializationJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: _Optional[_Union[MaterializationJob, _Mapping]] = ...) -> None: ...

class StartDatasetJobRequest(_message.Message):
    __slots__ = ["cluster_config", "compute_mode", "dataset_name", "datetime_range", "environment", "expected_schema", "extra_config", "feature_service_id", "feature_view_id", "from_source", "job_retry_times", "spine", "tecton_runtime", "workspace"]
    class DateTimeRangeInput(_message.Message):
        __slots__ = ["end", "entities_path", "max_lookback", "start"]
        END_FIELD_NUMBER: _ClassVar[int]
        ENTITIES_PATH_FIELD_NUMBER: _ClassVar[int]
        MAX_LOOKBACK_FIELD_NUMBER: _ClassVar[int]
        START_FIELD_NUMBER: _ClassVar[int]
        end: _timestamp_pb2.Timestamp
        entities_path: str
        max_lookback: _timestamp_pb2.Timestamp
        start: _timestamp_pb2.Timestamp
        def __init__(self, start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_lookback: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., entities_path: _Optional[str] = ...) -> None: ...
    class ExtraConfigEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SpineInput(_message.Message):
        __slots__ = ["column_names", "path", "timestamp_key"]
        COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_KEY_FIELD_NUMBER: _ClassVar[int]
        column_names: _containers.RepeatedScalarFieldContainer[str]
        path: str
        timestamp_key: str
        def __init__(self, path: _Optional[str] = ..., timestamp_key: _Optional[str] = ..., column_names: _Optional[_Iterable[str]] = ...) -> None: ...
    CLUSTER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_MODE_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    DATETIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    EXTRA_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_SOURCE_FIELD_NUMBER: _ClassVar[int]
    JOB_RETRY_TIMES_FIELD_NUMBER: _ClassVar[int]
    SPINE_FIELD_NUMBER: _ClassVar[int]
    TECTON_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    cluster_config: _feature_view__client_pb2.ClusterConfig
    compute_mode: _compute_mode__client_pb2.BatchComputeMode
    dataset_name: str
    datetime_range: StartDatasetJobRequest.DateTimeRangeInput
    environment: str
    expected_schema: _schema__client_pb2.Schema
    extra_config: _containers.ScalarMap[str, str]
    feature_service_id: _id__client_pb2.Id
    feature_view_id: _id__client_pb2.Id
    from_source: bool
    job_retry_times: int
    spine: StartDatasetJobRequest.SpineInput
    tecton_runtime: str
    workspace: str
    def __init__(self, compute_mode: _Optional[_Union[_compute_mode__client_pb2.BatchComputeMode, str]] = ..., from_source: bool = ..., workspace: _Optional[str] = ..., feature_service_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., spine: _Optional[_Union[StartDatasetJobRequest.SpineInput, _Mapping]] = ..., datetime_range: _Optional[_Union[StartDatasetJobRequest.DateTimeRangeInput, _Mapping]] = ..., dataset_name: _Optional[str] = ..., cluster_config: _Optional[_Union[_feature_view__client_pb2.ClusterConfig, _Mapping]] = ..., tecton_runtime: _Optional[str] = ..., environment: _Optional[str] = ..., extra_config: _Optional[_Mapping[str, str]] = ..., expected_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., job_retry_times: _Optional[int] = ...) -> None: ...

class StartDatasetJobResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: MaterializationJob
    def __init__(self, job: _Optional[_Union[MaterializationJob, _Mapping]] = ...) -> None: ...

class TestOnlyCompleteOnlineTableRequest(_message.Message):
    __slots__ = ["feature_view_name", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_view_name: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., feature_view_name: _Optional[str] = ...) -> None: ...

class TestOnlyCompleteOnlineTableResponse(_message.Message):
    __slots__ = ["table_name"]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    def __init__(self, table_name: _Optional[str] = ...) -> None: ...

class TestOnlyGetDatasetGenerationTaskParamsRequest(_message.Message):
    __slots__ = ["start_dataset_job_request"]
    START_DATASET_JOB_REQUEST_FIELD_NUMBER: _ClassVar[int]
    start_dataset_job_request: StartDatasetJobRequest
    def __init__(self, start_dataset_job_request: _Optional[_Union[StartDatasetJobRequest, _Mapping]] = ...) -> None: ...

class TestOnlyGetMaterializationTaskParamsRequest(_message.Message):
    __slots__ = ["df_path", "disable_offline", "disable_online", "feature_view_name", "job_end_time", "job_start_time", "job_type", "workspace"]
    DF_PATH_FIELD_NUMBER: _ClassVar[int]
    DISABLE_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_ONLINE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    JOB_END_TIME_FIELD_NUMBER: _ClassVar[int]
    JOB_START_TIME_FIELD_NUMBER: _ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    df_path: str
    disable_offline: bool
    disable_online: bool
    feature_view_name: str
    job_end_time: _timestamp_pb2.Timestamp
    job_start_time: _timestamp_pb2.Timestamp
    job_type: TestOnlyMaterializationJobType
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., feature_view_name: _Optional[str] = ..., job_type: _Optional[_Union[TestOnlyMaterializationJobType, str]] = ..., disable_offline: bool = ..., disable_online: bool = ..., job_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., job_end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., df_path: _Optional[str] = ...) -> None: ...

class TestOnlyGetMaterializationTaskParamsResponse(_message.Message):
    __slots__ = ["encoded_materialization_params"]
    ENCODED_MATERIALIZATION_PARAMS_FIELD_NUMBER: _ClassVar[int]
    encoded_materialization_params: str
    def __init__(self, encoded_materialization_params: _Optional[str] = ...) -> None: ...

class TestOnlyOnlineTableNameRequest(_message.Message):
    __slots__ = ["feature_view_name", "watermark", "workspace"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_view_name: str
    watermark: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., feature_view_name: _Optional[str] = ..., watermark: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TestOnlyOnlineTableNameResponse(_message.Message):
    __slots__ = ["table_name"]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    def __init__(self, table_name: _Optional[str] = ...) -> None: ...

class TestOnlyWriteFeatureServerConfigRequest(_message.Message):
    __slots__ = ["absolute_filepath", "transform_server_filepath", "workspace"]
    ABSOLUTE_FILEPATH_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SERVER_FILEPATH_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    absolute_filepath: str
    transform_server_filepath: str
    workspace: str
    def __init__(self, absolute_filepath: _Optional[str] = ..., transform_server_filepath: _Optional[str] = ..., workspace: _Optional[str] = ...) -> None: ...

class TestOnlyWriteFeatureServerConfigResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UploadDataframePartRequest(_message.Message):
    __slots__ = ["key", "parent_upload_id", "part_number", "workspace"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    PARENT_UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    key: str
    parent_upload_id: str
    part_number: int
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., key: _Optional[str] = ..., parent_upload_id: _Optional[str] = ..., part_number: _Optional[int] = ...) -> None: ...

class UploadDataframePartResponse(_message.Message):
    __slots__ = ["upload_url"]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    upload_url: str
    def __init__(self, upload_url: _Optional[str] = ...) -> None: ...

class TestOnlyMaterializationJobType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
