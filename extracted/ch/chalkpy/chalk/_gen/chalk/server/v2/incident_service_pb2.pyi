from chalk._gen.chalk.artifacts.v1 import monitor_pb2 as _monitor_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import incident_pb2 as _incident_pb2
from chalk._gen.chalk.server.v2 import incident_pb2 as _incident_pb2_1
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

class CloseIncidentRequest(_message.Message):
    __slots__ = ("incident_id", "mute_duration")
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    MUTE_DURATION_FIELD_NUMBER: _ClassVar[int]
    incident_id: str
    mute_duration: _duration_pb2.Duration
    def __init__(
        self,
        incident_id: _Optional[str] = ...,
        mute_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class CloseIncidentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetIncidentRequest(_message.Message):
    __slots__ = ("incident_id",)
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    incident_id: str
    def __init__(self, incident_id: _Optional[str] = ...) -> None: ...

class GetIncidentResponse(_message.Message):
    __slots__ = ("incident",)
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    incident: _incident_pb2_1.MonitorIncident
    def __init__(self, incident: _Optional[_Union[_incident_pb2_1.MonitorIncident, _Mapping]] = ...) -> None: ...

class ListIncidentsFilters(_message.Message):
    __slots__ = (
        "created_at_lower_bound_inclusive",
        "created_at_upper_bound_exclusive",
        "has_closed_filter",
        "linked_entity_kind_filter",
        "linked_entity_id_filter",
        "monitor_id_filter",
        "monitor_type_filter",
    )
    CREATED_AT_LOWER_BOUND_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_UPPER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    HAS_CLOSED_FILTER_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_KIND_FILTER_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    MONITOR_TYPE_FILTER_FIELD_NUMBER: _ClassVar[int]
    created_at_lower_bound_inclusive: _timestamp_pb2.Timestamp
    created_at_upper_bound_exclusive: _timestamp_pb2.Timestamp
    has_closed_filter: bool
    linked_entity_kind_filter: _incident_pb2.IncidentEntityKind
    linked_entity_id_filter: str
    monitor_id_filter: str
    monitor_type_filter: _monitor_pb2.MonitorType
    def __init__(
        self,
        created_at_lower_bound_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_at_upper_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        has_closed_filter: bool = ...,
        linked_entity_kind_filter: _Optional[_Union[_incident_pb2.IncidentEntityKind, str]] = ...,
        linked_entity_id_filter: _Optional[str] = ...,
        monitor_id_filter: _Optional[str] = ...,
        monitor_type_filter: _Optional[_Union[_monitor_pb2.MonitorType, str]] = ...,
    ) -> None: ...

class ListIncidentsRequest(_message.Message):
    __slots__ = ("filters", "limit", "page_token")
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    filters: ListIncidentsFilters
    limit: int
    page_token: str
    def __init__(
        self,
        filters: _Optional[_Union[ListIncidentsFilters, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class ListIncidentsResponse(_message.Message):
    __slots__ = ("incidents", "next_page_token")
    INCIDENTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    incidents: _containers.RepeatedCompositeFieldContainer[_incident_pb2_1.MonitorIncident]
    next_page_token: str
    def __init__(
        self,
        incidents: _Optional[_Iterable[_Union[_incident_pb2_1.MonitorIncident, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...
