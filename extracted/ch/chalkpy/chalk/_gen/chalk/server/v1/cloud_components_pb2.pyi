from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import cloud_credentials_pb2 as _cloud_credentials_pb2
from chalk._gen.chalk.server.v1 import environment_pb2 as _environment_pb2
from chalk._gen.chalk.server.v1 import team_pb2 as _team_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
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

class CloudStorageRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_STORAGE_ROLE_UNSPECIFIED: _ClassVar[CloudStorageRole]
    CLOUD_STORAGE_ROLE_DATASET: _ClassVar[CloudStorageRole]
    CLOUD_STORAGE_ROLE_PLAN_STAGES: _ClassVar[CloudStorageRole]
    CLOUD_STORAGE_ROLE_SOURCE_BUNDLE: _ClassVar[CloudStorageRole]
    CLOUD_STORAGE_ROLE_MODEL_REGISTRY: _ClassVar[CloudStorageRole]
    CLOUD_STORAGE_ROLE_VOLUME: _ClassVar[CloudStorageRole]

class ClusterClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLUSTER_CLASS_UNSPECIFIED: _ClassVar[ClusterClass]
    CLUSTER_CLASS_HOSTED: _ClassVar[ClusterClass]
    CLUSTER_CLASS_SERVERLESS: _ClassVar[ClusterClass]

CLOUD_STORAGE_ROLE_UNSPECIFIED: CloudStorageRole
CLOUD_STORAGE_ROLE_DATASET: CloudStorageRole
CLOUD_STORAGE_ROLE_PLAN_STAGES: CloudStorageRole
CLOUD_STORAGE_ROLE_SOURCE_BUNDLE: CloudStorageRole
CLOUD_STORAGE_ROLE_MODEL_REGISTRY: CloudStorageRole
CLOUD_STORAGE_ROLE_VOLUME: CloudStorageRole
CLUSTER_CLASS_UNSPECIFIED: ClusterClass
CLUSTER_CLASS_HOSTED: ClusterClass
CLUSTER_CLASS_SERVERLESS: ClusterClass

class CloudComponentVpc(_message.Message):
    __slots__ = ("name", "config", "designator")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    config: CloudVpcConfig
    designator: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        config: _Optional[_Union[CloudVpcConfig, _Mapping]] = ...,
        designator: _Optional[str] = ...,
    ) -> None: ...

class CloudComponentVpcResponse(_message.Message):
    __slots__ = (
        "name",
        "id",
        "designator",
        "team_id",
        "spec",
        "kind",
        "managed",
        "cloud_credential_id",
        "created_at",
        "updated_at",
        "applied_at",
        "status",
        "status_error",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_ERROR_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    designator: str
    team_id: str
    spec: CloudComponentVpc
    kind: str
    managed: bool
    cloud_credential_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    applied_at: _timestamp_pb2.Timestamp
    status: str
    status_error: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        id: _Optional[str] = ...,
        designator: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentVpc, _Mapping]] = ...,
        kind: _Optional[str] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        applied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[str] = ...,
        status_error: _Optional[str] = ...,
    ) -> None: ...

class CloudComponentVpcRequest(_message.Message):
    __slots__ = ("kind", "spec", "managed", "cloud_credential_id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    kind: str
    spec: CloudComponentVpc
    managed: bool
    cloud_credential_id: str
    def __init__(
        self,
        kind: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentVpc, _Mapping]] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
    ) -> None: ...

class CreateCloudComponentVpcRequest(_message.Message):
    __slots__ = ("vpc",)
    VPC_FIELD_NUMBER: _ClassVar[int]
    vpc: CloudComponentVpcRequest
    def __init__(self, vpc: _Optional[_Union[CloudComponentVpcRequest, _Mapping]] = ...) -> None: ...

class CreateCloudComponentVpcResponse(_message.Message):
    __slots__ = ("vpc",)
    VPC_FIELD_NUMBER: _ClassVar[int]
    vpc: CloudComponentVpcResponse
    def __init__(self, vpc: _Optional[_Union[CloudComponentVpcResponse, _Mapping]] = ...) -> None: ...

class GetCloudComponentVpcRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCloudComponentVpcResponse(_message.Message):
    __slots__ = ("vpc",)
    VPC_FIELD_NUMBER: _ClassVar[int]
    vpc: CloudComponentVpcResponse
    def __init__(self, vpc: _Optional[_Union[CloudComponentVpcResponse, _Mapping]] = ...) -> None: ...

class DeleteCloudComponentVpcRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCloudComponentVpcResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCloudComponentVpcRequest(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    def __init__(self, team_id: _Optional[str] = ...) -> None: ...

class ListCloudComponentVpcResponse(_message.Message):
    __slots__ = ("vpcs",)
    VPCS_FIELD_NUMBER: _ClassVar[int]
    vpcs: _containers.RepeatedCompositeFieldContainer[CloudComponentVpcResponse]
    def __init__(self, vpcs: _Optional[_Iterable[_Union[CloudComponentVpcResponse, _Mapping]]] = ...) -> None: ...

class CloudVpcConfig(_message.Message):
    __slots__ = ("aws", "gcp")
    AWS_FIELD_NUMBER: _ClassVar[int]
    GCP_FIELD_NUMBER: _ClassVar[int]
    aws: AWSVpcConfig
    gcp: GCPVpcConfig
    def __init__(
        self, aws: _Optional[_Union[AWSVpcConfig, _Mapping]] = ..., gcp: _Optional[_Union[GCPVpcConfig, _Mapping]] = ...
    ) -> None: ...

class AWSVpcConfig(_message.Message):
    __slots__ = (
        "cidr_block",
        "additional_cidr_blocks",
        "subnets",
        "additional_public_routes",
        "additional_private_routes",
        "disable_internet_gateway",
    )
    CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_CIDR_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    SUBNETS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PUBLIC_ROUTES_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PRIVATE_ROUTES_FIELD_NUMBER: _ClassVar[int]
    DISABLE_INTERNET_GATEWAY_FIELD_NUMBER: _ClassVar[int]
    cidr_block: str
    additional_cidr_blocks: _containers.RepeatedScalarFieldContainer[str]
    subnets: _containers.RepeatedCompositeFieldContainer[AwsSubnetConfig]
    additional_public_routes: _containers.RepeatedCompositeFieldContainer[AWSVpcRoute]
    additional_private_routes: _containers.RepeatedCompositeFieldContainer[AWSVpcRoute]
    disable_internet_gateway: bool
    def __init__(
        self,
        cidr_block: _Optional[str] = ...,
        additional_cidr_blocks: _Optional[_Iterable[str]] = ...,
        subnets: _Optional[_Iterable[_Union[AwsSubnetConfig, _Mapping]]] = ...,
        additional_public_routes: _Optional[_Iterable[_Union[AWSVpcRoute, _Mapping]]] = ...,
        additional_private_routes: _Optional[_Iterable[_Union[AWSVpcRoute, _Mapping]]] = ...,
        disable_internet_gateway: bool = ...,
    ) -> None: ...

class AWSVpcRoute(_message.Message):
    __slots__ = ("name", "destination_cidr_block", "peer_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    PEER_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    destination_cidr_block: str
    peer_id: str
    def __init__(
        self, name: _Optional[str] = ..., destination_cidr_block: _Optional[str] = ..., peer_id: _Optional[str] = ...
    ) -> None: ...

class AwsSubnetConfig(_message.Message):
    __slots__ = ("name", "private_cidr_block", "public_cidr_block", "availability_zone")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_ZONE_FIELD_NUMBER: _ClassVar[int]
    name: str
    private_cidr_block: str
    public_cidr_block: str
    availability_zone: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        private_cidr_block: _Optional[str] = ...,
        public_cidr_block: _Optional[str] = ...,
        availability_zone: _Optional[str] = ...,
    ) -> None: ...

class GCPVpcConfig(_message.Message):
    __slots__ = ("vpc_peer_addr", "subnets", "backup_subnets")
    VPC_PEER_ADDR_FIELD_NUMBER: _ClassVar[int]
    SUBNETS_FIELD_NUMBER: _ClassVar[int]
    BACKUP_SUBNETS_FIELD_NUMBER: _ClassVar[int]
    vpc_peer_addr: str
    subnets: _containers.RepeatedCompositeFieldContainer[GCPSubnetConfig]
    backup_subnets: _containers.RepeatedCompositeFieldContainer[GCPSubnetConfig]
    def __init__(
        self,
        vpc_peer_addr: _Optional[str] = ...,
        subnets: _Optional[_Iterable[_Union[GCPSubnetConfig, _Mapping]]] = ...,
        backup_subnets: _Optional[_Iterable[_Union[GCPSubnetConfig, _Mapping]]] = ...,
    ) -> None: ...

class GCPSubnetConfig(_message.Message):
    __slots__ = ("name", "cidr_range", "purpose", "role", "secondary_ip_ranges")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CIDR_RANGE_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_IP_RANGES_FIELD_NUMBER: _ClassVar[int]
    name: str
    cidr_range: str
    purpose: str
    role: str
    secondary_ip_ranges: _containers.RepeatedCompositeFieldContainer[GCPSecondaryIpRange]
    def __init__(
        self,
        name: _Optional[str] = ...,
        cidr_range: _Optional[str] = ...,
        purpose: _Optional[str] = ...,
        role: _Optional[str] = ...,
        secondary_ip_ranges: _Optional[_Iterable[_Union[GCPSecondaryIpRange, _Mapping]]] = ...,
    ) -> None: ...

class GCPSecondaryIpRange(_message.Message):
    __slots__ = ("range_name", "ip_cidr_range")
    RANGE_NAME_FIELD_NUMBER: _ClassVar[int]
    IP_CIDR_RANGE_FIELD_NUMBER: _ClassVar[int]
    range_name: str
    ip_cidr_range: str
    def __init__(self, range_name: _Optional[str] = ..., ip_cidr_range: _Optional[str] = ...) -> None: ...

class CloudComponentStorage(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class CloudComponentStorageResponse(_message.Message):
    __slots__ = (
        "name",
        "id",
        "designator",
        "team_id",
        "spec",
        "kind",
        "managed",
        "cloud_credential_id",
        "created_at",
        "updated_at",
        "applied_at",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    designator: str
    team_id: str
    spec: CloudComponentStorage
    kind: str
    managed: bool
    cloud_credential_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    applied_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        id: _Optional[str] = ...,
        designator: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentStorage, _Mapping]] = ...,
        kind: _Optional[str] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        applied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CloudComponentStorageRequest(_message.Message):
    __slots__ = ("kind", "spec", "managed", "cloud_credential_id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    kind: str
    spec: CloudComponentStorage
    managed: bool
    cloud_credential_id: str
    def __init__(
        self,
        kind: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentStorage, _Mapping]] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
    ) -> None: ...

class EnvironmentCloudStorageBinding(_message.Message):
    __slots__ = ("id", "cloud_storage_id", "storage_role", "environment_id", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_STORAGE_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    cloud_storage_id: str
    storage_role: CloudStorageRole
    environment_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        cloud_storage_id: _Optional[str] = ...,
        storage_role: _Optional[_Union[CloudStorageRole, str]] = ...,
        environment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ClusterCloudStorageBinding(_message.Message):
    __slots__ = ("id", "cloud_storage_id", "storage_role", "cluster_id", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_STORAGE_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    cloud_storage_id: str
    storage_role: CloudStorageRole
    cluster_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        cloud_storage_id: _Optional[str] = ...,
        storage_role: _Optional[_Union[CloudStorageRole, str]] = ...,
        cluster_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GarContainerRegistryConfig(_message.Message):
    __slots__ = ("repository_name",)
    REPOSITORY_NAME_FIELD_NUMBER: _ClassVar[int]
    repository_name: str
    def __init__(self, repository_name: _Optional[str] = ...) -> None: ...

class EcrContainerRegistryConfig(_message.Message):
    __slots__ = ("registry_id", "repository_name")
    REGISTRY_ID_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_NAME_FIELD_NUMBER: _ClassVar[int]
    registry_id: str
    repository_name: str
    def __init__(self, registry_id: _Optional[str] = ..., repository_name: _Optional[str] = ...) -> None: ...

class AcrContainerRegistryConfig(_message.Message):
    __slots__ = ("repository_name",)
    REPOSITORY_NAME_FIELD_NUMBER: _ClassVar[int]
    repository_name: str
    def __init__(self, repository_name: _Optional[str] = ...) -> None: ...

class CloudContainerRegistryConfig(_message.Message):
    __slots__ = ("gar", "ecr", "acr")
    GAR_FIELD_NUMBER: _ClassVar[int]
    ECR_FIELD_NUMBER: _ClassVar[int]
    ACR_FIELD_NUMBER: _ClassVar[int]
    gar: GarContainerRegistryConfig
    ecr: EcrContainerRegistryConfig
    acr: AcrContainerRegistryConfig
    def __init__(
        self,
        gar: _Optional[_Union[GarContainerRegistryConfig, _Mapping]] = ...,
        ecr: _Optional[_Union[EcrContainerRegistryConfig, _Mapping]] = ...,
        acr: _Optional[_Union[AcrContainerRegistryConfig, _Mapping]] = ...,
    ) -> None: ...

class CloudComponentContainerRegistry(_message.Message):
    __slots__ = ("name", "designator", "config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    designator: str
    config: CloudContainerRegistryConfig
    def __init__(
        self,
        name: _Optional[str] = ...,
        designator: _Optional[str] = ...,
        config: _Optional[_Union[CloudContainerRegistryConfig, _Mapping]] = ...,
    ) -> None: ...

class CloudComponentContainerRegistryResponse(_message.Message):
    __slots__ = (
        "name",
        "id",
        "designator",
        "team_id",
        "spec",
        "kind",
        "managed",
        "cloud_credential_id",
        "created_at",
        "updated_at",
        "applied_at",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    designator: str
    team_id: str
    spec: CloudComponentContainerRegistry
    kind: str
    managed: bool
    cloud_credential_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    applied_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        id: _Optional[str] = ...,
        designator: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentContainerRegistry, _Mapping]] = ...,
        kind: _Optional[str] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        applied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CloudComponentContainerRegistryRequest(_message.Message):
    __slots__ = ("kind", "spec", "managed", "cloud_credential_id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    kind: str
    spec: CloudComponentContainerRegistry
    managed: bool
    cloud_credential_id: str
    def __init__(
        self,
        kind: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentContainerRegistry, _Mapping]] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
    ) -> None: ...

class MaintenanceWindow(_message.Message):
    __slots__ = ("mode", "schedule", "duration", "override_active_until")
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MODE_UNSPECIFIED: _ClassVar[MaintenanceWindow.Mode]
        MODE_UNRESTRICTED: _ClassVar[MaintenanceWindow.Mode]
        MODE_CUSTOM: _ClassVar[MaintenanceWindow.Mode]

    MODE_UNSPECIFIED: MaintenanceWindow.Mode
    MODE_UNRESTRICTED: MaintenanceWindow.Mode
    MODE_CUSTOM: MaintenanceWindow.Mode
    MODE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_ACTIVE_UNTIL_FIELD_NUMBER: _ClassVar[int]
    mode: MaintenanceWindow.Mode
    schedule: str
    duration: str
    override_active_until: _timestamp_pb2.Timestamp
    def __init__(
        self,
        mode: _Optional[_Union[MaintenanceWindow.Mode, str]] = ...,
        schedule: _Optional[str] = ...,
        duration: _Optional[str] = ...,
        override_active_until: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CloudComponentCluster(_message.Message):
    __slots__ = (
        "name",
        "designator",
        "kubernetes_version",
        "dns_zone",
        "data_plane_redis",
        "dataplane_controller",
        "cluster_class",
        "maintenance_window",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_VERSION_FIELD_NUMBER: _ClassVar[int]
    DNS_ZONE_FIELD_NUMBER: _ClassVar[int]
    DATA_PLANE_REDIS_FIELD_NUMBER: _ClassVar[int]
    DATAPLANE_CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CLASS_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    name: str
    designator: str
    kubernetes_version: str
    dns_zone: str
    data_plane_redis: DataPlaneRedis
    dataplane_controller: DataplaneController
    cluster_class: ClusterClass
    maintenance_window: MaintenanceWindow
    def __init__(
        self,
        name: _Optional[str] = ...,
        designator: _Optional[str] = ...,
        kubernetes_version: _Optional[str] = ...,
        dns_zone: _Optional[str] = ...,
        data_plane_redis: _Optional[_Union[DataPlaneRedis, _Mapping]] = ...,
        dataplane_controller: _Optional[_Union[DataplaneController, _Mapping]] = ...,
        cluster_class: _Optional[_Union[ClusterClass, str]] = ...,
        maintenance_window: _Optional[_Union[MaintenanceWindow, _Mapping]] = ...,
    ) -> None: ...

class DataPlaneRedis(_message.Message):
    __slots__ = ("kind", "memory", "cpu", "cloud_secret_name")
    KIND_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    CLOUD_SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    kind: str
    memory: str
    cpu: str
    cloud_secret_name: str
    def __init__(
        self,
        kind: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        cpu: _Optional[str] = ...,
        cloud_secret_name: _Optional[str] = ...,
    ) -> None: ...

class DataplaneController(_message.Message):
    __slots__ = ("tier", "available_tiers", "node_pool", "restricted_node_pool", "host_pools")
    class Tier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIER_UNSPECIFIED: _ClassVar[DataplaneController.Tier]
        TIER_DISABLED: _ClassVar[DataplaneController.Tier]
        TIER_SMALL: _ClassVar[DataplaneController.Tier]
        TIER_MEDIUM: _ClassVar[DataplaneController.Tier]
        TIER_LARGE: _ClassVar[DataplaneController.Tier]

    TIER_UNSPECIFIED: DataplaneController.Tier
    TIER_DISABLED: DataplaneController.Tier
    TIER_SMALL: DataplaneController.Tier
    TIER_MEDIUM: DataplaneController.Tier
    TIER_LARGE: DataplaneController.Tier
    class TierInfo(_message.Message):
        __slots__ = ("tier", "max_containers", "max_scaling_groups", "memory", "cpu", "replicas")
        TIER_FIELD_NUMBER: _ClassVar[int]
        MAX_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
        MAX_SCALING_GROUPS_FIELD_NUMBER: _ClassVar[int]
        MEMORY_FIELD_NUMBER: _ClassVar[int]
        CPU_FIELD_NUMBER: _ClassVar[int]
        REPLICAS_FIELD_NUMBER: _ClassVar[int]
        tier: DataplaneController.Tier
        max_containers: int
        max_scaling_groups: int
        memory: str
        cpu: str
        replicas: int
        def __init__(
            self,
            tier: _Optional[_Union[DataplaneController.Tier, str]] = ...,
            max_containers: _Optional[int] = ...,
            max_scaling_groups: _Optional[int] = ...,
            memory: _Optional[str] = ...,
            cpu: _Optional[str] = ...,
            replicas: _Optional[int] = ...,
        ) -> None: ...

    TIER_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_TIERS_FIELD_NUMBER: _ClassVar[int]
    NODE_POOL_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_NODE_POOL_FIELD_NUMBER: _ClassVar[int]
    HOST_POOLS_FIELD_NUMBER: _ClassVar[int]
    tier: DataplaneController.Tier
    available_tiers: _containers.RepeatedCompositeFieldContainer[DataplaneController.TierInfo]
    node_pool: str
    restricted_node_pool: str
    host_pools: _containers.RepeatedCompositeFieldContainer[ChalkHostPool]
    def __init__(
        self,
        tier: _Optional[_Union[DataplaneController.Tier, str]] = ...,
        available_tiers: _Optional[_Iterable[_Union[DataplaneController.TierInfo, _Mapping]]] = ...,
        node_pool: _Optional[str] = ...,
        restricted_node_pool: _Optional[str] = ...,
        host_pools: _Optional[_Iterable[_Union[ChalkHostPool, _Mapping]]] = ...,
    ) -> None: ...

class ChalkHostPool(_message.Message):
    __slots__ = ("name", "count", "cpu", "memory", "machine_family")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    MACHINE_FAMILY_FIELD_NUMBER: _ClassVar[int]
    name: str
    count: int
    cpu: str
    memory: str
    machine_family: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        count: _Optional[int] = ...,
        cpu: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        machine_family: _Optional[str] = ...,
    ) -> None: ...

class DeploymentManifest(_message.Message):
    __slots__ = ("cluster_deployment", "vpc_deployment", "create", "delete", "update", "event_bus", "chalk_api_host")
    CLUSTER_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    VPC_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    CREATE_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    EVENT_BUS_FIELD_NUMBER: _ClassVar[int]
    CHALK_API_HOST_FIELD_NUMBER: _ClassVar[int]
    cluster_deployment: ClusterDeploymentManifest
    vpc_deployment: VpcDeploymentManifest
    create: DeploymentManifestCreate
    delete: DeploymentManifestDelete
    update: DeploymentManifestUpdate
    event_bus: str
    chalk_api_host: str
    def __init__(
        self,
        cluster_deployment: _Optional[_Union[ClusterDeploymentManifest, _Mapping]] = ...,
        vpc_deployment: _Optional[_Union[VpcDeploymentManifest, _Mapping]] = ...,
        create: _Optional[_Union[DeploymentManifestCreate, _Mapping]] = ...,
        delete: _Optional[_Union[DeploymentManifestDelete, _Mapping]] = ...,
        update: _Optional[_Union[DeploymentManifestUpdate, _Mapping]] = ...,
        event_bus: _Optional[str] = ...,
        chalk_api_host: _Optional[str] = ...,
    ) -> None: ...

class DeploymentManifestCreate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeploymentManifestDelete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeploymentManifestUpdate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClusterDeploymentManifest(_message.Message):
    __slots__ = ("cluster", "cloud_config", "team", "vpc", "cluster_id")
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    VPC_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster: CloudComponentCluster
    cloud_config: _environment_pb2.CloudConfig
    team: _team_pb2.Team
    vpc: CloudComponentVpc
    cluster_id: str
    def __init__(
        self,
        cluster: _Optional[_Union[CloudComponentCluster, _Mapping]] = ...,
        cloud_config: _Optional[_Union[_environment_pb2.CloudConfig, _Mapping]] = ...,
        team: _Optional[_Union[_team_pb2.Team, _Mapping]] = ...,
        vpc: _Optional[_Union[CloudComponentVpc, _Mapping]] = ...,
        cluster_id: _Optional[str] = ...,
    ) -> None: ...

class VpcDeploymentManifest(_message.Message):
    __slots__ = ("vpc", "cloud_config", "team", "vpc_id")
    VPC_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    VPC_ID_FIELD_NUMBER: _ClassVar[int]
    vpc: CloudComponentVpc
    cloud_config: _environment_pb2.CloudConfig
    team: _team_pb2.Team
    vpc_id: str
    def __init__(
        self,
        vpc: _Optional[_Union[CloudComponentVpc, _Mapping]] = ...,
        cloud_config: _Optional[_Union[_environment_pb2.CloudConfig, _Mapping]] = ...,
        team: _Optional[_Union[_team_pb2.Team, _Mapping]] = ...,
        vpc_id: _Optional[str] = ...,
    ) -> None: ...

class CloudComponentClusterResponse(_message.Message):
    __slots__ = (
        "name",
        "id",
        "designator",
        "team_id",
        "spec",
        "kind",
        "managed",
        "cloud_credential_id",
        "vpc_id",
        "created_at",
        "updated_at",
        "applied_at",
        "status",
        "status_error",
        "effective_maintenance_window",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    VPC_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_ERROR_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    designator: str
    team_id: str
    spec: CloudComponentCluster
    kind: str
    managed: bool
    cloud_credential_id: str
    vpc_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    applied_at: _timestamp_pb2.Timestamp
    status: str
    status_error: str
    effective_maintenance_window: MaintenanceWindow
    def __init__(
        self,
        name: _Optional[str] = ...,
        id: _Optional[str] = ...,
        designator: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentCluster, _Mapping]] = ...,
        kind: _Optional[str] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
        vpc_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        applied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[str] = ...,
        status_error: _Optional[str] = ...,
        effective_maintenance_window: _Optional[_Union[MaintenanceWindow, _Mapping]] = ...,
    ) -> None: ...

class CloudComponentClusterRequest(_message.Message):
    __slots__ = ("kind", "spec", "managed", "cloud_credential_id", "vpc_id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    VPC_ID_FIELD_NUMBER: _ClassVar[int]
    kind: str
    spec: CloudComponentCluster
    managed: bool
    cloud_credential_id: str
    vpc_id: str
    def __init__(
        self,
        kind: _Optional[str] = ...,
        spec: _Optional[_Union[CloudComponentCluster, _Mapping]] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
        vpc_id: _Optional[str] = ...,
    ) -> None: ...

class CreateCloudComponentClusterRequest(_message.Message):
    __slots__ = ("cluster",)
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    cluster: CloudComponentClusterRequest
    def __init__(self, cluster: _Optional[_Union[CloudComponentClusterRequest, _Mapping]] = ...) -> None: ...

class CreateCloudComponentClusterResponse(_message.Message):
    __slots__ = ("cluster",)
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    cluster: CloudComponentClusterResponse
    def __init__(self, cluster: _Optional[_Union[CloudComponentClusterResponse, _Mapping]] = ...) -> None: ...

class UpdateCloudComponentClusterRequest(_message.Message):
    __slots__ = ("id", "cluster")
    ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    id: str
    cluster: CloudComponentClusterRequest
    def __init__(
        self, id: _Optional[str] = ..., cluster: _Optional[_Union[CloudComponentClusterRequest, _Mapping]] = ...
    ) -> None: ...

class UpdateCloudComponentClusterResponse(_message.Message):
    __slots__ = ("cluster",)
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    cluster: CloudComponentClusterResponse
    def __init__(self, cluster: _Optional[_Union[CloudComponentClusterResponse, _Mapping]] = ...) -> None: ...

class GetCloudComponentClusterRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCloudComponentClusterResponse(_message.Message):
    __slots__ = ("cluster",)
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    cluster: CloudComponentClusterResponse
    def __init__(self, cluster: _Optional[_Union[CloudComponentClusterResponse, _Mapping]] = ...) -> None: ...

class DeleteCloudComponentClusterRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCloudComponentClusterResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestClusterConnectionRequest(_message.Message):
    __slots__ = ("id", "config")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    config: CloudComponentClusterRequest
    def __init__(
        self, id: _Optional[str] = ..., config: _Optional[_Union[CloudComponentClusterRequest, _Mapping]] = ...
    ) -> None: ...

class TestClusterConnectionResponse(_message.Message):
    __slots__ = ("success", "message", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    error: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class ListCloudComponentClusterRequest(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    def __init__(self, team_id: _Optional[str] = ...) -> None: ...

class ListCloudComponentClusterResponse(_message.Message):
    __slots__ = ("clusters",)
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[CloudComponentClusterResponse]
    def __init__(
        self, clusters: _Optional[_Iterable[_Union[CloudComponentClusterResponse, _Mapping]]] = ...
    ) -> None: ...

class ListServerlessClustersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ServerlessCluster(_message.Message):
    __slots__ = ("cluster", "cloud_credentials")
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    cluster: CloudComponentClusterResponse
    cloud_credentials: _cloud_credentials_pb2.CloudCredentialsResponse
    def __init__(
        self,
        cluster: _Optional[_Union[CloudComponentClusterResponse, _Mapping]] = ...,
        cloud_credentials: _Optional[_Union[_cloud_credentials_pb2.CloudCredentialsResponse, _Mapping]] = ...,
    ) -> None: ...

class ListServerlessClustersResponse(_message.Message):
    __slots__ = ("clusters",)
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[ServerlessCluster]
    def __init__(self, clusters: _Optional[_Iterable[_Union[ServerlessCluster, _Mapping]]] = ...) -> None: ...

class CreateCloudComponentStorageRequest(_message.Message):
    __slots__ = ("storage",)
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    storage: CloudComponentStorageRequest
    def __init__(self, storage: _Optional[_Union[CloudComponentStorageRequest, _Mapping]] = ...) -> None: ...

class CreateCloudComponentStorageResponse(_message.Message):
    __slots__ = ("storage",)
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    storage: CloudComponentStorageResponse
    def __init__(self, storage: _Optional[_Union[CloudComponentStorageResponse, _Mapping]] = ...) -> None: ...

class GetCloudComponentStorageRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCloudComponentStorageResponse(_message.Message):
    __slots__ = ("storage",)
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    storage: CloudComponentStorageResponse
    def __init__(self, storage: _Optional[_Union[CloudComponentStorageResponse, _Mapping]] = ...) -> None: ...

class DeleteCloudComponentStorageRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCloudComponentStorageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCloudComponentStorageRequest(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    def __init__(self, team_id: _Optional[str] = ...) -> None: ...

class ListCloudComponentStorageResponse(_message.Message):
    __slots__ = ("storages",)
    STORAGES_FIELD_NUMBER: _ClassVar[int]
    storages: _containers.RepeatedCompositeFieldContainer[CloudComponentStorageResponse]
    def __init__(
        self, storages: _Optional[_Iterable[_Union[CloudComponentStorageResponse, _Mapping]]] = ...
    ) -> None: ...

class CreateBindingEnvironmentCloudStorageRequest(_message.Message):
    __slots__ = ("environment_id", "cloud_storage_id", "storage_role")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_STORAGE_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cloud_storage_id: str
    storage_role: CloudStorageRole
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        cloud_storage_id: _Optional[str] = ...,
        storage_role: _Optional[_Union[CloudStorageRole, str]] = ...,
    ) -> None: ...

class CreateBindingEnvironmentCloudStorageResponse(_message.Message):
    __slots__ = ("binding",)
    BINDING_FIELD_NUMBER: _ClassVar[int]
    binding: EnvironmentCloudStorageBinding
    def __init__(self, binding: _Optional[_Union[EnvironmentCloudStorageBinding, _Mapping]] = ...) -> None: ...

class GetBindingEnvironmentCloudStorageRequest(_message.Message):
    __slots__ = ("environment_id", "storage_role")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    storage_role: CloudStorageRole
    def __init__(
        self, environment_id: _Optional[str] = ..., storage_role: _Optional[_Union[CloudStorageRole, str]] = ...
    ) -> None: ...

class GetBindingEnvironmentCloudStorageResponse(_message.Message):
    __slots__ = ("binding",)
    BINDING_FIELD_NUMBER: _ClassVar[int]
    binding: EnvironmentCloudStorageBinding
    def __init__(self, binding: _Optional[_Union[EnvironmentCloudStorageBinding, _Mapping]] = ...) -> None: ...

class ListBindingEnvironmentCloudStorageRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class ListBindingEnvironmentCloudStorageResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[EnvironmentCloudStorageBinding]
    def __init__(
        self, bindings: _Optional[_Iterable[_Union[EnvironmentCloudStorageBinding, _Mapping]]] = ...
    ) -> None: ...

class DeleteBindingEnvironmentCloudStorageRequest(_message.Message):
    __slots__ = ("environment_id", "storage_role")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    storage_role: CloudStorageRole
    def __init__(
        self, environment_id: _Optional[str] = ..., storage_role: _Optional[_Union[CloudStorageRole, str]] = ...
    ) -> None: ...

class DeleteBindingEnvironmentCloudStorageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateBindingClusterCloudStorageRequest(_message.Message):
    __slots__ = ("cluster_id", "cloud_storage_id", "storage_role")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_STORAGE_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    cloud_storage_id: str
    storage_role: CloudStorageRole
    def __init__(
        self,
        cluster_id: _Optional[str] = ...,
        cloud_storage_id: _Optional[str] = ...,
        storage_role: _Optional[_Union[CloudStorageRole, str]] = ...,
    ) -> None: ...

class CreateBindingClusterCloudStorageResponse(_message.Message):
    __slots__ = ("binding",)
    BINDING_FIELD_NUMBER: _ClassVar[int]
    binding: ClusterCloudStorageBinding
    def __init__(self, binding: _Optional[_Union[ClusterCloudStorageBinding, _Mapping]] = ...) -> None: ...

class GetBindingClusterCloudStorageRequest(_message.Message):
    __slots__ = ("cluster_id", "storage_role")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    storage_role: CloudStorageRole
    def __init__(
        self, cluster_id: _Optional[str] = ..., storage_role: _Optional[_Union[CloudStorageRole, str]] = ...
    ) -> None: ...

class GetBindingClusterCloudStorageResponse(_message.Message):
    __slots__ = ("binding",)
    BINDING_FIELD_NUMBER: _ClassVar[int]
    binding: ClusterCloudStorageBinding
    def __init__(self, binding: _Optional[_Union[ClusterCloudStorageBinding, _Mapping]] = ...) -> None: ...

class ListBindingClusterCloudStorageRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterCloudStorageResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[ClusterCloudStorageBinding]
    def __init__(self, bindings: _Optional[_Iterable[_Union[ClusterCloudStorageBinding, _Mapping]]] = ...) -> None: ...

class DeleteBindingClusterCloudStorageRequest(_message.Message):
    __slots__ = ("cluster_id", "storage_role")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    storage_role: CloudStorageRole
    def __init__(
        self, cluster_id: _Optional[str] = ..., storage_role: _Optional[_Union[CloudStorageRole, str]] = ...
    ) -> None: ...

class DeleteBindingClusterCloudStorageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateCloudComponentContainerRegistryRequest(_message.Message):
    __slots__ = ("container_registry",)
    CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    container_registry: CloudComponentContainerRegistryRequest
    def __init__(
        self, container_registry: _Optional[_Union[CloudComponentContainerRegistryRequest, _Mapping]] = ...
    ) -> None: ...

class CreateCloudComponentContainerRegistryResponse(_message.Message):
    __slots__ = ("container_registry",)
    CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    container_registry: CloudComponentContainerRegistryResponse
    def __init__(
        self, container_registry: _Optional[_Union[CloudComponentContainerRegistryResponse, _Mapping]] = ...
    ) -> None: ...

class UpdateCloudComponentContainerRegistryRequest(_message.Message):
    __slots__ = ("id", "container_registry")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    id: str
    container_registry: CloudComponentContainerRegistryRequest
    def __init__(
        self,
        id: _Optional[str] = ...,
        container_registry: _Optional[_Union[CloudComponentContainerRegistryRequest, _Mapping]] = ...,
    ) -> None: ...

class UpdateCloudComponentContainerRegistryResponse(_message.Message):
    __slots__ = ("container_registry",)
    CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    container_registry: CloudComponentContainerRegistryResponse
    def __init__(
        self, container_registry: _Optional[_Union[CloudComponentContainerRegistryResponse, _Mapping]] = ...
    ) -> None: ...

class GetCloudComponentContainerRegistryRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCloudComponentContainerRegistryResponse(_message.Message):
    __slots__ = ("container_registry",)
    CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    container_registry: CloudComponentContainerRegistryResponse
    def __init__(
        self, container_registry: _Optional[_Union[CloudComponentContainerRegistryResponse, _Mapping]] = ...
    ) -> None: ...

class DeleteCloudComponentContainerRegistryRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCloudComponentContainerRegistryResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCloudComponentContainerRegistryRequest(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    def __init__(self, team_id: _Optional[str] = ...) -> None: ...

class ListCloudComponentContainerRegistryResponse(_message.Message):
    __slots__ = ("container_registries",)
    CONTAINER_REGISTRIES_FIELD_NUMBER: _ClassVar[int]
    container_registries: _containers.RepeatedCompositeFieldContainer[CloudComponentContainerRegistryResponse]
    def __init__(
        self,
        container_registries: _Optional[_Iterable[_Union[CloudComponentContainerRegistryResponse, _Mapping]]] = ...,
    ) -> None: ...

class CreateBindingClusterContainerRegistryRequest(_message.Message):
    __slots__ = ("cluster_id", "container_registry_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_REGISTRY_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    container_registry_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., container_registry_id: _Optional[str] = ...) -> None: ...

class CreateBindingClusterContainerRegistryResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingClusterContainerRegistryRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class GetBindingClusterContainerRegistryResponse(_message.Message):
    __slots__ = ("cluster_id", "container_registry_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_REGISTRY_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    container_registry_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., container_registry_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterContainerRegistryRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterContainerRegistryResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[GetBindingClusterContainerRegistryResponse]
    def __init__(
        self, bindings: _Optional[_Iterable[_Union[GetBindingClusterContainerRegistryResponse, _Mapping]]] = ...
    ) -> None: ...

class DeleteBindingClusterContainerRegistryRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class DeleteBindingClusterContainerRegistryResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateBindingClusterGatewayRequest(_message.Message):
    __slots__ = ("cluster_id", "cluster_gateway_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    cluster_gateway_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., cluster_gateway_id: _Optional[str] = ...) -> None: ...

class CreateBindingClusterGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteBindingClusterGatewayRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class DeleteBindingClusterGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingClusterGatewayRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class GetBindingClusterGatewayResponse(_message.Message):
    __slots__ = ("cluster_id", "cluster_gateway_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    cluster_gateway_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., cluster_gateway_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterGatewayRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterGatewayResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[GetBindingClusterGatewayResponse]
    def __init__(
        self, bindings: _Optional[_Iterable[_Union[GetBindingClusterGatewayResponse, _Mapping]]] = ...
    ) -> None: ...

class CreateBindingPrivateGatewayRequest(_message.Message):
    __slots__ = ("cluster_id", "private_gateway_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    private_gateway_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., private_gateway_id: _Optional[str] = ...) -> None: ...

class CreateBindingPrivateGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteBindingPrivateGatewayRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class DeleteBindingPrivateGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingPrivateGatewayRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class GetBindingPrivateGatewayResponse(_message.Message):
    __slots__ = ("cluster_id", "private_gateway_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    private_gateway_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., private_gateway_id: _Optional[str] = ...) -> None: ...

class ListBindingPrivateGatewayRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingPrivateGatewayResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[GetBindingPrivateGatewayResponse]
    def __init__(
        self, bindings: _Optional[_Iterable[_Union[GetBindingPrivateGatewayResponse, _Mapping]]] = ...
    ) -> None: ...

class CreateBindingClusterBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id", "background_persistence_deployment_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_PERSISTENCE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    background_persistence_deployment_id: str
    def __init__(
        self, cluster_id: _Optional[str] = ..., background_persistence_deployment_id: _Optional[str] = ...
    ) -> None: ...

class CreateBindingClusterBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteBindingClusterBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class DeleteBindingClusterBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingClusterBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class GetBindingClusterBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ("cluster_id", "background_persistence_deployment_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_PERSISTENCE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    background_persistence_deployment_id: str
    def __init__(
        self, cluster_id: _Optional[str] = ..., background_persistence_deployment_id: _Optional[str] = ...
    ) -> None: ...

class ListBindingClusterBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[GetBindingClusterBackgroundPersistenceDeploymentResponse]
    def __init__(
        self,
        bindings: _Optional[
            _Iterable[_Union[GetBindingClusterBackgroundPersistenceDeploymentResponse, _Mapping]]
        ] = ...,
    ) -> None: ...

class CreateBindingClusterTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id", "telemetry_deployment_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    telemetry_deployment_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., telemetry_deployment_id: _Optional[str] = ...) -> None: ...

class CreateBindingClusterTelemetryDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteBindingClusterTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class DeleteBindingClusterTelemetryDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingClusterTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class GetBindingClusterTelemetryDeploymentResponse(_message.Message):
    __slots__ = ("cluster_id", "telemetry_deployment_id")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    telemetry_deployment_id: str
    def __init__(self, cluster_id: _Optional[str] = ..., telemetry_deployment_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterTelemetryDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingClusterTelemetryDeploymentResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[GetBindingClusterTelemetryDeploymentResponse]
    def __init__(
        self, bindings: _Optional[_Iterable[_Union[GetBindingClusterTelemetryDeploymentResponse, _Mapping]]] = ...
    ) -> None: ...

class CreateBindingEnvironmentGatewayRequest(_message.Message):
    __slots__ = ("environment_id", "cluster_gateway_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cluster_gateway_id: str
    def __init__(self, environment_id: _Optional[str] = ..., cluster_gateway_id: _Optional[str] = ...) -> None: ...

class CreateBindingEnvironmentGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteBindingEnvironmentGatewayRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class DeleteBindingEnvironmentGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingEnvironmentGatewayRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetBindingEnvironmentGatewayResponse(_message.Message):
    __slots__ = ("environment_id", "cluster_gateway_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cluster_gateway_id: str
    def __init__(self, environment_id: _Optional[str] = ..., cluster_gateway_id: _Optional[str] = ...) -> None: ...

class ListBindingEnvironmentGatewayRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingEnvironmentGatewayResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[GetBindingEnvironmentGatewayResponse]
    def __init__(
        self, bindings: _Optional[_Iterable[_Union[GetBindingEnvironmentGatewayResponse, _Mapping]]] = ...
    ) -> None: ...

class CreateBindingEnvironmentBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("environment_id", "background_persistence_deployment_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_PERSISTENCE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    background_persistence_deployment_id: str
    def __init__(
        self, environment_id: _Optional[str] = ..., background_persistence_deployment_id: _Optional[str] = ...
    ) -> None: ...

class CreateBindingEnvironmentBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteBindingEnvironmentBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class DeleteBindingEnvironmentBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingEnvironmentBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetBindingEnvironmentBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ("environment_id", "background_persistence_deployment_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_PERSISTENCE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    background_persistence_deployment_id: str
    def __init__(
        self, environment_id: _Optional[str] = ..., background_persistence_deployment_id: _Optional[str] = ...
    ) -> None: ...

class ListBindingEnvironmentBackgroundPersistenceDeploymentRequest(_message.Message):
    __slots__ = ("cluster_id",)
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ListBindingEnvironmentBackgroundPersistenceDeploymentResponse(_message.Message):
    __slots__ = ("bindings",)
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    bindings: _containers.RepeatedCompositeFieldContainer[GetBindingEnvironmentBackgroundPersistenceDeploymentResponse]
    def __init__(
        self,
        bindings: _Optional[
            _Iterable[_Union[GetBindingEnvironmentBackgroundPersistenceDeploymentResponse, _Mapping]]
        ] = ...,
    ) -> None: ...
