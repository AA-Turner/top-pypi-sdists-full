from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Secret(_message.Message):
    __slots__ = ["encrypted_value", "redacted_value", "value"]
    ENCRYPTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    REDACTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    encrypted_value: str
    redacted_value: str
    value: str
    def __init__(self, value: _Optional[str] = ..., redacted_value: _Optional[str] = ..., encrypted_value: _Optional[str] = ...) -> None: ...

class SecretReference(_message.Message):
    __slots__ = ["is_local", "key", "scope"]
    IS_LOCAL_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    is_local: bool
    key: str
    scope: str
    def __init__(self, scope: _Optional[str] = ..., key: _Optional[str] = ..., is_local: bool = ...) -> None: ...
