import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.types.object_storage import handle_pb2 as _handle_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatchFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATCH_FORMAT_UNSPECIFIED: _ClassVar[BatchFormat]
    BATCH_FORMAT_WRITE_BATCHES_REQUEST_PROTO: _ClassVar[BatchFormat]
BATCH_FORMAT_UNSPECIFIED: BatchFormat
BATCH_FORMAT_WRITE_BATCHES_REQUEST_PROTO: BatchFormat

class WriteFileDataRequest(_message.Message):
    __slots__ = ("batch_handle", "ingest_job_rid", "dataset_file_id", "org_rid", "batch_id", "file_created_at", "batch_format", "is_primary")
    BATCH_HANDLE_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_RID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    BATCH_FORMAT_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    batch_handle: _handle_pb2.Handle
    ingest_job_rid: str
    dataset_file_id: str
    org_rid: str
    batch_id: int
    file_created_at: _timestamp_pb2.Timestamp
    batch_format: BatchFormat
    is_primary: bool
    def __init__(self, batch_handle: _Optional[_Union[_handle_pb2.Handle, _Mapping]] = ..., ingest_job_rid: _Optional[str] = ..., dataset_file_id: _Optional[str] = ..., org_rid: _Optional[str] = ..., batch_id: _Optional[int] = ..., file_created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., batch_format: _Optional[_Union[BatchFormat, str]] = ..., is_primary: bool = ...) -> None: ...
