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

class ContentVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTENT_VISIBILITY_UNSPECIFIED: _ClassVar[ContentVisibility]
    CONTENT_VISIBILITY_ENVIRONMENT: _ClassVar[ContentVisibility]
    CONTENT_VISIBILITY_RESTRICTED: _ClassVar[ContentVisibility]

class ContentRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTENT_ROLE_UNSPECIFIED: _ClassVar[ContentRole]
    CONTENT_ROLE_VIEWER: _ClassVar[ContentRole]
    CONTENT_ROLE_EDITOR: _ClassVar[ContentRole]
    CONTENT_ROLE_OWNER: _ClassVar[ContentRole]

CONTENT_VISIBILITY_UNSPECIFIED: ContentVisibility
CONTENT_VISIBILITY_ENVIRONMENT: ContentVisibility
CONTENT_VISIBILITY_RESTRICTED: ContentVisibility
CONTENT_ROLE_UNSPECIFIED: ContentRole
CONTENT_ROLE_VIEWER: ContentRole
CONTENT_ROLE_EDITOR: ContentRole
CONTENT_ROLE_OWNER: ContentRole

class ContentGrant(_message.Message):
    __slots__ = ("user_id", "role")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    role: ContentRole
    def __init__(self, user_id: _Optional[str] = ..., role: _Optional[_Union[ContentRole, str]] = ...) -> None: ...

class ContentGrantList(_message.Message):
    __slots__ = ("grants",)
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    grants: _containers.RepeatedCompositeFieldContainer[ContentGrant]
    def __init__(self, grants: _Optional[_Iterable[_Union[ContentGrant, _Mapping]]] = ...) -> None: ...

class ContentSharing(_message.Message):
    __slots__ = ("visibility", "grants")
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    visibility: ContentVisibility
    grants: _containers.RepeatedCompositeFieldContainer[ContentGrant]
    def __init__(
        self,
        visibility: _Optional[_Union[ContentVisibility, str]] = ...,
        grants: _Optional[_Iterable[_Union[ContentGrant, _Mapping]]] = ...,
    ) -> None: ...
