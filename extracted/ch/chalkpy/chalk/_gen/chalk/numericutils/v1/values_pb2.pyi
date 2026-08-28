from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NumericValue(_message.Message):
    __slots__ = ("int_value", "double_value")
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    int_value: int
    double_value: float
    def __init__(self, int_value: _Optional[int] = ..., double_value: _Optional[float] = ...) -> None: ...
