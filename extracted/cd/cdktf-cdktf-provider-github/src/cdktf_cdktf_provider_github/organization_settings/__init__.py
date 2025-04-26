r'''
# `github_organization_settings`

Refer to the Terraform Registry for docs: [`github_organization_settings`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings).
'''
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class OrganizationSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationSettings.OrganizationSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings github_organization_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        billing_email: builtins.str,
        advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        blog: typing.Optional[builtins.str] = None,
        company: typing.Optional[builtins.str] = None,
        default_repository_permission: typing.Optional[builtins.str] = None,
        dependabot_alerts_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependabot_security_updates_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependency_graph_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        has_organization_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_repository_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        members_can_create_internal_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_private_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_public_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_public_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_fork_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter_username: typing.Optional[builtins.str] = None,
        web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings github_organization_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param billing_email: The billing email address for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#billing_email OrganizationSettings#billing_email}
        :param advanced_security_enabled_for_new_repositories: Whether or not advanced security is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#advanced_security_enabled_for_new_repositories OrganizationSettings#advanced_security_enabled_for_new_repositories}
        :param blog: The blog URL for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#blog OrganizationSettings#blog}
        :param company: The company name for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#company OrganizationSettings#company}
        :param default_repository_permission: The default permission for organization members to create new repositories. Can be one of 'read', 'write', 'admin' or 'none'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#default_repository_permission OrganizationSettings#default_repository_permission}
        :param dependabot_alerts_enabled_for_new_repositories: Whether or not dependabot alerts are enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependabot_alerts_enabled_for_new_repositories OrganizationSettings#dependabot_alerts_enabled_for_new_repositories}
        :param dependabot_security_updates_enabled_for_new_repositories: Whether or not dependabot security updates are enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependabot_security_updates_enabled_for_new_repositories OrganizationSettings#dependabot_security_updates_enabled_for_new_repositories}
        :param dependency_graph_enabled_for_new_repositories: Whether or not dependency graph is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependency_graph_enabled_for_new_repositories OrganizationSettings#dependency_graph_enabled_for_new_repositories}
        :param description: The description for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#description OrganizationSettings#description}
        :param email: The email address for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#email OrganizationSettings#email}
        :param has_organization_projects: Whether or not organization projects are enabled for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#has_organization_projects OrganizationSettings#has_organization_projects}
        :param has_repository_projects: Whether or not repository projects are enabled for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#has_repository_projects OrganizationSettings#has_repository_projects}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#id OrganizationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#location OrganizationSettings#location}
        :param members_can_create_internal_repositories: Whether or not organization members can create new internal repositories. For Enterprise Organizations only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_internal_repositories OrganizationSettings#members_can_create_internal_repositories}
        :param members_can_create_pages: Whether or not organization members can create new pages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_pages OrganizationSettings#members_can_create_pages}
        :param members_can_create_private_pages: Whether or not organization members can create new private pages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_private_pages OrganizationSettings#members_can_create_private_pages}
        :param members_can_create_private_repositories: Whether or not organization members can create new private repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_private_repositories OrganizationSettings#members_can_create_private_repositories}
        :param members_can_create_public_pages: Whether or not organization members can create new public pages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_public_pages OrganizationSettings#members_can_create_public_pages}
        :param members_can_create_public_repositories: Whether or not organization members can create new public repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_public_repositories OrganizationSettings#members_can_create_public_repositories}
        :param members_can_create_repositories: Whether or not organization members can create new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_repositories OrganizationSettings#members_can_create_repositories}
        :param members_can_fork_private_repositories: Whether or not organization members can fork private repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_fork_private_repositories OrganizationSettings#members_can_fork_private_repositories}
        :param name: The name for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#name OrganizationSettings#name}
        :param secret_scanning_enabled_for_new_repositories: Whether or not secret scanning is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#secret_scanning_enabled_for_new_repositories OrganizationSettings#secret_scanning_enabled_for_new_repositories}
        :param secret_scanning_push_protection_enabled_for_new_repositories: Whether or not secret scanning push protection is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#secret_scanning_push_protection_enabled_for_new_repositories OrganizationSettings#secret_scanning_push_protection_enabled_for_new_repositories}
        :param twitter_username: The Twitter username for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#twitter_username OrganizationSettings#twitter_username}
        :param web_commit_signoff_required: Whether or not commit signatures are required for commits to the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#web_commit_signoff_required OrganizationSettings#web_commit_signoff_required}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff26516a1a18b7ae1005dd371a79b7f18a58f1ed21b7f09cacc79d89bb790079)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrganizationSettingsConfig(
            billing_email=billing_email,
            advanced_security_enabled_for_new_repositories=advanced_security_enabled_for_new_repositories,
            blog=blog,
            company=company,
            default_repository_permission=default_repository_permission,
            dependabot_alerts_enabled_for_new_repositories=dependabot_alerts_enabled_for_new_repositories,
            dependabot_security_updates_enabled_for_new_repositories=dependabot_security_updates_enabled_for_new_repositories,
            dependency_graph_enabled_for_new_repositories=dependency_graph_enabled_for_new_repositories,
            description=description,
            email=email,
            has_organization_projects=has_organization_projects,
            has_repository_projects=has_repository_projects,
            id=id,
            location=location,
            members_can_create_internal_repositories=members_can_create_internal_repositories,
            members_can_create_pages=members_can_create_pages,
            members_can_create_private_pages=members_can_create_private_pages,
            members_can_create_private_repositories=members_can_create_private_repositories,
            members_can_create_public_pages=members_can_create_public_pages,
            members_can_create_public_repositories=members_can_create_public_repositories,
            members_can_create_repositories=members_can_create_repositories,
            members_can_fork_private_repositories=members_can_fork_private_repositories,
            name=name,
            secret_scanning_enabled_for_new_repositories=secret_scanning_enabled_for_new_repositories,
            secret_scanning_push_protection_enabled_for_new_repositories=secret_scanning_push_protection_enabled_for_new_repositories,
            twitter_username=twitter_username,
            web_commit_signoff_required=web_commit_signoff_required,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a OrganizationSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrganizationSettings to import.
        :param import_from_id: The id of the existing OrganizationSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrganizationSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debfca161615eb49a2b3f3c91f61bba3caa08876a249f0b040f55dc3490d50f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAdvancedSecurityEnabledForNewRepositories")
    def reset_advanced_security_enabled_for_new_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSecurityEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetBlog")
    def reset_blog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlog", []))

    @jsii.member(jsii_name="resetCompany")
    def reset_company(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompany", []))

    @jsii.member(jsii_name="resetDefaultRepositoryPermission")
    def reset_default_repository_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRepositoryPermission", []))

    @jsii.member(jsii_name="resetDependabotAlertsEnabledForNewRepositories")
    def reset_dependabot_alerts_enabled_for_new_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependabotAlertsEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetDependabotSecurityUpdatesEnabledForNewRepositories")
    def reset_dependabot_security_updates_enabled_for_new_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependabotSecurityUpdatesEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetDependencyGraphEnabledForNewRepositories")
    def reset_dependency_graph_enabled_for_new_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependencyGraphEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetHasOrganizationProjects")
    def reset_has_organization_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasOrganizationProjects", []))

    @jsii.member(jsii_name="resetHasRepositoryProjects")
    def reset_has_repository_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasRepositoryProjects", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMembersCanCreateInternalRepositories")
    def reset_members_can_create_internal_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreateInternalRepositories", []))

    @jsii.member(jsii_name="resetMembersCanCreatePages")
    def reset_members_can_create_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreatePages", []))

    @jsii.member(jsii_name="resetMembersCanCreatePrivatePages")
    def reset_members_can_create_private_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreatePrivatePages", []))

    @jsii.member(jsii_name="resetMembersCanCreatePrivateRepositories")
    def reset_members_can_create_private_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreatePrivateRepositories", []))

    @jsii.member(jsii_name="resetMembersCanCreatePublicPages")
    def reset_members_can_create_public_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreatePublicPages", []))

    @jsii.member(jsii_name="resetMembersCanCreatePublicRepositories")
    def reset_members_can_create_public_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreatePublicRepositories", []))

    @jsii.member(jsii_name="resetMembersCanCreateRepositories")
    def reset_members_can_create_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreateRepositories", []))

    @jsii.member(jsii_name="resetMembersCanForkPrivateRepositories")
    def reset_members_can_fork_private_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanForkPrivateRepositories", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSecretScanningEnabledForNewRepositories")
    def reset_secret_scanning_enabled_for_new_repositories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanningEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetSecretScanningPushProtectionEnabledForNewRepositories")
    def reset_secret_scanning_push_protection_enabled_for_new_repositories(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanningPushProtectionEnabledForNewRepositories", []))

    @jsii.member(jsii_name="resetTwitterUsername")
    def reset_twitter_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwitterUsername", []))

    @jsii.member(jsii_name="resetWebCommitSignoffRequired")
    def reset_web_commit_signoff_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebCommitSignoffRequired", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityEnabledForNewRepositoriesInput")
    def advanced_security_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "advancedSecurityEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="billingEmailInput")
    def billing_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="blogInput")
    def blog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blogInput"))

    @builtins.property
    @jsii.member(jsii_name="companyInput")
    def company_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "companyInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRepositoryPermissionInput")
    def default_repository_permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRepositoryPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="dependabotAlertsEnabledForNewRepositoriesInput")
    def dependabot_alerts_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dependabotAlertsEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="dependabotSecurityUpdatesEnabledForNewRepositoriesInput")
    def dependabot_security_updates_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dependabotSecurityUpdatesEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="dependencyGraphEnabledForNewRepositoriesInput")
    def dependency_graph_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dependencyGraphEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="hasOrganizationProjectsInput")
    def has_organization_projects_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hasOrganizationProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="hasRepositoryProjectsInput")
    def has_repository_projects_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hasRepositoryProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanCreateInternalRepositoriesInput")
    def members_can_create_internal_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanCreateInternalRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePagesInput")
    def members_can_create_pages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanCreatePagesInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePrivatePagesInput")
    def members_can_create_private_pages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanCreatePrivatePagesInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePrivateRepositoriesInput")
    def members_can_create_private_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanCreatePrivateRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePublicPagesInput")
    def members_can_create_public_pages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanCreatePublicPagesInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePublicRepositoriesInput")
    def members_can_create_public_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanCreatePublicRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanCreateRepositoriesInput")
    def members_can_create_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanCreateRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="membersCanForkPrivateRepositoriesInput")
    def members_can_fork_private_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "membersCanForkPrivateRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningEnabledForNewRepositoriesInput")
    def secret_scanning_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secretScanningEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtectionEnabledForNewRepositoriesInput")
    def secret_scanning_push_protection_enabled_for_new_repositories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secretScanningPushProtectionEnabledForNewRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="twitterUsernameInput")
    def twitter_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "twitterUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="webCommitSignoffRequiredInput")
    def web_commit_signoff_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webCommitSignoffRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityEnabledForNewRepositories")
    def advanced_security_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "advancedSecurityEnabledForNewRepositories"))

    @advanced_security_enabled_for_new_repositories.setter
    def advanced_security_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf49235923f819c1331c2027fd94016b1668d20a69e4555cfd16a2ebe2127c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedSecurityEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingEmail")
    def billing_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingEmail"))

    @billing_email.setter
    def billing_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2221b08e204b6607b34771a910ebd1ad81105069be5ea87f02ed42c5841cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blog")
    def blog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blog"))

    @blog.setter
    def blog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92c49d9e3e9a898308b563eeb8f9f65e5b6b843f4f62c371718dd21d83c0ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="company")
    def company(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "company"))

    @company.setter
    def company(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4910c10ce49d92d109d2a507da03c3ab42e95a05d13b33d0c7f311ed5a7a8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "company", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRepositoryPermission")
    def default_repository_permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRepositoryPermission"))

    @default_repository_permission.setter
    def default_repository_permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28c77b8eb811fdd1499940a09e9694b3f175a30ec3125ccbc2b2a388e7df950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRepositoryPermission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependabotAlertsEnabledForNewRepositories")
    def dependabot_alerts_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dependabotAlertsEnabledForNewRepositories"))

    @dependabot_alerts_enabled_for_new_repositories.setter
    def dependabot_alerts_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3042bfb5886321b227e7a7510212498ee5a711016d21cde89c3615945ff8cd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependabotAlertsEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependabotSecurityUpdatesEnabledForNewRepositories")
    def dependabot_security_updates_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dependabotSecurityUpdatesEnabledForNewRepositories"))

    @dependabot_security_updates_enabled_for_new_repositories.setter
    def dependabot_security_updates_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24155bd6f8a1a3920e9e2add27e69bb10b51cf0e4fdaee9ca3e38430bf73128e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependabotSecurityUpdatesEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependencyGraphEnabledForNewRepositories")
    def dependency_graph_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dependencyGraphEnabledForNewRepositories"))

    @dependency_graph_enabled_for_new_repositories.setter
    def dependency_graph_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb639ef89a6fef8cb73bd444da59238c8a4e6b1f0c1370035bbefb43057a2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencyGraphEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6d636ea2d0f8181c3110d15ba08438959bbcdbc167c5243e17bcc1bb461a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23efe6f3fc5fcd252ffcfea4debe936ef47004e95941f2711c60b32163890cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasOrganizationProjects")
    def has_organization_projects(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hasOrganizationProjects"))

    @has_organization_projects.setter
    def has_organization_projects(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7df0944f4ae41b574efbea17e12a0068e5cfe24e6770765a48256998eda524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasOrganizationProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasRepositoryProjects")
    def has_repository_projects(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hasRepositoryProjects"))

    @has_repository_projects.setter
    def has_repository_projects(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62e67f42cb9d5e19c818486d17faf3d06deb4fba61a79b8b3aa3c866137f0f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasRepositoryProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67efc117582a32c43be306a2e8672732a874f3c2b01d1b0038494f53aa927059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362aa189b2cd8d379e6a244c6e92e5ae5402e7e056c8bbe03e69ded3951206d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanCreateInternalRepositories")
    def members_can_create_internal_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanCreateInternalRepositories"))

    @members_can_create_internal_repositories.setter
    def members_can_create_internal_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae2bf8a3df8e12cb63706082c28089a6e0da48204953d1a5fcc143fdfb6067e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanCreateInternalRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePages")
    def members_can_create_pages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanCreatePages"))

    @members_can_create_pages.setter
    def members_can_create_pages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3ab4ec545ddca13133491fdef73a17e40369df3ddb90b0fd23830524256359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanCreatePages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePrivatePages")
    def members_can_create_private_pages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanCreatePrivatePages"))

    @members_can_create_private_pages.setter
    def members_can_create_private_pages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d79bd1fb86e3d69fbbed76d54fa00a3939395c968399f22001a53cb77609d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanCreatePrivatePages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePrivateRepositories")
    def members_can_create_private_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanCreatePrivateRepositories"))

    @members_can_create_private_repositories.setter
    def members_can_create_private_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b9b3d423d96f0838223b847cd28c6202f2db1fcb68131e4637e6424be9e2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanCreatePrivateRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePublicPages")
    def members_can_create_public_pages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanCreatePublicPages"))

    @members_can_create_public_pages.setter
    def members_can_create_public_pages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f467f7e75d24e0611f73c5c81544a5838eb4212b9aa97231b048830e8837a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanCreatePublicPages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanCreatePublicRepositories")
    def members_can_create_public_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanCreatePublicRepositories"))

    @members_can_create_public_repositories.setter
    def members_can_create_public_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e4907693f77874d3aa6a4e14b8c43734ffa10a338e87b47ba66123897de65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanCreatePublicRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanCreateRepositories")
    def members_can_create_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanCreateRepositories"))

    @members_can_create_repositories.setter
    def members_can_create_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c90e5e94528ef6b777429a9f5e15a6d00e9c820d040b434321e84d86862d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanCreateRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membersCanForkPrivateRepositories")
    def members_can_fork_private_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "membersCanForkPrivateRepositories"))

    @members_can_fork_private_repositories.setter
    def members_can_fork_private_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9b6e987a95ca13137172098cd90f50e1b8ada853044ee3e48ac24f78e4503a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membersCanForkPrivateRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacaad94d03fb082722f0404ba655c95e2ddea77850b97d1c892f03329ac7657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretScanningEnabledForNewRepositories")
    def secret_scanning_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secretScanningEnabledForNewRepositories"))

    @secret_scanning_enabled_for_new_repositories.setter
    def secret_scanning_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398a899d5accb25d1233481515cf670cc1bd66e2212e256e44ebed64851bb379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretScanningEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtectionEnabledForNewRepositories")
    def secret_scanning_push_protection_enabled_for_new_repositories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secretScanningPushProtectionEnabledForNewRepositories"))

    @secret_scanning_push_protection_enabled_for_new_repositories.setter
    def secret_scanning_push_protection_enabled_for_new_repositories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e669d751e07da361ab2169bf4109b091cca9d7ee5aab5f11042b77be7c6f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretScanningPushProtectionEnabledForNewRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="twitterUsername")
    def twitter_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "twitterUsername"))

    @twitter_username.setter
    def twitter_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea7c767cf2e5649a61f4bc46caaee333328b797247c4173564efa7ddb3f5a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twitterUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webCommitSignoffRequired")
    def web_commit_signoff_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webCommitSignoffRequired"))

    @web_commit_signoff_required.setter
    def web_commit_signoff_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d738b217537b5f804fe7a73e30ab0d39710002c025a3d49925cacb130ed5b2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webCommitSignoffRequired", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationSettings.OrganizationSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "billing_email": "billingEmail",
        "advanced_security_enabled_for_new_repositories": "advancedSecurityEnabledForNewRepositories",
        "blog": "blog",
        "company": "company",
        "default_repository_permission": "defaultRepositoryPermission",
        "dependabot_alerts_enabled_for_new_repositories": "dependabotAlertsEnabledForNewRepositories",
        "dependabot_security_updates_enabled_for_new_repositories": "dependabotSecurityUpdatesEnabledForNewRepositories",
        "dependency_graph_enabled_for_new_repositories": "dependencyGraphEnabledForNewRepositories",
        "description": "description",
        "email": "email",
        "has_organization_projects": "hasOrganizationProjects",
        "has_repository_projects": "hasRepositoryProjects",
        "id": "id",
        "location": "location",
        "members_can_create_internal_repositories": "membersCanCreateInternalRepositories",
        "members_can_create_pages": "membersCanCreatePages",
        "members_can_create_private_pages": "membersCanCreatePrivatePages",
        "members_can_create_private_repositories": "membersCanCreatePrivateRepositories",
        "members_can_create_public_pages": "membersCanCreatePublicPages",
        "members_can_create_public_repositories": "membersCanCreatePublicRepositories",
        "members_can_create_repositories": "membersCanCreateRepositories",
        "members_can_fork_private_repositories": "membersCanForkPrivateRepositories",
        "name": "name",
        "secret_scanning_enabled_for_new_repositories": "secretScanningEnabledForNewRepositories",
        "secret_scanning_push_protection_enabled_for_new_repositories": "secretScanningPushProtectionEnabledForNewRepositories",
        "twitter_username": "twitterUsername",
        "web_commit_signoff_required": "webCommitSignoffRequired",
    },
)
class OrganizationSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        billing_email: builtins.str,
        advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        blog: typing.Optional[builtins.str] = None,
        company: typing.Optional[builtins.str] = None,
        default_repository_permission: typing.Optional[builtins.str] = None,
        dependabot_alerts_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependabot_security_updates_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependency_graph_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        has_organization_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_repository_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        members_can_create_internal_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_private_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_public_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_public_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_create_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        members_can_fork_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter_username: typing.Optional[builtins.str] = None,
        web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param billing_email: The billing email address for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#billing_email OrganizationSettings#billing_email}
        :param advanced_security_enabled_for_new_repositories: Whether or not advanced security is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#advanced_security_enabled_for_new_repositories OrganizationSettings#advanced_security_enabled_for_new_repositories}
        :param blog: The blog URL for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#blog OrganizationSettings#blog}
        :param company: The company name for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#company OrganizationSettings#company}
        :param default_repository_permission: The default permission for organization members to create new repositories. Can be one of 'read', 'write', 'admin' or 'none'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#default_repository_permission OrganizationSettings#default_repository_permission}
        :param dependabot_alerts_enabled_for_new_repositories: Whether or not dependabot alerts are enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependabot_alerts_enabled_for_new_repositories OrganizationSettings#dependabot_alerts_enabled_for_new_repositories}
        :param dependabot_security_updates_enabled_for_new_repositories: Whether or not dependabot security updates are enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependabot_security_updates_enabled_for_new_repositories OrganizationSettings#dependabot_security_updates_enabled_for_new_repositories}
        :param dependency_graph_enabled_for_new_repositories: Whether or not dependency graph is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependency_graph_enabled_for_new_repositories OrganizationSettings#dependency_graph_enabled_for_new_repositories}
        :param description: The description for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#description OrganizationSettings#description}
        :param email: The email address for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#email OrganizationSettings#email}
        :param has_organization_projects: Whether or not organization projects are enabled for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#has_organization_projects OrganizationSettings#has_organization_projects}
        :param has_repository_projects: Whether or not repository projects are enabled for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#has_repository_projects OrganizationSettings#has_repository_projects}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#id OrganizationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#location OrganizationSettings#location}
        :param members_can_create_internal_repositories: Whether or not organization members can create new internal repositories. For Enterprise Organizations only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_internal_repositories OrganizationSettings#members_can_create_internal_repositories}
        :param members_can_create_pages: Whether or not organization members can create new pages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_pages OrganizationSettings#members_can_create_pages}
        :param members_can_create_private_pages: Whether or not organization members can create new private pages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_private_pages OrganizationSettings#members_can_create_private_pages}
        :param members_can_create_private_repositories: Whether or not organization members can create new private repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_private_repositories OrganizationSettings#members_can_create_private_repositories}
        :param members_can_create_public_pages: Whether or not organization members can create new public pages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_public_pages OrganizationSettings#members_can_create_public_pages}
        :param members_can_create_public_repositories: Whether or not organization members can create new public repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_public_repositories OrganizationSettings#members_can_create_public_repositories}
        :param members_can_create_repositories: Whether or not organization members can create new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_repositories OrganizationSettings#members_can_create_repositories}
        :param members_can_fork_private_repositories: Whether or not organization members can fork private repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_fork_private_repositories OrganizationSettings#members_can_fork_private_repositories}
        :param name: The name for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#name OrganizationSettings#name}
        :param secret_scanning_enabled_for_new_repositories: Whether or not secret scanning is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#secret_scanning_enabled_for_new_repositories OrganizationSettings#secret_scanning_enabled_for_new_repositories}
        :param secret_scanning_push_protection_enabled_for_new_repositories: Whether or not secret scanning push protection is enabled for new repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#secret_scanning_push_protection_enabled_for_new_repositories OrganizationSettings#secret_scanning_push_protection_enabled_for_new_repositories}
        :param twitter_username: The Twitter username for the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#twitter_username OrganizationSettings#twitter_username}
        :param web_commit_signoff_required: Whether or not commit signatures are required for commits to the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#web_commit_signoff_required OrganizationSettings#web_commit_signoff_required}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ced25d4543779eff538067206d9abc7dab01753f71d6054c5d41ce89661d2c1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument billing_email", value=billing_email, expected_type=type_hints["billing_email"])
            check_type(argname="argument advanced_security_enabled_for_new_repositories", value=advanced_security_enabled_for_new_repositories, expected_type=type_hints["advanced_security_enabled_for_new_repositories"])
            check_type(argname="argument blog", value=blog, expected_type=type_hints["blog"])
            check_type(argname="argument company", value=company, expected_type=type_hints["company"])
            check_type(argname="argument default_repository_permission", value=default_repository_permission, expected_type=type_hints["default_repository_permission"])
            check_type(argname="argument dependabot_alerts_enabled_for_new_repositories", value=dependabot_alerts_enabled_for_new_repositories, expected_type=type_hints["dependabot_alerts_enabled_for_new_repositories"])
            check_type(argname="argument dependabot_security_updates_enabled_for_new_repositories", value=dependabot_security_updates_enabled_for_new_repositories, expected_type=type_hints["dependabot_security_updates_enabled_for_new_repositories"])
            check_type(argname="argument dependency_graph_enabled_for_new_repositories", value=dependency_graph_enabled_for_new_repositories, expected_type=type_hints["dependency_graph_enabled_for_new_repositories"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument has_organization_projects", value=has_organization_projects, expected_type=type_hints["has_organization_projects"])
            check_type(argname="argument has_repository_projects", value=has_repository_projects, expected_type=type_hints["has_repository_projects"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument members_can_create_internal_repositories", value=members_can_create_internal_repositories, expected_type=type_hints["members_can_create_internal_repositories"])
            check_type(argname="argument members_can_create_pages", value=members_can_create_pages, expected_type=type_hints["members_can_create_pages"])
            check_type(argname="argument members_can_create_private_pages", value=members_can_create_private_pages, expected_type=type_hints["members_can_create_private_pages"])
            check_type(argname="argument members_can_create_private_repositories", value=members_can_create_private_repositories, expected_type=type_hints["members_can_create_private_repositories"])
            check_type(argname="argument members_can_create_public_pages", value=members_can_create_public_pages, expected_type=type_hints["members_can_create_public_pages"])
            check_type(argname="argument members_can_create_public_repositories", value=members_can_create_public_repositories, expected_type=type_hints["members_can_create_public_repositories"])
            check_type(argname="argument members_can_create_repositories", value=members_can_create_repositories, expected_type=type_hints["members_can_create_repositories"])
            check_type(argname="argument members_can_fork_private_repositories", value=members_can_fork_private_repositories, expected_type=type_hints["members_can_fork_private_repositories"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secret_scanning_enabled_for_new_repositories", value=secret_scanning_enabled_for_new_repositories, expected_type=type_hints["secret_scanning_enabled_for_new_repositories"])
            check_type(argname="argument secret_scanning_push_protection_enabled_for_new_repositories", value=secret_scanning_push_protection_enabled_for_new_repositories, expected_type=type_hints["secret_scanning_push_protection_enabled_for_new_repositories"])
            check_type(argname="argument twitter_username", value=twitter_username, expected_type=type_hints["twitter_username"])
            check_type(argname="argument web_commit_signoff_required", value=web_commit_signoff_required, expected_type=type_hints["web_commit_signoff_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "billing_email": billing_email,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if advanced_security_enabled_for_new_repositories is not None:
            self._values["advanced_security_enabled_for_new_repositories"] = advanced_security_enabled_for_new_repositories
        if blog is not None:
            self._values["blog"] = blog
        if company is not None:
            self._values["company"] = company
        if default_repository_permission is not None:
            self._values["default_repository_permission"] = default_repository_permission
        if dependabot_alerts_enabled_for_new_repositories is not None:
            self._values["dependabot_alerts_enabled_for_new_repositories"] = dependabot_alerts_enabled_for_new_repositories
        if dependabot_security_updates_enabled_for_new_repositories is not None:
            self._values["dependabot_security_updates_enabled_for_new_repositories"] = dependabot_security_updates_enabled_for_new_repositories
        if dependency_graph_enabled_for_new_repositories is not None:
            self._values["dependency_graph_enabled_for_new_repositories"] = dependency_graph_enabled_for_new_repositories
        if description is not None:
            self._values["description"] = description
        if email is not None:
            self._values["email"] = email
        if has_organization_projects is not None:
            self._values["has_organization_projects"] = has_organization_projects
        if has_repository_projects is not None:
            self._values["has_repository_projects"] = has_repository_projects
        if id is not None:
            self._values["id"] = id
        if location is not None:
            self._values["location"] = location
        if members_can_create_internal_repositories is not None:
            self._values["members_can_create_internal_repositories"] = members_can_create_internal_repositories
        if members_can_create_pages is not None:
            self._values["members_can_create_pages"] = members_can_create_pages
        if members_can_create_private_pages is not None:
            self._values["members_can_create_private_pages"] = members_can_create_private_pages
        if members_can_create_private_repositories is not None:
            self._values["members_can_create_private_repositories"] = members_can_create_private_repositories
        if members_can_create_public_pages is not None:
            self._values["members_can_create_public_pages"] = members_can_create_public_pages
        if members_can_create_public_repositories is not None:
            self._values["members_can_create_public_repositories"] = members_can_create_public_repositories
        if members_can_create_repositories is not None:
            self._values["members_can_create_repositories"] = members_can_create_repositories
        if members_can_fork_private_repositories is not None:
            self._values["members_can_fork_private_repositories"] = members_can_fork_private_repositories
        if name is not None:
            self._values["name"] = name
        if secret_scanning_enabled_for_new_repositories is not None:
            self._values["secret_scanning_enabled_for_new_repositories"] = secret_scanning_enabled_for_new_repositories
        if secret_scanning_push_protection_enabled_for_new_repositories is not None:
            self._values["secret_scanning_push_protection_enabled_for_new_repositories"] = secret_scanning_push_protection_enabled_for_new_repositories
        if twitter_username is not None:
            self._values["twitter_username"] = twitter_username
        if web_commit_signoff_required is not None:
            self._values["web_commit_signoff_required"] = web_commit_signoff_required

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def billing_email(self) -> builtins.str:
        '''The billing email address for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#billing_email OrganizationSettings#billing_email}
        '''
        result = self._values.get("billing_email")
        assert result is not None, "Required property 'billing_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_security_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not advanced security is enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#advanced_security_enabled_for_new_repositories OrganizationSettings#advanced_security_enabled_for_new_repositories}
        '''
        result = self._values.get("advanced_security_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def blog(self) -> typing.Optional[builtins.str]:
        '''The blog URL for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#blog OrganizationSettings#blog}
        '''
        result = self._values.get("blog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def company(self) -> typing.Optional[builtins.str]:
        '''The company name for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#company OrganizationSettings#company}
        '''
        result = self._values.get("company")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_repository_permission(self) -> typing.Optional[builtins.str]:
        '''The default permission for organization members to create new repositories. Can be one of 'read', 'write', 'admin' or 'none'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#default_repository_permission OrganizationSettings#default_repository_permission}
        '''
        result = self._values.get("default_repository_permission")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependabot_alerts_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not dependabot alerts are enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependabot_alerts_enabled_for_new_repositories OrganizationSettings#dependabot_alerts_enabled_for_new_repositories}
        '''
        result = self._values.get("dependabot_alerts_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dependabot_security_updates_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not dependabot security updates are enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependabot_security_updates_enabled_for_new_repositories OrganizationSettings#dependabot_security_updates_enabled_for_new_repositories}
        '''
        result = self._values.get("dependabot_security_updates_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dependency_graph_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not dependency graph is enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#dependency_graph_enabled_for_new_repositories OrganizationSettings#dependency_graph_enabled_for_new_repositories}
        '''
        result = self._values.get("dependency_graph_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#description OrganizationSettings#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The email address for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#email OrganizationSettings#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def has_organization_projects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization projects are enabled for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#has_organization_projects OrganizationSettings#has_organization_projects}
        '''
        result = self._values.get("has_organization_projects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def has_repository_projects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not repository projects are enabled for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#has_repository_projects OrganizationSettings#has_repository_projects}
        '''
        result = self._values.get("has_repository_projects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#id OrganizationSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#location OrganizationSettings#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def members_can_create_internal_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can create new internal repositories. For Enterprise Organizations only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_internal_repositories OrganizationSettings#members_can_create_internal_repositories}
        '''
        result = self._values.get("members_can_create_internal_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def members_can_create_pages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can create new pages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_pages OrganizationSettings#members_can_create_pages}
        '''
        result = self._values.get("members_can_create_pages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def members_can_create_private_pages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can create new private pages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_private_pages OrganizationSettings#members_can_create_private_pages}
        '''
        result = self._values.get("members_can_create_private_pages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def members_can_create_private_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can create new private repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_private_repositories OrganizationSettings#members_can_create_private_repositories}
        '''
        result = self._values.get("members_can_create_private_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def members_can_create_public_pages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can create new public pages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_public_pages OrganizationSettings#members_can_create_public_pages}
        '''
        result = self._values.get("members_can_create_public_pages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def members_can_create_public_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can create new public repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_public_repositories OrganizationSettings#members_can_create_public_repositories}
        '''
        result = self._values.get("members_can_create_public_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def members_can_create_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can create new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_create_repositories OrganizationSettings#members_can_create_repositories}
        '''
        result = self._values.get("members_can_create_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def members_can_fork_private_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not organization members can fork private repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#members_can_fork_private_repositories OrganizationSettings#members_can_fork_private_repositories}
        '''
        result = self._values.get("members_can_fork_private_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#name OrganizationSettings#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_scanning_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not secret scanning is enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#secret_scanning_enabled_for_new_repositories OrganizationSettings#secret_scanning_enabled_for_new_repositories}
        '''
        result = self._values.get("secret_scanning_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_scanning_push_protection_enabled_for_new_repositories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not secret scanning push protection is enabled for new repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#secret_scanning_push_protection_enabled_for_new_repositories OrganizationSettings#secret_scanning_push_protection_enabled_for_new_repositories}
        '''
        result = self._values.get("secret_scanning_push_protection_enabled_for_new_repositories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def twitter_username(self) -> typing.Optional[builtins.str]:
        '''The Twitter username for the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#twitter_username OrganizationSettings#twitter_username}
        '''
        result = self._values.get("twitter_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_commit_signoff_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not commit signatures are required for commits to the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_settings#web_commit_signoff_required OrganizationSettings#web_commit_signoff_required}
        '''
        result = self._values.get("web_commit_signoff_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OrganizationSettings",
    "OrganizationSettingsConfig",
]

publication.publish()

def _typecheckingstub__ff26516a1a18b7ae1005dd371a79b7f18a58f1ed21b7f09cacc79d89bb790079(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    billing_email: builtins.str,
    advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    blog: typing.Optional[builtins.str] = None,
    company: typing.Optional[builtins.str] = None,
    default_repository_permission: typing.Optional[builtins.str] = None,
    dependabot_alerts_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependabot_security_updates_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependency_graph_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    has_organization_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_repository_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    members_can_create_internal_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_private_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_public_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_public_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_fork_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    twitter_username: typing.Optional[builtins.str] = None,
    web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debfca161615eb49a2b3f3c91f61bba3caa08876a249f0b040f55dc3490d50f6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf49235923f819c1331c2027fd94016b1668d20a69e4555cfd16a2ebe2127c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2221b08e204b6607b34771a910ebd1ad81105069be5ea87f02ed42c5841cb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92c49d9e3e9a898308b563eeb8f9f65e5b6b843f4f62c371718dd21d83c0ec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4910c10ce49d92d109d2a507da03c3ab42e95a05d13b33d0c7f311ed5a7a8bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28c77b8eb811fdd1499940a09e9694b3f175a30ec3125ccbc2b2a388e7df950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3042bfb5886321b227e7a7510212498ee5a711016d21cde89c3615945ff8cd25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24155bd6f8a1a3920e9e2add27e69bb10b51cf0e4fdaee9ca3e38430bf73128e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb639ef89a6fef8cb73bd444da59238c8a4e6b1f0c1370035bbefb43057a2a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6d636ea2d0f8181c3110d15ba08438959bbcdbc167c5243e17bcc1bb461a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23efe6f3fc5fcd252ffcfea4debe936ef47004e95941f2711c60b32163890cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7df0944f4ae41b574efbea17e12a0068e5cfe24e6770765a48256998eda524(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62e67f42cb9d5e19c818486d17faf3d06deb4fba61a79b8b3aa3c866137f0f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67efc117582a32c43be306a2e8672732a874f3c2b01d1b0038494f53aa927059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362aa189b2cd8d379e6a244c6e92e5ae5402e7e056c8bbe03e69ded3951206d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae2bf8a3df8e12cb63706082c28089a6e0da48204953d1a5fcc143fdfb6067e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3ab4ec545ddca13133491fdef73a17e40369df3ddb90b0fd23830524256359(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d79bd1fb86e3d69fbbed76d54fa00a3939395c968399f22001a53cb77609d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b9b3d423d96f0838223b847cd28c6202f2db1fcb68131e4637e6424be9e2ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f467f7e75d24e0611f73c5c81544a5838eb4212b9aa97231b048830e8837a3a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e4907693f77874d3aa6a4e14b8c43734ffa10a338e87b47ba66123897de65f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c90e5e94528ef6b777429a9f5e15a6d00e9c820d040b434321e84d86862d79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9b6e987a95ca13137172098cd90f50e1b8ada853044ee3e48ac24f78e4503a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacaad94d03fb082722f0404ba655c95e2ddea77850b97d1c892f03329ac7657(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398a899d5accb25d1233481515cf670cc1bd66e2212e256e44ebed64851bb379(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e669d751e07da361ab2169bf4109b091cca9d7ee5aab5f11042b77be7c6f09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea7c767cf2e5649a61f4bc46caaee333328b797247c4173564efa7ddb3f5a20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d738b217537b5f804fe7a73e30ab0d39710002c025a3d49925cacb130ed5b2eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ced25d4543779eff538067206d9abc7dab01753f71d6054c5d41ce89661d2c1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    billing_email: builtins.str,
    advanced_security_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    blog: typing.Optional[builtins.str] = None,
    company: typing.Optional[builtins.str] = None,
    default_repository_permission: typing.Optional[builtins.str] = None,
    dependabot_alerts_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependabot_security_updates_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependency_graph_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    has_organization_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_repository_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    members_can_create_internal_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_private_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_public_pages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_public_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_create_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    members_can_fork_private_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    secret_scanning_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_scanning_push_protection_enabled_for_new_repositories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    twitter_username: typing.Optional[builtins.str] = None,
    web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
