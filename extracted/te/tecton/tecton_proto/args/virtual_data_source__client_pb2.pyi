from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import data_source__client_pb2 as _data_source__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.common import data_source_type__client_pb2 as _data_source_type__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema_container__client_pb2 as _schema_container__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VirtualDataSourceArgs(_message.Message):
    __slots__ = ["bigquery_ds_config", "file_ds_config", "forced_batch_schema", "forced_stream_schema", "hive_ds_config", "info", "kafka_ds_config", "kinesis_ds_config", "options", "pandas_batch_config", "prevent_destroy", "push_config", "pyarrow_batch_config", "redshift_ds_config", "schema", "snowflake_ds_config", "spark_batch_config", "spark_stream_config", "type", "unity_ds_config", "version", "virtual_data_source_id"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BIGQUERY_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FILE_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FORCED_BATCH_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    FORCED_STREAM_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    HIVE_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    KAFKA_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    KINESIS_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PANDAS_BATCH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: _ClassVar[int]
    PUSH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PYARROW_BATCH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REDSHIFT_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SNOWFLAKE_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SPARK_BATCH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SPARK_STREAM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNITY_DS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    bigquery_ds_config: _data_source__client_pb2.BigqueryDataSourceArgs
    file_ds_config: _data_source__client_pb2.FileDataSourceArgs
    forced_batch_schema: _spark_schema__client_pb2.SparkSchema
    forced_stream_schema: _spark_schema__client_pb2.SparkSchema
    hive_ds_config: _data_source__client_pb2.HiveDataSourceArgs
    info: _basic_info__client_pb2.BasicInfo
    kafka_ds_config: _data_source__client_pb2.KafkaDataSourceArgs
    kinesis_ds_config: _data_source__client_pb2.KinesisDataSourceArgs
    options: _containers.ScalarMap[str, str]
    pandas_batch_config: _data_source__client_pb2.PandasBatchConfigArgs
    prevent_destroy: bool
    push_config: _data_source__client_pb2.PushSourceArgs
    pyarrow_batch_config: _data_source__client_pb2.PyArrowBatchConfigArgs
    redshift_ds_config: _data_source__client_pb2.RedshiftDataSourceArgs
    schema: _schema_container__client_pb2.SchemaContainer
    snowflake_ds_config: _data_source__client_pb2.SnowflakeDataSourceArgs
    spark_batch_config: _data_source__client_pb2.SparkBatchConfigArgs
    spark_stream_config: _data_source__client_pb2.SparkStreamConfigArgs
    type: _data_source_type__client_pb2.DataSourceType
    unity_ds_config: _data_source__client_pb2.UnityDataSourceArgs
    version: _framework_version__client_pb2.FrameworkVersion
    virtual_data_source_id: _id__client_pb2.Id
    def __init__(self, virtual_data_source_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., info: _Optional[_Union[_basic_info__client_pb2.BasicInfo, _Mapping]] = ..., version: _Optional[_Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., prevent_destroy: bool = ..., options: _Optional[_Mapping[str, str]] = ..., hive_ds_config: _Optional[_Union[_data_source__client_pb2.HiveDataSourceArgs, _Mapping]] = ..., file_ds_config: _Optional[_Union[_data_source__client_pb2.FileDataSourceArgs, _Mapping]] = ..., redshift_ds_config: _Optional[_Union[_data_source__client_pb2.RedshiftDataSourceArgs, _Mapping]] = ..., snowflake_ds_config: _Optional[_Union[_data_source__client_pb2.SnowflakeDataSourceArgs, _Mapping]] = ..., spark_batch_config: _Optional[_Union[_data_source__client_pb2.SparkBatchConfigArgs, _Mapping]] = ..., unity_ds_config: _Optional[_Union[_data_source__client_pb2.UnityDataSourceArgs, _Mapping]] = ..., pandas_batch_config: _Optional[_Union[_data_source__client_pb2.PandasBatchConfigArgs, _Mapping]] = ..., bigquery_ds_config: _Optional[_Union[_data_source__client_pb2.BigqueryDataSourceArgs, _Mapping]] = ..., pyarrow_batch_config: _Optional[_Union[_data_source__client_pb2.PyArrowBatchConfigArgs, _Mapping]] = ..., kinesis_ds_config: _Optional[_Union[_data_source__client_pb2.KinesisDataSourceArgs, _Mapping]] = ..., kafka_ds_config: _Optional[_Union[_data_source__client_pb2.KafkaDataSourceArgs, _Mapping]] = ..., spark_stream_config: _Optional[_Union[_data_source__client_pb2.SparkStreamConfigArgs, _Mapping]] = ..., push_config: _Optional[_Union[_data_source__client_pb2.PushSourceArgs, _Mapping]] = ..., schema: _Optional[_Union[_schema_container__client_pb2.SchemaContainer, _Mapping]] = ..., type: _Optional[_Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., forced_batch_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., forced_stream_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ...) -> None: ...
