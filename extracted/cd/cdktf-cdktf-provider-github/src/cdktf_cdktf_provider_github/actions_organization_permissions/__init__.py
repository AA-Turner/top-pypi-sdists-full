r'''
# `github_actions_organization_permissions`

Refer to the Terraform Registry for docs: [`github_actions_organization_permissions`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions).
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


class ActionsOrganizationPermissions(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsOrganizationPermissions.ActionsOrganizationPermissions",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions github_actions_organization_permissions}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled_repositories: builtins.str,
        allowed_actions: typing.Optional[builtins.str] = None,
        allowed_actions_config: typing.Optional[typing.Union["ActionsOrganizationPermissionsAllowedActionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled_repositories_config: typing.Optional[typing.Union["ActionsOrganizationPermissionsEnabledRepositoriesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions github_actions_organization_permissions} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled_repositories: The policy that controls the repositories in the organization that are allowed to run GitHub Actions. Can be one of: 'all', 'none', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#enabled_repositories ActionsOrganizationPermissions#enabled_repositories}
        :param allowed_actions: The permissions policy that controls the actions that are allowed to run. Can be one of: 'all', 'local_only', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#allowed_actions ActionsOrganizationPermissions#allowed_actions}
        :param allowed_actions_config: allowed_actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#allowed_actions_config ActionsOrganizationPermissions#allowed_actions_config}
        :param enabled_repositories_config: enabled_repositories_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#enabled_repositories_config ActionsOrganizationPermissions#enabled_repositories_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#id ActionsOrganizationPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae5ece4e4318edf68cb7df861acff7c031c972c337be9294873930aa8dea42d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ActionsOrganizationPermissionsConfig(
            enabled_repositories=enabled_repositories,
            allowed_actions=allowed_actions,
            allowed_actions_config=allowed_actions_config,
            enabled_repositories_config=enabled_repositories_config,
            id=id,
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
        '''Generates CDKTF code for importing a ActionsOrganizationPermissions resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ActionsOrganizationPermissions to import.
        :param import_from_id: The id of the existing ActionsOrganizationPermissions that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ActionsOrganizationPermissions to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4c81928107dd6bd9d98f51989a43a4a0e494233204ba707d8341609bb8d10e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllowedActionsConfig")
    def put_allowed_actions_config(
        self,
        *,
        github_owned_allowed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        patterns_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        verified_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param github_owned_allowed: Whether GitHub-owned actions are allowed in the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#github_owned_allowed ActionsOrganizationPermissions#github_owned_allowed}
        :param patterns_allowed: Specifies a list of string-matching patterns to allow specific action(s). Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#patterns_allowed ActionsOrganizationPermissions#patterns_allowed}
        :param verified_allowed: Whether actions in GitHub Marketplace from verified creators are allowed. Set to 'true' to allow all GitHub Marketplace actions by verified creators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#verified_allowed ActionsOrganizationPermissions#verified_allowed}
        '''
        value = ActionsOrganizationPermissionsAllowedActionsConfig(
            github_owned_allowed=github_owned_allowed,
            patterns_allowed=patterns_allowed,
            verified_allowed=verified_allowed,
        )

        return typing.cast(None, jsii.invoke(self, "putAllowedActionsConfig", [value]))

    @jsii.member(jsii_name="putEnabledRepositoriesConfig")
    def put_enabled_repositories_config(
        self,
        *,
        repository_ids: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param repository_ids: List of repository IDs to enable for GitHub Actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#repository_ids ActionsOrganizationPermissions#repository_ids}
        '''
        value = ActionsOrganizationPermissionsEnabledRepositoriesConfig(
            repository_ids=repository_ids
        )

        return typing.cast(None, jsii.invoke(self, "putEnabledRepositoriesConfig", [value]))

    @jsii.member(jsii_name="resetAllowedActions")
    def reset_allowed_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedActions", []))

    @jsii.member(jsii_name="resetAllowedActionsConfig")
    def reset_allowed_actions_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedActionsConfig", []))

    @jsii.member(jsii_name="resetEnabledRepositoriesConfig")
    def reset_enabled_repositories_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledRepositoriesConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="allowedActionsConfig")
    def allowed_actions_config(
        self,
    ) -> "ActionsOrganizationPermissionsAllowedActionsConfigOutputReference":
        return typing.cast("ActionsOrganizationPermissionsAllowedActionsConfigOutputReference", jsii.get(self, "allowedActionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="enabledRepositoriesConfig")
    def enabled_repositories_config(
        self,
    ) -> "ActionsOrganizationPermissionsEnabledRepositoriesConfigOutputReference":
        return typing.cast("ActionsOrganizationPermissionsEnabledRepositoriesConfigOutputReference", jsii.get(self, "enabledRepositoriesConfig"))

    @builtins.property
    @jsii.member(jsii_name="allowedActionsConfigInput")
    def allowed_actions_config_input(
        self,
    ) -> typing.Optional["ActionsOrganizationPermissionsAllowedActionsConfig"]:
        return typing.cast(typing.Optional["ActionsOrganizationPermissionsAllowedActionsConfig"], jsii.get(self, "allowedActionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedActionsInput")
    def allowed_actions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledRepositoriesConfigInput")
    def enabled_repositories_config_input(
        self,
    ) -> typing.Optional["ActionsOrganizationPermissionsEnabledRepositoriesConfig"]:
        return typing.cast(typing.Optional["ActionsOrganizationPermissionsEnabledRepositoriesConfig"], jsii.get(self, "enabledRepositoriesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledRepositoriesInput")
    def enabled_repositories_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enabledRepositoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedActions")
    def allowed_actions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedActions"))

    @allowed_actions.setter
    def allowed_actions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68bb4d75483503fd76755d329c1b729b71c8ce82358bc3acb7bd98d151fa6163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabledRepositories")
    def enabled_repositories(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enabledRepositories"))

    @enabled_repositories.setter
    def enabled_repositories(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191f0a80f7079bdcf15e0680b608b0aa91267ffcee5d159db27f46f9d94c7505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledRepositories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8dba49260b07c2aca92c2f2293d5d30b9d61540333439d0209d9e8688d30593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsOrganizationPermissions.ActionsOrganizationPermissionsAllowedActionsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "github_owned_allowed": "githubOwnedAllowed",
        "patterns_allowed": "patternsAllowed",
        "verified_allowed": "verifiedAllowed",
    },
)
class ActionsOrganizationPermissionsAllowedActionsConfig:
    def __init__(
        self,
        *,
        github_owned_allowed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        patterns_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        verified_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param github_owned_allowed: Whether GitHub-owned actions are allowed in the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#github_owned_allowed ActionsOrganizationPermissions#github_owned_allowed}
        :param patterns_allowed: Specifies a list of string-matching patterns to allow specific action(s). Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#patterns_allowed ActionsOrganizationPermissions#patterns_allowed}
        :param verified_allowed: Whether actions in GitHub Marketplace from verified creators are allowed. Set to 'true' to allow all GitHub Marketplace actions by verified creators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#verified_allowed ActionsOrganizationPermissions#verified_allowed}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ee60654dfd9a79d8184c7480a615e3efae7591951166d69f2fc490418d8a60)
            check_type(argname="argument github_owned_allowed", value=github_owned_allowed, expected_type=type_hints["github_owned_allowed"])
            check_type(argname="argument patterns_allowed", value=patterns_allowed, expected_type=type_hints["patterns_allowed"])
            check_type(argname="argument verified_allowed", value=verified_allowed, expected_type=type_hints["verified_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "github_owned_allowed": github_owned_allowed,
        }
        if patterns_allowed is not None:
            self._values["patterns_allowed"] = patterns_allowed
        if verified_allowed is not None:
            self._values["verified_allowed"] = verified_allowed

    @builtins.property
    def github_owned_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether GitHub-owned actions are allowed in the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#github_owned_allowed ActionsOrganizationPermissions#github_owned_allowed}
        '''
        result = self._values.get("github_owned_allowed")
        assert result is not None, "Required property 'github_owned_allowed' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def patterns_allowed(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of string-matching patterns to allow specific action(s).

        Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#patterns_allowed ActionsOrganizationPermissions#patterns_allowed}
        '''
        result = self._values.get("patterns_allowed")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verified_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether actions in GitHub Marketplace from verified creators are allowed.

        Set to 'true' to allow all GitHub Marketplace actions by verified creators.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#verified_allowed ActionsOrganizationPermissions#verified_allowed}
        '''
        result = self._values.get("verified_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsOrganizationPermissionsAllowedActionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsOrganizationPermissionsAllowedActionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsOrganizationPermissions.ActionsOrganizationPermissionsAllowedActionsConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5418dffafc1dda98ecfc7ec9242ecd7514aa2836c3115e98895a9ff121ae42f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPatternsAllowed")
    def reset_patterns_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatternsAllowed", []))

    @jsii.member(jsii_name="resetVerifiedAllowed")
    def reset_verified_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifiedAllowed", []))

    @builtins.property
    @jsii.member(jsii_name="githubOwnedAllowedInput")
    def github_owned_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "githubOwnedAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="patternsAllowedInput")
    def patterns_allowed_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "patternsAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="verifiedAllowedInput")
    def verified_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifiedAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="githubOwnedAllowed")
    def github_owned_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "githubOwnedAllowed"))

    @github_owned_allowed.setter
    def github_owned_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa8d762ba468f0e4b9726c822b6c1ef2a29e9a6c4d49974e24846aa1d8e335e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubOwnedAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternsAllowed")
    def patterns_allowed(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "patternsAllowed"))

    @patterns_allowed.setter
    def patterns_allowed(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc90c4e22e1873d8d797ef7640e1da2c82dab561521230715e85a9712b9c418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternsAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verifiedAllowed")
    def verified_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifiedAllowed"))

    @verified_allowed.setter
    def verified_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81031723d8f4fcfc00c4ea4b727fb0dec6f222f77d2f81c92cf17ee256105080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifiedAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ActionsOrganizationPermissionsAllowedActionsConfig]:
        return typing.cast(typing.Optional[ActionsOrganizationPermissionsAllowedActionsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActionsOrganizationPermissionsAllowedActionsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7708da6c996e14a442c175752ef3b0555037c722c39fdf6d431f32fbaf2b003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsOrganizationPermissions.ActionsOrganizationPermissionsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled_repositories": "enabledRepositories",
        "allowed_actions": "allowedActions",
        "allowed_actions_config": "allowedActionsConfig",
        "enabled_repositories_config": "enabledRepositoriesConfig",
        "id": "id",
    },
)
class ActionsOrganizationPermissionsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enabled_repositories: builtins.str,
        allowed_actions: typing.Optional[builtins.str] = None,
        allowed_actions_config: typing.Optional[typing.Union[ActionsOrganizationPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        enabled_repositories_config: typing.Optional[typing.Union["ActionsOrganizationPermissionsEnabledRepositoriesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled_repositories: The policy that controls the repositories in the organization that are allowed to run GitHub Actions. Can be one of: 'all', 'none', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#enabled_repositories ActionsOrganizationPermissions#enabled_repositories}
        :param allowed_actions: The permissions policy that controls the actions that are allowed to run. Can be one of: 'all', 'local_only', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#allowed_actions ActionsOrganizationPermissions#allowed_actions}
        :param allowed_actions_config: allowed_actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#allowed_actions_config ActionsOrganizationPermissions#allowed_actions_config}
        :param enabled_repositories_config: enabled_repositories_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#enabled_repositories_config ActionsOrganizationPermissions#enabled_repositories_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#id ActionsOrganizationPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(allowed_actions_config, dict):
            allowed_actions_config = ActionsOrganizationPermissionsAllowedActionsConfig(**allowed_actions_config)
        if isinstance(enabled_repositories_config, dict):
            enabled_repositories_config = ActionsOrganizationPermissionsEnabledRepositoriesConfig(**enabled_repositories_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e45c4445830200511c1ef87e30bb8a2370f039a5a2dc7c6c81e6de29cec089)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled_repositories", value=enabled_repositories, expected_type=type_hints["enabled_repositories"])
            check_type(argname="argument allowed_actions", value=allowed_actions, expected_type=type_hints["allowed_actions"])
            check_type(argname="argument allowed_actions_config", value=allowed_actions_config, expected_type=type_hints["allowed_actions_config"])
            check_type(argname="argument enabled_repositories_config", value=enabled_repositories_config, expected_type=type_hints["enabled_repositories_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled_repositories": enabled_repositories,
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
        if allowed_actions is not None:
            self._values["allowed_actions"] = allowed_actions
        if allowed_actions_config is not None:
            self._values["allowed_actions_config"] = allowed_actions_config
        if enabled_repositories_config is not None:
            self._values["enabled_repositories_config"] = enabled_repositories_config
        if id is not None:
            self._values["id"] = id

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
    def enabled_repositories(self) -> builtins.str:
        '''The policy that controls the repositories in the organization that are allowed to run GitHub Actions.

        Can be one of: 'all', 'none', or 'selected'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#enabled_repositories ActionsOrganizationPermissions#enabled_repositories}
        '''
        result = self._values.get("enabled_repositories")
        assert result is not None, "Required property 'enabled_repositories' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_actions(self) -> typing.Optional[builtins.str]:
        '''The permissions policy that controls the actions that are allowed to run.

        Can be one of: 'all', 'local_only', or 'selected'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#allowed_actions ActionsOrganizationPermissions#allowed_actions}
        '''
        result = self._values.get("allowed_actions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_actions_config(
        self,
    ) -> typing.Optional[ActionsOrganizationPermissionsAllowedActionsConfig]:
        '''allowed_actions_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#allowed_actions_config ActionsOrganizationPermissions#allowed_actions_config}
        '''
        result = self._values.get("allowed_actions_config")
        return typing.cast(typing.Optional[ActionsOrganizationPermissionsAllowedActionsConfig], result)

    @builtins.property
    def enabled_repositories_config(
        self,
    ) -> typing.Optional["ActionsOrganizationPermissionsEnabledRepositoriesConfig"]:
        '''enabled_repositories_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#enabled_repositories_config ActionsOrganizationPermissions#enabled_repositories_config}
        '''
        result = self._values.get("enabled_repositories_config")
        return typing.cast(typing.Optional["ActionsOrganizationPermissionsEnabledRepositoriesConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#id ActionsOrganizationPermissions#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsOrganizationPermissionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsOrganizationPermissions.ActionsOrganizationPermissionsEnabledRepositoriesConfig",
    jsii_struct_bases=[],
    name_mapping={"repository_ids": "repositoryIds"},
)
class ActionsOrganizationPermissionsEnabledRepositoriesConfig:
    def __init__(self, *, repository_ids: typing.Sequence[jsii.Number]) -> None:
        '''
        :param repository_ids: List of repository IDs to enable for GitHub Actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#repository_ids ActionsOrganizationPermissions#repository_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fc3f3a96263ac8b85a19a296536dd2335030b3ee11a5a34d8dbd059fd7213f)
            check_type(argname="argument repository_ids", value=repository_ids, expected_type=type_hints["repository_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_ids": repository_ids,
        }

    @builtins.property
    def repository_ids(self) -> typing.List[jsii.Number]:
        '''List of repository IDs to enable for GitHub Actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_organization_permissions#repository_ids ActionsOrganizationPermissions#repository_ids}
        '''
        result = self._values.get("repository_ids")
        assert result is not None, "Required property 'repository_ids' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsOrganizationPermissionsEnabledRepositoriesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsOrganizationPermissionsEnabledRepositoriesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsOrganizationPermissions.ActionsOrganizationPermissionsEnabledRepositoriesConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff274bb8d189147445d681bc7da8b6ad457cc84e4b5c7d2ef7d51157a48ead86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryIdsInput")
    def repository_ids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "repositoryIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIds")
    def repository_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "repositoryIds"))

    @repository_ids.setter
    def repository_ids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e1efebb1295c3a9148ef65dc9745532e9aec0eb03dfdf0c777cbf9a531513f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ActionsOrganizationPermissionsEnabledRepositoriesConfig]:
        return typing.cast(typing.Optional[ActionsOrganizationPermissionsEnabledRepositoriesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActionsOrganizationPermissionsEnabledRepositoriesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a0ad106243a0ab3921fa5254f98ba45c972e4daaddcd6c51e573bdbf94e305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ActionsOrganizationPermissions",
    "ActionsOrganizationPermissionsAllowedActionsConfig",
    "ActionsOrganizationPermissionsAllowedActionsConfigOutputReference",
    "ActionsOrganizationPermissionsConfig",
    "ActionsOrganizationPermissionsEnabledRepositoriesConfig",
    "ActionsOrganizationPermissionsEnabledRepositoriesConfigOutputReference",
]

publication.publish()

def _typecheckingstub__4ae5ece4e4318edf68cb7df861acff7c031c972c337be9294873930aa8dea42d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled_repositories: builtins.str,
    allowed_actions: typing.Optional[builtins.str] = None,
    allowed_actions_config: typing.Optional[typing.Union[ActionsOrganizationPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled_repositories_config: typing.Optional[typing.Union[ActionsOrganizationPermissionsEnabledRepositoriesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4d4c81928107dd6bd9d98f51989a43a4a0e494233204ba707d8341609bb8d10e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68bb4d75483503fd76755d329c1b729b71c8ce82358bc3acb7bd98d151fa6163(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191f0a80f7079bdcf15e0680b608b0aa91267ffcee5d159db27f46f9d94c7505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8dba49260b07c2aca92c2f2293d5d30b9d61540333439d0209d9e8688d30593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ee60654dfd9a79d8184c7480a615e3efae7591951166d69f2fc490418d8a60(
    *,
    github_owned_allowed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    patterns_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
    verified_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5418dffafc1dda98ecfc7ec9242ecd7514aa2836c3115e98895a9ff121ae42f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa8d762ba468f0e4b9726c822b6c1ef2a29e9a6c4d49974e24846aa1d8e335e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc90c4e22e1873d8d797ef7640e1da2c82dab561521230715e85a9712b9c418(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81031723d8f4fcfc00c4ea4b727fb0dec6f222f77d2f81c92cf17ee256105080(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7708da6c996e14a442c175752ef3b0555037c722c39fdf6d431f32fbaf2b003(
    value: typing.Optional[ActionsOrganizationPermissionsAllowedActionsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e45c4445830200511c1ef87e30bb8a2370f039a5a2dc7c6c81e6de29cec089(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled_repositories: builtins.str,
    allowed_actions: typing.Optional[builtins.str] = None,
    allowed_actions_config: typing.Optional[typing.Union[ActionsOrganizationPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled_repositories_config: typing.Optional[typing.Union[ActionsOrganizationPermissionsEnabledRepositoriesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fc3f3a96263ac8b85a19a296536dd2335030b3ee11a5a34d8dbd059fd7213f(
    *,
    repository_ids: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff274bb8d189147445d681bc7da8b6ad457cc84e4b5c7d2ef7d51157a48ead86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e1efebb1295c3a9148ef65dc9745532e9aec0eb03dfdf0c777cbf9a531513f(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a0ad106243a0ab3921fa5254f98ba45c972e4daaddcd6c51e573bdbf94e305(
    value: typing.Optional[ActionsOrganizationPermissionsEnabledRepositoriesConfig],
) -> None:
    """Type checking stubs"""
    pass
