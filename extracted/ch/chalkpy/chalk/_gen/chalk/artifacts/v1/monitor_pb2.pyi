from chalk._gen.chalk.artifacts.v1 import alert_channel_pb2 as _alert_channel_pb2
from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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
    MONITOR_TYPE_SQL_BAD_ROWS: _ClassVar[MonitorType]
    MONITOR_TYPE_DATA_SOURCE: _ClassVar[MonitorType]
    MONITOR_TYPE_FEATURE_DRIFT: _ClassVar[MonitorType]

MONITOR_TYPE_UNSPECIFIED: MonitorType
MONITOR_TYPE_CHART: MonitorType
MONITOR_TYPE_LOG: MonitorType
MONITOR_TYPE_HEALTHCHECK: MonitorType
MONITOR_TYPE_SQL_BAD_ROWS: MonitorType
MONITOR_TYPE_DATA_SOURCE: MonitorType
MONITOR_TYPE_FEATURE_DRIFT: MonitorType

class LogsMonitor(_message.Message):
    __slots__ = ("query_string", "window_period", "data_source")
    QUERY_STRING_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    query_string: str
    window_period: _duration_pb2.Duration
    data_source: str
    def __init__(
        self,
        query_string: _Optional[str] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        data_source: _Optional[str] = ...,
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

class SqlBadRowsMonitor(_message.Message):
    __slots__ = ("query", "datasource_name", "resource_group")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    DATASOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    query: str
    datasource_name: str
    resource_group: str
    def __init__(
        self, query: _Optional[str] = ..., datasource_name: _Optional[str] = ..., resource_group: _Optional[str] = ...
    ) -> None: ...

class DataSourceMonitor(_message.Message):
    __slots__ = ("integration_id", "name")
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    integration_id: str
    name: str
    def __init__(self, integration_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class FeatureDriftMonitor(_message.Message):
    __slots__ = ("feature_fqn", "window_period", "baseline", "test")
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    BASELINE_FIELD_NUMBER: _ClassVar[int]
    TEST_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    window_period: _duration_pb2.Duration
    baseline: FeatureDriftBaseline
    test: FeatureDriftTest
    def __init__(
        self,
        feature_fqn: _Optional[str] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        baseline: _Optional[_Union[FeatureDriftBaseline, _Mapping]] = ...,
        test: _Optional[_Union[FeatureDriftTest, _Mapping]] = ...,
    ) -> None: ...

class FeatureDriftBaseline(_message.Message):
    __slots__ = ("dataset_revision",)
    DATASET_REVISION_FIELD_NUMBER: _ClassVar[int]
    dataset_revision: DatasetRevisionBaseline
    def __init__(self, dataset_revision: _Optional[_Union[DatasetRevisionBaseline, _Mapping]] = ...) -> None: ...

class DatasetRevisionBaseline(_message.Message):
    __slots__ = ("dataset_id", "dataset_name", "revision_id")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    dataset_name: str
    revision_id: str
    def __init__(
        self, dataset_id: _Optional[str] = ..., dataset_name: _Optional[str] = ..., revision_id: _Optional[str] = ...
    ) -> None: ...

class FeatureDriftTest(_message.Message):
    __slots__ = ("kolmogorov_smirnov",)
    KOLMOGOROV_SMIRNOV_FIELD_NUMBER: _ClassVar[int]
    kolmogorov_smirnov: KolmogorovSmirnovTest
    def __init__(self, kolmogorov_smirnov: _Optional[_Union[KolmogorovSmirnovTest, _Mapping]] = ...) -> None: ...

class KolmogorovSmirnovTest(_message.Message):
    __slots__ = ("alpha",)
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    alpha: float
    def __init__(self, alpha: _Optional[float] = ...) -> None: ...

class FeatureDriftTestResult(_message.Message):
    __slots__ = ("drifted", "baseline_sample_count", "window_sample_count", "kolmogorov_smirnov")
    DRIFTED_FIELD_NUMBER: _ClassVar[int]
    BASELINE_SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    WINDOW_SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    KOLMOGOROV_SMIRNOV_FIELD_NUMBER: _ClassVar[int]
    drifted: bool
    baseline_sample_count: int
    window_sample_count: int
    kolmogorov_smirnov: KolmogorovSmirnovResult
    def __init__(
        self,
        drifted: bool = ...,
        baseline_sample_count: _Optional[int] = ...,
        window_sample_count: _Optional[int] = ...,
        kolmogorov_smirnov: _Optional[_Union[KolmogorovSmirnovResult, _Mapping]] = ...,
    ) -> None: ...

class KolmogorovSmirnovResult(_message.Message):
    __slots__ = ("statistic", "critical_value")
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    statistic: float
    critical_value: float
    def __init__(self, statistic: _Optional[float] = ..., critical_value: _Optional[float] = ...) -> None: ...

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
        "evaluation_schedule",
        "chart_monitor",
        "healthcheck_monitor",
        "logs_monitor",
        "sql_bad_rows_monitor",
        "data_source_monitor",
        "feature_drift_monitor",
        "created_at",
        "updated_at",
        "muted_until",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    CHART_MONITOR_FIELD_NUMBER: _ClassVar[int]
    HEALTHCHECK_MONITOR_FIELD_NUMBER: _ClassVar[int]
    LOGS_MONITOR_FIELD_NUMBER: _ClassVar[int]
    SQL_BAD_ROWS_MONITOR_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_MONITOR_FIELD_NUMBER: _ClassVar[int]
    FEATURE_DRIFT_MONITOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    MUTED_UNTIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    name: str
    description: str
    created_by: str
    threshold: Threshold
    evaluation_schedule: str
    chart_monitor: ChartMonitor
    healthcheck_monitor: HealthcheckMonitor
    logs_monitor: LogsMonitor
    sql_bad_rows_monitor: SqlBadRowsMonitor
    data_source_monitor: DataSourceMonitor
    feature_drift_monitor: FeatureDriftMonitor
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    muted_until: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        threshold: _Optional[_Union[Threshold, _Mapping]] = ...,
        evaluation_schedule: _Optional[str] = ...,
        chart_monitor: _Optional[_Union[ChartMonitor, _Mapping]] = ...,
        healthcheck_monitor: _Optional[_Union[HealthcheckMonitor, _Mapping]] = ...,
        logs_monitor: _Optional[_Union[LogsMonitor, _Mapping]] = ...,
        sql_bad_rows_monitor: _Optional[_Union[SqlBadRowsMonitor, _Mapping]] = ...,
        data_source_monitor: _Optional[_Union[DataSourceMonitor, _Mapping]] = ...,
        feature_drift_monitor: _Optional[_Union[FeatureDriftMonitor, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        muted_until: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
