from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
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

class GridPosition(_message.Message):
    __slots__ = ("x", "y", "w", "h")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    H_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    w: int
    h: int
    def __init__(
        self, x: _Optional[int] = ..., y: _Optional[int] = ..., w: _Optional[int] = ..., h: _Optional[int] = ...
    ) -> None: ...

class DashboardElement(_message.Message):
    __slots__ = ("id", "position", "chart")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    CHART_FIELD_NUMBER: _ClassVar[int]
    id: str
    position: GridPosition
    chart: DashboardChart
    def __init__(
        self,
        id: _Optional[str] = ...,
        position: _Optional[_Union[GridPosition, _Mapping]] = ...,
        chart: _Optional[_Union[DashboardChart, _Mapping]] = ...,
    ) -> None: ...

class DashboardChart(_message.Message):
    __slots__ = ("name", "window_period", "series", "formulas", "display_window_period")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FORMULAS_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    name: str
    window_period: str
    series: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricConfigSeries]
    formulas: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricFormula]
    display_window_period: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        window_period: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[_chart_pb2.MetricConfigSeries, _Mapping]]] = ...,
        formulas: _Optional[_Iterable[_Union[_chart_pb2.MetricFormula, _Mapping]]] = ...,
        display_window_period: _Optional[str] = ...,
    ) -> None: ...

class Dashboard(_message.Message):
    __slots__ = ("id", "environment_id", "name", "elements", "created_at", "updated_at", "created_by")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    name: str
    elements: _containers.RepeatedCompositeFieldContainer[DashboardElement]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    created_by: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        elements: _Optional[_Iterable[_Union[DashboardElement, _Mapping]]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
    ) -> None: ...
