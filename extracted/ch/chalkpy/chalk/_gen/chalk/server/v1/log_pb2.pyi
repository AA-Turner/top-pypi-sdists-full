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

class SearchLogEntriesPageToken(_message.Message):
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
