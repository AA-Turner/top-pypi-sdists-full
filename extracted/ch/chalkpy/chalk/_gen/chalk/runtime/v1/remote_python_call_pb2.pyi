from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
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

class RemoteCallStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REMOTE_CALL_STATUS_UNSPECIFIED: _ClassVar[RemoteCallStatus]
    REMOTE_CALL_STATUS_PENDING: _ClassVar[RemoteCallStatus]
    REMOTE_CALL_STATUS_RUNNING: _ClassVar[RemoteCallStatus]
    REMOTE_CALL_STATUS_COMPLETED: _ClassVar[RemoteCallStatus]
    REMOTE_CALL_STATUS_FAILED: _ClassVar[RemoteCallStatus]
    REMOTE_CALL_STATUS_EXPIRED: _ClassVar[RemoteCallStatus]

REMOTE_CALL_STATUS_UNSPECIFIED: RemoteCallStatus
REMOTE_CALL_STATUS_PENDING: RemoteCallStatus
REMOTE_CALL_STATUS_RUNNING: RemoteCallStatus
REMOTE_CALL_STATUS_COMPLETED: RemoteCallStatus
REMOTE_CALL_STATUS_FAILED: RemoteCallStatus
REMOTE_CALL_STATUS_EXPIRED: RemoteCallStatus

class CallFunctionRequest(_message.Message):
    __slots__ = ("name", "feather_stream")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FEATHER_STREAM_FIELD_NUMBER: _ClassVar[int]
    name: str
    feather_stream: bytes
    def __init__(self, name: _Optional[str] = ..., feather_stream: _Optional[bytes] = ...) -> None: ...

class CallFunctionResponse(_message.Message):
    __slots__ = ("feather_stream",)
    FEATHER_STREAM_FIELD_NUMBER: _ClassVar[int]
    feather_stream: bytes
    def __init__(self, feather_stream: _Optional[bytes] = ...) -> None: ...

class RemoteCallArgs(_message.Message):
    __slots__ = ("feather_bytes", "storage_object_id")
    FEATHER_BYTES_FIELD_NUMBER: _ClassVar[int]
    STORAGE_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    feather_bytes: bytes
    storage_object_id: str
    def __init__(self, feather_bytes: _Optional[bytes] = ..., storage_object_id: _Optional[str] = ...) -> None: ...

class EnqueueRemoteCallRequest(_message.Message):
    __slots__ = ("name", "args")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    args: RemoteCallArgs
    def __init__(self, name: _Optional[str] = ..., args: _Optional[_Union[RemoteCallArgs, _Mapping]] = ...) -> None: ...

class EnqueueRemoteCallResponse(_message.Message):
    __slots__ = ("call_id",)
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    def __init__(self, call_id: _Optional[str] = ...) -> None: ...

class OpenRemoteCallBatch(_message.Message):
    __slots__ = ("name", "batch_id", "result_cursor")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    batch_id: str
    result_cursor: str
    def __init__(
        self, name: _Optional[str] = ..., batch_id: _Optional[str] = ..., result_cursor: _Optional[str] = ...
    ) -> None: ...

class SubmitRemoteCallBatchChunk(_message.Message):
    __slots__ = ("chunk_index", "first_row_index", "args")
    CHUNK_INDEX_FIELD_NUMBER: _ClassVar[int]
    FIRST_ROW_INDEX_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    chunk_index: int
    first_row_index: int
    args: RemoteCallArgs
    def __init__(
        self,
        chunk_index: _Optional[int] = ...,
        first_row_index: _Optional[int] = ...,
        args: _Optional[_Union[RemoteCallArgs, _Mapping]] = ...,
    ) -> None: ...

class FinishRemoteCallBatchSubmission(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CancelRemoteCallBatch(_message.Message):
    __slots__ = ("reason",)
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: str
    def __init__(self, reason: _Optional[str] = ...) -> None: ...

class StreamRemoteCallBatchRequest(_message.Message):
    __slots__ = ("open", "submit", "finish", "cancel")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    SUBMIT_FIELD_NUMBER: _ClassVar[int]
    FINISH_FIELD_NUMBER: _ClassVar[int]
    CANCEL_FIELD_NUMBER: _ClassVar[int]
    open: OpenRemoteCallBatch
    submit: SubmitRemoteCallBatchChunk
    finish: FinishRemoteCallBatchSubmission
    cancel: CancelRemoteCallBatch
    def __init__(
        self,
        open: _Optional[_Union[OpenRemoteCallBatch, _Mapping]] = ...,
        submit: _Optional[_Union[SubmitRemoteCallBatchChunk, _Mapping]] = ...,
        finish: _Optional[_Union[FinishRemoteCallBatchSubmission, _Mapping]] = ...,
        cancel: _Optional[_Union[CancelRemoteCallBatch, _Mapping]] = ...,
    ) -> None: ...

class RemoteCallBatchOpened(_message.Message):
    __slots__ = ("batch_id", "submission_finished", "next_chunk_index", "next_row_index")
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_FINISHED_FIELD_NUMBER: _ClassVar[int]
    NEXT_CHUNK_INDEX_FIELD_NUMBER: _ClassVar[int]
    NEXT_ROW_INDEX_FIELD_NUMBER: _ClassVar[int]
    batch_id: str
    submission_finished: bool
    next_chunk_index: int
    next_row_index: int
    def __init__(
        self,
        batch_id: _Optional[str] = ...,
        submission_finished: bool = ...,
        next_chunk_index: _Optional[int] = ...,
        next_row_index: _Optional[int] = ...,
    ) -> None: ...

class RemoteCallBatchCall(_message.Message):
    __slots__ = ("row_index", "call_id")
    ROW_INDEX_FIELD_NUMBER: _ClassVar[int]
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    row_index: int
    call_id: str
    def __init__(self, row_index: _Optional[int] = ..., call_id: _Optional[str] = ...) -> None: ...

class RemoteCallBatchChunkAccepted(_message.Message):
    __slots__ = ("chunk_index", "calls")
    CHUNK_INDEX_FIELD_NUMBER: _ClassVar[int]
    CALLS_FIELD_NUMBER: _ClassVar[int]
    chunk_index: int
    calls: _containers.RepeatedCompositeFieldContainer[RemoteCallBatchCall]
    def __init__(
        self,
        chunk_index: _Optional[int] = ...,
        calls: _Optional[_Iterable[_Union[RemoteCallBatchCall, _Mapping]]] = ...,
    ) -> None: ...

class RemoteCallBatchResult(_message.Message):
    __slots__ = ("row_index", "call_id", "sequence", "status", "result", "errors")
    ROW_INDEX_FIELD_NUMBER: _ClassVar[int]
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    row_index: int
    call_id: str
    sequence: int
    status: RemoteCallStatus
    result: CallFunctionResponse
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        row_index: _Optional[int] = ...,
        call_id: _Optional[str] = ...,
        sequence: _Optional[int] = ...,
        status: _Optional[_Union[RemoteCallStatus, str]] = ...,
        result: _Optional[_Union[CallFunctionResponse, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class RemoteCallBatchResultChunk(_message.Message):
    __slots__ = ("results", "cursor")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[RemoteCallBatchResult]
    cursor: str
    def __init__(
        self, results: _Optional[_Iterable[_Union[RemoteCallBatchResult, _Mapping]]] = ..., cursor: _Optional[str] = ...
    ) -> None: ...

class RemoteCallBatchCompleted(_message.Message):
    __slots__ = ("total_calls", "completed_calls", "failed_calls")
    TOTAL_CALLS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_CALLS_FIELD_NUMBER: _ClassVar[int]
    FAILED_CALLS_FIELD_NUMBER: _ClassVar[int]
    total_calls: int
    completed_calls: int
    failed_calls: int
    def __init__(
        self,
        total_calls: _Optional[int] = ...,
        completed_calls: _Optional[int] = ...,
        failed_calls: _Optional[int] = ...,
    ) -> None: ...

class StreamRemoteCallBatchResponse(_message.Message):
    __slots__ = ("opened", "accepted", "results", "completed")
    OPENED_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    opened: RemoteCallBatchOpened
    accepted: RemoteCallBatchChunkAccepted
    results: RemoteCallBatchResultChunk
    completed: RemoteCallBatchCompleted
    def __init__(
        self,
        opened: _Optional[_Union[RemoteCallBatchOpened, _Mapping]] = ...,
        accepted: _Optional[_Union[RemoteCallBatchChunkAccepted, _Mapping]] = ...,
        results: _Optional[_Union[RemoteCallBatchResultChunk, _Mapping]] = ...,
        completed: _Optional[_Union[RemoteCallBatchCompleted, _Mapping]] = ...,
    ) -> None: ...

class PollRemoteCallRequest(_message.Message):
    __slots__ = ("call_id", "cursor")
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    cursor: str
    def __init__(self, call_id: _Optional[str] = ..., cursor: _Optional[str] = ...) -> None: ...

class PollRemoteCallResponse(_message.Message):
    __slots__ = ("status", "results", "cursor", "errors")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    status: RemoteCallStatus
    results: _containers.RepeatedCompositeFieldContainer[CallFunctionResponse]
    cursor: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        status: _Optional[_Union[RemoteCallStatus, str]] = ...,
        results: _Optional[_Iterable[_Union[CallFunctionResponse, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class PurgeQueueRequest(_message.Message):
    __slots__ = ("function_name", "all")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ALL_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    all: bool
    def __init__(self, function_name: _Optional[str] = ..., all: bool = ...) -> None: ...

class PurgeQueueResponse(_message.Message):
    __slots__ = ("items_removed_by_function",)
    class ItemsRemovedByFunctionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

    ITEMS_REMOVED_BY_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    items_removed_by_function: _containers.ScalarMap[str, int]
    def __init__(self, items_removed_by_function: _Optional[_Mapping[str, int]] = ...) -> None: ...

class FunctionCallInfo(_message.Message):
    __slots__ = ("call_id", "function_name", "enqueued_at", "status", "result_summary", "trace_id")
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ENQUEUED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    function_name: str
    enqueued_at: _timestamp_pb2.Timestamp
    status: RemoteCallStatus
    result_summary: str
    trace_id: str
    def __init__(
        self,
        call_id: _Optional[str] = ...,
        function_name: _Optional[str] = ...,
        enqueued_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[_Union[RemoteCallStatus, str]] = ...,
        result_summary: _Optional[str] = ...,
        trace_id: _Optional[str] = ...,
    ) -> None: ...

class GetRecentCallsRequest(_message.Message):
    __slots__ = ("function_name", "limit", "page_token")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    limit: int
    page_token: str
    def __init__(
        self, function_name: _Optional[str] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...
    ) -> None: ...

class GetRecentCallsResponse(_message.Message):
    __slots__ = ("calls", "next_page_token")
    CALLS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    calls: _containers.RepeatedCompositeFieldContainer[FunctionCallInfo]
    next_page_token: str
    def __init__(
        self,
        calls: _Optional[_Iterable[_Union[FunctionCallInfo, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class GetCallResultsRequest(_message.Message):
    __slots__ = ("call_ids",)
    CALL_IDS_FIELD_NUMBER: _ClassVar[int]
    call_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, call_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CallResult(_message.Message):
    __slots__ = ("call_id", "response", "error_message")
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    call_id: str
    response: PollRemoteCallResponse
    error_message: str
    def __init__(
        self,
        call_id: _Optional[str] = ...,
        response: _Optional[_Union[PollRemoteCallResponse, _Mapping]] = ...,
        error_message: _Optional[str] = ...,
    ) -> None: ...

class GetCallResultsResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CallResult]
    def __init__(self, results: _Optional[_Iterable[_Union[CallResult, _Mapping]]] = ...) -> None: ...

class GetCallCountRequest(_message.Message):
    __slots__ = ("function_name",)
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    def __init__(self, function_name: _Optional[str] = ...) -> None: ...

class GetCallCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...
