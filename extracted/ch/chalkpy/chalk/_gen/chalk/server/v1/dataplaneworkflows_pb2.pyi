from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import dataplanejobqueue_pb2 as _dataplanejobqueue_pb2
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

class WorkflowKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKFLOW_KIND_UNSPECIFIED: _ClassVar[WorkflowKind]
    WORKFLOW_KIND_MANUAL: _ClassVar[WorkflowKind]
    WORKFLOW_KIND_CRON: _ClassVar[WorkflowKind]
    WORKFLOW_KIND_SCHEDULED_QUERY: _ClassVar[WorkflowKind]

class WorkflowExecutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKFLOW_EXECUTION_STATUS_UNSPECIFIED: _ClassVar[WorkflowExecutionStatus]
    WORKFLOW_EXECUTION_STATUS_QUEUED: _ClassVar[WorkflowExecutionStatus]
    WORKFLOW_EXECUTION_STATUS_WORKING: _ClassVar[WorkflowExecutionStatus]
    WORKFLOW_EXECUTION_STATUS_COMPLETED: _ClassVar[WorkflowExecutionStatus]
    WORKFLOW_EXECUTION_STATUS_FAILED: _ClassVar[WorkflowExecutionStatus]
    WORKFLOW_EXECUTION_STATUS_CANCELED: _ClassVar[WorkflowExecutionStatus]

WORKFLOW_KIND_UNSPECIFIED: WorkflowKind
WORKFLOW_KIND_MANUAL: WorkflowKind
WORKFLOW_KIND_CRON: WorkflowKind
WORKFLOW_KIND_SCHEDULED_QUERY: WorkflowKind
WORKFLOW_EXECUTION_STATUS_UNSPECIFIED: WorkflowExecutionStatus
WORKFLOW_EXECUTION_STATUS_QUEUED: WorkflowExecutionStatus
WORKFLOW_EXECUTION_STATUS_WORKING: WorkflowExecutionStatus
WORKFLOW_EXECUTION_STATUS_COMPLETED: WorkflowExecutionStatus
WORKFLOW_EXECUTION_STATUS_FAILED: WorkflowExecutionStatus
WORKFLOW_EXECUTION_STATUS_CANCELED: WorkflowExecutionStatus

class WorkflowExecution(_message.Message):
    __slots__ = (
        "id",
        "created_at",
        "environment_id",
        "deployment_id",
        "kind",
        "status",
        "branch_name",
        "mainline_deployment_id",
        "agent_id",
        "meta_data",
        "updated_at",
        "finalized_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    MAINLINE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    created_at: _timestamp_pb2.Timestamp
    environment_id: str
    deployment_id: str
    kind: WorkflowKind
    status: WorkflowExecutionStatus
    branch_name: str
    mainline_deployment_id: str
    agent_id: str
    meta_data: _struct_pb2.Struct
    updated_at: _timestamp_pb2.Timestamp
    finalized_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        kind: _Optional[_Union[WorkflowKind, str]] = ...,
        status: _Optional[_Union[WorkflowExecutionStatus, str]] = ...,
        branch_name: _Optional[str] = ...,
        mainline_deployment_id: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        meta_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetDataPlaneWorkflowRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDataPlaneWorkflowResponse(_message.Message):
    __slots__ = ("workflow",)
    WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    workflow: WorkflowExecution
    def __init__(self, workflow: _Optional[_Union[WorkflowExecution, _Mapping]] = ...) -> None: ...

class ListDataPlaneWorkflowsRequest(_message.Message):
    __slots__ = ("environment_id", "deployment_id", "kind", "status", "limit", "offset", "id_filter")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    deployment_id: str
    kind: WorkflowKind
    status: WorkflowExecutionStatus
    limit: int
    offset: int
    id_filter: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        kind: _Optional[_Union[WorkflowKind, str]] = ...,
        status: _Optional[_Union[WorkflowExecutionStatus, str]] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        id_filter: _Optional[str] = ...,
    ) -> None: ...

class ListDataPlaneWorkflowsResponse(_message.Message):
    __slots__ = ("workflows", "total")
    WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    workflows: _containers.RepeatedCompositeFieldContainer[WorkflowExecution]
    total: int
    def __init__(
        self, workflows: _Optional[_Iterable[_Union[WorkflowExecution, _Mapping]]] = ..., total: _Optional[int] = ...
    ) -> None: ...

class GetWorkflowGraphRequest(_message.Message):
    __slots__ = ("workflow_execution_id",)
    WORKFLOW_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_execution_id: str
    def __init__(self, workflow_execution_id: _Optional[str] = ...) -> None: ...

class JobQueueRowSummaryForWorkflows(_message.Message):
    __slots__ = ("id", "job_name", "state", "job_index", "created_at", "finalized_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    JOB_INDEX_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    job_name: str
    state: _dataplanejobqueue_pb2.JobQueueState
    job_index: int
    created_at: _timestamp_pb2.Timestamp
    finalized_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        job_name: _Optional[str] = ...,
        state: _Optional[_Union[_dataplanejobqueue_pb2.JobQueueState, str]] = ...,
        job_index: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class WorkflowGraphNode(_message.Message):
    __slots__ = (
        "job_queue_id",
        "job_name",
        "job_index",
        "state",
        "created_at",
        "finalized_at",
        "operation_id",
        "kind",
        "resource_group",
        "job_queue_row_summaries",
    )
    JOB_QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    JOB_INDEX_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    JOB_QUEUE_ROW_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    job_queue_id: int
    job_name: str
    job_index: int
    state: _dataplanejobqueue_pb2.JobQueueState
    created_at: _timestamp_pb2.Timestamp
    finalized_at: _timestamp_pb2.Timestamp
    operation_id: str
    kind: _dataplanejobqueue_pb2.JobQueueKind
    resource_group: str
    job_queue_row_summaries: _containers.RepeatedCompositeFieldContainer[JobQueueRowSummaryForWorkflows]
    def __init__(
        self,
        job_queue_id: _Optional[int] = ...,
        job_name: _Optional[str] = ...,
        job_index: _Optional[int] = ...,
        state: _Optional[_Union[_dataplanejobqueue_pb2.JobQueueState, str]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finalized_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        operation_id: _Optional[str] = ...,
        kind: _Optional[_Union[_dataplanejobqueue_pb2.JobQueueKind, str]] = ...,
        resource_group: _Optional[str] = ...,
        job_queue_row_summaries: _Optional[_Iterable[_Union[JobQueueRowSummaryForWorkflows, _Mapping]]] = ...,
    ) -> None: ...

class WorkflowGraphEdge(_message.Message):
    __slots__ = (
        "source_operation_id",
        "target_operation_id",
        "satisfied_at",
        "dependent_operation_id",
        "dependency_operation_id",
    )
    SOURCE_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    SATISFIED_AT_FIELD_NUMBER: _ClassVar[int]
    DEPENDENT_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    source_operation_id: str
    target_operation_id: str
    satisfied_at: _timestamp_pb2.Timestamp
    dependent_operation_id: str
    dependency_operation_id: str
    def __init__(
        self,
        source_operation_id: _Optional[str] = ...,
        target_operation_id: _Optional[str] = ...,
        satisfied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        dependent_operation_id: _Optional[str] = ...,
        dependency_operation_id: _Optional[str] = ...,
    ) -> None: ...

class GetWorkflowGraphResponse(_message.Message):
    __slots__ = ("nodes", "edges")
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[WorkflowGraphNode]
    edges: _containers.RepeatedCompositeFieldContainer[WorkflowGraphEdge]
    def __init__(
        self,
        nodes: _Optional[_Iterable[_Union[WorkflowGraphNode, _Mapping]]] = ...,
        edges: _Optional[_Iterable[_Union[WorkflowGraphEdge, _Mapping]]] = ...,
    ) -> None: ...
