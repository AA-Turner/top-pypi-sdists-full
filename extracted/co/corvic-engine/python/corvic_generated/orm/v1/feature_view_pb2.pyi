from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputSource(_message.Message):
    __slots__ = ("source_id",)
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    def __init__(self, source_id: _Optional[str] = ...) -> None: ...

class FeatureViewOutput(_message.Message):
    __slots__ = ("output_sources",)
    OUTPUT_SOURCES_FIELD_NUMBER: _ClassVar[int]
    output_sources: _containers.RepeatedCompositeFieldContainer[OutputSource]
    def __init__(self, output_sources: _Optional[_Iterable[_Union[OutputSource, _Mapping]]] = ...) -> None: ...
