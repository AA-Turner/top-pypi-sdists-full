from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class Series(_message.Message):
    __slots__ = ("points", "label", "units")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[float]
    label: str
    units: str
    def __init__(
        self, points: _Optional[_Iterable[float]] = ..., label: _Optional[str] = ..., units: _Optional[str] = ...
    ) -> None: ...

class Chart(_message.Message):
    __slots__ = ("title", "series", "x_timestamp_ms")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    X_TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[Series]
    x_timestamp_ms: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        title: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[Series, _Mapping]]] = ...,
        x_timestamp_ms: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class Point(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class TimeSeries(_message.Message):
    __slots__ = ("points", "label", "units")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Point]
    label: str
    units: str
    def __init__(
        self,
        points: _Optional[_Iterable[_Union[Point, _Mapping]]] = ...,
        label: _Optional[str] = ...,
        units: _Optional[str] = ...,
    ) -> None: ...

class TimeSeriesChart(_message.Message):
    __slots__ = ("title", "series", "x_series", "window_period")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    X_SERIES_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[TimeSeries]
    x_series: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    window_period: _duration_pb2.Duration
    def __init__(
        self,
        title: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[TimeSeries, _Mapping]]] = ...,
        x_series: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class ListChartsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListChartsResponse(_message.Message):
    __slots__ = ("charts",)
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricConfig]
    def __init__(self, charts: _Optional[_Iterable[_Union[_chart_pb2.MetricConfig, _Mapping]]] = ...) -> None: ...
