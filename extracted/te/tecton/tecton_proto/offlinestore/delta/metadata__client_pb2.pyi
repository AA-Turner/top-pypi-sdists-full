from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TectonDeltaMetadata(_message.Message):
    __slots__ = ["dataset_result_path", "deletion_path", "feature_start_time", "ingest_path"]
    DATASET_RESULT_PATH_FIELD_NUMBER: _ClassVar[int]
    DELETION_PATH_FIELD_NUMBER: _ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    INGEST_PATH_FIELD_NUMBER: _ClassVar[int]
    dataset_result_path: str
    deletion_path: str
    feature_start_time: _timestamp_pb2.Timestamp
    ingest_path: str
    def __init__(self, deletion_path: _Optional[str] = ..., ingest_path: _Optional[str] = ..., feature_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., dataset_result_path: _Optional[str] = ...) -> None: ...
