from tecton_proto.data import fco_metadata__client_pb2 as _fco_metadata__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FcoSummary(_message.Message):
    __slots__ = ["fco_metadata", "summary_items"]
    FCO_METADATA_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_ITEMS_FIELD_NUMBER: _ClassVar[int]
    fco_metadata: _fco_metadata__client_pb2.FcoMetadata
    summary_items: _containers.RepeatedCompositeFieldContainer[SummaryItem]
    def __init__(self, fco_metadata: _Optional[_Union[_fco_metadata__client_pb2.FcoMetadata, _Mapping]] = ..., summary_items: _Optional[_Iterable[_Union[SummaryItem, _Mapping]]] = ...) -> None: ...

class SummaryItem(_message.Message):
    __slots__ = ["display_name", "key", "multi_values", "nested_summary_items", "value"]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    MULTI_VALUES_FIELD_NUMBER: _ClassVar[int]
    NESTED_SUMMARY_ITEMS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    key: str
    multi_values: _containers.RepeatedScalarFieldContainer[str]
    nested_summary_items: _containers.RepeatedCompositeFieldContainer[SummaryItem]
    value: str
    def __init__(self, key: _Optional[str] = ..., display_name: _Optional[str] = ..., value: _Optional[str] = ..., multi_values: _Optional[_Iterable[str]] = ..., nested_summary_items: _Optional[_Iterable[_Union[SummaryItem, _Mapping]]] = ...) -> None: ...
