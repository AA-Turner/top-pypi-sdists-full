from tecton_proto.common import pair__client_pb2 as _pair__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
TEMPORAL_FEATURE_VIEW: CanaryFeatureViewType
UNDEFINED: CanaryFeatureViewType
WINDOW_AGGREGATE_FEATURE_VIEW: CanaryFeatureViewType

class CanaryUpdate(_message.Message):
    __slots__ = ["condition_expression", "dynamo_expression_attribute_names", "dynamo_expression_attribute_values", "feature_view_type", "is_status_table", "serialized_items", "table_name", "time"]
    CONDITION_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    DYNAMO_EXPRESSION_ATTRIBUTE_NAMES_FIELD_NUMBER: _ClassVar[int]
    DYNAMO_EXPRESSION_ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_STATUS_TABLE_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_ITEMS_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    condition_expression: str
    dynamo_expression_attribute_names: _containers.RepeatedCompositeFieldContainer[_pair__client_pb2.Pair]
    dynamo_expression_attribute_values: _containers.RepeatedCompositeFieldContainer[_pair__client_pb2.Pair]
    feature_view_type: CanaryFeatureViewType
    is_status_table: bool
    serialized_items: _containers.RepeatedCompositeFieldContainer[_pair__client_pb2.Pair]
    table_name: str
    time: str
    def __init__(self, table_name: _Optional[str] = ..., serialized_items: _Optional[_Iterable[_Union[_pair__client_pb2.Pair, _Mapping]]] = ..., condition_expression: _Optional[str] = ..., dynamo_expression_attribute_names: _Optional[_Iterable[_Union[_pair__client_pb2.Pair, _Mapping]]] = ..., dynamo_expression_attribute_values: _Optional[_Iterable[_Union[_pair__client_pb2.Pair, _Mapping]]] = ..., time: _Optional[str] = ..., is_status_table: bool = ..., feature_view_type: _Optional[_Union[CanaryFeatureViewType, str]] = ...) -> None: ...

class CanaryFeatureViewType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
