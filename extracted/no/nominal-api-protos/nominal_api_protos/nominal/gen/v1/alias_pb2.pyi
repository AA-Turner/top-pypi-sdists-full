from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor
ALIAS_FIELD_NUMBER: _ClassVar[int]
alias: _descriptor.FieldDescriptor

class Alias(_message.Message):
    __slots__ = ("java_name", "key_java_name", "value_java_name")
    JAVA_NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_JAVA_NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_JAVA_NAME_FIELD_NUMBER: _ClassVar[int]
    java_name: str
    key_java_name: str
    value_java_name: str
    def __init__(self, java_name: _Optional[str] = ..., key_java_name: _Optional[str] = ..., value_java_name: _Optional[str] = ...) -> None: ...
