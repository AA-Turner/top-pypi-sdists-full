from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

AVG_LENGTH: MetricType
AVG_VALUE: MetricType
COUNT_DISTINCT: MetricType
COUNT_NULLS: MetricType
COUNT_ROWS: MetricType
COUNT_ZEROS: MetricType
DESCRIPTOR: _descriptor.FileDescriptor
MAX_VALUE: MetricType
METRIC_STATUS_AVAILABLE: MetricStatus
METRIC_STATUS_NO_MATERIALIZATION: MetricStatus
METRIC_STATUS_UNAVAILABLE: MetricStatus
METRIC_STATUS_UNKNOWN: MetricStatus
METRIC_TYPE_UNKNOWN: MetricType
MIN_VALUE: MetricType
STDDEV_SAMPLE: MetricType
VAR_SAMPLE: MetricType

class FeatureMetric(_message.Message):
    __slots__ = ["column_name", "feature_name", "metric_type"]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    feature_name: str
    metric_type: MetricType
    def __init__(self, metric_type: _Optional[_Union[MetricType, str]] = ..., feature_name: _Optional[str] = ..., column_name: _Optional[str] = ...) -> None: ...

class Metric(_message.Message):
    __slots__ = ["creation_time", "expression", "input_column_names", "interval", "last_update_time", "name", "window"]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    INPUT_COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    creation_time: _timestamp_pb2.Timestamp
    expression: str
    input_column_names: _containers.RepeatedScalarFieldContainer[str]
    interval: _duration_pb2.Duration
    last_update_time: _timestamp_pb2.Timestamp
    name: str
    window: _duration_pb2.Duration
    def __init__(self, name: _Optional[str] = ..., expression: _Optional[str] = ..., window: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., interval: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., input_column_names: _Optional[_Iterable[str]] = ..., creation_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MetricDataPoint(_message.Message):
    __slots__ = ["interval_start_time", "materialization_run_id", "materialization_task_attempt_url", "metric_status", "metric_values"]
    INTERVAL_START_TIME_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_TASK_ATTEMPT_URL_FIELD_NUMBER: _ClassVar[int]
    METRIC_STATUS_FIELD_NUMBER: _ClassVar[int]
    METRIC_VALUES_FIELD_NUMBER: _ClassVar[int]
    interval_start_time: _timestamp_pb2.Timestamp
    materialization_run_id: str
    materialization_task_attempt_url: str
    metric_status: MetricStatus
    metric_values: _containers.RepeatedCompositeFieldContainer[MetricValue]
    def __init__(self, interval_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., metric_values: _Optional[_Iterable[_Union[MetricValue, _Mapping]]] = ..., materialization_run_id: _Optional[str] = ..., materialization_task_attempt_url: _Optional[str] = ..., metric_status: _Optional[_Union[MetricStatus, str]] = ...) -> None: ...

class MetricValue(_message.Message):
    __slots__ = ["feature_name", "value"]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    feature_name: str
    value: str
    def __init__(self, feature_name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class MetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MetricStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
