import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.types.object_storage import handle_pb2 as _handle_pb2
from nominal_api_protos.nominal.types.time import timestamp_parsers_pb2 as _timestamp_parsers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IngestFileRequest(_message.Message):
    __slots__ = ("ingest_job_rid", "dataset_file_id", "dataset_rid", "org_rid", "workspace_rid", "handle", "timestamp_metadata", "additional_tags", "log_ingest", "data_ingest", "file_created_at", "is_primary")
    class AdditionalTagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    ORG_RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_METADATA_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_TAGS_FIELD_NUMBER: _ClassVar[int]
    LOG_INGEST_FIELD_NUMBER: _ClassVar[int]
    DATA_INGEST_FIELD_NUMBER: _ClassVar[int]
    FILE_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    ingest_job_rid: str
    dataset_file_id: str
    dataset_rid: str
    org_rid: str
    workspace_rid: str
    handle: _handle_pb2.Handle
    timestamp_metadata: TimestampMetadata
    additional_tags: _containers.ScalarMap[str, str]
    log_ingest: LogFileIngest
    data_ingest: DataFileIngest
    file_created_at: _timestamp_pb2.Timestamp
    is_primary: bool
    def __init__(self, ingest_job_rid: _Optional[str] = ..., dataset_file_id: _Optional[str] = ..., dataset_rid: _Optional[str] = ..., org_rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ..., handle: _Optional[_Union[_handle_pb2.Handle, _Mapping]] = ..., timestamp_metadata: _Optional[_Union[TimestampMetadata, _Mapping]] = ..., additional_tags: _Optional[_Mapping[str, str]] = ..., log_ingest: _Optional[_Union[LogFileIngest, _Mapping]] = ..., data_ingest: _Optional[_Union[DataFileIngest, _Mapping]] = ..., file_created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_primary: bool = ...) -> None: ...

class LogFileIngest(_message.Message):
    __slots__ = ("log_channel",)
    LOG_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    log_channel: str
    def __init__(self, log_channel: _Optional[str] = ...) -> None: ...

class DataFileIngest(_message.Message):
    __slots__ = ("wide_opts", "long_opts", "batch_opts", "units", "channel_prefix")
    class UnitsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    WIDE_OPTS_FIELD_NUMBER: _ClassVar[int]
    LONG_OPTS_FIELD_NUMBER: _ClassVar[int]
    BATCH_OPTS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_PREFIX_FIELD_NUMBER: _ClassVar[int]
    wide_opts: WideOpts
    long_opts: LongOpts
    batch_opts: BatchOpts
    units: _containers.ScalarMap[str, str]
    channel_prefix: str
    def __init__(self, wide_opts: _Optional[_Union[WideOpts, _Mapping]] = ..., long_opts: _Optional[_Union[LongOpts, _Mapping]] = ..., batch_opts: _Optional[_Union[BatchOpts, _Mapping]] = ..., units: _Optional[_Mapping[str, str]] = ..., channel_prefix: _Optional[str] = ...) -> None: ...

class WideOpts(_message.Message):
    __slots__ = ("csv_opts", "parquet_opts", "avro_opts", "tag_columns", "exclude_columns")
    class TagColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CSV_OPTS_FIELD_NUMBER: _ClassVar[int]
    PARQUET_OPTS_FIELD_NUMBER: _ClassVar[int]
    AVRO_OPTS_FIELD_NUMBER: _ClassVar[int]
    TAG_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    csv_opts: CsvOpts
    parquet_opts: ParquetOpts
    avro_opts: AvroOpts
    tag_columns: _containers.ScalarMap[str, str]
    exclude_columns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, csv_opts: _Optional[_Union[CsvOpts, _Mapping]] = ..., parquet_opts: _Optional[_Union[ParquetOpts, _Mapping]] = ..., avro_opts: _Optional[_Union[AvroOpts, _Mapping]] = ..., tag_columns: _Optional[_Mapping[str, str]] = ..., exclude_columns: _Optional[_Iterable[str]] = ...) -> None: ...

class LongOpts(_message.Message):
    __slots__ = ("csv_opts", "parquet_opts", "avro_opts", "channel_column", "value_column", "tags_column")
    CSV_OPTS_FIELD_NUMBER: _ClassVar[int]
    PARQUET_OPTS_FIELD_NUMBER: _ClassVar[int]
    AVRO_OPTS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_COLUMN_FIELD_NUMBER: _ClassVar[int]
    VALUE_COLUMN_FIELD_NUMBER: _ClassVar[int]
    TAGS_COLUMN_FIELD_NUMBER: _ClassVar[int]
    csv_opts: CsvOpts
    parquet_opts: ParquetOpts
    avro_opts: AvroOpts
    channel_column: str
    value_column: str
    tags_column: str
    def __init__(self, csv_opts: _Optional[_Union[CsvOpts, _Mapping]] = ..., parquet_opts: _Optional[_Union[ParquetOpts, _Mapping]] = ..., avro_opts: _Optional[_Union[AvroOpts, _Mapping]] = ..., channel_column: _Optional[str] = ..., value_column: _Optional[str] = ..., tags_column: _Optional[str] = ...) -> None: ...

class BatchOpts(_message.Message):
    __slots__ = ("avro_opts", "channel_field", "timestamps_field", "values_field", "tags_field")
    AVRO_OPTS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPS_FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_FIELD_NUMBER: _ClassVar[int]
    avro_opts: AvroOpts
    channel_field: str
    timestamps_field: str
    values_field: str
    tags_field: str
    def __init__(self, avro_opts: _Optional[_Union[AvroOpts, _Mapping]] = ..., channel_field: _Optional[str] = ..., timestamps_field: _Optional[str] = ..., values_field: _Optional[str] = ..., tags_field: _Optional[str] = ...) -> None: ...

class TimestampMetadata(_message.Message):
    __slots__ = ("column", "type")
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    column: str
    type: _timestamp_parsers_pb2.TimestampType
    def __init__(self, column: _Optional[str] = ..., type: _Optional[_Union[_timestamp_parsers_pb2.TimestampType, _Mapping]] = ...) -> None: ...

class CsvOpts(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ParquetOpts(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AvroOpts(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
