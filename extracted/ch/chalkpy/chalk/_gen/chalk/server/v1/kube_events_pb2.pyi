from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class KubeEvent(_message.Message):
    __slots__ = (
        "timestamp",
        "event_type",
        "severity",
        "cluster_name",
        "namespace",
        "name",
        "kind",
        "reason",
        "message",
        "source_component",
        "first_timestamp",
        "last_timestamp",
        "count",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    FIRST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    event_type: str
    severity: str
    cluster_name: str
    namespace: str
    name: str
    kind: str
    reason: str
    message: str
    source_component: str
    first_timestamp: _timestamp_pb2.Timestamp
    last_timestamp: _timestamp_pb2.Timestamp
    count: int
    def __init__(
        self,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        event_type: _Optional[str] = ...,
        severity: _Optional[str] = ...,
        cluster_name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        name: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
        source_component: _Optional[str] = ...,
        first_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        count: _Optional[int] = ...,
    ) -> None: ...

class ListKubeEventsRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "namespaces", "pod_names", "message_filter", "limit", "offset")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    POD_NAMES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FILTER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    namespaces: _containers.RepeatedScalarFieldContainer[str]
    pod_names: _containers.RepeatedScalarFieldContainer[str]
    message_filter: str
    limit: int
    offset: int
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        namespaces: _Optional[_Iterable[str]] = ...,
        pod_names: _Optional[_Iterable[str]] = ...,
        message_filter: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
    ) -> None: ...

class ListKubeEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[KubeEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[KubeEvent, _Mapping]]] = ...) -> None: ...
