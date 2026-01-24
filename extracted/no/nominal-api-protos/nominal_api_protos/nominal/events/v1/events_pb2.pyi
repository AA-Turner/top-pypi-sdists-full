from nominal.direct_channel_writer.v2 import direct_nominal_channel_writer_pb2 as _direct_nominal_channel_writer_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.types.time import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Event(_message.Message):
    __slots__ = ("data_stream", "file_ingest")
    DATA_STREAM_FIELD_NUMBER: _ClassVar[int]
    FILE_INGEST_FIELD_NUMBER: _ClassVar[int]
    data_stream: DataStreamEvent
    file_ingest: FileIngestEvent
    def __init__(self, data_stream: _Optional[_Union[DataStreamEvent, _Mapping]] = ..., file_ingest: _Optional[_Union[FileIngestEvent, _Mapping]] = ...) -> None: ...

class DataStreamEvent(_message.Message):
    __slots__ = ("write_batches_request", "event_timestamp")
    WRITE_BATCHES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    write_batches_request: _containers.RepeatedCompositeFieldContainer[_direct_nominal_channel_writer_pb2.WriteBatchesRequest]
    event_timestamp: _time_pb2.Timestamp
    def __init__(self, write_batches_request: _Optional[_Iterable[_Union[_direct_nominal_channel_writer_pb2.WriteBatchesRequest, _Mapping]]] = ..., event_timestamp: _Optional[_Union[_time_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FileIngestEvent(_message.Message):
    __slots__ = ("dataset_rid", "file_id", "event_timestamp")
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    dataset_rid: str
    file_id: str
    event_timestamp: _time_pb2.Timestamp
    def __init__(self, dataset_rid: _Optional[str] = ..., file_id: _Optional[str] = ..., event_timestamp: _Optional[_Union[_time_pb2.Timestamp, _Mapping]] = ...) -> None: ...
