from union.internal.common import deployment_pb2 as _deployment_pb2
from union.internal.common import identifier_pb2 as _identifier_pb2
from union.internal.common import identity_pb2 as _identity_pb2
from union.internal.common import policy_pb2 as _policy_pb2
from union.internal.common import role_pb2 as _role_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthorizationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TYPE_UNSPECIFIED: _ClassVar[AuthorizationType]
    TYPE_DEPRECATED_ROLE: _ClassVar[AuthorizationType]
    TYPE_POLICY: _ClassVar[AuthorizationType]
TYPE_UNSPECIFIED: AuthorizationType
TYPE_DEPRECATED_ROLE: AuthorizationType
TYPE_POLICY: AuthorizationType

class RoleAssignment(_message.Message):
    __slots__ = ["role_id", "identities"]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITIES_FIELD_NUMBER: _ClassVar[int]
    role_id: _identifier_pb2.RoleIdentifier
    identities: _containers.RepeatedCompositeFieldContainer[_identity_pb2.Identity]
    def __init__(self, role_id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ..., identities: _Optional[_Iterable[_Union[_identity_pb2.Identity, _Mapping]]] = ...) -> None: ...

class PolicyAssignment(_message.Message):
    __slots__ = ["policy_id", "identities"]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITIES_FIELD_NUMBER: _ClassVar[int]
    policy_id: _identifier_pb2.PolicyIdentifier
    identities: _containers.RepeatedCompositeFieldContainer[_identity_pb2.Identity]
    def __init__(self, policy_id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ..., identities: _Optional[_Iterable[_Union[_identity_pb2.Identity, _Mapping]]] = ...) -> None: ...

class IdentityAssignment(_message.Message):
    __slots__ = ["identity", "roles", "policies"]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    identity: _identity_pb2.Identity
    roles: _containers.RepeatedCompositeFieldContainer[_role_pb2.Role]
    policies: _containers.RepeatedCompositeFieldContainer[_policy_pb2.Policy]
    def __init__(self, identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ..., roles: _Optional[_Iterable[_Union[_role_pb2.Role, _Mapping]]] = ..., policies: _Optional[_Iterable[_Union[_policy_pb2.Policy, _Mapping]]] = ...) -> None: ...

class OrganizationOptions(_message.Message):
    __slots__ = ["authorization_type", "parent", "deployment"]
    AUTHORIZATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    authorization_type: AuthorizationType
    parent: str
    deployment: _deployment_pb2.Deployment
    def __init__(self, authorization_type: _Optional[_Union[AuthorizationType, str]] = ..., parent: _Optional[str] = ..., deployment: _Optional[_Union[_deployment_pb2.Deployment, str]] = ...) -> None: ...
