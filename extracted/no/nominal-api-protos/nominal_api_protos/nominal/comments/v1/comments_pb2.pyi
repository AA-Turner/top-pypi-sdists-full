import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.conjure.v1 import compat_pb2 as _compat_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReactionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REACTION_TYPE_UNSPECIFIED: _ClassVar[ReactionType]
    LIKE: _ClassVar[ReactionType]
    DISLIKE: _ClassVar[ReactionType]
    HEART: _ClassVar[ReactionType]
    HOORAY: _ClassVar[ReactionType]
    ROCKET: _ClassVar[ReactionType]
    EYES: _ClassVar[ReactionType]

class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOURCE_TYPE_UNSPECIFIED: _ClassVar[ResourceType]
    RUN: _ClassVar[ResourceType]
    EVENT: _ClassVar[ResourceType]

class CommentsError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMMENTS_ERROR_COMMENT_NOT_FOUND: _ClassVar[CommentsError]
    COMMENTS_ERROR_CONTENT_TOO_LONG: _ClassVar[CommentsError]
    COMMENTS_ERROR_EMPTY_COMMENT_CONTENT: _ClassVar[CommentsError]
    COMMENTS_ERROR_INVALID_ATTACHMENT: _ClassVar[CommentsError]
    COMMENTS_ERROR_MAX_NESTING_DEPTH_EXCEEDED: _ClassVar[CommentsError]
    COMMENTS_ERROR_UNAUTHORIZED: _ClassVar[CommentsError]
REACTION_TYPE_UNSPECIFIED: ReactionType
LIKE: ReactionType
DISLIKE: ReactionType
HEART: ReactionType
HOORAY: ReactionType
ROCKET: ReactionType
EYES: ReactionType
RESOURCE_TYPE_UNSPECIFIED: ResourceType
RUN: ResourceType
EVENT: ResourceType
COMMENTS_ERROR_COMMENT_NOT_FOUND: CommentsError
COMMENTS_ERROR_CONTENT_TOO_LONG: CommentsError
COMMENTS_ERROR_EMPTY_COMMENT_CONTENT: CommentsError
COMMENTS_ERROR_INVALID_ATTACHMENT: CommentsError
COMMENTS_ERROR_MAX_NESTING_DEPTH_EXCEEDED: CommentsError
COMMENTS_ERROR_UNAUTHORIZED: CommentsError

class Comment(_message.Message):
    __slots__ = ("rid", "parent", "author_rid", "created_at", "edited_at", "deleted_at", "content", "pinned_by", "pinned_at", "reactions", "attachments")
    RID_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_RID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EDITED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PINNED_BY_FIELD_NUMBER: _ClassVar[int]
    PINNED_AT_FIELD_NUMBER: _ClassVar[int]
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    rid: str
    parent: CommentParent
    author_rid: str
    created_at: _timestamp_pb2.Timestamp
    edited_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    content: str
    pinned_by: str
    pinned_at: _timestamp_pb2.Timestamp
    reactions: _containers.RepeatedCompositeFieldContainer[Reaction]
    attachments: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, rid: _Optional[str] = ..., parent: _Optional[_Union[CommentParent, _Mapping]] = ..., author_rid: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., edited_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., content: _Optional[str] = ..., pinned_by: _Optional[str] = ..., pinned_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., reactions: _Optional[_Iterable[_Union[Reaction, _Mapping]]] = ..., attachments: _Optional[_Iterable[str]] = ...) -> None: ...

class CommentParent(_message.Message):
    __slots__ = ("resource", "comment")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    resource: CommentParentResource
    comment: CommentParentComment
    def __init__(self, resource: _Optional[_Union[CommentParentResource, _Mapping]] = ..., comment: _Optional[_Union[CommentParentComment, _Mapping]] = ...) -> None: ...

class CommentParentComment(_message.Message):
    __slots__ = ("comment_rid",)
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    def __init__(self, comment_rid: _Optional[str] = ...) -> None: ...

class CommentParentResource(_message.Message):
    __slots__ = ("resource_type", "resource_rid")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    resource_type: ResourceType
    resource_rid: str
    def __init__(self, resource_type: _Optional[_Union[ResourceType, str]] = ..., resource_rid: _Optional[str] = ...) -> None: ...

class Conversation(_message.Message):
    __slots__ = ("resource_rid", "resource_type", "comments")
    RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    resource_rid: str
    resource_type: ResourceType
    comments: _containers.RepeatedCompositeFieldContainer[ConversationNode]
    def __init__(self, resource_rid: _Optional[str] = ..., resource_type: _Optional[_Union[ResourceType, str]] = ..., comments: _Optional[_Iterable[_Union[ConversationNode, _Mapping]]] = ...) -> None: ...

class ConversationNode(_message.Message):
    __slots__ = ("comment", "replies")
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    replies: _containers.RepeatedCompositeFieldContainer[ConversationNode]
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ..., replies: _Optional[_Iterable[_Union[ConversationNode, _Mapping]]] = ...) -> None: ...

class CreateCommentRequest(_message.Message):
    __slots__ = ("parent", "content", "attachments")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    parent: CommentParent
    content: str
    attachments: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, parent: _Optional[_Union[CommentParent, _Mapping]] = ..., content: _Optional[str] = ..., attachments: _Optional[_Iterable[str]] = ...) -> None: ...

class EditCommentRequest(_message.Message):
    __slots__ = ("content", "attachments")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    content: str
    attachments: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, content: _Optional[str] = ..., attachments: _Optional[_Iterable[str]] = ...) -> None: ...

class Reaction(_message.Message):
    __slots__ = ("rid", "user_rid", "created_at", "type")
    RID_FIELD_NUMBER: _ClassVar[int]
    USER_RID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    user_rid: str
    created_at: _timestamp_pb2.Timestamp
    type: ReactionType
    def __init__(self, rid: _Optional[str] = ..., user_rid: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., type: _Optional[_Union[ReactionType, str]] = ...) -> None: ...

class GetConversationRequest(_message.Message):
    __slots__ = ("resource_type", "resource_rid")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    resource_type: ResourceType
    resource_rid: str
    def __init__(self, resource_type: _Optional[_Union[ResourceType, str]] = ..., resource_rid: _Optional[str] = ...) -> None: ...

class GetConversationResponse(_message.Message):
    __slots__ = ("conversation",)
    CONVERSATION_FIELD_NUMBER: _ClassVar[int]
    conversation: Conversation
    def __init__(self, conversation: _Optional[_Union[Conversation, _Mapping]] = ...) -> None: ...

class GetConversationCountRequest(_message.Message):
    __slots__ = ("resource_type", "resource_rid", "include_deleted")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    resource_type: ResourceType
    resource_rid: str
    include_deleted: bool
    def __init__(self, resource_type: _Optional[_Union[ResourceType, str]] = ..., resource_rid: _Optional[str] = ..., include_deleted: bool = ...) -> None: ...

class GetConversationCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class GetCommentRequest(_message.Message):
    __slots__ = ("comment_rid",)
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    def __init__(self, comment_rid: _Optional[str] = ...) -> None: ...

class GetCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class CreateCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class EditCommentRequestWrapper(_message.Message):
    __slots__ = ("comment_rid", "request")
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    request: EditCommentRequest
    def __init__(self, comment_rid: _Optional[str] = ..., request: _Optional[_Union[EditCommentRequest, _Mapping]] = ...) -> None: ...

class EditCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class DeleteCommentRequest(_message.Message):
    __slots__ = ("comment_rid",)
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    def __init__(self, comment_rid: _Optional[str] = ...) -> None: ...

class DeleteCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class PinCommentRequest(_message.Message):
    __slots__ = ("comment_rid",)
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    def __init__(self, comment_rid: _Optional[str] = ...) -> None: ...

class PinCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class UnpinCommentRequest(_message.Message):
    __slots__ = ("comment_rid",)
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    def __init__(self, comment_rid: _Optional[str] = ...) -> None: ...

class UnpinCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class AddReactionRequest(_message.Message):
    __slots__ = ("comment_rid", "type")
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    type: ReactionType
    def __init__(self, comment_rid: _Optional[str] = ..., type: _Optional[_Union[ReactionType, str]] = ...) -> None: ...

class AddReactionResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class RemoveReactionRequest(_message.Message):
    __slots__ = ("comment_rid", "type")
    COMMENT_RID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    comment_rid: str
    type: ReactionType
    def __init__(self, comment_rid: _Optional[str] = ..., type: _Optional[_Union[ReactionType, str]] = ...) -> None: ...

class RemoveReactionResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...
