from google.protobuf import duration_pb2 as _duration_pb2
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

class AggregateTimeSeriesRule(_message.Message):
    __slots__ = ("aggregation", "bucket_duration", "dependent_features", "retention", "datetime_feature")
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_FIELD_NUMBER: _ClassVar[int]
    DEPENDENT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    RETENTION_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FEATURE_FIELD_NUMBER: _ClassVar[int]
    aggregation: str
    bucket_duration: _duration_pb2.Duration
    dependent_features: _containers.RepeatedScalarFieldContainer[str]
    retention: _duration_pb2.Duration
    datetime_feature: str
    def __init__(
        self,
        aggregation: _Optional[str] = ...,
        bucket_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        dependent_features: _Optional[_Iterable[str]] = ...,
        retention: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        datetime_feature: _Optional[str] = ...,
    ) -> None: ...

class AggregateTimeSeries(_message.Message):
    __slots__ = ("namespace", "aggregate_on", "group_by", "rules", "filters_description", "bucket_feature")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    FILTERS_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FEATURE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    aggregate_on: str
    group_by: _containers.RepeatedScalarFieldContainer[str]
    rules: _containers.RepeatedCompositeFieldContainer[AggregateTimeSeriesRule]
    filters_description: str
    bucket_feature: str
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        aggregate_on: _Optional[str] = ...,
        group_by: _Optional[_Iterable[str]] = ...,
        rules: _Optional[_Iterable[_Union[AggregateTimeSeriesRule, _Mapping]]] = ...,
        filters_description: _Optional[str] = ...,
        bucket_feature: _Optional[str] = ...,
    ) -> None: ...
