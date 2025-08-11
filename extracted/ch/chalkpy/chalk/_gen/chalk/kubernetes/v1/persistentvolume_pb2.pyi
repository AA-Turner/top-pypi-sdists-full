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

class ChalkKubernetesPersistentVolume(_message.Message):
    __slots__ = ("spec", "metrics")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    spec: ChalkKubernetesPersistentVolumeSpec
    metrics: ChalkKubernetesPersistentVolumeMetrics
    def __init__(
        self,
        spec: _Optional[_Union[ChalkKubernetesPersistentVolumeSpec, _Mapping]] = ...,
        metrics: _Optional[_Union[ChalkKubernetesPersistentVolumeMetrics, _Mapping]] = ...,
    ) -> None: ...

class ChalkKubernetesPersistentVolumeSpec(_message.Message):
    __slots__ = ("storage_class", "name", "access_modes", "capacity", "status", "reclaim_policy", "claim")
    STORAGE_CLASS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACCESS_MODES_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RECLAIM_POLICY_FIELD_NUMBER: _ClassVar[int]
    CLAIM_FIELD_NUMBER: _ClassVar[int]
    storage_class: str
    name: str
    access_modes: _containers.RepeatedScalarFieldContainer[str]
    capacity: str
    status: str
    reclaim_policy: str
    claim: str
    def __init__(
        self,
        storage_class: _Optional[str] = ...,
        name: _Optional[str] = ...,
        access_modes: _Optional[_Iterable[str]] = ...,
        capacity: _Optional[str] = ...,
        status: _Optional[str] = ...,
        reclaim_policy: _Optional[str] = ...,
        claim: _Optional[str] = ...,
    ) -> None: ...

class ChalkKubernetesPersistentVolumeMetrics(_message.Message):
    __slots__ = ("capacity_bytes", "used_bytes", "available_bytes")
    CAPACITY_BYTES_FIELD_NUMBER: _ClassVar[int]
    USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_BYTES_FIELD_NUMBER: _ClassVar[int]
    capacity_bytes: float
    used_bytes: float
    available_bytes: float
    def __init__(
        self,
        capacity_bytes: _Optional[float] = ...,
        used_bytes: _Optional[float] = ...,
        available_bytes: _Optional[float] = ...,
    ) -> None: ...
