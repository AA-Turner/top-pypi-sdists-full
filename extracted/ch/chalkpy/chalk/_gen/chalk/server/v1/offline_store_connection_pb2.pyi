from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class StorageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STORAGE_TYPE_UNSPECIFIED: _ClassVar[StorageType]
    STORAGE_TYPE_OFFLINE_STORE: _ClassVar[StorageType]

STORAGE_TYPE_UNSPECIFIED: StorageType
STORAGE_TYPE_OFFLINE_STORE: StorageType

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
    __slots__ = ("s3", "gcp", "integration_name")
    S3_FIELD_NUMBER: _ClassVar[int]
    GCP_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
    s3: S3StorageIntegrationConfig
    gcp: GcpStorageIntegrationConfig
    integration_name: str
    def __init__(
        self,
        s3: _Optional[_Union[S3StorageIntegrationConfig, _Mapping]] = ...,
        gcp: _Optional[_Union[GcpStorageIntegrationConfig, _Mapping]] = ...,
        integration_name: _Optional[str] = ...,
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

class DatabricksOfflineStoreConnectionConfigInput(_message.Message):
    __slots__ = ("host", "http_path", "catalog", "schema", "client_id", "client_secret")
    HOST_FIELD_NUMBER: _ClassVar[int]
    HTTP_PATH_FIELD_NUMBER: _ClassVar[int]
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    host: str
    http_path: str
    catalog: str
    schema: str
    client_id: str
    client_secret: str
    def __init__(
        self,
        host: _Optional[str] = ...,
        http_path: _Optional[str] = ...,
        catalog: _Optional[str] = ...,
        schema: _Optional[str] = ...,
        client_id: _Optional[str] = ...,
        client_secret: _Optional[str] = ...,
    ) -> None: ...

class DatabricksOfflineStoreConnectionConfigStored(_message.Message):
    __slots__ = ("host", "http_path", "catalog", "schema", "client_id", "client_secret_secret_id")
    HOST_FIELD_NUMBER: _ClassVar[int]
    HTTP_PATH_FIELD_NUMBER: _ClassVar[int]
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    host: str
    http_path: str
    catalog: str
    schema: str
    client_id: str
    client_secret_secret_id: str
    def __init__(
        self,
        host: _Optional[str] = ...,
        http_path: _Optional[str] = ...,
        catalog: _Optional[str] = ...,
        schema: _Optional[str] = ...,
        client_id: _Optional[str] = ...,
        client_secret_secret_id: _Optional[str] = ...,
    ) -> None: ...

class IcebergGlueS3CatalogConfig(_message.Message):
    __slots__ = ("s3_bucket", "glue_database_name", "account_id", "role_arn", "region")
    S3_BUCKET_FIELD_NUMBER: _ClassVar[int]
    GLUE_DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    s3_bucket: str
    glue_database_name: str
    account_id: str
    role_arn: str
    region: str
    def __init__(
        self,
        s3_bucket: _Optional[str] = ...,
        glue_database_name: _Optional[str] = ...,
        account_id: _Optional[str] = ...,
        role_arn: _Optional[str] = ...,
        region: _Optional[str] = ...,
    ) -> None: ...

class IcebergOfflineStoreConnectionConfig(_message.Message):
    __slots__ = ("glue_s3",)
    GLUE_S3_FIELD_NUMBER: _ClassVar[int]
    glue_s3: IcebergGlueS3CatalogConfig
    def __init__(self, glue_s3: _Optional[_Union[IcebergGlueS3CatalogConfig, _Mapping]] = ...) -> None: ...

class OfflineStoreConnectionConfigInput(_message.Message):
    __slots__ = ("snowflake", "bigquery", "iceberg", "databricks")
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_FIELD_NUMBER: _ClassVar[int]
    ICEBERG_FIELD_NUMBER: _ClassVar[int]
    DATABRICKS_FIELD_NUMBER: _ClassVar[int]
    snowflake: SnowflakeOfflineStoreConnectionConfigInput
    bigquery: BigQueryOfflineStoreConnectionConfig
    iceberg: IcebergOfflineStoreConnectionConfig
    databricks: DatabricksOfflineStoreConnectionConfigInput
    def __init__(
        self,
        snowflake: _Optional[_Union[SnowflakeOfflineStoreConnectionConfigInput, _Mapping]] = ...,
        bigquery: _Optional[_Union[BigQueryOfflineStoreConnectionConfig, _Mapping]] = ...,
        iceberg: _Optional[_Union[IcebergOfflineStoreConnectionConfig, _Mapping]] = ...,
        databricks: _Optional[_Union[DatabricksOfflineStoreConnectionConfigInput, _Mapping]] = ...,
    ) -> None: ...

class OfflineStoreConnectionConfigStored(_message.Message):
    __slots__ = ("snowflake", "bigquery", "iceberg", "databricks")
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_FIELD_NUMBER: _ClassVar[int]
    ICEBERG_FIELD_NUMBER: _ClassVar[int]
    DATABRICKS_FIELD_NUMBER: _ClassVar[int]
    snowflake: SnowflakeOfflineStoreConnectionConfigStored
    bigquery: BigQueryOfflineStoreConnectionConfig
    iceberg: IcebergOfflineStoreConnectionConfig
    databricks: DatabricksOfflineStoreConnectionConfigStored
    def __init__(
        self,
        snowflake: _Optional[_Union[SnowflakeOfflineStoreConnectionConfigStored, _Mapping]] = ...,
        bigquery: _Optional[_Union[BigQueryOfflineStoreConnectionConfig, _Mapping]] = ...,
        iceberg: _Optional[_Union[IcebergOfflineStoreConnectionConfig, _Mapping]] = ...,
        databricks: _Optional[_Union[DatabricksOfflineStoreConnectionConfigStored, _Mapping]] = ...,
    ) -> None: ...

class OfflineStoreConnectionInput(_message.Message):
    __slots__ = ("name", "config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    config: OfflineStoreConnectionConfigInput
    def __init__(
        self, name: _Optional[str] = ..., config: _Optional[_Union[OfflineStoreConnectionConfigInput, _Mapping]] = ...
    ) -> None: ...

class OfflineStoreConnection(_message.Message):
    __slots__ = ("id", "team_id", "environment_id", "name", "config", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    environment_id: str
    name: str
    config: OfflineStoreConnectionConfigStored
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        config: _Optional[_Union[OfflineStoreConnectionConfigStored, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CreateOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: OfflineStoreConnectionInput
    def __init__(self, connection: _Optional[_Union[OfflineStoreConnectionInput, _Mapping]] = ...) -> None: ...

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
    __slots__ = ("id", "connection", "update_mask")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    connection: OfflineStoreConnectionInput
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        id: _Optional[str] = ...,
        connection: _Optional[_Union[OfflineStoreConnectionInput, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
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

class CreateBindingEnvironmentOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("environment_id", "offline_store_connection_id", "name")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    offline_store_connection_id: str
    name: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        offline_store_connection_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class CreateBindingEnvironmentOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBindingEnvironmentOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetBindingEnvironmentOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ("environment_id", "offline_store_connection_id", "name")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    offline_store_connection_id: str
    name: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        offline_store_connection_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class DeleteBindingEnvironmentOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("environment_id", "offline_store_connection_id")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    offline_store_connection_id: str
    def __init__(
        self, environment_id: _Optional[str] = ..., offline_store_connection_id: _Optional[str] = ...
    ) -> None: ...

class DeleteBindingEnvironmentOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MigrateOfflineStoreConnectionRequest(_message.Message):
    __slots__ = ("offline_store_connection_id",)
    OFFLINE_STORE_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    offline_store_connection_id: str
    def __init__(self, offline_store_connection_id: _Optional[str] = ...) -> None: ...

class MigrateOfflineStoreConnectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
