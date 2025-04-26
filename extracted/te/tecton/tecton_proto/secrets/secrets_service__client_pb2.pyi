from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSecretScopeRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: str
    def __init__(self, scope: _Optional[str] = ...) -> None: ...

class CreateSecretScopeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteSecretRequest(_message.Message):
    __slots__ = ["key", "scope"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    key: str
    scope: str
    def __init__(self, scope: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class DeleteSecretResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteSecretScopeRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: str
    def __init__(self, scope: _Optional[str] = ...) -> None: ...

class DeleteSecretScopeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSecretValueRequest(_message.Message):
    __slots__ = ["key", "scope"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    key: str
    scope: str
    def __init__(self, scope: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class GetSecretValueResponse(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ListSecretScopesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListSecretScopesResponse(_message.Message):
    __slots__ = ["scopes"]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    scopes: _containers.RepeatedCompositeFieldContainer[SecretScope]
    def __init__(self, scopes: _Optional[_Iterable[_Union[SecretScope, _Mapping]]] = ...) -> None: ...

class ListSecretsRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: str
    def __init__(self, scope: _Optional[str] = ...) -> None: ...

class ListSecretsResponse(_message.Message):
    __slots__ = ["keys"]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[SecretKey]
    def __init__(self, keys: _Optional[_Iterable[_Union[SecretKey, _Mapping]]] = ...) -> None: ...

class PutSecretValueRequest(_message.Message):
    __slots__ = ["key", "scope", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    scope: str
    value: str
    def __init__(self, scope: _Optional[str] = ..., key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class PutSecretValueResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SecretKey(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class SecretScope(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
