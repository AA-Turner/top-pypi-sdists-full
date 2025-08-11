from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import link_pb2 as _link_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetTokenRequest(_message.Message):
    __slots__ = ("client_id", "client_secret", "grant_type", "scope")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    GRANT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    grant_type: str
    scope: str
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        client_secret: _Optional[str] = ...,
        grant_type: _Optional[str] = ...,
        scope: _Optional[str] = ...,
    ) -> None: ...

class GetTokenResponse(_message.Message):
    __slots__ = (
        "access_token",
        "token_type",
        "expires_in",
        "expires_at",
        "api_server",
        "primary_environment",
        "engines",
        "grpc_engines",
        "environment_id_to_name",
    )
    class EnginesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class GrpcEnginesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class EnvironmentIdToNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    API_SERVER_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    ENGINES_FIELD_NUMBER: _ClassVar[int]
    GRPC_ENGINES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_TO_NAME_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    token_type: str
    expires_in: int
    expires_at: _timestamp_pb2.Timestamp
    api_server: str
    primary_environment: str
    engines: _containers.ScalarMap[str, str]
    grpc_engines: _containers.ScalarMap[str, str]
    environment_id_to_name: _containers.ScalarMap[str, str]
    def __init__(
        self,
        access_token: _Optional[str] = ...,
        token_type: _Optional[str] = ...,
        expires_in: _Optional[int] = ...,
        expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        api_server: _Optional[str] = ...,
        primary_environment: _Optional[str] = ...,
        engines: _Optional[_Mapping[str, str]] = ...,
        grpc_engines: _Optional[_Mapping[str, str]] = ...,
        environment_id_to_name: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class UpdateLinkSessionRequest(_message.Message):
    __slots__ = ("status", "user_id", "session_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    status: str
    user_id: str
    session_id: str
    def __init__(
        self, status: _Optional[str] = ..., user_id: _Optional[str] = ..., session_id: _Optional[str] = ...
    ) -> None: ...

class UpdateLinkSessionResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...
