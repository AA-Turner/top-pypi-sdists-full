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
    __slots__ = ("operation_id", "feature_fqn", "resolver_fqn", "query_name")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    feature_fqn: str
    resolver_fqn: str
    query_name: str
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        feature_fqn: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
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
