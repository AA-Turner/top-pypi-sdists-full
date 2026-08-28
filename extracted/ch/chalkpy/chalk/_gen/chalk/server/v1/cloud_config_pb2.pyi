from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
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

class AWSCloudWatchConfig(_message.Message):
    __slots__ = ("log_group_path", "log_group_paths")
    LOG_GROUP_PATH_FIELD_NUMBER: _ClassVar[int]
    LOG_GROUP_PATHS_FIELD_NUMBER: _ClassVar[int]
    log_group_path: str
    log_group_paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, log_group_path: _Optional[str] = ..., log_group_paths: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class AWSSecretManagerConfig(_message.Message):
    __slots__ = ("secret_kms_arn", "secret_tags", "secret_prefix")
    class SecretTagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    SECRET_KMS_ARN_FIELD_NUMBER: _ClassVar[int]
    SECRET_TAGS_FIELD_NUMBER: _ClassVar[int]
    SECRET_PREFIX_FIELD_NUMBER: _ClassVar[int]
    secret_kms_arn: str
    secret_tags: _containers.ScalarMap[str, str]
    secret_prefix: str
    def __init__(
        self,
        secret_kms_arn: _Optional[str] = ...,
        secret_tags: _Optional[_Mapping[str, str]] = ...,
        secret_prefix: _Optional[str] = ...,
    ) -> None: ...

class GCPSecretReplicationReplica(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: str
    def __init__(self, location: _Optional[str] = ...) -> None: ...

class GCPRegionConfig(_message.Message):
    __slots__ = ("scope_type",)
    SCOPE_TYPE_FIELD_NUMBER: _ClassVar[int]
    scope_type: str
    def __init__(self, scope_type: _Optional[str] = ...) -> None: ...

class GCPSecretManagerConfig(_message.Message):
    __slots__ = ("secret_region", "replicas")
    SECRET_REGION_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    secret_region: str
    replicas: _containers.RepeatedCompositeFieldContainer[GCPSecretReplicationReplica]
    def __init__(
        self,
        secret_region: _Optional[str] = ...,
        replicas: _Optional[_Iterable[_Union[GCPSecretReplicationReplica, _Mapping]]] = ...,
    ) -> None: ...

class GCPWorkloadIdentity(_message.Message):
    __slots__ = ("gcp_project_number", "gcp_service_account", "pool_id", "provider_id")
    GCP_PROJECT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    GCP_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ID_FIELD_NUMBER: _ClassVar[int]
    gcp_project_number: str
    gcp_service_account: str
    pool_id: str
    provider_id: str
    def __init__(
        self,
        gcp_project_number: _Optional[str] = ...,
        gcp_service_account: _Optional[str] = ...,
        pool_id: _Optional[str] = ...,
        provider_id: _Optional[str] = ...,
    ) -> None: ...

class DockerBuildConfig(_message.Message):
    __slots__ = (
        "builder",
        "push_registry_type",
        "push_registry_tag_prefix",
        "registry_credentials_secret_id",
        "notification_topic",
    )
    BUILDER_FIELD_NUMBER: _ClassVar[int]
    PUSH_REGISTRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PUSH_REGISTRY_TAG_PREFIX_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_CREDENTIALS_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_TOPIC_FIELD_NUMBER: _ClassVar[int]
    builder: str
    push_registry_type: str
    push_registry_tag_prefix: str
    registry_credentials_secret_id: str
    notification_topic: str
    def __init__(
        self,
        builder: _Optional[str] = ...,
        push_registry_type: _Optional[str] = ...,
        push_registry_tag_prefix: _Optional[str] = ...,
        registry_credentials_secret_id: _Optional[str] = ...,
        notification_topic: _Optional[str] = ...,
    ) -> None: ...

class ElasticsearchLogConfig(_message.Message):
    __slots__ = ("username", "password", "endpoint")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    endpoint: str
    def __init__(
        self, username: _Optional[str] = ..., password: _Optional[str] = ..., endpoint: _Optional[str] = ...
    ) -> None: ...

class AWSCloudConfig(_message.Message):
    __slots__ = (
        "account_id",
        "management_role_arn",
        "region",
        "external_id",
        "deprecated_cloud_watch_config",
        "deprecated_secret_manager_config",
        "workload_identity",
        "docker_build_config",
        "elasticsearch_log_config",
        "cloudwatch_config",
        "secretmanager_config",
        "gcp_workload_identity",
        "permissions_boundary_arn",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MANAGEMENT_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_CLOUD_WATCH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_SECRET_MANAGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    DOCKER_BUILD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ELASTICSEARCH_LOG_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CLOUDWATCH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SECRETMANAGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GCP_WORKLOAD_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_BOUNDARY_ARN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    management_role_arn: str
    region: str
    external_id: str
    deprecated_cloud_watch_config: AWSCloudWatchConfig
    deprecated_secret_manager_config: AWSSecretManagerConfig
    workload_identity: GCPWorkloadIdentity
    docker_build_config: DockerBuildConfig
    elasticsearch_log_config: ElasticsearchLogConfig
    cloudwatch_config: AWSCloudWatchConfig
    secretmanager_config: AWSSecretManagerConfig
    gcp_workload_identity: GCPWorkloadIdentity
    permissions_boundary_arn: str
    def __init__(
        self,
        account_id: _Optional[str] = ...,
        management_role_arn: _Optional[str] = ...,
        region: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        deprecated_cloud_watch_config: _Optional[_Union[AWSCloudWatchConfig, _Mapping]] = ...,
        deprecated_secret_manager_config: _Optional[_Union[AWSSecretManagerConfig, _Mapping]] = ...,
        workload_identity: _Optional[_Union[GCPWorkloadIdentity, _Mapping]] = ...,
        docker_build_config: _Optional[_Union[DockerBuildConfig, _Mapping]] = ...,
        elasticsearch_log_config: _Optional[_Union[ElasticsearchLogConfig, _Mapping]] = ...,
        cloudwatch_config: _Optional[_Union[AWSCloudWatchConfig, _Mapping]] = ...,
        secretmanager_config: _Optional[_Union[AWSSecretManagerConfig, _Mapping]] = ...,
        gcp_workload_identity: _Optional[_Union[GCPWorkloadIdentity, _Mapping]] = ...,
        permissions_boundary_arn: _Optional[str] = ...,
    ) -> None: ...

class GCPCloudConfig(_message.Message):
    __slots__ = (
        "project_id",
        "region",
        "management_service_account",
        "docker_build_config",
        "secretmanager_config",
        "region_config",
    )
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    MANAGEMENT_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DOCKER_BUILD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SECRETMANAGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REGION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    region: str
    management_service_account: str
    docker_build_config: DockerBuildConfig
    secretmanager_config: GCPSecretManagerConfig
    region_config: GCPRegionConfig
    def __init__(
        self,
        project_id: _Optional[str] = ...,
        region: _Optional[str] = ...,
        management_service_account: _Optional[str] = ...,
        docker_build_config: _Optional[_Union[DockerBuildConfig, _Mapping]] = ...,
        secretmanager_config: _Optional[_Union[GCPSecretManagerConfig, _Mapping]] = ...,
        region_config: _Optional[_Union[GCPRegionConfig, _Mapping]] = ...,
    ) -> None: ...

class AzureContainerRegistryConfig(_message.Message):
    __slots__ = ("registry_name",)
    REGISTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    registry_name: str
    def __init__(self, registry_name: _Optional[str] = ...) -> None: ...

class AzureKeyVaultConfig(_message.Message):
    __slots__ = ("vault_name",)
    VAULT_NAME_FIELD_NUMBER: _ClassVar[int]
    vault_name: str
    def __init__(self, vault_name: _Optional[str] = ...) -> None: ...

class AzureCloudConfig(_message.Message):
    __slots__ = (
        "subscription_id",
        "tenant_id",
        "region",
        "resource_group",
        "docker_build_config",
        "container_registry_config",
        "key_vault_config",
        "gcp_workload_identity",
    )
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    DOCKER_BUILD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_REGISTRY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    KEY_VAULT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GCP_WORKLOAD_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    subscription_id: str
    tenant_id: str
    region: str
    resource_group: str
    docker_build_config: DockerBuildConfig
    container_registry_config: AzureContainerRegistryConfig
    key_vault_config: AzureKeyVaultConfig
    gcp_workload_identity: GCPWorkloadIdentity
    def __init__(
        self,
        subscription_id: _Optional[str] = ...,
        tenant_id: _Optional[str] = ...,
        region: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        docker_build_config: _Optional[_Union[DockerBuildConfig, _Mapping]] = ...,
        container_registry_config: _Optional[_Union[AzureContainerRegistryConfig, _Mapping]] = ...,
        key_vault_config: _Optional[_Union[AzureKeyVaultConfig, _Mapping]] = ...,
        gcp_workload_identity: _Optional[_Union[GCPWorkloadIdentity, _Mapping]] = ...,
    ) -> None: ...

class CloudConfig(_message.Message):
    __slots__ = ("aws", "gcp", "azure")
    AWS_FIELD_NUMBER: _ClassVar[int]
    GCP_FIELD_NUMBER: _ClassVar[int]
    AZURE_FIELD_NUMBER: _ClassVar[int]
    aws: AWSCloudConfig
    gcp: GCPCloudConfig
    azure: AzureCloudConfig
    def __init__(
        self,
        aws: _Optional[_Union[AWSCloudConfig, _Mapping]] = ...,
        gcp: _Optional[_Union[GCPCloudConfig, _Mapping]] = ...,
        azure: _Optional[_Union[AzureCloudConfig, _Mapping]] = ...,
    ) -> None: ...
