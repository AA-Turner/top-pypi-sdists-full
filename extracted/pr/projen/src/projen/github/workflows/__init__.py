from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ..._jsii import *

from ... import GroupRunnerOptions as _GroupRunnerOptions_148c59c1


@jsii.enum(jsii_type="projen.github.workflows.AppPermission")
class AppPermission(enum.Enum):
    '''(experimental) The permissions available for an access token for a GitHub App.

    :stability: experimental
    '''

    READ = "READ"
    '''(experimental) Read-only acccess.

    :stability: experimental
    '''
    WRITE = "WRITE"
    '''(experimental) Read-write access.

    :stability: experimental
    '''
    ADMIN = "ADMIN"
    '''(experimental) Read-write and admin access.

    Not all permissions support ``admin``.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.github.workflows.AppPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "administration": "administration",
        "attestations": "attestations",
        "checks": "checks",
        "codespaces": "codespaces",
        "contents": "contents",
        "dependabot_secrets": "dependabotSecrets",
        "deployments": "deployments",
        "email_addresses": "emailAddresses",
        "environments": "environments",
        "followers": "followers",
        "git_ssh_keys": "gitSshKeys",
        "gpg_keys": "gpgKeys",
        "interaction_limits": "interactionLimits",
        "issues": "issues",
        "members": "members",
        "metadata": "metadata",
        "organization_administration": "organizationAdministration",
        "organization_announcement_banners": "organizationAnnouncementBanners",
        "organization_copilot_seat_management": "organizationCopilotSeatManagement",
        "organization_custom_org_roles": "organizationCustomOrgRoles",
        "organization_custom_properties": "organizationCustomProperties",
        "organization_custom_roles": "organizationCustomRoles",
        "organization_events": "organizationEvents",
        "organization_hooks": "organizationHooks",
        "organization_packages": "organizationPackages",
        "organization_personal_access_token_requests": "organizationPersonalAccessTokenRequests",
        "organization_personal_access_tokens": "organizationPersonalAccessTokens",
        "organization_plan": "organizationPlan",
        "organization_projects": "organizationProjects",
        "organization_secrets": "organizationSecrets",
        "organization_self_hosted_runners": "organizationSelfHostedRunners",
        "orgnaization_user_blocking": "orgnaizationUserBlocking",
        "packages": "packages",
        "pages": "pages",
        "profile": "profile",
        "pull_requests": "pullRequests",
        "repository_announcement_banners": "repositoryAnnouncementBanners",
        "repository_custom_properties": "repositoryCustomProperties",
        "repository_hooks": "repositoryHooks",
        "repository_projects": "repositoryProjects",
        "secrets": "secrets",
        "secret_scanning_alerts": "secretScanningAlerts",
        "security_events": "securityEvents",
        "single_file": "singleFile",
        "starring": "starring",
        "statuses": "statuses",
        "team_discussions": "teamDiscussions",
        "vulnerability_alerts": "vulnerabilityAlerts",
        "workflows": "workflows",
    },
)
class AppPermissions:
    def __init__(
        self,
        *,
        actions: typing.Optional[AppPermission] = None,
        administration: typing.Optional[AppPermission] = None,
        attestations: typing.Optional[AppPermission] = None,
        checks: typing.Optional[AppPermission] = None,
        codespaces: typing.Optional[AppPermission] = None,
        contents: typing.Optional[AppPermission] = None,
        dependabot_secrets: typing.Optional[AppPermission] = None,
        deployments: typing.Optional[AppPermission] = None,
        email_addresses: typing.Optional[AppPermission] = None,
        environments: typing.Optional[AppPermission] = None,
        followers: typing.Optional[AppPermission] = None,
        git_ssh_keys: typing.Optional[AppPermission] = None,
        gpg_keys: typing.Optional[AppPermission] = None,
        interaction_limits: typing.Optional[AppPermission] = None,
        issues: typing.Optional[AppPermission] = None,
        members: typing.Optional[AppPermission] = None,
        metadata: typing.Optional[AppPermission] = None,
        organization_administration: typing.Optional[AppPermission] = None,
        organization_announcement_banners: typing.Optional[AppPermission] = None,
        organization_copilot_seat_management: typing.Optional[AppPermission] = None,
        organization_custom_org_roles: typing.Optional[AppPermission] = None,
        organization_custom_properties: typing.Optional[AppPermission] = None,
        organization_custom_roles: typing.Optional[AppPermission] = None,
        organization_events: typing.Optional[AppPermission] = None,
        organization_hooks: typing.Optional[AppPermission] = None,
        organization_packages: typing.Optional[AppPermission] = None,
        organization_personal_access_token_requests: typing.Optional[AppPermission] = None,
        organization_personal_access_tokens: typing.Optional[AppPermission] = None,
        organization_plan: typing.Optional[AppPermission] = None,
        organization_projects: typing.Optional[AppPermission] = None,
        organization_secrets: typing.Optional[AppPermission] = None,
        organization_self_hosted_runners: typing.Optional[AppPermission] = None,
        orgnaization_user_blocking: typing.Optional[AppPermission] = None,
        packages: typing.Optional[AppPermission] = None,
        pages: typing.Optional[AppPermission] = None,
        profile: typing.Optional[AppPermission] = None,
        pull_requests: typing.Optional[AppPermission] = None,
        repository_announcement_banners: typing.Optional[AppPermission] = None,
        repository_custom_properties: typing.Optional[AppPermission] = None,
        repository_hooks: typing.Optional[AppPermission] = None,
        repository_projects: typing.Optional[AppPermission] = None,
        secrets: typing.Optional[AppPermission] = None,
        secret_scanning_alerts: typing.Optional[AppPermission] = None,
        security_events: typing.Optional[AppPermission] = None,
        single_file: typing.Optional[AppPermission] = None,
        starring: typing.Optional[AppPermission] = None,
        statuses: typing.Optional[AppPermission] = None,
        team_discussions: typing.Optional[AppPermission] = None,
        vulnerability_alerts: typing.Optional[AppPermission] = None,
        workflows: typing.Optional[AppPermission] = None,
    ) -> None:
        '''(experimental) The permissions available to a GitHub App.

        Typically a token for a GitHub App has all the available scopes/permissions available to the app
        itself; however, a more limited set of permissions can be specified. When permissions are provided,
        **only** the specified permissions are granted to the token.

        :param actions: 
        :param administration: 
        :param attestations: 
        :param checks: 
        :param codespaces: 
        :param contents: 
        :param dependabot_secrets: 
        :param deployments: 
        :param email_addresses: 
        :param environments: 
        :param followers: 
        :param git_ssh_keys: 
        :param gpg_keys: 
        :param interaction_limits: 
        :param issues: 
        :param members: 
        :param metadata: 
        :param organization_administration: 
        :param organization_announcement_banners: 
        :param organization_copilot_seat_management: 
        :param organization_custom_org_roles: 
        :param organization_custom_properties: 
        :param organization_custom_roles: 
        :param organization_events: 
        :param organization_hooks: 
        :param organization_packages: 
        :param organization_personal_access_token_requests: 
        :param organization_personal_access_tokens: 
        :param organization_plan: 
        :param organization_projects: 
        :param organization_secrets: 
        :param organization_self_hosted_runners: 
        :param orgnaization_user_blocking: 
        :param packages: 
        :param pages: 
        :param profile: 
        :param pull_requests: 
        :param repository_announcement_banners: 
        :param repository_custom_properties: 
        :param repository_hooks: 
        :param repository_projects: 
        :param secrets: 
        :param secret_scanning_alerts: 
        :param security_events: 
        :param single_file: 
        :param starring: 
        :param statuses: 
        :param team_discussions: 
        :param vulnerability_alerts: 
        :param workflows: 

        :see: https://github.com/actions/create-github-app-token/blob/main/action.yml#L28
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0085e134a87f8de8cb54bc56e329333881c3520710c833f5ed76097c8d1299)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument administration", value=administration, expected_type=type_hints["administration"])
            check_type(argname="argument attestations", value=attestations, expected_type=type_hints["attestations"])
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument codespaces", value=codespaces, expected_type=type_hints["codespaces"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument dependabot_secrets", value=dependabot_secrets, expected_type=type_hints["dependabot_secrets"])
            check_type(argname="argument deployments", value=deployments, expected_type=type_hints["deployments"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
            check_type(argname="argument followers", value=followers, expected_type=type_hints["followers"])
            check_type(argname="argument git_ssh_keys", value=git_ssh_keys, expected_type=type_hints["git_ssh_keys"])
            check_type(argname="argument gpg_keys", value=gpg_keys, expected_type=type_hints["gpg_keys"])
            check_type(argname="argument interaction_limits", value=interaction_limits, expected_type=type_hints["interaction_limits"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument organization_administration", value=organization_administration, expected_type=type_hints["organization_administration"])
            check_type(argname="argument organization_announcement_banners", value=organization_announcement_banners, expected_type=type_hints["organization_announcement_banners"])
            check_type(argname="argument organization_copilot_seat_management", value=organization_copilot_seat_management, expected_type=type_hints["organization_copilot_seat_management"])
            check_type(argname="argument organization_custom_org_roles", value=organization_custom_org_roles, expected_type=type_hints["organization_custom_org_roles"])
            check_type(argname="argument organization_custom_properties", value=organization_custom_properties, expected_type=type_hints["organization_custom_properties"])
            check_type(argname="argument organization_custom_roles", value=organization_custom_roles, expected_type=type_hints["organization_custom_roles"])
            check_type(argname="argument organization_events", value=organization_events, expected_type=type_hints["organization_events"])
            check_type(argname="argument organization_hooks", value=organization_hooks, expected_type=type_hints["organization_hooks"])
            check_type(argname="argument organization_packages", value=organization_packages, expected_type=type_hints["organization_packages"])
            check_type(argname="argument organization_personal_access_token_requests", value=organization_personal_access_token_requests, expected_type=type_hints["organization_personal_access_token_requests"])
            check_type(argname="argument organization_personal_access_tokens", value=organization_personal_access_tokens, expected_type=type_hints["organization_personal_access_tokens"])
            check_type(argname="argument organization_plan", value=organization_plan, expected_type=type_hints["organization_plan"])
            check_type(argname="argument organization_projects", value=organization_projects, expected_type=type_hints["organization_projects"])
            check_type(argname="argument organization_secrets", value=organization_secrets, expected_type=type_hints["organization_secrets"])
            check_type(argname="argument organization_self_hosted_runners", value=organization_self_hosted_runners, expected_type=type_hints["organization_self_hosted_runners"])
            check_type(argname="argument orgnaization_user_blocking", value=orgnaization_user_blocking, expected_type=type_hints["orgnaization_user_blocking"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument pages", value=pages, expected_type=type_hints["pages"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument repository_announcement_banners", value=repository_announcement_banners, expected_type=type_hints["repository_announcement_banners"])
            check_type(argname="argument repository_custom_properties", value=repository_custom_properties, expected_type=type_hints["repository_custom_properties"])
            check_type(argname="argument repository_hooks", value=repository_hooks, expected_type=type_hints["repository_hooks"])
            check_type(argname="argument repository_projects", value=repository_projects, expected_type=type_hints["repository_projects"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument secret_scanning_alerts", value=secret_scanning_alerts, expected_type=type_hints["secret_scanning_alerts"])
            check_type(argname="argument security_events", value=security_events, expected_type=type_hints["security_events"])
            check_type(argname="argument single_file", value=single_file, expected_type=type_hints["single_file"])
            check_type(argname="argument starring", value=starring, expected_type=type_hints["starring"])
            check_type(argname="argument statuses", value=statuses, expected_type=type_hints["statuses"])
            check_type(argname="argument team_discussions", value=team_discussions, expected_type=type_hints["team_discussions"])
            check_type(argname="argument vulnerability_alerts", value=vulnerability_alerts, expected_type=type_hints["vulnerability_alerts"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if administration is not None:
            self._values["administration"] = administration
        if attestations is not None:
            self._values["attestations"] = attestations
        if checks is not None:
            self._values["checks"] = checks
        if codespaces is not None:
            self._values["codespaces"] = codespaces
        if contents is not None:
            self._values["contents"] = contents
        if dependabot_secrets is not None:
            self._values["dependabot_secrets"] = dependabot_secrets
        if deployments is not None:
            self._values["deployments"] = deployments
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if environments is not None:
            self._values["environments"] = environments
        if followers is not None:
            self._values["followers"] = followers
        if git_ssh_keys is not None:
            self._values["git_ssh_keys"] = git_ssh_keys
        if gpg_keys is not None:
            self._values["gpg_keys"] = gpg_keys
        if interaction_limits is not None:
            self._values["interaction_limits"] = interaction_limits
        if issues is not None:
            self._values["issues"] = issues
        if members is not None:
            self._values["members"] = members
        if metadata is not None:
            self._values["metadata"] = metadata
        if organization_administration is not None:
            self._values["organization_administration"] = organization_administration
        if organization_announcement_banners is not None:
            self._values["organization_announcement_banners"] = organization_announcement_banners
        if organization_copilot_seat_management is not None:
            self._values["organization_copilot_seat_management"] = organization_copilot_seat_management
        if organization_custom_org_roles is not None:
            self._values["organization_custom_org_roles"] = organization_custom_org_roles
        if organization_custom_properties is not None:
            self._values["organization_custom_properties"] = organization_custom_properties
        if organization_custom_roles is not None:
            self._values["organization_custom_roles"] = organization_custom_roles
        if organization_events is not None:
            self._values["organization_events"] = organization_events
        if organization_hooks is not None:
            self._values["organization_hooks"] = organization_hooks
        if organization_packages is not None:
            self._values["organization_packages"] = organization_packages
        if organization_personal_access_token_requests is not None:
            self._values["organization_personal_access_token_requests"] = organization_personal_access_token_requests
        if organization_personal_access_tokens is not None:
            self._values["organization_personal_access_tokens"] = organization_personal_access_tokens
        if organization_plan is not None:
            self._values["organization_plan"] = organization_plan
        if organization_projects is not None:
            self._values["organization_projects"] = organization_projects
        if organization_secrets is not None:
            self._values["organization_secrets"] = organization_secrets
        if organization_self_hosted_runners is not None:
            self._values["organization_self_hosted_runners"] = organization_self_hosted_runners
        if orgnaization_user_blocking is not None:
            self._values["orgnaization_user_blocking"] = orgnaization_user_blocking
        if packages is not None:
            self._values["packages"] = packages
        if pages is not None:
            self._values["pages"] = pages
        if profile is not None:
            self._values["profile"] = profile
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if repository_announcement_banners is not None:
            self._values["repository_announcement_banners"] = repository_announcement_banners
        if repository_custom_properties is not None:
            self._values["repository_custom_properties"] = repository_custom_properties
        if repository_hooks is not None:
            self._values["repository_hooks"] = repository_hooks
        if repository_projects is not None:
            self._values["repository_projects"] = repository_projects
        if secrets is not None:
            self._values["secrets"] = secrets
        if secret_scanning_alerts is not None:
            self._values["secret_scanning_alerts"] = secret_scanning_alerts
        if security_events is not None:
            self._values["security_events"] = security_events
        if single_file is not None:
            self._values["single_file"] = single_file
        if starring is not None:
            self._values["starring"] = starring
        if statuses is not None:
            self._values["statuses"] = statuses
        if team_discussions is not None:
            self._values["team_discussions"] = team_discussions
        if vulnerability_alerts is not None:
            self._values["vulnerability_alerts"] = vulnerability_alerts
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def actions(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def administration(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("administration")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def attestations(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("attestations")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def checks(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("checks")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def codespaces(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("codespaces")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def contents(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def dependabot_secrets(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("dependabot_secrets")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def deployments(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deployments")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def environments(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("environments")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def followers(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("followers")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def git_ssh_keys(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("git_ssh_keys")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def interaction_limits(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("interaction_limits")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def issues(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def members(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def metadata(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_administration(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_administration")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_announcement_banners(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_announcement_banners")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_copilot_seat_management(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_copilot_seat_management")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_custom_org_roles(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_custom_org_roles")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_custom_properties(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_custom_properties")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_custom_roles(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_custom_roles")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_events(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_events")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_hooks(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_hooks")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_packages(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_packages")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_personal_access_token_requests(
        self,
    ) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_personal_access_token_requests")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_personal_access_tokens(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_personal_access_tokens")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_plan(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_plan")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_projects(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_projects")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_secrets(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_secrets")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def organization_self_hosted_runners(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("organization_self_hosted_runners")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def orgnaization_user_blocking(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("orgnaization_user_blocking")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def packages(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def pages(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pages")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def profile(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def repository_announcement_banners(self) -> typing.Optional[AppPermission]:
        '''
        :deprecated: removed by GitHub

        :stability: deprecated
        '''
        result = self._values.get("repository_announcement_banners")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def repository_custom_properties(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("repository_custom_properties")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def repository_hooks(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("repository_hooks")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def repository_projects(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("repository_projects")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def secrets(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def secret_scanning_alerts(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("secret_scanning_alerts")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def security_events(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_events")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def single_file(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("single_file")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def starring(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("starring")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def statuses(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("statuses")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def team_discussions(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("team_discussions")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def vulnerability_alerts(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vulnerability_alerts")
        return typing.cast(typing.Optional[AppPermission], result)

    @builtins.property
    def workflows(self) -> typing.Optional[AppPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("workflows")
        return typing.cast(typing.Optional[AppPermission], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.BranchProtectionRuleOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class BranchProtectionRuleOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Branch Protection Rule options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c11d1dd0003925c76d3c0071c26d26436e2dec53d9ad08c4e3abe2db2c75e91)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.CheckRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Check run options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4347e11acd26f11508a618d0b238a95d67a7f80349876130ff38e9061f584370)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.CheckSuiteOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckSuiteOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Check suite options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b40134ecf1ce3d1252c6d518b83fbd48bccf3592878c8a25a5e61380cc82b3)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckSuiteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.CommonJobDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "permissions": "permissions",
        "concurrency": "concurrency",
        "if_": "if",
        "name": "name",
        "needs": "needs",
        "strategy": "strategy",
    },
)
class CommonJobDefinition:
    def __init__(
        self,
        *,
        permissions: typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]],
        concurrency: typing.Any = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param permissions: (experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access. Use ``{ contents: READ }`` if your job only needs to clone code. This is intentionally a required field since it is required in order to allow workflows to run in GitHub repositories with restricted default access.
        :param concurrency: (experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time. A concurrency group can be any string or expression. The expression can use any context except for the secrets context.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) The name of the job displayed on GitHub.
        :param needs: (experimental) Identifies any jobs that must complete successfully before this job will run. It can be a string or array of strings. If a job fails, all jobs that need it are skipped unless the jobs use a conditional expression that causes the job to continue.
        :param strategy: (experimental) A strategy creates a build matrix for your jobs. You can define different variations to run each job in.

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if isinstance(strategy, dict):
            strategy = JobStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2014a638b9f0a055f9914f90ac8de197a8741af9ed5179f476f1c565146134)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions": permissions,
        }
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def permissions(self) -> "JobPermissions":
        '''(experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access.

        Use ``{ contents: READ }`` if your job only needs to clone code.

        This is intentionally a required field since it is required in order to
        allow workflows to run in GitHub repositories with restricted default
        access.

        :see: https://docs.github.com/en/actions/reference/authentication-in-a-workflow#permissions-for-the-github_token
        :stability: experimental
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast("JobPermissions", result)

    @builtins.property
    def concurrency(self) -> typing.Any:
        '''(experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.

        A concurrency group can be any
        string or expression. The expression can use any context except for the
        secrets context.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Any, result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the job displayed on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifies any jobs that must complete successfully before this job will run.

        It can be a string or array of strings. If a job fails, all jobs
        that need it are skipped unless the jobs use a conditional expression
        that causes the job to continue.

        :stability: experimental
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["JobStrategy"]:
        '''(experimental) A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["JobStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonJobDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ContainerCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ContainerCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''(experimental) Credentials to use to authenticate to Docker registries.

        :param password: (experimental) The password.
        :param username: (experimental) The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c068cd566cf3598395667d999333ef7561bfd204ce91a842b6f660134873bf5)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ContainerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "credentials": "credentials",
        "env": "env",
        "options": "options",
        "ports": "ports",
        "volumes": "volumes",
    },
)
class ContainerOptions:
    def __init__(
        self,
        *,
        image: builtins.str,
        credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options pertaining to container environments.

        :param image: (experimental) The Docker image to use as the container to run the action. The value can be the Docker Hub image name or a registry name.
        :param credentials: (experimental) f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password. The credentials are the same values that you would provide to the docker login command.
        :param env: (experimental) Sets a map of environment variables in the container.
        :param options: (experimental) Additional Docker container resource options.
        :param ports: (experimental) Sets an array of ports to expose on the container.
        :param volumes: (experimental) Sets an array of volumes for the container to use. You can use volumes to share data between services or other steps in a job. You can specify named Docker volumes, anonymous Docker volumes, or bind mounts on the host. To specify a volume, you specify the source and destination path: ``<source>:<destinationPath>``.

        :stability: experimental
        '''
        if isinstance(credentials, dict):
            credentials = ContainerCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3745b83f4463c4fc52b9717275f5271dfc3bca86f6f6742576a53ec8359dbb05)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if env is not None:
            self._values["env"] = env
        if options is not None:
            self._values["options"] = options
        if ports is not None:
            self._values["ports"] = ports
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> builtins.str:
        '''(experimental) The Docker image to use as the container to run the action.

        The value can
        be the Docker Hub image name or a registry name.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(self) -> typing.Optional[ContainerCredentials]:
        '''(experimental) f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password.

        The credentials are the same values that you would provide to the docker
        login command.

        :stability: experimental
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[ContainerCredentials], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Sets a map of environment variables in the container.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional Docker container resource options.

        :see: https://docs.docker.com/engine/reference/commandline/create/#options
        :stability: experimental
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) Sets an array of ports to expose on the container.

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Sets an array of volumes for the container to use.

        You can use volumes to
        share data between services or other steps in a job. You can specify
        named Docker volumes, anonymous Docker volumes, or bind mounts on the
        host.

        To specify a volume, you specify the source and destination path:
        ``<source>:<destinationPath>``.

        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.CreateOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CreateOptions:
    def __init__(self) -> None:
        '''(experimental) The Create event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.CronScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class CronScheduleOptions:
    def __init__(self, *, cron: builtins.str) -> None:
        '''(experimental) CRON schedule options.

        :param cron: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b942d3c2ff8727f2ff55175941fa65b503b9b9b5509291efe52190850c93afaa)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cron": cron,
        }

    @builtins.property
    def cron(self) -> builtins.str:
        '''
        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        :stability: experimental
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.DeleteOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeleteOptions:
    def __init__(self) -> None:
        '''(experimental) The Delete event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeleteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.DeploymentOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentOptions:
    def __init__(self) -> None:
        '''(experimental) The Deployment event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.DeploymentStatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentStatusOptions:
    def __init__(self) -> None:
        '''(experimental) The Deployment status event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentStatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.DiscussionCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class DiscussionCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Discussion comment options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af138b824decbcd8cf918b7d2032093418049a345b01ed01f88accfcee395b5a)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscussionCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.DiscussionOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class DiscussionOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Discussion options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97467ebe6e40905d2acd015311e4fbde640f5ab410b74b1de055967ddf4e771)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscussionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ForkOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class ForkOptions:
    def __init__(self) -> None:
        '''(experimental) The Fork event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.GollumOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GollumOptions:
    def __init__(self) -> None:
        '''(experimental) The Gollum event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GollumOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.IssueCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssueCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Issue comment options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217e744007dbc2c9e22b6c0ad4aa07d2a4711631c6fc1de1414dea628db3841b)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.IssuesOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssuesOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Issues options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86720be0c98429300bca3b757935fb0a6d341673f54d031b808b1f9d1b3512e3)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssuesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.Job",
    jsii_struct_bases=[CommonJobDefinition],
    name_mapping={
        "permissions": "permissions",
        "concurrency": "concurrency",
        "if_": "if",
        "name": "name",
        "needs": "needs",
        "strategy": "strategy",
        "steps": "steps",
        "container": "container",
        "continue_on_error": "continueOnError",
        "defaults": "defaults",
        "env": "env",
        "environment": "environment",
        "outputs": "outputs",
        "runs_on": "runsOn",
        "runs_on_group": "runsOnGroup",
        "services": "services",
        "timeout_minutes": "timeoutMinutes",
        "tools": "tools",
    },
)
class Job(CommonJobDefinition):
    def __init__(
        self,
        *,
        permissions: typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]],
        concurrency: typing.Any = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        steps: typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]],
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union["JobDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Any = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, typing.Union["JobStepOutput", typing.Dict[builtins.str, typing.Any]]]] = None,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        tools: typing.Optional[typing.Union["Tools", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) A GitHub Workflow job definition.

        :param permissions: (experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access. Use ``{ contents: READ }`` if your job only needs to clone code. This is intentionally a required field since it is required in order to allow workflows to run in GitHub repositories with restricted default access.
        :param concurrency: (experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time. A concurrency group can be any string or expression. The expression can use any context except for the secrets context.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) The name of the job displayed on GitHub.
        :param needs: (experimental) Identifies any jobs that must complete successfully before this job will run. It can be a string or array of strings. If a job fails, all jobs that need it are skipped unless the jobs use a conditional expression that causes the job to continue.
        :param strategy: (experimental) A strategy creates a build matrix for your jobs. You can define different variations to run each job in.
        :param steps: (experimental) A job contains a sequence of tasks called steps. Steps can run commands, run setup tasks, or run an action in your repository, a public repository, or an action published in a Docker registry. Not all steps run actions, but all actions run as a step. Each step runs in its own process in the runner environment and has access to the workspace and filesystem. Because steps run in their own process, changes to environment variables are not preserved between steps. GitHub provides built-in steps to set up and complete a job.
        :param container: (experimental) A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: (experimental) Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: (experimental) A map of default settings that will apply to all steps in the job. You can also set default settings for the entire workflow.
        :param env: (experimental) A map of environment variables that are available to all steps in the job. You can also set environment variables for the entire workflow or an individual step.
        :param environment: (experimental) The environment that the job references. All environment protection rules must pass before a job referencing the environment is sent to a runner.
        :param outputs: (experimental) A map of outputs for a job. Job outputs are available to all downstream jobs that depend on this job.
        :param runs_on: (experimental) The type of machine to run the job on. The machine can be either a GitHub-hosted runner or a self-hosted runner.
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param services: (experimental) Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param timeout_minutes: (experimental) The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360
        :param tools: (experimental) Tools required for this job. Translates into ``actions/setup-xxx`` steps at the beginning of the job.

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if isinstance(strategy, dict):
            strategy = JobStrategy(**strategy)
        if isinstance(container, dict):
            container = ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = JobDefaults(**defaults)
        if isinstance(runs_on_group, dict):
            runs_on_group = _GroupRunnerOptions_148c59c1(**runs_on_group)
        if isinstance(tools, dict):
            tools = Tools(**tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b405f548924ed15a8a6902fcc20e3f048e3450d8a016b7904ed920f64aab582)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument runs_on_group", value=runs_on_group, expected_type=type_hints["runs_on_group"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions": permissions,
            "steps": steps,
        }
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if strategy is not None:
            self._values["strategy"] = strategy
        if container is not None:
            self._values["container"] = container
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env
        if environment is not None:
            self._values["environment"] = environment
        if outputs is not None:
            self._values["outputs"] = outputs
        if runs_on is not None:
            self._values["runs_on"] = runs_on
        if runs_on_group is not None:
            self._values["runs_on_group"] = runs_on_group
        if services is not None:
            self._values["services"] = services
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if tools is not None:
            self._values["tools"] = tools

    @builtins.property
    def permissions(self) -> "JobPermissions":
        '''(experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access.

        Use ``{ contents: READ }`` if your job only needs to clone code.

        This is intentionally a required field since it is required in order to
        allow workflows to run in GitHub repositories with restricted default
        access.

        :see: https://docs.github.com/en/actions/reference/authentication-in-a-workflow#permissions-for-the-github_token
        :stability: experimental
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast("JobPermissions", result)

    @builtins.property
    def concurrency(self) -> typing.Any:
        '''(experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.

        A concurrency group can be any
        string or expression. The expression can use any context except for the
        secrets context.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Any, result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the job displayed on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifies any jobs that must complete successfully before this job will run.

        It can be a string or array of strings. If a job fails, all jobs
        that need it are skipped unless the jobs use a conditional expression
        that causes the job to continue.

        :stability: experimental
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["JobStrategy"]:
        '''(experimental) A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["JobStrategy"], result)

    @builtins.property
    def steps(self) -> typing.List["JobStep"]:
        '''(experimental) A job contains a sequence of tasks called steps.

        Steps can run commands,
        run setup tasks, or run an action in your repository, a public repository,
        or an action published in a Docker registry. Not all steps run actions,
        but all actions run as a step. Each step runs in its own process in the
        runner environment and has access to the workspace and filesystem.
        Because steps run in their own process, changes to environment variables
        are not preserved between steps. GitHub provides built-in steps to set up
        and complete a job.

        :stability: experimental
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.List["JobStep"], result)

    @builtins.property
    def container(self) -> typing.Optional[ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevents a workflow run from failing when a job fails.

        Set to true to
        allow a workflow run to pass when this job fails.

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def defaults(self) -> typing.Optional["JobDefaults"]:
        '''(experimental) A map of default settings that will apply to all steps in the job.

        You
        can also set default settings for the entire workflow.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional["JobDefaults"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A map of environment variables that are available to all steps in the job.

        You can also set environment variables for the entire workflow or an
        individual step.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Any:
        '''(experimental) The environment that the job references.

        All environment protection rules
        must pass before a job referencing the environment is sent to a runner.

        :see: https://docs.github.com/en/actions/reference/environments
        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Any, result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, "JobStepOutput"]]:
        '''(experimental) A map of outputs for a job.

        Job outputs are available to all downstream
        jobs that depend on this job.

        :stability: experimental
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "JobStepOutput"]], result)

    @builtins.property
    def runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The type of machine to run the job on.

        The machine can be either a
        GitHub-hosted runner or a self-hosted runner.

        :stability: experimental

        Example::

            ["ubuntu-latest"]
        '''
        result = self._values.get("runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    @builtins.property
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of minutes to let a job run before GitHub automatically cancels it.

        :default: 360

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tools(self) -> typing.Optional["Tools"]:
        '''(experimental) Tools required for this job.

        Translates into ``actions/setup-xxx`` steps at
        the beginning of the job.

        :stability: experimental
        '''
        result = self._values.get("tools")
        return typing.cast(typing.Optional["Tools"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Job(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.JobCallingReusableWorkflow",
    jsii_struct_bases=[CommonJobDefinition],
    name_mapping={
        "permissions": "permissions",
        "concurrency": "concurrency",
        "if_": "if",
        "name": "name",
        "needs": "needs",
        "strategy": "strategy",
        "uses": "uses",
        "secrets": "secrets",
        "with_": "with",
    },
)
class JobCallingReusableWorkflow(CommonJobDefinition):
    def __init__(
        self,
        *,
        permissions: typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]],
        concurrency: typing.Any = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        uses: builtins.str,
        secrets: typing.Optional[typing.Union[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    ) -> None:
        '''(experimental) A GitHub Workflow Job calling a reusable workflow.

        :param permissions: (experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access. Use ``{ contents: READ }`` if your job only needs to clone code. This is intentionally a required field since it is required in order to allow workflows to run in GitHub repositories with restricted default access.
        :param concurrency: (experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time. A concurrency group can be any string or expression. The expression can use any context except for the secrets context.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) The name of the job displayed on GitHub.
        :param needs: (experimental) Identifies any jobs that must complete successfully before this job will run. It can be a string or array of strings. If a job fails, all jobs that need it are skipped unless the jobs use a conditional expression that causes the job to continue.
        :param strategy: (experimental) A strategy creates a build matrix for your jobs. You can define different variations to run each job in.
        :param uses: (experimental) The location and version of a reusable workflow file to run as a job.
        :param secrets: (experimental) When a job is used to call a reusable workflow, you can use secrets to provide a map of secrets that are passed to the called workflow. Use the 'inherit' keyword to pass all the calling workflow's secrets to the called workflow
        :param with_: (experimental) When a job is used to call a reusable workflow, you can use with to provide a map of inputs that are passed to the called workflow. Allowed expression contexts: ``github``, and ``needs``.

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if isinstance(strategy, dict):
            strategy = JobStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9905a897c84934e8ed2bde6e0bd6fdd798275b2a8b89a503c19dba40649562)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument with_", value=with_, expected_type=type_hints["with_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions": permissions,
            "uses": uses,
        }
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if strategy is not None:
            self._values["strategy"] = strategy
        if secrets is not None:
            self._values["secrets"] = secrets
        if with_ is not None:
            self._values["with_"] = with_

    @builtins.property
    def permissions(self) -> "JobPermissions":
        '''(experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access.

        Use ``{ contents: READ }`` if your job only needs to clone code.

        This is intentionally a required field since it is required in order to
        allow workflows to run in GitHub repositories with restricted default
        access.

        :see: https://docs.github.com/en/actions/reference/authentication-in-a-workflow#permissions-for-the-github_token
        :stability: experimental
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast("JobPermissions", result)

    @builtins.property
    def concurrency(self) -> typing.Any:
        '''(experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.

        A concurrency group can be any
        string or expression. The expression can use any context except for the
        secrets context.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Any, result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the job displayed on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifies any jobs that must complete successfully before this job will run.

        It can be a string or array of strings. If a job fails, all jobs
        that need it are skipped unless the jobs use a conditional expression
        that causes the job to continue.

        :stability: experimental
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["JobStrategy"]:
        '''(experimental) A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["JobStrategy"], result)

    @builtins.property
    def uses(self) -> builtins.str:
        '''(experimental) The location and version of a reusable workflow file to run as a job.

        :stability: experimental
        '''
        result = self._values.get("uses")
        assert result is not None, "Required property 'uses' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.Mapping[builtins.str, builtins.str]]]:
        '''(experimental) When a job is used to call a reusable workflow, you can use secrets to provide a map of secrets that are passed to the called workflow.

        Use the 'inherit' keyword to pass all the calling workflow's secrets to the called workflow

        :stability: experimental
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[builtins.str, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def with_(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]]:
        '''(experimental) When a job is used to call a reusable workflow, you can use with to provide a map of inputs that are passed to the called workflow.

        Allowed expression contexts: ``github``, and ``needs``.

        :stability: experimental
        '''
        result = self._values.get("with_")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobCallingReusableWorkflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.JobDefaults",
    jsii_struct_bases=[],
    name_mapping={"run": "run"},
)
class JobDefaults:
    def __init__(
        self,
        *,
        run: typing.Optional[typing.Union["RunSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Default settings for all steps in the job.

        :param run: (experimental) Default run settings.

        :stability: experimental
        '''
        if isinstance(run, dict):
            run = RunSettings(**run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afc181ec4ce3844469de535090d57cb39b9f47cf28d0bdc1e7a95bf29c34199)
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if run is not None:
            self._values["run"] = run

    @builtins.property
    def run(self) -> typing.Optional["RunSettings"]:
        '''(experimental) Default run settings.

        :stability: experimental
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional["RunSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.JobMatrix",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "exclude": "exclude", "include": "include"},
)
class JobMatrix:
    def __init__(
        self,
        *,
        domain: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool]]]]] = None,
        exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]] = None,
        include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]] = None,
    ) -> None:
        '''(experimental) A job matrix.

        :param domain: (experimental) Each option you define in the matrix has a key and value. The keys you define become properties in the matrix context and you can reference the property in other areas of your workflow file. For example, if you define the key os that contains an array of operating systems, you can use the matrix.os property as the value of the runs-on keyword to create a job for each operating system.
        :param exclude: (experimental) You can remove a specific configurations defined in the build matrix using the exclude option. Using exclude removes a job defined by the build matrix.
        :param include: (experimental) You can add additional configuration options to a build matrix job that already exists. For example, if you want to use a specific version of npm when the job that uses windows-latest and version 8 of node runs, you can use include to specify that additional option.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c1bb692367ba40c0c0307ec4a86916287ff1f39e99b1eeab7f30bb7886bbda)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool]]]]]:
        '''(experimental) Each option you define in the matrix has a key and value.

        The keys you
        define become properties in the matrix context and you can reference the
        property in other areas of your workflow file. For example, if you define
        the key os that contains an array of operating systems, you can use the
        matrix.os property as the value of the runs-on keyword to create a job
        for each operating system.

        :stability: experimental
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool]]]]], result)

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]]:
        '''(experimental) You can remove a specific configurations defined in the build matrix using the exclude option.

        Using exclude removes a job defined by the
        build matrix.

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]], result)

    @builtins.property
    def include(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]]:
        '''(experimental) You can add additional configuration options to a build matrix job that already exists.

        For example, if you want to use a specific version of npm
        when the job that uses windows-latest and version 8 of node runs, you can
        use include to specify that additional option.

        :stability: experimental
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobMatrix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.github.workflows.JobPermission")
class JobPermission(enum.Enum):
    '''(experimental) Access level for workflow permission scopes.

    :stability: experimental
    '''

    READ = "READ"
    '''(experimental) Read-only access.

    :stability: experimental
    '''
    WRITE = "WRITE"
    '''(experimental) Read-write access.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) No access at all.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.github.workflows.JobPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "attestations": "attestations",
        "checks": "checks",
        "contents": "contents",
        "deployments": "deployments",
        "discussions": "discussions",
        "id_token": "idToken",
        "issues": "issues",
        "models": "models",
        "packages": "packages",
        "pages": "pages",
        "pull_requests": "pullRequests",
        "repository_projects": "repositoryProjects",
        "security_events": "securityEvents",
        "statuses": "statuses",
    },
)
class JobPermissions:
    def __init__(
        self,
        *,
        actions: typing.Optional[JobPermission] = None,
        attestations: typing.Optional[JobPermission] = None,
        checks: typing.Optional[JobPermission] = None,
        contents: typing.Optional[JobPermission] = None,
        deployments: typing.Optional[JobPermission] = None,
        discussions: typing.Optional[JobPermission] = None,
        id_token: typing.Optional[JobPermission] = None,
        issues: typing.Optional[JobPermission] = None,
        models: typing.Optional[JobPermission] = None,
        packages: typing.Optional[JobPermission] = None,
        pages: typing.Optional[JobPermission] = None,
        pull_requests: typing.Optional[JobPermission] = None,
        repository_projects: typing.Optional[JobPermission] = None,
        security_events: typing.Optional[JobPermission] = None,
        statuses: typing.Optional[JobPermission] = None,
    ) -> None:
        '''(experimental) The available scopes and access values for workflow permissions.

        If you
        specify the access for any of these scopes, all those that are not
        specified are set to ``JobPermission.NONE``, instead of the default behavior
        when none is specified.

        :param actions: 
        :param attestations: 
        :param checks: 
        :param contents: 
        :param deployments: 
        :param discussions: 
        :param id_token: 
        :param issues: 
        :param models: 
        :param packages: 
        :param pages: 
        :param pull_requests: 
        :param repository_projects: 
        :param security_events: 
        :param statuses: 

        :see: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/controlling-permissions-for-github_token#defining-access-for-the-github_token-permissions
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9b6a3fbdc58e402a1aaac55747b5faedde783c61dcd4c97c759406d925e9a5)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument attestations", value=attestations, expected_type=type_hints["attestations"])
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument deployments", value=deployments, expected_type=type_hints["deployments"])
            check_type(argname="argument discussions", value=discussions, expected_type=type_hints["discussions"])
            check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument models", value=models, expected_type=type_hints["models"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument pages", value=pages, expected_type=type_hints["pages"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument repository_projects", value=repository_projects, expected_type=type_hints["repository_projects"])
            check_type(argname="argument security_events", value=security_events, expected_type=type_hints["security_events"])
            check_type(argname="argument statuses", value=statuses, expected_type=type_hints["statuses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if attestations is not None:
            self._values["attestations"] = attestations
        if checks is not None:
            self._values["checks"] = checks
        if contents is not None:
            self._values["contents"] = contents
        if deployments is not None:
            self._values["deployments"] = deployments
        if discussions is not None:
            self._values["discussions"] = discussions
        if id_token is not None:
            self._values["id_token"] = id_token
        if issues is not None:
            self._values["issues"] = issues
        if models is not None:
            self._values["models"] = models
        if packages is not None:
            self._values["packages"] = packages
        if pages is not None:
            self._values["pages"] = pages
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if repository_projects is not None:
            self._values["repository_projects"] = repository_projects
        if security_events is not None:
            self._values["security_events"] = security_events
        if statuses is not None:
            self._values["statuses"] = statuses

    @builtins.property
    def actions(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def attestations(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("attestations")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def checks(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("checks")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def contents(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def deployments(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deployments")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def discussions(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("discussions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def id_token(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("id_token")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def issues(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def models(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("models")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def packages(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def pages(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pages")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def repository_projects(self) -> typing.Optional[JobPermission]:
        '''
        :deprecated: removed by GitHub

        :stability: deprecated
        '''
        result = self._values.get("repository_projects")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def security_events(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_events")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def statuses(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("statuses")
        return typing.cast(typing.Optional[JobPermission], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.JobStepOutput",
    jsii_struct_bases=[],
    name_mapping={"output_name": "outputName", "step_id": "stepId"},
)
class JobStepOutput:
    def __init__(self, *, output_name: builtins.str, step_id: builtins.str) -> None:
        '''(experimental) An output binding for a job.

        :param output_name: (experimental) The name of the job output that is being bound.
        :param step_id: (experimental) The ID of the step that exposes the output.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54660692cd1951dfa8376b33c95c26d58e87bbafc6ed590fb6fe9216ce01ba7)
            check_type(argname="argument output_name", value=output_name, expected_type=type_hints["output_name"])
            check_type(argname="argument step_id", value=step_id, expected_type=type_hints["step_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_name": output_name,
            "step_id": step_id,
        }

    @builtins.property
    def output_name(self) -> builtins.str:
        '''(experimental) The name of the job output that is being bound.

        :stability: experimental
        '''
        result = self._values.get("output_name")
        assert result is not None, "Required property 'output_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def step_id(self) -> builtins.str:
        '''(experimental) The ID of the step that exposes the output.

        :stability: experimental
        '''
        result = self._values.get("step_id")
        assert result is not None, "Required property 'step_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStepOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.JobStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "fail_fast": "failFast",
        "matrix": "matrix",
        "max_parallel": "maxParallel",
    },
)
class JobStrategy:
    def __init__(
        self,
        *,
        fail_fast: typing.Optional[builtins.bool] = None,
        matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[builtins.str, typing.Any]]] = None,
        max_parallel: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :param fail_fast: (experimental) When set to true, GitHub cancels all in-progress jobs if any matrix job fails. Default: true
        :param matrix: (experimental) You can define a matrix of different job configurations. A matrix allows you to create multiple jobs by performing variable substitution in a single job definition. For example, you can use a matrix to create jobs for more than one supported version of a programming language, operating system, or tool. A matrix reuses the job's configuration and creates a job for each matrix you configure. A job matrix can generate a maximum of 256 jobs per workflow run. This limit also applies to self-hosted runners.
        :param max_parallel: (experimental) The maximum number of jobs that can run simultaneously when using a matrix job strategy. By default, GitHub will maximize the number of jobs run in parallel depending on the available runners on GitHub-hosted virtual machines.

        :stability: experimental
        '''
        if isinstance(matrix, dict):
            matrix = JobMatrix(**matrix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134570ab28cf6023a626f13de20038e5ad2ad2ee907973354ce8dd6e36636499)
            check_type(argname="argument fail_fast", value=fail_fast, expected_type=type_hints["fail_fast"])
            check_type(argname="argument matrix", value=matrix, expected_type=type_hints["matrix"])
            check_type(argname="argument max_parallel", value=max_parallel, expected_type=type_hints["max_parallel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fail_fast is not None:
            self._values["fail_fast"] = fail_fast
        if matrix is not None:
            self._values["matrix"] = matrix
        if max_parallel is not None:
            self._values["max_parallel"] = max_parallel

    @builtins.property
    def fail_fast(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When set to true, GitHub cancels all in-progress jobs if any matrix job fails.

        Default: true

        :stability: experimental
        '''
        result = self._values.get("fail_fast")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def matrix(self) -> typing.Optional[JobMatrix]:
        '''(experimental) You can define a matrix of different job configurations.

        A matrix allows
        you to create multiple jobs by performing variable substitution in a
        single job definition. For example, you can use a matrix to create jobs
        for more than one supported version of a programming language, operating
        system, or tool. A matrix reuses the job's configuration and creates a
        job for each matrix you configure.

        A job matrix can generate a maximum of 256 jobs per workflow run. This
        limit also applies to self-hosted runners.

        :stability: experimental
        '''
        result = self._values.get("matrix")
        return typing.cast(typing.Optional[JobMatrix], result)

    @builtins.property
    def max_parallel(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of jobs that can run simultaneously when using a matrix job strategy.

        By default, GitHub will maximize the number of jobs
        run in parallel depending on the available runners on GitHub-hosted
        virtual machines.

        :stability: experimental
        '''
        result = self._values.get("max_parallel")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.LabelOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class LabelOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Label options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50bb7bfbc56deada571dfd117b208118a0999144362cd066f2fa72083f2dbde6)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.MergeGroupOptions",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches"},
)
class MergeGroupOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Merge group options.

        :param branches: (experimental) When using the merge_group events, you can configure a workflow to run on specific base branches. If not specified, all branches will trigger the workflow.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1bf8c4c650a790f23377cc4e527f5235804e0ede24bec6d08006307448d1da2)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the merge_group events, you can configure a workflow to run on specific base branches.

        If not specified, all branches will
        trigger the workflow.

        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MergeGroupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.MilestoneOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class MilestoneOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Milestone options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82a3af3c1c9a05cdcbb3e82973ff2c7209b0845f46e0f375d7b1b923b61c594)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MilestoneOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.PageBuildOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PageBuildOptions:
    def __init__(self) -> None:
        '''(experimental) The Page build event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PageBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ProjectCardOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectCardOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Project card options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cd16cd68d37babc3afecf26110f73a792b6caee362abfc413ead1fec8f686f)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectCardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ProjectColumnOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectColumnOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Probject column options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16dee1fa11035cd0fd9d7774dd224981d0fd92e7c44649b8af742e00f8c80f5d)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectColumnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ProjectOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Project options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a3bdc315041b645bf04461deaf270cc61bdfc779c62610457121f16d55f943)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.PublicOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PublicOptions:
    def __init__(self) -> None:
        '''(experimental) The Public event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublicOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.PullRequestReviewCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request review comment options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924a9205551b733fad7955355cf317e09d79435bc464c13625ab82a4083b4eeb)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.PullRequestReviewOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request review options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa7e340b849b51a5bbea8528f24bc797b353586438c6d939f514b86f547b2c9)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.PushOptions",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches", "paths": "paths", "tags": "tags"},
)
class PushOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for push-like events.

        :param branches: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1b5ef2dd2ebfefd88be7a903d4676960437a284d29f5ac056b2cdde3f62932)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.RegistryPackageOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RegistryPackageOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Registry package options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d555b19711887db4995273ee0e8c73ea2c0546a60c3796166a1f4419dd61e73c)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryPackageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ReleaseOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Release options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119a914e5bfb3cdea007b3544b187a2e3b2ab765b6fe743053491bc2496fede7)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.RepositoryDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RepositoryDispatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Repository dispatch options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf1842c4c0435b3b65c1c33f941a09c9bd78ebb950136703bc50a6a6ee27adf)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.RunSettings",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell", "working_directory": "workingDirectory"},
)
class RunSettings:
    def __init__(
        self,
        *,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Run settings for a job.

        :param shell: (experimental) Which shell to use for running the step.
        :param working_directory: (experimental) Working directory to use when running the step.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613ab93b76c86dd88502480397a66c39b983fc805b068e953f6ad756edee792e)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Which shell to use for running the step.

        :stability: experimental

        Example::

            "bash"
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Working directory to use when running the step.

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.StatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class StatusOptions:
    def __init__(self) -> None:
        '''(experimental) The Status event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.StepConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "shell": "shell",
        "working_directory": "workingDirectory",
    },
)
class StepConfiguration:
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Fields that describe the How, Why, When, and Who of a Step.

        These fields can have none present, but can be present on every Step, and have no effect on one another.

        This stands in contrast to the Command (non-Configuration) fields, which are mutually exclusive, and describe the What.

        :param env: (experimental) Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: (experimental) A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) A name for your step to display on GitHub.
        :param shell: (experimental) Overrides the default shell settings in the runner's operating system and the job's default. Refer to GitHub documentation for allowed values.
        :param working_directory: (experimental) Specifies a working directory for a step. Overrides a job's working directory.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044349b8d18055b991a5680dc1d218dc2901bc2369d30fa23e79229d8bde3b73)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique identifier for the step.

        You can use the id to reference the
        step in contexts.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for your step to display on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Overrides the default shell settings in the runner's operating system and the job's default.

        Refer to GitHub documentation for allowed values.

        :see: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsshell
        :stability: experimental
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies a working directory for a step.

        Overrides a job's working directory.

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.ToolRequirement",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class ToolRequirement:
    def __init__(self, *, version: builtins.str) -> None:
        '''(experimental) Version requirement for tools.

        :param version: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49e39102f958d999716dd94aae1647a49fe1d2fd3d73add88292e5067592c14)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }

    @builtins.property
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ToolRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.Tools",
    jsii_struct_bases=[],
    name_mapping={
        "dotnet": "dotnet",
        "go": "go",
        "java": "java",
        "node": "node",
        "python": "python",
    },
)
class Tools:
    def __init__(
        self,
        *,
        dotnet: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
        go: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
        java: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
        node: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
        python: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Supported tools.

        :param dotnet: (experimental) Setup .NET Core. Default: - not installed
        :param go: (experimental) Setup golang. Default: - not installed
        :param java: (experimental) Setup java (temurin distribution). Default: - not installed
        :param node: (experimental) Setup node.js. Default: - not installed
        :param python: (experimental) Setup python. Default: - not installed

        :stability: experimental
        '''
        if isinstance(dotnet, dict):
            dotnet = ToolRequirement(**dotnet)
        if isinstance(go, dict):
            go = ToolRequirement(**go)
        if isinstance(java, dict):
            java = ToolRequirement(**java)
        if isinstance(node, dict):
            node = ToolRequirement(**node)
        if isinstance(python, dict):
            python = ToolRequirement(**python)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dab9f9edea4d6d3c0897aa6348f12a4359741f0e29873be48495120ea2a4b12)
            check_type(argname="argument dotnet", value=dotnet, expected_type=type_hints["dotnet"])
            check_type(argname="argument go", value=go, expected_type=type_hints["go"])
            check_type(argname="argument java", value=java, expected_type=type_hints["java"])
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument python", value=python, expected_type=type_hints["python"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dotnet is not None:
            self._values["dotnet"] = dotnet
        if go is not None:
            self._values["go"] = go
        if java is not None:
            self._values["java"] = java
        if node is not None:
            self._values["node"] = node
        if python is not None:
            self._values["python"] = python

    @builtins.property
    def dotnet(self) -> typing.Optional[ToolRequirement]:
        '''(experimental) Setup .NET Core.

        :default: - not installed

        :stability: experimental
        '''
        result = self._values.get("dotnet")
        return typing.cast(typing.Optional[ToolRequirement], result)

    @builtins.property
    def go(self) -> typing.Optional[ToolRequirement]:
        '''(experimental) Setup golang.

        :default: - not installed

        :stability: experimental
        '''
        result = self._values.get("go")
        return typing.cast(typing.Optional[ToolRequirement], result)

    @builtins.property
    def java(self) -> typing.Optional[ToolRequirement]:
        '''(experimental) Setup java (temurin distribution).

        :default: - not installed

        :stability: experimental
        '''
        result = self._values.get("java")
        return typing.cast(typing.Optional[ToolRequirement], result)

    @builtins.property
    def node(self) -> typing.Optional[ToolRequirement]:
        '''(experimental) Setup node.js.

        :default: - not installed

        :stability: experimental
        '''
        result = self._values.get("node")
        return typing.cast(typing.Optional[ToolRequirement], result)

    @builtins.property
    def python(self) -> typing.Optional[ToolRequirement]:
        '''(experimental) Setup python.

        :default: - not installed

        :stability: experimental
        '''
        result = self._values.get("python")
        return typing.cast(typing.Optional[ToolRequirement], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.Triggers",
    jsii_struct_bases=[],
    name_mapping={
        "branch_protection_rule": "branchProtectionRule",
        "check_run": "checkRun",
        "check_suite": "checkSuite",
        "create": "create",
        "delete": "delete",
        "deployment": "deployment",
        "deployment_status": "deploymentStatus",
        "discussion": "discussion",
        "discussion_comment": "discussionComment",
        "fork": "fork",
        "gollum": "gollum",
        "issue_comment": "issueComment",
        "issues": "issues",
        "label": "label",
        "merge_group": "mergeGroup",
        "milestone": "milestone",
        "page_build": "pageBuild",
        "project": "project",
        "project_card": "projectCard",
        "project_column": "projectColumn",
        "public": "public",
        "pull_request": "pullRequest",
        "pull_request_review": "pullRequestReview",
        "pull_request_review_comment": "pullRequestReviewComment",
        "pull_request_target": "pullRequestTarget",
        "push": "push",
        "registry_package": "registryPackage",
        "release": "release",
        "repository_dispatch": "repositoryDispatch",
        "schedule": "schedule",
        "status": "status",
        "watch": "watch",
        "workflow_call": "workflowCall",
        "workflow_dispatch": "workflowDispatch",
        "workflow_run": "workflowRun",
    },
)
class Triggers:
    def __init__(
        self,
        *,
        branch_protection_rule: typing.Optional[typing.Union[BranchProtectionRuleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        create: typing.Optional[typing.Union[CreateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        discussion: typing.Optional[typing.Union[DiscussionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        discussion_comment: typing.Optional[typing.Union[DiscussionCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        merge_group: typing.Optional[typing.Union[MergeGroupOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        public: typing.Optional[typing.Union[PublicOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request: typing.Optional[typing.Union["PullRequestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_target: typing.Optional[typing.Union["PullRequestTargetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[typing.Union[StatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        watch: typing.Optional[typing.Union["WatchOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_call: typing.Optional[typing.Union["WorkflowCallOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_dispatch: typing.Optional[typing.Union["WorkflowDispatchOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_run: typing.Optional[typing.Union["WorkflowRunOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The set of available triggers for GitHub Workflows.

        :param branch_protection_rule: (experimental) Runs your workflow anytime the branch_protection_rule event occurs.
        :param check_run: (experimental) Runs your workflow anytime the check_run event occurs.
        :param check_suite: (experimental) Runs your workflow anytime the check_suite event occurs.
        :param create: (experimental) Runs your workflow anytime someone creates a branch or tag, which triggers the create event.
        :param delete: (experimental) Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.
        :param deployment: (experimental) Runs your workflow anytime someone creates a deployment, which triggers the deployment event. Deployments created with a commit SHA may not have a Git ref.
        :param deployment_status: (experimental) Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event. Deployments created with a commit SHA may not have a Git ref.
        :param discussion: (experimental) Runs your workflow anytime the discussion event occurs. More than one activity type triggers this event.
        :param discussion_comment: (experimental) Runs your workflow anytime the discussion_comment event occurs. More than one activity type triggers this event.
        :param fork: (experimental) Runs your workflow anytime when someone forks a repository, which triggers the fork event.
        :param gollum: (experimental) Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.
        :param issue_comment: (experimental) Runs your workflow anytime the issue_comment event occurs.
        :param issues: (experimental) Runs your workflow anytime the issues event occurs.
        :param label: (experimental) Runs your workflow anytime the label event occurs.
        :param merge_group: (experimental) Runs your workflow when a pull request is added to a merge queue, which adds the pull request to a merge group.
        :param milestone: (experimental) Runs your workflow anytime the milestone event occurs.
        :param page_build: (experimental) Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.
        :param project: (experimental) Runs your workflow anytime the project event occurs.
        :param project_card: (experimental) Runs your workflow anytime the project_card event occurs.
        :param project_column: (experimental) Runs your workflow anytime the project_column event occurs.
        :param public: (experimental) Runs your workflow anytime someone makes a private repository public, which triggers the public event.
        :param pull_request: (experimental) Runs your workflow anytime the pull_request event occurs.
        :param pull_request_review: (experimental) Runs your workflow anytime the pull_request_review event occurs.
        :param pull_request_review_comment: (experimental) Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.
        :param pull_request_target: (experimental) This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does. This prevents executing unsafe workflow code from the head of the pull request that could alter your repository or steal any secrets you use in your workflow. This event allows you to do things like create workflows that label and comment on pull requests based on the contents of the event payload. WARNING: The ``pull_request_target`` event is granted read/write repository token and can access secrets, even when it is triggered from a fork. Although the workflow runs in the context of the base of the pull request, you should make sure that you do not check out, build, or run untrusted code from the pull request with this event. Additionally, any caches share the same scope as the base branch, and to help prevent cache poisoning, you should not save the cache if there is a possibility that the cache contents were altered.
        :param push: (experimental) Runs your workflow when someone pushes to a repository branch, which triggers the push event.
        :param registry_package: (experimental) Runs your workflow anytime a package is published or updated.
        :param release: (experimental) Runs your workflow anytime the release event occurs.
        :param repository_dispatch: (experimental) You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.
        :param schedule: (experimental) You can schedule a workflow to run at specific UTC times using POSIX cron syntax. Scheduled workflows run on the latest commit on the default or base branch. The shortest interval you can run scheduled workflows is once every 5 minutes.
        :param status: (experimental) Runs your workflow anytime the status of a Git commit changes, which triggers the status event.
        :param watch: (experimental) Runs your workflow anytime the watch event occurs.
        :param workflow_call: (experimental) Can be called from another workflow.
        :param workflow_dispatch: (experimental) You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow. When the workflow runs, you can access the input values in the github.event.inputs context.
        :param workflow_run: (experimental) This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow. A workflow run is triggered regardless of the result of the previous workflow.

        :see: https://docs.github.com/en/actions/reference/events-that-trigger-workflows
        :stability: experimental
        '''
        if isinstance(branch_protection_rule, dict):
            branch_protection_rule = BranchProtectionRuleOptions(**branch_protection_rule)
        if isinstance(check_run, dict):
            check_run = CheckRunOptions(**check_run)
        if isinstance(check_suite, dict):
            check_suite = CheckSuiteOptions(**check_suite)
        if isinstance(create, dict):
            create = CreateOptions(**create)
        if isinstance(delete, dict):
            delete = DeleteOptions(**delete)
        if isinstance(deployment, dict):
            deployment = DeploymentOptions(**deployment)
        if isinstance(deployment_status, dict):
            deployment_status = DeploymentStatusOptions(**deployment_status)
        if isinstance(discussion, dict):
            discussion = DiscussionOptions(**discussion)
        if isinstance(discussion_comment, dict):
            discussion_comment = DiscussionCommentOptions(**discussion_comment)
        if isinstance(fork, dict):
            fork = ForkOptions(**fork)
        if isinstance(gollum, dict):
            gollum = GollumOptions(**gollum)
        if isinstance(issue_comment, dict):
            issue_comment = IssueCommentOptions(**issue_comment)
        if isinstance(issues, dict):
            issues = IssuesOptions(**issues)
        if isinstance(label, dict):
            label = LabelOptions(**label)
        if isinstance(merge_group, dict):
            merge_group = MergeGroupOptions(**merge_group)
        if isinstance(milestone, dict):
            milestone = MilestoneOptions(**milestone)
        if isinstance(page_build, dict):
            page_build = PageBuildOptions(**page_build)
        if isinstance(project, dict):
            project = ProjectOptions(**project)
        if isinstance(project_card, dict):
            project_card = ProjectCardOptions(**project_card)
        if isinstance(project_column, dict):
            project_column = ProjectColumnOptions(**project_column)
        if isinstance(public, dict):
            public = PublicOptions(**public)
        if isinstance(pull_request, dict):
            pull_request = PullRequestOptions(**pull_request)
        if isinstance(pull_request_review, dict):
            pull_request_review = PullRequestReviewOptions(**pull_request_review)
        if isinstance(pull_request_review_comment, dict):
            pull_request_review_comment = PullRequestReviewCommentOptions(**pull_request_review_comment)
        if isinstance(pull_request_target, dict):
            pull_request_target = PullRequestTargetOptions(**pull_request_target)
        if isinstance(push, dict):
            push = PushOptions(**push)
        if isinstance(registry_package, dict):
            registry_package = RegistryPackageOptions(**registry_package)
        if isinstance(release, dict):
            release = ReleaseOptions(**release)
        if isinstance(repository_dispatch, dict):
            repository_dispatch = RepositoryDispatchOptions(**repository_dispatch)
        if isinstance(status, dict):
            status = StatusOptions(**status)
        if isinstance(watch, dict):
            watch = WatchOptions(**watch)
        if isinstance(workflow_call, dict):
            workflow_call = WorkflowCallOptions(**workflow_call)
        if isinstance(workflow_dispatch, dict):
            workflow_dispatch = WorkflowDispatchOptions(**workflow_dispatch)
        if isinstance(workflow_run, dict):
            workflow_run = WorkflowRunOptions(**workflow_run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252f759e84d601d9474266ff1dc7b2c70bc4a30664c418991e9d2b002e43b9d3)
            check_type(argname="argument branch_protection_rule", value=branch_protection_rule, expected_type=type_hints["branch_protection_rule"])
            check_type(argname="argument check_run", value=check_run, expected_type=type_hints["check_run"])
            check_type(argname="argument check_suite", value=check_suite, expected_type=type_hints["check_suite"])
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument deployment_status", value=deployment_status, expected_type=type_hints["deployment_status"])
            check_type(argname="argument discussion", value=discussion, expected_type=type_hints["discussion"])
            check_type(argname="argument discussion_comment", value=discussion_comment, expected_type=type_hints["discussion_comment"])
            check_type(argname="argument fork", value=fork, expected_type=type_hints["fork"])
            check_type(argname="argument gollum", value=gollum, expected_type=type_hints["gollum"])
            check_type(argname="argument issue_comment", value=issue_comment, expected_type=type_hints["issue_comment"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument merge_group", value=merge_group, expected_type=type_hints["merge_group"])
            check_type(argname="argument milestone", value=milestone, expected_type=type_hints["milestone"])
            check_type(argname="argument page_build", value=page_build, expected_type=type_hints["page_build"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument project_card", value=project_card, expected_type=type_hints["project_card"])
            check_type(argname="argument project_column", value=project_column, expected_type=type_hints["project_column"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument pull_request_review", value=pull_request_review, expected_type=type_hints["pull_request_review"])
            check_type(argname="argument pull_request_review_comment", value=pull_request_review_comment, expected_type=type_hints["pull_request_review_comment"])
            check_type(argname="argument pull_request_target", value=pull_request_target, expected_type=type_hints["pull_request_target"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
            check_type(argname="argument registry_package", value=registry_package, expected_type=type_hints["registry_package"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument repository_dispatch", value=repository_dispatch, expected_type=type_hints["repository_dispatch"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument watch", value=watch, expected_type=type_hints["watch"])
            check_type(argname="argument workflow_call", value=workflow_call, expected_type=type_hints["workflow_call"])
            check_type(argname="argument workflow_dispatch", value=workflow_dispatch, expected_type=type_hints["workflow_dispatch"])
            check_type(argname="argument workflow_run", value=workflow_run, expected_type=type_hints["workflow_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch_protection_rule is not None:
            self._values["branch_protection_rule"] = branch_protection_rule
        if check_run is not None:
            self._values["check_run"] = check_run
        if check_suite is not None:
            self._values["check_suite"] = check_suite
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if deployment is not None:
            self._values["deployment"] = deployment
        if deployment_status is not None:
            self._values["deployment_status"] = deployment_status
        if discussion is not None:
            self._values["discussion"] = discussion
        if discussion_comment is not None:
            self._values["discussion_comment"] = discussion_comment
        if fork is not None:
            self._values["fork"] = fork
        if gollum is not None:
            self._values["gollum"] = gollum
        if issue_comment is not None:
            self._values["issue_comment"] = issue_comment
        if issues is not None:
            self._values["issues"] = issues
        if label is not None:
            self._values["label"] = label
        if merge_group is not None:
            self._values["merge_group"] = merge_group
        if milestone is not None:
            self._values["milestone"] = milestone
        if page_build is not None:
            self._values["page_build"] = page_build
        if project is not None:
            self._values["project"] = project
        if project_card is not None:
            self._values["project_card"] = project_card
        if project_column is not None:
            self._values["project_column"] = project_column
        if public is not None:
            self._values["public"] = public
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if pull_request_review is not None:
            self._values["pull_request_review"] = pull_request_review
        if pull_request_review_comment is not None:
            self._values["pull_request_review_comment"] = pull_request_review_comment
        if pull_request_target is not None:
            self._values["pull_request_target"] = pull_request_target
        if push is not None:
            self._values["push"] = push
        if registry_package is not None:
            self._values["registry_package"] = registry_package
        if release is not None:
            self._values["release"] = release
        if repository_dispatch is not None:
            self._values["repository_dispatch"] = repository_dispatch
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status
        if watch is not None:
            self._values["watch"] = watch
        if workflow_call is not None:
            self._values["workflow_call"] = workflow_call
        if workflow_dispatch is not None:
            self._values["workflow_dispatch"] = workflow_dispatch
        if workflow_run is not None:
            self._values["workflow_run"] = workflow_run

    @builtins.property
    def branch_protection_rule(self) -> typing.Optional[BranchProtectionRuleOptions]:
        '''(experimental) Runs your workflow anytime the branch_protection_rule event occurs.

        :stability: experimental
        '''
        result = self._values.get("branch_protection_rule")
        return typing.cast(typing.Optional[BranchProtectionRuleOptions], result)

    @builtins.property
    def check_run(self) -> typing.Optional[CheckRunOptions]:
        '''(experimental) Runs your workflow anytime the check_run event occurs.

        :stability: experimental
        '''
        result = self._values.get("check_run")
        return typing.cast(typing.Optional[CheckRunOptions], result)

    @builtins.property
    def check_suite(self) -> typing.Optional[CheckSuiteOptions]:
        '''(experimental) Runs your workflow anytime the check_suite event occurs.

        :stability: experimental
        '''
        result = self._values.get("check_suite")
        return typing.cast(typing.Optional[CheckSuiteOptions], result)

    @builtins.property
    def create(self) -> typing.Optional[CreateOptions]:
        '''(experimental) Runs your workflow anytime someone creates a branch or tag, which triggers the create event.

        :stability: experimental
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[CreateOptions], result)

    @builtins.property
    def delete(self) -> typing.Optional[DeleteOptions]:
        '''(experimental) Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.

        :stability: experimental
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[DeleteOptions], result)

    @builtins.property
    def deployment(self) -> typing.Optional[DeploymentOptions]:
        '''(experimental) Runs your workflow anytime someone creates a deployment, which triggers the deployment event.

        Deployments created with a commit SHA may not have
        a Git ref.

        :stability: experimental
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional[DeploymentOptions], result)

    @builtins.property
    def deployment_status(self) -> typing.Optional[DeploymentStatusOptions]:
        '''(experimental) Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event.

        Deployments created with a
        commit SHA may not have a Git ref.

        :stability: experimental
        '''
        result = self._values.get("deployment_status")
        return typing.cast(typing.Optional[DeploymentStatusOptions], result)

    @builtins.property
    def discussion(self) -> typing.Optional[DiscussionOptions]:
        '''(experimental) Runs your workflow anytime the discussion event occurs.

        More than one activity type triggers this event.

        :see: https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions
        :stability: experimental
        '''
        result = self._values.get("discussion")
        return typing.cast(typing.Optional[DiscussionOptions], result)

    @builtins.property
    def discussion_comment(self) -> typing.Optional[DiscussionCommentOptions]:
        '''(experimental) Runs your workflow anytime the discussion_comment event occurs.

        More than one activity type triggers this event.

        :see: https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions
        :stability: experimental
        '''
        result = self._values.get("discussion_comment")
        return typing.cast(typing.Optional[DiscussionCommentOptions], result)

    @builtins.property
    def fork(self) -> typing.Optional[ForkOptions]:
        '''(experimental) Runs your workflow anytime when someone forks a repository, which triggers the fork event.

        :stability: experimental
        '''
        result = self._values.get("fork")
        return typing.cast(typing.Optional[ForkOptions], result)

    @builtins.property
    def gollum(self) -> typing.Optional[GollumOptions]:
        '''(experimental) Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.

        :stability: experimental
        '''
        result = self._values.get("gollum")
        return typing.cast(typing.Optional[GollumOptions], result)

    @builtins.property
    def issue_comment(self) -> typing.Optional[IssueCommentOptions]:
        '''(experimental) Runs your workflow anytime the issue_comment event occurs.

        :stability: experimental
        '''
        result = self._values.get("issue_comment")
        return typing.cast(typing.Optional[IssueCommentOptions], result)

    @builtins.property
    def issues(self) -> typing.Optional[IssuesOptions]:
        '''(experimental) Runs your workflow anytime the issues event occurs.

        :stability: experimental
        '''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[IssuesOptions], result)

    @builtins.property
    def label(self) -> typing.Optional[LabelOptions]:
        '''(experimental) Runs your workflow anytime the label event occurs.

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[LabelOptions], result)

    @builtins.property
    def merge_group(self) -> typing.Optional[MergeGroupOptions]:
        '''(experimental) Runs your workflow when a pull request is added to a merge queue, which adds the pull request to a merge group.

        :stability: experimental
        '''
        result = self._values.get("merge_group")
        return typing.cast(typing.Optional[MergeGroupOptions], result)

    @builtins.property
    def milestone(self) -> typing.Optional[MilestoneOptions]:
        '''(experimental) Runs your workflow anytime the milestone event occurs.

        :stability: experimental
        '''
        result = self._values.get("milestone")
        return typing.cast(typing.Optional[MilestoneOptions], result)

    @builtins.property
    def page_build(self) -> typing.Optional[PageBuildOptions]:
        '''(experimental) Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.

        :stability: experimental
        '''
        result = self._values.get("page_build")
        return typing.cast(typing.Optional[PageBuildOptions], result)

    @builtins.property
    def project(self) -> typing.Optional[ProjectOptions]:
        '''(experimental) Runs your workflow anytime the project event occurs.

        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[ProjectOptions], result)

    @builtins.property
    def project_card(self) -> typing.Optional[ProjectCardOptions]:
        '''(experimental) Runs your workflow anytime the project_card event occurs.

        :stability: experimental
        '''
        result = self._values.get("project_card")
        return typing.cast(typing.Optional[ProjectCardOptions], result)

    @builtins.property
    def project_column(self) -> typing.Optional[ProjectColumnOptions]:
        '''(experimental) Runs your workflow anytime the project_column event occurs.

        :stability: experimental
        '''
        result = self._values.get("project_column")
        return typing.cast(typing.Optional[ProjectColumnOptions], result)

    @builtins.property
    def public(self) -> typing.Optional[PublicOptions]:
        '''(experimental) Runs your workflow anytime someone makes a private repository public, which triggers the public event.

        :stability: experimental
        '''
        result = self._values.get("public")
        return typing.cast(typing.Optional[PublicOptions], result)

    @builtins.property
    def pull_request(self) -> typing.Optional["PullRequestOptions"]:
        '''(experimental) Runs your workflow anytime the pull_request event occurs.

        :stability: experimental
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["PullRequestOptions"], result)

    @builtins.property
    def pull_request_review(self) -> typing.Optional[PullRequestReviewOptions]:
        '''(experimental) Runs your workflow anytime the pull_request_review event occurs.

        :stability: experimental
        '''
        result = self._values.get("pull_request_review")
        return typing.cast(typing.Optional[PullRequestReviewOptions], result)

    @builtins.property
    def pull_request_review_comment(
        self,
    ) -> typing.Optional[PullRequestReviewCommentOptions]:
        '''(experimental) Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.

        :stability: experimental
        '''
        result = self._values.get("pull_request_review_comment")
        return typing.cast(typing.Optional[PullRequestReviewCommentOptions], result)

    @builtins.property
    def pull_request_target(self) -> typing.Optional["PullRequestTargetOptions"]:
        '''(experimental) This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does.

        This prevents
        executing unsafe workflow code from the head of the pull request that
        could alter your repository or steal any secrets you use in your workflow.
        This event allows you to do things like create workflows that label and
        comment on pull requests based on the contents of the event payload.

        WARNING: The ``pull_request_target`` event is granted read/write repository
        token and can access secrets, even when it is triggered from a fork.
        Although the workflow runs in the context of the base of the pull request,
        you should make sure that you do not check out, build, or run untrusted
        code from the pull request with this event. Additionally, any caches
        share the same scope as the base branch, and to help prevent cache
        poisoning, you should not save the cache if there is a possibility that
        the cache contents were altered.

        :see: https://securitylab.github.com/research/github-actions-preventing-pwn-requests
        :stability: experimental
        '''
        result = self._values.get("pull_request_target")
        return typing.cast(typing.Optional["PullRequestTargetOptions"], result)

    @builtins.property
    def push(self) -> typing.Optional[PushOptions]:
        '''(experimental) Runs your workflow when someone pushes to a repository branch, which triggers the push event.

        :stability: experimental
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional[PushOptions], result)

    @builtins.property
    def registry_package(self) -> typing.Optional[RegistryPackageOptions]:
        '''(experimental) Runs your workflow anytime a package is published or updated.

        :stability: experimental
        '''
        result = self._values.get("registry_package")
        return typing.cast(typing.Optional[RegistryPackageOptions], result)

    @builtins.property
    def release(self) -> typing.Optional[ReleaseOptions]:
        '''(experimental) Runs your workflow anytime the release event occurs.

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[ReleaseOptions], result)

    @builtins.property
    def repository_dispatch(self) -> typing.Optional[RepositoryDispatchOptions]:
        '''(experimental) You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.

        :stability: experimental
        '''
        result = self._values.get("repository_dispatch")
        return typing.cast(typing.Optional[RepositoryDispatchOptions], result)

    @builtins.property
    def schedule(self) -> typing.Optional[typing.List[CronScheduleOptions]]:
        '''(experimental) You can schedule a workflow to run at specific UTC times using POSIX cron syntax.

        Scheduled workflows run on the latest commit on the default or
        base branch. The shortest interval you can run scheduled workflows is
        once every 5 minutes.

        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.List[CronScheduleOptions]], result)

    @builtins.property
    def status(self) -> typing.Optional[StatusOptions]:
        '''(experimental) Runs your workflow anytime the status of a Git commit changes, which triggers the status event.

        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[StatusOptions], result)

    @builtins.property
    def watch(self) -> typing.Optional["WatchOptions"]:
        '''(experimental) Runs your workflow anytime the watch event occurs.

        :stability: experimental
        '''
        result = self._values.get("watch")
        return typing.cast(typing.Optional["WatchOptions"], result)

    @builtins.property
    def workflow_call(self) -> typing.Optional["WorkflowCallOptions"]:
        '''(experimental) Can be called from another workflow.

        :see: https://docs.github.com/en/actions/learn-github-actions/reusing-workflows
        :stability: experimental
        '''
        result = self._values.get("workflow_call")
        return typing.cast(typing.Optional["WorkflowCallOptions"], result)

    @builtins.property
    def workflow_dispatch(self) -> typing.Optional["WorkflowDispatchOptions"]:
        '''(experimental) You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow.

        When the
        workflow runs, you can access the input values in the github.event.inputs
        context.

        :stability: experimental
        '''
        result = self._values.get("workflow_dispatch")
        return typing.cast(typing.Optional["WorkflowDispatchOptions"], result)

    @builtins.property
    def workflow_run(self) -> typing.Optional["WorkflowRunOptions"]:
        '''(experimental) This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow.

        A workflow run is triggered regardless of the result of the
        previous workflow.

        :stability: experimental
        '''
        result = self._values.get("workflow_run")
        return typing.cast(typing.Optional["WorkflowRunOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Triggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.WatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Watch options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b802e2c64940a026e155d7eed07be19bc7ff95ded67b900f0ebb5c8ebaf2e0a)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.WorkflowCallOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkflowCallOptions:
    def __init__(self) -> None:
        '''(experimental) The Workflow Call event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowCallOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.WorkflowDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkflowDispatchOptions:
    def __init__(self) -> None:
        '''(experimental) The Workflow dispatch event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.WorkflowRunOptions",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches", "types": "types", "workflows": "workflows"},
)
class WorkflowRunOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflows: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Workflow run options.

        :param branches: (experimental) Which branches or branch-ignore to limit the trigger to.
        :param types: (experimental) Which activity types to trigger on.
        :param workflows: (experimental) Which workflow to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585f016972d6eec9e010fe83a5c43507031992141443c1f2e89e954a93653cb7)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if types is not None:
            self._values["types"] = types
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which branches or branch-ignore to limit the trigger to.

        :stability: experimental
        :defaults: - no branch limits
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflows(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which workflow to trigger on.

        :stability: experimental
        :defaults: - any workflows
        '''
        result = self._values.get("workflows")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.JobStepConfiguration",
    jsii_struct_bases=[StepConfiguration],
    name_mapping={
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "shell": "shell",
        "working_directory": "workingDirectory",
        "continue_on_error": "continueOnError",
        "timeout_minutes": "timeoutMinutes",
    },
)
class JobStepConfiguration(StepConfiguration):
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) These settings are unique to a JobStep from the fields contained within the metadata action.yaml file present in when creating a new GitHub Action. These fields are not present in action.yml, but are in JobStep, which are using when creating workflows.

        :param env: (experimental) Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: (experimental) A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) A name for your step to display on GitHub.
        :param shell: (experimental) Overrides the default shell settings in the runner's operating system and the job's default. Refer to GitHub documentation for allowed values.
        :param working_directory: (experimental) Specifies a working directory for a step. Overrides a job's working directory.
        :param continue_on_error: (experimental) Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.
        :param timeout_minutes: (experimental) The maximum number of minutes to run the step before killing the process.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015947eea91a5bd0b89e515aeca63fc47bd80c9c63472b7c37f32a247b878ba9)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique identifier for the step.

        You can use the id to reference the
        step in contexts.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for your step to display on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Overrides the default shell settings in the runner's operating system and the job's default.

        Refer to GitHub documentation for allowed values.

        :see: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsshell
        :stability: experimental
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies a working directory for a step.

        Overrides a job's working directory.

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevents a job from failing when a step fails.

        Set to true to allow a job
        to pass when this step fails.

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of minutes to run the step before killing the process.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStepConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.PullRequestOptions",
    jsii_struct_bases=[PushOptions],
    name_mapping={
        "branches": "branches",
        "paths": "paths",
        "tags": "tags",
        "types": "types",
    },
)
class PullRequestOptions(PushOptions):
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request options.

        :param branches: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f89a958393ccc6e519bb6f35efb7b5890d5f02f862fb898a55f18fadb17bd8)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.PullRequestTargetOptions",
    jsii_struct_bases=[PushOptions],
    name_mapping={
        "branches": "branches",
        "paths": "paths",
        "tags": "tags",
        "types": "types",
    },
)
class PullRequestTargetOptions(PushOptions):
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request target options.

        :param branches: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: (experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca7cc715b84ec3cf61f2ce2a905a0d5ec7555e282d1ce9b79e5c3773fe5c25a)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push, pull_request and pull_request_target events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.Step",
    jsii_struct_bases=[StepConfiguration],
    name_mapping={
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "shell": "shell",
        "working_directory": "workingDirectory",
        "run": "run",
        "uses": "uses",
        "with_": "with",
    },
)
class Step(StepConfiguration):
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
        run: typing.Optional[builtins.str] = None,
        uses: typing.Optional[builtins.str] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) This contains the fields that are common amongst both: - JobStep, which is a step that is part of a Job in Github Actions.

        This is by far the most common use case.

        - The metadata file ``action.yaml`` that is used to define an Action when you are creating one. As in, if you were creating an Action to be used in a JobStep.
          There is some overlap between the two, and this captures that overlap.

        :param env: (experimental) Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: (experimental) A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) A name for your step to display on GitHub.
        :param shell: (experimental) Overrides the default shell settings in the runner's operating system and the job's default. Refer to GitHub documentation for allowed values.
        :param working_directory: (experimental) Specifies a working directory for a step. Overrides a job's working directory.
        :param run: (experimental) Runs command-line programs using the operating system's shell. If you do not provide a name, the step name will default to the text specified in the run command.
        :param uses: (experimental) Selects an action to run as part of a step in your job. An action is a reusable unit of code. You can use an action defined in the same repository as the workflow, a public repository, or in a published Docker container image.
        :param with_: (experimental) A map of the input parameters defined by the action. Each input parameter is a key/value pair. Input parameters are set as environment variables. The variable is prefixed with INPUT_ and converted to upper case.

        :see: https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91711bdec7a542de93f053fdd93de2213c56069702113a10e2c71564ce543ff2)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument with_", value=with_, expected_type=type_hints["with_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory
        if run is not None:
            self._values["run"] = run
        if uses is not None:
            self._values["uses"] = uses
        if with_ is not None:
            self._values["with_"] = with_

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique identifier for the step.

        You can use the id to reference the
        step in contexts.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for your step to display on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Overrides the default shell settings in the runner's operating system and the job's default.

        Refer to GitHub documentation for allowed values.

        :see: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsshell
        :stability: experimental
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies a working directory for a step.

        Overrides a job's working directory.

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run(self) -> typing.Optional[builtins.str]:
        '''(experimental) Runs command-line programs using the operating system's shell.

        If you do
        not provide a name, the step name will default to the text specified in
        the run command.

        :stability: experimental
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uses(self) -> typing.Optional[builtins.str]:
        '''(experimental) Selects an action to run as part of a step in your job.

        An action is a
        reusable unit of code. You can use an action defined in the same
        repository as the workflow, a public repository, or in a published Docker
        container image.

        :stability: experimental
        '''
        result = self._values.get("uses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) A map of the input parameters defined by the action.

        Each input parameter
        is a key/value pair. Input parameters are set as environment variables.
        The variable is prefixed with INPUT_ and converted to upper case.

        :stability: experimental
        '''
        result = self._values.get("with_")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Step(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.workflows.JobStep",
    jsii_struct_bases=[Step, JobStepConfiguration],
    name_mapping={
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "shell": "shell",
        "working_directory": "workingDirectory",
        "run": "run",
        "uses": "uses",
        "with_": "with",
        "continue_on_error": "continueOnError",
        "timeout_minutes": "timeoutMinutes",
    },
)
class JobStep(Step, JobStepConfiguration):
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
        run: typing.Optional[builtins.str] = None,
        uses: typing.Optional[builtins.str] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) JobSteps run as part of a GitHub Workflow Job.

        :param env: (experimental) Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: (experimental) A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) A name for your step to display on GitHub.
        :param shell: (experimental) Overrides the default shell settings in the runner's operating system and the job's default. Refer to GitHub documentation for allowed values.
        :param working_directory: (experimental) Specifies a working directory for a step. Overrides a job's working directory.
        :param run: (experimental) Runs command-line programs using the operating system's shell. If you do not provide a name, the step name will default to the text specified in the run command.
        :param uses: (experimental) Selects an action to run as part of a step in your job. An action is a reusable unit of code. You can use an action defined in the same repository as the workflow, a public repository, or in a published Docker container image.
        :param with_: (experimental) A map of the input parameters defined by the action. Each input parameter is a key/value pair. Input parameters are set as environment variables. The variable is prefixed with INPUT_ and converted to upper case.
        :param continue_on_error: (experimental) Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.
        :param timeout_minutes: (experimental) The maximum number of minutes to run the step before killing the process.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df3f4a2690eb7ddc82908948a9807cfdc9923a4466ac38225eda950e85a59ff)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument with_", value=with_, expected_type=type_hints["with_"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory
        if run is not None:
            self._values["run"] = run
        if uses is not None:
            self._values["uses"] = uses
        if with_ is not None:
            self._values["with_"] = with_
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique identifier for the step.

        You can use the id to reference the
        step in contexts.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for your step to display on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Overrides the default shell settings in the runner's operating system and the job's default.

        Refer to GitHub documentation for allowed values.

        :see: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsshell
        :stability: experimental
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies a working directory for a step.

        Overrides a job's working directory.

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run(self) -> typing.Optional[builtins.str]:
        '''(experimental) Runs command-line programs using the operating system's shell.

        If you do
        not provide a name, the step name will default to the text specified in
        the run command.

        :stability: experimental
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uses(self) -> typing.Optional[builtins.str]:
        '''(experimental) Selects an action to run as part of a step in your job.

        An action is a
        reusable unit of code. You can use an action defined in the same
        repository as the workflow, a public repository, or in a published Docker
        container image.

        :stability: experimental
        '''
        result = self._values.get("uses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) A map of the input parameters defined by the action.

        Each input parameter
        is a key/value pair. Input parameters are set as environment variables.
        The variable is prefixed with INPUT_ and converted to upper case.

        :stability: experimental
        '''
        result = self._values.get("with_")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevents a job from failing when a step fails.

        Set to true to allow a job
        to pass when this step fails.

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of minutes to run the step before killing the process.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppPermission",
    "AppPermissions",
    "BranchProtectionRuleOptions",
    "CheckRunOptions",
    "CheckSuiteOptions",
    "CommonJobDefinition",
    "ContainerCredentials",
    "ContainerOptions",
    "CreateOptions",
    "CronScheduleOptions",
    "DeleteOptions",
    "DeploymentOptions",
    "DeploymentStatusOptions",
    "DiscussionCommentOptions",
    "DiscussionOptions",
    "ForkOptions",
    "GollumOptions",
    "IssueCommentOptions",
    "IssuesOptions",
    "Job",
    "JobCallingReusableWorkflow",
    "JobDefaults",
    "JobMatrix",
    "JobPermission",
    "JobPermissions",
    "JobStep",
    "JobStepConfiguration",
    "JobStepOutput",
    "JobStrategy",
    "LabelOptions",
    "MergeGroupOptions",
    "MilestoneOptions",
    "PageBuildOptions",
    "ProjectCardOptions",
    "ProjectColumnOptions",
    "ProjectOptions",
    "PublicOptions",
    "PullRequestOptions",
    "PullRequestReviewCommentOptions",
    "PullRequestReviewOptions",
    "PullRequestTargetOptions",
    "PushOptions",
    "RegistryPackageOptions",
    "ReleaseOptions",
    "RepositoryDispatchOptions",
    "RunSettings",
    "StatusOptions",
    "Step",
    "StepConfiguration",
    "ToolRequirement",
    "Tools",
    "Triggers",
    "WatchOptions",
    "WorkflowCallOptions",
    "WorkflowDispatchOptions",
    "WorkflowRunOptions",
]

publication.publish()

def _typecheckingstub__6e0085e134a87f8de8cb54bc56e329333881c3520710c833f5ed76097c8d1299(
    *,
    actions: typing.Optional[AppPermission] = None,
    administration: typing.Optional[AppPermission] = None,
    attestations: typing.Optional[AppPermission] = None,
    checks: typing.Optional[AppPermission] = None,
    codespaces: typing.Optional[AppPermission] = None,
    contents: typing.Optional[AppPermission] = None,
    dependabot_secrets: typing.Optional[AppPermission] = None,
    deployments: typing.Optional[AppPermission] = None,
    email_addresses: typing.Optional[AppPermission] = None,
    environments: typing.Optional[AppPermission] = None,
    followers: typing.Optional[AppPermission] = None,
    git_ssh_keys: typing.Optional[AppPermission] = None,
    gpg_keys: typing.Optional[AppPermission] = None,
    interaction_limits: typing.Optional[AppPermission] = None,
    issues: typing.Optional[AppPermission] = None,
    members: typing.Optional[AppPermission] = None,
    metadata: typing.Optional[AppPermission] = None,
    organization_administration: typing.Optional[AppPermission] = None,
    organization_announcement_banners: typing.Optional[AppPermission] = None,
    organization_copilot_seat_management: typing.Optional[AppPermission] = None,
    organization_custom_org_roles: typing.Optional[AppPermission] = None,
    organization_custom_properties: typing.Optional[AppPermission] = None,
    organization_custom_roles: typing.Optional[AppPermission] = None,
    organization_events: typing.Optional[AppPermission] = None,
    organization_hooks: typing.Optional[AppPermission] = None,
    organization_packages: typing.Optional[AppPermission] = None,
    organization_personal_access_token_requests: typing.Optional[AppPermission] = None,
    organization_personal_access_tokens: typing.Optional[AppPermission] = None,
    organization_plan: typing.Optional[AppPermission] = None,
    organization_projects: typing.Optional[AppPermission] = None,
    organization_secrets: typing.Optional[AppPermission] = None,
    organization_self_hosted_runners: typing.Optional[AppPermission] = None,
    orgnaization_user_blocking: typing.Optional[AppPermission] = None,
    packages: typing.Optional[AppPermission] = None,
    pages: typing.Optional[AppPermission] = None,
    profile: typing.Optional[AppPermission] = None,
    pull_requests: typing.Optional[AppPermission] = None,
    repository_announcement_banners: typing.Optional[AppPermission] = None,
    repository_custom_properties: typing.Optional[AppPermission] = None,
    repository_hooks: typing.Optional[AppPermission] = None,
    repository_projects: typing.Optional[AppPermission] = None,
    secrets: typing.Optional[AppPermission] = None,
    secret_scanning_alerts: typing.Optional[AppPermission] = None,
    security_events: typing.Optional[AppPermission] = None,
    single_file: typing.Optional[AppPermission] = None,
    starring: typing.Optional[AppPermission] = None,
    statuses: typing.Optional[AppPermission] = None,
    team_discussions: typing.Optional[AppPermission] = None,
    vulnerability_alerts: typing.Optional[AppPermission] = None,
    workflows: typing.Optional[AppPermission] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c11d1dd0003925c76d3c0071c26d26436e2dec53d9ad08c4e3abe2db2c75e91(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4347e11acd26f11508a618d0b238a95d67a7f80349876130ff38e9061f584370(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b40134ecf1ce3d1252c6d518b83fbd48bccf3592878c8a25a5e61380cc82b3(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2014a638b9f0a055f9914f90ac8de197a8741af9ed5179f476f1c565146134(
    *,
    permissions: typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]],
    concurrency: typing.Any = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    strategy: typing.Optional[typing.Union[JobStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c068cd566cf3598395667d999333ef7561bfd204ce91a842b6f660134873bf5(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3745b83f4463c4fc52b9717275f5271dfc3bca86f6f6742576a53ec8359dbb05(
    *,
    image: builtins.str,
    credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b942d3c2ff8727f2ff55175941fa65b503b9b9b5509291efe52190850c93afaa(
    *,
    cron: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af138b824decbcd8cf918b7d2032093418049a345b01ed01f88accfcee395b5a(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97467ebe6e40905d2acd015311e4fbde640f5ab410b74b1de055967ddf4e771(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217e744007dbc2c9e22b6c0ad4aa07d2a4711631c6fc1de1414dea628db3841b(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86720be0c98429300bca3b757935fb0a6d341673f54d031b808b1f9d1b3512e3(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b405f548924ed15a8a6902fcc20e3f048e3450d8a016b7904ed920f64aab582(
    *,
    permissions: typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]],
    concurrency: typing.Any = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    strategy: typing.Optional[typing.Union[JobStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    steps: typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]],
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[JobDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Any = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, typing.Union[JobStepOutput, typing.Dict[builtins.str, typing.Any]]]] = None,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    tools: typing.Optional[typing.Union[Tools, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9905a897c84934e8ed2bde6e0bd6fdd798275b2a8b89a503c19dba40649562(
    *,
    permissions: typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]],
    concurrency: typing.Any = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    strategy: typing.Optional[typing.Union[JobStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    uses: builtins.str,
    secrets: typing.Optional[typing.Union[builtins.str, typing.Mapping[builtins.str, builtins.str]]] = None,
    with_: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afc181ec4ce3844469de535090d57cb39b9f47cf28d0bdc1e7a95bf29c34199(
    *,
    run: typing.Optional[typing.Union[RunSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c1bb692367ba40c0c0307ec4a86916287ff1f39e99b1eeab7f30bb7886bbda(
    *,
    domain: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool]]]]] = None,
    exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]] = None,
    include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9b6a3fbdc58e402a1aaac55747b5faedde783c61dcd4c97c759406d925e9a5(
    *,
    actions: typing.Optional[JobPermission] = None,
    attestations: typing.Optional[JobPermission] = None,
    checks: typing.Optional[JobPermission] = None,
    contents: typing.Optional[JobPermission] = None,
    deployments: typing.Optional[JobPermission] = None,
    discussions: typing.Optional[JobPermission] = None,
    id_token: typing.Optional[JobPermission] = None,
    issues: typing.Optional[JobPermission] = None,
    models: typing.Optional[JobPermission] = None,
    packages: typing.Optional[JobPermission] = None,
    pages: typing.Optional[JobPermission] = None,
    pull_requests: typing.Optional[JobPermission] = None,
    repository_projects: typing.Optional[JobPermission] = None,
    security_events: typing.Optional[JobPermission] = None,
    statuses: typing.Optional[JobPermission] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54660692cd1951dfa8376b33c95c26d58e87bbafc6ed590fb6fe9216ce01ba7(
    *,
    output_name: builtins.str,
    step_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134570ab28cf6023a626f13de20038e5ad2ad2ee907973354ce8dd6e36636499(
    *,
    fail_fast: typing.Optional[builtins.bool] = None,
    matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[builtins.str, typing.Any]]] = None,
    max_parallel: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50bb7bfbc56deada571dfd117b208118a0999144362cd066f2fa72083f2dbde6(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1bf8c4c650a790f23377cc4e527f5235804e0ede24bec6d08006307448d1da2(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82a3af3c1c9a05cdcbb3e82973ff2c7209b0845f46e0f375d7b1b923b61c594(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cd16cd68d37babc3afecf26110f73a792b6caee362abfc413ead1fec8f686f(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16dee1fa11035cd0fd9d7774dd224981d0fd92e7c44649b8af742e00f8c80f5d(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a3bdc315041b645bf04461deaf270cc61bdfc779c62610457121f16d55f943(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924a9205551b733fad7955355cf317e09d79435bc464c13625ab82a4083b4eeb(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa7e340b849b51a5bbea8528f24bc797b353586438c6d939f514b86f547b2c9(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1b5ef2dd2ebfefd88be7a903d4676960437a284d29f5ac056b2cdde3f62932(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d555b19711887db4995273ee0e8c73ea2c0546a60c3796166a1f4419dd61e73c(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119a914e5bfb3cdea007b3544b187a2e3b2ab765b6fe743053491bc2496fede7(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf1842c4c0435b3b65c1c33f941a09c9bd78ebb950136703bc50a6a6ee27adf(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613ab93b76c86dd88502480397a66c39b983fc805b068e953f6ad756edee792e(
    *,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044349b8d18055b991a5680dc1d218dc2901bc2369d30fa23e79229d8bde3b73(
    *,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49e39102f958d999716dd94aae1647a49fe1d2fd3d73add88292e5067592c14(
    *,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dab9f9edea4d6d3c0897aa6348f12a4359741f0e29873be48495120ea2a4b12(
    *,
    dotnet: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    go: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    java: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    node: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
    python: typing.Optional[typing.Union[ToolRequirement, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252f759e84d601d9474266ff1dc7b2c70bc4a30664c418991e9d2b002e43b9d3(
    *,
    branch_protection_rule: typing.Optional[typing.Union[BranchProtectionRuleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    create: typing.Optional[typing.Union[CreateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    discussion: typing.Optional[typing.Union[DiscussionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    discussion_comment: typing.Optional[typing.Union[DiscussionCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    merge_group: typing.Optional[typing.Union[MergeGroupOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    public: typing.Optional[typing.Union[PublicOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_target: typing.Optional[typing.Union[PullRequestTargetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[typing.Union[StatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_call: typing.Optional[typing.Union[WorkflowCallOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_dispatch: typing.Optional[typing.Union[WorkflowDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b802e2c64940a026e155d7eed07be19bc7ff95ded67b900f0ebb5c8ebaf2e0a(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585f016972d6eec9e010fe83a5c43507031992141443c1f2e89e954a93653cb7(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflows: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015947eea91a5bd0b89e515aeca63fc47bd80c9c63472b7c37f32a247b878ba9(
    *,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f89a958393ccc6e519bb6f35efb7b5890d5f02f862fb898a55f18fadb17bd8(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca7cc715b84ec3cf61f2ce2a905a0d5ec7555e282d1ce9b79e5c3773fe5c25a(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91711bdec7a542de93f053fdd93de2213c56069702113a10e2c71564ce543ff2(
    *,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
    run: typing.Optional[builtins.str] = None,
    uses: typing.Optional[builtins.str] = None,
    with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df3f4a2690eb7ddc82908948a9807cfdc9923a4466ac38225eda950e85a59ff(
    *,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
    run: typing.Optional[builtins.str] = None,
    uses: typing.Optional[builtins.str] = None,
    with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
