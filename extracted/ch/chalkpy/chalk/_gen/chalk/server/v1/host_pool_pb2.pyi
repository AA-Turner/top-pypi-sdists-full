from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import cloud_components_pb2 as _cloud_components_pb2
from chalk._gen.chalk.server.v1 import cluster_class_pb2 as _cluster_class_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.rpc import error_details_pb2 as _error_details_pb2
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

class HostPoolStorage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HOST_POOL_STORAGE_UNSPECIFIED: _ClassVar[HostPoolStorage]
    HOST_POOL_STORAGE_STANDARD: _ClassVar[HostPoolStorage]
    HOST_POOL_STORAGE_LOCAL_SSD: _ClassVar[HostPoolStorage]

class HostPoolPendingUpdateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HOST_POOL_PENDING_UPDATE_TYPE_UNSPECIFIED: _ClassVar[HostPoolPendingUpdateType]
    HOST_POOL_PENDING_UPDATE_TYPE_IMAGE: _ClassVar[HostPoolPendingUpdateType]
    HOST_POOL_PENDING_UPDATE_TYPE_INTERNAL_CONFIG: _ClassVar[HostPoolPendingUpdateType]

class HostPoolPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HOST_POOL_PHASE_UNSPECIFIED: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_INACTIVE: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_PENDING: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_RUNNING: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_DEGRADED: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_ERROR: _ClassVar[HostPoolPhase]
    HOST_POOL_PHASE_UNKNOWN: _ClassVar[HostPoolPhase]

HOST_POOL_STORAGE_UNSPECIFIED: HostPoolStorage
HOST_POOL_STORAGE_STANDARD: HostPoolStorage
HOST_POOL_STORAGE_LOCAL_SSD: HostPoolStorage
HOST_POOL_PENDING_UPDATE_TYPE_UNSPECIFIED: HostPoolPendingUpdateType
HOST_POOL_PENDING_UPDATE_TYPE_IMAGE: HostPoolPendingUpdateType
HOST_POOL_PENDING_UPDATE_TYPE_INTERNAL_CONFIG: HostPoolPendingUpdateType
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
        "maintenance_window",
        "storage_config",
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
    MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    min_hosts: int
    max_hosts: int
    idle_timeout: _duration_pb2.Duration
    cpu: str
    memory: str
    machine_family: str
    compute_class: str
    gpu: str
    maintenance_window: _cloud_components_pb2.MaintenanceWindow
    storage_config: StorageConfig
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
        maintenance_window: _Optional[_Union[_cloud_components_pb2.MaintenanceWindow, _Mapping]] = ...,
        storage_config: _Optional[_Union[StorageConfig, _Mapping]] = ...,
    ) -> None: ...

class StorageConfig(_message.Message):
    __slots__ = ("storage_type",)
    STORAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    storage_type: HostPoolStorage
    def __init__(self, storage_type: _Optional[_Union[HostPoolStorage, str]] = ...) -> None: ...

class HostPoolPendingUpdate(_message.Message):
    __slots__ = ("types",)
    TYPES_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedScalarFieldContainer[HostPoolPendingUpdateType]
    def __init__(self, types: _Optional[_Iterable[_Union[HostPoolPendingUpdateType, str]]] = ...) -> None: ...

class HostPool(_message.Message):
    __slots__ = (
        "id",
        "team_id",
        "environment_id",
        "cluster_id",
        "spec",
        "created_at",
        "updated_at",
        "system_managed",
        "pending_update",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_MANAGED_FIELD_NUMBER: _ClassVar[int]
    PENDING_UPDATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    environment_id: str
    cluster_id: str
    spec: HostPoolSpec
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    system_managed: bool
    pending_update: HostPoolPendingUpdate
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
        pending_update: _Optional[_Union[HostPoolPendingUpdate, _Mapping]] = ...,
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

class ValidateHostPoolConfigurationRequest(_message.Message):
    __slots__ = ("environment_id", "cluster_id", "spec", "host_pool_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    HOST_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cluster_id: str
    spec: HostPoolSpec
    host_pool_id: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        cluster_id: _Optional[str] = ...,
        spec: _Optional[_Union[HostPoolSpec, _Mapping]] = ...,
        host_pool_id: _Optional[str] = ...,
    ) -> None: ...

class ValidateHostPoolConfigurationResponse(_message.Message):
    __slots__ = ("allowed_storage", "errors")
    ALLOWED_STORAGE_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    allowed_storage: _containers.RepeatedScalarFieldContainer[HostPoolStorage]
    errors: _containers.RepeatedCompositeFieldContainer[_error_details_pb2.BadRequest.FieldViolation]
    def __init__(
        self,
        allowed_storage: _Optional[_Iterable[_Union[HostPoolStorage, str]]] = ...,
        errors: _Optional[_Iterable[_Union[_error_details_pb2.BadRequest.FieldViolation, _Mapping]]] = ...,
    ) -> None: ...

class HostPoolResources(_message.Message):
    __slots__ = ("cpu_cores", "memory_bytes", "gpus")
    class GpusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

    CPU_CORES_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    GPUS_FIELD_NUMBER: _ClassVar[int]
    cpu_cores: float
    memory_bytes: int
    gpus: _containers.ScalarMap[str, int]
    def __init__(
        self,
        cpu_cores: _Optional[float] = ...,
        memory_bytes: _Optional[int] = ...,
        gpus: _Optional[_Mapping[str, int]] = ...,
    ) -> None: ...

class VersionInfo(_message.Message):
    __slots__ = ("commit_sha",)
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    commit_sha: str
    def __init__(self, commit_sha: _Optional[str] = ...) -> None: ...

class HostCapacity(_message.Message):
    __slots__ = (
        "host_id",
        "ready",
        "placed_containers",
        "capacity",
        "allocated",
        "available",
        "last_heartbeat_at",
        "external_control_stream_connected",
        "unavailable_reason",
        "usage_history",
        "version_info",
    )
    HOST_ID_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    PLACED_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    ALLOCATED_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARTBEAT_AT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONTROL_STREAM_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    UNAVAILABLE_REASON_FIELD_NUMBER: _ClassVar[int]
    USAGE_HISTORY_FIELD_NUMBER: _ClassVar[int]
    VERSION_INFO_FIELD_NUMBER: _ClassVar[int]
    host_id: str
    ready: bool
    placed_containers: int
    capacity: HostPoolResources
    allocated: HostPoolResources
    available: HostPoolResources
    last_heartbeat_at: _timestamp_pb2.Timestamp
    external_control_stream_connected: bool
    unavailable_reason: str
    usage_history: HostUsageHistory
    version_info: VersionInfo
    def __init__(
        self,
        host_id: _Optional[str] = ...,
        ready: bool = ...,
        placed_containers: _Optional[int] = ...,
        capacity: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        allocated: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        available: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        last_heartbeat_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        external_control_stream_connected: bool = ...,
        unavailable_reason: _Optional[str] = ...,
        usage_history: _Optional[_Union[HostUsageHistory, _Mapping]] = ...,
        version_info: _Optional[_Union[VersionInfo, _Mapping]] = ...,
    ) -> None: ...

class UtilizationPoint(_message.Message):
    __slots__ = ("observed_at", "ratio")
    OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    RATIO_FIELD_NUMBER: _ClassVar[int]
    observed_at: _timestamp_pb2.Timestamp
    ratio: float
    def __init__(
        self, observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ratio: _Optional[float] = ...
    ) -> None: ...

class UtilizationSeries(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[UtilizationPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[UtilizationPoint, _Mapping]]] = ...) -> None: ...

class HostUsageHistory(_message.Message):
    __slots__ = ("cpu", "memory", "gpus")
    class GpusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GpuUsageHistory
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[GpuUsageHistory, _Mapping]] = ...
        ) -> None: ...

    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    GPUS_FIELD_NUMBER: _ClassVar[int]
    cpu: UtilizationSeries
    memory: UtilizationSeries
    gpus: _containers.MessageMap[str, GpuUsageHistory]
    def __init__(
        self,
        cpu: _Optional[_Union[UtilizationSeries, _Mapping]] = ...,
        memory: _Optional[_Union[UtilizationSeries, _Mapping]] = ...,
        gpus: _Optional[_Mapping[str, GpuUsageHistory]] = ...,
    ) -> None: ...

class GpuUsageHistory(_message.Message):
    __slots__ = ("uuid", "utilization", "memory")
    UUID_FIELD_NUMBER: _ClassVar[int]
    UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    utilization: UtilizationSeries
    memory: UtilizationSeries
    def __init__(
        self,
        uuid: _Optional[str] = ...,
        utilization: _Optional[_Union[UtilizationSeries, _Mapping]] = ...,
        memory: _Optional[_Union[UtilizationSeries, _Mapping]] = ...,
    ) -> None: ...

class HostPoolReservationHistory(_message.Message):
    __slots__ = ("cpu", "memory", "gpus")
    class GpusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: UtilizationSeries
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[UtilizationSeries, _Mapping]] = ...
        ) -> None: ...

    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    GPUS_FIELD_NUMBER: _ClassVar[int]
    cpu: UtilizationSeries
    memory: UtilizationSeries
    gpus: _containers.MessageMap[str, UtilizationSeries]
    def __init__(
        self,
        cpu: _Optional[_Union[UtilizationSeries, _Mapping]] = ...,
        memory: _Optional[_Union[UtilizationSeries, _Mapping]] = ...,
        gpus: _Optional[_Mapping[str, UtilizationSeries]] = ...,
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
        "external",
        "observed_at",
        "reservation_history",
        "total",
        "reserved",
        "cluster_id",
        "cluster_name",
        "namespace",
        "environment_id",
        "pending_update",
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
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_HISTORY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PENDING_UPDATE_FIELD_NUMBER: _ClassVar[int]
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
    external: bool
    observed_at: _timestamp_pb2.Timestamp
    reservation_history: HostPoolReservationHistory
    total: HostPoolResources
    reserved: HostPoolResources
    cluster_id: str
    cluster_name: str
    namespace: str
    environment_id: str
    pending_update: HostPoolPendingUpdate
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
        external: bool = ...,
        observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        reservation_history: _Optional[_Union[HostPoolReservationHistory, _Mapping]] = ...,
        total: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        reserved: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        cluster_id: _Optional[str] = ...,
        cluster_name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        pending_update: _Optional[_Union[HostPoolPendingUpdate, _Mapping]] = ...,
    ) -> None: ...

class GetHostPoolCapacityRequest(_message.Message):
    __slots__ = ("environment_id", "filters")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    filters: GetHostPoolCapacityFilters
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        filters: _Optional[_Union[GetHostPoolCapacityFilters, _Mapping]] = ...,
    ) -> None: ...

class GetHostPoolCapacityFilters(_message.Message):
    __slots__ = ("environment_id", "cluster_id", "cluster_classes")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CLASSES_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cluster_id: str
    cluster_classes: _containers.RepeatedScalarFieldContainer[_cluster_class_pb2.ClusterClass]
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        cluster_id: _Optional[str] = ...,
        cluster_classes: _Optional[_Iterable[_Union[_cluster_class_pb2.ClusterClass, str]]] = ...,
        **kwargs,
    ) -> None: ...

class GetHostPoolCapacityResponse(_message.Message):
    __slots__ = (
        "host_pools",
        "pending_containers",
        "largest_pending_request",
        "observed_at",
        "history_unavailable_reason",
    )
    HOST_POOLS_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    LARGEST_PENDING_REQUEST_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    HISTORY_UNAVAILABLE_REASON_FIELD_NUMBER: _ClassVar[int]
    host_pools: _containers.RepeatedCompositeFieldContainer[HostPoolCapacity]
    pending_containers: int
    largest_pending_request: HostPoolResources
    observed_at: _timestamp_pb2.Timestamp
    history_unavailable_reason: str
    def __init__(
        self,
        host_pools: _Optional[_Iterable[_Union[HostPoolCapacity, _Mapping]]] = ...,
        pending_containers: _Optional[int] = ...,
        largest_pending_request: _Optional[_Union[HostPoolResources, _Mapping]] = ...,
        observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        history_unavailable_reason: _Optional[str] = ...,
    ) -> None: ...

class HostPoolReportedResources(_message.Message):
    __slots__ = ("cpu_millicores", "memory_bytes", "gpus")
    class GpusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

    CPU_MILLICORES_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    GPUS_FIELD_NUMBER: _ClassVar[int]
    cpu_millicores: int
    memory_bytes: int
    gpus: _containers.ScalarMap[str, int]
    def __init__(
        self,
        cpu_millicores: _Optional[int] = ...,
        memory_bytes: _Optional[int] = ...,
        gpus: _Optional[_Mapping[str, int]] = ...,
    ) -> None: ...

class HostPoolHostStatus(_message.Message):
    __slots__ = (
        "host_id",
        "accepting_placements",
        "unavailable_reason",
        "container_count",
        "total",
        "reserved",
        "free",
        "last_heartbeat_at",
        "external_control_stream_connected",
        "version_info",
    )
    HOST_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPTING_PLACEMENTS_FIELD_NUMBER: _ClassVar[int]
    UNAVAILABLE_REASON_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    FREE_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARTBEAT_AT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONTROL_STREAM_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    VERSION_INFO_FIELD_NUMBER: _ClassVar[int]
    host_id: str
    accepting_placements: bool
    unavailable_reason: str
    container_count: int
    total: HostPoolReportedResources
    reserved: HostPoolReportedResources
    free: HostPoolReportedResources
    last_heartbeat_at: _timestamp_pb2.Timestamp
    external_control_stream_connected: bool
    version_info: VersionInfo
    def __init__(
        self,
        host_id: _Optional[str] = ...,
        accepting_placements: bool = ...,
        unavailable_reason: _Optional[str] = ...,
        container_count: _Optional[int] = ...,
        total: _Optional[_Union[HostPoolReportedResources, _Mapping]] = ...,
        reserved: _Optional[_Union[HostPoolReportedResources, _Mapping]] = ...,
        free: _Optional[_Union[HostPoolReportedResources, _Mapping]] = ...,
        last_heartbeat_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        external_control_stream_connected: bool = ...,
        version_info: _Optional[_Union[VersionInfo, _Mapping]] = ...,
    ) -> None: ...

class HostPoolCapacityStatus(_message.Message):
    __slots__ = (
        "unavailable_reason",
        "total",
        "accepting_placements",
        "reserved",
        "free",
        "registered_host_count",
        "accepting_host_count",
        "idle_host_count",
        "hosts",
    )
    UNAVAILABLE_REASON_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ACCEPTING_PLACEMENTS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    FREE_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_HOST_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACCEPTING_HOST_COUNT_FIELD_NUMBER: _ClassVar[int]
    IDLE_HOST_COUNT_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    unavailable_reason: str
    total: HostPoolReportedResources
    accepting_placements: HostPoolReportedResources
    reserved: HostPoolReportedResources
    free: HostPoolReportedResources
    registered_host_count: int
    accepting_host_count: int
    idle_host_count: int
    hosts: _containers.RepeatedCompositeFieldContainer[HostPoolHostStatus]
    def __init__(
        self,
        unavailable_reason: _Optional[str] = ...,
        total: _Optional[_Union[HostPoolReportedResources, _Mapping]] = ...,
        accepting_placements: _Optional[_Union[HostPoolReportedResources, _Mapping]] = ...,
        reserved: _Optional[_Union[HostPoolReportedResources, _Mapping]] = ...,
        free: _Optional[_Union[HostPoolReportedResources, _Mapping]] = ...,
        registered_host_count: _Optional[int] = ...,
        accepting_host_count: _Optional[int] = ...,
        idle_host_count: _Optional[int] = ...,
        hosts: _Optional[_Iterable[_Union[HostPoolHostStatus, _Mapping]]] = ...,
    ) -> None: ...

class HostPoolStatusReport(_message.Message):
    __slots__ = (
        "name",
        "external",
        "system_managed",
        "phase",
        "message",
        "desired_hosts",
        "min_hosts",
        "max_hosts",
        "idle_timeout_seconds",
        "cpu",
        "memory",
        "gpu",
        "idle_since",
        "capacity",
        "resource_name",
        "cluster_scoped",
        "pending_update",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_MANAGED_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DESIRED_HOSTS_FIELD_NUMBER: _ClassVar[int]
    MIN_HOSTS_FIELD_NUMBER: _ClassVar[int]
    MAX_HOSTS_FIELD_NUMBER: _ClassVar[int]
    IDLE_TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    IDLE_SINCE_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_SCOPED_FIELD_NUMBER: _ClassVar[int]
    PENDING_UPDATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    external: bool
    system_managed: bool
    phase: str
    message: str
    desired_hosts: int
    min_hosts: int
    max_hosts: int
    idle_timeout_seconds: int
    cpu: str
    memory: str
    gpu: str
    idle_since: _timestamp_pb2.Timestamp
    capacity: HostPoolCapacityStatus
    resource_name: str
    cluster_scoped: bool
    pending_update: HostPoolPendingUpdate
    def __init__(
        self,
        name: _Optional[str] = ...,
        external: bool = ...,
        system_managed: bool = ...,
        phase: _Optional[str] = ...,
        message: _Optional[str] = ...,
        desired_hosts: _Optional[int] = ...,
        min_hosts: _Optional[int] = ...,
        max_hosts: _Optional[int] = ...,
        idle_timeout_seconds: _Optional[int] = ...,
        cpu: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        gpu: _Optional[str] = ...,
        idle_since: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        capacity: _Optional[_Union[HostPoolCapacityStatus, _Mapping]] = ...,
        resource_name: _Optional[str] = ...,
        cluster_scoped: bool = ...,
        pending_update: _Optional[_Union[HostPoolPendingUpdate, _Mapping]] = ...,
    ) -> None: ...

class HostPoolStatusUpdate(_message.Message):
    __slots__ = ("namespace", "pool_id", "environment_id", "status")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pool_id: str
    environment_id: str
    status: HostPoolStatusReport
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        pool_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        status: _Optional[_Union[HostPoolStatusReport, _Mapping]] = ...,
    ) -> None: ...

class BatchUpdateHostPoolStatusRequest(_message.Message):
    __slots__ = ("namespace", "partial", "observed_at", "updates")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    partial: bool
    observed_at: _timestamp_pb2.Timestamp
    updates: _containers.RepeatedCompositeFieldContainer[HostPoolStatusUpdate]
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        partial: bool = ...,
        observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updates: _Optional[_Iterable[_Union[HostPoolStatusUpdate, _Mapping]]] = ...,
    ) -> None: ...

class BatchUpdateHostPoolStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
