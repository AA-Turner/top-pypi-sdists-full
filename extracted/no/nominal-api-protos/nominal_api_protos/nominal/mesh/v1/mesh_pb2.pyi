from google.api import annotations_pb2 as _annotations_pb2
from nominal_api_protos.nominal.direct_channel_writer.v2 import direct_nominal_channel_writer_pb2 as _direct_nominal_channel_writer_pb2
from nominal_api_protos.nominal.mesh.v1 import links_pb2 as _links_pb2
from nominal_api_protos.nominal.mesh.v1 import remote_connections_pb2 as _remote_connections_pb2
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
    write_batches_request: _containers.RepeatedCompositeFieldContainer[_direct_nominal_channel_writer_pb2.InternalWriteBatchesRequest]
    def __init__(self, write_batches_request: _Optional[_Iterable[_Union[_direct_nominal_channel_writer_pb2.InternalWriteBatchesRequest, _Mapping]]] = ...) -> None: ...

class FileIngestRequest(_message.Message):
    __slots__ = ("ingest_request",)
    INGEST_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ingest_request: bytes
    def __init__(self, ingest_request: _Optional[bytes] = ...) -> None: ...

class HealthCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
