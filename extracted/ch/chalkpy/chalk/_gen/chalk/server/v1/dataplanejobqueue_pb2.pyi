from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.kubernetes.v1 import resourcequota_pb2 as _resourcequota_pb2
from chalk._gen.chalk.kubernetes.v1 import scaledobject_pb2 as _scaledobject_pb2
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
    JOB_QUEUE_STATE_WAITING: _ClassVar[JobQueueState]

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
JOB_QUEUE_STATE_WAITING: JobQueueState
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
        "shard_id",
        "job_index",
        "fetch_priority",
        "workflow_execution_id",
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
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_INDEX_FIELD_NUMBER: _ClassVar[int]
    FETCH_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
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
    shard_id: int
    job_index: int
    fetch_priority: int
    workflow_execution_id: str
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
        shard_id: _Optional[int] = ...,
        job_index: _Optional[int] = ...,
        fetch_priority: _Optional[int] = ...,
        workflow_execution_id: _Optional[str] = ...,
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

class GetJobQueueAuxiliaryResourcesRequest(_message.Message):
    __slots__ = ("environment_id", "resource_group")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    resource_group: str
    def __init__(self, environment_id: _Optional[str] = ..., resource_group: _Optional[str] = ...) -> None: ...

class GetJobQueueAuxiliaryResourcesResponse(_message.Message):
    __slots__ = ("deployment_scaled_objects", "resource_quota")
    class DeploymentScaledObjectsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _scaledobject_pb2.KubernetesScaledObjectData
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[_scaledobject_pb2.KubernetesScaledObjectData, _Mapping]] = ...,
        ) -> None: ...

    DEPLOYMENT_SCALED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_QUOTA_FIELD_NUMBER: _ClassVar[int]
    deployment_scaled_objects: _containers.MessageMap[str, _scaledobject_pb2.KubernetesScaledObjectData]
    resource_quota: _resourcequota_pb2.KubernetesResourceQuotaData
    def __init__(
        self,
        deployment_scaled_objects: _Optional[_Mapping[str, _scaledobject_pb2.KubernetesScaledObjectData]] = ...,
        resource_quota: _Optional[_Union[_resourcequota_pb2.KubernetesResourceQuotaData, _Mapping]] = ...,
    ) -> None: ...

class JobQueueRowSummary(_message.Message):
    __slots__ = (
        "id",
        "created_at",
        "attempt_idx",
        "state",
        "finalized_at",
        "last_attempted_at",
        "attempter_idxs",
        "last_heartbeat_at",
        "max_attempts",
        "job_idx",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_IDX_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_ATTEMPTED_AT_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTER_IDXS_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARTBEAT_AT_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    JOB_IDX_FIELD_NUMBER: _ClassVar[int]
    id: int
    created_at: _timestamp_pb2.Timestamp
    attempt_idx: int
    state: JobQueueState
    finalized_at: _timestamp_pb2.Timestamp
    last_attempted_at: _timestamp_pb2.Timestamp
    attempter_idxs: _containers.RepeatedScalarFieldContainer[int]
    last_heartbeat_at: _timestamp_pb2.Timestamp
    max_attempts: int
    job_idx: int
    def __init__(
        self,
        id: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        attempt_idx: _Optional[int] = ...,
        state: _Optional[_Union[JobQueueState, str]] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_attempted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        attempter_idxs: _Optional[_Iterable[int]] = ...,
        last_heartbeat_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_attempts: _Optional[int] = ...,
        job_idx: _Optional[int] = ...,
    ) -> None: ...

class JobQueueOperationSummary(_message.Message):
    __slots__ = (
        "indexed_row_summaries",
        "resource_group_name",
        "mainline_deployment_id",
        "kind",
        "attempters",
        "workflow_execution_id",
        "unsatisfied_dependency_operation_ids",
    )
    class IndexedRowSummariesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: JobQueueRowSummary
        def __init__(
            self, key: _Optional[int] = ..., value: _Optional[_Union[JobQueueRowSummary, _Mapping]] = ...
        ) -> None: ...

    INDEXED_ROW_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    MAINLINE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTERS_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    UNSATISFIED_DEPENDENCY_OPERATION_IDS_FIELD_NUMBER: _ClassVar[int]
    indexed_row_summaries: _containers.MessageMap[int, JobQueueRowSummary]
    resource_group_name: str
    mainline_deployment_id: str
    kind: JobQueueKind
    attempters: _containers.RepeatedScalarFieldContainer[str]
    workflow_execution_id: str
    unsatisfied_dependency_operation_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        indexed_row_summaries: _Optional[_Mapping[int, JobQueueRowSummary]] = ...,
        resource_group_name: _Optional[str] = ...,
        mainline_deployment_id: _Optional[str] = ...,
        kind: _Optional[_Union[JobQueueKind, str]] = ...,
        attempters: _Optional[_Iterable[str]] = ...,
        workflow_execution_id: _Optional[str] = ...,
        unsatisfied_dependency_operation_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetJobQueueOperationSummaryRequest(_message.Message):
    __slots__ = ("environment_id", "operation_id", "limit", "offset")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    operation_id: str
    limit: int
    offset: int
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        operation_id: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
    ) -> None: ...

class GetJobQueueOperationSummaryResponse(_message.Message):
    __slots__ = ("summary",)
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    summary: JobQueueOperationSummary
    def __init__(self, summary: _Optional[_Union[JobQueueOperationSummary, _Mapping]] = ...) -> None: ...

class JobQueueAttempt(_message.Message):
    __slots__ = (
        "id",
        "created_at",
        "environment_id",
        "deployment_id",
        "job_queue_id",
        "attempt_idx",
        "queued_at",
        "started_at",
        "attempted_by",
        "state",
        "finished_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_IDX_FIELD_NUMBER: _ClassVar[int]
    QUEUED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTED_BY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    created_at: _timestamp_pb2.Timestamp
    environment_id: str
    deployment_id: str
    job_queue_id: int
    attempt_idx: int
    queued_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    attempted_by: str
    state: int
    finished_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        job_queue_id: _Optional[int] = ...,
        attempt_idx: _Optional[int] = ...,
        queued_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        attempted_by: _Optional[str] = ...,
        state: _Optional[int] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListJobQueueAttemptsRequest(_message.Message):
    __slots__ = ("job_queue_id", "operation_id")
    JOB_QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    job_queue_id: int
    operation_id: str
    def __init__(self, job_queue_id: _Optional[int] = ..., operation_id: _Optional[str] = ...) -> None: ...

class ListJobQueueAttemptsResponse(_message.Message):
    __slots__ = ("attempts",)
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    attempts: _containers.RepeatedCompositeFieldContainer[JobQueueAttempt]
    def __init__(self, attempts: _Optional[_Iterable[_Union[JobQueueAttempt, _Mapping]]] = ...) -> None: ...

class OperationAndShard(_message.Message):
    __slots__ = ("operation_id", "shard_id")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    shard_id: int
    def __init__(self, operation_id: _Optional[str] = ..., shard_id: _Optional[int] = ...) -> None: ...

class ForceCancelJobQueueJobRequest(_message.Message):
    __slots__ = ("environment_id", "by_job_queue_id", "by_operation_and_shard")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BY_JOB_QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    BY_OPERATION_AND_SHARD_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    by_job_queue_id: int
    by_operation_and_shard: OperationAndShard
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        by_job_queue_id: _Optional[int] = ...,
        by_operation_and_shard: _Optional[_Union[OperationAndShard, _Mapping]] = ...,
    ) -> None: ...

class ForceCancelJobQueueJobResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CancelWorkflowExecutionRequest(_message.Message):
    __slots__ = ("workflow_execution_id",)
    WORKFLOW_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_execution_id: str
    def __init__(self, workflow_execution_id: _Optional[str] = ...) -> None: ...

class CancelWorkflowExecutionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
