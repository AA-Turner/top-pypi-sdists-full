from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesScaledObjectTargetRef(_message.Message):
    __slots__ = ("name", "api_version", "kind", "env_source_container_name")
    NAME_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ENV_SOURCE_CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    api_version: str
    kind: str
    env_source_container_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        api_version: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        env_source_container_name: _Optional[str] = ...,
    ) -> None: ...

class KubernetesScaledObjectStatus(_message.Message):
    __slots__ = ("scale_target_kind", "original_replica_count", "last_active_time", "paused_replica_count", "hpa_name")
    SCALE_TARGET_KIND_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    PAUSED_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    HPA_NAME_FIELD_NUMBER: _ClassVar[int]
    scale_target_kind: str
    original_replica_count: int
    last_active_time: _timestamp_pb2.Timestamp
    paused_replica_count: int
    hpa_name: str
    def __init__(
        self,
        scale_target_kind: _Optional[str] = ...,
        original_replica_count: _Optional[int] = ...,
        last_active_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        paused_replica_count: _Optional[int] = ...,
        hpa_name: _Optional[str] = ...,
    ) -> None: ...

class KubernetesScaledObjectSpec(_message.Message):
    __slots__ = (
        "scale_target_ref",
        "polling_interval",
        "initial_cooldown_period",
        "cooldown_period",
        "idle_replica_count",
        "max_replica_count",
    )
    SCALE_TARGET_REF_FIELD_NUMBER: _ClassVar[int]
    POLLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    INITIAL_COOLDOWN_PERIOD_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_PERIOD_FIELD_NUMBER: _ClassVar[int]
    IDLE_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    scale_target_ref: KubernetesScaledObjectTargetRef
    polling_interval: int
    initial_cooldown_period: int
    cooldown_period: int
    idle_replica_count: int
    max_replica_count: int
    def __init__(
        self,
        scale_target_ref: _Optional[_Union[KubernetesScaledObjectTargetRef, _Mapping]] = ...,
        polling_interval: _Optional[int] = ...,
        initial_cooldown_period: _Optional[int] = ...,
        cooldown_period: _Optional[int] = ...,
        idle_replica_count: _Optional[int] = ...,
        max_replica_count: _Optional[int] = ...,
    ) -> None: ...

class KubernetesScaledObjectData(_message.Message):
    __slots__ = ("spec", "status")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    spec: KubernetesScaledObjectSpec
    status: KubernetesScaledObjectStatus
    def __init__(
        self,
        spec: _Optional[_Union[KubernetesScaledObjectSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesScaledObjectStatus, _Mapping]] = ...,
    ) -> None: ...
