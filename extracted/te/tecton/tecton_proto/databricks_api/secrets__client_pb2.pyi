from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListSecretScopesResponse(_message.Message):
    __slots__ = ["scopes"]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    scopes: _containers.RepeatedCompositeFieldContainer[SecretScopeInfo]
    def __init__(self, scopes: _Optional[_Iterable[_Union[SecretScopeInfo, _Mapping]]] = ...) -> None: ...

class PutRequest(_message.Message):
    __slots__ = ["contents", "overwrite", "path"]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    contents: bytes
    overwrite: bool
    path: str
    def __init__(self, path: _Optional[str] = ..., contents: _Optional[bytes] = ..., overwrite: bool = ...) -> None: ...

class ScopeCreateRequest(_message.Message):
    __slots__ = ["scope"]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: str
    def __init__(self, scope: _Optional[str] = ...) -> None: ...

class SecretAclPutRequest(_message.Message):
    __slots__ = ["permission", "principal", "scope"]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    permission: str
    principal: str
    scope: str
    def __init__(self, scope: _Optional[str] = ..., principal: _Optional[str] = ..., permission: _Optional[str] = ...) -> None: ...

class SecretPutRequest(_message.Message):
    __slots__ = ["key", "scope", "string_value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    scope: str
    string_value: str
    def __init__(self, scope: _Optional[str] = ..., key: _Optional[str] = ..., string_value: _Optional[str] = ...) -> None: ...

class SecretScopeInfo(_message.Message):
    __slots__ = ["backend_type", "name"]
    BACKEND_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    backend_type: str
    name: str
    def __init__(self, name: _Optional[str] = ..., backend_type: _Optional[str] = ...) -> None: ...
