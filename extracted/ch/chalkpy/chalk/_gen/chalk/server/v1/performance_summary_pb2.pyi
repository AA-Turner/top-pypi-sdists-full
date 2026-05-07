from google.protobuf import struct_pb2 as _struct_pb2
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

class ShardPerformanceSummary(_message.Message):
    __slots__ = ("operation_id", "shard_id", "performance_summary_with_query_config")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SUMMARY_WITH_QUERY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    shard_id: int
    performance_summary_with_query_config: _struct_pb2.Struct
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        shard_id: _Optional[int] = ...,
        performance_summary_with_query_config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class ListOfflineQueryShardPerformanceSummariesPageToken(_message.Message):
    __slots__ = ("shard_id_hwm",)
    SHARD_ID_HWM_FIELD_NUMBER: _ClassVar[int]
    shard_id_hwm: int
    def __init__(self, shard_id_hwm: _Optional[int] = ...) -> None: ...

class ListOfflineQueryShardPerformanceSummariesRequest(_message.Message):
    __slots__ = ("operation_id", "limit", "page_token")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    limit: int
    page_token: str
    def __init__(
        self, operation_id: _Optional[str] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...
    ) -> None: ...

class ListOfflineQueryShardPerformanceSummariesResponse(_message.Message):
    __slots__ = ("performance_summaries", "next_page_token")
    PERFORMANCE_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    performance_summaries: _containers.RepeatedCompositeFieldContainer[ShardPerformanceSummary]
    next_page_token: str
    def __init__(
        self,
        performance_summaries: _Optional[_Iterable[_Union[ShardPerformanceSummary, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...
