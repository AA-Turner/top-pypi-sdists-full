from chalk._gen.chalk.aggregate.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import online_query_pb2 as _online_query_pb2
from chalk._gen.chalk.common.v1 import upload_features_pb2 as _upload_features_pb2
from chalk._gen.chalk.engine.v1 import bloom_filter_pb2 as _bloom_filter_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PullQueryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PULL_QUERY_STATUS_UNSPECIFIED: _ClassVar[PullQueryStatus]
    PULL_QUERY_STATUS_PENDING: _ClassVar[PullQueryStatus]
    PULL_QUERY_STATUS_COMPLETED: _ClassVar[PullQueryStatus]
    PULL_QUERY_STATUS_FAILED: _ClassVar[PullQueryStatus]
    PULL_QUERY_STATUS_NOT_FOUND: _ClassVar[PullQueryStatus]

PULL_QUERY_STATUS_UNSPECIFIED: PullQueryStatus
PULL_QUERY_STATUS_PENDING: PullQueryStatus
PULL_QUERY_STATUS_COMPLETED: PullQueryStatus
PULL_QUERY_STATUS_FAILED: PullQueryStatus
PULL_QUERY_STATUS_NOT_FOUND: PullQueryStatus

class PingRequest(_message.Message):
    __slots__ = ("num",)
    NUM_FIELD_NUMBER: _ClassVar[int]
    num: int
    def __init__(self, num: _Optional[int] = ...) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("num",)
    NUM_FIELD_NUMBER: _ClassVar[int]
    num: int
    def __init__(self, num: _Optional[int] = ...) -> None: ...

class GetPullQueryResultRequest(_message.Message):
    __slots__ = ("query_id",)
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    def __init__(self, query_id: _Optional[str] = ...) -> None: ...

class GetPullQueryResultResponse(_message.Message):
    __slots__ = ("status", "result", "error_message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: PullQueryStatus
    result: _online_query_pb2.OnlineQueryBulkResponse
    error_message: str
    def __init__(
        self,
        status: _Optional[_Union[PullQueryStatus, str]] = ...,
        result: _Optional[_Union[_online_query_pb2.OnlineQueryBulkResponse, _Mapping]] = ...,
        error_message: _Optional[str] = ...,
    ) -> None: ...
