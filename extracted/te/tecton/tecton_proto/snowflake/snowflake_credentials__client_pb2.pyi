from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SnowflakeCredentials(_message.Message):
    __slots__ = ["password_secret_name", "private_key_alias", "user"]
    PASSWORD_SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_ALIAS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    password_secret_name: str
    private_key_alias: str
    user: str
    def __init__(self, user: _Optional[str] = ..., password_secret_name: _Optional[str] = ..., private_key_alias: _Optional[str] = ...) -> None: ...
