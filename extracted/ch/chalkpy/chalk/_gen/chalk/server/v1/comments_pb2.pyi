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

class CommentAnchor(_message.Message):
    __slots__ = ("context", "entity_id", "sub_entity_id")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    SUB_ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    context: str
    entity_id: str
    sub_entity_id: str
    def __init__(
        self, context: _Optional[str] = ..., entity_id: _Optional[str] = ..., sub_entity_id: _Optional[str] = ...
    ) -> None: ...

class CommentReaction(_message.Message):
    __slots__ = ("emoji", "reacted_by")
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    REACTED_BY_FIELD_NUMBER: _ClassVar[int]
    emoji: str
    reacted_by: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, emoji: _Optional[str] = ..., reacted_by: _Optional[_Iterable[str]] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ("id", "anchor", "body", "created_by", "created_at", "parent_id", "resolved_at", "reactions")
    ID_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_AT_FIELD_NUMBER: _ClassVar[int]
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    anchor: CommentAnchor
    body: str
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    parent_id: str
    resolved_at: _timestamp_pb2.Timestamp
    reactions: _containers.RepeatedCompositeFieldContainer[CommentReaction]
    def __init__(
        self,
        id: _Optional[str] = ...,
        anchor: _Optional[_Union[CommentAnchor, _Mapping]] = ...,
        body: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        parent_id: _Optional[str] = ...,
        resolved_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        reactions: _Optional[_Iterable[_Union[CommentReaction, _Mapping]]] = ...,
    ) -> None: ...

class CreateCommentRequest(_message.Message):
    __slots__ = ("anchor", "body", "parent_id")
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    anchor: CommentAnchor
    body: str
    parent_id: str
    def __init__(
        self,
        anchor: _Optional[_Union[CommentAnchor, _Mapping]] = ...,
        body: _Optional[str] = ...,
        parent_id: _Optional[str] = ...,
    ) -> None: ...

class CreateCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class ListCommentsRequest(_message.Message):
    __slots__ = ("anchor",)
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    anchor: CommentAnchor
    def __init__(self, anchor: _Optional[_Union[CommentAnchor, _Mapping]] = ...) -> None: ...

class ListCommentsResponse(_message.Message):
    __slots__ = ("comments",)
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    def __init__(self, comments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ...) -> None: ...

class DeleteCommentRequest(_message.Message):
    __slots__ = ("comment_id",)
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    comment_id: str
    def __init__(self, comment_id: _Optional[str] = ...) -> None: ...

class DeleteCommentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetCommentResolvedRequest(_message.Message):
    __slots__ = ("comment_id", "resolved")
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_FIELD_NUMBER: _ClassVar[int]
    comment_id: str
    resolved: bool
    def __init__(self, comment_id: _Optional[str] = ..., resolved: bool = ...) -> None: ...

class SetCommentResolvedResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class ToggleCommentReactionRequest(_message.Message):
    __slots__ = ("comment_id", "emoji")
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    comment_id: str
    emoji: str
    def __init__(self, comment_id: _Optional[str] = ..., emoji: _Optional[str] = ...) -> None: ...

class ToggleCommentReactionResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...
