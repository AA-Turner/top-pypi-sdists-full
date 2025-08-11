from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
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

class PodRequestGrouping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POD_REQUEST_GROUPING_UNSPECIFIED: _ClassVar[PodRequestGrouping]
    POD_REQUEST_GROUPING_NAMESPACE: _ClassVar[PodRequestGrouping]
    POD_REQUEST_GROUPING_CLUSTER: _ClassVar[PodRequestGrouping]
    POD_REQUEST_GROUPING_ENVIRONMENT: _ClassVar[PodRequestGrouping]
    POD_REQUEST_GROUPING_SERVICE: _ClassVar[PodRequestGrouping]

class PodRequestResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POD_REQUEST_RESOURCE_TYPE_UNSPECIFIED: _ClassVar[PodRequestResourceType]
    POD_REQUEST_RESOURCE_TYPE_CPU: _ClassVar[PodRequestResourceType]
    POD_REQUEST_RESOURCE_TYPE_MEMORY: _ClassVar[PodRequestResourceType]
    POD_REQUEST_RESOURCE_TYPE_EPHEMERAL_STORAGE: _ClassVar[PodRequestResourceType]

POD_REQUEST_GROUPING_UNSPECIFIED: PodRequestGrouping
POD_REQUEST_GROUPING_NAMESPACE: PodRequestGrouping
POD_REQUEST_GROUPING_CLUSTER: PodRequestGrouping
POD_REQUEST_GROUPING_ENVIRONMENT: PodRequestGrouping
POD_REQUEST_GROUPING_SERVICE: PodRequestGrouping
POD_REQUEST_RESOURCE_TYPE_UNSPECIFIED: PodRequestResourceType
POD_REQUEST_RESOURCE_TYPE_CPU: PodRequestResourceType
POD_REQUEST_RESOURCE_TYPE_MEMORY: PodRequestResourceType
POD_REQUEST_RESOURCE_TYPE_EPHEMERAL_STORAGE: PodRequestResourceType

class GetPodRequestChartsRequest(_message.Message):
    __slots__ = ("start_timestamp_inclusive", "end_timestamp_exclusive", "window_period", "grouping", "resource_types")
    START_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    GROUPING_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPES_FIELD_NUMBER: _ClassVar[int]
    start_timestamp_inclusive: _timestamp_pb2.Timestamp
    end_timestamp_exclusive: _timestamp_pb2.Timestamp
    window_period: _duration_pb2.Duration
    grouping: PodRequestGrouping
    resource_types: _containers.RepeatedScalarFieldContainer[PodRequestResourceType]
    def __init__(
        self,
        start_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        grouping: _Optional[_Union[PodRequestGrouping, str]] = ...,
        resource_types: _Optional[_Iterable[_Union[PodRequestResourceType, str]]] = ...,
    ) -> None: ...

class GetPodRequestChartsResponse(_message.Message):
    __slots__ = ("charts",)
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_densetimeserieschart_pb2.DenseTimeSeriesChart]
    def __init__(
        self, charts: _Optional[_Iterable[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]]] = ...
    ) -> None: ...
