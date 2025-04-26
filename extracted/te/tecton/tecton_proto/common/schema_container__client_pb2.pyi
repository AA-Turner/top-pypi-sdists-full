from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchemaContainer(_message.Message):
    __slots__ = ["tecton_schema"]
    TECTON_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    tecton_schema: _schema__client_pb2.Schema
    def __init__(self, tecton_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ...) -> None: ...
