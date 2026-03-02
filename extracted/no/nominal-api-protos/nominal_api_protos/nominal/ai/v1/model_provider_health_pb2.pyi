import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DegradationReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEGRADATION_REASON_UNSPECIFIED: _ClassVar[DegradationReason]
    DEGRADATION_REASON_HIGH_LATENCY: _ClassVar[DegradationReason]
    DEGRADATION_REASON_FAILURES: _ClassVar[DegradationReason]
    DEGRADATION_REASON_HIGH_LATENCY_AND_FAILURES: _ClassVar[DegradationReason]
DEGRADATION_REASON_UNSPECIFIED: DegradationReason
DEGRADATION_REASON_HIGH_LATENCY: DegradationReason
DEGRADATION_REASON_FAILURES: DegradationReason
DEGRADATION_REASON_HIGH_LATENCY_AND_FAILURES: DegradationReason

class GetProviderStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetProviderStatusResponse(_message.Message):
    __slots__ = ("timestamp", "last_status", "aggregated_status_over_last_30m", "aggregated_status")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_STATUS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATED_STATUS_OVER_LAST_30M_FIELD_NUMBER: _ClassVar[int]
    AGGREGATED_STATUS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    last_status: ProviderStatus
    aggregated_status_over_last_30m: ProviderStatus
    aggregated_status: ProviderStatus
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_status: _Optional[_Union[ProviderStatus, _Mapping]] = ..., aggregated_status_over_last_30m: _Optional[_Union[ProviderStatus, _Mapping]] = ..., aggregated_status: _Optional[_Union[ProviderStatus, _Mapping]] = ...) -> None: ...

class ProviderStatus(_message.Message):
    __slots__ = ("healthy", "degraded")
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    healthy: Healthy
    degraded: Degraded
    def __init__(self, healthy: _Optional[_Union[Healthy, _Mapping]] = ..., degraded: _Optional[_Union[Degraded, _Mapping]] = ...) -> None: ...

class Healthy(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Degraded(_message.Message):
    __slots__ = ("reason",)
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: DegradationReason
    def __init__(self, reason: _Optional[_Union[DegradationReason, str]] = ...) -> None: ...

class ProviderMetrics(_message.Message):
    __slots__ = ("time_to_first_token_ms", "total_time_ms")
    TIME_TO_FIRST_TOKEN_MS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    time_to_first_token_ms: int
    total_time_ms: int
    def __init__(self, time_to_first_token_ms: _Optional[int] = ..., total_time_ms: _Optional[int] = ...) -> None: ...
