from google.protobuf import timestamp_pb2 as _timestamp_pb2
from seltz_public_api.proto.v1 import seltz_pb2 as _seltz_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitorStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MONITOR_STATUS_UNSPECIFIED: _ClassVar[MonitorStatus]
    MONITOR_STATUS_ACTIVE: _ClassVar[MonitorStatus]
    MONITOR_STATUS_PAUSED: _ClassVar[MonitorStatus]
    MONITOR_STATUS_DISABLED: _ClassVar[MonitorStatus]
    MONITOR_STATUS_DELETED: _ClassVar[MonitorStatus]

class RunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUN_STATUS_UNSPECIFIED: _ClassVar[RunStatus]
    RUN_STATUS_COMPLETED: _ClassVar[RunStatus]
    RUN_STATUS_PARTIAL: _ClassVar[RunStatus]
    RUN_STATUS_FAILED: _ClassVar[RunStatus]
    RUN_STATUS_SKIPPED: _ClassVar[RunStatus]

class WebhookStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WEBHOOK_STATUS_UNSPECIFIED: _ClassVar[WebhookStatus]
    WEBHOOK_STATUS_ACTIVE: _ClassVar[WebhookStatus]
    WEBHOOK_STATUS_DISABLED: _ClassVar[WebhookStatus]

class RecordType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RECORD_TYPE_UNSPECIFIED: _ClassVar[RecordType]
    RECORD_TYPE_SEARCH_RESULT: _ClassVar[RecordType]

class RequestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REQUEST_STATUS_UNSPECIFIED: _ClassVar[RequestStatus]
    REQUEST_STATUS_OK: _ClassVar[RequestStatus]
    REQUEST_STATUS_FAILED: _ClassVar[RequestStatus]

class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_ORDER_UNSPECIFIED: _ClassVar[SortOrder]
    SORT_ORDER_DESC: _ClassVar[SortOrder]
    SORT_ORDER_ASC: _ClassVar[SortOrder]

class RunState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUN_STATE_UNSPECIFIED: _ClassVar[RunState]
    RUN_STATE_IDLE: _ClassVar[RunState]
    RUN_STATE_RUNNING: _ClassVar[RunState]
    RUN_STATE_UNKNOWN: _ClassVar[RunState]
MONITOR_STATUS_UNSPECIFIED: MonitorStatus
MONITOR_STATUS_ACTIVE: MonitorStatus
MONITOR_STATUS_PAUSED: MonitorStatus
MONITOR_STATUS_DISABLED: MonitorStatus
MONITOR_STATUS_DELETED: MonitorStatus
RUN_STATUS_UNSPECIFIED: RunStatus
RUN_STATUS_COMPLETED: RunStatus
RUN_STATUS_PARTIAL: RunStatus
RUN_STATUS_FAILED: RunStatus
RUN_STATUS_SKIPPED: RunStatus
WEBHOOK_STATUS_UNSPECIFIED: WebhookStatus
WEBHOOK_STATUS_ACTIVE: WebhookStatus
WEBHOOK_STATUS_DISABLED: WebhookStatus
RECORD_TYPE_UNSPECIFIED: RecordType
RECORD_TYPE_SEARCH_RESULT: RecordType
REQUEST_STATUS_UNSPECIFIED: RequestStatus
REQUEST_STATUS_OK: RequestStatus
REQUEST_STATUS_FAILED: RequestStatus
SORT_ORDER_UNSPECIFIED: SortOrder
SORT_ORDER_DESC: SortOrder
SORT_ORDER_ASC: SortOrder
RUN_STATE_UNSPECIFIED: RunState
RUN_STATE_IDLE: RunState
RUN_STATE_RUNNING: RunState
RUN_STATE_UNKNOWN: RunState

class Webhook(_message.Message):
    __slots__ = ("url", "events", "status")
    URL_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    url: str
    events: _containers.RepeatedScalarFieldContainer[str]
    status: WebhookStatus
    def __init__(self, url: _Optional[str] = ..., events: _Optional[_Iterable[str]] = ..., status: _Optional[_Union[WebhookStatus, str]] = ...) -> None: ...

class MonitorSearchRequest(_message.Message):
    __slots__ = ("request_id", "request", "consecutive_failures", "last_success_at")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    CONSECUTIVE_FAILURES_FIELD_NUMBER: _ClassVar[int]
    LAST_SUCCESS_AT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    request: _seltz_pb2.SearchRequest
    consecutive_failures: int
    last_success_at: _timestamp_pb2.Timestamp
    def __init__(self, request_id: _Optional[str] = ..., request: _Optional[_Union[_seltz_pb2.SearchRequest, _Mapping]] = ..., consecutive_failures: _Optional[int] = ..., last_success_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Monitor(_message.Message):
    __slots__ = ("monitor_id", "status", "name", "search_requests", "cadence", "webhook", "created_at", "updated_at")
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEARCH_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    monitor_id: str
    status: MonitorStatus
    name: str
    search_requests: _containers.RepeatedCompositeFieldContainer[MonitorSearchRequest]
    cadence: str
    webhook: Webhook
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, monitor_id: _Optional[str] = ..., status: _Optional[_Union[MonitorStatus, str]] = ..., name: _Optional[str] = ..., search_requests: _Optional[_Iterable[_Union[MonitorSearchRequest, _Mapping]]] = ..., cadence: _Optional[str] = ..., webhook: _Optional[_Union[Webhook, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RunRequest(_message.Message):
    __slots__ = ("request_id", "status", "reason", "results_returned", "new_records", "completed_at")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    RESULTS_RETURNED_FIELD_NUMBER: _ClassVar[int]
    NEW_RECORDS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    status: RequestStatus
    reason: str
    results_returned: int
    new_records: int
    completed_at: _timestamp_pb2.Timestamp
    def __init__(self, request_id: _Optional[str] = ..., status: _Optional[_Union[RequestStatus, str]] = ..., reason: _Optional[str] = ..., results_returned: _Optional[int] = ..., new_records: _Optional[int] = ..., completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Run(_message.Message):
    __slots__ = ("run_id", "monitor_id", "started_at", "completed_at", "status", "status_reason", "first_record_id", "last_record_id", "record_count", "requests_total", "requests_ok", "requests_failed")
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    FIRST_RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_OK_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FAILED_FIELD_NUMBER: _ClassVar[int]
    run_id: int
    monitor_id: str
    started_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    status: RunStatus
    status_reason: str
    first_record_id: int
    last_record_id: int
    record_count: int
    requests_total: int
    requests_ok: int
    requests_failed: int
    def __init__(self, run_id: _Optional[int] = ..., monitor_id: _Optional[str] = ..., started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[RunStatus, str]] = ..., status_reason: _Optional[str] = ..., first_record_id: _Optional[int] = ..., last_record_id: _Optional[int] = ..., record_count: _Optional[int] = ..., requests_total: _Optional[int] = ..., requests_ok: _Optional[int] = ..., requests_failed: _Optional[int] = ...) -> None: ...

class SearchRequestRef(_message.Message):
    __slots__ = ("request_id", "query")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    query: str
    def __init__(self, request_id: _Optional[str] = ..., query: _Optional[str] = ...) -> None: ...

class SearchRecord(_message.Message):
    __slots__ = ("document", "matched_requests")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    MATCHED_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    document: _seltz_pb2.Document
    matched_requests: _containers.RepeatedCompositeFieldContainer[SearchRequestRef]
    def __init__(self, document: _Optional[_Union[_seltz_pb2.Document, _Mapping]] = ..., matched_requests: _Optional[_Iterable[_Union[SearchRequestRef, _Mapping]]] = ...) -> None: ...

class Record(_message.Message):
    __slots__ = ("record_id", "run_id", "type", "first_seen_at", "search_result")
    RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FIRST_SEEN_AT_FIELD_NUMBER: _ClassVar[int]
    SEARCH_RESULT_FIELD_NUMBER: _ClassVar[int]
    record_id: int
    run_id: int
    type: RecordType
    first_seen_at: _timestamp_pb2.Timestamp
    search_result: SearchRecord
    def __init__(self, record_id: _Optional[int] = ..., run_id: _Optional[int] = ..., type: _Optional[_Union[RecordType, str]] = ..., first_seen_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., search_result: _Optional[_Union[SearchRecord, _Mapping]] = ...) -> None: ...

class CreateMonitorRequest(_message.Message):
    __slots__ = ("api_key", "name", "cadence", "search_requests", "webhook", "status")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    name: str
    cadence: str
    search_requests: _containers.RepeatedCompositeFieldContainer[_seltz_pb2.SearchRequest]
    webhook: Webhook
    status: MonitorStatus
    def __init__(self, api_key: _Optional[str] = ..., name: _Optional[str] = ..., cadence: _Optional[str] = ..., search_requests: _Optional[_Iterable[_Union[_seltz_pb2.SearchRequest, _Mapping]]] = ..., webhook: _Optional[_Union[Webhook, _Mapping]] = ..., status: _Optional[_Union[MonitorStatus, str]] = ...) -> None: ...

class CreateMonitorResponse(_message.Message):
    __slots__ = ("monitor", "webhook_secret")
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_SECRET_FIELD_NUMBER: _ClassVar[int]
    monitor: Monitor
    webhook_secret: str
    def __init__(self, monitor: _Optional[_Union[Monitor, _Mapping]] = ..., webhook_secret: _Optional[str] = ...) -> None: ...

class GetMonitorRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ...) -> None: ...

class GetMonitorResponse(_message.Message):
    __slots__ = ("monitor", "run_state")
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    RUN_STATE_FIELD_NUMBER: _ClassVar[int]
    monitor: Monitor
    run_state: RunState
    def __init__(self, monitor: _Optional[_Union[Monitor, _Mapping]] = ..., run_state: _Optional[_Union[RunState, str]] = ...) -> None: ...

class ListMonitorsRequest(_message.Message):
    __slots__ = ("api_key", "name", "status", "since", "before", "limit")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    name: str
    status: MonitorStatus
    since: str
    before: str
    limit: int
    def __init__(self, api_key: _Optional[str] = ..., name: _Optional[str] = ..., status: _Optional[_Union[MonitorStatus, str]] = ..., since: _Optional[str] = ..., before: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class ListMonitorsResponse(_message.Message):
    __slots__ = ("monitors", "has_more")
    MONITORS_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    monitors: _containers.RepeatedCompositeFieldContainer[Monitor]
    has_more: bool
    def __init__(self, monitors: _Optional[_Iterable[_Union[Monitor, _Mapping]]] = ..., has_more: bool = ...) -> None: ...

class UpdateMonitorRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id", "name", "status", "cadence", "search_requests", "webhook")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    name: str
    status: MonitorStatus
    cadence: str
    search_requests: _containers.RepeatedCompositeFieldContainer[_seltz_pb2.SearchRequest]
    webhook: Webhook
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ..., name: _Optional[str] = ..., status: _Optional[_Union[MonitorStatus, str]] = ..., cadence: _Optional[str] = ..., search_requests: _Optional[_Iterable[_Union[_seltz_pb2.SearchRequest, _Mapping]]] = ..., webhook: _Optional[_Union[Webhook, _Mapping]] = ...) -> None: ...

class UpdateMonitorResponse(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: Monitor
    def __init__(self, monitor: _Optional[_Union[Monitor, _Mapping]] = ...) -> None: ...

class DeleteMonitorRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ...) -> None: ...

class DeleteMonitorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListRecordsRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id", "since", "before", "limit", "include_content")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    since: int
    before: int
    limit: int
    include_content: bool
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ..., since: _Optional[int] = ..., before: _Optional[int] = ..., limit: _Optional[int] = ..., include_content: bool = ...) -> None: ...

class ListRecordsResponse(_message.Message):
    __slots__ = ("records", "has_more")
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[Record]
    has_more: bool
    def __init__(self, records: _Optional[_Iterable[_Union[Record, _Mapping]]] = ..., has_more: bool = ...) -> None: ...

class StreamRecordsRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id", "since")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    since: int
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ..., since: _Optional[int] = ...) -> None: ...

class StreamRecordsResponse(_message.Message):
    __slots__ = ("record",)
    RECORD_FIELD_NUMBER: _ClassVar[int]
    record: Record
    def __init__(self, record: _Optional[_Union[Record, _Mapping]] = ...) -> None: ...

class ListRunsRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id", "since", "before", "limit", "sort")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    since: int
    before: int
    limit: int
    sort: SortOrder
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ..., since: _Optional[int] = ..., before: _Optional[int] = ..., limit: _Optional[int] = ..., sort: _Optional[_Union[SortOrder, str]] = ...) -> None: ...

class ListRunsResponse(_message.Message):
    __slots__ = ("runs", "has_more")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[Run]
    has_more: bool
    def __init__(self, runs: _Optional[_Iterable[_Union[Run, _Mapping]]] = ..., has_more: bool = ...) -> None: ...

class GetRunRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id", "run_id")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    run_id: int
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ..., run_id: _Optional[int] = ...) -> None: ...

class GetRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: Run
    def __init__(self, run: _Optional[_Union[Run, _Mapping]] = ...) -> None: ...

class ListRunRequestsRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id", "run_id")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    run_id: int
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ..., run_id: _Optional[int] = ...) -> None: ...

class ListRunRequestsResponse(_message.Message):
    __slots__ = ("requests",)
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[RunRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[RunRequest, _Mapping]]] = ...) -> None: ...

class ListRunRecordsRequest(_message.Message):
    __slots__ = ("api_key", "monitor_id", "run_id", "since", "before", "limit", "include_content")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    monitor_id: str
    run_id: int
    since: int
    before: int
    limit: int
    include_content: bool
    def __init__(self, api_key: _Optional[str] = ..., monitor_id: _Optional[str] = ..., run_id: _Optional[int] = ..., since: _Optional[int] = ..., before: _Optional[int] = ..., limit: _Optional[int] = ..., include_content: bool = ...) -> None: ...

class ListRunRecordsResponse(_message.Message):
    __slots__ = ("records", "has_more")
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[Record]
    has_more: bool
    def __init__(self, records: _Optional[_Iterable[_Union[Record, _Mapping]]] = ..., has_more: bool = ...) -> None: ...
