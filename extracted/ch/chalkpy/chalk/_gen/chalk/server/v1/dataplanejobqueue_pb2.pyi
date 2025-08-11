from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class JobQueueState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_QUEUE_STATE_UNSPECIFIED: _ClassVar[JobQueueState]
    JOB_QUEUE_STATE_SCHEDULED: _ClassVar[JobQueueState]
    JOB_QUEUE_STATE_RUNNING: _ClassVar[JobQueueState]
    JOB_QUEUE_STATE_COMPLETED: _ClassVar[JobQueueState]
    JOB_QUEUE_STATE_FAILED: _ClassVar[JobQueueState]
    JOB_QUEUE_STATE_CANCELED: _ClassVar[JobQueueState]
    JOB_QUEUE_STATE_NOT_READY: _ClassVar[JobQueueState]

class JobQueueKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOB_QUEUE_KIND_UNSPECIFIED: _ClassVar[JobQueueKind]
    JOB_QUEUE_KIND_ASYNC_OFFLINE_QUERY: _ClassVar[JobQueueKind]
    JOB_QUEUE_KIND_SCHEDULED_QUERY: _ClassVar[JobQueueKind]
    JOB_QUEUE_KIND_SCRIPT_TASK: _ClassVar[JobQueueKind]

JOB_QUEUE_STATE_UNSPECIFIED: JobQueueState
JOB_QUEUE_STATE_SCHEDULED: JobQueueState
JOB_QUEUE_STATE_RUNNING: JobQueueState
JOB_QUEUE_STATE_COMPLETED: JobQueueState
JOB_QUEUE_STATE_FAILED: JobQueueState
JOB_QUEUE_STATE_CANCELED: JobQueueState
JOB_QUEUE_STATE_NOT_READY: JobQueueState
JOB_QUEUE_KIND_UNSPECIFIED: JobQueueKind
JOB_QUEUE_KIND_ASYNC_OFFLINE_QUERY: JobQueueKind
JOB_QUEUE_KIND_SCHEDULED_QUERY: JobQueueKind
JOB_QUEUE_KIND_SCRIPT_TASK: JobQueueKind

class JobQueueItem(_message.Message):
    __slots__ = (
        "id",
        "created_at",
        "environment_id",
        "deployment_id",
        "job_name",
        "attempt_idx",
        "state",
        "scheduled_at",
        "kind",
        "job_args",
        "resource_group",
        "finalized_at",
        "last_attempted_at",
        "attempted_by",
        "last_heartbeat_at",
        "operation_id",
        "cancelation_requested_at",
        "max_attempts",
        "mainline_deployment_id",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_IDX_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_AT_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    JOB_ARGS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_ATTEMPTED_AT_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTED_BY_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARTBEAT_AT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    CANCELATION_REQUESTED_AT_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    MAINLINE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    created_at: _timestamp_pb2.Timestamp
    environment_id: str
    deployment_id: str
    job_name: str
    attempt_idx: int
    state: JobQueueState
    scheduled_at: _timestamp_pb2.Timestamp
    kind: JobQueueKind
    job_args: bytes
    resource_group: str
    finalized_at: _timestamp_pb2.Timestamp
    last_attempted_at: _timestamp_pb2.Timestamp
    attempted_by: _containers.RepeatedScalarFieldContainer[str]
    last_heartbeat_at: _timestamp_pb2.Timestamp
    operation_id: str
    cancelation_requested_at: _timestamp_pb2.Timestamp
    max_attempts: int
    mainline_deployment_id: str
    def __init__(
        self,
        id: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        job_name: _Optional[str] = ...,
        attempt_idx: _Optional[int] = ...,
        state: _Optional[_Union[JobQueueState, str]] = ...,
        scheduled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        kind: _Optional[_Union[JobQueueKind, str]] = ...,
        job_args: _Optional[bytes] = ...,
        resource_group: _Optional[str] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_attempted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        attempted_by: _Optional[_Iterable[str]] = ...,
        last_heartbeat_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        operation_id: _Optional[str] = ...,
        cancelation_requested_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_attempts: _Optional[int] = ...,
        mainline_deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetDataPlaneJobQueueRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetDataPlaneJobQueueResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: JobQueueItem
    def __init__(self, job: _Optional[_Union[JobQueueItem, _Mapping]] = ...) -> None: ...

class ListDataPlaneJobQueueRequest(_message.Message):
    __slots__ = ("environment_id", "deployment_id", "state", "kind", "limit", "offset", "operation_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    deployment_id: str
    state: JobQueueState
    kind: JobQueueKind
    limit: int
    offset: int
    operation_id: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        state: _Optional[_Union[JobQueueState, str]] = ...,
        kind: _Optional[_Union[JobQueueKind, str]] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        operation_id: _Optional[str] = ...,
    ) -> None: ...

class ListDataPlaneJobQueueResponse(_message.Message):
    __slots__ = ("jobs", "total")
    JOBS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[JobQueueItem]
    total: int
    def __init__(
        self, jobs: _Optional[_Iterable[_Union[JobQueueItem, _Mapping]]] = ..., total: _Optional[int] = ...
    ) -> None: ...
