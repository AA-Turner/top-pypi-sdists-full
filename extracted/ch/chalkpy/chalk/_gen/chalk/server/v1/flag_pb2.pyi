from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class FlagScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FLAG_SCOPE_UNSPECIFIED: _ClassVar[FlagScope]
    FLAG_SCOPE_TEAM: _ClassVar[FlagScope]
    FLAG_SCOPE_ENVIRONMENT: _ClassVar[FlagScope]

FLAG_SCOPE_UNSPECIFIED: FlagScope
FLAG_SCOPE_TEAM: FlagScope
FLAG_SCOPE_ENVIRONMENT: FlagScope

class FeatureFlagValue(_message.Message):
    __slots__ = ("flag", "value")
    FLAG_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    flag: str
    value: bool
    def __init__(self, flag: _Optional[str] = ..., value: bool = ...) -> None: ...

class GetFeatureFlagsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetFeatureFlagsResponse(_message.Message):
    __slots__ = ("flags",)
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: _containers.RepeatedCompositeFieldContainer[FeatureFlagValue]
    def __init__(self, flags: _Optional[_Iterable[_Union[FeatureFlagValue, _Mapping]]] = ...) -> None: ...

class SetFeatureFlagRequest(_message.Message):
    __slots__ = ("flag", "value", "scope")
    FLAG_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    flag: str
    value: bool
    scope: FlagScope
    def __init__(
        self, flag: _Optional[str] = ..., value: bool = ..., scope: _Optional[_Union[FlagScope, str]] = ...
    ) -> None: ...

class SetFeatureFlagResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
