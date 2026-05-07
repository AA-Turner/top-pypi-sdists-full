import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.direct_channel_writer.v2 import file_data_pb2 as _file_data_pb2
from nominal_api_protos.nominal.file_ingest.v1 import ingest_request_pb2 as _ingest_request_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.types.object_storage import handle_pb2 as _handle_pb2
from nominal_api_protos.nominal.types.time import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetDatasetFileIngestStatusRequest(_message.Message):
    __slots__ = ("dataset_file_id", "dataset_rid", "parsing", "ingesting", "error", "ingest_job_rid")
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    PARSING_FIELD_NUMBER: _ClassVar[int]
    INGESTING_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    dataset_file_id: str
    dataset_rid: str
    parsing: Parsing
    ingesting: Ingesting
    error: Error
    ingest_job_rid: str
    def __init__(self, dataset_file_id: _Optional[str] = ..., dataset_rid: _Optional[str] = ..., parsing: _Optional[_Union[Parsing, _Mapping]] = ..., ingesting: _Optional[_Union[Ingesting, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., ingest_job_rid: _Optional[str] = ...) -> None: ...

class SetDatasetFileIngestStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Parsing(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Ingesting(_message.Message):
    __slots__ = ("bounds",)
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    bounds: _time_pb2.Range
    def __init__(self, bounds: _Optional[_Union[_time_pb2.Range, _Mapping]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("error_type", "message")
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_type: str
    message: str
    def __init__(self, error_type: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ParseFileRequest(_message.Message):
    __slots__ = ("ingest_job_rid", "dataset_file_id", "dataset_rid", "data_ingest", "workspace_rid")
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    DATA_INGEST_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    ingest_job_rid: str
    dataset_file_id: str
    dataset_rid: str
    data_ingest: _ingest_request_pb2.DataFileIngest
    workspace_rid: str
    def __init__(self, ingest_job_rid: _Optional[str] = ..., dataset_file_id: _Optional[str] = ..., dataset_rid: _Optional[str] = ..., data_ingest: _Optional[_Union[_ingest_request_pb2.DataFileIngest, _Mapping]] = ..., workspace_rid: _Optional[str] = ...) -> None: ...

class ParseFileResponse(_message.Message):
    __slots__ = ("staged_batches", "bounds")
    STAGED_BATCHES_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    staged_batches: _containers.RepeatedCompositeFieldContainer[StagedBatch]
    bounds: _time_pb2.Range
    def __init__(self, staged_batches: _Optional[_Iterable[_Union[StagedBatch, _Mapping]]] = ..., bounds: _Optional[_Union[_time_pb2.Range, _Mapping]] = ...) -> None: ...

class WriteFileBatchesToKafkaRequest(_message.Message):
    __slots__ = ("staged_batches", "ingest_job_rid", "file_rid", "org_rid", "dataset_file_id", "dataset_rid", "file_created_at")
    STAGED_BATCHES_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    FILE_RID_FIELD_NUMBER: _ClassVar[int]
    ORG_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    FILE_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    staged_batches: _containers.RepeatedCompositeFieldContainer[StagedBatch]
    ingest_job_rid: str
    file_rid: str
    org_rid: str
    dataset_file_id: str
    dataset_rid: str
    file_created_at: _timestamp_pb2.Timestamp
    def __init__(self, staged_batches: _Optional[_Iterable[_Union[StagedBatch, _Mapping]]] = ..., ingest_job_rid: _Optional[str] = ..., file_rid: _Optional[str] = ..., org_rid: _Optional[str] = ..., dataset_file_id: _Optional[str] = ..., dataset_rid: _Optional[str] = ..., file_created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StagedBatch(_message.Message):
    __slots__ = ("batch_id", "handle", "format")
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    batch_id: int
    handle: _handle_pb2.Handle
    format: _file_data_pb2.BatchFormat
    def __init__(self, batch_id: _Optional[int] = ..., handle: _Optional[_Union[_handle_pb2.Handle, _Mapping]] = ..., format: _Optional[_Union[_file_data_pb2.BatchFormat, str]] = ...) -> None: ...

class WriteFileBatchesToKafkaResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
