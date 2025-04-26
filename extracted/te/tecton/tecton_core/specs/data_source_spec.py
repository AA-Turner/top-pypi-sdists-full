from types import MappingProxyType
from typing import Callable
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import errors
from tecton_core import function_deserialization
from tecton_core import time_utils
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import data_source__client_pb2 as data_source__args_pb2
from tecton_proto.args import data_source_config__client_pb2 as data_source_config_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import data_source_type__client_pb2 as data_source_type_pb2
from tecton_proto.common import schema_container__client_pb2 as schema_container_pb2
from tecton_proto.common import secret__client_pb2 as secret_pb2
from tecton_proto.common import spark_schema__client_pb2 as spark_schema_pb2
from tecton_proto.data import batch_data_source__client_pb2 as batch_data_source__data_pb2
from tecton_proto.data import stream_data_source__client_pb2 as stream_data_source__data_pb2
from tecton_proto.data import virtual_data_source__client_pb2 as virtual_data_source__data_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


__all__ = [
    "DataSourceSpec",
    "DataSourceSpecArgsSupplement",
    "BatchSourceSpec",
    "HiveSourceSpec",
    "UnitySourceSpec",
    "FileSourceSpec",
    "SparkBatchSourceSpec",
    "PandasBatchSourceSpec",
    "PyArrowBatchSourceSpec",
    "PushTableSourceSpec",
    "RedshiftSourceSpec",
    "SnowflakeSourceSpec",
    "BigquerySourceSpec",
    "DatetimePartitionColumnSpec",
    "StreamSourceSpec",
    "KinesisSourceSpec",
    "KafkaSourceSpec",
    "SparkStreamSourceSpec",
]


@utils.frozen_strict
class DataSourceSpec(tecton_object_spec.TectonObjectSpec):
    batch_source: Optional["BatchSourceSpec"]
    stream_source: Optional["StreamSourceSpec"]
    schema: Optional[schema_container_pb2.SchemaContainer]
    type: data_source_type_pb2.DataSourceType.ValueType
    prevent_destroy: bool

    options: Mapping[str, str]

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: virtual_data_source__data_pb2.VirtualDataSource, include_main_variables_in_scope: bool = False
    ) -> "DataSourceSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.virtual_data_source_id, proto.fco_metadata
            ),
            batch_source=create_batch_source_from_data_proto(proto.batch_data_source, include_main_variables_in_scope),
            stream_source=create_stream_source_from_data_proto(
                proto.stream_data_source, include_main_variables_in_scope
            ),
            type=utils.get_field_or_none(proto, "data_source_type"),
            schema=utils.get_field_or_none(proto, "schema"),
            validation_args=validator_pb2.FcoValidationArgs(virtual_data_source=proto.validation_args),
            options=MappingProxyType(proto.options),
            prevent_destroy=proto.validation_args.args.prevent_destroy,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls,
        proto: virtual_data_source__args_pb2.VirtualDataSourceArgs,
        supplement: "DataSourceSpecArgsSupplement",
    ) -> "DataSourceSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.virtual_data_source_id, proto.info, proto.version
            ),
            batch_source=create_batch_source_from_args_proto(proto, supplement),
            stream_source=create_stream_source_from_args_proto(proto, supplement),
            schema=utils.get_field_or_none(proto, "schema"),
            type=utils.get_field_or_none(proto, "type"),
            validation_args=None,
            options=MappingProxyType(proto.options),
            prevent_destroy=proto.prevent_destroy,
        )


@attrs.define
class DataSourceSpecArgsSupplement:
    """A data class used for supplementing args protos during DataSourceSpec construction.

    This Python data class can be used to pass non-serializable types (e.g. Python functions) or data that is not
    included in args protos (e.g. schemas) into the DataSourceSpec constructor.
    """

    batch_schema: Optional[spark_schema_pb2.SparkSchema] = attrs.field(default=None)
    stream_schema: Optional[spark_schema_pb2.SparkSchema] = attrs.field(default=None)

    batch_post_processor: Optional[Callable] = attrs.field(default=None)
    stream_post_processor: Optional[Callable] = attrs.field(default=None)

    batch_data_source_function: Optional[Callable] = attrs.field(default=None)
    stream_data_source_function: Optional[Callable] = attrs.field(default=None)


@utils.frozen_strict
class BatchSourceSpec:
    """Base class for batch source specs, e.g. a HiveSourceSpec or SnowflakeSourceSpec."""

    timestamp_field: Optional[str]
    timestamp_format: Optional[str]
    post_processor: Optional[Callable] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    spark_schema: spark_schema_pb2.SparkSchema
    data_delay: Optional[pendulum.Duration]
    secrets: Optional[Mapping[str, secret_pb2.SecretReference]]


@typechecked
def create_batch_source_from_data_proto(
    proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
) -> Optional[
    Union[
        "HiveSourceSpec",
        "SparkBatchSourceSpec",
        "PandasBatchSourceSpec",
        "PyArrowBatchSourceSpec",
        "FileSourceSpec",
        "RedshiftSourceSpec",
        "SnowflakeSourceSpec",
        "UnitySourceSpec",
        "PushTableSourceSpec",
        "BigquerySourceSpec",
    ]
]:
    if proto.HasField("hive_table"):
        return HiveSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("unity_table"):
        return UnitySourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("spark_data_source_function"):
        return SparkBatchSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("pandas_data_source_function"):
        return PandasBatchSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("pyarrow_data_source_function"):
        return PyArrowBatchSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("redshift_db"):
        return RedshiftSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("snowflake"):
        return SnowflakeSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("file"):
        return FileSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("push_source_table"):
        return PushTableSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("bigquery"):
        return BigquerySourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    else:
        return None


@typechecked
def create_batch_source_from_args_proto(
    proto: virtual_data_source__args_pb2.VirtualDataSourceArgs, supplement: DataSourceSpecArgsSupplement
) -> Optional[
    Union[
        "HiveSourceSpec",
        "SparkBatchSourceSpec",
        "PandasBatchSourceSpec",
        "PyArrowBatchSourceSpec",
        "FileSourceSpec",
        "RedshiftSourceSpec",
        "SnowflakeSourceSpec",
        "UnitySourceSpec",
        "PushTableSourceSpec",
        "BigquerySourceSpec",
    ]
]:
    if proto.HasField("hive_ds_config"):
        return HiveSourceSpec.from_args_proto(proto.hive_ds_config, supplement)
    elif proto.HasField("unity_ds_config"):
        return UnitySourceSpec.from_args_proto(proto.unity_ds_config, supplement)
    elif proto.HasField("spark_batch_config"):
        return SparkBatchSourceSpec.from_args_proto(proto.spark_batch_config, supplement)
    elif proto.HasField("pandas_batch_config"):
        return PandasBatchSourceSpec.from_args_proto(proto.pandas_batch_config, supplement)
    elif proto.HasField("pyarrow_batch_config"):
        return PyArrowBatchSourceSpec.from_args_proto(proto.pyarrow_batch_config, supplement)
    elif proto.HasField("redshift_ds_config"):
        return RedshiftSourceSpec.from_args_proto(proto.redshift_ds_config, supplement)
    elif proto.HasField("snowflake_ds_config"):
        return SnowflakeSourceSpec.from_args_proto(proto.snowflake_ds_config, supplement)
    elif proto.HasField("file_ds_config"):
        return FileSourceSpec.from_args_proto(proto.file_ds_config, supplement)
    elif proto.HasField("bigquery_ds_config"):
        return BigquerySourceSpec.from_args_proto(proto.bigquery_ds_config, supplement)
    elif proto.HasField("push_config"):
        return PushTableSourceSpec.from_args_proto(proto, supplement)
    else:
        return None


def _datepart_to_minimum_seconds(datepart: str) -> int:
    if datepart == "year":
        return 365 * 24 * 60 * 60
    elif datepart == "month":
        return 28 * 24 * 60 * 60
    elif datepart == "day":
        return 24 * 60 * 60
    elif datepart == "hour":
        return 60 * 60
    elif datepart == "date":
        return 24 * 60 * 60
    else:
        msg = f"Unexpected datepart string: {datepart}"
        raise ValueError(msg)


def _datepart_to_default_format_string(datepart: str) -> str:
    if datepart == "year":
        return "%Y"
    elif datepart == "month":
        return "%m"
    elif datepart == "day":
        return "%d"
    elif datepart == "hour":
        return "%H"
    elif datepart == "date":
        return "%Y-%m-%d"
    else:
        msg = f"Unexpected datepart string: {datepart}"
        raise ValueError(msg)


@utils.frozen_strict
class DatetimePartitionColumnSpec:
    column_name: str
    format_string: str
    minimum_seconds: int

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.DatetimePartitionColumn
    ) -> "DatetimePartitionColumnSpec":
        return cls(
            column_name=utils.get_field_or_none(proto, "column_name"),
            format_string=utils.get_field_or_none(proto, "format_string"),
            minimum_seconds=utils.get_field_or_none(proto, "minimum_seconds"),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: data_source__args_pb2.DatetimePartitionColumnArgs) -> "DatetimePartitionColumnSpec":
        # This constructor mirrors backend Kotlin logic: https://github.com/tecton-ai/tecton/blob/6107d76680fa97e6155c6da9ee7d2da47bc3d6a7/java/com/tecton/datamodel/datasource/Utils.kt#L41.
        # In the short-term, divergence between Python and Kotlin will be prevented using integration test coverage. Longer-term, these values should probably be derived client-side only and included in the data source args.
        minimum_seconds = _datepart_to_minimum_seconds(proto.datepart)

        if proto.format_string:
            # NOTE: we do not use `zero_padded` if the user specified a format_string. However,
            # we do not directly validate that this is unset. We may want to in the future, but
            # not making the change now in case it causes a repo failure.
            format_string = proto.format_string
        else:
            if proto.datepart == "date" and not proto.zero_padded:
                msg = "Non-zero padded date strings are not supported. Please set `zero_padded = True` in your `DatetimePartitionColumn`."
                raise ValueError(msg)

            default_format_string = _datepart_to_default_format_string(proto.datepart)
            if proto.zero_padded:
                # The default string format should be zero padded.
                format_string = default_format_string
            else:
                format_string = default_format_string.replace("%", "%-")

        return DatetimePartitionColumnSpec(
            column_name=proto.column_name, format_string=format_string, minimum_seconds=minimum_seconds
        )


@utils.frozen_strict
class HiveSourceSpec(BatchSourceSpec):
    database: str
    table: str
    datetime_partition_columns: Tuple[DatetimePartitionColumnSpec, ...]

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "HiveSourceSpec":
        # Needed for canary backwards compatability. Can be deleted on the following release.
        if proto.date_partition_column and not proto.datetime_partition_columns:
            proto.datetime_partition_columns.append(
                batch_data_source__data_pb2.DatetimePartitionColumn(
                    column_name=proto.date_partition_column,
                    format_string="%Y-%m-%d",
                    minimum_seconds=24 * 60 * 60,
                )
            )

        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_batch_translator, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            table=utils.get_field_or_none(proto.hive_table, "table"),
            database=utils.get_field_or_none(proto.hive_table, "database"),
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_data_proto(column) for column in proto.datetime_partition_columns
            ),
            secrets=None,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.HiveDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "HiveSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.batch_post_processor

        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=utils.get_field_or_none(proto, "timestamp_format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            table=utils.get_field_or_none(proto, "table"),
            database=utils.get_field_or_none(proto, "database"),
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_args_proto(column) for column in proto.datetime_partition_columns
            ),
            secrets=None,
        )


@utils.frozen_strict
class PushTableSourceSpec(BatchSourceSpec):
    ingested_data_location: str = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    spark_schema: spark_schema_pb2.SparkSchema = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, _: bool = False
    ) -> "PushTableSourceSpec":
        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=None,
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            ingested_data_location=utils.get_field_or_none(proto.push_source_table, "ingested_data_location"),
            secrets=None,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: virtual_data_source__args_pb2.VirtualDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "PushTableSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.

        # from tecton_spark.schema_spark_utils import schema_to_spark
        # from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper
        #
        # schema = Schema(proto.schema.tecton_schema)
        # spark_schema = SparkSchemaWrapper(schema_to_spark(schema)).to_proto()
        return cls(
            timestamp_field=utils.get_field_or_none(proto.push_config, "timestamp_field"),
            timestamp_format=None,
            post_processor=None,
            data_delay=None,
            spark_schema=supplement.batch_schema,
            # TODO(Achal): Push sources don't really support this because you can't read from a
            # push source that we haven't written to and logged offline.
            ingested_data_location="",
            secrets=None,
        )


@utils.frozen_strict
class UnitySourceSpec(BatchSourceSpec):
    catalog: str
    schema: str
    table: str
    datetime_partition_columns: Tuple[DatetimePartitionColumnSpec, ...]
    access_mode: data_source__args_pb2.UnityCatalogAccessMode

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "UnitySourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_batch_translator, include_main_variables_in_scope
            )
        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            table=utils.get_field_or_none(proto.unity_table, "table"),
            schema=utils.get_field_or_none(proto.unity_table, "schema"),
            catalog=utils.get_field_or_none(proto.unity_table, "catalog"),
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_data_proto(column) for column in proto.datetime_partition_columns
            ),
            access_mode=utils.get_field_or_none(proto.unity_table, "access_mode"),
            secrets=None,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.UnityDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "UnitySourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.batch_post_processor
        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=utils.get_field_or_none(proto, "timestamp_format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            table=utils.get_field_or_none(proto, "table"),
            schema=utils.get_field_or_none(proto, "schema"),
            catalog=utils.get_field_or_none(proto, "catalog"),
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_args_proto(column) for column in proto.datetime_partition_columns
            ),
            access_mode=utils.get_field_or_none(proto, "access_mode"),
            secrets=None,
        )


@utils.frozen_strict
class FileSourceSpec(BatchSourceSpec):
    uri: Optional[str]
    file_format: batch_data_source__data_pb2.FileDataSourceFormat.ValueType
    convert_to_glue_format: bool
    schema_uri: Optional[str]
    schema_override: Optional[spark_schema_pb2.SparkSchema]
    datetime_partition_columns: Tuple[DatetimePartitionColumnSpec, ...]

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "FileSourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_batch_translator, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            uri=utils.get_field_or_none(proto.file, "uri"),
            file_format=utils.get_field_or_none(proto.file, "format"),
            convert_to_glue_format=proto.file.convert_to_glue_format,
            schema_uri=utils.get_field_or_none(proto.file, "schema_uri"),
            schema_override=utils.get_field_or_none(proto.file, "schema_override"),
            secrets=None,
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_data_proto(column) for column in proto.datetime_partition_columns
            ),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.FileDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "FileSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.batch_post_processor

        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=utils.get_field_or_none(proto, "timestamp_format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema if supplement.batch_schema else spark_schema_pb2.SparkSchema(),
            uri=utils.get_field_or_none(proto, "uri"),
            file_format=FileSourceSpec._convert_file_format_string_to_enum(proto.file_format),
            convert_to_glue_format=proto.convert_to_glue_format,
            schema_uri=utils.get_field_or_none(proto, "schema_uri"),
            schema_override=utils.get_field_or_none(proto, "schema_override"),
            secrets=None,
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_args_proto(column) for column in proto.datetime_partition_columns
            ),
        )

    @staticmethod
    @typechecked
    def _convert_file_format_string_to_enum(
        file_format: str,
    ) -> batch_data_source__data_pb2.FileDataSourceFormat.ValueType:
        return batch_data_source__data_pb2.FileDataSourceFormat.Value(f"FILE_DATA_SOURCE_FORMAT_{file_format.upper()}")


@utils.frozen_strict
class SparkBatchSourceSpec(BatchSourceSpec):
    function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    supports_time_filtering: bool

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "SparkBatchSourceSpec":
        function = None
        if proto.spark_data_source_function.HasField("function"):
            function = function_deserialization.from_proto(
                proto.spark_data_source_function.function, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            supports_time_filtering=proto.spark_data_source_function.supports_time_filtering,
            function=function,
            secrets=None,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.SparkBatchConfigArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "SparkBatchSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.HasField("data_source_function"):
            data_source_function = function_deserialization.from_proto(proto.data_source_function)
        else:
            data_source_function = supplement.batch_data_source_function

        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=supplement.batch_schema,
            supports_time_filtering=proto.supports_time_filtering,
            function=data_source_function,
            secrets=None,
        )


@utils.frozen_strict
class PandasBatchSourceSpec(BatchSourceSpec):
    function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    supports_time_filtering: bool

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "PandasBatchSourceSpec":
        function = None
        if proto.pandas_data_source_function.HasField("function"):
            function = function_deserialization.from_proto(
                proto.pandas_data_source_function.function, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            supports_time_filtering=proto.pandas_data_source_function.supports_time_filtering,
            function=function,
            secrets=proto.secrets,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.PandasBatchConfigArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "PandasBatchSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.HasField("data_source_function"):
            data_source_function = function_deserialization.from_proto(proto.data_source_function)
        else:
            data_source_function = supplement.batch_data_source_function

        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=supplement.batch_schema,
            supports_time_filtering=proto.supports_time_filtering,
            function=data_source_function,
            secrets=proto.secrets,
        )


@utils.frozen_strict
class PyArrowBatchSourceSpec(BatchSourceSpec):
    function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    supports_time_filtering: bool

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "PyArrowBatchSourceSpec":
        function = None
        if proto.pyarrow_data_source_function.HasField("function"):
            function = function_deserialization.from_proto(
                proto.pyarrow_data_source_function.function, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            supports_time_filtering=proto.pyarrow_data_source_function.supports_time_filtering,
            function=function,
            secrets=proto.secrets,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.PyArrowBatchConfigArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "PyArrowBatchSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.HasField("data_source_function"):
            data_source_function = function_deserialization.from_proto(proto.data_source_function)
        else:
            data_source_function = supplement.batch_data_source_function

        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=supplement.batch_schema,
            supports_time_filtering=proto.supports_time_filtering,
            function=data_source_function,
            secrets=proto.secrets,
        )


@utils.frozen_strict
class RedshiftSourceSpec(BatchSourceSpec):
    endpoint: str
    table: Optional[str]
    query: Optional[str]
    temp_s3: Optional[str]

    def __attrs_post_init__(self):
        if (self.table and self.query) or (not self.table and not self.query):
            raise errors.REDSHIFT_DS_EITHER_TABLE_OR_QUERY

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "RedshiftSourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_batch_translator, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            endpoint=utils.get_field_or_none(proto.redshift_db, "endpoint"),
            table=utils.get_field_or_none(proto.redshift_db, "table"),
            query=utils.get_field_or_none(proto.redshift_db, "query"),
            temp_s3=utils.get_field_or_none(proto.redshift_db, "temp_s3"),
            secrets=None,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.RedshiftDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "RedshiftSourceSpec":
        # The temp_s3 directory should be set, and this should have been verified during validation. The one exception
        # is for unit tests (i.e. `test_run()`). In unit tests, validation is skipped and the redshift directory should
        # not need to be set, so fallback to an empty string.
        temp_s3 = conf.get_or_none("SPARK_REDSHIFT_TEMP_DIR") or ""

        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.batch_post_processor

        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=None,
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            endpoint=utils.get_field_or_none(proto, "endpoint"),
            table=utils.get_field_or_none(proto, "table"),
            query=utils.get_field_or_none(proto, "query"),
            temp_s3=temp_s3,
            secrets=None,
        )


@utils.frozen_strict
class SnowflakeSourceSpec(BatchSourceSpec):
    database: Optional[str]
    schema: Optional[str]
    warehouse: Optional[str]
    url: Optional[str]
    role: Optional[str]
    table: Optional[str]
    query: Optional[str]
    user: Optional[secret_pb2.SecretReference]
    password: Optional[secret_pb2.SecretReference]

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "SnowflakeSourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_batch_translator, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            url=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "url"),
            database=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "database"),
            schema=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "schema"),
            warehouse=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "warehouse"),
            role=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "role"),
            table=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "table"),
            query=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "query"),
            secrets=None,
            user=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "user"),
            password=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "password"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.SnowflakeDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "SnowflakeSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.batch_post_processor

        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=None,
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            url=utils.get_field_or_none(proto, "url"),
            database=utils.get_field_or_none(proto, "database"),
            schema=utils.get_field_or_none(proto, "schema"),
            warehouse=utils.get_field_or_none(proto, "warehouse"),
            role=utils.get_field_or_none(proto, "role"),
            table=utils.get_field_or_none(proto, "table"),
            query=utils.get_field_or_none(proto, "query"),
            secrets=None,
            user=utils.get_field_or_none(proto, "user"),
            password=utils.get_field_or_none(proto, "password"),
        )


@utils.frozen_strict
class BigquerySourceSpec(BatchSourceSpec):
    project_id: Optional[str]
    dataset: Optional[str]
    table: Optional[str]
    query: Optional[str]
    location: Optional[str]
    credentials: Optional[secret_pb2.SecretReference]

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.BatchDataSource, include_main_variables_in_scope: bool = False
    ) -> "BigquerySourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_batch_translator, include_main_variables_in_scope
            )

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            project_id=utils.get_field_or_none(proto.bigquery, "project_id"),
            dataset=utils.get_field_or_none(proto.bigquery, "dataset"),
            location=utils.get_field_or_none(proto.bigquery, "location"),
            table=utils.get_field_or_none(proto.bigquery, "table"),
            query=utils.get_field_or_none(proto.bigquery, "query"),
            secrets=None,
            credentials=utils.get_field_or_none(proto.bigquery, "credentials"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.BigqueryDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "BigquerySourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.batch_post_processor

        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=None,
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            project_id=utils.get_field_or_none(proto, "project_id"),
            dataset=utils.get_field_or_none(proto, "dataset"),
            location=utils.get_field_or_none(proto, "location"),
            table=utils.get_field_or_none(proto, "table"),
            query=utils.get_field_or_none(proto, "query"),
            secrets=None,
            credentials=utils.get_field_or_none(proto, "credentials"),
        )


@utils.frozen_strict
class StreamOptionSpec:
    key: str
    value: str


@utils.frozen_strict
class StreamSourceSpec:
    """Base class for stream source specs, e.g. a KinesisSourceSpec or KafkaSourceSpec."""

    deduplication_column_names: Tuple[str, ...]
    options: Tuple[StreamOptionSpec, ...]
    watermark_delay_threshold: pendulum.Duration
    spark_schema: spark_schema_pb2.SparkSchema


@typechecked
def create_stream_source_from_data_proto(
    proto: stream_data_source__data_pb2.StreamDataSource, include_main_variables_in_scope: bool = False
) -> Optional[Union["KinesisSourceSpec", "KafkaSourceSpec", "SparkStreamSourceSpec"]]:
    if proto.HasField("kinesis_data_source"):
        return KinesisSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("kafka_data_source"):
        return KafkaSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    elif proto.HasField("spark_data_source_function"):
        return SparkStreamSourceSpec.from_data_proto(proto, include_main_variables_in_scope)
    else:
        return None


@typechecked
def create_stream_source_from_args_proto(
    proto: virtual_data_source__args_pb2.VirtualDataSourceArgs, supplement: DataSourceSpecArgsSupplement
) -> Optional[Union["KinesisSourceSpec", "KafkaSourceSpec", "SparkStreamSourceSpec"]]:
    if proto.HasField("kinesis_ds_config"):
        return KinesisSourceSpec.from_args_proto(proto.kinesis_ds_config, supplement)
    elif proto.HasField("kafka_ds_config"):
        return KafkaSourceSpec.from_args_proto(proto.kafka_ds_config, supplement)
    elif proto.HasField("spark_stream_config"):
        return SparkStreamSourceSpec.from_args_proto(proto.spark_stream_config, supplement)
    else:
        return None


@utils.frozen_strict
class KinesisSourceSpec(StreamSourceSpec):
    post_processor: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    stream_name: str
    region: str
    initial_stream_position: data_source_config_pb2.InitialStreamPosition.ValueType

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: stream_data_source__data_pb2.StreamDataSource, include_main_variables_in_scope: bool = False
    ) -> "KinesisSourceSpec":
        post_processor = None
        if proto.HasField("raw_stream_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_stream_translator, include_main_variables_in_scope
            )

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.deduplication_column_names),
            post_processor=post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.stream_config.watermark_delay_threshold),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            stream_name=utils.get_field_or_none(proto.kinesis_data_source, "stream_name"),
            region=utils.get_field_or_none(proto.kinesis_data_source, "region"),
            initial_stream_position=proto.stream_config.initial_stream_position,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.KinesisDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "KinesisSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.stream_post_processor

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.common_args.deduplication_columns),
            post_processor=post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.common_args.watermark_delay_threshold),
            spark_schema=supplement.stream_schema,
            stream_name=utils.get_field_or_none(proto, "stream_name"),
            region=utils.get_field_or_none(proto, "region"),
            initial_stream_position=proto.initial_stream_position,
        )


@utils.frozen_strict
class KafkaSourceSpec(StreamSourceSpec):
    post_processor: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    bootstrap_servers: str
    topics: str
    ssl_keystore_location: Optional[str]
    ssl_keystore_password_secret_id: Optional[str]
    ssl_truststore_location: Optional[str]
    ssl_truststore_password_secret_id: Optional[str]
    security_protocol: Optional[str]

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: stream_data_source__data_pb2.StreamDataSource, include_main_variables_in_scope: bool = False
    ) -> "KafkaSourceSpec":
        post_processor = None
        if proto.HasField("raw_stream_translator"):
            post_processor = function_deserialization.from_proto(
                proto.raw_stream_translator, include_main_variables_in_scope
            )

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.deduplication_column_names),
            post_processor=post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.stream_config.watermark_delay_threshold),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            bootstrap_servers=utils.get_field_or_none(proto.kafka_data_source, "bootstrap_servers"),
            topics=utils.get_field_or_none(proto.kafka_data_source, "topics"),
            ssl_keystore_location=utils.get_field_or_none(proto.kafka_data_source, "ssl_keystore_location"),
            ssl_keystore_password_secret_id=utils.get_field_or_none(
                proto.kafka_data_source, "ssl_keystore_password_secret_id"
            ),
            ssl_truststore_location=utils.get_field_or_none(proto.kafka_data_source, "ssl_truststore_location"),
            ssl_truststore_password_secret_id=utils.get_field_or_none(
                proto.kafka_data_source, "ssl_truststore_password_secret_id"
            ),
            security_protocol=utils.get_field_or_none(proto.kafka_data_source, "security_protocol"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.KafkaDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "KafkaSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.common_args.HasField("post_processor"):
            post_processor = function_deserialization.from_proto(proto.common_args.post_processor)
        else:
            post_processor = supplement.stream_post_processor

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.common_args.deduplication_columns),
            post_processor=post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.common_args.watermark_delay_threshold),
            spark_schema=supplement.stream_schema,
            bootstrap_servers=utils.get_field_or_none(proto, "kafka_bootstrap_servers"),
            topics=utils.get_field_or_none(proto, "topics"),
            ssl_keystore_location=utils.get_field_or_none(proto, "ssl_keystore_location"),
            ssl_keystore_password_secret_id=utils.get_field_or_none(proto, "ssl_keystore_password_secret_id"),
            ssl_truststore_location=utils.get_field_or_none(proto, "ssl_truststore_location"),
            ssl_truststore_password_secret_id=utils.get_field_or_none(proto, "ssl_truststore_password_secret_id"),
            security_protocol=utils.get_field_or_none(proto, "security_protocol"),
        )


@utils.frozen_strict
class SparkStreamSourceSpec(StreamSourceSpec):
    function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: stream_data_source__data_pb2.StreamDataSource, include_main_variables_in_scope: bool = False
    ) -> "SparkStreamSourceSpec":
        function = None
        if proto.spark_data_source_function.HasField("function"):
            function = function_deserialization.from_proto(
                proto.spark_data_source_function.function, include_main_variables_in_scope
            )

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.deduplication_column_names),
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.stream_config.watermark_delay_threshold),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            function=function,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.SparkStreamConfigArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "SparkStreamSourceSpec":
        # If a function was serialized for this data source (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.HasField("data_source_function"):
            data_source_function = function_deserialization.from_proto(proto.data_source_function)
        else:
            data_source_function = supplement.stream_data_source_function

        return cls(
            deduplication_column_names=(),
            options=(),
            watermark_delay_threshold=pendulum.Duration(),
            spark_schema=supplement.stream_schema,
            function=data_source_function,
        )


# Resolve forward type declarations.
attrs.resolve_types(DataSourceSpec, locals(), globals())
attrs.resolve_types(StreamSourceSpec, locals(), globals())
