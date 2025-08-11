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

class GetQueryPerformanceSummaryRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class GetQueryPerformanceSummaryResponse(_message.Message):
    __slots__ = ("operation_id", "performance_summary")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    performance_summary: str
    def __init__(self, operation_id: _Optional[str] = ..., performance_summary: _Optional[str] = ...) -> None: ...

class ListQueryErrorsPageToken(_message.Message):
    __slots__ = ("numeric_id_hwm", "error_timestamp_hwm")
    NUMERIC_ID_HWM_FIELD_NUMBER: _ClassVar[int]
    ERROR_TIMESTAMP_HWM_FIELD_NUMBER: _ClassVar[int]
    numeric_id_hwm: int
    error_timestamp_hwm: _timestamp_pb2.Timestamp
    def __init__(
        self,
        numeric_id_hwm: _Optional[int] = ...,
        error_timestamp_hwm: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class QueryErrorFilters(_message.Message):
    __slots__ = ("operation_id", "feature_fqn", "resolver_fqn", "query_name", "message")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    feature_fqn: str
    resolver_fqn: str
    query_name: str
    message: str
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        feature_fqn: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class QueryErrorMeta(_message.Message):
    __slots__ = (
        "id",
        "code",
        "category",
        "message",
        "display_primary_key",
        "display_primary_key_fqn",
        "feature",
        "resolver",
        "query_name",
        "exception_kind",
        "exception_message",
        "exception_stacktrace",
        "exception_internal_stacktrace",
        "operation_id",
        "deployment_id",
        "created_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PRIMARY_KEY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PRIMARY_KEY_FQN_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_KIND_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_STACKTRACE_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_INTERNAL_STACKTRACE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    code: str
    category: str
    message: str
    display_primary_key: str
    display_primary_key_fqn: str
    feature: str
    resolver: str
    query_name: str
    exception_kind: str
    exception_message: str
    exception_stacktrace: str
    exception_internal_stacktrace: str
    operation_id: str
    deployment_id: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        code: _Optional[str] = ...,
        category: _Optional[str] = ...,
        message: _Optional[str] = ...,
        display_primary_key: _Optional[str] = ...,
        display_primary_key_fqn: _Optional[str] = ...,
        feature: _Optional[str] = ...,
        resolver: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        exception_kind: _Optional[str] = ...,
        exception_message: _Optional[str] = ...,
        exception_stacktrace: _Optional[str] = ...,
        exception_internal_stacktrace: _Optional[str] = ...,
        operation_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListQueryErrorsRequest(_message.Message):
    __slots__ = ("start_date", "end_date", "filters", "page_size", "page_token")
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    filters: QueryErrorFilters
    page_size: int
    page_token: str
    def __init__(
        self,
        start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        filters: _Optional[_Union[QueryErrorFilters, _Mapping]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class ListQueryErrorsResponse(_message.Message):
    __slots__ = ("query_errors", "next_page_token")
    QUERY_ERRORS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query_errors: _containers.RepeatedCompositeFieldContainer[QueryErrorMeta]
    next_page_token: str
    def __init__(
        self,
        query_errors: _Optional[_Iterable[_Union[QueryErrorMeta, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class GetQueryErrorsChartRequest(_message.Message):
    __slots__ = ("start_timestamp_inclusive", "end_timestamp_exclusive", "window_period", "filters")
    START_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    start_timestamp_inclusive: _timestamp_pb2.Timestamp
    end_timestamp_exclusive: _timestamp_pb2.Timestamp
    window_period: _duration_pb2.Duration
    filters: QueryErrorFilters
    def __init__(
        self,
        start_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        filters: _Optional[_Union[QueryErrorFilters, _Mapping]] = ...,
    ) -> None: ...

class GetQueryErrorsChartResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...

class GetQueryPlanRequest(_message.Message):
    __slots__ = ("query_plan_id",)
    QUERY_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    query_plan_id: str
    def __init__(self, query_plan_id: _Optional[str] = ...) -> None: ...

class QueryPlan(_message.Message):
    __slots__ = ("id", "environment_id", "deployment_id", "query_plan", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    deployment_id: str
    query_plan: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        query_plan: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetQueryPlanResponse(_message.Message):
    __slots__ = ("query_plan",)
    QUERY_PLAN_FIELD_NUMBER: _ClassVar[int]
    query_plan: QueryPlan
    def __init__(self, query_plan: _Optional[_Union[QueryPlan, _Mapping]] = ...) -> None: ...

class AggregatedQueryError(_message.Message):
    __slots__ = ("sample_error", "count", "first_seen", "last_seen")
    SAMPLE_ERROR_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FIRST_SEEN_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    sample_error: QueryErrorMeta
    count: int
    first_seen: _timestamp_pb2.Timestamp
    last_seen: _timestamp_pb2.Timestamp
    def __init__(
        self,
        sample_error: _Optional[_Union[QueryErrorMeta, _Mapping]] = ...,
        count: _Optional[int] = ...,
        first_seen: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_seen: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class AggregateQueryErrorsRequest(_message.Message):
    __slots__ = ("start_date", "end_date", "filters", "page_size", "page_token")
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    filters: QueryErrorFilters
    page_size: int
    page_token: str
    def __init__(
        self,
        start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        filters: _Optional[_Union[QueryErrorFilters, _Mapping]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class AggregateQueryErrorsResponse(_message.Message):
    __slots__ = ("aggregated_errors", "next_page_token")
    AGGREGATED_ERRORS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    aggregated_errors: _containers.RepeatedCompositeFieldContainer[AggregatedQueryError]
    next_page_token: str
    def __init__(
        self,
        aggregated_errors: _Optional[_Iterable[_Union[AggregatedQueryError, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class MetaQueryRun(_message.Message):
    __slots__ = (
        "id",
        "meta_query_id",
        "external_id",
        "created_at",
        "query_plan_id",
        "correlation_id",
        "has_errors",
        "agent_id",
        "branch_name",
        "deployment_id",
        "has_plan_stages",
        "duration",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    META_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    HAS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    HAS_PLAN_STAGES_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    meta_query_id: str
    external_id: str
    created_at: _timestamp_pb2.Timestamp
    query_plan_id: str
    correlation_id: str
    has_errors: bool
    agent_id: str
    branch_name: str
    deployment_id: str
    has_plan_stages: bool
    duration: float
    def __init__(
        self,
        id: _Optional[str] = ...,
        meta_query_id: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_plan_id: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        has_errors: bool = ...,
        agent_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        has_plan_stages: bool = ...,
        duration: _Optional[float] = ...,
    ) -> None: ...

class MetaQueryRunWithMeta(_message.Message):
    __slots__ = ("id", "run", "latency")
    ID_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    id: str
    run: MetaQueryRun
    latency: float
    def __init__(
        self,
        id: _Optional[str] = ...,
        run: _Optional[_Union[MetaQueryRun, _Mapping]] = ...,
        latency: _Optional[float] = ...,
    ) -> None: ...

class ListMetaQueryRunsRequest(_message.Message):
    __slots__ = (
        "include_latency",
        "min_latency_ms",
        "query_plan_id",
        "meta_query_id",
        "meta_query_name",
        "id_filter",
        "branch_filter",
        "agent_id",
        "root_ns_pkey",
        "cursor",
        "limit",
        "start",
        "end",
        "has_errors",
    )
    INCLUDE_LATENCY_FIELD_NUMBER: _ClassVar[int]
    MIN_LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    META_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    META_QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FILTER_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    ROOT_NS_PKEY_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    HAS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    include_latency: bool
    min_latency_ms: float
    query_plan_id: str
    meta_query_id: int
    meta_query_name: str
    id_filter: str
    branch_filter: str
    agent_id: str
    root_ns_pkey: str
    cursor: _timestamp_pb2.Timestamp
    limit: int
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    has_errors: bool
    def __init__(
        self,
        include_latency: bool = ...,
        min_latency_ms: _Optional[float] = ...,
        query_plan_id: _Optional[str] = ...,
        meta_query_id: _Optional[int] = ...,
        meta_query_name: _Optional[str] = ...,
        id_filter: _Optional[str] = ...,
        branch_filter: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        root_ns_pkey: _Optional[str] = ...,
        cursor: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        has_errors: bool = ...,
    ) -> None: ...

class ListMetaQueryRunsResponse(_message.Message):
    __slots__ = ("query_runs",)
    QUERY_RUNS_FIELD_NUMBER: _ClassVar[int]
    query_runs: _containers.RepeatedCompositeFieldContainer[MetaQueryRunWithMeta]
    def __init__(self, query_runs: _Optional[_Iterable[_Union[MetaQueryRunWithMeta, _Mapping]]] = ...) -> None: ...

class MetaQuery(_message.Message):
    __slots__ = (
        "id",
        "query_name",
        "input_features",
        "output_features",
        "output_root_fqns",
        "query_features_count",
        "query_resolvers",
        "owner",
        "tags",
        "last_observed_at",
        "created_at",
        "archived_at",
        "query_hash",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ROOT_FQNS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FEATURES_COUNT_FIELD_NUMBER: _ClassVar[int]
    QUERY_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LAST_OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    QUERY_HASH_FIELD_NUMBER: _ClassVar[int]
    id: str
    query_name: str
    input_features: _containers.RepeatedScalarFieldContainer[str]
    output_features: _containers.RepeatedScalarFieldContainer[str]
    output_root_fqns: _containers.RepeatedScalarFieldContainer[str]
    query_features_count: int
    query_resolvers: _containers.RepeatedScalarFieldContainer[str]
    owner: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    last_observed_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    archived_at: _timestamp_pb2.Timestamp
    query_hash: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        input_features: _Optional[_Iterable[str]] = ...,
        output_features: _Optional[_Iterable[str]] = ...,
        output_root_fqns: _Optional[_Iterable[str]] = ...,
        query_features_count: _Optional[int] = ...,
        query_resolvers: _Optional[_Iterable[str]] = ...,
        owner: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        last_observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_hash: _Optional[str] = ...,
    ) -> None: ...

class ListMetaQueriesRequest(_message.Message):
    __slots__ = ("name_filter", "start", "end", "has_name", "cursor", "limit")
    NAME_FILTER_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    HAS_NAME_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    name_filter: str
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    has_name: bool
    cursor: _timestamp_pb2.Timestamp
    limit: int
    def __init__(
        self,
        name_filter: _Optional[str] = ...,
        start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        has_name: bool = ...,
        cursor: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListMetaQueriesResponse(_message.Message):
    __slots__ = ("meta_queries",)
    META_QUERIES_FIELD_NUMBER: _ClassVar[int]
    meta_queries: _containers.RepeatedCompositeFieldContainer[MetaQuery]
    def __init__(self, meta_queries: _Optional[_Iterable[_Union[MetaQuery, _Mapping]]] = ...) -> None: ...

class ListLatestMetaQueriesRequest(_message.Message):
    __slots__ = ("has_name",)
    HAS_NAME_FIELD_NUMBER: _ClassVar[int]
    has_name: bool
    def __init__(self, has_name: bool = ...) -> None: ...

class ListLatestMetaQueriesResponse(_message.Message):
    __slots__ = ("meta_queries",)
    META_QUERIES_FIELD_NUMBER: _ClassVar[int]
    meta_queries: _containers.RepeatedCompositeFieldContainer[MetaQuery]
    def __init__(self, meta_queries: _Optional[_Iterable[_Union[MetaQuery, _Mapping]]] = ...) -> None: ...

class GetMetaQueryRequest(_message.Message):
    __slots__ = ("meta_query_id",)
    META_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    meta_query_id: str
    def __init__(self, meta_query_id: _Optional[str] = ...) -> None: ...

class GetMetaQueryResponse(_message.Message):
    __slots__ = ("meta_query",)
    META_QUERY_FIELD_NUMBER: _ClassVar[int]
    meta_query: MetaQuery
    def __init__(self, meta_query: _Optional[_Union[MetaQuery, _Mapping]] = ...) -> None: ...

class GetMetaQueryByNameRequest(_message.Message):
    __slots__ = ("meta_query_name",)
    META_QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    meta_query_name: str
    def __init__(self, meta_query_name: _Optional[str] = ...) -> None: ...

class GetMetaQueryByNameResponse(_message.Message):
    __slots__ = ("meta_query",)
    META_QUERY_FIELD_NUMBER: _ClassVar[int]
    meta_query: MetaQuery
    def __init__(self, meta_query: _Optional[_Union[MetaQuery, _Mapping]] = ...) -> None: ...

class ListMetaQueriesByIdsRequest(_message.Message):
    __slots__ = ("meta_query_ids",)
    META_QUERY_IDS_FIELD_NUMBER: _ClassVar[int]
    meta_query_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, meta_query_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListMetaQueriesByIdsResponse(_message.Message):
    __slots__ = ("meta_queries",)
    META_QUERIES_FIELD_NUMBER: _ClassVar[int]
    meta_queries: _containers.RepeatedCompositeFieldContainer[MetaQuery]
    def __init__(self, meta_queries: _Optional[_Iterable[_Union[MetaQuery, _Mapping]]] = ...) -> None: ...

class ListArchivedMetaQueriesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListArchivedMetaQueriesResponse(_message.Message):
    __slots__ = ("meta_queries",)
    META_QUERIES_FIELD_NUMBER: _ClassVar[int]
    meta_queries: _containers.RepeatedCompositeFieldContainer[MetaQuery]
    def __init__(self, meta_queries: _Optional[_Iterable[_Union[MetaQuery, _Mapping]]] = ...) -> None: ...

class ListMetaQueriesForResolverRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class ListMetaQueriesForResolverResponse(_message.Message):
    __slots__ = ("meta_queries",)
    META_QUERIES_FIELD_NUMBER: _ClassVar[int]
    meta_queries: _containers.RepeatedCompositeFieldContainer[MetaQuery]
    def __init__(self, meta_queries: _Optional[_Iterable[_Union[MetaQuery, _Mapping]]] = ...) -> None: ...

class ListMetaQueriesForFeatureRequest(_message.Message):
    __slots__ = ("feature_fqn",)
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    def __init__(self, feature_fqn: _Optional[str] = ...) -> None: ...

class ListMetaQueriesForFeatureResponse(_message.Message):
    __slots__ = ("meta_queries",)
    META_QUERIES_FIELD_NUMBER: _ClassVar[int]
    meta_queries: _containers.RepeatedCompositeFieldContainer[MetaQuery]
    def __init__(self, meta_queries: _Optional[_Iterable[_Union[MetaQuery, _Mapping]]] = ...) -> None: ...

class ListMetaQueryVersionsRequest(_message.Message):
    __slots__ = ("meta_query_name", "cursor", "limit")
    META_QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    meta_query_name: str
    cursor: _timestamp_pb2.Timestamp
    limit: int
    def __init__(
        self,
        meta_query_name: _Optional[str] = ...,
        cursor: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListMetaQueryVersionsResponse(_message.Message):
    __slots__ = ("meta_query_versions",)
    META_QUERY_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    meta_query_versions: _containers.RepeatedCompositeFieldContainer[MetaQuery]
    def __init__(self, meta_query_versions: _Optional[_Iterable[_Union[MetaQuery, _Mapping]]] = ...) -> None: ...
