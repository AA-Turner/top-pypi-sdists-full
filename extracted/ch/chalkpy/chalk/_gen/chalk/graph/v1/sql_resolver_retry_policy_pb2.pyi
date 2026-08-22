from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SQLResolverExponentialBackoff(_message.Message):
    __slots__ = ("factor", "n_retries", "base_ns")
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    N_RETRIES_FIELD_NUMBER: _ClassVar[int]
    BASE_NS_FIELD_NUMBER: _ClassVar[int]
    factor: float
    n_retries: int
    base_ns: int
    def __init__(
        self, factor: _Optional[float] = ..., n_retries: _Optional[int] = ..., base_ns: _Optional[int] = ...
    ) -> None: ...

class SQLResolverBackoff(_message.Message):
    __slots__ = ("exp",)
    EXP_FIELD_NUMBER: _ClassVar[int]
    exp: SQLResolverExponentialBackoff
    def __init__(self, exp: _Optional[_Union[SQLResolverExponentialBackoff, _Mapping]] = ...) -> None: ...

class SQLResolverRetryPolicy(_message.Message):
    __slots__ = ("if_not_found", "if_timeout")
    IF_NOT_FOUND_FIELD_NUMBER: _ClassVar[int]
    IF_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    if_not_found: SQLResolverBackoff
    if_timeout: SQLResolverBackoff
    def __init__(
        self,
        if_not_found: _Optional[_Union[SQLResolverBackoff, _Mapping]] = ...,
        if_timeout: _Optional[_Union[SQLResolverBackoff, _Mapping]] = ...,
    ) -> None: ...
