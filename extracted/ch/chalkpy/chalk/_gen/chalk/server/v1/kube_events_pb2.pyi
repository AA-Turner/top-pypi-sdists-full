from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
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

class KubeEvent(_message.Message):
    __slots__ = (
        "timestamp",
        "event_type",
        "severity",
        "cluster_name",
        "namespace",
        "name",
        "kind",
        "reason",
        "message",
        "source_component",
        "first_timestamp",
        "last_timestamp",
        "count",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    FIRST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    event_type: str
    severity: str
    cluster_name: str
    namespace: str
    name: str
    kind: str
    reason: str
    message: str
    source_component: str
    first_timestamp: _timestamp_pb2.Timestamp
    last_timestamp: _timestamp_pb2.Timestamp
    count: int
    def __init__(
        self,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        event_type: _Optional[str] = ...,
        severity: _Optional[str] = ...,
        cluster_name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        name: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
        source_component: _Optional[str] = ...,
        first_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        count: _Optional[int] = ...,
    ) -> None: ...

class ListKubeEventsPageToken(_message.Message):
    __slots__ = ("next_page_token",)
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    def __init__(self, next_page_token: _Optional[str] = ...) -> None: ...

class ListKubeEventsRequest(_message.Message):
    __slots__ = (
        "start_time",
        "end_time",
        "namespaces",
        "pod_names",
        "message_filter",
        "limit",
        "offset",
        "query",
        "page_token",
    )
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    POD_NAMES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FILTER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    namespaces: _containers.RepeatedScalarFieldContainer[str]
    pod_names: _containers.RepeatedScalarFieldContainer[str]
    message_filter: str
    limit: int
    offset: int
    query: str
    page_token: ListKubeEventsPageToken
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        namespaces: _Optional[_Iterable[str]] = ...,
        pod_names: _Optional[_Iterable[str]] = ...,
        message_filter: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        query: _Optional[str] = ...,
        page_token: _Optional[_Union[ListKubeEventsPageToken, _Mapping]] = ...,
    ) -> None: ...

class ListKubeEventsResponse(_message.Message):
    __slots__ = ("events", "next_page_token")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[KubeEvent]
    next_page_token: ListKubeEventsPageToken
    def __init__(
        self,
        events: _Optional[_Iterable[_Union[KubeEvent, _Mapping]]] = ...,
        next_page_token: _Optional[_Union[ListKubeEventsPageToken, _Mapping]] = ...,
    ) -> None: ...

class KubeEventFacet(_message.Message):
    __slots__ = ("path", "name")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetKubeEventFacetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKubeEventFacetsResponse(_message.Message):
    __slots__ = ("facets",)
    FACETS_FIELD_NUMBER: _ClassVar[int]
    facets: _containers.RepeatedCompositeFieldContainer[KubeEventFacet]
    def __init__(self, facets: _Optional[_Iterable[_Union[KubeEventFacet, _Mapping]]] = ...) -> None: ...

class GetKubeEventFacetValuesRequest(_message.Message):
    __slots__ = ("path", "start_time", "end_time", "limit", "query")
    PATH_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    path: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    query: str
    def __init__(
        self,
        path: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        query: _Optional[str] = ...,
    ) -> None: ...

class KubeEventFacetValue(_message.Message):
    __slots__ = ("value", "count")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    value: str
    count: int
    def __init__(self, value: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetKubeEventFacetValuesResponse(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[KubeEventFacetValue]
    def __init__(self, values: _Optional[_Iterable[_Union[KubeEventFacetValue, _Mapping]]] = ...) -> None: ...

class ListKubeEventsAggregatedRequest(_message.Message):
    __slots__ = ("query", "start_time", "end_time", "window_period")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    query: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    window_period: _duration_pb2.Duration
    def __init__(
        self,
        query: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class ListKubeEventsAggregatedResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...
