from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import environment_secrets_pb2 as _environment_secrets_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
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

class IntegrationKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTEGRATION_KIND_UNSPECIFIED: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_ATHENA: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_AWS: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_BIGQUERY: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_CLICKHOUSE: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_COHERE: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_DATABRICKS: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_DYNAMODB: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_GCP: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_KAFKA: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_KINESIS: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_MYSQL: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_OPENAI: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_POSTGRESQL: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_PUBSUB: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_REDSHIFT: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_SNOWFLAKE: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_SPANNER: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_TRINO: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_MSSQL: _ClassVar[IntegrationKind]
    INTEGRATION_KIND_HUGGINGFACE: _ClassVar[IntegrationKind]

class IntegrationWarningCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTEGRATION_WARNING_CODE_UNSPECIFIED: _ClassVar[IntegrationWarningCode]
    INTEGRATION_WARNING_CODE_SNOWFLAKE_UNLOAD_NOT_CONFIGURED: _ClassVar[IntegrationWarningCode]

INTEGRATION_KIND_UNSPECIFIED: IntegrationKind
INTEGRATION_KIND_ATHENA: IntegrationKind
INTEGRATION_KIND_AWS: IntegrationKind
INTEGRATION_KIND_BIGQUERY: IntegrationKind
INTEGRATION_KIND_CLICKHOUSE: IntegrationKind
INTEGRATION_KIND_COHERE: IntegrationKind
INTEGRATION_KIND_DATABRICKS: IntegrationKind
INTEGRATION_KIND_DYNAMODB: IntegrationKind
INTEGRATION_KIND_GCP: IntegrationKind
INTEGRATION_KIND_KAFKA: IntegrationKind
INTEGRATION_KIND_KINESIS: IntegrationKind
INTEGRATION_KIND_MYSQL: IntegrationKind
INTEGRATION_KIND_OPENAI: IntegrationKind
INTEGRATION_KIND_POSTGRESQL: IntegrationKind
INTEGRATION_KIND_PUBSUB: IntegrationKind
INTEGRATION_KIND_REDSHIFT: IntegrationKind
INTEGRATION_KIND_SNOWFLAKE: IntegrationKind
INTEGRATION_KIND_SPANNER: IntegrationKind
INTEGRATION_KIND_TRINO: IntegrationKind
INTEGRATION_KIND_MSSQL: IntegrationKind
INTEGRATION_KIND_HUGGINGFACE: IntegrationKind
INTEGRATION_WARNING_CODE_UNSPECIFIED: IntegrationWarningCode
INTEGRATION_WARNING_CODE_SNOWFLAKE_UNLOAD_NOT_CONFIGURED: IntegrationWarningCode

class IntegrationWarning(_message.Message):
    __slots__ = ("code", "title", "message", "config_keys")
    CODE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_KEYS_FIELD_NUMBER: _ClassVar[int]
    code: IntegrationWarningCode
    title: str
    message: str
    config_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        code: _Optional[_Union[IntegrationWarningCode, str]] = ...,
        title: _Optional[str] = ...,
        message: _Optional[str] = ...,
        config_keys: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class Integration(_message.Message):
    __slots__ = ("id", "name", "kind", "environment_id", "created_at", "updated_at", "warnings")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    kind: IntegrationKind
    environment_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    warnings: _containers.RepeatedCompositeFieldContainer[IntegrationWarning]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        kind: _Optional[_Union[IntegrationKind, str]] = ...,
        environment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        warnings: _Optional[_Iterable[_Union[IntegrationWarning, _Mapping]]] = ...,
    ) -> None: ...

class IntegrationWithSecrets(_message.Message):
    __slots__ = ("integration", "secrets")
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    integration: Integration
    secrets: _containers.RepeatedCompositeFieldContainer[_environment_secrets_pb2.SecretWithValue]
    def __init__(
        self,
        integration: _Optional[_Union[Integration, _Mapping]] = ...,
        secrets: _Optional[_Iterable[_Union[_environment_secrets_pb2.SecretWithValue, _Mapping]]] = ...,
    ) -> None: ...

class DatasourcePermissionTag(_message.Message):
    __slots__ = ("kind", "name", "permission_tags", "created_at", "updated_at")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    kind: IntegrationKind
    name: str
    permission_tags: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        kind: _Optional[_Union[IntegrationKind, str]] = ...,
        name: _Optional[str] = ...,
        permission_tags: _Optional[_Iterable[str]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListIntegrationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListIntegrationsResponse(_message.Message):
    __slots__ = ("integrations",)
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[Integration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[Integration, _Mapping]]] = ...) -> None: ...

class ListDatasourcePermissionTagsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDatasourcePermissionTagsResponse(_message.Message):
    __slots__ = ("datasource_permission_tags",)
    DATASOURCE_PERMISSION_TAGS_FIELD_NUMBER: _ClassVar[int]
    datasource_permission_tags: _containers.RepeatedCompositeFieldContainer[DatasourcePermissionTag]
    def __init__(
        self, datasource_permission_tags: _Optional[_Iterable[_Union[DatasourcePermissionTag, _Mapping]]] = ...
    ) -> None: ...

class GetDatasourcePermissionTagRequest(_message.Message):
    __slots__ = ("kind", "name")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    kind: IntegrationKind
    name: str
    def __init__(self, kind: _Optional[_Union[IntegrationKind, str]] = ..., name: _Optional[str] = ...) -> None: ...

class GetDatasourcePermissionTagResponse(_message.Message):
    __slots__ = ("datasource_permission_tag",)
    DATASOURCE_PERMISSION_TAG_FIELD_NUMBER: _ClassVar[int]
    datasource_permission_tag: DatasourcePermissionTag
    def __init__(
        self, datasource_permission_tag: _Optional[_Union[DatasourcePermissionTag, _Mapping]] = ...
    ) -> None: ...

class ListIntegrationsAndSecretsRequest(_message.Message):
    __slots__ = ("decrypt",)
    DECRYPT_FIELD_NUMBER: _ClassVar[int]
    decrypt: bool
    def __init__(self, decrypt: bool = ...) -> None: ...

class ListIntegrationsAndSecretsResponse(_message.Message):
    __slots__ = ("integrations", "custom_secrets")
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_SECRETS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[IntegrationWithSecrets]
    custom_secrets: _containers.RepeatedCompositeFieldContainer[_environment_secrets_pb2.SecretWithValue]
    def __init__(
        self,
        integrations: _Optional[_Iterable[_Union[IntegrationWithSecrets, _Mapping]]] = ...,
        custom_secrets: _Optional[_Iterable[_Union[_environment_secrets_pb2.SecretWithValue, _Mapping]]] = ...,
    ) -> None: ...

class GetIntegrationValueRequest(_message.Message):
    __slots__ = ("integration_id", "secret_name")
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    integration_id: str
    secret_name: str
    def __init__(self, integration_id: _Optional[str] = ..., secret_name: _Optional[str] = ...) -> None: ...

class GetIntegrationValueResponse(_message.Message):
    __slots__ = ("secretvalue",)
    SECRETVALUE_FIELD_NUMBER: _ClassVar[int]
    secretvalue: _environment_secrets_pb2.SecretValue
    def __init__(
        self, secretvalue: _Optional[_Union[_environment_secrets_pb2.SecretValue, _Mapping]] = ...
    ) -> None: ...

class GetIntegrationRequest(_message.Message):
    __slots__ = ("integration_id",)
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    integration_id: str
    def __init__(self, integration_id: _Optional[str] = ...) -> None: ...

class GetIntegrationResponse(_message.Message):
    __slots__ = ("integration_with_secrets",)
    INTEGRATION_WITH_SECRETS_FIELD_NUMBER: _ClassVar[int]
    integration_with_secrets: IntegrationWithSecrets
    def __init__(self, integration_with_secrets: _Optional[_Union[IntegrationWithSecrets, _Mapping]] = ...) -> None: ...

class GetIntegrationByNameRequest(_message.Message):
    __slots__ = ("integration_name",)
    INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
    integration_name: str
    def __init__(self, integration_name: _Optional[str] = ...) -> None: ...

class GetIntegrationByNameResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: Integration
    def __init__(self, integration: _Optional[_Union[Integration, _Mapping]] = ...) -> None: ...

class IntegrationConfigValue(_message.Message):
    __slots__ = ("literal", "secret_id")
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    literal: str
    secret_id: str
    def __init__(self, literal: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class InsertIntegrationRequest(_message.Message):
    __slots__ = ("name", "integration_kind", "environment_variables", "config")
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: IntegrationConfigValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[IntegrationConfigValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_KIND_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    integration_kind: IntegrationKind
    environment_variables: _containers.ScalarMap[str, str]
    config: _containers.MessageMap[str, IntegrationConfigValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        integration_kind: _Optional[_Union[IntegrationKind, str]] = ...,
        environment_variables: _Optional[_Mapping[str, str]] = ...,
        config: _Optional[_Mapping[str, IntegrationConfigValue]] = ...,
    ) -> None: ...

class InsertIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: Integration
    def __init__(self, integration: _Optional[_Union[Integration, _Mapping]] = ...) -> None: ...

class UpdateIntegrationRequest(_message.Message):
    __slots__ = ("name", "integration_id", "environment_variables", "config")
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: IntegrationConfigValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[IntegrationConfigValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    integration_id: str
    environment_variables: _containers.ScalarMap[str, str]
    config: _containers.MessageMap[str, IntegrationConfigValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        integration_id: _Optional[str] = ...,
        environment_variables: _Optional[_Mapping[str, str]] = ...,
        config: _Optional[_Mapping[str, IntegrationConfigValue]] = ...,
    ) -> None: ...

class UpdateIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: Integration
    def __init__(self, integration: _Optional[_Union[Integration, _Mapping]] = ...) -> None: ...

class DeleteIntegrationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteIntegrationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpsertDatasourcePermissionTagRequest(_message.Message):
    __slots__ = ("kind", "name", "permission_tags")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TAGS_FIELD_NUMBER: _ClassVar[int]
    kind: IntegrationKind
    name: str
    permission_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        kind: _Optional[_Union[IntegrationKind, str]] = ...,
        name: _Optional[str] = ...,
        permission_tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UpsertDatasourcePermissionTagResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteDatasourcePermissionTagRequest(_message.Message):
    __slots__ = ("kind", "name")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    kind: IntegrationKind
    name: str
    def __init__(self, kind: _Optional[_Union[IntegrationKind, str]] = ..., name: _Optional[str] = ...) -> None: ...

class DeleteDatasourcePermissionTagResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PreviewedMessage(_message.Message):
    __slots__ = ("value_base64", "key_base64", "topic", "partition", "offset", "timestamp_ms")
    VALUE_BASE64_FIELD_NUMBER: _ClassVar[int]
    KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
    value_base64: str
    key_base64: str
    topic: str
    partition: str
    offset: str
    timestamp_ms: int
    def __init__(
        self,
        value_base64: _Optional[str] = ...,
        key_base64: _Optional[str] = ...,
        topic: _Optional[str] = ...,
        partition: _Optional[str] = ...,
        offset: _Optional[str] = ...,
        timestamp_ms: _Optional[int] = ...,
    ) -> None: ...

class TestIntegrationRequest(_message.Message):
    __slots__ = ("kind", "environment_variables", "config", "integration_id", "include_preview")
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: IntegrationConfigValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[IntegrationConfigValue, _Mapping]] = ...
        ) -> None: ...

    KIND_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    kind: IntegrationKind
    environment_variables: _containers.ScalarMap[str, str]
    config: _containers.MessageMap[str, IntegrationConfigValue]
    integration_id: str
    include_preview: bool
    def __init__(
        self,
        kind: _Optional[_Union[IntegrationKind, str]] = ...,
        environment_variables: _Optional[_Mapping[str, str]] = ...,
        config: _Optional[_Mapping[str, IntegrationConfigValue]] = ...,
        integration_id: _Optional[str] = ...,
        include_preview: bool = ...,
    ) -> None: ...

class TestIntegrationResponse(_message.Message):
    __slots__ = ("kind", "success", "message", "latency_seconds", "preview_messages")
    KIND_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    kind: str
    success: bool
    message: str
    latency_seconds: float
    preview_messages: _containers.RepeatedCompositeFieldContainer[PreviewedMessage]
    def __init__(
        self,
        kind: _Optional[str] = ...,
        success: bool = ...,
        message: _Optional[str] = ...,
        latency_seconds: _Optional[float] = ...,
        preview_messages: _Optional[_Iterable[_Union[PreviewedMessage, _Mapping]]] = ...,
    ) -> None: ...

class SnowflakeNamedStage(_message.Message):
    __slots__ = ("name", "database_name", "schema_name", "reference", "kind", "url", "comment", "storage_integration")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    STORAGE_INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    database_name: str
    schema_name: str
    reference: str
    kind: str
    url: str
    comment: str
    storage_integration: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        database_name: _Optional[str] = ...,
        schema_name: _Optional[str] = ...,
        reference: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        url: _Optional[str] = ...,
        comment: _Optional[str] = ...,
        storage_integration: _Optional[str] = ...,
    ) -> None: ...

class SnowflakeUnloadStorageIntegration(_message.Message):
    __slots__ = ("name", "type", "provider", "enabled", "allowed_locations", "comment")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    provider: str
    enabled: bool
    allowed_locations: _containers.RepeatedScalarFieldContainer[str]
    comment: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[str] = ...,
        provider: _Optional[str] = ...,
        enabled: bool = ...,
        allowed_locations: _Optional[_Iterable[str]] = ...,
        comment: _Optional[str] = ...,
    ) -> None: ...

class ListSnowflakeNamedStagesRequest(_message.Message):
    __slots__ = ("config", "integration_id")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: IntegrationConfigValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[IntegrationConfigValue, _Mapping]] = ...
        ) -> None: ...

    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    config: _containers.MessageMap[str, IntegrationConfigValue]
    integration_id: str
    def __init__(
        self, config: _Optional[_Mapping[str, IntegrationConfigValue]] = ..., integration_id: _Optional[str] = ...
    ) -> None: ...

class ListSnowflakeNamedStagesResponse(_message.Message):
    __slots__ = ("stages", "truncated", "storage_integrations")
    STAGES_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    STORAGE_INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    stages: _containers.RepeatedCompositeFieldContainer[SnowflakeNamedStage]
    truncated: bool
    storage_integrations: _containers.RepeatedCompositeFieldContainer[SnowflakeUnloadStorageIntegration]
    def __init__(
        self,
        stages: _Optional[_Iterable[_Union[SnowflakeNamedStage, _Mapping]]] = ...,
        truncated: bool = ...,
        storage_integrations: _Optional[_Iterable[_Union[SnowflakeUnloadStorageIntegration, _Mapping]]] = ...,
    ) -> None: ...
