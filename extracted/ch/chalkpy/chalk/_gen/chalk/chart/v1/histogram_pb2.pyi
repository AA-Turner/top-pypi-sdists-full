from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
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

class HistogramBucket(_message.Message):
    __slots__ = ("lower_bound", "upper_bound", "count", "label")
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    lower_bound: float
    upper_bound: float
    count: float
    label: str
    def __init__(
        self,
        lower_bound: _Optional[float] = ...,
        upper_bound: _Optional[float] = ...,
        count: _Optional[float] = ...,
        label: _Optional[str] = ...,
    ) -> None: ...

class HistogramSeries(_message.Message):
    __slots__ = ("buckets", "label", "group_tags")
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    GROUP_TAGS_FIELD_NUMBER: _ClassVar[int]
    buckets: _containers.RepeatedCompositeFieldContainer[HistogramBucket]
    label: str
    group_tags: _containers.RepeatedCompositeFieldContainer[_densetimeserieschart_pb2.GroupTag]
    def __init__(
        self,
        buckets: _Optional[_Iterable[_Union[HistogramBucket, _Mapping]]] = ...,
        label: _Optional[str] = ...,
        group_tags: _Optional[_Iterable[_Union[_densetimeserieschart_pb2.GroupTag, _Mapping]]] = ...,
    ) -> None: ...

class HistogramChart(_message.Message):
    __slots__ = ("title", "series")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[HistogramSeries]
    def __init__(
        self, title: _Optional[str] = ..., series: _Optional[_Iterable[_Union[HistogramSeries, _Mapping]]] = ...
    ) -> None: ...
