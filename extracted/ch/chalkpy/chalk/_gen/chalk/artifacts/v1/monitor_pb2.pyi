from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
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

class TriggerThreshold(_message.Message):
    __slots__ = ("severity_kind", "threshold_kind", "threshold_value", "description")
    SEVERITY_KIND_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_KIND_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    severity_kind: _chart_pb2.AlertSeverityKind
    threshold_kind: _chart_pb2.ThresholdKind
    threshold_value: float
    description: str
    def __init__(
        self,
        severity_kind: _Optional[_Union[_chart_pb2.AlertSeverityKind, str]] = ...,
        threshold_kind: _Optional[_Union[_chart_pb2.ThresholdKind, str]] = ...,
        threshold_value: _Optional[float] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class TieredFrequencyTrigger(_message.Message):
    __slots__ = ("trigger_thresholds",)
    TRIGGER_THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    trigger_thresholds: _containers.RepeatedCompositeFieldContainer[TriggerThreshold]
    def __init__(self, trigger_thresholds: _Optional[_Iterable[_Union[TriggerThreshold, _Mapping]]] = ...) -> None: ...

class BooleanTrigger(_message.Message):
    __slots__ = ("severity_kind", "description")
    SEVERITY_KIND_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    severity_kind: _chart_pb2.AlertSeverityKind
    description: str
    def __init__(
        self,
        severity_kind: _Optional[_Union[_chart_pb2.AlertSeverityKind, str]] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class LogsMonitor(_message.Message):
    __slots__ = ("query_string", "tags", "window_period", "trigger")
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
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    query_string: str
    tags: _containers.ScalarMap[str, str]
    window_period: str
    trigger: TieredFrequencyTrigger
    def __init__(
        self,
        query_string: _Optional[str] = ...,
        tags: _Optional[_Mapping[str, str]] = ...,
        window_period: _Optional[str] = ...,
        trigger: _Optional[_Union[TieredFrequencyTrigger, _Mapping]] = ...,
    ) -> None: ...

class HealthcheckMonitor(_message.Message):
    __slots__ = ("healthcheck_name", "trigger")
    HEALTHCHECK_NAME_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    healthcheck_name: str
    trigger: BooleanTrigger
    def __init__(
        self, healthcheck_name: _Optional[str] = ..., trigger: _Optional[_Union[BooleanTrigger, _Mapping]] = ...
    ) -> None: ...

class ChartMonitor(_message.Message):
    __slots__ = ("chart_id", "series_name", "trigger")
    CHART_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_NAME_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    chart_id: str
    series_name: str
    trigger: TieredFrequencyTrigger
    def __init__(
        self,
        chart_id: _Optional[str] = ...,
        series_name: _Optional[str] = ...,
        trigger: _Optional[_Union[TieredFrequencyTrigger, _Mapping]] = ...,
    ) -> None: ...

class Monitor(_message.Message):
    __slots__ = (
        "id",
        "type",
        "alert_owners",
        "alert_channels",
        "name",
        "created_by",
        "chart_monitor",
        "healthcheck_monitor",
        "logs_monitor",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ALERT_OWNERS_FIELD_NUMBER: _ClassVar[int]
    ALERT_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CHART_MONITOR_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECK_MONITOR_FIELD_NUMBER: _ClassVar[int]
    LOGS_MONITOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    alert_owners: _containers.RepeatedScalarFieldContainer[str]
    alert_channels: _containers.RepeatedScalarFieldContainer[str]
    name: str
    created_by: str
    chart_monitor: ChartMonitor
    healthcheck_monitor: HealthcheckMonitor
    logs_monitor: LogsMonitor
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        type: _Optional[str] = ...,
        alert_owners: _Optional[_Iterable[str]] = ...,
        alert_channels: _Optional[_Iterable[str]] = ...,
        name: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        chart_monitor: _Optional[_Union[ChartMonitor, _Mapping]] = ...,
        healthcheck_monitor: _Optional[_Union[HealthcheckMonitor, _Mapping]] = ...,
        logs_monitor: _Optional[_Union[LogsMonitor, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
