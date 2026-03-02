from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_TYPE_UNSPECIFIED: _ClassVar[DataType]
    DATA_TYPE_INT: _ClassVar[DataType]
    DATA_TYPE_DOUBLE: _ClassVar[DataType]
    DATA_TYPE_STRING: _ClassVar[DataType]
DATA_TYPE_UNSPECIFIED: DataType
DATA_TYPE_INT: DataType
DATA_TYPE_DOUBLE: DataType
DATA_TYPE_STRING: DataType

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos", "picos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    PICOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    picos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ..., picos: _Optional[int] = ...) -> None: ...

class Range(_message.Message):
    __slots__ = ("start_time_inclusive", "end_time_exclusive")
    START_TIME_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIME_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    start_time_inclusive: Timestamp
    end_time_exclusive: Timestamp
    def __init__(self, start_time_inclusive: _Optional[_Union[Timestamp, _Mapping]] = ..., end_time_exclusive: _Optional[_Union[Timestamp, _Mapping]] = ...) -> None: ...

class TagValues(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class ChannelMetadata(_message.Message):
    __slots__ = ("channel", "data_type", "all_tag_values")
    class AllTagValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TagValues
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TagValues, _Mapping]] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    ALL_TAG_VALUES_FIELD_NUMBER: _ClassVar[int]
    channel: str
    data_type: DataType
    all_tag_values: _containers.MessageMap[str, TagValues]
    def __init__(self, channel: _Optional[str] = ..., data_type: _Optional[_Union[DataType, str]] = ..., all_tag_values: _Optional[_Mapping[str, TagValues]] = ...) -> None: ...

class ListChannelsRequest(_message.Message):
    __slots__ = ("page_size", "range", "page_token")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    range: Range
    page_token: str
    def __init__(self, page_size: _Optional[int] = ..., range: _Optional[_Union[Range, _Mapping]] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListChannelsResponse(_message.Message):
    __slots__ = ("channels", "page_token")
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[ChannelMetadata]
    page_token: str
    def __init__(self, channels: _Optional[_Iterable[_Union[ChannelMetadata, _Mapping]]] = ..., page_token: _Optional[str] = ...) -> None: ...

class QueryChannelRequest(_message.Message):
    __slots__ = ("channel", "tags", "range")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    channel: str
    tags: _containers.ScalarMap[str, str]
    range: Range
    def __init__(self, channel: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., range: _Optional[_Union[Range, _Mapping]] = ...) -> None: ...

class IntPoints(_message.Message):
    __slots__ = ("timestamps", "values")
    TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    timestamps: _containers.RepeatedCompositeFieldContainer[Timestamp]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, timestamps: _Optional[_Iterable[_Union[Timestamp, _Mapping]]] = ..., values: _Optional[_Iterable[int]] = ...) -> None: ...

class DoublePoints(_message.Message):
    __slots__ = ("timestamps", "values")
    TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    timestamps: _containers.RepeatedCompositeFieldContainer[Timestamp]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, timestamps: _Optional[_Iterable[_Union[Timestamp, _Mapping]]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class StringPoints(_message.Message):
    __slots__ = ("timestamps", "values")
    TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    timestamps: _containers.RepeatedCompositeFieldContainer[Timestamp]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, timestamps: _Optional[_Iterable[_Union[Timestamp, _Mapping]]] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryChannelResponse(_message.Message):
    __slots__ = ("ints", "doubles", "strings")
    INTS_FIELD_NUMBER: _ClassVar[int]
    DOUBLES_FIELD_NUMBER: _ClassVar[int]
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    ints: IntPoints
    doubles: DoublePoints
    strings: StringPoints
    def __init__(self, ints: _Optional[_Union[IntPoints, _Mapping]] = ..., doubles: _Optional[_Union[DoublePoints, _Mapping]] = ..., strings: _Optional[_Union[StringPoints, _Mapping]] = ...) -> None: ...
