from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.lsp.v1 import lsp_pb2 as _lsp_pb2
from chalk._gen.chalk.nodepools.v1 import gke_pb2 as _gke_pb2
from chalk._gen.chalk.nodepools.v1 import karpenter_pb2 as _karpenter_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from chalk._gen.chalk.server.v1 import log_pb2 as _log_pb2
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

class DeploymentBuildStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEPLOYMENT_BUILD_STATUS_UNSPECIFIED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_UNKNOWN: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_PENDING: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_QUEUED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_WORKING: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_SUCCESS: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_FAILURE: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_INTERNAL_ERROR: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_TIMEOUT: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_CANCELLED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_EXPIRED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_BOOT_ERRORS: _ClassVar[DeploymentBuildStatus]

class BranchScalingState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BRANCH_SCALING_STATE_UNSPECIFIED: _ClassVar[BranchScalingState]
    BRANCH_SCALING_STATE_SUCCESS: _ClassVar[BranchScalingState]
    BRANCH_SCALING_STATE_IN_PROGRESS: _ClassVar[BranchScalingState]

DEPLOYMENT_BUILD_STATUS_UNSPECIFIED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_UNKNOWN: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_PENDING: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_QUEUED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_WORKING: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_SUCCESS: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_FAILURE: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_INTERNAL_ERROR: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_TIMEOUT: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_CANCELLED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_EXPIRED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_BOOT_ERRORS: DeploymentBuildStatus
BRANCH_SCALING_STATE_UNSPECIFIED: BranchScalingState
BRANCH_SCALING_STATE_SUCCESS: BranchScalingState
BRANCH_SCALING_STATE_IN_PROGRESS: BranchScalingState

class ActivateDeploymentTarget(_message.Message):
    __slots__ = ("service_kind", "resource_group_name")
    SERVICE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    service_kind: str
    resource_group_name: str
    def __init__(self, service_kind: _Optional[str] = ..., resource_group_name: _Optional[str] = ...) -> None: ...

class ActivateDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "targets")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    targets: _containers.RepeatedCompositeFieldContainer[ActivateDeploymentTarget]
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        targets: _Optional[_Iterable[_Union[ActivateDeploymentTarget, _Mapping]]] = ...,
    ) -> None: ...

class ActivateDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IndexDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id",)
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ...) -> None: ...

class IndexDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeployKubeComponentsRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "targets")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    targets: _containers.RepeatedCompositeFieldContainer[ActivateDeploymentTarget]
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        targets: _Optional[_Iterable[_Union[ActivateDeploymentTarget, _Mapping]]] = ...,
    ) -> None: ...

class DeployKubeComponentsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RebuildDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "new_image_tag", "base_image_override", "enable_profiling")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_IMAGE_TAG_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    new_image_tag: str
    base_image_override: str
    enable_profiling: bool
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        new_image_tag: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        enable_profiling: bool = ...,
    ) -> None: ...

class RebuildDeploymentResponse(_message.Message):
    __slots__ = ("build_id",)
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    def __init__(self, build_id: _Optional[str] = ...) -> None: ...

class RedeployDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "enable_profiling", "deployment_tags", "base_image_override")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    enable_profiling: bool
    deployment_tags: _containers.RepeatedScalarFieldContainer[str]
    base_image_override: str
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        enable_profiling: bool = ...,
        deployment_tags: _Optional[_Iterable[str]] = ...,
        base_image_override: _Optional[str] = ...,
    ) -> None: ...

class RedeployDeploymentResponse(_message.Message):
    __slots__ = ("build_id", "deployment_id")
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    deployment_id: str
    def __init__(self, build_id: _Optional[str] = ..., deployment_id: _Optional[str] = ...) -> None: ...

class UploadSourceRequest(_message.Message):
    __slots__ = (
        "deployment_id",
        "archive",
        "no_promote",
        "dependency_hash",
        "base_image_override",
        "use_grpc",
        "enable_profiling",
    )
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    NO_PROMOTE_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_HASH_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    USE_GRPC_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    archive: bytes
    no_promote: bool
    dependency_hash: str
    base_image_override: str
    use_grpc: bool
    enable_profiling: bool
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        archive: _Optional[bytes] = ...,
        no_promote: bool = ...,
        dependency_hash: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        use_grpc: bool = ...,
        enable_profiling: bool = ...,
    ) -> None: ...

class UploadSourceResponse(_message.Message):
    __slots__ = ("status", "progress_url")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_URL_FIELD_NUMBER: _ClassVar[int]
    status: str
    progress_url: str
    def __init__(self, status: _Optional[str] = ..., progress_url: _Optional[str] = ...) -> None: ...

class LintSourceRequest(_message.Message):
    __slots__ = ("archive",)
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    archive: bytes
    def __init__(self, archive: _Optional[bytes] = ...) -> None: ...

class LintSourceResponse(_message.Message):
    __slots__ = ("graph", "lsp")
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    LSP_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    lsp: _lsp_pb2.LSP
    def __init__(
        self,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        lsp: _Optional[_Union[_lsp_pb2.LSP, _Mapping]] = ...,
    ) -> None: ...

class GetDeploymentStepsRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class DeploymentBuildStep(_message.Message):
    __slots__ = ("id", "display_name", "status", "start_time", "end_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    status: DeploymentBuildStatus
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        status: _Optional[_Union[DeploymentBuildStatus, str]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetDeploymentStepsResponse(_message.Message):
    __slots__ = ("steps", "deployment")
    STEPS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    steps: _containers.RepeatedCompositeFieldContainer[DeploymentBuildStep]
    deployment: _deployment_pb2.Deployment
    def __init__(
        self,
        steps: _Optional[_Iterable[_Union[DeploymentBuildStep, _Mapping]]] = ...,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
    ) -> None: ...

class GetDeploymentLogsRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetDeploymentLogsResponse(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[_log_pb2.LogEntry]
    def __init__(self, logs: _Optional[_Iterable[_Union[_log_pb2.LogEntry, _Mapping]]] = ...) -> None: ...

class GetClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetClusterTimescaleDBResponse(_message.Message):
    __slots__ = ("id", "specs_string", "created_at", "updated_at", "specs")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    id: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    specs: ClusterTimescaleSpecs
    def __init__(
        self,
        id: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...,
    ) -> None: ...

class GetClusterGatewayRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetClusterGatewayResponse(_message.Message):
    __slots__ = ("id", "specs_string", "created_at", "updated_at", "specs")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    id: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    specs: EnvoyGatewaySpecs
    def __init__(
        self,
        id: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        specs: _Optional[_Union[EnvoyGatewaySpecs, _Mapping]] = ...,
    ) -> None: ...

class BackgroundPersistence(_message.Message):
    __slots__ = ("id", "kind", "specs_string", "created_at", "updated_at", "specs")
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    id: str
    kind: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    specs: BackgroundPersistenceDeploymentSpecs
    def __init__(
        self,
        id: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        specs: _Optional[_Union[BackgroundPersistenceDeploymentSpecs, _Mapping]] = ...,
    ) -> None: ...

class GetClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ("background_persistence",)
    BACKGROUND_PERSISTENCE_FIELD_NUMBER: _ClassVar[int]
    background_persistence: BackgroundPersistence
    def __init__(self, background_persistence: _Optional[_Union[BackgroundPersistence, _Mapping]] = ...) -> None: ...

class CreateClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("environment_id", "environment_ids", "specs_string", "specs")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    environment_id: _containers.RepeatedScalarFieldContainer[str]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    specs: ClusterTimescaleSpecs
    def __init__(
        self,
        environment_id: _Optional[_Iterable[str]] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
        specs: _Optional[_Union[ClusterTimescaleSpecs, _Mapping]] = ...,
    ) -> None: ...

class KubeResourceConfig(_message.Message):
    __slots__ = ("cpu", "memory", "ephemeral_storage", "storage")
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_STORAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    cpu: str
    memory: str
    ephemeral_storage: str
    storage: str
    def __init__(
        self,
        cpu: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        ephemeral_storage: _Optional[str] = ...,
        storage: _Optional[str] = ...,
    ) -> None: ...

class ClusterTimescaleSpecs(_message.Message):
    __slots__ = (
        "timescale_image",
        "database_name",
        "database_replicas",
        "storage",
        "storage_class",
        "namespace",
        "request",
        "limit",
        "connection_pool_replicas",
        "connection_pool_max_connections",
        "connection_pool_size",
        "connection_pool_mode",
        "backup_bucket",
        "backup_iam_role_arn",
        "secret_name",
        "internal",
        "service_type",
        "postgres_parameters",
        "include_chalk_node_selector",
        "backup_gcp_service_account",
        "instance_type",
    )
    class PostgresParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TIMESCALE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    DATABASE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CLASS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_MAX_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_SIZE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_POOL_MODE_FIELD_NUMBER: _ClassVar[int]
    BACKUP_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BACKUP_IAM_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSTGRES_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CHALK_NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    BACKUP_GCP_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    timescale_image: str
    database_name: str
    database_replicas: int
    storage: str
    storage_class: str
    namespace: str
    request: KubeResourceConfig
    limit: KubeResourceConfig
    connection_pool_replicas: int
    connection_pool_max_connections: str
    connection_pool_size: str
    connection_pool_mode: str
    backup_bucket: str
    backup_iam_role_arn: str
    secret_name: str
    internal: bool
    service_type: str
    postgres_parameters: _containers.ScalarMap[str, str]
    include_chalk_node_selector: bool
    backup_gcp_service_account: str
    instance_type: str
    def __init__(
        self,
        timescale_image: _Optional[str] = ...,
        database_name: _Optional[str] = ...,
        database_replicas: _Optional[int] = ...,
        storage: _Optional[str] = ...,
        storage_class: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        connection_pool_replicas: _Optional[int] = ...,
        connection_pool_max_connections: _Optional[str] = ...,
        connection_pool_size: _Optional[str] = ...,
        connection_pool_mode: _Optional[str] = ...,
        backup_bucket: _Optional[str] = ...,
        backup_iam_role_arn: _Optional[str] = ...,
        secret_name: _Optional[str] = ...,
        internal: bool = ...,
        service_type: _Optional[str] = ...,
        postgres_parameters: _Optional[_Mapping[str, str]] = ...,
        include_chalk_node_selector: bool = ...,
        backup_gcp_service_account: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
    ) -> None: ...

class CreateClusterTimescaleDBResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MigrateClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("cluster_timescale_id", "migration_image", "environment_ids")
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    MIGRATION_IMAGE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_id: str
    migration_image: str
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        cluster_timescale_id: _Optional[str] = ...,
        migration_image: _Optional[str] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class MigrateClusterTimescaleDBResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateClusterGatewayRequest(_message.Message):
    __slots__ = ("environment_id", "environment_ids", "specs_string", "specs")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    environment_id: _containers.RepeatedScalarFieldContainer[str]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    specs: EnvoyGatewaySpecs
    def __init__(
        self,
        environment_id: _Optional[_Iterable[str]] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
        specs: _Optional[_Union[EnvoyGatewaySpecs, _Mapping]] = ...,
    ) -> None: ...

class EnvoyGatewaySpecs(_message.Message):
    __slots__ = (
        "namespace",
        "gateway_name",
        "gateway_class_name",
        "listeners",
        "config",
        "include_chalk_node_selector",
        "ip_allowlist",
        "tls_certificate",
        "service_annotations",
        "load_balancer_class",
    )
    class ServiceAnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_NAME_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    LISTENERS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CHALK_NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    IP_ALLOWLIST_FIELD_NUMBER: _ClassVar[int]
    TLS_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_CLASS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    gateway_name: str
    gateway_class_name: str
    listeners: _containers.RepeatedCompositeFieldContainer[EnvoyGatewayListener]
    config: GatewayProviderConfig
    include_chalk_node_selector: bool
    ip_allowlist: _containers.RepeatedScalarFieldContainer[str]
    tls_certificate: TLSCertificateConfig
    service_annotations: _containers.ScalarMap[str, str]
    load_balancer_class: str
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        gateway_name: _Optional[str] = ...,
        gateway_class_name: _Optional[str] = ...,
        listeners: _Optional[_Iterable[_Union[EnvoyGatewayListener, _Mapping]]] = ...,
        config: _Optional[_Union[GatewayProviderConfig, _Mapping]] = ...,
        include_chalk_node_selector: bool = ...,
        ip_allowlist: _Optional[_Iterable[str]] = ...,
        tls_certificate: _Optional[_Union[TLSCertificateConfig, _Mapping]] = ...,
        service_annotations: _Optional[_Mapping[str, str]] = ...,
        load_balancer_class: _Optional[str] = ...,
    ) -> None: ...

class EnvoyGatewayListener(_message.Message):
    __slots__ = ("port", "protocol", "name", "allowed_routes")
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_ROUTES_FIELD_NUMBER: _ClassVar[int]
    port: int
    protocol: str
    name: str
    allowed_routes: EnvoyGatewayAllowedRoutes
    def __init__(
        self,
        port: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
        name: _Optional[str] = ...,
        allowed_routes: _Optional[_Union[EnvoyGatewayAllowedRoutes, _Mapping]] = ...,
    ) -> None: ...

class EnvoyGatewayAllowedRoutes(_message.Message):
    __slots__ = ("namespaces",)
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    namespaces: EnvoyGatewayAllowedNamespaces
    def __init__(self, namespaces: _Optional[_Union[EnvoyGatewayAllowedNamespaces, _Mapping]] = ...) -> None: ...

class EnvoyGatewayAllowedNamespaces(_message.Message):
    __slots__ = ()
    FROM_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class GatewayProviderConfig(_message.Message):
    __slots__ = ("envoy", "gcp")
    ENVOY_FIELD_NUMBER: _ClassVar[int]
    GCP_FIELD_NUMBER: _ClassVar[int]
    envoy: EnvoyGatewayProviderConfig
    gcp: GCPGatewayProviderConfig
    def __init__(
        self,
        envoy: _Optional[_Union[EnvoyGatewayProviderConfig, _Mapping]] = ...,
        gcp: _Optional[_Union[GCPGatewayProviderConfig, _Mapping]] = ...,
    ) -> None: ...

class EnvoyGatewayProviderConfig(_message.Message):
    __slots__ = ("timeout_duration", "dns_hostname", "replicas", "min_available")
    TIMEOUT_DURATION_FIELD_NUMBER: _ClassVar[int]
    DNS_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    MIN_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    timeout_duration: str
    dns_hostname: str
    replicas: int
    min_available: int
    def __init__(
        self,
        timeout_duration: _Optional[str] = ...,
        dns_hostname: _Optional[str] = ...,
        replicas: _Optional[int] = ...,
        min_available: _Optional[int] = ...,
    ) -> None: ...

class GCPGatewayProviderConfig(_message.Message):
    __slots__ = ("dns_hostname",)
    DNS_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    dns_hostname: str
    def __init__(self, dns_hostname: _Optional[str] = ...) -> None: ...

class TLSCertificateConfig(_message.Message):
    __slots__ = ("manual_certificate",)
    MANUAL_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    manual_certificate: TLSManualCertificateRef
    def __init__(self, manual_certificate: _Optional[_Union[TLSManualCertificateRef, _Mapping]] = ...) -> None: ...

class TLSManualCertificateRef(_message.Message):
    __slots__ = ("secret_name", "secret_namespace")
    SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    SECRET_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    secret_name: str
    secret_namespace: str
    def __init__(self, secret_name: _Optional[str] = ..., secret_namespace: _Optional[str] = ...) -> None: ...

class CreateClusterGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ("environment_ids", "specs_string", "specs")
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    specs: BackgroundPersistenceDeploymentSpecs
    def __init__(
        self,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
        specs: _Optional[_Union[BackgroundPersistenceDeploymentSpecs, _Mapping]] = ...,
    ) -> None: ...

class BackgroundPersistenceCommonSpecs(_message.Message):
    __slots__ = (
        "namespace",
        "bus_writer_image_go",
        "bus_writer_image_python",
        "bus_writer_image_bswl",
        "service_account_name",
        "bus_backend",
        "secret_client",
        "bigquery_parquet_upload_subscription_id",
        "bigquery_streaming_write_subscription_id",
        "bigquery_streaming_write_topic",
        "bigquery_upload_bucket",
        "bigquery_upload_topic",
        "google_cloud_project",
        "kafka_dlq_topic",
        "metrics_bus_subscription_id",
        "metrics_bus_topic_id",
        "operation_subscription_id",
        "query_log_result_topic",
        "query_log_subscription_id",
        "result_bus_metrics_subscription_id",
        "result_bus_offline_store_subscription_id",
        "result_bus_online_store_subscription_id",
        "result_bus_topic_id",
        "usage_bus_topic_id",
        "usage_events_subscription_id",
        "bq_upload_bucket",
        "bq_upload_topic",
        "include_chalk_node_selector",
        "bus_writer_image_rust",
    )
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_GO_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_PYTHON_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_BSWL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    BUS_BACKEND_FIELD_NUMBER: _ClassVar[int]
    SECRET_CLIENT_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_PARQUET_UPLOAD_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_STREAMING_WRITE_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_STREAMING_WRITE_TOPIC_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_UPLOAD_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_UPLOAD_TOPIC_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_CLOUD_PROJECT_FIELD_NUMBER: _ClassVar[int]
    KAFKA_DLQ_TOPIC_FIELD_NUMBER: _ClassVar[int]
    METRICS_BUS_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    METRICS_BUS_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_LOG_RESULT_TOPIC_FIELD_NUMBER: _ClassVar[int]
    QUERY_LOG_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_METRICS_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_OFFLINE_STORE_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_ONLINE_STORE_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    USAGE_BUS_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    USAGE_EVENTS_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    BQ_UPLOAD_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BQ_UPLOAD_TOPIC_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CHALK_NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    BUS_WRITER_IMAGE_RUST_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    bus_writer_image_go: str
    bus_writer_image_python: str
    bus_writer_image_bswl: str
    service_account_name: str
    bus_backend: str
    secret_client: str
    bigquery_parquet_upload_subscription_id: str
    bigquery_streaming_write_subscription_id: str
    bigquery_streaming_write_topic: str
    bigquery_upload_bucket: str
    bigquery_upload_topic: str
    google_cloud_project: str
    kafka_dlq_topic: str
    metrics_bus_subscription_id: str
    metrics_bus_topic_id: str
    operation_subscription_id: str
    query_log_result_topic: str
    query_log_subscription_id: str
    result_bus_metrics_subscription_id: str
    result_bus_offline_store_subscription_id: str
    result_bus_online_store_subscription_id: str
    result_bus_topic_id: str
    usage_bus_topic_id: str
    usage_events_subscription_id: str
    bq_upload_bucket: str
    bq_upload_topic: str
    include_chalk_node_selector: bool
    bus_writer_image_rust: str
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        bus_writer_image_go: _Optional[str] = ...,
        bus_writer_image_python: _Optional[str] = ...,
        bus_writer_image_bswl: _Optional[str] = ...,
        service_account_name: _Optional[str] = ...,
        bus_backend: _Optional[str] = ...,
        secret_client: _Optional[str] = ...,
        bigquery_parquet_upload_subscription_id: _Optional[str] = ...,
        bigquery_streaming_write_subscription_id: _Optional[str] = ...,
        bigquery_streaming_write_topic: _Optional[str] = ...,
        bigquery_upload_bucket: _Optional[str] = ...,
        bigquery_upload_topic: _Optional[str] = ...,
        google_cloud_project: _Optional[str] = ...,
        kafka_dlq_topic: _Optional[str] = ...,
        metrics_bus_subscription_id: _Optional[str] = ...,
        metrics_bus_topic_id: _Optional[str] = ...,
        operation_subscription_id: _Optional[str] = ...,
        query_log_result_topic: _Optional[str] = ...,
        query_log_subscription_id: _Optional[str] = ...,
        result_bus_metrics_subscription_id: _Optional[str] = ...,
        result_bus_offline_store_subscription_id: _Optional[str] = ...,
        result_bus_online_store_subscription_id: _Optional[str] = ...,
        result_bus_topic_id: _Optional[str] = ...,
        usage_bus_topic_id: _Optional[str] = ...,
        usage_events_subscription_id: _Optional[str] = ...,
        bq_upload_bucket: _Optional[str] = ...,
        bq_upload_topic: _Optional[str] = ...,
        include_chalk_node_selector: bool = ...,
        bus_writer_image_rust: _Optional[str] = ...,
    ) -> None: ...

class BackgroundPersistenceWriterHpaSpecs(_message.Message):
    __slots__ = ("hpa_pubsub_subscription_id", "hpa_min_replicas", "hpa_max_replicas", "hpa_target_average_value")
    HPA_PUBSUB_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    HPA_MIN_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    HPA_MAX_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    HPA_TARGET_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    hpa_pubsub_subscription_id: str
    hpa_min_replicas: int
    hpa_max_replicas: int
    hpa_target_average_value: int
    def __init__(
        self,
        hpa_pubsub_subscription_id: _Optional[str] = ...,
        hpa_min_replicas: _Optional[int] = ...,
        hpa_max_replicas: _Optional[int] = ...,
        hpa_target_average_value: _Optional[int] = ...,
    ) -> None: ...

class BackgroundPersistenceWriterSpecs(_message.Message):
    __slots__ = (
        "name",
        "image_override",
        "hpa_specs",
        "gke_spot",
        "load_writer_configmap",
        "version",
        "request",
        "limit",
        "bus_subscriber_type",
        "default_replica_count",
        "kafka_consumer_group_override",
        "max_batch_size",
        "message_processing_concurrency",
        "metadata_sql_ssl_ca_cert_secret",
        "metadata_sql_ssl_client_cert_secret",
        "metadata_sql_ssl_client_key_secret",
        "metadata_sql_uri_secret",
        "offline_store_inserter_db_type",
        "storage_cache_prefix",
        "usage_store_uri",
        "results_writer_skip_producing_feature_metrics",
        "query_table_write_drop_ratio",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    HPA_SPECS_FIELD_NUMBER: _ClassVar[int]
    GKE_SPOT_FIELD_NUMBER: _ClassVar[int]
    LOAD_WRITER_CONFIGMAP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    BUS_SUBSCRIBER_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    KAFKA_CONSUMER_GROUP_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    MAX_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_PROCESSING_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_SSL_CA_CERT_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_SSL_CLIENT_CERT_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_SSL_CLIENT_KEY_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_SQL_URI_SECRET_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_INSERTER_DB_TYPE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CACHE_PREFIX_FIELD_NUMBER: _ClassVar[int]
    USAGE_STORE_URI_FIELD_NUMBER: _ClassVar[int]
    RESULTS_WRITER_SKIP_PRODUCING_FEATURE_METRICS_FIELD_NUMBER: _ClassVar[int]
    QUERY_TABLE_WRITE_DROP_RATIO_FIELD_NUMBER: _ClassVar[int]
    name: str
    image_override: str
    hpa_specs: BackgroundPersistenceWriterHpaSpecs
    gke_spot: bool
    load_writer_configmap: bool
    version: str
    request: KubeResourceConfig
    limit: KubeResourceConfig
    bus_subscriber_type: str
    default_replica_count: int
    kafka_consumer_group_override: str
    max_batch_size: int
    message_processing_concurrency: int
    metadata_sql_ssl_ca_cert_secret: str
    metadata_sql_ssl_client_cert_secret: str
    metadata_sql_ssl_client_key_secret: str
    metadata_sql_uri_secret: str
    offline_store_inserter_db_type: str
    storage_cache_prefix: str
    usage_store_uri: str
    results_writer_skip_producing_feature_metrics: bool
    query_table_write_drop_ratio: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        image_override: _Optional[str] = ...,
        hpa_specs: _Optional[_Union[BackgroundPersistenceWriterHpaSpecs, _Mapping]] = ...,
        gke_spot: bool = ...,
        load_writer_configmap: bool = ...,
        version: _Optional[str] = ...,
        request: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        limit: _Optional[_Union[KubeResourceConfig, _Mapping]] = ...,
        bus_subscriber_type: _Optional[str] = ...,
        default_replica_count: _Optional[int] = ...,
        kafka_consumer_group_override: _Optional[str] = ...,
        max_batch_size: _Optional[int] = ...,
        message_processing_concurrency: _Optional[int] = ...,
        metadata_sql_ssl_ca_cert_secret: _Optional[str] = ...,
        metadata_sql_ssl_client_cert_secret: _Optional[str] = ...,
        metadata_sql_ssl_client_key_secret: _Optional[str] = ...,
        metadata_sql_uri_secret: _Optional[str] = ...,
        offline_store_inserter_db_type: _Optional[str] = ...,
        storage_cache_prefix: _Optional[str] = ...,
        usage_store_uri: _Optional[str] = ...,
        results_writer_skip_producing_feature_metrics: bool = ...,
        query_table_write_drop_ratio: _Optional[str] = ...,
    ) -> None: ...

class BackgroundPersistenceDeploymentSpecs(_message.Message):
    __slots__ = (
        "common_persistence_specs",
        "api_server_host",
        "kafka_sasl_secret",
        "metadata_provider",
        "kafka_bootstrap_servers",
        "kafka_security_protocol",
        "kafka_sasl_mechanism",
        "redis_is_clustered",
        "snowflake_storage_integration_name",
        "redis_lightning_supports_has_many",
        "insecure",
        "writers",
    )
    COMMON_PERSISTENCE_SPECS_FIELD_NUMBER: _ClassVar[int]
    API_SERVER_HOST_FIELD_NUMBER: _ClassVar[int]
    KAFKA_SASL_SECRET_FIELD_NUMBER: _ClassVar[int]
    METADATA_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    KAFKA_BOOTSTRAP_SERVERS_FIELD_NUMBER: _ClassVar[int]
    KAFKA_SECURITY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    KAFKA_SASL_MECHANISM_FIELD_NUMBER: _ClassVar[int]
    REDIS_IS_CLUSTERED_FIELD_NUMBER: _ClassVar[int]
    SNOWFLAKE_STORAGE_INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
    REDIS_LIGHTNING_SUPPORTS_HAS_MANY_FIELD_NUMBER: _ClassVar[int]
    INSECURE_FIELD_NUMBER: _ClassVar[int]
    WRITERS_FIELD_NUMBER: _ClassVar[int]
    common_persistence_specs: BackgroundPersistenceCommonSpecs
    api_server_host: str
    kafka_sasl_secret: str
    metadata_provider: str
    kafka_bootstrap_servers: str
    kafka_security_protocol: str
    kafka_sasl_mechanism: str
    redis_is_clustered: str
    snowflake_storage_integration_name: str
    redis_lightning_supports_has_many: bool
    insecure: bool
    writers: _containers.RepeatedCompositeFieldContainer[BackgroundPersistenceWriterSpecs]
    def __init__(
        self,
        common_persistence_specs: _Optional[_Union[BackgroundPersistenceCommonSpecs, _Mapping]] = ...,
        api_server_host: _Optional[str] = ...,
        kafka_sasl_secret: _Optional[str] = ...,
        metadata_provider: _Optional[str] = ...,
        kafka_bootstrap_servers: _Optional[str] = ...,
        kafka_security_protocol: _Optional[str] = ...,
        kafka_sasl_mechanism: _Optional[str] = ...,
        redis_is_clustered: _Optional[str] = ...,
        snowflake_storage_integration_name: _Optional[str] = ...,
        redis_lightning_supports_has_many: bool = ...,
        insecure: bool = ...,
        writers: _Optional[_Iterable[_Union[BackgroundPersistenceWriterSpecs, _Mapping]]] = ...,
    ) -> None: ...

class CreateClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSearchConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSearchConfigResponse(_message.Message):
    __slots__ = ("team_id", "team_api_key")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_API_KEY_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    team_api_key: str
    def __init__(self, team_id: _Optional[str] = ..., team_api_key: _Optional[str] = ...) -> None: ...

class UpdateEnvironmentVariablesRequest(_message.Message):
    __slots__ = ("environment_variables",)
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    environment_variables: _containers.ScalarMap[str, str]
    def __init__(self, environment_variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateEnvironmentVariablesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StartBranchRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StartBranchResponse(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: BranchScalingState
    def __init__(self, state: _Optional[_Union[BranchScalingState, str]] = ...) -> None: ...

class ScaleBranchRequest(_message.Message):
    __slots__ = ("replicas",)
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    def __init__(self, replicas: _Optional[int] = ...) -> None: ...

class ScaleBranchResponse(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: BranchScalingState
    def __init__(self, state: _Optional[_Union[BranchScalingState, str]] = ...) -> None: ...

class GetBranchProfileRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBranchProfileResponse(_message.Message):
    __slots__ = ("environment_id", "deployment_id", "base_image_sha", "supports_remote_graph_validation")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_SHA_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_REMOTE_GRAPH_VALIDATION_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    deployment_id: str
    base_image_sha: str
    supports_remote_graph_validation: bool
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        base_image_sha: _Optional[str] = ...,
        supports_remote_graph_validation: bool = ...,
    ) -> None: ...

class KafkaTopic(_message.Message):
    __slots__ = ("name", "partitions", "replication", "retention_ms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    REPLICATION_FIELD_NUMBER: _ClassVar[int]
    RETENTION_MS_FIELD_NUMBER: _ClassVar[int]
    name: str
    partitions: int
    replication: int
    retention_ms: int
    def __init__(
        self,
        name: _Optional[str] = ...,
        partitions: _Optional[int] = ...,
        replication: _Optional[int] = ...,
        retention_ms: _Optional[int] = ...,
    ) -> None: ...

class CreateKafkaTopicsRequest(_message.Message):
    __slots__ = ("topics",)
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    topics: _containers.RepeatedCompositeFieldContainer[KafkaTopic]
    def __init__(self, topics: _Optional[_Iterable[_Union[KafkaTopic, _Mapping]]] = ...) -> None: ...

class CreateKafkaTopicsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKafkaTopicsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKafkaTopicsResponse(_message.Message):
    __slots__ = ("topics",)
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    topics: _containers.RepeatedCompositeFieldContainer[KafkaTopic]
    def __init__(self, topics: _Optional[_Iterable[_Union[KafkaTopic, _Mapping]]] = ...) -> None: ...

class GetNodepoolsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNodepoolsResponse(_message.Message):
    __slots__ = ("karpenter_nodepools", "gke_nodepools")
    KARPENTER_NODEPOOLS_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOLS_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepools: _containers.RepeatedCompositeFieldContainer[_karpenter_pb2.KarpenterNodepool]
    gke_nodepools: _containers.RepeatedCompositeFieldContainer[_gke_pb2.GKENodePool]
    def __init__(
        self,
        karpenter_nodepools: _Optional[_Iterable[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]]] = ...,
        gke_nodepools: _Optional[_Iterable[_Union[_gke_pb2.GKENodePool, _Mapping]]] = ...,
    ) -> None: ...

class AddNodepoolRequest(_message.Message):
    __slots__ = ("karpenter_nodepool", "gke_nodepool")
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    gke_nodepool: _gke_pb2.GKENodePool
    def __init__(
        self,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
    ) -> None: ...

class AddNodepoolResponse(_message.Message):
    __slots__ = ("karpenter_nodepool", "gke_nodepool")
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    gke_nodepool: _gke_pb2.GKENodePool
    def __init__(
        self,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
    ) -> None: ...

class UpdateNodepoolRequest(_message.Message):
    __slots__ = ("name", "gke_nodepool", "karpenter_nodepool")
    NAME_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    name: str
    gke_nodepool: _gke_pb2.GKENodePool
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(
        self,
        name: _Optional[str] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
    ) -> None: ...

class UpdateNodepoolResponse(_message.Message):
    __slots__ = ("karpenter_nodepool", "gke_nodepool")
    KARPENTER_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    GKE_NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    karpenter_nodepool: _karpenter_pb2.KarpenterNodepool
    gke_nodepool: _gke_pb2.GKENodePool
    def __init__(
        self,
        karpenter_nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...,
        gke_nodepool: _Optional[_Union[_gke_pb2.GKENodePool, _Mapping]] = ...,
    ) -> None: ...

class DeleteNodepoolRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteNodepoolResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterNodepoolsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterNodepoolsResponse(_message.Message):
    __slots__ = ("nodepools",)
    NODEPOOLS_FIELD_NUMBER: _ClassVar[int]
    nodepools: _containers.RepeatedCompositeFieldContainer[_karpenter_pb2.KarpenterNodepool]
    def __init__(
        self, nodepools: _Optional[_Iterable[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]]] = ...
    ) -> None: ...

class AddKarpenterNodepoolRequest(_message.Message):
    __slots__ = ("nodepool",)
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(self, nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...) -> None: ...

class AddKarpenterNodepoolResponse(_message.Message):
    __slots__ = ("nodepool",)
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(self, nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...) -> None: ...

class UpdateKarpenterNodepoolRequest(_message.Message):
    __slots__ = ("name", "nodepool")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    name: str
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(
        self, name: _Optional[str] = ..., nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...
    ) -> None: ...

class UpdateKarpenterNodepoolResponse(_message.Message):
    __slots__ = ("nodepool",)
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    nodepool: _karpenter_pb2.KarpenterNodepool
    def __init__(self, nodepool: _Optional[_Union[_karpenter_pb2.KarpenterNodepool, _Mapping]] = ...) -> None: ...

class DeleteKarpenterNodepoolRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteKarpenterNodepoolResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterInstallationMetadataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKarpenterInstallationMetadataResponse(_message.Message):
    __slots__ = ("deployment_labels",)
    class DeploymentLabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    DEPLOYMENT_LABELS_FIELD_NUMBER: _ClassVar[int]
    deployment_labels: _containers.ScalarMap[str, str]
    def __init__(self, deployment_labels: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DeploymentTag(_message.Message):
    __slots__ = ("tag", "weight", "deployment_id", "mirror_weight")
    TAG_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MIRROR_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    tag: str
    weight: int
    deployment_id: str
    mirror_weight: int
    def __init__(
        self,
        tag: _Optional[str] = ...,
        weight: _Optional[int] = ...,
        deployment_id: _Optional[str] = ...,
        mirror_weight: _Optional[int] = ...,
    ) -> None: ...

class GetTagWeightsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTagWeightsResponse(_message.Message):
    __slots__ = ("tags",)
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[DeploymentTag]
    def __init__(self, tags: _Optional[_Iterable[_Union[DeploymentTag, _Mapping]]] = ...) -> None: ...

class SetTagWeightsRequest(_message.Message):
    __slots__ = ("tags",)
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[DeploymentTag]
    def __init__(self, tags: _Optional[_Iterable[_Union[DeploymentTag, _Mapping]]] = ...) -> None: ...

class SetTagWeightsResponse(_message.Message):
    __slots__ = ("tags",)
    TAGS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[DeploymentTag]
    def __init__(self, tags: _Optional[_Iterable[_Union[DeploymentTag, _Mapping]]] = ...) -> None: ...
