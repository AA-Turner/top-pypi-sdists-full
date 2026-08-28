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

class WorkflowOrchestratorExecutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_UNSPECIFIED: _ClassVar[WorkflowOrchestratorExecutionStatus]
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_RUNNING: _ClassVar[WorkflowOrchestratorExecutionStatus]
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_COMPLETED: _ClassVar[WorkflowOrchestratorExecutionStatus]
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_FAILED: _ClassVar[WorkflowOrchestratorExecutionStatus]
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_CANCELED: _ClassVar[WorkflowOrchestratorExecutionStatus]
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_TERMINATED: _ClassVar[WorkflowOrchestratorExecutionStatus]
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_CONTINUED_AS_NEW: _ClassVar[WorkflowOrchestratorExecutionStatus]
    WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_TIMED_OUT: _ClassVar[WorkflowOrchestratorExecutionStatus]

WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_UNSPECIFIED: WorkflowOrchestratorExecutionStatus
WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_RUNNING: WorkflowOrchestratorExecutionStatus
WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_COMPLETED: WorkflowOrchestratorExecutionStatus
WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_FAILED: WorkflowOrchestratorExecutionStatus
WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_CANCELED: WorkflowOrchestratorExecutionStatus
WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_TERMINATED: WorkflowOrchestratorExecutionStatus
WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_CONTINUED_AS_NEW: WorkflowOrchestratorExecutionStatus
WORKFLOW_ORCHESTRATOR_EXECUTION_STATUS_TIMED_OUT: WorkflowOrchestratorExecutionStatus

class WorkflowOrchestratorNamespace(_message.Message):
    __slots__ = ("name", "state", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    state: str
    description: str
    def __init__(
        self, name: _Optional[str] = ..., state: _Optional[str] = ..., description: _Optional[str] = ...
    ) -> None: ...

class WorkflowOrchestratorExecutionSummary(_message.Message):
    __slots__ = (
        "workflow_id",
        "run_id",
        "workflow_type",
        "status",
        "start_time",
        "close_time",
        "task_queue",
        "history_length",
        "parent_workflow_id",
        "parent_run_id",
        "state_transition_count",
    )
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    CLOSE_TIME_FIELD_NUMBER: _ClassVar[int]
    TASK_QUEUE_FIELD_NUMBER: _ClassVar[int]
    HISTORY_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PARENT_WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_TRANSITION_COUNT_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    run_id: str
    workflow_type: str
    status: WorkflowOrchestratorExecutionStatus
    start_time: _timestamp_pb2.Timestamp
    close_time: _timestamp_pb2.Timestamp
    task_queue: str
    history_length: int
    parent_workflow_id: str
    parent_run_id: str
    state_transition_count: int
    def __init__(
        self,
        workflow_id: _Optional[str] = ...,
        run_id: _Optional[str] = ...,
        workflow_type: _Optional[str] = ...,
        status: _Optional[_Union[WorkflowOrchestratorExecutionStatus, str]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        close_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        task_queue: _Optional[str] = ...,
        history_length: _Optional[int] = ...,
        parent_workflow_id: _Optional[str] = ...,
        parent_run_id: _Optional[str] = ...,
        state_transition_count: _Optional[int] = ...,
    ) -> None: ...

class WorkflowOrchestratorPendingActivity(_message.Message):
    __slots__ = (
        "activity_id",
        "activity_type",
        "state",
        "attempt",
        "maximum_attempts",
        "scheduled_time",
        "last_started_time",
        "last_heartbeat_time",
        "last_failure_message",
        "last_worker_identity",
    )
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_STARTED_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARTBEAT_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_FAILURE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_WORKER_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    activity_id: str
    activity_type: str
    state: str
    attempt: int
    maximum_attempts: int
    scheduled_time: _timestamp_pb2.Timestamp
    last_started_time: _timestamp_pb2.Timestamp
    last_heartbeat_time: _timestamp_pb2.Timestamp
    last_failure_message: str
    last_worker_identity: str
    def __init__(
        self,
        activity_id: _Optional[str] = ...,
        activity_type: _Optional[str] = ...,
        state: _Optional[str] = ...,
        attempt: _Optional[int] = ...,
        maximum_attempts: _Optional[int] = ...,
        scheduled_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_started_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_heartbeat_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_failure_message: _Optional[str] = ...,
        last_worker_identity: _Optional[str] = ...,
    ) -> None: ...

class WorkflowOrchestratorHistoryEvent(_message.Message):
    __slots__ = ("event_id", "event_time", "event_type", "attributes_json")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_JSON_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    event_time: _timestamp_pb2.Timestamp
    event_type: str
    attributes_json: str
    def __init__(
        self,
        event_id: _Optional[int] = ...,
        event_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        event_type: _Optional[str] = ...,
        attributes_json: _Optional[str] = ...,
    ) -> None: ...

class WorkflowOrchestratorTraceSpan(_message.Message):
    __slots__ = (
        "span_id",
        "parent_span_id",
        "name",
        "kind",
        "status",
        "scheduled_time",
        "started_time",
        "end_time",
        "attempt",
        "failure_message",
        "resource_id",
        "initiating_event_id",
    )
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KIND_UNSPECIFIED: _ClassVar[WorkflowOrchestratorTraceSpan.Kind]
        KIND_WORKFLOW: _ClassVar[WorkflowOrchestratorTraceSpan.Kind]
        KIND_ACTIVITY: _ClassVar[WorkflowOrchestratorTraceSpan.Kind]
        KIND_TIMER: _ClassVar[WorkflowOrchestratorTraceSpan.Kind]
        KIND_CHILD_WORKFLOW: _ClassVar[WorkflowOrchestratorTraceSpan.Kind]

    KIND_UNSPECIFIED: WorkflowOrchestratorTraceSpan.Kind
    KIND_WORKFLOW: WorkflowOrchestratorTraceSpan.Kind
    KIND_ACTIVITY: WorkflowOrchestratorTraceSpan.Kind
    KIND_TIMER: WorkflowOrchestratorTraceSpan.Kind
    KIND_CHILD_WORKFLOW: WorkflowOrchestratorTraceSpan.Kind
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[WorkflowOrchestratorTraceSpan.Status]
        STATUS_RUNNING: _ClassVar[WorkflowOrchestratorTraceSpan.Status]
        STATUS_COMPLETED: _ClassVar[WorkflowOrchestratorTraceSpan.Status]
        STATUS_FAILED: _ClassVar[WorkflowOrchestratorTraceSpan.Status]
        STATUS_TIMED_OUT: _ClassVar[WorkflowOrchestratorTraceSpan.Status]
        STATUS_CANCELED: _ClassVar[WorkflowOrchestratorTraceSpan.Status]
        STATUS_TERMINATED: _ClassVar[WorkflowOrchestratorTraceSpan.Status]

    STATUS_UNSPECIFIED: WorkflowOrchestratorTraceSpan.Status
    STATUS_RUNNING: WorkflowOrchestratorTraceSpan.Status
    STATUS_COMPLETED: WorkflowOrchestratorTraceSpan.Status
    STATUS_FAILED: WorkflowOrchestratorTraceSpan.Status
    STATUS_TIMED_OUT: WorkflowOrchestratorTraceSpan.Status
    STATUS_CANCELED: WorkflowOrchestratorTraceSpan.Status
    STATUS_TERMINATED: WorkflowOrchestratorTraceSpan.Status
    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_TIME_FIELD_NUMBER: _ClassVar[int]
    STARTED_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    FAILURE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    INITIATING_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    span_id: str
    parent_span_id: str
    name: str
    kind: WorkflowOrchestratorTraceSpan.Kind
    status: WorkflowOrchestratorTraceSpan.Status
    scheduled_time: _timestamp_pb2.Timestamp
    started_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    attempt: int
    failure_message: str
    resource_id: str
    initiating_event_id: int
    def __init__(
        self,
        span_id: _Optional[str] = ...,
        parent_span_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        kind: _Optional[_Union[WorkflowOrchestratorTraceSpan.Kind, str]] = ...,
        status: _Optional[_Union[WorkflowOrchestratorTraceSpan.Status, str]] = ...,
        scheduled_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        attempt: _Optional[int] = ...,
        failure_message: _Optional[str] = ...,
        resource_id: _Optional[str] = ...,
        initiating_event_id: _Optional[int] = ...,
    ) -> None: ...

class ListWorkflowOrchestratorNamespacesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListWorkflowOrchestratorNamespacesResponse(_message.Message):
    __slots__ = ("namespaces",)
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    namespaces: _containers.RepeatedCompositeFieldContainer[WorkflowOrchestratorNamespace]
    def __init__(
        self, namespaces: _Optional[_Iterable[_Union[WorkflowOrchestratorNamespace, _Mapping]]] = ...
    ) -> None: ...

class ListWorkflowOrchestratorWorkflowsRequest(_message.Message):
    __slots__ = ("namespace", "query", "page_size", "next_page_token")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    query: str
    page_size: int
    next_page_token: bytes
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        query: _Optional[str] = ...,
        page_size: _Optional[int] = ...,
        next_page_token: _Optional[bytes] = ...,
    ) -> None: ...

class ListWorkflowOrchestratorWorkflowsResponse(_message.Message):
    __slots__ = ("workflows", "next_page_token")
    WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    workflows: _containers.RepeatedCompositeFieldContainer[WorkflowOrchestratorExecutionSummary]
    next_page_token: bytes
    def __init__(
        self,
        workflows: _Optional[_Iterable[_Union[WorkflowOrchestratorExecutionSummary, _Mapping]]] = ...,
        next_page_token: _Optional[bytes] = ...,
    ) -> None: ...

class DescribeWorkflowOrchestratorWorkflowRequest(_message.Message):
    __slots__ = ("namespace", "workflow_id", "run_id")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    workflow_id: str
    run_id: str
    def __init__(
        self, namespace: _Optional[str] = ..., workflow_id: _Optional[str] = ..., run_id: _Optional[str] = ...
    ) -> None: ...

class DescribeWorkflowOrchestratorWorkflowResponse(_message.Message):
    __slots__ = ("workflow", "pending_activities")
    WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    PENDING_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    workflow: WorkflowOrchestratorExecutionSummary
    pending_activities: _containers.RepeatedCompositeFieldContainer[WorkflowOrchestratorPendingActivity]
    def __init__(
        self,
        workflow: _Optional[_Union[WorkflowOrchestratorExecutionSummary, _Mapping]] = ...,
        pending_activities: _Optional[_Iterable[_Union[WorkflowOrchestratorPendingActivity, _Mapping]]] = ...,
    ) -> None: ...

class GetWorkflowOrchestratorWorkflowHistoryRequest(_message.Message):
    __slots__ = ("namespace", "workflow_id", "run_id")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    workflow_id: str
    run_id: str
    def __init__(
        self, namespace: _Optional[str] = ..., workflow_id: _Optional[str] = ..., run_id: _Optional[str] = ...
    ) -> None: ...

class GetWorkflowOrchestratorWorkflowHistoryResponse(_message.Message):
    __slots__ = ("events", "spans", "truncated")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[WorkflowOrchestratorHistoryEvent]
    spans: _containers.RepeatedCompositeFieldContainer[WorkflowOrchestratorTraceSpan]
    truncated: bool
    def __init__(
        self,
        events: _Optional[_Iterable[_Union[WorkflowOrchestratorHistoryEvent, _Mapping]]] = ...,
        spans: _Optional[_Iterable[_Union[WorkflowOrchestratorTraceSpan, _Mapping]]] = ...,
        truncated: bool = ...,
    ) -> None: ...

class GetWorkflowOrchestratorConnectionDetailsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetWorkflowOrchestratorConnectionDetailsResponse(_message.Message):
    __slots__ = ("endpoint", "temporal_namespace", "default_task_queue")
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    TEMPORAL_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TASK_QUEUE_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    temporal_namespace: str
    default_task_queue: str
    def __init__(
        self,
        endpoint: _Optional[str] = ...,
        temporal_namespace: _Optional[str] = ...,
        default_task_queue: _Optional[str] = ...,
    ) -> None: ...
