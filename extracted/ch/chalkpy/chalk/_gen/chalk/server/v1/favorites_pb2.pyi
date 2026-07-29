from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
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

class Favorite(_message.Message):
    __slots__ = ("context", "entity_id", "created_at")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    context: str
    entity_id: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        context: _Optional[str] = ...,
        entity_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SetFavoriteRequest(_message.Message):
    __slots__ = ("context", "entity_id", "favorite")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_FIELD_NUMBER: _ClassVar[int]
    context: str
    entity_id: str
    favorite: bool
    def __init__(
        self, context: _Optional[str] = ..., entity_id: _Optional[str] = ..., favorite: bool = ...
    ) -> None: ...

class SetFavoriteResponse(_message.Message):
    __slots__ = ("favorite",)
    FAVORITE_FIELD_NUMBER: _ClassVar[int]
    favorite: bool
    def __init__(self, favorite: bool = ...) -> None: ...

class ListFavoritesRequest(_message.Message):
    __slots__ = ("context",)
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    context: str
    def __init__(self, context: _Optional[str] = ...) -> None: ...

class ListFavoritesResponse(_message.Message):
    __slots__ = ("favorites",)
    FAVORITES_FIELD_NUMBER: _ClassVar[int]
    favorites: _containers.RepeatedCompositeFieldContainer[Favorite]
    def __init__(self, favorites: _Optional[_Iterable[_Union[Favorite, _Mapping]]] = ...) -> None: ...
