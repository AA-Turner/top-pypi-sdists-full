from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
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

class S3StorageIntegrationConfig(_message.Message):
    __slots__ = ("bucket_name", "region", "role_arn")
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    bucket_name: str
    region: str
    role_arn: str
    def __init__(
        self, bucket_name: _Optional[str] = ..., region: _Optional[str] = ..., role_arn: _Optional[str] = ...
    ) -> None: ...

class GcpStorageIntegrationConfig(_message.Message):
    __slots__ = ("bucket_name", "service_account")
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    bucket_name: str
    service_account: str
    def __init__(self, bucket_name: _Optional[str] = ..., service_account: _Optional[str] = ...) -> None: ...

class SnowflakeStorageIntegration(_message.Message):
    __slots__ = ("s3", "gcp")
    S3_FIELD_NUMBER: _ClassVar[int]
    GCP_FIELD_NUMBER: _ClassVar[int]
    s3: S3StorageIntegrationConfig
    gcp: GcpStorageIntegrationConfig
    def __init__(
        self,
        s3: _Optional[_Union[S3StorageIntegrationConfig, _Mapping]] = ...,
        gcp: _Optional[_Union[GcpStorageIntegrationConfig, _Mapping]] = ...,
    ) -> None: ...

class SnowflakeCredentialsInput(_message.Message):
    __slots__ = ("account", "username", "password", "private_key", "warehouse", "database", "schema", "role")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    account: str
    username: str
    password: str
    private_key: str
    warehouse: str
    database: str
    schema: str
    role: str
    def __init__(
        self,
        account: _Optional[str] = ...,
        username: _Optional[str] = ...,
        password: _Optional[str] = ...,
        private_key: _Optional[str] = ...,
        warehouse: _Optional[str] = ...,
        database: _Optional[str] = ...,
        schema: _Optional[str] = ...,
        role: _Optional[str] = ...,
    ) -> None: ...

class SnowflakeCredentialsStored(_message.Message):
    __slots__ = (
        "account",
        "username",
        "password_secret_id",
        "private_key_secret_id",
        "warehouse",
        "database",
        "schema",
        "role",
    )
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    account: str
    username: str
    password_secret_id: str
    private_key_secret_id: str
    warehouse: str
    database: str
    schema: str
    role: str
    def __init__(
        self,
        account: _Optional[str] = ...,
        username: _Optional[str] = ...,
        password_secret_id: _Optional[str] = ...,
        private_key_secret_id: _Optional[str] = ...,
        warehouse: _Optional[str] = ...,
        database: _Optional[str] = ...,
        schema: _Optional[str] = ...,
        role: _Optional[str] = ...,
    ) -> None: ...

class SnowflakeOfflineStoreConnectionConfigInput(_message.Message):
    __slots__ = ("credentials", "storage_integration")
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    credentials: SnowflakeCredentialsInput
    storage_integration: SnowflakeStorageIntegration
    def __init__(
        self,
        credentials: _Optional[_Union[SnowflakeCredentialsInput, _Mapping]] = ...,
        storage_integration: _Optional[_Union[SnowflakeStorageIntegration, _Mapping]] = ...,
    ) -> None: ...

class SnowflakeOfflineStoreConnectionConfigStored(_message.Message):
    __slots__ = ("credentials", "storage_integration")
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    credentials: SnowflakeCredentialsStored
    storage_integration: SnowflakeStorageIntegration
    def __init__(
        self,
        credentials: _Optional[_Union[SnowflakeCredentialsStored, _Mapping]] = ...,
        storage_integration: _Optional[_Union[SnowflakeStorageIntegration, _Mapping]] = ...,
    ) -> None: ...

class BigQueryOfflineStoreConnectionConfig(_message.Message):
    __slots__ = ("project_id", "dataset_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    dataset_id: str
    def __init__(self, project_id: _Optional[str] = ..., dataset_id: _Optional[str] = ...) -> None: ...

class OfflineStoreConnectionConfigInput(_message.Message):
    __slots__ = ("snowflake", "bigquery")
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_FIELD_NUMBER: _ClassVar[int]
    snowflake: SnowflakeOfflineStoreConnectionConfigInput
    bigquery: BigQueryOfflineStoreConnectionConfig
    def __init__(
        self,
        snowflake: _Optional[_Union[SnowflakeOfflineStoreConnectionConfigInput, _Mapping]] = ...,
        bigquery: _Optional[_Union[BigQueryOfflineStoreConnectionConfig, _Mapping]] = ...,
    ) -> None: ...

class OfflineStoreConnectionConfigStored(_message.Message):
    __slots__ = ("snowflake", "bigquery")
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_FIELD_NUMBER: _ClassVar[int]
    snowflake: SnowflakeOfflineStoreConnectionConfigStored
    bigquery: BigQueryOfflineStoreConnectionConfig
    def __init__(
        self,
        snowflake: _Optional[_Union[SnowflakeOfflineStoreConnectionConfigStored, _Mapping]] = ...,
        bigquery: _Optional[_Union[BigQueryOfflineStoreConnectionConfig, _Mapping]] = ...,
    ) -> None: ...

class OfflineStoreConnection(_message.Message):
    __slots__ = ("id", "environment_id", "team_id", "name", "config", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    team_id: str
    name: str
    config: OfflineStoreConnectionConfigStored
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        config: _Optional[_Union[OfflineStoreConnectionConfigStored, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CreateOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("name", "config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    config: OfflineStoreConnectionConfigInput
    def __init__(
        self, name: _Optional[str] = ..., config: _Optional[_Union[OfflineStoreConnectionConfigInput, _Mapping]] = ...
    ) -> None: ...

class CreateOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: OfflineStoreConnection
    def __init__(self, connection: _Optional[_Union[OfflineStoreConnection, _Mapping]] = ...) -> None: ...

class GetOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: OfflineStoreConnection
    def __init__(self, connection: _Optional[_Union[OfflineStoreConnection, _Mapping]] = ...) -> None: ...

class ListOfflineStoreConnectionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOfflineStoreConnectionsResponse(_message.Message):
    __slots__ = ("connections",)
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[OfflineStoreConnection]
    def __init__(self, connections: _Optional[_Iterable[_Union[OfflineStoreConnection, _Mapping]]] = ...) -> None: ...

class UpdateOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("id", "name", "config")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    config: OfflineStoreConnectionConfigInput
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        config: _Optional[_Union[OfflineStoreConnectionConfigInput, _Mapping]] = ...,
    ) -> None: ...

class UpdateOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: OfflineStoreConnection
    def __init__(self, connection: _Optional[_Union[OfflineStoreConnection, _Mapping]] = ...) -> None: ...

class DeleteOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("id", "config")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    config: OfflineStoreConnectionConfigInput
    def __init__(
        self, id: _Optional[str] = ..., config: _Optional[_Union[OfflineStoreConnectionConfigInput, _Mapping]] = ...
    ) -> None: ...

class TestOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ("success", "message", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    error: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...
