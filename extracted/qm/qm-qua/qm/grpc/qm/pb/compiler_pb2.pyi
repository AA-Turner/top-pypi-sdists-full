from qm.grpc.qm.pb import inc_qua_pb2 as _inc_qua_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from qm.grpc.qm.pb import qm_manager_pb2 as _qm_manager_pb2
from qm.grpc.qm.pb import general_messages_pb2 as _general_messages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuaValues(_message.Message):
    __slots__ = ["int_value", "double_value", "boolean_value"]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    int_value: int
    double_value: float
    boolean_value: bool
    def __init__(self, int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., boolean_value: bool = ...) -> None: ...

class CompileRequest(_message.Message):
    __slots__ = ["program", "jobId"]
    PROGRAM_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    program: _inc_qua_pb2.QuaProgram
    jobId: str
    def __init__(self, program: _Optional[_Union[_inc_qua_pb2.QuaProgram, _Mapping]] = ..., jobId: _Optional[str] = ...) -> None: ...

class CompileResponse(_message.Message):
    __slots__ = ["ok", "messages", "binary", "metadata", "debug"]
    class DebugEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OK_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    BINARY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    messages: _containers.RepeatedCompositeFieldContainer[CompilerMessage]
    binary: bytes
    metadata: str
    debug: _containers.ScalarMap[str, str]
    def __init__(self, ok: bool = ..., messages: _Optional[_Iterable[_Union[CompilerMessage, _Mapping]]] = ..., binary: _Optional[bytes] = ..., metadata: _Optional[str] = ..., debug: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CompilerMessage(_message.Message):
    __slots__ = ["message", "level"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    message: str
    level: _general_messages_pb2.MessageLevel
    def __init__(self, message: _Optional[str] = ..., level: _Optional[_Union[_general_messages_pb2.MessageLevel, str]] = ...) -> None: ...

class ValidationResponse(_message.Message):
    __slots__ = ["messages"]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[_qm_manager_pb2.ConfigValidationMessage]
    def __init__(self, messages: _Optional[_Iterable[_Union[_qm_manager_pb2.ConfigValidationMessage, _Mapping]]] = ...) -> None: ...

class DynamicConfig(_message.Message):
    __slots__ = ["version", "root"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    version: int
    root: _struct_pb2.Struct
    def __init__(self, version: _Optional[int] = ..., root: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
