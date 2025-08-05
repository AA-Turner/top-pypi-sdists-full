from union.internal.authorizer import definition_pb2 as _definition_pb2
from union.internal.common import authorization_pb2 as _authorization_pb2
from union.internal.common import identifier_pb2 as _identifier_pb2
from union.internal.common import identity_pb2 as _identity_pb2
from union.internal.common import policy_pb2 as _policy_pb2
from union.internal.common import role_pb2 as _role_pb2
from union.internal.validate.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthorizeRequest(_message.Message):
    __slots__ = ["organization", "identity", "resource", "action"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    organization: str
    identity: _identity_pb2.Identity
    resource: _authorization_pb2.Resource
    action: _authorization_pb2.Action
    def __init__(self, organization: _Optional[str] = ..., identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ..., resource: _Optional[_Union[_authorization_pb2.Resource, _Mapping]] = ..., action: _Optional[_Union[_authorization_pb2.Action, str]] = ...) -> None: ...

class AuthorizeResponse(_message.Message):
    __slots__ = ["allowed"]
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    allowed: bool
    def __init__(self, allowed: bool = ...) -> None: ...

class CreateIdentityRequest(_message.Message):
    __slots__ = ["organization", "identity"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    organization: str
    identity: _identity_pb2.Identity
    def __init__(self, organization: _Optional[str] = ..., identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ...) -> None: ...

class CreateIdentityResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteIdentityRequest(_message.Message):
    __slots__ = ["organization", "identity"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    organization: str
    identity: _identity_pb2.Identity
    def __init__(self, organization: _Optional[str] = ..., identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ...) -> None: ...

class DeleteIdentityResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class AssignIdentityRequest(_message.Message):
    __slots__ = ["organization", "identity", "role_id", "policy_id"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    organization: str
    identity: _identity_pb2.Identity
    role_id: _identifier_pb2.RoleIdentifier
    policy_id: _identifier_pb2.PolicyIdentifier
    def __init__(self, organization: _Optional[str] = ..., identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ..., role_id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ..., policy_id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ...) -> None: ...

class AssignIdentityResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UnassignIdentityRequest(_message.Message):
    __slots__ = ["organization", "identity", "role_id", "policy_id"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    organization: str
    identity: _identity_pb2.Identity
    role_id: _identifier_pb2.RoleIdentifier
    policy_id: _identifier_pb2.PolicyIdentifier
    def __init__(self, organization: _Optional[str] = ..., identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ..., role_id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ..., policy_id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ...) -> None: ...

class UnassignIdentityResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetIdentityAssignmentRequest(_message.Message):
    __slots__ = ["identity", "organization"]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    identity: _identity_pb2.Identity
    organization: str
    def __init__(self, identity: _Optional[_Union[_identity_pb2.Identity, _Mapping]] = ..., organization: _Optional[str] = ...) -> None: ...

class GetIdentityAssignmentResponse(_message.Message):
    __slots__ = ["identity_assignment"]
    IDENTITY_ASSIGNMENT_FIELD_NUMBER: _ClassVar[int]
    identity_assignment: _definition_pb2.IdentityAssignment
    def __init__(self, identity_assignment: _Optional[_Union[_definition_pb2.IdentityAssignment, _Mapping]] = ...) -> None: ...

class ListIdentityAssignmentsRequest(_message.Message):
    __slots__ = ["organization", "identities"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    IDENTITIES_FIELD_NUMBER: _ClassVar[int]
    organization: str
    identities: _containers.RepeatedCompositeFieldContainer[_identity_pb2.Identity]
    def __init__(self, organization: _Optional[str] = ..., identities: _Optional[_Iterable[_Union[_identity_pb2.Identity, _Mapping]]] = ...) -> None: ...

class ListIdentityAssignmentsResponse(_message.Message):
    __slots__ = ["identity_assignments"]
    IDENTITY_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    identity_assignments: _containers.RepeatedCompositeFieldContainer[_definition_pb2.IdentityAssignment]
    def __init__(self, identity_assignments: _Optional[_Iterable[_Union[_definition_pb2.IdentityAssignment, _Mapping]]] = ...) -> None: ...

class GetPolicyAssignmentRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.PolicyIdentifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ...) -> None: ...

class GetPolicyAssignmentResponse(_message.Message):
    __slots__ = ["policy_assignment"]
    POLICY_ASSIGNMENT_FIELD_NUMBER: _ClassVar[int]
    policy_assignment: _definition_pb2.PolicyAssignment
    def __init__(self, policy_assignment: _Optional[_Union[_definition_pb2.PolicyAssignment, _Mapping]] = ...) -> None: ...

class CreateResourceRequest(_message.Message):
    __slots__ = ["resource"]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _authorization_pb2.Resource
    def __init__(self, resource: _Optional[_Union[_authorization_pb2.Resource, _Mapping]] = ...) -> None: ...

class CreateResourceResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteResourceRequest(_message.Message):
    __slots__ = ["resource"]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _authorization_pb2.Resource
    def __init__(self, resource: _Optional[_Union[_authorization_pb2.Resource, _Mapping]] = ...) -> None: ...

class DeleteResourceResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateOrganizationRequest(_message.Message):
    __slots__ = ["organization", "identity_assignments", "options"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    organization: str
    identity_assignments: _containers.RepeatedCompositeFieldContainer[_definition_pb2.IdentityAssignment]
    options: _definition_pb2.OrganizationOptions
    def __init__(self, organization: _Optional[str] = ..., identity_assignments: _Optional[_Iterable[_Union[_definition_pb2.IdentityAssignment, _Mapping]]] = ..., options: _Optional[_Union[_definition_pb2.OrganizationOptions, _Mapping]] = ...) -> None: ...

class CreateOrganizationResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetOrganizationRequest(_message.Message):
    __slots__ = ["organization"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: str
    def __init__(self, organization: _Optional[str] = ...) -> None: ...

class GetOrganizationResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteOrganizationRequest(_message.Message):
    __slots__ = ["organization"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: str
    def __init__(self, organization: _Optional[str] = ...) -> None: ...

class DeleteOrganizationResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreatePolicyRequest(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.Policy
    def __init__(self, policy: _Optional[_Union[_policy_pb2.Policy, _Mapping]] = ...) -> None: ...

class CreatePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.PolicyIdentifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ...) -> None: ...

class GetPolicyResponse(_message.Message):
    __slots__ = ["policy"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: _policy_pb2.Policy
    def __init__(self, policy: _Optional[_Union[_policy_pb2.Policy, _Mapping]] = ...) -> None: ...

class DeletePolicyRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.PolicyIdentifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ...) -> None: ...

class DeletePolicyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListPoliciesRequest(_message.Message):
    __slots__ = ["organization"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: str
    def __init__(self, organization: _Optional[str] = ...) -> None: ...

class ListPoliciesResponse(_message.Message):
    __slots__ = ["policies"]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[_policy_pb2.Policy]
    def __init__(self, policies: _Optional[_Iterable[_Union[_policy_pb2.Policy, _Mapping]]] = ...) -> None: ...

class CreatePolicyBindingRequest(_message.Message):
    __slots__ = ["policy_id", "binding"]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    BINDING_FIELD_NUMBER: _ClassVar[int]
    policy_id: _identifier_pb2.PolicyIdentifier
    binding: _policy_pb2.PolicyBinding
    def __init__(self, policy_id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ..., binding: _Optional[_Union[_policy_pb2.PolicyBinding, _Mapping]] = ...) -> None: ...

class CreatePolicyBindingResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeletePolicyBindingRequest(_message.Message):
    __slots__ = ["policy_id", "binding"]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    BINDING_FIELD_NUMBER: _ClassVar[int]
    policy_id: _identifier_pb2.PolicyIdentifier
    binding: _policy_pb2.PolicyBinding
    def __init__(self, policy_id: _Optional[_Union[_identifier_pb2.PolicyIdentifier, _Mapping]] = ..., binding: _Optional[_Union[_policy_pb2.PolicyBinding, _Mapping]] = ...) -> None: ...

class DeletePolicyBindingResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CreateRoleRequest(_message.Message):
    __slots__ = ["role"]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: _role_pb2.Role
    def __init__(self, role: _Optional[_Union[_role_pb2.Role, _Mapping]] = ...) -> None: ...

class CreateRoleResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetRoleRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.RoleIdentifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ...) -> None: ...

class GetRoleResponse(_message.Message):
    __slots__ = ["role"]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: _role_pb2.Role
    def __init__(self, role: _Optional[_Union[_role_pb2.Role, _Mapping]] = ...) -> None: ...

class DeleteRoleRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.RoleIdentifier
    def __init__(self, id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ...) -> None: ...

class DeleteRoleResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListRolesRequest(_message.Message):
    __slots__ = ["organization"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: str
    def __init__(self, organization: _Optional[str] = ...) -> None: ...

class ListRolesResponse(_message.Message):
    __slots__ = ["roles"]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[_role_pb2.Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[_role_pb2.Role, _Mapping]]] = ...) -> None: ...

class CreateRoleActionRequest(_message.Message):
    __slots__ = ["id", "action"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.RoleIdentifier
    action: _authorization_pb2.Action
    def __init__(self, id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ..., action: _Optional[_Union[_authorization_pb2.Action, str]] = ...) -> None: ...

class CreateRoleActionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteRoleActionRequest(_message.Message):
    __slots__ = ["id", "action"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    id: _identifier_pb2.RoleIdentifier
    action: _authorization_pb2.Action
    def __init__(self, id: _Optional[_Union[_identifier_pb2.RoleIdentifier, _Mapping]] = ..., action: _Optional[_Union[_authorization_pb2.Action, str]] = ...) -> None: ...

class DeleteRoleActionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
