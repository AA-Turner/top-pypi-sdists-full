from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MessageLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Message_LEVEL_ERROR: _ClassVar[MessageLevel]
    Message_LEVEL_WARNING: _ClassVar[MessageLevel]
    Message_LEVEL_INFO: _ClassVar[MessageLevel]
Message_LEVEL_ERROR: MessageLevel
Message_LEVEL_WARNING: MessageLevel
Message_LEVEL_INFO: MessageLevel

class ErrorMessage(_message.Message):
    __slots__ = ["code", "message"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class Matrix(_message.Message):
    __slots__ = ["v00", "v01", "v10", "v11"]
    V00_FIELD_NUMBER: _ClassVar[int]
    V01_FIELD_NUMBER: _ClassVar[int]
    V10_FIELD_NUMBER: _ClassVar[int]
    V11_FIELD_NUMBER: _ClassVar[int]
    v00: float
    v01: float
    v10: float
    v11: float
    def __init__(self, v00: _Optional[float] = ..., v01: _Optional[float] = ..., v10: _Optional[float] = ..., v11: _Optional[float] = ...) -> None: ...
