from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class WorkflowScheduleOverlapPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKFLOW_SCHEDULE_OVERLAP_POLICY_UNSPECIFIED: _ClassVar[WorkflowScheduleOverlapPolicy]
    WORKFLOW_SCHEDULE_OVERLAP_POLICY_SKIP: _ClassVar[WorkflowScheduleOverlapPolicy]
    WORKFLOW_SCHEDULE_OVERLAP_POLICY_ALLOW_ALL: _ClassVar[WorkflowScheduleOverlapPolicy]

class WorkflowScheduleControlStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKFLOW_SCHEDULE_CONTROL_STATUS_UNSPECIFIED: _ClassVar[WorkflowScheduleControlStatus]
    WORKFLOW_SCHEDULE_CONTROL_STATUS_PLAY: _ClassVar[WorkflowScheduleControlStatus]
    WORKFLOW_SCHEDULE_CONTROL_STATUS_PAUSE: _ClassVar[WorkflowScheduleControlStatus]

class WorkflowScheduleTriggerKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKFLOW_SCHEDULE_TRIGGER_KIND_UNSPECIFIED: _ClassVar[WorkflowScheduleTriggerKind]
    WORKFLOW_SCHEDULE_TRIGGER_KIND_SCHEDULED: _ClassVar[WorkflowScheduleTriggerKind]
    WORKFLOW_SCHEDULE_TRIGGER_KIND_MANUAL: _ClassVar[WorkflowScheduleTriggerKind]

class WorkflowScheduleRunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKFLOW_SCHEDULE_RUN_STATUS_UNSPECIFIED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_SCHEDULED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_INITIALIZING: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_INIT_FAILED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_SKIPPED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_QUEUED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_RUNNING: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_COMPLETED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_FAILED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_CANCELED: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_TIMED_OUT: _ClassVar[WorkflowScheduleRunStatus]
    WORKFLOW_SCHEDULE_RUN_STATUS_TERMINATED: _ClassVar[WorkflowScheduleRunStatus]

WORKFLOW_SCHEDULE_OVERLAP_POLICY_UNSPECIFIED: WorkflowScheduleOverlapPolicy
WORKFLOW_SCHEDULE_OVERLAP_POLICY_SKIP: WorkflowScheduleOverlapPolicy
WORKFLOW_SCHEDULE_OVERLAP_POLICY_ALLOW_ALL: WorkflowScheduleOverlapPolicy
WORKFLOW_SCHEDULE_CONTROL_STATUS_UNSPECIFIED: WorkflowScheduleControlStatus
WORKFLOW_SCHEDULE_CONTROL_STATUS_PLAY: WorkflowScheduleControlStatus
WORKFLOW_SCHEDULE_CONTROL_STATUS_PAUSE: WorkflowScheduleControlStatus
WORKFLOW_SCHEDULE_TRIGGER_KIND_UNSPECIFIED: WorkflowScheduleTriggerKind
WORKFLOW_SCHEDULE_TRIGGER_KIND_SCHEDULED: WorkflowScheduleTriggerKind
WORKFLOW_SCHEDULE_TRIGGER_KIND_MANUAL: WorkflowScheduleTriggerKind
WORKFLOW_SCHEDULE_RUN_STATUS_UNSPECIFIED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_SCHEDULED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_INITIALIZING: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_INIT_FAILED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_SKIPPED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_QUEUED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_RUNNING: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_COMPLETED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_FAILED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_CANCELED: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_TIMED_OUT: WorkflowScheduleRunStatus
WORKFLOW_SCHEDULE_RUN_STATUS_TERMINATED: WorkflowScheduleRunStatus

class WorkflowInvocationSpec(_message.Message):
    __slots__ = ("workflow_name", "task_queue", "inputs", "execution_timeout")
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_QUEUE_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    task_queue: str
    inputs: _struct_pb2.Struct
    execution_timeout: _duration_pb2.Duration
    def __init__(
        self,
        workflow_name: _Optional[str] = ...,
        task_queue: _Optional[str] = ...,
        inputs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        execution_timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class WorkflowScheduleSpec(_message.Message):
    __slots__ = ("workflow", "schedule", "overlap_policy", "status")
    WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    OVERLAP_POLICY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    workflow: WorkflowInvocationSpec
    schedule: str
    overlap_policy: WorkflowScheduleOverlapPolicy
    status: WorkflowScheduleControlStatus
    def __init__(
        self,
        workflow: _Optional[_Union[WorkflowInvocationSpec, _Mapping]] = ...,
        schedule: _Optional[str] = ...,
        overlap_policy: _Optional[_Union[WorkflowScheduleOverlapPolicy, str]] = ...,
        status: _Optional[_Union[WorkflowScheduleControlStatus, str]] = ...,
    ) -> None: ...

class WorkflowSchedule(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "spec",
        "created_by",
        "created_at",
        "updated_at",
        "deleted_at",
        "deleted_by",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_BY_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    spec: WorkflowScheduleSpec
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    deleted_by: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        spec: _Optional[_Union[WorkflowScheduleSpec, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        deleted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        deleted_by: _Optional[str] = ...,
    ) -> None: ...

class WorkflowExecutionReference(_message.Message):
    __slots__ = ("workflow_id", "workflow_run_id")
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    workflow_run_id: str
    def __init__(self, workflow_id: _Optional[str] = ..., workflow_run_id: _Optional[str] = ...) -> None: ...

class WorkflowScheduleRun(_message.Message):
    __slots__ = (
        "id",
        "workflow_schedule_id",
        "trigger_kind",
        "status",
        "status_message",
        "source_job_id",
        "triggered_at",
        "execution",
        "created_at",
        "updated_at",
        "completed_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_KIND_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGERED_AT_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    workflow_schedule_id: str
    trigger_kind: WorkflowScheduleTriggerKind
    status: WorkflowScheduleRunStatus
    status_message: str
    source_job_id: int
    triggered_at: _timestamp_pb2.Timestamp
    execution: WorkflowExecutionReference
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        workflow_schedule_id: _Optional[str] = ...,
        trigger_kind: _Optional[_Union[WorkflowScheduleTriggerKind, str]] = ...,
        status: _Optional[_Union[WorkflowScheduleRunStatus, str]] = ...,
        status_message: _Optional[str] = ...,
        source_job_id: _Optional[int] = ...,
        triggered_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        execution: _Optional[_Union[WorkflowExecutionReference, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CreateWorkflowScheduleRequest(_message.Message):
    __slots__ = ("name", "description", "spec")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    spec: WorkflowScheduleSpec
    def __init__(
        self,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        spec: _Optional[_Union[WorkflowScheduleSpec, _Mapping]] = ...,
    ) -> None: ...

class CreateWorkflowScheduleResponse(_message.Message):
    __slots__ = ("schedule",)
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    schedule: WorkflowSchedule
    def __init__(self, schedule: _Optional[_Union[WorkflowSchedule, _Mapping]] = ...) -> None: ...

class GetWorkflowScheduleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetWorkflowScheduleResponse(_message.Message):
    __slots__ = ("schedule",)
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    schedule: WorkflowSchedule
    def __init__(self, schedule: _Optional[_Union[WorkflowSchedule, _Mapping]] = ...) -> None: ...

class ListWorkflowSchedulesFilters(_message.Message):
    __slots__ = ("task_queue", "status", "trigger_kind", "include_deleted")
    TASK_QUEUE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_KIND_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    task_queue: str
    status: WorkflowScheduleControlStatus
    trigger_kind: WorkflowScheduleTriggerKind
    include_deleted: bool
    def __init__(
        self,
        task_queue: _Optional[str] = ...,
        status: _Optional[_Union[WorkflowScheduleControlStatus, str]] = ...,
        trigger_kind: _Optional[_Union[WorkflowScheduleTriggerKind, str]] = ...,
        include_deleted: bool = ...,
    ) -> None: ...

class ListWorkflowSchedulesRequest(_message.Message):
    __slots__ = ("filters", "cursor", "limit")
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    filters: ListWorkflowSchedulesFilters
    cursor: str
    limit: int
    def __init__(
        self,
        filters: _Optional[_Union[ListWorkflowSchedulesFilters, _Mapping]] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListWorkflowSchedulesResponse(_message.Message):
    __slots__ = ("schedules", "next_cursor")
    SCHEDULES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    schedules: _containers.RepeatedCompositeFieldContainer[WorkflowSchedule]
    next_cursor: str
    def __init__(
        self,
        schedules: _Optional[_Iterable[_Union[WorkflowSchedule, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class UpdateWorkflowInvocationOperation(_message.Message):
    __slots__ = ("workflow_name", "task_queue", "inputs", "execution_timeout")
    WORKFLOW_NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_QUEUE_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    workflow_name: str
    task_queue: str
    inputs: _struct_pb2.Struct
    execution_timeout: _duration_pb2.Duration
    def __init__(
        self,
        workflow_name: _Optional[str] = ...,
        task_queue: _Optional[str] = ...,
        inputs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        execution_timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class UpdateWorkflowScheduleSpecOperation(_message.Message):
    __slots__ = ("workflow", "schedule", "overlap_policy", "status")
    WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    OVERLAP_POLICY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    workflow: UpdateWorkflowInvocationOperation
    schedule: str
    overlap_policy: WorkflowScheduleOverlapPolicy
    status: WorkflowScheduleControlStatus
    def __init__(
        self,
        workflow: _Optional[_Union[UpdateWorkflowInvocationOperation, _Mapping]] = ...,
        schedule: _Optional[str] = ...,
        overlap_policy: _Optional[_Union[WorkflowScheduleOverlapPolicy, str]] = ...,
        status: _Optional[_Union[WorkflowScheduleControlStatus, str]] = ...,
    ) -> None: ...

class UpdateWorkflowScheduleOperation(_message.Message):
    __slots__ = ("name", "description", "spec")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    spec: UpdateWorkflowScheduleSpecOperation
    def __init__(
        self,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        spec: _Optional[_Union[UpdateWorkflowScheduleSpecOperation, _Mapping]] = ...,
    ) -> None: ...

class UpdateWorkflowScheduleRequest(_message.Message):
    __slots__ = ("id", "update", "update_mask")
    ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    update: UpdateWorkflowScheduleOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        id: _Optional[str] = ...,
        update: _Optional[_Union[UpdateWorkflowScheduleOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateWorkflowScheduleResponse(_message.Message):
    __slots__ = ("schedule",)
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    schedule: WorkflowSchedule
    def __init__(self, schedule: _Optional[_Union[WorkflowSchedule, _Mapping]] = ...) -> None: ...

class DeleteWorkflowScheduleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteWorkflowScheduleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TriggerWorkflowScheduleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TriggerWorkflowScheduleResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: WorkflowScheduleRun
    def __init__(self, run: _Optional[_Union[WorkflowScheduleRun, _Mapping]] = ...) -> None: ...

class ListWorkflowScheduleRunsFilters(_message.Message):
    __slots__ = ("status", "trigger_kind")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_KIND_FIELD_NUMBER: _ClassVar[int]
    status: WorkflowScheduleRunStatus
    trigger_kind: WorkflowScheduleTriggerKind
    def __init__(
        self,
        status: _Optional[_Union[WorkflowScheduleRunStatus, str]] = ...,
        trigger_kind: _Optional[_Union[WorkflowScheduleTriggerKind, str]] = ...,
    ) -> None: ...

class ListWorkflowScheduleRunsRequest(_message.Message):
    __slots__ = ("workflow_schedule_id", "filters", "cursor", "limit")
    WORKFLOW_SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    workflow_schedule_id: str
    filters: ListWorkflowScheduleRunsFilters
    cursor: str
    limit: int
    def __init__(
        self,
        workflow_schedule_id: _Optional[str] = ...,
        filters: _Optional[_Union[ListWorkflowScheduleRunsFilters, _Mapping]] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListWorkflowScheduleRunsResponse(_message.Message):
    __slots__ = ("runs", "next_cursor")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[WorkflowScheduleRun]
    next_cursor: str
    def __init__(
        self, runs: _Optional[_Iterable[_Union[WorkflowScheduleRun, _Mapping]]] = ..., next_cursor: _Optional[str] = ...
    ) -> None: ...
