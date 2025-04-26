from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class GetOverviewSummaryMetricsRequest(_message.Message):
    __slots__ = ("range_start", "range_end")
    RANGE_START_FIELD_NUMBER: _ClassVar[int]
    RANGE_END_FIELD_NUMBER: _ClassVar[int]
    range_start: str
    range_end: str
    def __init__(self, range_start: _Optional[str] = ..., range_end: _Optional[str] = ...) -> None: ...

class OverviewSummaryMetric(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: float
    def __init__(self, name: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...

class GetOverviewSummaryMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[OverviewSummaryMetric]
    def __init__(self, metrics: _Optional[_Iterable[_Union[OverviewSummaryMetric, _Mapping]]] = ...) -> None: ...
