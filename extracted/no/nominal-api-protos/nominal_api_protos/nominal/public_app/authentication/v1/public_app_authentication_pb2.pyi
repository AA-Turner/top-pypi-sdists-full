from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PublicAppAuthenticationError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUBLIC_APP_AUTHENTICATION_ERROR_UNSPECIFIED: _ClassVar[PublicAppAuthenticationError]
    PUBLIC_APP_AUTHENTICATION_ERROR_NOT_SUPPORTED: _ClassVar[PublicAppAuthenticationError]
    PUBLIC_APP_AUTHENTICATION_ERROR_UNAUTHENTICATED: _ClassVar[PublicAppAuthenticationError]
    PUBLIC_APP_AUTHENTICATION_ERROR_EXPIRED: _ClassVar[PublicAppAuthenticationError]
    PUBLIC_APP_AUTHENTICATION_ERROR_UNKNOWN_CLIENT: _ClassVar[PublicAppAuthenticationError]
    PUBLIC_APP_AUTHENTICATION_ERROR_UNKNOWN_REDIRECT_URI: _ClassVar[PublicAppAuthenticationError]
    PUBLIC_APP_AUTHENTICATION_ERROR_INVALID_GRANT: _ClassVar[PublicAppAuthenticationError]
    PUBLIC_APP_AUTHENTICATION_ERROR_INVALID_CLIENT_CREDENTIALS: _ClassVar[PublicAppAuthenticationError]
PUBLIC_APP_AUTHENTICATION_ERROR_UNSPECIFIED: PublicAppAuthenticationError
PUBLIC_APP_AUTHENTICATION_ERROR_NOT_SUPPORTED: PublicAppAuthenticationError
PUBLIC_APP_AUTHENTICATION_ERROR_UNAUTHENTICATED: PublicAppAuthenticationError
PUBLIC_APP_AUTHENTICATION_ERROR_EXPIRED: PublicAppAuthenticationError
PUBLIC_APP_AUTHENTICATION_ERROR_UNKNOWN_CLIENT: PublicAppAuthenticationError
PUBLIC_APP_AUTHENTICATION_ERROR_UNKNOWN_REDIRECT_URI: PublicAppAuthenticationError
PUBLIC_APP_AUTHENTICATION_ERROR_INVALID_GRANT: PublicAppAuthenticationError
PUBLIC_APP_AUTHENTICATION_ERROR_INVALID_CLIENT_CREDENTIALS: PublicAppAuthenticationError

class HealthCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("will_expire",)
    WILL_EXPIRE_FIELD_NUMBER: _ClassVar[int]
    will_expire: bool
    def __init__(self, will_expire: bool = ...) -> None: ...

class GetOidcInitRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOidcInitResponse(_message.Message):
    __slots__ = ("client_id", "login_url", "redirect_uris")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOGIN_URL_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    login_url: str
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, client_id: _Optional[str] = ..., login_url: _Optional[str] = ..., redirect_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class ExchangeAuthorizationCodeRequest(_message.Message):
    __slots__ = ("client_id", "code", "redirect_uri", "code_verifier")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    CODE_VERIFIER_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    code: str
    redirect_uri: str
    code_verifier: str
    def __init__(self, client_id: _Optional[str] = ..., code: _Optional[str] = ..., redirect_uri: _Optional[str] = ..., code_verifier: _Optional[str] = ...) -> None: ...

class ExchangeAuthorizationCodeResponse(_message.Message):
    __slots__ = ("id_token", "expires_in", "scope")
    ID_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    id_token: str
    expires_in: int
    scope: str
    def __init__(self, id_token: _Optional[str] = ..., expires_in: _Optional[int] = ..., scope: _Optional[str] = ...) -> None: ...
