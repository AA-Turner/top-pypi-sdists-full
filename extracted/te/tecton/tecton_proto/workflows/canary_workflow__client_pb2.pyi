from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import fco_locator__client_pb2 as _fco_locator__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CANARY_WORKFLOW_STATE_CANCELLATION_REQUESTED: CanaryWorkflowState
CANARY_WORKFLOW_STATE_COMPLETED: CanaryWorkflowState
CANARY_WORKFLOW_STATE_FVS_SELECTED: CanaryWorkflowState
CANARY_WORKFLOW_STATE_PREPARED_STREAMING_JOBS: CanaryWorkflowState
CANARY_WORKFLOW_STATE_SPARK_EXECUTIONS_SUBMITTED: CanaryWorkflowState
CANARY_WORKFLOW_STATE_STARTED: CanaryWorkflowState
CANARY_WORKFLOW_STATE_UNKNOWN: CanaryWorkflowState
DESCRIPTOR: _descriptor.FileDescriptor

class CanaryWorkflow(_message.Message):
    __slots__ = ["canary_id", "fv_canaries", "state_transitions", "tecton_materialization_runtime_to_test"]
    CANARY_ID_FIELD_NUMBER: _ClassVar[int]
    FV_CANARIES_FIELD_NUMBER: _ClassVar[int]
    STATE_TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_TO_TEST_FIELD_NUMBER: _ClassVar[int]
    canary_id: str
    fv_canaries: _containers.RepeatedCompositeFieldContainer[FVCanary]
    state_transitions: _containers.RepeatedCompositeFieldContainer[CanaryWorkflowStateTransition]
    tecton_materialization_runtime_to_test: str
    def __init__(self, state_transitions: _Optional[_Iterable[_Union[CanaryWorkflowStateTransition, _Mapping]]] = ..., canary_id: _Optional[str] = ..., fv_canaries: _Optional[_Iterable[_Union[FVCanary, _Mapping]]] = ..., tecton_materialization_runtime_to_test: _Optional[str] = ...) -> None: ...

class CanaryWorkflowStateTransition(_message.Message):
    __slots__ = ["timestamp", "workflow_state"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_STATE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    workflow_state: CanaryWorkflowState
    def __init__(self, workflow_state: _Optional[_Union[CanaryWorkflowState, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FVCanary(_message.Message):
    __slots__ = ["base_batch_workflows", "base_streaming_workflow", "canary_table_name", "fv_name", "has_batch_canary", "has_stream_canary", "id_fv_locator", "new_batch_workflows", "new_streaming_workflow"]
    BASE_BATCH_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    BASE_STREAMING_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    CANARY_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    FV_NAME_FIELD_NUMBER: _ClassVar[int]
    HAS_BATCH_CANARY_FIELD_NUMBER: _ClassVar[int]
    HAS_STREAM_CANARY_FIELD_NUMBER: _ClassVar[int]
    ID_FV_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    NEW_BATCH_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    NEW_STREAMING_WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    base_batch_workflows: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    base_streaming_workflow: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    canary_table_name: str
    fv_name: str
    has_batch_canary: bool
    has_stream_canary: bool
    id_fv_locator: _fco_locator__client_pb2.IdFcoLocator
    new_batch_workflows: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    new_streaming_workflow: _containers.RepeatedCompositeFieldContainer[_id__client_pb2.Id]
    def __init__(self, id_fv_locator: _Optional[_Union[_fco_locator__client_pb2.IdFcoLocator, _Mapping]] = ..., fv_name: _Optional[str] = ..., has_batch_canary: bool = ..., has_stream_canary: bool = ..., base_batch_workflows: _Optional[_Iterable[_Union[_id__client_pb2.Id, _Mapping]]] = ..., new_batch_workflows: _Optional[_Iterable[_Union[_id__client_pb2.Id, _Mapping]]] = ..., base_streaming_workflow: _Optional[_Iterable[_Union[_id__client_pb2.Id, _Mapping]]] = ..., new_streaming_workflow: _Optional[_Iterable[_Union[_id__client_pb2.Id, _Mapping]]] = ..., canary_table_name: _Optional[str] = ...) -> None: ...

class CanaryWorkflowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
