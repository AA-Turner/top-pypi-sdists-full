from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class HealthCheckStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_CHECK_STATUS_UNSPECIFIED: _ClassVar[HealthCheckStatus]
    HEALTH_CHECK_STATUS_OK: _ClassVar[HealthCheckStatus]
    HEALTH_CHECK_STATUS_FAILING: _ClassVar[HealthCheckStatus]

HEALTH_CHECK_STATUS_UNSPECIFIED: HealthCheckStatus
HEALTH_CHECK_STATUS_OK: HealthCheckStatus
HEALTH_CHECK_STATUS_FAILING: HealthCheckStatus

class HealthCheck(_message.Message):
    __slots__ = ("name", "status", "message", "latency", "kube_data", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    KUBE_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: HealthCheckStatus
    message: str
    latency: _duration_pb2.Duration
    kube_data: _struct_pb2.Struct
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        status: _Optional[_Union[HealthCheckStatus, str]] = ...,
        message: _Optional[str] = ...,
        latency: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        kube_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class HealthCheckFilters(_message.Message):
    __slots__ = ("name", "status")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    name: _containers.RepeatedScalarFieldContainer[str]
    status: _containers.RepeatedScalarFieldContainer[HealthCheckStatus]
    def __init__(
        self, name: _Optional[_Iterable[str]] = ..., status: _Optional[_Iterable[_Union[HealthCheckStatus, str]]] = ...
    ) -> None: ...

class CheckHealthRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: HealthCheckFilters
    def __init__(self, filters: _Optional[_Union[HealthCheckFilters, _Mapping]] = ...) -> None: ...

class CheckHealthResponse(_message.Message):
    __slots__ = ("checks",)
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    checks: _containers.RepeatedCompositeFieldContainer[HealthCheck]
    def __init__(self, checks: _Optional[_Iterable[_Union[HealthCheck, _Mapping]]] = ...) -> None: ...

class GetHealthRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: HealthCheckFilters
    def __init__(self, filters: _Optional[_Union[HealthCheckFilters, _Mapping]] = ...) -> None: ...

class GetHealthResponse(_message.Message):
    __slots__ = ("checks",)
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    checks: _containers.RepeatedCompositeFieldContainer[HealthCheck]
    def __init__(self, checks: _Optional[_Iterable[_Union[HealthCheck, _Mapping]]] = ...) -> None: ...

class GetClusterMetricsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClusterMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: str
    def __init__(self, metrics: _Optional[str] = ...) -> None: ...
