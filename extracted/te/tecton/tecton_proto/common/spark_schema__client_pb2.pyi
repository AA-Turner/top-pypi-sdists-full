from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SparkField(_message.Message):
    __slots__ = ["name", "structfield_json"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRUCTFIELD_JSON_FIELD_NUMBER: _ClassVar[int]
    name: str
    structfield_json: str
    def __init__(self, name: _Optional[str] = ..., structfield_json: _Optional[str] = ...) -> None: ...

class SparkSchema(_message.Message):
    __slots__ = ["fields"]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[SparkField]
    def __init__(self, fields: _Optional[_Iterable[_Union[SparkField, _Mapping]]] = ...) -> None: ...
