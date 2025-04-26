from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserDefinedFunction(_message.Message):
    __slots__ = ["body", "isolate_function_deserialization", "name"]
    BODY_FIELD_NUMBER: _ClassVar[int]
    ISOLATE_FUNCTION_DESERIALIZATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    body: str
    isolate_function_deserialization: bool
    name: str
    def __init__(self, name: _Optional[str] = ..., body: _Optional[str] = ..., isolate_function_deserialization: bool = ...) -> None: ...
