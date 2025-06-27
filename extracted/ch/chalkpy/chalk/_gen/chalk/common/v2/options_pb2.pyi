from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class ExecutionOptions(_message.Message):
    __slots__ = ("query_now", "query_context", "correlation_id", "deadline", "include_request_meta")
    class QueryContextEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    QUERY_NOW_FIELD_NUMBER: _ClassVar[int]
    QUERY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_REQUEST_META_FIELD_NUMBER: _ClassVar[int]
    query_now: _timestamp_pb2.Timestamp
    query_context: _containers.MessageMap[str, _struct_pb2.Value]
    correlation_id: str
    deadline: _timestamp_pb2.Timestamp
    include_request_meta: bool
    def __init__(
        self,
        query_now: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_context: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        correlation_id: _Optional[str] = ...,
        deadline: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        include_request_meta: bool = ...,
    ) -> None: ...

class PlanningOptions(_message.Message):
    __slots__ = ("tags", "required_resolver_tags", "planner_flags", "overlay_graph")
    class PlannerFlagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    TAGS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_RESOLVER_TAGS_FIELD_NUMBER: _ClassVar[int]
    PLANNER_FLAGS_FIELD_NUMBER: _ClassVar[int]
    OVERLAY_GRAPH_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedScalarFieldContainer[str]
    required_resolver_tags: _containers.RepeatedScalarFieldContainer[str]
    planner_flags: _containers.MessageMap[str, _struct_pb2.Value]
    overlay_graph: _graph_pb2.OverlayGraph
    def __init__(
        self,
        tags: _Optional[_Iterable[str]] = ...,
        required_resolver_tags: _Optional[_Iterable[str]] = ...,
        planner_flags: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        overlay_graph: _Optional[_Union[_graph_pb2.OverlayGraph, _Mapping]] = ...,
    ) -> None: ...
