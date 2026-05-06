import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.direct_channel_writer.v2 import direct_nominal_channel_writer_pb2 as _direct_nominal_channel_writer_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WriteFileDataRequest(_message.Message):
    __slots__ = ("write_batches_request", "ingest_job_rid", "dataset_file_id", "org_rid", "batch_id", "file_created_at")
    WRITE_BATCHES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_RID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    write_batches_request: _direct_nominal_channel_writer_pb2.InternalWriteBatchesRequest
    ingest_job_rid: str
    dataset_file_id: str
    org_rid: str
    batch_id: int
    file_created_at: _timestamp_pb2.Timestamp
    def __init__(self, write_batches_request: _Optional[_Union[_direct_nominal_channel_writer_pb2.InternalWriteBatchesRequest, _Mapping]] = ..., ingest_job_rid: _Optional[str] = ..., dataset_file_id: _Optional[str] = ..., org_rid: _Optional[str] = ..., batch_id: _Optional[int] = ..., file_created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
