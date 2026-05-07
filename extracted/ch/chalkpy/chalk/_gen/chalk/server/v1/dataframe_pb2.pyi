from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.dataframe.v1 import dataframe_pb2 as _dataframe_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class DataFrameRunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_FRAME_RUN_STATUS_UNSPECIFIED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_QUEUED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_WORKING: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_COMPLETED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_FAILED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_CANCELED: _ClassVar[DataFrameRunStatus]
    DATA_FRAME_RUN_STATUS_STARTING: _ClassVar[DataFrameRunStatus]

class JobAttemptState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_ATTEMPT_STATE_UNSPECIFIED: _ClassVar[JobAttemptState]
    JOB_ATTEMPT_STATE_QUEUED: _ClassVar[JobAttemptState]
    JOB_ATTEMPT_STATE_RUNNING: _ClassVar[JobAttemptState]
    JOB_ATTEMPT_STATE_COMPLETED: _ClassVar[JobAttemptState]
    JOB_ATTEMPT_STATE_FAILED: _ClassVar[JobAttemptState]
    JOB_ATTEMPT_STATE_CANCELED: _ClassVar[JobAttemptState]

DATA_FRAME_RUN_STATUS_UNSPECIFIED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_QUEUED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_WORKING: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_COMPLETED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_FAILED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_CANCELED: DataFrameRunStatus
DATA_FRAME_RUN_STATUS_STARTING: DataFrameRunStatus
JOB_ATTEMPT_STATE_UNSPECIFIED: JobAttemptState
JOB_ATTEMPT_STATE_QUEUED: JobAttemptState
JOB_ATTEMPT_STATE_RUNNING: JobAttemptState
JOB_ATTEMPT_STATE_COMPLETED: JobAttemptState
JOB_ATTEMPT_STATE_FAILED: JobAttemptState
JOB_ATTEMPT_STATE_CANCELED: JobAttemptState

class ExecuteDataFramePlanRequest(_message.Message):
    __slots__ = ("plan", "compressed_plan_uri_prefix", "correlation_id", "resource_group")
    PLAN_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    plan: _dataframe_pb2.DataFramePlan
    compressed_plan_uri_prefix: str
    correlation_id: str
    resource_group: str
    def __init__(
        self,
        plan: _Optional[_Union[_dataframe_pb2.DataFramePlan, _Mapping]] = ...,
        compressed_plan_uri_prefix: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
    ) -> None: ...

class ExecuteDataFramePlanResponse(_message.Message):
    __slots__ = ("operation_id", "run", "errors")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    run: DataFrameRun
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        run: _Optional[_Union[DataFrameRun, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetDataFramePlanUploadUrlRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDataFramePlanUploadUrlResponse(_message.Message):
    __slots__ = ("upload_url", "compressed_plan_uri_prefix")
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    upload_url: str
    compressed_plan_uri_prefix: str
    def __init__(self, upload_url: _Optional[str] = ..., compressed_plan_uri_prefix: _Optional[str] = ...) -> None: ...

class GetDataFrameRunRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class GetDataFrameRunStatusRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class GetDataFrameRunStatusResponse(_message.Message):
    __slots__ = ("status", "output_uri_prefix", "finalized_at")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    status: DataFrameRunStatus
    output_uri_prefix: str
    finalized_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        status: _Optional[_Union[DataFrameRunStatus, str]] = ...,
        output_uri_prefix: _Optional[str] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class DataFrameRunAttempt(_message.Message):
    __slots__ = ("attempt_idx", "worker_pod_name", "queued_at", "started_at", "finished_at", "state", "error_message")
    ATTEMPT_IDX_FIELD_NUMBER: _ClassVar[int]
    WORKER_POD_NAME_FIELD_NUMBER: _ClassVar[int]
    QUEUED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    attempt_idx: int
    worker_pod_name: str
    queued_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    state: JobAttemptState
    error_message: str
    def __init__(
        self,
        attempt_idx: _Optional[int] = ...,
        worker_pod_name: _Optional[str] = ...,
        queued_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        state: _Optional[_Union[JobAttemptState, str]] = ...,
        error_message: _Optional[str] = ...,
    ) -> None: ...

class DataFrameRunShard(_message.Message):
    __slots__ = (
        "operation_id",
        "shard_id",
        "status",
        "finalized_at",
        "updated_at",
        "compressed_plan_uri_prefix",
        "attempts",
        "max_attempts",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    shard_id: int
    status: DataFrameRunStatus
    finalized_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    compressed_plan_uri_prefix: str
    attempts: _containers.RepeatedCompositeFieldContainer[DataFrameRunAttempt]
    max_attempts: int
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        shard_id: _Optional[int] = ...,
        status: _Optional[_Union[DataFrameRunStatus, str]] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        compressed_plan_uri_prefix: _Optional[str] = ...,
        attempts: _Optional[_Iterable[_Union[DataFrameRunAttempt, _Mapping]]] = ...,
        max_attempts: _Optional[int] = ...,
    ) -> None: ...

class DataFrameRun(_message.Message):
    __slots__ = (
        "operation_id",
        "status",
        "output_uri_prefix",
        "agent_id",
        "finalized_at",
        "updated_at",
        "correlation_id",
        "external_id",
        "branch_name",
        "resource_group",
        "meta_data",
        "compressed_plan_uri_prefix",
        "created_at",
        "deployment_id",
        "error_message",
        "worker_pod_name",
        "started_at",
        "shards",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_PLAN_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WORKER_POD_NAME_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    SHARDS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    status: DataFrameRunStatus
    output_uri_prefix: str
    agent_id: str
    finalized_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    correlation_id: str
    external_id: str
    branch_name: str
    resource_group: str
    meta_data: _struct_pb2.Struct
    compressed_plan_uri_prefix: str
    created_at: _timestamp_pb2.Timestamp
    deployment_id: str
    error_message: str
    worker_pod_name: str
    started_at: _timestamp_pb2.Timestamp
    shards: _containers.RepeatedCompositeFieldContainer[DataFrameRunShard]
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        status: _Optional[_Union[DataFrameRunStatus, str]] = ...,
        output_uri_prefix: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        correlation_id: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        meta_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        compressed_plan_uri_prefix: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        deployment_id: _Optional[str] = ...,
        error_message: _Optional[str] = ...,
        worker_pod_name: _Optional[str] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        shards: _Optional[_Iterable[_Union[DataFrameRunShard, _Mapping]]] = ...,
    ) -> None: ...

class GetDataFrameRunDownloadUrlsRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class DataFrameRunDownloadUrl(_message.Message):
    __slots__ = ("filename", "download_url")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    filename: str
    download_url: str
    def __init__(self, filename: _Optional[str] = ..., download_url: _Optional[str] = ...) -> None: ...

class GetDataFrameRunDownloadUrlsResponse(_message.Message):
    __slots__ = ("download_urls",)
    DOWNLOAD_URLS_FIELD_NUMBER: _ClassVar[int]
    download_urls: _containers.RepeatedCompositeFieldContainer[DataFrameRunDownloadUrl]
    def __init__(
        self, download_urls: _Optional[_Iterable[_Union[DataFrameRunDownloadUrl, _Mapping]]] = ...
    ) -> None: ...

class ListDataFrameRunsRequest(_message.Message):
    __slots__ = (
        "limit",
        "cursor",
        "agent_id",
        "deployment_id",
        "status",
        "branch_name",
        "external_id",
        "correlation_id",
        "start",
        "end",
    )
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    agent_id: str
    deployment_id: str
    status: int
    branch_name: str
    external_id: str
    correlation_id: str
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    def __init__(
        self,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        status: _Optional[int] = ...,
        branch_name: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListDataFrameRunsResponse(_message.Message):
    __slots__ = ("runs", "next_cursor")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[DataFrameRun]
    next_cursor: str
    def __init__(
        self, runs: _Optional[_Iterable[_Union[DataFrameRun, _Mapping]]] = ..., next_cursor: _Optional[str] = ...
    ) -> None: ...

class GetDataFrameRunResponse(_message.Message):
    __slots__ = ("run", "errors")
    RUN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    run: DataFrameRun
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        run: _Optional[_Union[DataFrameRun, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...
