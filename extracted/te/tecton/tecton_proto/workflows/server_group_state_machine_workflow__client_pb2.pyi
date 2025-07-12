from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import server_group_type__client_pb2 as _server_group_type__client_pb2
from tecton_proto.workflows import state_machine_workflow__client_pb2 as _state_machine_workflow__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServerGroupStateMachineWorkflowData(_message.Message):
    __slots__ = ["consecutive_failed_updates", "error_message", "server_group_state_id", "server_group_type", "state", "workspace"]
    class ServerGroupStateMachineWorkflowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CANCELLED: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    CANCELLED_DELETED: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    CANCELLING: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    CONSECUTIVE_FAILED_UPDATES_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PENDING: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    PERMANENTLY_FAILED: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    RUNNING: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    SERVER_GROUP_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    UNSPECIFIED: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    consecutive_failed_updates: int
    error_message: str
    server_group_state_id: _id__client_pb2.Id
    server_group_type: _server_group_type__client_pb2.ServerGroupType
    state: ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState
    workspace: str
    def __init__(self, state: _Optional[_Union[ServerGroupStateMachineWorkflowData.ServerGroupStateMachineWorkflowState, str]] = ..., consecutive_failed_updates: _Optional[int] = ..., server_group_state_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., workspace: _Optional[str] = ..., server_group_type: _Optional[_Union[_server_group_type__client_pb2.ServerGroupType, str]] = ..., error_message: _Optional[str] = ...) -> None: ...
