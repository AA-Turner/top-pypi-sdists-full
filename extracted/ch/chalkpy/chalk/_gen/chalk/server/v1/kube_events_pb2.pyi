from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
from chalk._gen.chalk.searchaggregates.v1 import aggregation_pb2 as _aggregation_pb2
from chalk._gen.chalk.server.v1 import chart_pb2 as _chart_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class KubeEventFacetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KUBE_EVENT_FACET_TYPE_UNSPECIFIED: _ClassVar[KubeEventFacetType]
    KUBE_EVENT_FACET_TYPE_LIST: _ClassVar[KubeEventFacetType]
    KUBE_EVENT_FACET_TYPE_RANGE: _ClassVar[KubeEventFacetType]
    KUBE_EVENT_FACET_TYPE_TEXT: _ClassVar[KubeEventFacetType]
    KUBE_EVENT_FACET_TYPE_ID: _ClassVar[KubeEventFacetType]

KUBE_EVENT_FACET_TYPE_UNSPECIFIED: KubeEventFacetType
KUBE_EVENT_FACET_TYPE_LIST: KubeEventFacetType
KUBE_EVENT_FACET_TYPE_RANGE: KubeEventFacetType
KUBE_EVENT_FACET_TYPE_TEXT: KubeEventFacetType
KUBE_EVENT_FACET_TYPE_ID: KubeEventFacetType

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
        "id",
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
    ID_FIELD_NUMBER: _ClassVar[int]
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
    id: str
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
        id: _Optional[str] = ...,
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
    __slots__ = ("path", "name", "groupable", "facet_type", "supported_aggregations")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GROUPABLE_FIELD_NUMBER: _ClassVar[int]
    FACET_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    groupable: bool
    facet_type: KubeEventFacetType
    supported_aggregations: _containers.RepeatedScalarFieldContainer[_aggregation_pb2.AggregationFunction]
    def __init__(
        self,
        path: _Optional[str] = ...,
        name: _Optional[str] = ...,
        groupable: bool = ...,
        facet_type: _Optional[_Union[KubeEventFacetType, str]] = ...,
        supported_aggregations: _Optional[_Iterable[_Union[_aggregation_pb2.AggregationFunction, str]]] = ...,
    ) -> None: ...

class GetKubeEventFacetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKubeEventFacetsResponse(_message.Message):
    __slots__ = ("facets",)
    FACETS_FIELD_NUMBER: _ClassVar[int]
    facets: _containers.RepeatedCompositeFieldContainer[KubeEventFacet]
    def __init__(self, facets: _Optional[_Iterable[_Union[KubeEventFacet, _Mapping]]] = ...) -> None: ...

class GetKubeEventFacetValuesRequest(_message.Message):
    __slots__ = ("path", "start_time", "end_time", "limit", "query", "include_synthetic_rows", "facets")
    PATH_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SYNTHETIC_ROWS_FIELD_NUMBER: _ClassVar[int]
    FACETS_FIELD_NUMBER: _ClassVar[int]
    path: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    query: str
    include_synthetic_rows: bool
    facets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        path: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        query: _Optional[str] = ...,
        include_synthetic_rows: bool = ...,
        facets: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class KubeEventFacetValue(_message.Message):
    __slots__ = ("value", "count", "values")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    value: str
    count: int
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, value: _Optional[str] = ..., count: _Optional[int] = ..., values: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class GetKubeEventFacetValuesResponse(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[KubeEventFacetValue]
    def __init__(self, values: _Optional[_Iterable[_Union[KubeEventFacetValue, _Mapping]]] = ...) -> None: ...

class GetKubeEventAggregatesRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "query", "options")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    query: str
    options: _aggregation_pb2.AggregateOptions
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query: _Optional[str] = ...,
        options: _Optional[_Union[_aggregation_pb2.AggregateOptions, _Mapping]] = ...,
    ) -> None: ...

class GetKubeEventAggregatesResponse(_message.Message):
    __slots__ = ("table",)
    TABLE_FIELD_NUMBER: _ClassVar[int]
    table: _aggregation_pb2.AggregateTable
    def __init__(self, table: _Optional[_Union[_aggregation_pb2.AggregateTable, _Mapping]] = ...) -> None: ...

class ListKubeEventsAggregatedRequest(_message.Message):
    __slots__ = ("query", "start_time", "end_time", "window_period", "facets", "limit", "options")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    FACETS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    query: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    window_period: _duration_pb2.Duration
    facets: _containers.RepeatedScalarFieldContainer[str]
    limit: int
    options: _aggregation_pb2.AggregateOptions
    def __init__(
        self,
        query: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        facets: _Optional[_Iterable[str]] = ...,
        limit: _Optional[int] = ...,
        options: _Optional[_Union[_aggregation_pb2.AggregateOptions, _Mapping]] = ...,
    ) -> None: ...

class ListKubeEventsAggregatedResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...

class GetKubeEventStatRequest(_message.Message):
    __slots__ = ("query", "start_time", "end_time", "comparison_lookback_offset", "aggregation")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_LOOKBACK_OFFSET_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    query: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    comparison_lookback_offset: _duration_pb2.Duration
    aggregation: _aggregation_pb2.Aggregation
    def __init__(
        self,
        query: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        comparison_lookback_offset: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        aggregation: _Optional[_Union[_aggregation_pb2.Aggregation, _Mapping]] = ...,
    ) -> None: ...

class GetKubeEventStatResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _chart_pb2.StatisticResult
    def __init__(self, result: _Optional[_Union[_chart_pb2.StatisticResult, _Mapping]] = ...) -> None: ...
