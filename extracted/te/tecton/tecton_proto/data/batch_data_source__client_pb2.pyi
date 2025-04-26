from google.protobuf import duration_pb2 as _duration_pb2
from tecton_proto.args import data_source__client_pb2 as _data_source__client_pb2
from tecton_proto.args import data_source_config__client_pb2 as _data_source_config__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.data import hive_metastore__client_pb2 as _hive_metastore__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
FILE_DATA_SOURCE_FORMAT_CSV: FileDataSourceFormat
FILE_DATA_SOURCE_FORMAT_JSON: FileDataSourceFormat
FILE_DATA_SOURCE_FORMAT_PARQUET: FileDataSourceFormat

class BatchDataSource(_message.Message):
    __slots__ = ["batch_config", "bigquery", "data_delay", "date_partition_column", "datetime_partition_columns", "file", "hive_table", "pandas_data_source_function", "push_source_table", "pyarrow_data_source_function", "raw_batch_translator", "redshift_db", "secrets", "snowflake", "spark_data_source_function", "spark_schema", "timestamp_column_properties", "unity_table"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    BATCH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_FIELD_NUMBER: _ClassVar[int]
    DATA_DELAY_FIELD_NUMBER: _ClassVar[int]
    DATETIME_PARTITION_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    DATE_PARTITION_COLUMN_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    HIVE_TABLE_FIELD_NUMBER: _ClassVar[int]
    PANDAS_DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    PUSH_SOURCE_TABLE_FIELD_NUMBER: _ClassVar[int]
    PYARROW_DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    RAW_BATCH_TRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    REDSHIFT_DB_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    SPARK_DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SPARK_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    UNITY_TABLE_FIELD_NUMBER: _ClassVar[int]
    batch_config: _data_source_config__client_pb2.BatchConfig
    bigquery: BigqueryDataSource
    data_delay: _duration_pb2.Duration
    date_partition_column: str
    datetime_partition_columns: _containers.RepeatedCompositeFieldContainer[DatetimePartitionColumn]
    file: FileDataSource
    hive_table: _hive_metastore__client_pb2.HiveTableDataSource
    pandas_data_source_function: PandasBatchDataSourceFunction
    push_source_table: PushDataSource
    pyarrow_data_source_function: PyArrowBatchDataSourceFunction
    raw_batch_translator: _user_defined_function__client_pb2.UserDefinedFunction
    redshift_db: RedshiftDataSource
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    snowflake: SnowflakeDataSource
    spark_data_source_function: SparkBatchDataSourceFunction
    spark_schema: _spark_schema__client_pb2.SparkSchema
    timestamp_column_properties: TimestampColumnProperties
    unity_table: UnityTableDataSource
    def __init__(self, hive_table: _Optional[_Union[_hive_metastore__client_pb2.HiveTableDataSource, _Mapping]] = ..., file: _Optional[_Union[FileDataSource, _Mapping]] = ..., redshift_db: _Optional[_Union[RedshiftDataSource, _Mapping]] = ..., snowflake: _Optional[_Union[SnowflakeDataSource, _Mapping]] = ..., spark_data_source_function: _Optional[_Union[SparkBatchDataSourceFunction, _Mapping]] = ..., unity_table: _Optional[_Union[UnityTableDataSource, _Mapping]] = ..., push_source_table: _Optional[_Union[PushDataSource, _Mapping]] = ..., pandas_data_source_function: _Optional[_Union[PandasBatchDataSourceFunction, _Mapping]] = ..., bigquery: _Optional[_Union[BigqueryDataSource, _Mapping]] = ..., pyarrow_data_source_function: _Optional[_Union[PyArrowBatchDataSourceFunction, _Mapping]] = ..., spark_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., timestamp_column_properties: _Optional[_Union[TimestampColumnProperties, _Mapping]] = ..., batch_config: _Optional[_Union[_data_source_config__client_pb2.BatchConfig, _Mapping]] = ..., date_partition_column: _Optional[str] = ..., datetime_partition_columns: _Optional[_Iterable[_Union[DatetimePartitionColumn, _Mapping]]] = ..., raw_batch_translator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., data_delay: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ...) -> None: ...

class BigqueryDataSource(_message.Message):
    __slots__ = ["credentials", "dataset", "location", "project_id", "query", "table"]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    credentials: _secret__client_pb2.SecretReference
    dataset: str
    location: str
    project_id: str
    query: str
    table: str
    def __init__(self, project_id: _Optional[str] = ..., dataset: _Optional[str] = ..., location: _Optional[str] = ..., table: _Optional[str] = ..., query: _Optional[str] = ..., credentials: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...

class DatetimePartitionColumn(_message.Message):
    __slots__ = ["column_name", "format_string", "minimum_seconds"]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    FORMAT_STRING_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_SECONDS_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    format_string: str
    minimum_seconds: int
    def __init__(self, column_name: _Optional[str] = ..., format_string: _Optional[str] = ..., minimum_seconds: _Optional[int] = ...) -> None: ...

class FileDataSource(_message.Message):
    __slots__ = ["convert_to_glue_format", "format", "schema_override", "schema_uri", "uri"]
    CONVERT_TO_GLUE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_URI_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    convert_to_glue_format: bool
    format: FileDataSourceFormat
    schema_override: _spark_schema__client_pb2.SparkSchema
    schema_uri: str
    uri: str
    def __init__(self, uri: _Optional[str] = ..., format: _Optional[_Union[FileDataSourceFormat, str]] = ..., convert_to_glue_format: bool = ..., schema_uri: _Optional[str] = ..., schema_override: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ...) -> None: ...

class PandasBatchDataSourceFunction(_message.Message):
    __slots__ = ["function", "supports_time_filtering"]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class PushDataSource(_message.Message):
    __slots__ = ["ingested_data_location"]
    INGESTED_DATA_LOCATION_FIELD_NUMBER: _ClassVar[int]
    ingested_data_location: str
    def __init__(self, ingested_data_location: _Optional[str] = ...) -> None: ...

class PyArrowBatchDataSourceFunction(_message.Message):
    __slots__ = ["function", "supports_time_filtering"]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class RedshiftDataSource(_message.Message):
    __slots__ = ["cluster_id", "database", "endpoint", "query", "table", "temp_s3"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    TEMP_S3_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    database: str
    endpoint: str
    query: str
    table: str
    temp_s3: str
    def __init__(self, endpoint: _Optional[str] = ..., cluster_id: _Optional[str] = ..., database: _Optional[str] = ..., table: _Optional[str] = ..., query: _Optional[str] = ..., temp_s3: _Optional[str] = ...) -> None: ...

class SnowflakeDataSource(_message.Message):
    __slots__ = ["snowflakeArgs"]
    SNOWFLAKEARGS_FIELD_NUMBER: _ClassVar[int]
    snowflakeArgs: _data_source__client_pb2.SnowflakeDataSourceArgs
    def __init__(self, snowflakeArgs: _Optional[_Union[_data_source__client_pb2.SnowflakeDataSourceArgs, _Mapping]] = ...) -> None: ...

class SparkBatchDataSourceFunction(_message.Message):
    __slots__ = ["function", "supports_time_filtering"]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TIME_FILTERING_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    supports_time_filtering: bool
    def __init__(self, function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., supports_time_filtering: bool = ...) -> None: ...

class TimestampColumnProperties(_message.Message):
    __slots__ = ["column_name", "format"]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    format: str
    def __init__(self, column_name: _Optional[str] = ..., format: _Optional[str] = ...) -> None: ...

class UnityTableDataSource(_message.Message):
    __slots__ = ["access_mode", "catalog", "schema", "table"]
    ACCESS_MODE_FIELD_NUMBER: _ClassVar[int]
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    access_mode: _data_source__client_pb2.UnityCatalogAccessMode
    catalog: str
    schema: str
    table: str
    def __init__(self, catalog: _Optional[str] = ..., schema: _Optional[str] = ..., table: _Optional[str] = ..., access_mode: _Optional[_Union[_data_source__client_pb2.UnityCatalogAccessMode, str]] = ...) -> None: ...

class FileDataSourceFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
