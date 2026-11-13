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

class TagFilter(_message.Message):
    __slots__ = ("tags", "match_mode")
    class MatchMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MATCH_MODE_UNSPECIFIED: _ClassVar[TagFilter.MatchMode]
        MATCH_MODE_ALL: _ClassVar[TagFilter.MatchMode]
        MATCH_MODE_ANY: _ClassVar[TagFilter.MatchMode]

    MATCH_MODE_UNSPECIFIED: TagFilter.MatchMode
    MATCH_MODE_ALL: TagFilter.MatchMode
    MATCH_MODE_ANY: TagFilter.MatchMode
    class Tag(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    TAGS_FIELD_NUMBER: _ClassVar[int]
    MATCH_MODE_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedCompositeFieldContainer[TagFilter.Tag]
    match_mode: TagFilter.MatchMode
    def __init__(
        self,
        tags: _Optional[_Iterable[_Union[TagFilter.Tag, _Mapping]]] = ...,
        match_mode: _Optional[_Union[TagFilter.MatchMode, str]] = ...,
    ) -> None: ...
