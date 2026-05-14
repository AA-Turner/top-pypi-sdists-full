from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
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

class IncidentEntityKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INCIDENT_ENTITY_KIND_UNSPECIFIED: _ClassVar[IncidentEntityKind]
    INCIDENT_ENTITY_KIND_FEATURE: _ClassVar[IncidentEntityKind]
    INCIDENT_ENTITY_KIND_RESOLVER: _ClassVar[IncidentEntityKind]
    INCIDENT_ENTITY_KIND_SCHEDULED_QUERY: _ClassVar[IncidentEntityKind]

INCIDENT_ENTITY_KIND_UNSPECIFIED: IncidentEntityKind
INCIDENT_ENTITY_KIND_FEATURE: IncidentEntityKind
INCIDENT_ENTITY_KIND_RESOLVER: IncidentEntityKind
INCIDENT_ENTITY_KIND_SCHEDULED_QUERY: IncidentEntityKind

class IncidentLinkedEntity(_message.Message):
    __slots__ = ("entity_kind", "entity_id")
    ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    entity_kind: IncidentEntityKind
    entity_id: str
    def __init__(
        self, entity_kind: _Optional[_Union[IncidentEntityKind, str]] = ..., entity_id: _Optional[str] = ...
    ) -> None: ...

class IncidentGroup(_message.Message):
    __slots__ = ("group_key", "value")
    GROUP_KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    group_key: str
    value: str
    def __init__(self, group_key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class MetricIncident(_message.Message):
    __slots__ = ("id", "started_at", "closed_at", "metric_config", "linked_entity", "dedupe_key", "groups")
    ID_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    CLOSED_AT_FIELD_NUMBER: _ClassVar[int]
    METRIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_FIELD_NUMBER: _ClassVar[int]
    DEDUPE_KEY_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    id: str
    started_at: _timestamp_pb2.Timestamp
    closed_at: _timestamp_pb2.Timestamp
    metric_config: _chart_pb2.MetricConfig
    linked_entity: IncidentLinkedEntity
    dedupe_key: str
    groups: _containers.RepeatedCompositeFieldContainer[IncidentGroup]
    def __init__(
        self,
        id: _Optional[str] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        closed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        metric_config: _Optional[_Union[_chart_pb2.MetricConfig, _Mapping]] = ...,
        linked_entity: _Optional[_Union[IncidentLinkedEntity, _Mapping]] = ...,
        dedupe_key: _Optional[str] = ...,
        groups: _Optional[_Iterable[_Union[IncidentGroup, _Mapping]]] = ...,
    ) -> None: ...

class GetIncidentRequest(_message.Message):
    __slots__ = ("incident_id",)
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    incident_id: str
    def __init__(self, incident_id: _Optional[str] = ...) -> None: ...

class GetIncidentResponse(_message.Message):
    __slots__ = ("incident",)
    INCIDENT_FIELD_NUMBER: _ClassVar[int]
    incident: MetricIncident
    def __init__(self, incident: _Optional[_Union[MetricIncident, _Mapping]] = ...) -> None: ...

class GetIncidentAlertsChartRequest(_message.Message):
    __slots__ = ("incident_id", "point_limit")
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    incident_id: str
    point_limit: int
    def __init__(self, incident_id: _Optional[str] = ..., point_limit: _Optional[int] = ...) -> None: ...

class GetIncidentAlertsChartResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...

class ListIncidentsPageToken(_message.Message):
    __slots__ = ("created_at_hwm", "id_hwm")
    CREATED_AT_HWM_FIELD_NUMBER: _ClassVar[int]
    ID_HWM_FIELD_NUMBER: _ClassVar[int]
    created_at_hwm: _timestamp_pb2.Timestamp
    id_hwm: str
    def __init__(
        self, created_at_hwm: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id_hwm: _Optional[str] = ...
    ) -> None: ...

class ListIncidentsFilters(_message.Message):
    __slots__ = (
        "created_at_lower_bound_inclusive",
        "created_at_upper_bound_exclusive",
        "has_closed_filter",
        "linked_entity_kind_filter",
        "linked_entity_id_filter",
    )
    CREATED_AT_LOWER_BOUND_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_UPPER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    HAS_CLOSED_FILTER_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_KIND_FILTER_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    created_at_lower_bound_inclusive: _timestamp_pb2.Timestamp
    created_at_upper_bound_exclusive: _timestamp_pb2.Timestamp
    has_closed_filter: bool
    linked_entity_kind_filter: IncidentEntityKind
    linked_entity_id_filter: str
    def __init__(
        self,
        created_at_lower_bound_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_at_upper_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        has_closed_filter: bool = ...,
        linked_entity_kind_filter: _Optional[_Union[IncidentEntityKind, str]] = ...,
        linked_entity_id_filter: _Optional[str] = ...,
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
    incidents: _containers.RepeatedCompositeFieldContainer[MetricIncident]
    next_page_token: str
    def __init__(
        self,
        incidents: _Optional[_Iterable[_Union[MetricIncident, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...
