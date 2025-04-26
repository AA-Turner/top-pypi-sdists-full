from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CLIENT_LOG_MESSAGE_TYPE_METHOD_ENTRY: LogMessageType
CLIENT_LOG_MESSAGE_TYPE_METHOD_RETURN: LogMessageType
CLIENT_LOG_MESSAGE_TYPE_UNKNOWN: LogMessageType
DESCRIPTOR: _descriptor.FileDescriptor

class ErrorLog(_message.Message):
    __slots__ = ["cause", "message", "stacktrace"]
    CAUSE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STACKTRACE_FIELD_NUMBER: _ClassVar[int]
    cause: ErrorLog
    message: str
    stacktrace: str
    def __init__(self, message: _Optional[str] = ..., stacktrace: _Optional[str] = ..., cause: _Optional[_Union[ErrorLog, _Mapping]] = ...) -> None: ...

class LoggedValue(_message.Message):
    __slots__ = ["name", "value"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SDKMethodInvocation(_message.Message):
    __slots__ = ["class_name", "error", "execution_time", "is_local_fco", "log_level", "method_name", "params_or_return_values", "python_version", "sdk_version", "time", "trace_id", "type", "user_id", "workspace"]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_LOCAL_FCO_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    METHOD_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMS_OR_RETURN_VALUES_FIELD_NUMBER: _ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    class_name: str
    error: ErrorLog
    execution_time: _duration_pb2.Duration
    is_local_fco: bool
    log_level: str
    method_name: str
    params_or_return_values: _containers.RepeatedCompositeFieldContainer[LoggedValue]
    python_version: str
    sdk_version: str
    time: _timestamp_pb2.Timestamp
    trace_id: str
    type: LogMessageType
    user_id: str
    workspace: str
    def __init__(self, time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_id: _Optional[str] = ..., trace_id: _Optional[str] = ..., log_level: _Optional[str] = ..., type: _Optional[_Union[LogMessageType, str]] = ..., class_name: _Optional[str] = ..., method_name: _Optional[str] = ..., execution_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., params_or_return_values: _Optional[_Iterable[_Union[LoggedValue, _Mapping]]] = ..., error: _Optional[_Union[ErrorLog, _Mapping]] = ..., workspace: _Optional[str] = ..., sdk_version: _Optional[str] = ..., python_version: _Optional[str] = ..., is_local_fco: bool = ...) -> None: ...

class LogMessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
