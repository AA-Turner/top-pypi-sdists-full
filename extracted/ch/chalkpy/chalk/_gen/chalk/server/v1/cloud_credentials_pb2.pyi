from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import environment_pb2 as _environment_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class ListCloudCredentialsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCloudCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[CloudCredentialsResponse]
    def __init__(self, credentials: _Optional[_Iterable[_Union[CloudCredentialsResponse, _Mapping]]] = ...) -> None: ...

class CloudCredentialsResponse(_message.Message):
    __slots__ = ("id", "team_id", "name", "kind", "spec", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    name: str
    kind: str
    spec: _environment_pb2.CloudConfig
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        spec: _Optional[_Union[_environment_pb2.CloudConfig, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CloudCredentialsRequest(_message.Message):
    __slots__ = ("name", "kind", "config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    config: _environment_pb2.CloudConfig
    def __init__(
        self,
        name: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        config: _Optional[_Union[_environment_pb2.CloudConfig, _Mapping]] = ...,
    ) -> None: ...

class CreateCloudCredentialsRequest(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: CloudCredentialsRequest
    def __init__(self, credentials: _Optional[_Union[CloudCredentialsRequest, _Mapping]] = ...) -> None: ...

class CreateCloudCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: CloudCredentialsResponse
    def __init__(self, credentials: _Optional[_Union[CloudCredentialsResponse, _Mapping]] = ...) -> None: ...

class GetCloudCredentialsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCloudCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: CloudCredentialsResponse
    def __init__(self, credentials: _Optional[_Union[CloudCredentialsResponse, _Mapping]] = ...) -> None: ...

class DeleteCloudCredentialsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCloudCredentialsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
