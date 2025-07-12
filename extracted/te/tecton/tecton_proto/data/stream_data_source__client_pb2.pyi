from tecton_proto.args import data_source_config__client_pb2 as _data_source_config__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KafkaDSConfig(_message.Message):
    __slots__ = ["bootstrap_servers", "security_protocol", "ssl_keystore_location", "ssl_keystore_password_secret_id", "ssl_truststore_location", "ssl_truststore_password_secret_id", "topics"]
    BOOTSTRAP_SERVERS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SSL_TRUSTSTORE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SSL_TRUSTSTORE_PASSWORD_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    bootstrap_servers: str
    security_protocol: str
    ssl_keystore_location: str
    ssl_keystore_password_secret_id: str
    ssl_truststore_location: str
    ssl_truststore_password_secret_id: str
    topics: str
    def __init__(self, bootstrap_servers: _Optional[str] = ..., topics: _Optional[str] = ..., ssl_keystore_location: _Optional[str] = ..., ssl_keystore_password_secret_id: _Optional[str] = ..., ssl_truststore_location: _Optional[str] = ..., ssl_truststore_password_secret_id: _Optional[str] = ..., security_protocol: _Optional[str] = ...) -> None: ...

class KinesisDSConfig(_message.Message):
    __slots__ = ["region", "stream_name"]
    REGION_FIELD_NUMBER: _ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    region: str
    stream_name: str
    def __init__(self, stream_name: _Optional[str] = ..., region: _Optional[str] = ...) -> None: ...

class PushDataSourceConfig(_message.Message):
    __slots__ = ["ingest_server_group_id", "input_schema", "log_offline", "post_processor", "post_processor_mode"]
    INGEST_SERVER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    LOG_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESSOR_MODE_FIELD_NUMBER: _ClassVar[int]
    ingest_server_group_id: _id__client_pb2.Id
    input_schema: _schema__client_pb2.Schema
    log_offline: bool
    post_processor: _user_defined_function__client_pb2.UserDefinedFunction
    post_processor_mode: _transformation__client_pb2.TransformationMode
    def __init__(self, log_offline: bool = ..., post_processor: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., input_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., post_processor_mode: _Optional[_Union[_transformation__client_pb2.TransformationMode, str]] = ..., ingest_server_group_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...

class SparkStreamDataSourceFunction(_message.Message):
    __slots__ = ["function"]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    def __init__(self, function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...

class StreamDataSource(_message.Message):
    __slots__ = ["deduplication_column_names", "kafka_data_source", "kinesis_data_source", "options", "push_source", "raw_stream_translator", "spark_data_source_function", "spark_schema", "stream_config", "time_column"]
    class Option(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DEDUPLICATION_COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    KAFKA_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    KINESIS_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PUSH_SOURCE_FIELD_NUMBER: _ClassVar[int]
    RAW_STREAM_TRANSLATOR_FIELD_NUMBER: _ClassVar[int]
    SPARK_DATA_SOURCE_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    SPARK_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    STREAM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TIME_COLUMN_FIELD_NUMBER: _ClassVar[int]
    deduplication_column_names: _containers.RepeatedScalarFieldContainer[str]
    kafka_data_source: KafkaDSConfig
    kinesis_data_source: KinesisDSConfig
    options: _containers.RepeatedCompositeFieldContainer[StreamDataSource.Option]
    push_source: PushDataSourceConfig
    raw_stream_translator: _user_defined_function__client_pb2.UserDefinedFunction
    spark_data_source_function: SparkStreamDataSourceFunction
    spark_schema: _spark_schema__client_pb2.SparkSchema
    stream_config: _data_source_config__client_pb2.StreamConfig
    time_column: str
    def __init__(self, kinesis_data_source: _Optional[_Union[KinesisDSConfig, _Mapping]] = ..., kafka_data_source: _Optional[_Union[KafkaDSConfig, _Mapping]] = ..., spark_data_source_function: _Optional[_Union[SparkStreamDataSourceFunction, _Mapping]] = ..., push_source: _Optional[_Union[PushDataSourceConfig, _Mapping]] = ..., spark_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., raw_stream_translator: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., deduplication_column_names: _Optional[_Iterable[str]] = ..., time_column: _Optional[str] = ..., stream_config: _Optional[_Union[_data_source_config__client_pb2.StreamConfig, _Mapping]] = ..., options: _Optional[_Iterable[_Union[StreamDataSource.Option, _Mapping]]] = ...) -> None: ...
