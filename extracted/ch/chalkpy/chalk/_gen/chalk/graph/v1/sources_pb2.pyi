from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class StreamSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STREAM_SOURCE_TYPE_UNSPECIFIED: _ClassVar[StreamSourceType]
    STREAM_SOURCE_TYPE_KAFKA: _ClassVar[StreamSourceType]
    STREAM_SOURCE_TYPE_KINESIS: _ClassVar[StreamSourceType]
    STREAM_SOURCE_TYPE_PUBSUB: _ClassVar[StreamSourceType]

class DatabaseSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATABASE_SOURCE_TYPE_UNSPECIFIED: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_BIGQUERY: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_CLOUDSQL: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_DATABRICKS: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_MYSQL: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_POSTGRES: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_REDSHIFT: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_SNOWFLAKE: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_SQLITE: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_SPANNER: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_TRINO: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_DYNAMODB: _ClassVar[DatabaseSourceType]
    DATABASE_SOURCE_TYPE_ATHENA: _ClassVar[DatabaseSourceType]

STREAM_SOURCE_TYPE_UNSPECIFIED: StreamSourceType
STREAM_SOURCE_TYPE_KAFKA: StreamSourceType
STREAM_SOURCE_TYPE_KINESIS: StreamSourceType
STREAM_SOURCE_TYPE_PUBSUB: StreamSourceType
DATABASE_SOURCE_TYPE_UNSPECIFIED: DatabaseSourceType
DATABASE_SOURCE_TYPE_BIGQUERY: DatabaseSourceType
DATABASE_SOURCE_TYPE_CLOUDSQL: DatabaseSourceType
DATABASE_SOURCE_TYPE_DATABRICKS: DatabaseSourceType
DATABASE_SOURCE_TYPE_MYSQL: DatabaseSourceType
DATABASE_SOURCE_TYPE_POSTGRES: DatabaseSourceType
DATABASE_SOURCE_TYPE_REDSHIFT: DatabaseSourceType
DATABASE_SOURCE_TYPE_SNOWFLAKE: DatabaseSourceType
DATABASE_SOURCE_TYPE_SQLITE: DatabaseSourceType
DATABASE_SOURCE_TYPE_SPANNER: DatabaseSourceType
DATABASE_SOURCE_TYPE_TRINO: DatabaseSourceType
DATABASE_SOURCE_TYPE_DYNAMODB: DatabaseSourceType
DATABASE_SOURCE_TYPE_ATHENA: DatabaseSourceType

class StreamSourceReference(_message.Message):
    __slots__ = ("type", "name")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    type: StreamSourceType
    name: str
    def __init__(self, type: _Optional[_Union[StreamSourceType, str]] = ..., name: _Optional[str] = ...) -> None: ...

class StreamSource(_message.Message):
    __slots__ = ("kafka", "kinesis", "pubsub")
    KAFKA_FIELD_NUMBER: _ClassVar[int]
    KINESIS_FIELD_NUMBER: _ClassVar[int]
    PUBSUB_FIELD_NUMBER: _ClassVar[int]
    kafka: KafkaSource
    kinesis: KinesisSource
    pubsub: PubSubSource
    def __init__(
        self,
        kafka: _Optional[_Union[KafkaSource, _Mapping]] = ...,
        kinesis: _Optional[_Union[KinesisSource, _Mapping]] = ...,
        pubsub: _Optional[_Union[PubSubSource, _Mapping]] = ...,
    ) -> None: ...

class KinesisSource(_message.Message):
    __slots__ = (
        "name",
        "stream_name",
        "stream_arn",
        "region_name",
        "late_arrival_deadline",
        "dead_letter_queue_stream_name",
        "aws_access_key_id",
        "aws_secret_access_key",
        "aws_session_token",
        "endpoint_url",
        "consumer_role_arn",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    STREAM_ARN_FIELD_NUMBER: _ClassVar[int]
    REGION_NAME_FIELD_NUMBER: _ClassVar[int]
    LATE_ARRIVAL_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    DEAD_LETTER_QUEUE_STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    AWS_SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    name: str
    stream_name: str
    stream_arn: str
    region_name: str
    late_arrival_deadline: _duration_pb2.Duration
    dead_letter_queue_stream_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    endpoint_url: str
    consumer_role_arn: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        stream_name: _Optional[str] = ...,
        stream_arn: _Optional[str] = ...,
        region_name: _Optional[str] = ...,
        late_arrival_deadline: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        dead_letter_queue_stream_name: _Optional[str] = ...,
        aws_access_key_id: _Optional[str] = ...,
        aws_secret_access_key: _Optional[str] = ...,
        aws_session_token: _Optional[str] = ...,
        endpoint_url: _Optional[str] = ...,
        consumer_role_arn: _Optional[str] = ...,
    ) -> None: ...

class KafkaSource(_message.Message):
    __slots__ = (
        "name",
        "bootstrap_servers",
        "topic",
        "ssl_keystore_location",
        "ssl_ca_file",
        "client_id_prefix",
        "group_id_prefix",
        "security_protocol",
        "sasl_mechanism",
        "sasl_username",
        "sasl_password",
        "late_arrival_deadline",
        "dead_letter_queue_topic",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAP_SERVERS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SSL_CA_FILE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_PREFIX_FIELD_NUMBER: _ClassVar[int]
    SECURITY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SASL_MECHANISM_FIELD_NUMBER: _ClassVar[int]
    SASL_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SASL_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    LATE_ARRIVAL_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    DEAD_LETTER_QUEUE_TOPIC_FIELD_NUMBER: _ClassVar[int]
    name: str
    bootstrap_servers: _containers.RepeatedScalarFieldContainer[str]
    topic: str
    ssl_keystore_location: str
    ssl_ca_file: str
    client_id_prefix: str
    group_id_prefix: str
    security_protocol: str
    sasl_mechanism: str
    sasl_username: str
    sasl_password: str
    late_arrival_deadline: _duration_pb2.Duration
    dead_letter_queue_topic: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        bootstrap_servers: _Optional[_Iterable[str]] = ...,
        topic: _Optional[str] = ...,
        ssl_keystore_location: _Optional[str] = ...,
        ssl_ca_file: _Optional[str] = ...,
        client_id_prefix: _Optional[str] = ...,
        group_id_prefix: _Optional[str] = ...,
        security_protocol: _Optional[str] = ...,
        sasl_mechanism: _Optional[str] = ...,
        sasl_username: _Optional[str] = ...,
        sasl_password: _Optional[str] = ...,
        late_arrival_deadline: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        dead_letter_queue_topic: _Optional[str] = ...,
    ) -> None: ...

class PubSubSource(_message.Message):
    __slots__ = ("name", "project_id", "subscription_id", "late_arrival_deadline", "dead_letter_queue_topic")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    LATE_ARRIVAL_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    DEAD_LETTER_QUEUE_TOPIC_FIELD_NUMBER: _ClassVar[int]
    name: str
    project_id: str
    subscription_id: str
    late_arrival_deadline: _duration_pb2.Duration
    dead_letter_queue_topic: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        project_id: _Optional[str] = ...,
        subscription_id: _Optional[str] = ...,
        late_arrival_deadline: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        dead_letter_queue_topic: _Optional[str] = ...,
    ) -> None: ...

class DatabaseSourceReference(_message.Message):
    __slots__ = ("type", "name")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    type: DatabaseSourceType
    name: str
    def __init__(self, type: _Optional[_Union[DatabaseSourceType, str]] = ..., name: _Optional[str] = ...) -> None: ...

class DatabaseSource(_message.Message):
    __slots__ = (
        "bigquery",
        "cloudsql",
        "databricks",
        "mysql",
        "postgres",
        "redshift",
        "snowflake",
        "sqlite",
        "spanner",
        "trino",
        "dynamodb",
        "athena",
    )
    BIGQUERY_FIELD_NUMBER: _ClassVar[int]
    CLOUDSQL_FIELD_NUMBER: _ClassVar[int]
    DATABRICKS_FIELD_NUMBER: _ClassVar[int]
    MYSQL_FIELD_NUMBER: _ClassVar[int]
    POSTGRES_FIELD_NUMBER: _ClassVar[int]
    REDSHIFT_FIELD_NUMBER: _ClassVar[int]
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    SQLITE_FIELD_NUMBER: _ClassVar[int]
    SPANNER_FIELD_NUMBER: _ClassVar[int]
    TRINO_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_FIELD_NUMBER: _ClassVar[int]
    ATHENA_FIELD_NUMBER: _ClassVar[int]
    bigquery: BigQuerySource
    cloudsql: CloudSQLSource
    databricks: DatabricksSource
    mysql: MySQLSource
    postgres: PostgresSource
    redshift: RedshiftSource
    snowflake: SnowflakeSource
    sqlite: SQLiteSource
    spanner: SpannerSource
    trino: TrinoSource
    dynamodb: DynamoDBSource
    athena: AthenaSource
    def __init__(
        self,
        bigquery: _Optional[_Union[BigQuerySource, _Mapping]] = ...,
        cloudsql: _Optional[_Union[CloudSQLSource, _Mapping]] = ...,
        databricks: _Optional[_Union[DatabricksSource, _Mapping]] = ...,
        mysql: _Optional[_Union[MySQLSource, _Mapping]] = ...,
        postgres: _Optional[_Union[PostgresSource, _Mapping]] = ...,
        redshift: _Optional[_Union[RedshiftSource, _Mapping]] = ...,
        snowflake: _Optional[_Union[SnowflakeSource, _Mapping]] = ...,
        sqlite: _Optional[_Union[SQLiteSource, _Mapping]] = ...,
        spanner: _Optional[_Union[SpannerSource, _Mapping]] = ...,
        trino: _Optional[_Union[TrinoSource, _Mapping]] = ...,
        dynamodb: _Optional[_Union[DynamoDBSource, _Mapping]] = ...,
        athena: _Optional[_Union[AthenaSource, _Mapping]] = ...,
    ) -> None: ...

class BigQuerySource(_message.Message):
    __slots__ = (
        "name",
        "project",
        "dataset",
        "location",
        "credentials_base64",
        "credentials_path",
        "engine_args",
        "async_engine_args",
    )
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_BASE64_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_PATH_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    project: str
    dataset: str
    location: str
    credentials_base64: str
    credentials_path: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        project: _Optional[str] = ...,
        dataset: _Optional[str] = ...,
        location: _Optional[str] = ...,
        credentials_base64: _Optional[str] = ...,
        credentials_path: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class CloudSQLSource(_message.Message):
    __slots__ = ("name", "db", "user", "password", "instance_name", "engine_args", "async_engine_args")
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    db: str
    user: str
    password: str
    instance_name: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        db: _Optional[str] = ...,
        user: _Optional[str] = ...,
        password: _Optional[str] = ...,
        instance_name: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class DatabricksSource(_message.Message):
    __slots__ = ("name", "host", "port", "db", "http_path", "access_token", "engine_args", "async_engine_args")
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    HTTP_PATH_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    host: str
    port: str
    db: str
    http_path: str
    access_token: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        host: _Optional[str] = ...,
        port: _Optional[str] = ...,
        db: _Optional[str] = ...,
        http_path: _Optional[str] = ...,
        access_token: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class DynamoDBSource(_message.Message):
    __slots__ = (
        "name",
        "aws_client_id_override",
        "aws_client_secret_override",
        "aws_region_override",
        "endpoint_override",
        "engine_args",
        "async_engine_args",
    )
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_CLIENT_ID_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    AWS_CLIENT_SECRET_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    AWS_REGION_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    aws_client_id_override: str
    aws_client_secret_override: str
    aws_region_override: str
    endpoint_override: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        aws_client_id_override: _Optional[str] = ...,
        aws_client_secret_override: _Optional[str] = ...,
        aws_region_override: _Optional[str] = ...,
        endpoint_override: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class MySQLSource(_message.Message):
    __slots__ = ("name", "host", "port", "db", "user", "password", "engine_args", "async_engine_args")
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    host: str
    port: str
    db: str
    user: str
    password: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        host: _Optional[str] = ...,
        port: _Optional[str] = ...,
        db: _Optional[str] = ...,
        user: _Optional[str] = ...,
        password: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class PostgresSource(_message.Message):
    __slots__ = ("name", "host", "port", "db", "user", "password", "engine_args", "async_engine_args")
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    host: str
    port: str
    db: str
    user: str
    password: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        host: _Optional[str] = ...,
        port: _Optional[str] = ...,
        db: _Optional[str] = ...,
        user: _Optional[str] = ...,
        password: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class RedshiftSource(_message.Message):
    __slots__ = (
        "name",
        "host",
        "port",
        "db",
        "user",
        "password",
        "s3_client",
        "s3_bucket",
        "engine_args",
        "async_engine_args",
        "unload_iam_role",
    )
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    S3_CLIENT_FIELD_NUMBER: _ClassVar[int]
    S3_BUCKET_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    UNLOAD_IAM_ROLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    host: str
    port: str
    db: str
    user: str
    password: str
    s3_client: str
    s3_bucket: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    unload_iam_role: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        host: _Optional[str] = ...,
        port: _Optional[str] = ...,
        db: _Optional[str] = ...,
        user: _Optional[str] = ...,
        password: _Optional[str] = ...,
        s3_client: _Optional[str] = ...,
        s3_bucket: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        unload_iam_role: _Optional[str] = ...,
    ) -> None: ...

class SnowflakeSource(_message.Message):
    __slots__ = (
        "name",
        "db",
        "schema",
        "role",
        "user",
        "password",
        "account_identifier",
        "warehouse",
        "engine_args",
        "async_engine_args",
        "private_key_b64",
    )
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_B64_FIELD_NUMBER: _ClassVar[int]
    name: str
    db: str
    schema: str
    role: str
    user: str
    password: str
    account_identifier: str
    warehouse: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    private_key_b64: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        db: _Optional[str] = ...,
        schema: _Optional[str] = ...,
        role: _Optional[str] = ...,
        user: _Optional[str] = ...,
        password: _Optional[str] = ...,
        account_identifier: _Optional[str] = ...,
        warehouse: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        private_key_b64: _Optional[str] = ...,
    ) -> None: ...

class SQLiteSource(_message.Message):
    __slots__ = ("name", "file_name", "engine_args", "async_engine_args")
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    file_name: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        file_name: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class SpannerSource(_message.Message):
    __slots__ = ("name", "project", "instance", "db", "credentials_base64", "engine_args", "async_engine_args")
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_BASE64_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    project: str
    instance: str
    db: str
    credentials_base64: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        project: _Optional[str] = ...,
        instance: _Optional[str] = ...,
        db: _Optional[str] = ...,
        credentials_base64: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class TrinoSource(_message.Message):
    __slots__ = ("name", "host", "port", "catalog", "schema", "user", "password", "engine_args", "async_engine_args")
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    host: str
    port: str
    catalog: str
    schema: str
    user: str
    password: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    def __init__(
        self,
        name: _Optional[str] = ...,
        host: _Optional[str] = ...,
        port: _Optional[str] = ...,
        catalog: _Optional[str] = ...,
        schema: _Optional[str] = ...,
        user: _Optional[str] = ...,
        password: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
    ) -> None: ...

class AthenaSource(_message.Message):
    __slots__ = (
        "name",
        "aws_region",
        "aws_access_key_id",
        "aws_access_key_secret",
        "s3_staging_dir",
        "catalog_name",
        "schema_name",
        "role_arn",
        "engine_args",
        "async_engine_args",
        "work_group",
    )
    class EngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    class AsyncEngineArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_REGION_FIELD_NUMBER: _ClassVar[int]
    AWS_ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_ACCESS_KEY_SECRET_FIELD_NUMBER: _ClassVar[int]
    S3_STAGING_DIR_FIELD_NUMBER: _ClassVar[int]
    CATALOG_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_ENGINE_ARGS_FIELD_NUMBER: _ClassVar[int]
    WORK_GROUP_FIELD_NUMBER: _ClassVar[int]
    name: str
    aws_region: str
    aws_access_key_id: str
    aws_access_key_secret: str
    s3_staging_dir: str
    catalog_name: str
    schema_name: str
    role_arn: str
    engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    async_engine_args: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    work_group: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        aws_region: _Optional[str] = ...,
        aws_access_key_id: _Optional[str] = ...,
        aws_access_key_secret: _Optional[str] = ...,
        s3_staging_dir: _Optional[str] = ...,
        catalog_name: _Optional[str] = ...,
        schema_name: _Optional[str] = ...,
        role_arn: _Optional[str] = ...,
        engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        async_engine_args: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        work_group: _Optional[str] = ...,
    ) -> None: ...
