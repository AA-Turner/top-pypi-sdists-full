from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class HostPoolPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HOST_POOL_PHASE_UNSPECIFIED: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_INACTIVE: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_PENDING: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_RUNNING: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_DEGRADED: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_ERROR: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_UNKNOWN: _ClassVar[HostPoolPhase]

HOST_POOL_PHASE_UNSPECIFIED: HostPoolPhase
HOST_POOL_PHASE_INACTIVE: HostPoolPhase
HOST_POOL_PHASE_PENDING: HostPoolPhase
HOST_POOL_PHASE_RUNNING: HostPoolPhase
HOST_POOL_PHASE_DEGRADED: HostPoolPhase
HOST_POOL_PHASE_ERROR: HostPoolPhase
HOST_POOL_PHASE_UNKNOWN: HostPoolPhase

class HostPoolSpec(_message.Message):
    __slots__ = (
        "name",
        "min_hosts",
        "max_hosts",
        "idle_timeout",
        "cpu",
        "memory",
        "machine_family",
        "compute_class",
        "gpu",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    MIN_HOSTS_FIELD_NUMBER: _ClassVar[int]
    MAX_HOSTS_FIELD_NUMBER: _ClassVar[int]
    IDLE_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    MACHINE_FAMILY_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_CLASS_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    name: str
    min_hosts: int
    max_hosts: int
    idle_timeout: _duration_pb2.Duration
    cpu: str
    memory: str
    machine_family: str
    compute_class: str
    gpu: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        min_hosts: _Optional[int] = ...,
        max_hosts: _Optional[int] = ...,
        idle_timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        cpu: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        machine_family: _Optional[str] = ...,
        compute_class: _Optional[str] = ...,
        gpu: _Optional[str] = ...,
    ) -> None: ...

class HostPool(_message.Message):
    __slots__ = ("id", "team_id", "environment_id", "cluster_id", "spec", "created_at", "updated_at", "system_managed")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_MANAGED_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    environment_id: str
    cluster_id: str
    spec: HostPoolSpec
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    system_managed: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        cluster_id: _Optional[str] = ...,
        spec: _Optional[_Union[HostPoolSpec, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        system_managed: bool = ...,
    ) -> None: ...

class CreateEnvironmentHostPoolRequest(_message.Message):
    __slots__ = ("spec",)
    SPEC_FIELD_NUMBER: _ClassVar[int]
    spec: HostPoolSpec
    def __init__(self, spec: _Optional[_Union[HostPoolSpec, _Mapping]] = ...) -> None: ...

class CreateEnvironmentHostPoolResponse(_message.Message):
    __slots__ = ("host_pool",)
    HOST_POOL_FIELD_NUMBER: _ClassVar[int]
    host_pool: HostPool
    def __init__(self, host_pool: _Optional[_Union[HostPool, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentHostPoolRequest(_message.Message):
    __slots__ = ("id", "spec", "update_mask")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    spec: HostPoolSpec
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        id: _Optional[str] = ...,
        spec: _Optional[_Union[HostPoolSpec, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateEnvironmentHostPoolResponse(_message.Message):
    __slots__ = ("host_pool",)
    HOST_POOL_FIELD_NUMBER: _ClassVar[int]
    host_pool: HostPool
    def __init__(self, host_pool: _Optional[_Union[HostPool, _Mapping]] = ...) -> None: ...

class DeleteEnvironmentHostPoolRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteEnvironmentHostPoolResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateClusterHostPoolRequest(_message.Message):
    __slots__ = ("cluster_id", "spec")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    spec: HostPoolSpec
    def __init__(
        self, cluster_id: _Optional[str] = ..., spec: _Optional[_Union[HostPoolSpec, _Mapping]] = ...
    ) -> None: ...

class CreateClusterHostPoolResponse(_message.Message):
    __slots__ = ("host_pool",)
    HOST_POOL_FIELD_NUMBER: _ClassVar[int]
    host_pool: HostPool
    def __init__(self, host_pool: _Optional[_Union[HostPool, _Mapping]] = ...) -> None: ...

class UpdateClusterHostPoolRequest(_message.Message):
    __slots__ = ("id", "spec", "update_mask")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    spec: HostPoolSpec
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        id: _Optional[str] = ...,
        spec: _Optional[_Union[HostPoolSpec, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateClusterHostPoolResponse(_message.Message):
    __slots__ = ("host_pool",)
    HOST_POOL_FIELD_NUMBER: _ClassVar[int]
    host_pool: HostPool
    def __init__(self, host_pool: _Optional[_Union[HostPool, _Mapping]] = ...) -> None: ...

class DeleteClusterHostPoolRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteClusterHostPoolResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetHostPoolRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetHostPoolResponse(_message.Message):
    __slots__ = ("host_pool",)
    HOST_POOL_FIELD_NUMBER: _ClassVar[int]
    host_pool: HostPool
    def __init__(self, host_pool: _Optional[_Union[HostPool, _Mapping]] = ...) -> None: ...

class ListHostPoolsRequest(_message.Message):
    __slots__ = ("environment_id", "cluster_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cluster_id: str
    def __init__(self, environment_id: _Optional[str] = ..., cluster_id: _Optional[str] = ...) -> None: ...

class ListHostPoolsResponse(_message.Message):
    __slots__ = ("host_pools",)
    HOST_POOLS_FIELD_NUMBER: _ClassVar[int]
    host_pools: _containers.RepeatedCompositeFieldContainer[HostPool]
    def __init__(self, host_pools: _Optional[_Iterable[_Union[HostPool, _Mapping]]] = ...) -> None: ...

class HostPoolResources(_message.Message):
    __slots__ = ("cpu_cores", "memory_bytes")
    CPU_CORES_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    cpu_cores: float
    memory_bytes: int
    def __init__(self, cpu_cores: _Optional[float] = ..., memory_bytes: _Optional[int] = ...) -> None: ...

class HostCapacity(_message.Message):
    __slots__ = ("host_id", "ready", "placed_containers", "capacity", "allocated", "available")
    HOST_ID_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    PLACED_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    ALLOCATED_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    host_id: str
    ready: bool
    placed_containers: int
    capacity: HostPoolResources
    allocated: HostPoolResources
    available: HostPoolResources
    def __init__(
        self,
        host_id: _Optional[str] = ...,
        ready: bool = ...,
        placed_containers: _Optional[int] = ...,
        capacity: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        allocated: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        available: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
    ) -> None: ...

class HostPoolCapacity(_message.Message):
    __slots__ = (
        "host_pool_id",
        "name",
        "cluster_scoped",
        "system_managed",
        "min_hosts",
        "max_hosts",
        "idle_timeout",
        "cpu",
        "memory",
        "phase",
        "message",
        "desired_hosts",
        "ready_hosts",
        "idle_hosts",
        "idle_since",
        "ready",
        "allocated",
        "available",
        "at_max_scale",
        "largest_placeable",
        "largest_placeable_at_max_scale",
        "placed_containers",
        "placed_containers_in_environment",
        "hosts",
    )
    HOST_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_SCOPED_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_MANAGED_FIELD_NUMBER: _ClassVar[int]
    MIN_HOSTS_FIELD_NUMBER: _ClassVar[int]
    MAX_HOSTS_FIELD_NUMBER: _ClassVar[int]
    IDLE_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DESIRED_HOSTS_FIELD_NUMBER: _ClassVar[int]
    READY_HOSTS_FIELD_NUMBER: _ClassVar[int]
    IDLE_HOSTS_FIELD_NUMBER: _ClassVar[int]
    IDLE_SINCE_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ALLOCATED_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    AT_MAX_SCALE_FIELD_NUMBER: _ClassVar[int]
    LARGEST_PLACEABLE_FIELD_NUMBER: _ClassVar[int]
    LARGEST_PLACEABLE_AT_MAX_SCALE_FIELD_NUMBER: _ClassVar[int]
    PLACED_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    PLACED_CONTAINERS_IN_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    host_pool_id: str
    name: str
    cluster_scoped: bool
    system_managed: bool
    min_hosts: int
    max_hosts: int
    idle_timeout: _duration_pb2.Duration
    cpu: str
    memory: str
    phase: HostPoolPhase
    message: str
    desired_hosts: int
    ready_hosts: int
    idle_hosts: int
    idle_since: _timestamp_pb2.Timestamp
    ready: HostPoolResources
    allocated: HostPoolResources
    available: HostPoolResources
    at_max_scale: HostPoolResources
    largest_placeable: HostPoolResources
    largest_placeable_at_max_scale: HostPoolResources
    placed_containers: int
    placed_containers_in_environment: int
    hosts: _containers.RepeatedCompositeFieldContainer[HostCapacity]
    def __init__(
        self,
        host_pool_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        cluster_scoped: bool = ...,
        system_managed: bool = ...,
        min_hosts: _Optional[int] = ...,
        max_hosts: _Optional[int] = ...,
        idle_timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        cpu: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        phase: _Optional[_Union[HostPoolPhase, str]] = ...,
        message: _Optional[str] = ...,
        desired_hosts: _Optional[int] = ...,
        ready_hosts: _Optional[int] = ...,
        idle_hosts: _Optional[int] = ...,
        idle_since: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ready: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        allocated: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        available: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        at_max_scale: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        largest_placeable: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        largest_placeable_at_max_scale: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        placed_containers: _Optional[int] = ...,
        placed_containers_in_environment: _Optional[int] = ...,
        hosts: _Optional[_Iterable[_Union[HostCapacity, _Mapping]]] = ...,
    ) -> None: ...

class GetHostPoolCapacityRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetHostPoolCapacityResponse(_message.Message):
    __slots__ = ("host_pools", "pending_containers", "largest_pending_request", "observed_at")
    HOST_POOLS_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    LARGEST_PENDING_REQUEST_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    host_pools: _containers.RepeatedCompositeFieldContainer[HostPoolCapacity]
    pending_containers: int
    largest_pending_request: HostPoolResources
    observed_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        host_pools: _Optional[_Iterable[_Union[HostPoolCapacity, _Mapping]]] = ...,
        pending_containers: _Optional[int] = ...,
        largest_pending_request: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
