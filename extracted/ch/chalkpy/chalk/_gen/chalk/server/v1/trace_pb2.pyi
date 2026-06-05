from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
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

class ChalkStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHALK_STATUS_CODE_UNSPECIFIED: _ClassVar[ChalkStatusCode]
    CHALK_STATUS_CODE_OK: _ClassVar[ChalkStatusCode]
    CHALK_STATUS_CODE_ERROR: _ClassVar[ChalkStatusCode]

class ChalkSpanKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHALK_SPAN_KIND_UNSPECIFIED: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_SERVER: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_CLIENT: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_PRODUCER: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_CONSUMER: _ClassVar[ChalkSpanKind]
    CHALK_SPAN_KIND_INTERNAL: _ClassVar[ChalkSpanKind]

CHALK_STATUS_CODE_UNSPECIFIED: ChalkStatusCode
CHALK_STATUS_CODE_OK: ChalkStatusCode
CHALK_STATUS_CODE_ERROR: ChalkStatusCode
CHALK_SPAN_KIND_UNSPECIFIED: ChalkSpanKind
CHALK_SPAN_KIND_SERVER: ChalkSpanKind
CHALK_SPAN_KIND_CLIENT: ChalkSpanKind
CHALK_SPAN_KIND_PRODUCER: ChalkSpanKind
CHALK_SPAN_KIND_CONSUMER: ChalkSpanKind
CHALK_SPAN_KIND_INTERNAL: ChalkSpanKind

class ChalkSpan(_message.Message):
    __slots__ = (
        "span_id",
        "trace_id",
        "parent_span_id",
        "operation_name",
        "start_time",
        "end_time",
        "duration",
        "status",
        "attributes",
        "events",
        "links",
        "kind",
        "resource_attributes",
    )
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class ResourceAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    span_id: str
    trace_id: str
    parent_span_id: str
    operation_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    status: ChalkSpanStatus
    attributes: _containers.ScalarMap[str, str]
    events: _containers.RepeatedCompositeFieldContainer[ChalkSpanEvent]
    links: _containers.RepeatedCompositeFieldContainer[ChalkSpanLink]
    kind: ChalkSpanKind
    resource_attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        span_id: _Optional[str] = ...,
        trace_id: _Optional[str] = ...,
        parent_span_id: _Optional[str] = ...,
        operation_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        status: _Optional[_Union[ChalkSpanStatus, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
        events: _Optional[_Iterable[_Union[ChalkSpanEvent, _Mapping]]] = ...,
        links: _Optional[_Iterable[_Union[ChalkSpanLink, _Mapping]]] = ...,
        kind: _Optional[_Union[ChalkSpanKind, str]] = ...,
        resource_attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ChalkSpanStatus(_message.Message):
    __slots__ = ("code", "description")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    code: ChalkStatusCode
    description: str
    def __init__(
        self, code: _Optional[_Union[ChalkStatusCode, str]] = ..., description: _Optional[str] = ...
    ) -> None: ...

class ChalkSpanEvent(_message.Message):
    __slots__ = ("name", "timestamp", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    name: str
    timestamp: _timestamp_pb2.Timestamp
    attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ChalkSpanLink(_message.Message):
    __slots__ = ("trace_id", "span_id", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    span_id: str
    attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        trace_id: _Optional[str] = ...,
        span_id: _Optional[str] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ChalkTrace(_message.Message):
    __slots__ = ("trace_id", "spans", "root_span_id", "service_name", "resource_attributes")
    class ResourceAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    spans: _containers.RepeatedCompositeFieldContainer[ChalkSpan]
    root_span_id: str
    service_name: str
    resource_attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        trace_id: _Optional[str] = ...,
        spans: _Optional[_Iterable[_Union[ChalkSpan, _Mapping]]] = ...,
        root_span_id: _Optional[str] = ...,
        service_name: _Optional[str] = ...,
        resource_attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ChalkTraceSummaryRootSpan(_message.Message):
    __slots__ = ("span_id", "attributes", "resource_attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class ResourceAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    span_id: str
    attributes: _containers.ScalarMap[str, str]
    resource_attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        span_id: _Optional[str] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
        resource_attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ChalkTraceSummary(_message.Message):
    __slots__ = ("trace_id", "start_time", "end_time", "duration", "root_spans")
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPANS_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    root_spans: _containers.RepeatedCompositeFieldContainer[ChalkTraceSummaryRootSpan]
    def __init__(
        self,
        trace_id: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        root_spans: _Optional[_Iterable[_Union[ChalkTraceSummaryRootSpan, _Mapping]]] = ...,
    ) -> None: ...

class TraceCallGraphAiInfo(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    def __init__(
        self,
        prompt_tokens: _Optional[int] = ...,
        completion_tokens: _Optional[int] = ...,
        total_tokens: _Optional[int] = ...,
    ) -> None: ...

class TraceCallGraphDatabaseInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TraceCallGraphOperationInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TraceCallGraphRemoteFunctionInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TraceCallGraphServiceInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TraceCallGraphNode(_message.Message):
    __slots__ = (
        "id",
        "label",
        "category_label",
        "span_count",
        "trace_count",
        "error_count",
        "total_duration_us",
        "duration_share",
        "ai",
        "database",
        "operation",
        "remote_function",
        "service",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_LABEL_FIELD_NUMBER: _ClassVar[int]
    SPAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRACE_COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_US_FIELD_NUMBER: _ClassVar[int]
    DURATION_SHARE_FIELD_NUMBER: _ClassVar[int]
    AI_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    REMOTE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    id: str
    label: str
    category_label: str
    span_count: int
    trace_count: int
    error_count: int
    total_duration_us: int
    duration_share: float
    ai: TraceCallGraphAiInfo
    database: TraceCallGraphDatabaseInfo
    operation: TraceCallGraphOperationInfo
    remote_function: TraceCallGraphRemoteFunctionInfo
    service: TraceCallGraphServiceInfo
    def __init__(
        self,
        id: _Optional[str] = ...,
        label: _Optional[str] = ...,
        category_label: _Optional[str] = ...,
        span_count: _Optional[int] = ...,
        trace_count: _Optional[int] = ...,
        error_count: _Optional[int] = ...,
        total_duration_us: _Optional[int] = ...,
        duration_share: _Optional[float] = ...,
        ai: _Optional[_Union[TraceCallGraphAiInfo, _Mapping]] = ...,
        database: _Optional[_Union[TraceCallGraphDatabaseInfo, _Mapping]] = ...,
        operation: _Optional[_Union[TraceCallGraphOperationInfo, _Mapping]] = ...,
        remote_function: _Optional[_Union[TraceCallGraphRemoteFunctionInfo, _Mapping]] = ...,
        service: _Optional[_Union[TraceCallGraphServiceInfo, _Mapping]] = ...,
    ) -> None: ...

class TraceCallGraphEdge(_message.Message):
    __slots__ = (
        "id",
        "source_id",
        "target_id",
        "span_count",
        "trace_count",
        "error_count",
        "total_duration_us",
        "duration_share",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    SPAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRACE_COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_US_FIELD_NUMBER: _ClassVar[int]
    DURATION_SHARE_FIELD_NUMBER: _ClassVar[int]
    id: str
    source_id: str
    target_id: str
    span_count: int
    trace_count: int
    error_count: int
    total_duration_us: int
    duration_share: float
    def __init__(
        self,
        id: _Optional[str] = ...,
        source_id: _Optional[str] = ...,
        target_id: _Optional[str] = ...,
        span_count: _Optional[int] = ...,
        trace_count: _Optional[int] = ...,
        error_count: _Optional[int] = ...,
        total_duration_us: _Optional[int] = ...,
        duration_share: _Optional[float] = ...,
    ) -> None: ...

class TraceCallGraph(_message.Message):
    __slots__ = ("nodes", "edges", "matched_span_count", "matched_trace_count", "total_duration_us")
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    MATCHED_SPAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MATCHED_TRACE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_US_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[TraceCallGraphNode]
    edges: _containers.RepeatedCompositeFieldContainer[TraceCallGraphEdge]
    matched_span_count: int
    matched_trace_count: int
    total_duration_us: int
    def __init__(
        self,
        nodes: _Optional[_Iterable[_Union[TraceCallGraphNode, _Mapping]]] = ...,
        edges: _Optional[_Iterable[_Union[TraceCallGraphEdge, _Mapping]]] = ...,
        matched_span_count: _Optional[int] = ...,
        matched_trace_count: _Optional[int] = ...,
        total_duration_us: _Optional[int] = ...,
    ) -> None: ...

class GetTraceRequest(_message.Message):
    __slots__ = ("operation_id", "trace_id")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    trace_id: str
    def __init__(self, operation_id: _Optional[str] = ..., trace_id: _Optional[str] = ...) -> None: ...

class GetTraceResponse(_message.Message):
    __slots__ = ("trace",)
    TRACE_FIELD_NUMBER: _ClassVar[int]
    trace: ChalkTrace
    def __init__(self, trace: _Optional[_Union[ChalkTrace, _Mapping]] = ...) -> None: ...

class ListTraceRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "limit", "service_name", "span_name", "page_token")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SPAN_NAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    service_name: str
    span_name: str
    page_token: str
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        service_name: _Optional[str] = ...,
        span_name: _Optional[str] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class ListTraceResponse(_message.Message):
    __slots__ = ("traces", "next_page_token")
    TRACES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    traces: _containers.RepeatedCompositeFieldContainer[ChalkTrace]
    next_page_token: str
    def __init__(
        self, traces: _Optional[_Iterable[_Union[ChalkTrace, _Mapping]]] = ..., next_page_token: _Optional[str] = ...
    ) -> None: ...

class SearchTraceSummariesRequest(_message.Message):
    __slots__ = (
        "start_time",
        "end_time",
        "limit",
        "page_token",
        "trace_ids",
        "min_duration_us",
        "max_duration_us",
        "root_span_ids",
        "root_span_attribute_filters",
        "root_span_resource_attribute_filters",
        "root_span_attribute_values",
        "root_span_resource_attribute_values",
    )
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TRACE_IDS_FIELD_NUMBER: _ClassVar[int]
    MIN_DURATION_US_FIELD_NUMBER: _ClassVar[int]
    MAX_DURATION_US_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPAN_IDS_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPAN_ATTRIBUTE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPAN_RESOURCE_ATTRIBUTE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPAN_ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    ROOT_SPAN_RESOURCE_ATTRIBUTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    page_token: str
    trace_ids: _containers.RepeatedScalarFieldContainer[str]
    min_duration_us: int
    max_duration_us: int
    root_span_ids: _containers.RepeatedScalarFieldContainer[str]
    root_span_attribute_filters: _containers.RepeatedCompositeFieldContainer[AttributeFilter]
    root_span_resource_attribute_filters: _containers.RepeatedCompositeFieldContainer[AttributeFilter]
    root_span_attribute_values: _containers.RepeatedScalarFieldContainer[str]
    root_span_resource_attribute_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
        trace_ids: _Optional[_Iterable[str]] = ...,
        min_duration_us: _Optional[int] = ...,
        max_duration_us: _Optional[int] = ...,
        root_span_ids: _Optional[_Iterable[str]] = ...,
        root_span_attribute_filters: _Optional[_Iterable[_Union[AttributeFilter, _Mapping]]] = ...,
        root_span_resource_attribute_filters: _Optional[_Iterable[_Union[AttributeFilter, _Mapping]]] = ...,
        root_span_attribute_values: _Optional[_Iterable[str]] = ...,
        root_span_resource_attribute_values: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class SearchTraceSummariesResponse(_message.Message):
    __slots__ = ("trace_summaries", "next_page_token")
    TRACE_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    trace_summaries: _containers.RepeatedCompositeFieldContainer[ChalkTraceSummary]
    next_page_token: str
    def __init__(
        self,
        trace_summaries: _Optional[_Iterable[_Union[ChalkTraceSummary, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class GetTraceCallGraphRequest(_message.Message):
    __slots__ = (
        "start_time",
        "end_time",
        "limit",
        "function_name",
        "attribute_filters",
        "resource_attribute_filters",
        "cursor",
    )
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    function_name: str
    attribute_filters: _containers.RepeatedCompositeFieldContainer[AttributeFilter]
    resource_attribute_filters: _containers.RepeatedCompositeFieldContainer[AttributeFilter]
    cursor: str
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        function_name: _Optional[str] = ...,
        attribute_filters: _Optional[_Iterable[_Union[AttributeFilter, _Mapping]]] = ...,
        resource_attribute_filters: _Optional[_Iterable[_Union[AttributeFilter, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
    ) -> None: ...

class GetTraceCallGraphResponse(_message.Message):
    __slots__ = ("call_graph", "next_cursor")
    CALL_GRAPH_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    call_graph: TraceCallGraph
    next_cursor: str
    def __init__(
        self, call_graph: _Optional[_Union[TraceCallGraph, _Mapping]] = ..., next_cursor: _Optional[str] = ...
    ) -> None: ...

class GetSpanRequest(_message.Message):
    __slots__ = ("span_id", "trace_id")
    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    span_id: str
    trace_id: str
    def __init__(self, span_id: _Optional[str] = ..., trace_id: _Optional[str] = ...) -> None: ...

class GetSpanResponse(_message.Message):
    __slots__ = ("span",)
    SPAN_FIELD_NUMBER: _ClassVar[int]
    span: ChalkSpan
    def __init__(self, span: _Optional[_Union[ChalkSpan, _Mapping]] = ...) -> None: ...

class AttributeFilter(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ListSpanRequest(_message.Message):
    __slots__ = (
        "trace_id",
        "start_time",
        "end_time",
        "limit",
        "page_token",
        "parent_span_id",
        "operation_name",
        "service_name",
        "status_code",
        "min_duration_us",
        "max_duration_us",
        "attribute_filters",
        "span_kind",
        "resource_attribute_filters",
    )
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PARENT_SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    MIN_DURATION_US_FIELD_NUMBER: _ClassVar[int]
    MAX_DURATION_US_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    SPAN_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ATTRIBUTE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    page_token: str
    parent_span_id: str
    operation_name: str
    service_name: str
    status_code: ChalkStatusCode
    min_duration_us: int
    max_duration_us: int
    attribute_filters: _containers.RepeatedCompositeFieldContainer[AttributeFilter]
    span_kind: ChalkSpanKind
    resource_attribute_filters: _containers.RepeatedCompositeFieldContainer[AttributeFilter]
    def __init__(
        self,
        trace_id: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
        parent_span_id: _Optional[str] = ...,
        operation_name: _Optional[str] = ...,
        service_name: _Optional[str] = ...,
        status_code: _Optional[_Union[ChalkStatusCode, str]] = ...,
        min_duration_us: _Optional[int] = ...,
        max_duration_us: _Optional[int] = ...,
        attribute_filters: _Optional[_Iterable[_Union[AttributeFilter, _Mapping]]] = ...,
        span_kind: _Optional[_Union[ChalkSpanKind, str]] = ...,
        resource_attribute_filters: _Optional[_Iterable[_Union[AttributeFilter, _Mapping]]] = ...,
    ) -> None: ...

class ListSpanResponse(_message.Message):
    __slots__ = ("spans", "next_page_token")
    SPANS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    spans: _containers.RepeatedCompositeFieldContainer[ChalkSpan]
    next_page_token: str
    def __init__(
        self, spans: _Optional[_Iterable[_Union[ChalkSpan, _Mapping]]] = ..., next_page_token: _Optional[str] = ...
    ) -> None: ...

class SpanFacet(_message.Message):
    __slots__ = ("path", "name")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetSpanFacetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSpanFacetsResponse(_message.Message):
    __slots__ = ("facets",)
    FACETS_FIELD_NUMBER: _ClassVar[int]
    facets: _containers.RepeatedCompositeFieldContainer[SpanFacet]
    def __init__(self, facets: _Optional[_Iterable[_Union[SpanFacet, _Mapping]]] = ...) -> None: ...

class GetSpanFacetValuesRequest(_message.Message):
    __slots__ = ("path", "start_time", "end_time", "limit")
    PATH_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    path: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    def __init__(
        self,
        path: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class SpanFacetValue(_message.Message):
    __slots__ = ("value", "count")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    value: str
    count: int
    def __init__(self, value: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetSpanFacetValuesResponse(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[SpanFacetValue]
    def __init__(self, values: _Optional[_Iterable[_Union[SpanFacetValue, _Mapping]]] = ...) -> None: ...

class ListSpanAggregatedRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "window_period", "operation_name", "service_name")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    OPERATION_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    window_period: _duration_pb2.Duration
    operation_name: str
    service_name: str
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        operation_name: _Optional[str] = ...,
        service_name: _Optional[str] = ...,
    ) -> None: ...

class ListSpanAggregatedResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...

class SpanSourceAggregate(_message.Message):
    __slots__ = ("service_name", "resource_group", "span_count", "error_count", "ok_count")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    SPAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_COUNT_FIELD_NUMBER: _ClassVar[int]
    OK_COUNT_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    resource_group: str
    span_count: int
    error_count: int
    ok_count: int
    def __init__(
        self,
        service_name: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        span_count: _Optional[int] = ...,
        error_count: _Optional[int] = ...,
        ok_count: _Optional[int] = ...,
    ) -> None: ...

class GetSpanSourceAggregatesRequest(_message.Message):
    __slots__ = ("start_time", "end_time")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetSpanSourceAggregatesResponse(_message.Message):
    __slots__ = ("aggregates",)
    AGGREGATES_FIELD_NUMBER: _ClassVar[int]
    aggregates: _containers.RepeatedCompositeFieldContainer[SpanSourceAggregate]
    def __init__(self, aggregates: _Optional[_Iterable[_Union[SpanSourceAggregate, _Mapping]]] = ...) -> None: ...
