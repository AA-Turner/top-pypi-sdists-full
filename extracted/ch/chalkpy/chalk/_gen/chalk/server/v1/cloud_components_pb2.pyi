from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class CloudComponentVpc(_message.Message):
    __slots__ = ("name", "config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    config: CloudVpcConfig
    def __init__(
        self, name: _Optional[str] = ..., config: _Optional[_Union[CloudVpcConfig, _Mapping]] = ...
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
    spec: CloudComponentVpc
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
        spec: _Optional[_Union[CloudComponentVpc, _Mapping]] = ...,
        kind: _Optional[str] = ...,
        managed: bool = ...,
        cloud_credential_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        applied_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
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
    __slots__ = ()
    def __init__(self) -> None: ...

class CloudComponentStorage(_message.Message):
    __slots__ = ("name", "designator", "plan_stages_bucket", "source_upload_bucket", "dataset_bucket")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    PLAN_STAGES_BUCKET_FIELD_NUMBER: _ClassVar[int]
    SOURCE_UPLOAD_BUCKET_FIELD_NUMBER: _ClassVar[int]
    DATASET_BUCKET_FIELD_NUMBER: _ClassVar[int]
    name: str
    designator: str
    plan_stages_bucket: str
    source_upload_bucket: str
    dataset_bucket: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        designator: _Optional[str] = ...,
        plan_stages_bucket: _Optional[str] = ...,
        source_upload_bucket: _Optional[str] = ...,
        dataset_bucket: _Optional[str] = ...,
    ) -> None: ...

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

class CloudComponentCluster(_message.Message):
    __slots__ = ("name", "designator", "kubernetes_version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESIGNATOR_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    designator: str
    kubernetes_version: str
    def __init__(
        self, name: _Optional[str] = ..., designator: _Optional[str] = ..., kubernetes_version: _Optional[str] = ...
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
