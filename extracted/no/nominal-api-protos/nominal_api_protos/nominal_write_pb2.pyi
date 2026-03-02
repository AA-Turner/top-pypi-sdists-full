import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WriteRequestNominal(_message.Message):
    __slots__ = ("series",)
    SERIES_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[Series]
    def __init__(self, series: _Optional[_Iterable[_Union[Series, _Mapping]]] = ...) -> None: ...

class Series(_message.Message):
    __slots__ = ("channel", "tags", "points")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    channel: Channel
    tags: _containers.ScalarMap[str, str]
    points: Points
    def __init__(self, channel: _Optional[_Union[Channel, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ..., points: _Optional[_Union[Points, _Mapping]] = ...) -> None: ...

class Channel(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Points(_message.Message):
    __slots__ = ("double_points", "string_points", "integer_points", "array_points", "struct_points", "uint64_points")
    DOUBLE_POINTS_FIELD_NUMBER: _ClassVar[int]
    STRING_POINTS_FIELD_NUMBER: _ClassVar[int]
    INTEGER_POINTS_FIELD_NUMBER: _ClassVar[int]
    ARRAY_POINTS_FIELD_NUMBER: _ClassVar[int]
    STRUCT_POINTS_FIELD_NUMBER: _ClassVar[int]
    UINT64_POINTS_FIELD_NUMBER: _ClassVar[int]
    double_points: DoublePoints
    string_points: StringPoints
    integer_points: IntegerPoints
    array_points: ArrayPoints
    struct_points: StructPoints
    uint64_points: Uint64Points
    def __init__(self, double_points: _Optional[_Union[DoublePoints, _Mapping]] = ..., string_points: _Optional[_Union[StringPoints, _Mapping]] = ..., integer_points: _Optional[_Union[IntegerPoints, _Mapping]] = ..., array_points: _Optional[_Union[ArrayPoints, _Mapping]] = ..., struct_points: _Optional[_Union[StructPoints, _Mapping]] = ..., uint64_points: _Optional[_Union[Uint64Points, _Mapping]] = ...) -> None: ...

class DoublePoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[DoublePoint]
    def __init__(self, points: _Optional[_Iterable[_Union[DoublePoint, _Mapping]]] = ...) -> None: ...

class StringPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[StringPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[StringPoint, _Mapping]]] = ...) -> None: ...

class IntegerPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[IntegerPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[IntegerPoint, _Mapping]]] = ...) -> None: ...

class Uint64Points(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Uint64Point]
    def __init__(self, points: _Optional[_Iterable[_Union[Uint64Point, _Mapping]]] = ...) -> None: ...

class StructPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[StructPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[StructPoint, _Mapping]]] = ...) -> None: ...

class DoublePoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: float
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[float] = ...) -> None: ...

class StringPoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: str
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[str] = ...) -> None: ...

class IntegerPoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: int
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[int] = ...) -> None: ...

class Uint64Point(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: int
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[int] = ...) -> None: ...

class StructPoint(_message.Message):
    __slots__ = ("timestamp", "json_string")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    JSON_STRING_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    json_string: str
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., json_string: _Optional[str] = ...) -> None: ...

class ArrayPoints(_message.Message):
    __slots__ = ("double_array_points", "string_array_points")
    DOUBLE_ARRAY_POINTS_FIELD_NUMBER: _ClassVar[int]
    STRING_ARRAY_POINTS_FIELD_NUMBER: _ClassVar[int]
    double_array_points: DoubleArrayPoints
    string_array_points: StringArrayPoints
    def __init__(self, double_array_points: _Optional[_Union[DoubleArrayPoints, _Mapping]] = ..., string_array_points: _Optional[_Union[StringArrayPoints, _Mapping]] = ...) -> None: ...

class DoubleArrayPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[DoubleArrayPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[DoubleArrayPoint, _Mapping]]] = ...) -> None: ...

class StringArrayPoints(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[StringArrayPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[StringArrayPoint, _Mapping]]] = ...) -> None: ...

class DoubleArrayPoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[_Iterable[float]] = ...) -> None: ...

class StringArrayPoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[_Iterable[str]] = ...) -> None: ...
