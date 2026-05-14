from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ParseSQLResolverRequest(_message.Message):
    __slots__ = ("sql_string",)
    SQL_STRING_FIELD_NUMBER: _ClassVar[int]
    sql_string: str
    def __init__(self, sql_string: _Optional[str] = ...) -> None: ...

class ParseSQLResolverResponse(_message.Message):
    __slots__ = ("inputs", "outputs")
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedScalarFieldContainer[str]
    outputs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, inputs: _Optional[_Iterable[str]] = ..., outputs: _Optional[_Iterable[str]] = ...) -> None: ...
