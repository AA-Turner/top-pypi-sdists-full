from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class DensePoint(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...

class GroupTag(_message.Message):
    __slots__ = ("group_key", "value")
    GROUP_KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    group_key: str
    value: _arrow_pb2.ScalarValue
    def __init__(
        self, group_key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
    ) -> None: ...

class DenseTimeSeries(_message.Message):
    __slots__ = ("points", "label", "unit", "group_tags")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    GROUP_TAGS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[DensePoint]
    label: str
    unit: str
    group_tags: _containers.RepeatedCompositeFieldContainer[GroupTag]
    def __init__(
        self,
        points: _Optional[_Iterable[_Union[DensePoint, _Mapping]]] = ...,
        label: _Optional[str] = ...,
        unit: _Optional[str] = ...,
        group_tags: _Optional[_Iterable[_Union[GroupTag, _Mapping]]] = ...,
    ) -> None: ...

class DenseTimeSeriesChart(_message.Message):
    __slots__ = ("title", "series", "x_series", "window_period")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    X_SERIES_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[DenseTimeSeries]
    x_series: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    window_period: _duration_pb2.Duration
    def __init__(
        self,
        title: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[DenseTimeSeries, _Mapping]]] = ...,
        x_series: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...
