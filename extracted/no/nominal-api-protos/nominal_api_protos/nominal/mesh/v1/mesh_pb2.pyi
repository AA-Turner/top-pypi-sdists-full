from nominal.direct_channel_writer.v2 import direct_nominal_channel_writer_pb2 as _direct_nominal_channel_writer_pb2
from nominal.mesh.v1 import links_pb2 as _links_pb2
from nominal.mesh.v1 import remote_connections_pb2 as _remote_connections_pb2
from nominal.types.time import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeshRequest(_message.Message):
    __slots__ = ("data_stream", "file_ingest")
    DATA_STREAM_FIELD_NUMBER: _ClassVar[int]
    FILE_INGEST_FIELD_NUMBER: _ClassVar[int]
    data_stream: DataStreamRequest
    file_ingest: FileIngestRequest
    def __init__(self, data_stream: _Optional[_Union[DataStreamRequest, _Mapping]] = ..., file_ingest: _Optional[_Union[FileIngestRequest, _Mapping]] = ...) -> None: ...

class MeshResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DataStreamRequest(_message.Message):
    __slots__ = ("write_batches_request",)
    WRITE_BATCHES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    write_batches_request: _containers.RepeatedCompositeFieldContainer[_direct_nominal_channel_writer_pb2.WriteBatchesRequest]
    def __init__(self, write_batches_request: _Optional[_Iterable[_Union[_direct_nominal_channel_writer_pb2.WriteBatchesRequest, _Mapping]]] = ...) -> None: ...

class FileIngestRequest(_message.Message):
    __slots__ = ("file_metadata",)
    FILE_METADATA_FIELD_NUMBER: _ClassVar[int]
    file_metadata: FileMetadata
    def __init__(self, file_metadata: _Optional[_Union[FileMetadata, _Mapping]] = ...) -> None: ...

class FileMetadata(_message.Message):
    __slots__ = ("uuid", "dataset_uuid", "s3_path", "file_name", "origin_metadata", "bounds", "uploaded_at", "ingested_at_nanos", "tag_columns", "additional_file_tags", "file_size", "metadata")
    class OriginMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class AdditionalFileTagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    DATASET_UUID_FIELD_NUMBER: _ClassVar[int]
    S3_PATH_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_METADATA_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    UPLOADED_AT_FIELD_NUMBER: _ClassVar[int]
    INGESTED_AT_NANOS_FIELD_NUMBER: _ClassVar[int]
    TAG_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_FILE_TAGS_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    dataset_uuid: str
    s3_path: str
    file_name: str
    origin_metadata: _containers.ScalarMap[str, str]
    bounds: _time_pb2.Range
    uploaded_at: _time_pb2.Timestamp
    ingested_at_nanos: int
    tag_columns: _containers.RepeatedScalarFieldContainer[str]
    additional_file_tags: _containers.ScalarMap[str, str]
    file_size: int
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, uuid: _Optional[str] = ..., dataset_uuid: _Optional[str] = ..., s3_path: _Optional[str] = ..., file_name: _Optional[str] = ..., origin_metadata: _Optional[_Mapping[str, str]] = ..., bounds: _Optional[_Union[_time_pb2.Range, _Mapping]] = ..., uploaded_at: _Optional[_Union[_time_pb2.Timestamp, _Mapping]] = ..., ingested_at_nanos: _Optional[int] = ..., tag_columns: _Optional[_Iterable[str]] = ..., additional_file_tags: _Optional[_Mapping[str, str]] = ..., file_size: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class HealthCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
