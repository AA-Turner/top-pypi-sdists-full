from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
from chalk._gen.chalk.common.v1 import chart_pb2 as _chart_pb2
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

class FeatureValueAggregation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEATURE_VALUE_AGGREGATION_UNSPECIFIED: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_UNIQUE_VALUES: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_TOTAL_OBSERVATIONS: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_NULL_PERCENTAGE: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_MAX_VALUE: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_MIN_VALUE: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_AVERAGE: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_UNIQUE_PKEYS: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_P95: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_P75: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_P50: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_P25: _ClassVar[FeatureValueAggregation]
    FEATURE_VALUE_AGGREGATION_P05: _ClassVar[FeatureValueAggregation]

FEATURE_VALUE_AGGREGATION_UNSPECIFIED: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_UNIQUE_VALUES: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_TOTAL_OBSERVATIONS: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_NULL_PERCENTAGE: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_MAX_VALUE: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_MIN_VALUE: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_AVERAGE: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_UNIQUE_PKEYS: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_P95: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_P75: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_P50: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_P25: FeatureValueAggregation
FEATURE_VALUE_AGGREGATION_P05: FeatureValueAggregation

class GetFeatureValuesChartRequest(_message.Message):
    __slots__ = ("fqn", "aggregate_by", "window_period", "start_ms", "end_ms")
    FQN_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BY_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    START_MS_FIELD_NUMBER: _ClassVar[int]
    END_MS_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    aggregate_by: _containers.RepeatedScalarFieldContainer[FeatureValueAggregation]
    window_period: str
    start_ms: int
    end_ms: int
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        aggregate_by: _Optional[_Iterable[_Union[FeatureValueAggregation, str]]] = ...,
        window_period: _Optional[str] = ...,
        start_ms: _Optional[int] = ...,
        end_ms: _Optional[int] = ...,
    ) -> None: ...

class GetFeatureValuesChartResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _chart_pb2.Chart
    def __init__(self, chart: _Optional[_Union[_chart_pb2.Chart, _Mapping]] = ...) -> None: ...

class GetFeatureValuesTimeSeriesChartRequest(_message.Message):
    __slots__ = ("fqn", "aggregate_by", "window_period", "start_timestamp_inclusive", "end_timestamp_exclusive")
    FQN_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BY_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    aggregate_by: _containers.RepeatedScalarFieldContainer[FeatureValueAggregation]
    window_period: _duration_pb2.Duration
    start_timestamp_inclusive: _timestamp_pb2.Timestamp
    end_timestamp_exclusive: _timestamp_pb2.Timestamp
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        aggregate_by: _Optional[_Iterable[_Union[FeatureValueAggregation, str]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        start_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetFeatureValuesTimeSeriesChartResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetFeatureValuesTimeSeriesChartV2Request(_message.Message):
    __slots__ = ("fqn", "aggregate_by", "window_period", "start_timestamp_inclusive", "end_timestamp_exclusive")
    FQN_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BY_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    aggregate_by: _containers.RepeatedScalarFieldContainer[FeatureValueAggregation]
    window_period: _duration_pb2.Duration
    start_timestamp_inclusive: _timestamp_pb2.Timestamp
    end_timestamp_exclusive: _timestamp_pb2.Timestamp
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        aggregate_by: _Optional[_Iterable[_Union[FeatureValueAggregation, str]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        start_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetFeatureValuesTimeSeriesChartV2Response(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...
