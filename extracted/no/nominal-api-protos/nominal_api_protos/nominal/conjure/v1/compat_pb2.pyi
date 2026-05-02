from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor
CONJURE_COMPAT_FIELD_NUMBER: _ClassVar[int]
conjure_compat: _descriptor.FieldDescriptor
CONJURE_FIELD_COMPAT_FIELD_NUMBER: _ClassVar[int]
conjure_field_compat: _descriptor.FieldDescriptor

class ConjureCompatibility(_message.Message):
    __slots__ = ("union_message",)
    UNION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    union_message: bool
    def __init__(self, union_message: bool = ...) -> None: ...

class ConjureFieldCompatibility(_message.Message):
    __slots__ = ("map_value_wrapper",)
    MAP_VALUE_WRAPPER_FIELD_NUMBER: _ClassVar[int]
    map_value_wrapper: bool
    def __init__(self, map_value_wrapper: bool = ...) -> None: ...
