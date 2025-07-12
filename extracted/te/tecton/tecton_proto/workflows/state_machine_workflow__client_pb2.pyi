from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
LEGACY_STATE_HISTORY_FIELD_FIELD_NUMBER: _ClassVar[int]
STATE_FIELD_FIELD_NUMBER: _ClassVar[int]
TERMINAL_FIELD_NUMBER: _ClassVar[int]
legacy_state_history_field: _descriptor.FieldDescriptor
state_field: _descriptor.FieldDescriptor
terminal: _descriptor.FieldDescriptor

class TerminalStateOptions(_message.Message):
    __slots__ = ["retry_policy", "termination_code"]
    class WorkflowTerminationCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class RetryPolicy(_message.Message):
        __slots__ = ["enabled"]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        enabled: bool
        def __init__(self, enabled: bool = ...) -> None: ...
    CANCELLED: TerminalStateOptions.WorkflowTerminationCode
    OK: TerminalStateOptions.WorkflowTerminationCode
    RETRY_POLICY_FIELD_NUMBER: _ClassVar[int]
    TERMINATION_CODE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_ERROR: TerminalStateOptions.WorkflowTerminationCode
    retry_policy: TerminalStateOptions.RetryPolicy
    termination_code: TerminalStateOptions.WorkflowTerminationCode
    def __init__(self, termination_code: _Optional[_Union[TerminalStateOptions.WorkflowTerminationCode, str]] = ..., retry_policy: _Optional[_Union[TerminalStateOptions.RetryPolicy, _Mapping]] = ...) -> None: ...
