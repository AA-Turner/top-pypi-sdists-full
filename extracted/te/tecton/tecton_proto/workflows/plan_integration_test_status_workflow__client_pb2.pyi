from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.data import state_update__client_pb2 as _state_update__client_pb2
from tecton_proto.materialization import materialization_task__client_pb2 as _materialization_task__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlanIntegrationTestStateTransition(_message.Message):
    __slots__ = ["plan_status", "timestamp"]
    PLAN_STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    plan_status: _state_update__client_pb2.PlanStatusType
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., plan_status: _Optional[_Union[_state_update__client_pb2.PlanStatusType, str]] = ...) -> None: ...

class PlanIntegrationTestStatusWorkflow(_message.Message):
    __slots__ = ["job_urls", "plan_integration_select_type", "state_transitions", "tasks", "workspace_state_id"]
    JOB_URLS_FIELD_NUMBER: _ClassVar[int]
    PLAN_INTEGRATION_SELECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    job_urls: _containers.RepeatedScalarFieldContainer[str]
    plan_integration_select_type: _state_update__client_pb2.PlanIntegrationTestSelectType
    state_transitions: _containers.RepeatedCompositeFieldContainer[PlanIntegrationTestStateTransition]
    tasks: _containers.RepeatedCompositeFieldContainer[_materialization_task__client_pb2.MaterializationTask]
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, tasks: _Optional[_Iterable[_Union[_materialization_task__client_pb2.MaterializationTask, _Mapping]]] = ..., workspace_state_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., job_urls: _Optional[_Iterable[str]] = ..., plan_integration_select_type: _Optional[_Union[_state_update__client_pb2.PlanIntegrationTestSelectType, str]] = ..., state_transitions: _Optional[_Iterable[_Union[PlanIntegrationTestStateTransition, _Mapping]]] = ...) -> None: ...
