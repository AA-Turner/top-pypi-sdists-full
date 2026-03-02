from buf.validate import validate_pb2 as _validate_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RemoteConnection(_message.Message):
    __slots__ = ("rid", "name", "base_url", "secret_rid")
    RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    SECRET_RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    name: str
    base_url: str
    secret_rid: str
    def __init__(self, rid: _Optional[str] = ..., name: _Optional[str] = ..., base_url: _Optional[str] = ..., secret_rid: _Optional[str] = ...) -> None: ...

class CreateRemoteConnectionRequest(_message.Message):
    __slots__ = ("name", "base_url", "secret_rid", "workspace_rid")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    SECRET_RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    name: str
    base_url: str
    secret_rid: str
    workspace_rid: str
    def __init__(self, name: _Optional[str] = ..., base_url: _Optional[str] = ..., secret_rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ...) -> None: ...

class CreateRemoteConnectionResponse(_message.Message):
    __slots__ = ("remote_connection",)
    REMOTE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    remote_connection: RemoteConnection
    def __init__(self, remote_connection: _Optional[_Union[RemoteConnection, _Mapping]] = ...) -> None: ...

class GetRemoteConnectionRequest(_message.Message):
    __slots__ = ("remote_connection_rid",)
    REMOTE_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    remote_connection_rid: str
    def __init__(self, remote_connection_rid: _Optional[str] = ...) -> None: ...

class GetRemoteConnectionResponse(_message.Message):
    __slots__ = ("remote_connection",)
    REMOTE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    remote_connection: RemoteConnection
    def __init__(self, remote_connection: _Optional[_Union[RemoteConnection, _Mapping]] = ...) -> None: ...

class UpdateRemoteConnectionRequest(_message.Message):
    __slots__ = ("remote_connection_rid", "name", "base_url", "secret_rid")
    REMOTE_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    SECRET_RID_FIELD_NUMBER: _ClassVar[int]
    remote_connection_rid: str
    name: str
    base_url: str
    secret_rid: str
    def __init__(self, remote_connection_rid: _Optional[str] = ..., name: _Optional[str] = ..., base_url: _Optional[str] = ..., secret_rid: _Optional[str] = ...) -> None: ...

class UpdateRemoteConnectionResponse(_message.Message):
    __slots__ = ("remote_connection",)
    REMOTE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    remote_connection: RemoteConnection
    def __init__(self, remote_connection: _Optional[_Union[RemoteConnection, _Mapping]] = ...) -> None: ...

class DeleteRemoteConnectionRequest(_message.Message):
    __slots__ = ("remote_connection_rid",)
    REMOTE_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    remote_connection_rid: str
    def __init__(self, remote_connection_rid: _Optional[str] = ...) -> None: ...

class DeleteRemoteConnectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListRemoteConnectionsRequest(_message.Message):
    __slots__ = ("workspace_rid", "page_size", "page_token")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    page_size: int
    page_token: str
    def __init__(self, workspace_rid: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListRemoteConnectionsResponse(_message.Message):
    __slots__ = ("remote_connections", "next_page_token")
    REMOTE_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    remote_connections: _containers.RepeatedCompositeFieldContainer[RemoteConnection]
    next_page_token: str
    def __init__(self, remote_connections: _Optional[_Iterable[_Union[RemoteConnection, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...
