from union.internal.common import identifier_pb2 as _identifier_pb2
from union.internal.common import identity_pb2 as _identity_pb2
from union.internal.common import list_pb2 as _list_pb2
from union.internal.validate.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateUserRequest(_message.Message):
    __slots__ = ["spec"]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    spec: _identity_pb2.UserSpec
    def __init__(self, spec: _Optional[_Union[_identity_pb2.UserSpec, _Mapping]] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.UserIdentifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.UserIdentifier, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.UserIdentifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.UserIdentifier, _Mapping]] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ["user"]
    USER_FIELD_NUMBER: _ClassVar[int]
    user: _identity_pb2.User
    def __init__(self, user: _Optional[_Union[_identity_pb2.User, _Mapping]] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ["id", "organization"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.UserIdentifier
    organization: str
    def __init__(self, id: _Optional[_Union[_identifier_pb2.UserIdentifier, _Mapping]] = ..., organization: _Optional[str] = ...) -> None: ...

class DeleteUserResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ["organization", "role_id", "request", "include_support_staff", "exclude_identity_assignments"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SUPPORT_STAFF_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_IDENTITY_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    organization: str
    role_id: _identifier_pb2.RoleIdentifier
    request: _list_pb2.ListRequest
    include_support_staff: bool
    exclude_identity_assignments: bool
    def __init__(self, organization: _Optional[str] = ..., role_id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ..., request: _Optional[_Union[_list_pb2.ListRequest, _Mapping]] = ..., include_support_staff: bool = ..., exclude_identity_assignments: bool = ...) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ["users", "token"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[_identity_pb2.User]
    token: str
    def __init__(self, users: _Optional[_Iterable[_Union[_identity_pb2.User, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...

class ListUsersCountRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListUsersCountResponse(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class GetUserAndGroupsForOrgRequest(_message.Message):
    __slots__ = ["organization"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: str
    def __init__(self, organization: _Optional[str] = ...) -> None: ...

class GetUserAndGroupsForOrgResponse(_message.Message):
    __slots__ = ["users"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[_identity_pb2.User]
    def __init__(self, users: _Optional[_Iterable[_Union[_identity_pb2.User, _Mapping]]] = ...) -> None: ...
