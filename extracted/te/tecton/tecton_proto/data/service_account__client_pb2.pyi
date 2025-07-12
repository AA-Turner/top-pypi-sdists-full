from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
SERVICE_ACCOUNT_CREDENTIALS_TYPE_API_KEY: ServiceAccountCredentialsType
SERVICE_ACCOUNT_CREDENTIALS_TYPE_OAUTH_CLIENT_CREDENTIALS: ServiceAccountCredentialsType
SERVICE_ACCOUNT_CREDENTIALS_TYPE_UNSPECIFIED: ServiceAccountCredentialsType

class CreateServiceAccountRequest(_message.Message):
    __slots__ = ["credentials_type", "description", "name"]
    CREDENTIALS_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    credentials_type: ServiceAccountCredentialsType
    description: str
    name: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., credentials_type: _Optional[_Union[ServiceAccountCredentialsType, str]] = ...) -> None: ...

class CreateServiceAccountResponse(_message.Message):
    __slots__ = ["api_key", "client_secret", "created_at", "credentials_type", "description", "id", "is_active", "name"]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    client_secret: str
    created_at: _timestamp_pb2.Timestamp
    credentials_type: ServiceAccountCredentialsType
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., api_key: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., credentials_type: _Optional[_Union[ServiceAccountCredentialsType, str]] = ..., client_secret: _Optional[str] = ...) -> None: ...

class DeleteServiceAccountRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteServiceAccountResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetServiceAccountsRequest(_message.Message):
    __slots__ = ["ids", "search"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    search: str
    def __init__(self, search: _Optional[str] = ..., ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetServiceAccountsResponse(_message.Message):
    __slots__ = ["service_accounts"]
    SERVICE_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    service_accounts: _containers.RepeatedCompositeFieldContainer[ServiceAccount]
    def __init__(self, service_accounts: _Optional[_Iterable[_Union[ServiceAccount, _Mapping]]] = ...) -> None: ...

class MaskedClientSecret(_message.Message):
    __slots__ = ["created_at", "masked_secret", "secret_id", "status", "updated_at"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MASKED_SECRET_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    created_at: str
    masked_secret: str
    secret_id: str
    status: str
    updated_at: str
    def __init__(self, secret_id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., status: _Optional[str] = ..., masked_secret: _Optional[str] = ...) -> None: ...

class NewClientSecret(_message.Message):
    __slots__ = ["created_at", "secret", "secret_id", "status"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    created_at: str
    secret: str
    secret_id: str
    status: str
    def __init__(self, secret_id: _Optional[str] = ..., created_at: _Optional[str] = ..., status: _Optional[str] = ..., secret: _Optional[str] = ...) -> None: ...

class ServiceAccount(_message.Message):
    __slots__ = ["created_at", "created_by", "credentials_type", "description", "id", "is_active", "name"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    created_by: _principal__client_pb2.PrincipalBasic
    credentials_type: ServiceAccountCredentialsType
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., created_by: _Optional[_Union[_principal__client_pb2.PrincipalBasic, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., credentials_type: _Optional[_Union[ServiceAccountCredentialsType, str]] = ...) -> None: ...

class UpdateServiceAccountRequest(_message.Message):
    __slots__ = ["description", "id", "is_active", "name"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ...) -> None: ...

class UpdateServiceAccountResponse(_message.Message):
    __slots__ = ["created_at", "description", "id", "is_active", "name"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    description: str
    id: str
    is_active: bool
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ServiceAccountCredentialsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
