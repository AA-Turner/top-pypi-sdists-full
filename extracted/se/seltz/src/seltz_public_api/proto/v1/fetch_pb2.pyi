from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FetchStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FETCH_STATUS_UNSPECIFIED: _ClassVar[FetchStatus]
    FETCH_STATUS_OK: _ClassVar[FetchStatus]
    FETCH_STATUS_ERROR: _ClassVar[FetchStatus]
FETCH_STATUS_UNSPECIFIED: FetchStatus
FETCH_STATUS_OK: FetchStatus
FETCH_STATUS_ERROR: FetchStatus

class FetchRequest(_message.Message):
    __slots__ = ("urls", "api_key", "formats", "tier", "timeout_ms")
    URLS_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    FORMATS_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    urls: _containers.RepeatedScalarFieldContainer[str]
    api_key: str
    formats: _containers.RepeatedScalarFieldContainer[str]
    tier: str
    timeout_ms: int
    def __init__(self, urls: _Optional[_Iterable[str]] = ..., api_key: _Optional[str] = ..., formats: _Optional[_Iterable[str]] = ..., tier: _Optional[str] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class FetchResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[FetchResult]
    def __init__(self, results: _Optional[_Iterable[_Union[FetchResult, _Mapping]]] = ...) -> None: ...

class FetchResult(_message.Message):
    __slots__ = ("requested_url", "status", "error", "markdown", "fetched_at", "final_url", "http_status_code", "content_type")
    REQUESTED_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_FIELD_NUMBER: _ClassVar[int]
    FETCHED_AT_FIELD_NUMBER: _ClassVar[int]
    FINAL_URL_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    requested_url: str
    status: FetchStatus
    error: FetchError
    markdown: str
    fetched_at: _timestamp_pb2.Timestamp
    final_url: str
    http_status_code: int
    content_type: str
    def __init__(self, requested_url: _Optional[str] = ..., status: _Optional[_Union[FetchStatus, str]] = ..., error: _Optional[_Union[FetchError, _Mapping]] = ..., markdown: _Optional[str] = ..., fetched_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., final_url: _Optional[str] = ..., http_status_code: _Optional[int] = ..., content_type: _Optional[str] = ...) -> None: ...

class FetchError(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
