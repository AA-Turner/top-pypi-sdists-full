from buf.validate import validate_pb2 as _validate_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MarkBatchesCompletedRequest(_message.Message):
    __slots__ = ("ingest_job_rid", "dataset_file_id", "batch_ids")
    INGEST_JOB_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_IDS_FIELD_NUMBER: _ClassVar[int]
    ingest_job_rid: str
    dataset_file_id: str
    batch_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ingest_job_rid: _Optional[str] = ..., dataset_file_id: _Optional[str] = ..., batch_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class MarkBatchesCompletedResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
