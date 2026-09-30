from chalk._gen.chalk.server.v1 import incident_pb2 as _incident_pb2
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

class MetricIncidentBody(_message.Message):
    __slots__ = ("groups",)
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[_incident_pb2.IncidentGroup]
    def __init__(self, groups: _Optional[_Iterable[_Union[_incident_pb2.IncidentGroup, _Mapping]]] = ...) -> None: ...

class HealthcheckIncidentBody(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LogsIncidentBody(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SqlBadRowsIncidentBody(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DataSourceIncidentBody(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MonitorIncident(_message.Message):
    __slots__ = (
        "id",
        "monitor_id",
        "started_at",
        "closed_at",
        "dedupe_key",
        "linked_entities",
        "metric_incident",
        "health_incident",
        "logs_incident",
        "sql_bad_rows_incident",
        "data_source_incident",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    CLOSED_AT_FIELD_NUMBER: _ClassVar[int]
    DEDUPE_KEY_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    METRIC_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    HEALTH_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    LOGS_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    SQL_BAD_ROWS_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    monitor_id: str
    started_at: _timestamp_pb2.Timestamp
    closed_at: _timestamp_pb2.Timestamp
    dedupe_key: str
    linked_entities: _containers.RepeatedCompositeFieldContainer[_incident_pb2.IncidentLinkedEntity]
    metric_incident: MetricIncidentBody
    health_incident: HealthcheckIncidentBody
    logs_incident: LogsIncidentBody
    sql_bad_rows_incident: SqlBadRowsIncidentBody
    data_source_incident: DataSourceIncidentBody
    def __init__(
        self,
        id: _Optional[str] = ...,
        monitor_id: _Optional[str] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        closed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        dedupe_key: _Optional[str] = ...,
        linked_entities: _Optional[_Iterable[_Union[_incident_pb2.IncidentLinkedEntity, _Mapping]]] = ...,
        metric_incident: _Optional[_Union[MetricIncidentBody, _Mapping]] = ...,
        health_incident: _Optional[_Union[HealthcheckIncidentBody, _Mapping]] = ...,
        logs_incident: _Optional[_Union[LogsIncidentBody, _Mapping]] = ...,
        sql_bad_rows_incident: _Optional[_Union[SqlBadRowsIncidentBody, _Mapping]] = ...,
        data_source_incident: _Optional[_Union[DataSourceIncidentBody, _Mapping]] = ...,
    ) -> None: ...
