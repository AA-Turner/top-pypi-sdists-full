from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLE_UNSPECIFIED: _ClassVar[Role]
    ROLE_ORG_ADMIN: _ClassVar[Role]
    ROLE_ORG_USER: _ClassVar[Role]
ROLE_UNSPECIFIED: Role
ROLE_ORG_ADMIN: Role
ROLE_ORG_USER: Role

class Org(_message.Message):
    __slots__ = ("name", "id", "created_at", "modified_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    created_at: _timestamp_pb2.Timestamp
    modified_at: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., modified_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "org_name", "email", "roles")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_name: str
    email: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., org_name: _Optional[str] = ..., email: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateOrgRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateOrgResponse(_message.Message):
    __slots__ = ("org",)
    ORG_FIELD_NUMBER: _ClassVar[int]
    org: Org
    def __init__(self, org: _Optional[_Union[Org, _Mapping]] = ...) -> None: ...

class GetOrgRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetOrgResponse(_message.Message):
    __slots__ = ("org",)
    ORG_FIELD_NUMBER: _ClassVar[int]
    org: Org
    def __init__(self, org: _Optional[_Union[Org, _Mapping]] = ...) -> None: ...

class ListOrgsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOrgsResponse(_message.Message):
    __slots__ = ("orgs",)
    ORGS_FIELD_NUMBER: _ClassVar[int]
    orgs: _containers.RepeatedCompositeFieldContainer[Org]
    def __init__(self, orgs: _Optional[_Iterable[_Union[Org, _Mapping]]] = ...) -> None: ...

class ListOrgUsersRequest(_message.Message):
    __slots__ = ("org_name",)
    ORG_NAME_FIELD_NUMBER: _ClassVar[int]
    org_name: str
    def __init__(self, org_name: _Optional[str] = ...) -> None: ...

class ListOrgUsersResponse(_message.Message):
    __slots__ = ("users",)
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class AddOrgUserRequest(_message.Message):
    __slots__ = ("email", "org_name", "roles")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ORG_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    email: str
    org_name: str
    roles: _containers.RepeatedScalarFieldContainer[Role]
    def __init__(self, email: _Optional[str] = ..., org_name: _Optional[str] = ..., roles: _Optional[_Iterable[_Union[Role, str]]] = ...) -> None: ...

class AddOrgUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetOrgUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetOrgUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class DeactivateOrgUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeactivateOrgUserResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
