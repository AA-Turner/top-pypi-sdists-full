from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor
SERVICE_ACCOUNT_CREDENTIALS_TYPE_API_KEY: ServiceAccountCredentialsType
SERVICE_ACCOUNT_CREDENTIALS_TYPE_OAUTH_CLIENT_CREDENTIALS: ServiceAccountCredentialsType
SERVICE_ACCOUNT_CREDENTIALS_TYPE_UNSPECIFIED: ServiceAccountCredentialsType

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

class ServiceAccountCredentialsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
