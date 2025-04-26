from google.protobuf import duration_pb2 as _duration_pb2
from tecton_proto.args import data_source_config__client_pb2 as _data_source_config__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
UNITY_CATALOG_ACCESS_MODE_SHARED: UnityCatalogAccessMode
UNITY_CATALOG_ACCESS_MODE_SINGLE_USER: UnityCatalogAccessMode
UNITY_CATALOG_ACCESS_MODE_SINGLE_USER_WITH_FGAC: UnityCatalogAccessMode
UNITY_CATALOG_ACCESS_MODE_UNSPECIFIED: UnityCatalogAccessMode

class BatchDataSourceCommonArgs(_message.Message):
    __slots__ = ["data_delay", "post_processor", "timestamp_field"]
    DATA_DELAY_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: _ClassVar[int]
    data_delay: _duration_pb2.Duration
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    timestamp_field: str
    def __init__(self, timestamp_field: _Optional[str] = ..., post_processor: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., data_delay: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class BigqueryDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "credentials", "dataset", "location", "project_id", "query", "table"]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    credentials: _secret__client_pb2.SecretReference
    dataset: str
    location: str
    project_id: str
    query: str
    table: str
    def __init__(self, project_id: _Optional[str] = ..., dataset: _Optional[str] = ..., location: _Optional[str] = ..., table: _Optional[str] = ..., query: _Optional[str] = ..., common_args: _Optional[_Union[BatchDataSourceCommonArgs, _Mapping]] = ..., credentials: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...

class DatetimePartitionColumnArgs(_message.Message):
    __slots__ = ["column_name", "datepart", "format_string", "zero_padded"]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    DATEPART_FIELD_NUMBER: _ClassVar[int]
    FORMAT_STRING_FIELD_NUMBER: _ClassVar[int]
    ZERO_PADDED_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    datepart: str
    format_string: str
    zero_padded: bool
    def __init__(self, column_name: _Optional[str] = ..., datepart: _Optional[str] = ..., zero_padded: bool = ..., format_string: _Optional[str] = ...) -> None: ...

class FileDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "convert_to_glue_format", "datetime_partition_columns", "file_format", "schema_override", "schema_uri", "timestamp_format", "uri"]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    CONVERT_TO_GLUE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    FILE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_URI_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FORMAT_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    convert_to_glue_format: bool
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumnArgs]
    file_format: str
    schema_override: _spark_schema__client_pb2.SparkSchema
    schema_uri: str
    timestamp_format: str
    uri: str
    def __init__(self, uri: _Optional[str] = ..., file_format: _Optional[str] = ..., convert_to_glue_format: bool = ..., schema_uri: _Optional[str] = ..., timestamp_format: _Optional[str] = ..., schema_override: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., common_args: _Optional[_Union[BatchDataSourceCommonArgs, _Mapping]] = ..., datetime_partition_columns: _Optional[_Iterable[_Union[DatetimePartitionColumnArgs, _Mapping]]] = ...) -> None: ...

class HiveDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "database", "datetime_partition_columns", "table", "timestamp_format"]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FORMAT_FIELD_NUMBER: _ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    database: str
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumnArgs]
    table: str
    timestamp_format: str
    def __init__(self, table: _Optional[str] = ..., database: _Optional[str] = ..., timestamp_format: _Optional[str] = ..., datetime_partition_columns: _Optional[_Iterable[_Union[DatetimePartitionColumnArgs, _Mapping]]] = ..., common_args: _Optional[_Union[BatchDataSourceCommonArgs, _Mapping]] = ...) -> None: ...

class KafkaDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "kafka_bootstrap_servers", "options", "security_protocol", "ssl_keystore_location", "ssl_keystore_password_secret_id", "ssl_truststore_location", "ssl_truststore_password_secret_id", "topics"]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    KAFKA_BOOTSTRAP_SERVERS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SSL_TRUSTSTORE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SSL_TRUSTSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    common_args: StreamDataSourceCommonArgs
    kafka_bootstrap_servers: str
    options: _containers.RepeatedCompositeFieldContainer[Option]
    security_protocol: str
    ssl_keystore_location: str
    ssl_keystore_password_secret_id: str
    ssl_truststore_location: str
    ssl_truststore_password_secret_id: str
    topics: str
    def __init__(self, kafka_bootstrap_servers: _Optional[str] = ..., topics: _Optional[str] = ..., options: _Optional[_Iterable[_Union[Option, _Mapping]]] = ..., ssl_keystore_location: _Optional[str] = ..., ssl_keystore_password_secret_id: _Optional[str] = ..., ssl_truststore_location: _Optional[str] = ..., ssl_truststore_password_secret_id: _Optional[str] = ..., security_protocol: _Optional[str] = ..., common_args: _Optional[_Union[StreamDataSourceCommonArgs, _Mapping]] = ...) -> None: ...

class KinesisDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "initial_stream_position", "options", "region", "stream_name"]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STREAM_POSITION_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    common_args: StreamDataSourceCommonArgs
    initial_stream_position: _data_source_config__client_pb2.InitialStreamPosition
    options: _containers.RepeatedCompositeFieldContainer[Option]
    region: str
    stream_name: str
    def __init__(self, stream_name: _Optional[str] = ..., region: _Optional[str] = ..., initial_stream_position: _Optional[_Union[_data_source_config__client_pb2.InitialStreamPosition, str]] = ..., options: _Optional[_Iterable[_Union[Option, _Mapping]]] = ..., common_args: _Optional[_Union[StreamDataSourceCommonArgs, _Mapping]] = ...) -> None: ...

class Option(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class PandasBatchConfigArgs(_message.Message):
    __slots__ = ["data_delay", "data_source_function", "secrets", "supports_time_filtering"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    DATA_DELAY_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: _ClassVar[int]
    data_delay: _duration_pb2.Duration
    data_source_function: _user_defined_function__client_pb2.UserDefinedFunction
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    supports_time_filtering: bool
    def __init__(self, data_source_function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., data_delay: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., supports_time_filtering: bool = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ...) -> None: ...

class PushSourceArgs(_message.Message):
    __slots__ = ["input_schema", "log_offline", "post_processor", "post_processor_mode", "timestamp_field"]
    INPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    LOG_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSOR_MODE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: _ClassVar[int]
    input_schema: _schema__client_pb2.Schema
    log_offline: bool
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    post_processor_mode: _transformation__client_pb2.TransformationMode
    timestamp_field: str
    def __init__(self, log_offline: bool = ..., post_processor: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., input_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., post_processor_mode: _Optional[_Union[_transformation__client_pb2.TransformationMode, str]] = ..., timestamp_field: _Optional[str] = ...) -> None: ...

class PyArrowBatchConfigArgs(_message.Message):
    __slots__ = ["data_delay", "data_source_function", "secrets", "supports_time_filtering"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    DATA_DELAY_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: _ClassVar[int]
    data_delay: _duration_pb2.Duration
    data_source_function: _user_defined_function__client_pb2.UserDefinedFunction
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    supports_time_filtering: bool
    def __init__(self, data_source_function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., data_delay: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., supports_time_filtering: bool = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ...) -> None: ...

class RedshiftDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "endpoint", "query", "table"]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    endpoint: str
    query: str
    table: str
    def __init__(self, endpoint: _Optional[str] = ..., table: _Optional[str] = ..., query: _Optional[str] = ..., common_args: _Optional[_Union[BatchDataSourceCommonArgs, _Mapping]] = ...) -> None: ...

class SnowflakeDataSourceArgs(_message.Message):
    __slots__ = ["common_args", "database", "password", "query", "role", "schema", "table", "url", "user", "warehouse"]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    common_args: BatchDataSourceCommonArgs
    database: str
    password: _secret__client_pb2.SecretReference
    query: str
    role: str
    schema: str
    table: str
    url: str
    user: _secret__client_pb2.SecretReference
    warehouse: str
    def __init__(self, url: _Optional[str] = ..., role: _Optional[str] = ..., database: _Optional[str] = ..., schema: _Optional[str] = ..., warehouse: _Optional[str] = ..., table: _Optional[str] = ..., query: _Optional[str] = ..., common_args: _Optional[_Union[BatchDataSourceCommonArgs, _Mapping]] = ..., user: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ..., password: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...

class SparkBatchConfigArgs(_message.Message):
    __slots__ = ["data_delay", "data_source_function", "supports_time_filtering"]
    DATA_DELAY_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: _ClassVar[int]
    data_delay: _duration_pb2.Duration
    data_source_function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, data_source_function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., data_delay: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class SparkStreamConfigArgs(_message.Message):
    __slots__ = ["data_source_function"]
    DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    data_source_function: _user_defined_function__client_pb2.UserDefinedFunction
    def __init__(self, data_source_function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...

class StreamDataSourceCommonArgs(_message.Message):
    __slots__ = ["deduplication_columns", "post_processor", "timestamp_field", "watermark_delay_threshold"]
    DEDUPLICATION_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_DELAY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    deduplication_columns: _containers.RepeatedScalarFieldContainer[str]
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    timestamp_field: str
    watermark_delay_threshold: _duration_pb2.Duration
    def __init__(self, timestamp_field: _Optional[str] = ..., watermark_delay_threshold: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., post_processor: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., deduplication_columns: _Optional[_Iterable[str]] = ...) -> None: ...

class UnityDataSourceArgs(_message.Message):
    __slots__ = ["access_mode", "catalog", "common_args", "datetime_partition_columns", "schema", "table", "timestamp_format"]
    ACCESS_MODE_FIELD_NUMBER: _ClassVar[int]
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    COMMON_ARGS_FIELD_NUMBER: _ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FORMAT_FIELD_NUMBER: _ClassVar[int]
    access_mode: UnityCatalogAccessMode
    catalog: str
    common_args: BatchDataSourceCommonArgs
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumnArgs]
    schema: str
    table: str
    timestamp_format: str
    def __init__(self, catalog: _Optional[str] = ..., schema: _Optional[str] = ..., table: _Optional[str] = ..., common_args: _Optional[_Union[BatchDataSourceCommonArgs, _Mapping]] = ..., timestamp_format: _Optional[str] = ..., datetime_partition_columns: _Optional[_Iterable[_Union[DatetimePartitionColumnArgs, _Mapping]]] = ..., access_mode: _Optional[_Union[UnityCatalogAccessMode, str]] = ...) -> None: ...

class UnityCatalogAccessMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
