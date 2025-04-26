from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CDCTableReference(_message.Message):
    __slots__ = ("name", "schema")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    name: str
    schema: str
    def __init__(self, name: _Optional[str] = ..., schema: _Optional[str] = ...) -> None: ...

class CDCSource(_message.Message):
    __slots__ = ("integration_name", "tables")
    INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    integration_name: str
    tables: _containers.RepeatedCompositeFieldContainer[CDCTableReference]
    def __init__(
        self,
        integration_name: _Optional[str] = ...,
        tables: _Optional[_Iterable[_Union[CDCTableReference, _Mapping]]] = ...,
    ) -> None: ...
