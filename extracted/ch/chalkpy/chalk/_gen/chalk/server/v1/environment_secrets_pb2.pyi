from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class SecretScopeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SECRET_SCOPE_TYPE_UNSPECIFIED: _ClassVar[SecretScopeType]
    SECRET_SCOPE_TYPE_ENVIRONMENT: _ClassVar[SecretScopeType]
    SECRET_SCOPE_TYPE_SANDBOX: _ClassVar[SecretScopeType]
    SECRET_SCOPE_TYPE_SCALING_GROUP: _ClassVar[SecretScopeType]
    SECRET_SCOPE_TYPE_FUNCTION: _ClassVar[SecretScopeType]
    SECRET_SCOPE_TYPE_NOTEBOOK: _ClassVar[SecretScopeType]

class SecretSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SECRET_SOURCE_UNSPECIFIED: _ClassVar[SecretSource]
    SECRET_SOURCE_MANAGED: _ClassVar[SecretSource]
    SECRET_SOURCE_EXTERNAL: _ClassVar[SecretSource]

SECRET_SCOPE_TYPE_UNSPECIFIED: SecretScopeType
SECRET_SCOPE_TYPE_ENVIRONMENT: SecretScopeType
SECRET_SCOPE_TYPE_SANDBOX: SecretScopeType
SECRET_SCOPE_TYPE_SCALING_GROUP: SecretScopeType
SECRET_SCOPE_TYPE_FUNCTION: SecretScopeType
SECRET_SCOPE_TYPE_NOTEBOOK: SecretScopeType
SECRET_SOURCE_UNSPECIFIED: SecretSource
SECRET_SOURCE_MANAGED: SecretSource
SECRET_SOURCE_EXTERNAL: SecretSource

class Secret(_message.Message):
    __slots__ = ("id", "name", "updated_at", "integration_id", "source", "scope", "granted_scopes")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    GRANTED_SCOPES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    updated_at: _timestamp_pb2.Timestamp
    integration_id: str
    source: SecretSource
    scope: SecretScope
    granted_scopes: _containers.RepeatedCompositeFieldContainer[SecretScope]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        integration_id: _Optional[str] = ...,
        source: _Optional[_Union[SecretSource, str]] = ...,
        scope: _Optional[_Union[SecretScope, _Mapping]] = ...,
        granted_scopes: _Optional[_Iterable[_Union[SecretScope, _Mapping]]] = ...,
    ) -> None: ...

class SecretScope(_message.Message):
    __slots__ = ("type", "ref")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    type: SecretScopeType
    ref: str
    def __init__(self, type: _Optional[_Union[SecretScopeType, str]] = ..., ref: _Optional[str] = ...) -> None: ...

class SecretValue(_message.Message):
    __slots__ = ("name", "value", "source")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    source: SecretSource
    def __init__(
        self,
        name: _Optional[str] = ...,
        value: _Optional[str] = ...,
        source: _Optional[_Union[SecretSource, str]] = ...,
    ) -> None: ...

class SecretConfigValue(_message.Message):
    __slots__ = ("literal", "secret_id")
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    literal: str
    secret_id: str
    def __init__(self, literal: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class SecretWithValue(_message.Message):
    __slots__ = ("id", "updated_at", "name", "full_name", "value", "source")
    ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    updated_at: _timestamp_pb2.Timestamp
    name: str
    full_name: str
    value: str
    source: SecretSource
    def __init__(
        self,
        id: _Optional[str] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        name: _Optional[str] = ...,
        full_name: _Optional[str] = ...,
        value: _Optional[str] = ...,
        source: _Optional[_Union[SecretSource, str]] = ...,
    ) -> None: ...

class ListSecretsRequest(_message.Message):
    __slots__ = ("include_scoped",)
    INCLUDE_SCOPED_FIELD_NUMBER: _ClassVar[int]
    include_scoped: bool
    def __init__(self, include_scoped: bool = ...) -> None: ...

class ListSecretsResponse(_message.Message):
    __slots__ = ("secrets",)
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    secrets: _containers.RepeatedCompositeFieldContainer[Secret]
    def __init__(self, secrets: _Optional[_Iterable[_Union[Secret, _Mapping]]] = ...) -> None: ...

class GetSecretValueRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSecretValueResponse(_message.Message):
    __slots__ = ("secret_value",)
    SECRET_VALUE_FIELD_NUMBER: _ClassVar[int]
    secret_value: SecretValue
    def __init__(self, secret_value: _Optional[_Union[SecretValue, _Mapping]] = ...) -> None: ...

class UpsertSecretRequest(_message.Message):
    __slots__ = ("name", "value", "config", "scope")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    config: SecretConfigValue
    scope: SecretScope
    def __init__(
        self,
        name: _Optional[str] = ...,
        value: _Optional[str] = ...,
        config: _Optional[_Union[SecretConfigValue, _Mapping]] = ...,
        scope: _Optional[_Union[SecretScope, _Mapping]] = ...,
    ) -> None: ...

class UpsertSecretResponse(_message.Message):
    __slots__ = ("secrets",)
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    secrets: _containers.RepeatedCompositeFieldContainer[Secret]
    def __init__(self, secrets: _Optional[_Iterable[_Union[Secret, _Mapping]]] = ...) -> None: ...

class DeleteSecretRequest(_message.Message):
    __slots__ = ("name", "scope")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    scope: SecretScope
    def __init__(self, name: _Optional[str] = ..., scope: _Optional[_Union[SecretScope, _Mapping]] = ...) -> None: ...

class DeleteSecretResponse(_message.Message):
    __slots__ = ("secrets",)
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    secrets: _containers.RepeatedCompositeFieldContainer[Secret]
    def __init__(self, secrets: _Optional[_Iterable[_Union[Secret, _Mapping]]] = ...) -> None: ...

class GetAllSecretValuesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllSecretValuesResponse(_message.Message):
    __slots__ = ("values",)
    class ValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.ScalarMap[str, str]
    def __init__(self, values: _Optional[_Mapping[str, str]] = ...) -> None: ...
