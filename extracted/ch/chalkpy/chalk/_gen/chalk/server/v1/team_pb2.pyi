from chalk._gen.chalk.auth.v1 import agent_pb2 as _agent_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import displayagent_pb2 as _displayagent_pb2
from chalk._gen.chalk.auth.v1 import featurepermission_pb2 as _featurepermission_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import environment_pb2 as _environment_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class GetEnvRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetEnvResponse(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: _environment_pb2.Environment
    def __init__(self, environment: _Optional[_Union[_environment_pb2.Environment, _Mapping]] = ...) -> None: ...

class GetEnvironmentsRequest(_message.Message):
    __slots__ = ("project",)
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: str
    def __init__(self, project: _Optional[str] = ...) -> None: ...

class GetEnvironmentsResponse(_message.Message):
    __slots__ = ("environments",)
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    environments: _containers.RepeatedCompositeFieldContainer[_environment_pb2.Environment]
    def __init__(
        self, environments: _Optional[_Iterable[_Union[_environment_pb2.Environment, _Mapping]]] = ...
    ) -> None: ...

class GetAgentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAgentResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: _agent_pb2.Agent
    def __init__(self, agent: _Optional[_Union[_agent_pb2.Agent, _Mapping]] = ...) -> None: ...

class GetDisplayAgentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDisplayAgentResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: _displayagent_pb2.DisplayAgent
    def __init__(self, agent: _Optional[_Union[_displayagent_pb2.DisplayAgent, _Mapping]] = ...) -> None: ...

class Team(_message.Message):
    __slots__ = ("id", "name", "slug", "logo", "projects", "scim_provider", "spec_config_json")
    class SpecConfigJsonEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    SCIM_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    SPEC_CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    slug: str
    logo: str
    projects: _containers.RepeatedCompositeFieldContainer[Project]
    scim_provider: str
    spec_config_json: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        slug: _Optional[str] = ...,
        logo: _Optional[str] = ...,
        projects: _Optional[_Iterable[_Union[Project, _Mapping]]] = ...,
        scim_provider: _Optional[str] = ...,
        spec_config_json: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class Project(_message.Message):
    __slots__ = ("id", "team_id", "name", "environments", "git_repo")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    name: str
    environments: _containers.RepeatedCompositeFieldContainer[_environment_pb2.Environment]
    git_repo: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        environments: _Optional[_Iterable[_Union[_environment_pb2.Environment, _Mapping]]] = ...,
        git_repo: _Optional[str] = ...,
    ) -> None: ...

class CreateTeamRequest(_message.Message):
    __slots__ = ("name", "slug", "logo")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    name: str
    slug: str
    logo: str
    def __init__(self, name: _Optional[str] = ..., slug: _Optional[str] = ..., logo: _Optional[str] = ...) -> None: ...

class CreateTeamResponse(_message.Message):
    __slots__ = ("team",)
    TEAM_FIELD_NUMBER: _ClassVar[int]
    team: Team
    def __init__(self, team: _Optional[_Union[Team, _Mapping]] = ...) -> None: ...

class CreateProjectRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateProjectResponse(_message.Message):
    __slots__ = ("project",)
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: Project
    def __init__(self, project: _Optional[_Union[Project, _Mapping]] = ...) -> None: ...

class CreateEnvironmentRequest(_message.Message):
    __slots__ = ("project_id", "name", "is_default")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    name: str
    is_default: bool
    def __init__(
        self, project_id: _Optional[str] = ..., name: _Optional[str] = ..., is_default: bool = ...
    ) -> None: ...

class CreateEnvironmentResponse(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: _environment_pb2.Environment
    def __init__(self, environment: _Optional[_Union[_environment_pb2.Environment, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentOperation(_message.Message):
    __slots__ = ("specs_config_json", "additional_env_vars", "private_pip_repositories")
    class AdditionalEnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    SPECS_CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_PIP_REPOSITORIES_FIELD_NUMBER: _ClassVar[int]
    specs_config_json: str
    additional_env_vars: _containers.ScalarMap[str, str]
    private_pip_repositories: str
    def __init__(
        self,
        specs_config_json: _Optional[str] = ...,
        additional_env_vars: _Optional[_Mapping[str, str]] = ...,
        private_pip_repositories: _Optional[str] = ...,
    ) -> None: ...

class UpdateEnvironmentRequest(_message.Message):
    __slots__ = ("id", "update", "update_mask")
    ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    update: UpdateEnvironmentOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        id: _Optional[str] = ...,
        update: _Optional[_Union[UpdateEnvironmentOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateEnvironmentResponse(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: _environment_pb2.Environment
    def __init__(self, environment: _Optional[_Union[_environment_pb2.Environment, _Mapping]] = ...) -> None: ...

class GetTeamRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTeamResponse(_message.Message):
    __slots__ = ("team",)
    TEAM_FIELD_NUMBER: _ClassVar[int]
    team: Team
    def __init__(self, team: _Optional[_Union[Team, _Mapping]] = ...) -> None: ...

class CreateServiceTokenRequest(_message.Message):
    __slots__ = ("name", "permissions", "custom_claims", "customer_claims", "feature_tag_to_permission")
    class FeatureTagToPermissionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _featurepermission_pb2.FeaturePermission
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[_featurepermission_pb2.FeaturePermission, str]] = ...,
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TAG_TO_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    permissions: _containers.RepeatedScalarFieldContainer[_permissions_pb2.Permission]
    custom_claims: _containers.RepeatedScalarFieldContainer[str]
    customer_claims: _containers.RepeatedCompositeFieldContainer[_agent_pb2.CustomClaim]
    feature_tag_to_permission: _containers.ScalarMap[str, _featurepermission_pb2.FeaturePermission]
    def __init__(
        self,
        name: _Optional[str] = ...,
        permissions: _Optional[_Iterable[_Union[_permissions_pb2.Permission, str]]] = ...,
        custom_claims: _Optional[_Iterable[str]] = ...,
        customer_claims: _Optional[_Iterable[_Union[_agent_pb2.CustomClaim, _Mapping]]] = ...,
        feature_tag_to_permission: _Optional[_Mapping[str, _featurepermission_pb2.FeaturePermission]] = ...,
    ) -> None: ...

class CreateServiceTokenResponse(_message.Message):
    __slots__ = ("agent", "client_secret")
    AGENT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    agent: _agent_pb2.ServiceTokenAgent
    client_secret: str
    def __init__(
        self,
        agent: _Optional[_Union[_agent_pb2.ServiceTokenAgent, _Mapping]] = ...,
        client_secret: _Optional[str] = ...,
    ) -> None: ...

class DeleteServiceTokenRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteServiceTokenResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PermissionDescription(_message.Message):
    __slots__ = ("id", "slug", "namespace", "name", "description", "group_description")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: _permissions_pb2.Permission
    slug: str
    namespace: str
    name: str
    description: str
    group_description: str
    def __init__(
        self,
        id: _Optional[_Union[_permissions_pb2.Permission, str]] = ...,
        slug: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        group_description: _Optional[str] = ...,
    ) -> None: ...

class RoleDescription(_message.Message):
    __slots__ = ("id", "name", "description", "permissions", "feature_permissions", "is_default")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    permissions: _containers.RepeatedScalarFieldContainer[_permissions_pb2.Permission]
    feature_permissions: _featurepermission_pb2.FeaturePermissions
    is_default: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        permissions: _Optional[_Iterable[_Union[_permissions_pb2.Permission, str]]] = ...,
        feature_permissions: _Optional[_Union[_featurepermission_pb2.FeaturePermissions, _Mapping]] = ...,
        is_default: bool = ...,
    ) -> None: ...

class GetAvailablePermissionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAvailablePermissionsResponse(_message.Message):
    __slots__ = ("permissions", "roles", "available_service_token_permissions")
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_SERVICE_TOKEN_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[PermissionDescription]
    roles: _containers.RepeatedCompositeFieldContainer[RoleDescription]
    available_service_token_permissions: _containers.RepeatedScalarFieldContainer[_permissions_pb2.Permission]
    def __init__(
        self,
        permissions: _Optional[_Iterable[_Union[PermissionDescription, _Mapping]]] = ...,
        roles: _Optional[_Iterable[_Union[RoleDescription, _Mapping]]] = ...,
        available_service_token_permissions: _Optional[_Iterable[_Union[_permissions_pb2.Permission, str]]] = ...,
    ) -> None: ...

class UpsertFeaturePermissionsRequest(_message.Message):
    __slots__ = ("role", "permissions")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    role: str
    permissions: _featurepermission_pb2.FeaturePermissions
    def __init__(
        self,
        role: _Optional[str] = ...,
        permissions: _Optional[_Union[_featurepermission_pb2.FeaturePermissions, _Mapping]] = ...,
    ) -> None: ...

class UpsertFeaturePermissionsResponse(_message.Message):
    __slots__ = ("role", "permissions")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    role: str
    permissions: _featurepermission_pb2.FeaturePermissions
    def __init__(
        self,
        role: _Optional[str] = ...,
        permissions: _Optional[_Union[_featurepermission_pb2.FeaturePermissions, _Mapping]] = ...,
    ) -> None: ...

class ListServiceTokensRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListServiceTokensResponse(_message.Message):
    __slots__ = ("agents",)
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    agents: _containers.RepeatedCompositeFieldContainer[_displayagent_pb2.DisplayServiceTokenAgent]
    def __init__(
        self, agents: _Optional[_Iterable[_Union[_displayagent_pb2.DisplayServiceTokenAgent, _Mapping]]] = ...
    ) -> None: ...

class UpdateServiceTokenRequest(_message.Message):
    __slots__ = ("client_id", "name", "permissions", "customer_claims", "feature_tag_to_permission")
    class FeatureTagToPermissionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _featurepermission_pb2.FeaturePermission
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[_featurepermission_pb2.FeaturePermission, str]] = ...,
        ) -> None: ...

    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TAG_TO_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    name: str
    permissions: _containers.RepeatedScalarFieldContainer[_permissions_pb2.Permission]
    customer_claims: _containers.RepeatedCompositeFieldContainer[_agent_pb2.CustomClaim]
    feature_tag_to_permission: _containers.ScalarMap[str, _featurepermission_pb2.FeaturePermission]
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        permissions: _Optional[_Iterable[_Union[_permissions_pb2.Permission, str]]] = ...,
        customer_claims: _Optional[_Iterable[_Union[_agent_pb2.CustomClaim, _Mapping]]] = ...,
        feature_tag_to_permission: _Optional[_Mapping[str, _featurepermission_pb2.FeaturePermission]] = ...,
    ) -> None: ...

class UpdateServiceTokenResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: _displayagent_pb2.DisplayServiceTokenAgent
    def __init__(
        self, agent: _Optional[_Union[_displayagent_pb2.DisplayServiceTokenAgent, _Mapping]] = ...
    ) -> None: ...

class UpdateScimGroupSettingsRequest(_message.Message):
    __slots__ = ("query_tags", "group")
    QUERY_TAGS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    query_tags: _containers.RepeatedScalarFieldContainer[str]
    group: str
    def __init__(self, query_tags: _Optional[_Iterable[str]] = ..., group: _Optional[str] = ...) -> None: ...

class UpdateScimGroupSettingsResponse(_message.Message):
    __slots__ = ("query_tags",)
    QUERY_TAGS_FIELD_NUMBER: _ClassVar[int]
    query_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, query_tags: _Optional[_Iterable[str]] = ...) -> None: ...

class InviteTeamMemberRequest(_message.Message):
    __slots__ = ("email", "role_id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    role_id: str
    def __init__(self, email: _Optional[str] = ..., role_id: _Optional[str] = ...) -> None: ...

class InviteTeamMemberResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExpireTeamInviteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ExpireTeamInviteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TeamInvite(_message.Message):
    __slots__ = ("id", "email", "team", "role", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    team: str
    role: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        email: _Optional[str] = ...,
        team: _Optional[str] = ...,
        role: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListTeamInvitesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTeamInvitesResponse(_message.Message):
    __slots__ = ("invites",)
    INVITES_FIELD_NUMBER: _ClassVar[int]
    invites: _containers.RepeatedCompositeFieldContainer[TeamInvite]
    def __init__(self, invites: _Optional[_Iterable[_Union[TeamInvite, _Mapping]]] = ...) -> None: ...

class ScimGroup(_message.Message):
    __slots__ = ("id", "display", "team_id", "members")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    display: str
    team_id: str
    members: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        display: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        members: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ScimGroupRoleAssignment(_message.Message):
    __slots__ = ("group_id", "environment_id", "role_id", "query_tags")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_TAGS_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    environment_id: str
    role_id: str
    query_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        group_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        role_id: _Optional[str] = ...,
        query_tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UserRoleAssignment(_message.Message):
    __slots__ = ("role_id", "type")
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    role_id: str
    type: str
    def __init__(self, role_id: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class UserPermissions(_message.Message):
    __slots__ = ("user_id", "environment_id", "user_roles", "user_permissions")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ROLES_FIELD_NUMBER: _ClassVar[int]
    USER_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    environment_id: str
    user_roles: _containers.RepeatedCompositeFieldContainer[UserRoleAssignment]
    user_permissions: _containers.RepeatedScalarFieldContainer[_permissions_pb2.Permission]
    def __init__(
        self,
        user_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        user_roles: _Optional[_Iterable[_Union[UserRoleAssignment, _Mapping]]] = ...,
        user_permissions: _Optional[_Iterable[_Union[_permissions_pb2.Permission, str]]] = ...,
    ) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name", "email", "image", "team_id", "deactivated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    email: str
    image: str
    team_id: str
    deactivated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        email: _Optional[str] = ...,
        image: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        deactivated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class EnvironmentPermissions(_message.Message):
    __slots__ = ("environment_id", "scim_roles", "user_permissions")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SCIM_ROLES_FIELD_NUMBER: _ClassVar[int]
    USER_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    scim_roles: _containers.RepeatedCompositeFieldContainer[ScimGroupRoleAssignment]
    user_permissions: _containers.RepeatedCompositeFieldContainer[UserPermissions]
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        scim_roles: _Optional[_Iterable[_Union[ScimGroupRoleAssignment, _Mapping]]] = ...,
        user_permissions: _Optional[_Iterable[_Union[UserPermissions, _Mapping]]] = ...,
    ) -> None: ...

class GetTeamPermissionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTeamPermissionsResponse(_message.Message):
    __slots__ = ("roles", "scim_groups", "environment_permissions", "team_members")
    ROLES_FIELD_NUMBER: _ClassVar[int]
    SCIM_GROUPS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    TEAM_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[RoleDescription]
    scim_groups: _containers.RepeatedCompositeFieldContainer[ScimGroup]
    environment_permissions: _containers.RepeatedCompositeFieldContainer[EnvironmentPermissions]
    team_members: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(
        self,
        roles: _Optional[_Iterable[_Union[RoleDescription, _Mapping]]] = ...,
        scim_groups: _Optional[_Iterable[_Union[ScimGroup, _Mapping]]] = ...,
        environment_permissions: _Optional[_Iterable[_Union[EnvironmentPermissions, _Mapping]]] = ...,
        team_members: _Optional[_Iterable[_Union[User, _Mapping]]] = ...,
    ) -> None: ...
