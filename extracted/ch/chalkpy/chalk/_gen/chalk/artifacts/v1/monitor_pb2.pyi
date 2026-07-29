from chalk._gen.chalk.artifacts.v1 import alert_channel_pb2 as _alert_channel_pb2
from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
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

class MonitorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MONITOR_TYPE_UNSPECIFIED: _ClassVar[MonitorType]
    MONITOR_TYPE_CHART: _ClassVar[MonitorType]
    MONITOR_TYPE_LOG: _ClassVar[MonitorType]
    MONITOR_TYPE_HEALTHCHECK: _ClassVar[MonitorType]

MONITOR_TYPE_UNSPECIFIED: MonitorType
MONITOR_TYPE_CHART: MonitorType
MONITOR_TYPE_LOG: MonitorType
MONITOR_TYPE_HEALTHCHECK: MonitorType

class LogsMonitor(_message.Message):
    __slots__ = ("query_string", "tags", "window_period")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    QUERY_STRING_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    query_string: str
    tags: _containers.ScalarMap[str, str]
    window_period: str
    def __init__(
        self,
        query_string: _Optional[str] = ...,
        tags: _Optional[_Mapping[str, str]] = ...,
        window_period: _Optional[str] = ...,
    ) -> None: ...

class HealthcheckMonitor(_message.Message):
    __slots__ = ("healthcheck_name",)
    HEALTHCHECK_NAME_FIELD_NUMBER: _ClassVar[int]
    healthcheck_name: str
    def __init__(self, healthcheck_name: _Optional[str] = ...) -> None: ...

class ChartMonitor(_message.Message):
    __slots__ = ("series_mql", "formula_mql")
    SERIES_MQL_FIELD_NUMBER: _ClassVar[int]
    FORMULA_MQL_FIELD_NUMBER: _ClassVar[int]
    series_mql: _containers.RepeatedScalarFieldContainer[str]
    formula_mql: str
    def __init__(self, series_mql: _Optional[_Iterable[str]] = ..., formula_mql: _Optional[str] = ...) -> None: ...

class AlertChannel(_message.Message):
    __slots__ = ("entity_kind", "entity_id", "entity_name")
    ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_kind: _alert_channel_pb2.AlertChannelKind
    entity_id: str
    entity_name: str
    def __init__(
        self,
        entity_kind: _Optional[_Union[_alert_channel_pb2.AlertChannelKind, str]] = ...,
        entity_id: _Optional[str] = ...,
        entity_name: _Optional[str] = ...,
    ) -> None: ...

class Threshold(_message.Message):
    __slots__ = ("threshold_kind", "threshold_value", "alert_channels")
    THRESHOLD_KIND_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    ALERT_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    threshold_kind: _chart_pb2.ThresholdKind
    threshold_value: float
    alert_channels: _containers.RepeatedCompositeFieldContainer[AlertChannel]
    def __init__(
        self,
        threshold_kind: _Optional[_Union[_chart_pb2.ThresholdKind, str]] = ...,
        threshold_value: _Optional[float] = ...,
        alert_channels: _Optional[_Iterable[_Union[AlertChannel, _Mapping]]] = ...,
    ) -> None: ...

class Monitor(_message.Message):
    __slots__ = (
        "id",
        "type",
        "name",
        "description",
        "created_by",
        "threshold",
        "chart_monitor",
        "healthcheck_monitor",
        "logs_monitor",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    CHART_MONITOR_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECK_MONITOR_FIELD_NUMBER: _ClassVar[int]
    LOGS_MONITOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    name: str
    description: str
    created_by: str
    threshold: Threshold
    chart_monitor: ChartMonitor
    healthcheck_monitor: HealthcheckMonitor
    logs_monitor: LogsMonitor
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        threshold: _Optional[_Union[Threshold, _Mapping]] = ...,
        chart_monitor: _Optional[_Union[ChartMonitor, _Mapping]] = ...,
        healthcheck_monitor: _Optional[_Union[HealthcheckMonitor, _Mapping]] = ...,
        logs_monitor: _Optional[_Union[LogsMonitor, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
