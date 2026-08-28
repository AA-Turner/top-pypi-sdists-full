from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class HostPoolSpec(_message.Message):
    __slots__ = ("name", "min_hosts", "max_hosts", "idle_timeout", "cpu", "memory", "machine_family", "compute_class")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MIN_HOSTS_FIELD_NUMBER: _ClassVar[int]
    MAX_HOSTS_FIELD_NUMBER: _ClassVar[int]
    IDLE_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    MACHINE_FAMILY_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_CLASS_FIELD_NUMBER: _ClassVar[int]
    name: str
    min_hosts: int
    max_hosts: int
    idle_timeout: _duration_pb2.Duration
    cpu: str
    memory: str
    machine_family: str
    compute_class: str
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
