from buf.validate import validate_pb2 as _validate_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.mesh.v1 import remote_connections_pb2 as _remote_connections_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateRemoteConnectionStatusRequest(_message.Message):
    __slots__ = ("remote_connection_rid", "status")
    REMOTE_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    remote_connection_rid: str
    status: _remote_connections_pb2.RemoteConnectionStatus
    def __init__(self, remote_connection_rid: _Optional[str] = ..., status: _Optional[_Union[_remote_connections_pb2.RemoteConnectionStatus, str]] = ...) -> None: ...

class UpdateRemoteConnectionStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
