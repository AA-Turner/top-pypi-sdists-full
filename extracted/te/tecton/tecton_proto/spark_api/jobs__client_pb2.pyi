from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import compute_identity__client_pb2 as _compute_identity__client_pb2
from tecton_proto.spark_common import clusters__client_pb2 as _clusters__client_pb2
from tecton_proto.spark_common import libraries__client_pb2 as _libraries__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
INSTANCE_ALLOCATION_FAILURE: RunTerminationReason
JOB_FINISHED: RunTerminationReason
MANUAL_CANCELATION: RunTerminationReason
NON_CLOUD_FAILURE: RunTerminationReason
RUN_STATUS_CANCELED: RunStatus
RUN_STATUS_ERROR: RunStatus
RUN_STATUS_PENDING: RunStatus
RUN_STATUS_RUNNING: RunStatus
RUN_STATUS_SUBMISSION_ERROR: RunStatus
RUN_STATUS_SUCCESS: RunStatus
RUN_STATUS_TERMINATING: RunStatus
RUN_STATUS_UNKNOWN: RunStatus
SUBMISSION_ERROR: RunTerminationReason
UNKNOWN_TERMINATION_REASON: RunTerminationReason

class GetJobRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    def __init__(self, run_id: _Optional[str] = ...) -> None: ...

class GetJobResponse(_message.Message):
    __slots__ = ["additional_metadata", "details", "job_id", "run_id", "run_page_url", "spark_cluster_id"]
    class AdditionalMetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ADDITIONAL_METADATA_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_PAGE_URL_FIELD_NUMBER: _ClassVar[int]
    SPARK_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    additional_metadata: _containers.ScalarMap[str, str]
    details: RunDetails
    job_id: str
    run_id: str
    run_page_url: str
    spark_cluster_id: str
    def __init__(self, run_id: _Optional[str] = ..., job_id: _Optional[str] = ..., run_page_url: _Optional[str] = ..., spark_cluster_id: _Optional[str] = ..., details: _Optional[_Union[RunDetails, _Mapping]] = ..., additional_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ListJobRequest(_message.Message):
    __slots__ = ["marker", "offset"]
    MARKER_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    marker: str
    offset: int
    def __init__(self, offset: _Optional[int] = ..., marker: _Optional[str] = ...) -> None: ...

class ListJobResponse(_message.Message):
    __slots__ = ["has_more", "marker", "runs"]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    MARKER_FIELD_NUMBER: _ClassVar[int]
    RUNS_FIELD_NUMBER: _ClassVar[int]
    has_more: bool
    marker: str
    runs: _containers.RepeatedCompositeFieldContainer[RunSummary]
    def __init__(self, runs: _Optional[_Iterable[_Union[RunSummary, _Mapping]]] = ..., has_more: bool = ..., marker: _Optional[str] = ...) -> None: ...

class PythonMaterializationTask(_message.Message):
    __slots__ = ["base_parameters", "materialization_path_uri", "taskType"]
    class TaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class BaseParametersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BASE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    BATCH: PythonMaterializationTask.TaskType
    DATASET_GENERATION: PythonMaterializationTask.TaskType
    DELETION: PythonMaterializationTask.TaskType
    DELTA_MAINTENANCE: PythonMaterializationTask.TaskType
    FEATURE_EXPORT: PythonMaterializationTask.TaskType
    ICEBERG_MAINTENANCE: PythonMaterializationTask.TaskType
    INGEST: PythonMaterializationTask.TaskType
    MATERIALIZATION_PATH_URI_FIELD_NUMBER: _ClassVar[int]
    PLAN_INTEGRATION_TEST_BATCH: PythonMaterializationTask.TaskType
    PLAN_INTEGRATION_TEST_STREAM: PythonMaterializationTask.TaskType
    STREAMING: PythonMaterializationTask.TaskType
    TASKTYPE_FIELD_NUMBER: _ClassVar[int]
    base_parameters: _containers.ScalarMap[str, str]
    materialization_path_uri: str
    taskType: PythonMaterializationTask.TaskType
    def __init__(self, materialization_path_uri: _Optional[str] = ..., base_parameters: _Optional[_Mapping[str, str]] = ..., taskType: _Optional[_Union[PythonMaterializationTask.TaskType, str]] = ...) -> None: ...

class RunDetails(_message.Message):
    __slots__ = ["end_time", "run_status", "start_time", "state_message", "termination_reason", "vendor_termination_reason"]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    RUN_STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TERMINATION_REASON_FIELD_NUMBER: _ClassVar[int]
    VENDOR_TERMINATION_REASON_FIELD_NUMBER: _ClassVar[int]
    end_time: _timestamp_pb2.Timestamp
    run_status: RunStatus
    start_time: _timestamp_pb2.Timestamp
    state_message: str
    termination_reason: RunTerminationReason
    vendor_termination_reason: str
    def __init__(self, run_status: _Optional[_Union[RunStatus, str]] = ..., termination_reason: _Optional[_Union[RunTerminationReason, str]] = ..., state_message: _Optional[str] = ..., vendor_termination_reason: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RunSummary(_message.Message):
    __slots__ = ["additional_metadata", "resource_locator", "run_id", "run_state"]
    class AdditionalMetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ADDITIONAL_METADATA_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    additional_metadata: _containers.ScalarMap[str, str]
    resource_locator: str
    run_id: str
    run_state: str
    def __init__(self, run_id: _Optional[str] = ..., run_state: _Optional[str] = ..., resource_locator: _Optional[str] = ..., additional_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class StartJobRequest(_message.Message):
    __slots__ = ["compute_identity", "databricks_jobs_api_version", "existing_cluster", "is_notebook", "libraries", "materialization_task", "new_cluster", "run_name", "timeout_seconds", "use_stepped_materialization"]
    COMPUTE_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    DATABRICKS_JOBS_API_VERSION_FIELD_NUMBER: _ClassVar[int]
    EXISTING_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    IS_NOTEBOOK_FIELD_NUMBER: _ClassVar[int]
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_TASK_FIELD_NUMBER: _ClassVar[int]
    NEW_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    RUN_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    USE_STEPPED_MATERIALIZATION_FIELD_NUMBER: _ClassVar[int]
    compute_identity: _compute_identity__client_pb2.ComputeIdentity
    databricks_jobs_api_version: str
    existing_cluster: _clusters__client_pb2.ExistingCluster
    is_notebook: bool
    libraries: _containers.RepeatedCompositeFieldContainer[_libraries__client_pb2.Library]
    materialization_task: PythonMaterializationTask
    new_cluster: _clusters__client_pb2.NewCluster
    run_name: str
    timeout_seconds: int
    use_stepped_materialization: bool
    def __init__(self, new_cluster: _Optional[_Union[_clusters__client_pb2.NewCluster, _Mapping]] = ..., existing_cluster: _Optional[_Union[_clusters__client_pb2.ExistingCluster, _Mapping]] = ..., materialization_task: _Optional[_Union[PythonMaterializationTask, _Mapping]] = ..., run_name: _Optional[str] = ..., libraries: _Optional[_Iterable[_Union[_libraries__client_pb2.Library, _Mapping]]] = ..., timeout_seconds: _Optional[int] = ..., is_notebook: bool = ..., use_stepped_materialization: bool = ..., databricks_jobs_api_version: _Optional[str] = ..., compute_identity: _Optional[_Union[_compute_identity__client_pb2.ComputeIdentity, _Mapping]] = ...) -> None: ...

class StartJobResponse(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    def __init__(self, run_id: _Optional[str] = ...) -> None: ...

class StopJobRequest(_message.Message):
    __slots__ = ["run_id"]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    def __init__(self, run_id: _Optional[str] = ...) -> None: ...

class RunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RunTerminationReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
