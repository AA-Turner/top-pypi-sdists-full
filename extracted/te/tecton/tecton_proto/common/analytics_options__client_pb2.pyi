from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

ANALYTICS_FIELD_NUMBER: _ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
NOOP_FILTER: AnalyticsFilterType
PSEUDONYMIZE: AnalyticsFilterType
analytics: _descriptor.FieldDescriptor

class Analytics(_message.Message):
    __slots__ = ["filter_type"]
    FILTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    filter_type: AnalyticsFilterType
    def __init__(self, filter_type: _Optional[_Union[AnalyticsFilterType, str]] = ...) -> None: ...

class AnalyticsFilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
