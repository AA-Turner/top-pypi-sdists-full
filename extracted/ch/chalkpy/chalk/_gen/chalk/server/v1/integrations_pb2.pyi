from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import environment_secrets_pb2 as _environment_secrets_pb2
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

class Integration(_message.Message):
    __slots__ = ("id", "name", "kind", "environment_id", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    kind: IntegrationKind
    environment_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        kind: _Optional[_Union[IntegrationKind, str]] = ...,
        environment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
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

class ListIntegrationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListIntegrationsResponse(_message.Message):
    __slots__ = ("integrations",)
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[Integration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[Integration, _Mapping]]] = ...) -> None: ...

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

class InsertIntegrationRequest(_message.Message):
    __slots__ = ("name", "integration_kind", "environment_variables")
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_KIND_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    name: str
    integration_kind: IntegrationKind
    environment_variables: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        integration_kind: _Optional[_Union[IntegrationKind, str]] = ...,
        environment_variables: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class InsertIntegrationResponse(_message.Message):
    __slots__ = ("integration",)
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    integration: Integration
    def __init__(self, integration: _Optional[_Union[Integration, _Mapping]] = ...) -> None: ...

class UpdateIntegrationRequest(_message.Message):
    __slots__ = ("name", "integration_id", "environment_variables")
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    name: str
    integration_id: str
    environment_variables: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        integration_id: _Optional[str] = ...,
        environment_variables: _Optional[_Mapping[str, str]] = ...,
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

class TestIntegrationRequest(_message.Message):
    __slots__ = ("kind", "environment_variables", "integration_id")
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    KIND_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    kind: IntegrationKind
    environment_variables: _containers.ScalarMap[str, str]
    integration_id: str
    def __init__(
        self,
        kind: _Optional[_Union[IntegrationKind, str]] = ...,
        environment_variables: _Optional[_Mapping[str, str]] = ...,
        integration_id: _Optional[str] = ...,
    ) -> None: ...

class TestIntegrationResponse(_message.Message):
    __slots__ = ("kind", "success", "message", "latency_seconds")
    KIND_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    kind: str
    success: bool
    message: str
    latency_seconds: float
    def __init__(
        self,
        kind: _Optional[str] = ...,
        success: bool = ...,
        message: _Optional[str] = ...,
        latency_seconds: _Optional[float] = ...,
    ) -> None: ...
