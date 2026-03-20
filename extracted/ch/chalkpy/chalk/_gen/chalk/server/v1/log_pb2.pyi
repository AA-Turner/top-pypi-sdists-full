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

class LogFacetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOG_FACET_TYPE_UNSPECIFIED: _ClassVar[LogFacetType]
    LOG_FACET_TYPE_LIST: _ClassVar[LogFacetType]
    LOG_FACET_TYPE_RANGE: _ClassVar[LogFacetType]

LOG_FACET_TYPE_UNSPECIFIED: LogFacetType
LOG_FACET_TYPE_LIST: LogFacetType
LOG_FACET_TYPE_RANGE: LogFacetType

class LogEntry(_message.Message):
    __slots__ = (
        "id",
        "severity",
        "timestamp",
        "message",
        "function_name",
        "operation_id",
        "logger_name",
        "agent_id",
        "operation_producer",
        "is_user_logger",
        "labels",
    )
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    LOGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_PRODUCER_FIELD_NUMBER: _ClassVar[int]
    IS_USER_LOGGER_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    id: str
    severity: str
    timestamp: _timestamp_pb2.Timestamp
    message: str
    function_name: str
    operation_id: str
    logger_name: str
    agent_id: str
    operation_producer: str
    is_user_logger: bool
    labels: _containers.ScalarMap[str, str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        severity: _Optional[str] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        message: _Optional[str] = ...,
        function_name: _Optional[str] = ...,
        operation_id: _Optional[str] = ...,
        logger_name: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        operation_producer: _Optional[str] = ...,
        is_user_logger: bool = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class AccessLogEntry(_message.Message):
    __slots__ = (
        "timestamp",
        "trace_id",
        "authority",
        "duration",
        "start_time",
        "upstream_host",
        "downstream_remote_address",
        "environment_id",
        "path",
        "response_code",
        "grpc_status_number",
        "grpc_status",
        "attributes",
    )
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    UPSTREAM_HOST_FIELD_NUMBER: _ClassVar[int]
    DOWNSTREAM_REMOTE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CODE_FIELD_NUMBER: _ClassVar[int]
    GRPC_STATUS_NUMBER_FIELD_NUMBER: _ClassVar[int]
    GRPC_STATUS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    trace_id: str
    authority: str
    duration: int
    start_time: _timestamp_pb2.Timestamp
    upstream_host: str
    downstream_remote_address: str
    environment_id: str
    path: str
    response_code: str
    grpc_status_number: int
    grpc_status: str
    attributes: _containers.ScalarMap[str, str]
    def __init__(
        self,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        trace_id: _Optional[str] = ...,
        authority: _Optional[str] = ...,
        duration: _Optional[int] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upstream_host: _Optional[str] = ...,
        downstream_remote_address: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        path: _Optional[str] = ...,
        response_code: _Optional[str] = ...,
        grpc_status_number: _Optional[int] = ...,
        grpc_status: _Optional[str] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class SearchLogEntriesPageToken(_message.Message):
    __slots__ = ("next_page_token",)
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    def __init__(self, next_page_token: _Optional[str] = ...) -> None: ...

class SearchAccessLogEntriesPageToken(_message.Message):
    __slots__ = ("next_page_token",)
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    def __init__(self, next_page_token: _Optional[str] = ...) -> None: ...

class SearchLogEntriesRequest(_message.Message):
    __slots__ = ("query", "page_token", "start_time", "end_time")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_token: SearchLogEntriesPageToken
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        query: _Optional[str] = ...,
        page_token: _Optional[_Union[SearchLogEntriesPageToken, _Mapping]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SearchLogEntriesResponse(_message.Message):
    __slots__ = ("log_entries", "next_page_token", "logging_client")
    LOG_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    LOGGING_CLIENT_FIELD_NUMBER: _ClassVar[int]
    log_entries: _containers.RepeatedCompositeFieldContainer[LogEntry]
    next_page_token: SearchLogEntriesPageToken
    logging_client: str
    def __init__(
        self,
        log_entries: _Optional[_Iterable[_Union[LogEntry, _Mapping]]] = ...,
        next_page_token: _Optional[_Union[SearchLogEntriesPageToken, _Mapping]] = ...,
        logging_client: _Optional[str] = ...,
    ) -> None: ...

class SearchAccessLogEntriesRequest(_message.Message):
    __slots__ = ("query", "page_token", "start_time", "end_time")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_token: SearchAccessLogEntriesPageToken
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        query: _Optional[str] = ...,
        page_token: _Optional[_Union[SearchAccessLogEntriesPageToken, _Mapping]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SearchAccessLogEntriesResponse(_message.Message):
    __slots__ = ("access_log_entries", "next_page_token")
    ACCESS_LOG_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_log_entries: _containers.RepeatedCompositeFieldContainer[AccessLogEntry]
    next_page_token: SearchAccessLogEntriesPageToken
    def __init__(
        self,
        access_log_entries: _Optional[_Iterable[_Union[AccessLogEntry, _Mapping]]] = ...,
        next_page_token: _Optional[_Union[SearchAccessLogEntriesPageToken, _Mapping]] = ...,
    ) -> None: ...

class SearchLogEntriesAggregatedRequest(_message.Message):
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

class SearchLogEntriesAggregatedResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...

class GetLogFacetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LogFacet(_message.Message):
    __slots__ = ("path", "name", "facet_type")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FACET_TYPE_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    facet_type: LogFacetType
    def __init__(
        self,
        path: _Optional[str] = ...,
        name: _Optional[str] = ...,
        facet_type: _Optional[_Union[LogFacetType, str]] = ...,
    ) -> None: ...

class GetLogFacetsResponse(_message.Message):
    __slots__ = ("facets",)
    FACETS_FIELD_NUMBER: _ClassVar[int]
    facets: _containers.RepeatedCompositeFieldContainer[LogFacet]
    def __init__(self, facets: _Optional[_Iterable[_Union[LogFacet, _Mapping]]] = ...) -> None: ...

class GetLogFacetValuesRequest(_message.Message):
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

class LogFacetValue(_message.Message):
    __slots__ = ("value", "count")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    value: str
    count: int
    def __init__(self, value: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetLogFacetValuesResponse(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[LogFacetValue]
    def __init__(self, values: _Optional[_Iterable[_Union[LogFacetValue, _Mapping]]] = ...) -> None: ...

class SearchAccessLogEntriesAggregatedRequest(_message.Message):
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

class SearchAccessLogEntriesAggregatedResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...

class GetAccessLogFacetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAccessLogFacetsResponse(_message.Message):
    __slots__ = ("facets",)
    FACETS_FIELD_NUMBER: _ClassVar[int]
    facets: _containers.RepeatedCompositeFieldContainer[LogFacet]
    def __init__(self, facets: _Optional[_Iterable[_Union[LogFacet, _Mapping]]] = ...) -> None: ...

class GetAccessLogFacetValuesRequest(_message.Message):
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

class GetAccessLogFacetValuesResponse(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[LogFacetValue]
    def __init__(self, values: _Optional[_Iterable[_Union[LogFacetValue, _Mapping]]] = ...) -> None: ...
