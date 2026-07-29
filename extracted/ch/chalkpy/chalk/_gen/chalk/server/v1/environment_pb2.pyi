from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import cloud_config_pb2 as _cloud_config_pb2
from chalk._gen.chalk.server.v1 import cluster_class_pb2 as _cluster_class_pb2
from chalk._gen.chalk.utils.v1 import field_change_pb2 as _field_change_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class CloudProviderKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_PROVIDER_KIND_UNSPECIFIED: _ClassVar[CloudProviderKind]
    CLOUD_PROVIDER_KIND_UNKNOWN: _ClassVar[CloudProviderKind]
    CLOUD_PROVIDER_KIND_GCP: _ClassVar[CloudProviderKind]
    CLOUD_PROVIDER_KIND_AWS: _ClassVar[CloudProviderKind]
    CLOUD_PROVIDER_KIND_AZURE: _ClassVar[CloudProviderKind]

class VectorDBKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VECTOR_DB_KIND_UNSPECIFIED: _ClassVar[VectorDBKind]
    VECTOR_DB_KIND_OPENSEARCH: _ClassVar[VectorDBKind]
    VECTOR_DB_KIND_PGVECTOR: _ClassVar[VectorDBKind]
    VECTOR_DB_KIND_MILVUS: _ClassVar[VectorDBKind]
    VECTOR_DB_KIND_VALKEY: _ClassVar[VectorDBKind]
    VECTOR_DB_KIND_TURBOPUFFER: _ClassVar[VectorDBKind]

class DeploymentBuildProfile(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEPLOYMENT_BUILD_PROFILE_UNSPECIFIED: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_RUST_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_RUST_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_RUST_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_RUST_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_RUST_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_RUST_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_RUST_NO_PROFILING: _ClassVar[DeploymentBuildProfile]
    DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_RUST_PROFILING: _ClassVar[DeploymentBuildProfile]

class DiscoveredBucketSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISCOVERED_BUCKET_SOURCE_UNSPECIFIED: _ClassVar[DiscoveredBucketSource]
    DISCOVERED_BUCKET_SOURCE_ENGINE: _ClassVar[DiscoveredBucketSource]
    DISCOVERED_BUCKET_SOURCE_METADATA_PLANE: _ClassVar[DiscoveredBucketSource]
    DISCOVERED_BUCKET_SOURCE_CLUSTER_MANAGER: _ClassVar[DiscoveredBucketSource]

class DiscoveredBucketScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISCOVERED_BUCKET_SCOPE_UNSPECIFIED: _ClassVar[DiscoveredBucketScope]
    DISCOVERED_BUCKET_SCOPE_ENVIRONMENT: _ClassVar[DiscoveredBucketScope]
    DISCOVERED_BUCKET_SCOPE_CLUSTER: _ClassVar[DiscoveredBucketScope]

class DiscoveredBucketRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISCOVERED_BUCKET_ROLE_UNSPECIFIED: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_DATASET: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_PLAN_STAGES: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_DEBUG: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_DATA_TRANSFER: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_SNOWFLAKE_UNLOAD: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_VOLUME: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_SOURCE_BUNDLE: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_MODEL_REGISTRY: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_INGESTER_SNAPSHOT: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_STREAMING_LOG: _ClassVar[DiscoveredBucketRole]
    DISCOVERED_BUCKET_ROLE_OTHER: _ClassVar[DiscoveredBucketRole]

CLOUD_PROVIDER_KIND_UNSPECIFIED: CloudProviderKind
CLOUD_PROVIDER_KIND_UNKNOWN: CloudProviderKind
CLOUD_PROVIDER_KIND_GCP: CloudProviderKind
CLOUD_PROVIDER_KIND_AWS: CloudProviderKind
CLOUD_PROVIDER_KIND_AZURE: CloudProviderKind
VECTOR_DB_KIND_UNSPECIFIED: VectorDBKind
VECTOR_DB_KIND_OPENSEARCH: VectorDBKind
VECTOR_DB_KIND_PGVECTOR: VectorDBKind
VECTOR_DB_KIND_MILVUS: VectorDBKind
VECTOR_DB_KIND_VALKEY: VectorDBKind
VECTOR_DB_KIND_TURBOPUFFER: VectorDBKind
DEPLOYMENT_BUILD_PROFILE_UNSPECIFIED: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_RUST_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_RUST_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_RUST_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_RUST_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_RUST_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O3_BAZEL_RUST_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_RUST_NO_PROFILING: DeploymentBuildProfile
DEPLOYMENT_BUILD_PROFILE_O2_BAZEL_RUST_PROFILING: DeploymentBuildProfile
DISCOVERED_BUCKET_SOURCE_UNSPECIFIED: DiscoveredBucketSource
DISCOVERED_BUCKET_SOURCE_ENGINE: DiscoveredBucketSource
DISCOVERED_BUCKET_SOURCE_METADATA_PLANE: DiscoveredBucketSource
DISCOVERED_BUCKET_SOURCE_CLUSTER_MANAGER: DiscoveredBucketSource
DISCOVERED_BUCKET_SCOPE_UNSPECIFIED: DiscoveredBucketScope
DISCOVERED_BUCKET_SCOPE_ENVIRONMENT: DiscoveredBucketScope
DISCOVERED_BUCKET_SCOPE_CLUSTER: DiscoveredBucketScope
DISCOVERED_BUCKET_ROLE_UNSPECIFIED: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_DATASET: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_PLAN_STAGES: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_DEBUG: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_DATA_TRANSFER: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_SNOWFLAKE_UNLOAD: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_VOLUME: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_SOURCE_BUNDLE: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_MODEL_REGISTRY: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_INGESTER_SNAPSHOT: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_STREAMING_LOG: DiscoveredBucketRole
DISCOVERED_BUCKET_ROLE_OTHER: DiscoveredBucketRole

class EnvironmentObjectStorageConfig(_message.Message):
    __slots__ = ("dataset_bucket", "plan_stages_bucket", "source_bundle_bucket", "model_registry_bucket")
    DATASET_BUCKET_FIELD_NUMBER: _ClassVar[int]
    PLAN_STAGES_BUCKET_FIELD_NUMBER: _ClassVar[int]
    SOURCE_BUNDLE_BUCKET_FIELD_NUMBER: _ClassVar[int]
    MODEL_REGISTRY_BUCKET_FIELD_NUMBER: _ClassVar[int]
    dataset_bucket: str
    plan_stages_bucket: str
    source_bundle_bucket: str
    model_registry_bucket: str
    def __init__(
        self,
        dataset_bucket: _Optional[str] = ...,
        plan_stages_bucket: _Optional[str] = ...,
        source_bundle_bucket: _Optional[str] = ...,
        model_registry_bucket: _Optional[str] = ...,
    ) -> None: ...

class Environment(_message.Message):
    __slots__ = (
        "name",
        "project_id",
        "id",
        "team_id",
        "active_deployment_id",
        "worker_url",
        "service_url",
        "branch_url",
        "offline_store_secret",
        "online_store_secret",
        "feature_store_secret",
        "postgres_secret",
        "online_store_kind",
        "emq_uri",
        "vpc_connector_name",
        "kube_cluster_name",
        "branch_kube_cluster_name",
        "engine_kube_cluster_name",
        "shadow_engine_kube_cluster_name",
        "kube_job_namespace",
        "kube_preview_namespace",
        "kube_service_account_name",
        "streaming_query_service_uri",
        "skip_offline_writes_for_online_cached_features",
        "result_bus_topic",
        "online_persistence_mode",
        "metrics_bus_topic",
        "bigtable_instance_name",
        "bigtable_table_name",
        "cloud_account_locator",
        "cloud_region",
        "cloud_tenancy_id",
        "source_bundle_bucket",
        "engine_docker_registry_path",
        "default_planner",
        "additional_env_vars",
        "additional_cron_env_vars",
        "private_pip_repositories",
        "is_sandbox",
        "cloud_provider",
        "cloud_config",
        "spec_config_json",
        "archived_at",
        "metadata_server_metrics_store_secret",
        "query_server_metrics_store_secret",
        "pinned_base_image",
        "cluster_gateway_id",
        "cluster_timescaledb_id",
        "background_persistence_deployment_id",
        "cluster_workflow_orchestrator_id",
        "environment_buckets",
        "cluster_timescaledb_secret",
        "grpc_engine_url",
        "kube_cluster_mode",
        "dashboard_url",
        "kube_cluster_id",
        "managed",
        "telemetry_deployment_id",
        "suspended_at",
        "default_build_profile",
        "vector_db_kind",
        "vector_db_secret",
        "internal_metadata",
        "customer_metadata",
        "dataplane_db_direct_secret",
        "primary_linked_cluster_class",
    )
    class AdditionalEnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class AdditionalCronEnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class SpecConfigJsonEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    class InternalMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    class CustomerMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKER_URL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_URL_FIELD_NUMBER: _ClassVar[int]
    BRANCH_URL_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_SECRET_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_SECRET_FIELD_NUMBER: _ClassVar[int]
    FEATURE_STORE_SECRET_FIELD_NUMBER: _ClassVar[int]
    POSTGRES_SECRET_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_KIND_FIELD_NUMBER: _ClassVar[int]
    EMQ_URI_FIELD_NUMBER: _ClassVar[int]
    VPC_CONNECTOR_NAME_FIELD_NUMBER: _ClassVar[int]
    KUBE_CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    BRANCH_KUBE_CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    ENGINE_KUBE_CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    SHADOW_ENGINE_KUBE_CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    KUBE_JOB_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    KUBE_PREVIEW_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    KUBE_SERVICE_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    STREAMING_QUERY_SERVICE_URI_FIELD_NUMBER: _ClassVar[int]
    SKIP_OFFLINE_WRITES_FOR_ONLINE_CACHED_FEATURES_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUS_TOPIC_FIELD_NUMBER: _ClassVar[int]
    ONLINE_PERSISTENCE_MODE_FIELD_NUMBER: _ClassVar[int]
    METRICS_BUS_TOPIC_FIELD_NUMBER: _ClassVar[int]
    BIGTABLE_INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    BIGTABLE_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUD_ACCOUNT_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    CLOUD_REGION_FIELD_NUMBER: _ClassVar[int]
    CLOUD_TENANCY_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_BUNDLE_BUCKET_FIELD_NUMBER: _ClassVar[int]
    ENGINE_DOCKER_REGISTRY_PATH_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PLANNER_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_CRON_ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_PIP_REPOSITORIES_FIELD_NUMBER: _ClassVar[int]
    IS_SANDBOX_FIELD_NUMBER: _ClassVar[int]
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SPEC_CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    METADATA_SERVER_METRICS_STORE_SECRET_FIELD_NUMBER: _ClassVar[int]
    QUERY_SERVER_METRICS_STORE_SECRET_FIELD_NUMBER: _ClassVar[int]
    PINNED_BASE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_TIMESCALEDB_ID_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_PERSISTENCE_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_WORKFLOW_ORCHESTRATOR_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_TIMESCALEDB_SECRET_FIELD_NUMBER: _ClassVar[int]
    GRPC_ENGINE_URL_FIELD_NUMBER: _ClassVar[int]
    KUBE_CLUSTER_MODE_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_URL_FIELD_NUMBER: _ClassVar[int]
    KUBE_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    MANAGED_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_AT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BUILD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_DB_KIND_FIELD_NUMBER: _ClassVar[int]
    VECTOR_DB_SECRET_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_METADATA_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_METADATA_FIELD_NUMBER: _ClassVar[int]
    DATAPLANE_DB_DIRECT_SECRET_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_LINKED_CLUSTER_CLASS_FIELD_NUMBER: _ClassVar[int]
    name: str
    project_id: str
    id: str
    team_id: str
    active_deployment_id: str
    worker_url: str
    service_url: str
    branch_url: str
    offline_store_secret: str
    online_store_secret: str
    feature_store_secret: str
    postgres_secret: str
    online_store_kind: str
    emq_uri: str
    vpc_connector_name: str
    kube_cluster_name: str
    branch_kube_cluster_name: str
    engine_kube_cluster_name: str
    shadow_engine_kube_cluster_name: str
    kube_job_namespace: str
    kube_preview_namespace: str
    kube_service_account_name: str
    streaming_query_service_uri: str
    skip_offline_writes_for_online_cached_features: bool
    result_bus_topic: str
    online_persistence_mode: str
    metrics_bus_topic: str
    bigtable_instance_name: str
    bigtable_table_name: str
    cloud_account_locator: str
    cloud_region: str
    cloud_tenancy_id: str
    source_bundle_bucket: str
    engine_docker_registry_path: str
    default_planner: str
    additional_env_vars: _containers.ScalarMap[str, str]
    additional_cron_env_vars: _containers.ScalarMap[str, str]
    private_pip_repositories: str
    is_sandbox: bool
    cloud_provider: CloudProviderKind
    cloud_config: _cloud_config_pb2.CloudConfig
    spec_config_json: _containers.MessageMap[str, _struct_pb2.Value]
    archived_at: _timestamp_pb2.Timestamp
    metadata_server_metrics_store_secret: str
    query_server_metrics_store_secret: str
    pinned_base_image: str
    cluster_gateway_id: str
    cluster_timescaledb_id: str
    background_persistence_deployment_id: str
    cluster_workflow_orchestrator_id: str
    environment_buckets: EnvironmentObjectStorageConfig
    cluster_timescaledb_secret: str
    grpc_engine_url: str
    kube_cluster_mode: str
    dashboard_url: str
    kube_cluster_id: str
    managed: bool
    telemetry_deployment_id: str
    suspended_at: _timestamp_pb2.Timestamp
    default_build_profile: DeploymentBuildProfile
    vector_db_kind: VectorDBKind
    vector_db_secret: str
    internal_metadata: _containers.MessageMap[str, _struct_pb2.Value]
    customer_metadata: _containers.MessageMap[str, _struct_pb2.Value]
    dataplane_db_direct_secret: str
    primary_linked_cluster_class: _cluster_class_pb2.ClusterClass
    def __init__(
        self,
        name: _Optional[str] = ...,
        project_id: _Optional[str] = ...,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        active_deployment_id: _Optional[str] = ...,
        worker_url: _Optional[str] = ...,
        service_url: _Optional[str] = ...,
        branch_url: _Optional[str] = ...,
        offline_store_secret: _Optional[str] = ...,
        online_store_secret: _Optional[str] = ...,
        feature_store_secret: _Optional[str] = ...,
        postgres_secret: _Optional[str] = ...,
        online_store_kind: _Optional[str] = ...,
        emq_uri: _Optional[str] = ...,
        vpc_connector_name: _Optional[str] = ...,
        kube_cluster_name: _Optional[str] = ...,
        branch_kube_cluster_name: _Optional[str] = ...,
        engine_kube_cluster_name: _Optional[str] = ...,
        shadow_engine_kube_cluster_name: _Optional[str] = ...,
        kube_job_namespace: _Optional[str] = ...,
        kube_preview_namespace: _Optional[str] = ...,
        kube_service_account_name: _Optional[str] = ...,
        streaming_query_service_uri: _Optional[str] = ...,
        skip_offline_writes_for_online_cached_features: bool = ...,
        result_bus_topic: _Optional[str] = ...,
        online_persistence_mode: _Optional[str] = ...,
        metrics_bus_topic: _Optional[str] = ...,
        bigtable_instance_name: _Optional[str] = ...,
        bigtable_table_name: _Optional[str] = ...,
        cloud_account_locator: _Optional[str] = ...,
        cloud_region: _Optional[str] = ...,
        cloud_tenancy_id: _Optional[str] = ...,
        source_bundle_bucket: _Optional[str] = ...,
        engine_docker_registry_path: _Optional[str] = ...,
        default_planner: _Optional[str] = ...,
        additional_env_vars: _Optional[_Mapping[str, str]] = ...,
        additional_cron_env_vars: _Optional[_Mapping[str, str]] = ...,
        private_pip_repositories: _Optional[str] = ...,
        is_sandbox: bool = ...,
        cloud_provider: _Optional[_Union[CloudProviderKind, str]] = ...,
        cloud_config: _Optional[_Union[_cloud_config_pb2.CloudConfig, _Mapping]] = ...,
        spec_config_json: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        metadata_server_metrics_store_secret: _Optional[str] = ...,
        query_server_metrics_store_secret: _Optional[str] = ...,
        pinned_base_image: _Optional[str] = ...,
        cluster_gateway_id: _Optional[str] = ...,
        cluster_timescaledb_id: _Optional[str] = ...,
        background_persistence_deployment_id: _Optional[str] = ...,
        cluster_workflow_orchestrator_id: _Optional[str] = ...,
        environment_buckets: _Optional[_Union[EnvironmentObjectStorageConfig, _Mapping]] = ...,
        cluster_timescaledb_secret: _Optional[str] = ...,
        grpc_engine_url: _Optional[str] = ...,
        kube_cluster_mode: _Optional[str] = ...,
        dashboard_url: _Optional[str] = ...,
        kube_cluster_id: _Optional[str] = ...,
        managed: bool = ...,
        telemetry_deployment_id: _Optional[str] = ...,
        suspended_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        default_build_profile: _Optional[_Union[DeploymentBuildProfile, str]] = ...,
        vector_db_kind: _Optional[_Union[VectorDBKind, str]] = ...,
        vector_db_secret: _Optional[str] = ...,
        internal_metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        customer_metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        dataplane_db_direct_secret: _Optional[str] = ...,
        primary_linked_cluster_class: _Optional[_Union[_cluster_class_pb2.ClusterClass, str]] = ...,
    ) -> None: ...

class CreateEnvironmentV2Request(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    def __init__(self, environment: _Optional[_Union[Environment, _Mapping]] = ...) -> None: ...

class CreateEnvironmentV2Response(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    def __init__(self, environment: _Optional[_Union[Environment, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentV2Request(_message.Message):
    __slots__ = ("environment", "update_mask")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        environment: _Optional[_Union[Environment, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateEnvironmentV2Response(_message.Message):
    __slots__ = ("environment", "field_changes")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    FIELD_CHANGES_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    field_changes: _containers.RepeatedCompositeFieldContainer[_field_change_pb2.FieldChange]
    def __init__(
        self,
        environment: _Optional[_Union[Environment, _Mapping]] = ...,
        field_changes: _Optional[_Iterable[_Union[_field_change_pb2.FieldChange, _Mapping]]] = ...,
    ) -> None: ...

class DeleteEnvironmentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteEnvironmentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetDefaultEnvironmentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SetDefaultEnvironmentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DiscoveredBucketProbe(_message.Message):
    __slots__ = ("ok", "error", "skipped")
    OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    error: str
    skipped: bool
    def __init__(self, ok: bool = ..., error: _Optional[str] = ..., skipped: bool = ...) -> None: ...

class DiscoveredBucket(_message.Message):
    __slots__ = ("name", "role", "role_label", "source", "config_key", "read", "write", "scope")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ROLE_LABEL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_KEY_FIELD_NUMBER: _ClassVar[int]
    READ_FIELD_NUMBER: _ClassVar[int]
    WRITE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    role: DiscoveredBucketRole
    role_label: str
    source: DiscoveredBucketSource
    config_key: str
    read: DiscoveredBucketProbe
    write: DiscoveredBucketProbe
    scope: DiscoveredBucketScope
    def __init__(
        self,
        name: _Optional[str] = ...,
        role: _Optional[_Union[DiscoveredBucketRole, str]] = ...,
        role_label: _Optional[str] = ...,
        source: _Optional[_Union[DiscoveredBucketSource, str]] = ...,
        config_key: _Optional[str] = ...,
        read: _Optional[_Union[DiscoveredBucketProbe, _Mapping]] = ...,
        write: _Optional[_Union[DiscoveredBucketProbe, _Mapping]] = ...,
        scope: _Optional[_Union[DiscoveredBucketScope, str]] = ...,
    ) -> None: ...

class DiscoverEnvironmentBucketsRequest(_message.Message):
    __slots__ = ("skip_probes",)
    SKIP_PROBES_FIELD_NUMBER: _ClassVar[int]
    skip_probes: bool
    def __init__(self, skip_probes: bool = ...) -> None: ...

class DiscoverEnvironmentBucketsResponse(_message.Message):
    __slots__ = ("buckets",)
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    buckets: _containers.RepeatedCompositeFieldContainer[DiscoveredBucket]
    def __init__(self, buckets: _Optional[_Iterable[_Union[DiscoveredBucket, _Mapping]]] = ...) -> None: ...
