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

class MaterializedAggregateTileTimelineInterval(_message.Message):
    __slots__ = ("coverage_lower_bound", "coverage_upper_bound")
    COVERAGE_LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    coverage_lower_bound: _timestamp_pb2.Timestamp
    coverage_upper_bound: _timestamp_pb2.Timestamp
    def __init__(
        self,
        coverage_lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        coverage_upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class MaterializedAggregateTileTimeline(_message.Message):
    __slots__ = (
        "materialization_key_hash",
        "aggregation",
        "aggregate_on",
        "group_by",
        "bucket_on",
        "coverage",
        "intervals",
    )
    MATERIALIZATION_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    BUCKET_ON_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    INTERVALS_FIELD_NUMBER: _ClassVar[int]
    materialization_key_hash: str
    aggregation: str
    aggregate_on: str
    group_by: str
    bucket_on: str
    coverage: MaterializedAggregateTileTimelineInterval
    intervals: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileTimelineInterval]
    def __init__(
        self,
        materialization_key_hash: _Optional[str] = ...,
        aggregation: _Optional[str] = ...,
        aggregate_on: _Optional[str] = ...,
        group_by: _Optional[str] = ...,
        bucket_on: _Optional[str] = ...,
        coverage: _Optional[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]] = ...,
        intervals: _Optional[_Iterable[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]]] = ...,
    ) -> None: ...

class MaterializedAggregateTileTimelineGroup(_message.Message):
    __slots__ = ("aggregate_on", "timelines", "coverage")
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    TIMELINES_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    aggregate_on: str
    timelines: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileTimeline]
    coverage: MaterializedAggregateTileTimelineInterval
    def __init__(
        self,
        aggregate_on: _Optional[str] = ...,
        timelines: _Optional[_Iterable[_Union[MaterializedAggregateTileTimeline, _Mapping]]] = ...,
        coverage: _Optional[_Union[MaterializedAggregateTileTimelineInterval, _Mapping]] = ...,
    ) -> None: ...

class ListMaterializedAggregateTileTimelinesFilter(_message.Message):
    __slots__ = ("aggregate_on_prefix",)
    AGGREGATE_ON_PREFIX_FIELD_NUMBER: _ClassVar[int]
    aggregate_on_prefix: str
    def __init__(self, aggregate_on_prefix: _Optional[str] = ...) -> None: ...

class ListMaterializedAggregateTileTimelinesRequest(_message.Message):
    __slots__ = ("cursor", "limit", "filter")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    filter: ListMaterializedAggregateTileTimelinesFilter
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        filter: _Optional[_Union[ListMaterializedAggregateTileTimelinesFilter, _Mapping]] = ...,
    ) -> None: ...

class ListMaterializedAggregateTileTimelinesResponse(_message.Message):
    __slots__ = ("timeline_groups", "next_cursor")
    TIMELINE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    timeline_groups: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileTimelineGroup]
    next_cursor: str
    def __init__(
        self,
        timeline_groups: _Optional[_Iterable[_Union[MaterializedAggregateTileTimelineGroup, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...
