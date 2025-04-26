r'''
# `github_enterprise_actions_permissions`

Refer to the Terraform Registry for docs: [`github_enterprise_actions_permissions`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions).
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


class EnterpriseActionsPermissions(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.enterpriseActionsPermissions.EnterpriseActionsPermissions",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions github_enterprise_actions_permissions}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled_organizations: builtins.str,
        enterprise_slug: builtins.str,
        allowed_actions: typing.Optional[builtins.str] = None,
        allowed_actions_config: typing.Optional[typing.Union["EnterpriseActionsPermissionsAllowedActionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled_organizations_config: typing.Optional[typing.Union["EnterpriseActionsPermissionsEnabledOrganizationsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions github_enterprise_actions_permissions} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled_organizations: The policy that controls the organizations in the enterprise that are allowed to run GitHub Actions. Can be one of: 'all', 'none', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enabled_organizations EnterpriseActionsPermissions#enabled_organizations}
        :param enterprise_slug: The slug of the enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enterprise_slug EnterpriseActionsPermissions#enterprise_slug}
        :param allowed_actions: The permissions policy that controls the actions that are allowed to run. Can be one of: 'all', 'local_only', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#allowed_actions EnterpriseActionsPermissions#allowed_actions}
        :param allowed_actions_config: allowed_actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#allowed_actions_config EnterpriseActionsPermissions#allowed_actions_config}
        :param enabled_organizations_config: enabled_organizations_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enabled_organizations_config EnterpriseActionsPermissions#enabled_organizations_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#id EnterpriseActionsPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d513abaf652d4ca2ba7531d0ffecf6aedfa65db0ba77fa427a7a678f2647936c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EnterpriseActionsPermissionsConfig(
            enabled_organizations=enabled_organizations,
            enterprise_slug=enterprise_slug,
            allowed_actions=allowed_actions,
            allowed_actions_config=allowed_actions_config,
            enabled_organizations_config=enabled_organizations_config,
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
        '''Generates CDKTF code for importing a EnterpriseActionsPermissions resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EnterpriseActionsPermissions to import.
        :param import_from_id: The id of the existing EnterpriseActionsPermissions that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EnterpriseActionsPermissions to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638d1ce434d9b22f848273a6484f32d79aed50bb5855ac504d20288b236346d5)
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
        :param github_owned_allowed: Whether GitHub-owned actions are allowed in the enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#github_owned_allowed EnterpriseActionsPermissions#github_owned_allowed}
        :param patterns_allowed: Specifies a list of string-matching patterns to allow specific action(s). Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#patterns_allowed EnterpriseActionsPermissions#patterns_allowed}
        :param verified_allowed: Whether actions in GitHub Marketplace from verified creators are allowed. Set to 'true' to allow all GitHub Marketplace actions by verified creators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#verified_allowed EnterpriseActionsPermissions#verified_allowed}
        '''
        value = EnterpriseActionsPermissionsAllowedActionsConfig(
            github_owned_allowed=github_owned_allowed,
            patterns_allowed=patterns_allowed,
            verified_allowed=verified_allowed,
        )

        return typing.cast(None, jsii.invoke(self, "putAllowedActionsConfig", [value]))

    @jsii.member(jsii_name="putEnabledOrganizationsConfig")
    def put_enabled_organizations_config(
        self,
        *,
        organization_ids: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param organization_ids: List of organization IDs to enable for GitHub Actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#organization_ids EnterpriseActionsPermissions#organization_ids}
        '''
        value = EnterpriseActionsPermissionsEnabledOrganizationsConfig(
            organization_ids=organization_ids
        )

        return typing.cast(None, jsii.invoke(self, "putEnabledOrganizationsConfig", [value]))

    @jsii.member(jsii_name="resetAllowedActions")
    def reset_allowed_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedActions", []))

    @jsii.member(jsii_name="resetAllowedActionsConfig")
    def reset_allowed_actions_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedActionsConfig", []))

    @jsii.member(jsii_name="resetEnabledOrganizationsConfig")
    def reset_enabled_organizations_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledOrganizationsConfig", []))

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
    ) -> "EnterpriseActionsPermissionsAllowedActionsConfigOutputReference":
        return typing.cast("EnterpriseActionsPermissionsAllowedActionsConfigOutputReference", jsii.get(self, "allowedActionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="enabledOrganizationsConfig")
    def enabled_organizations_config(
        self,
    ) -> "EnterpriseActionsPermissionsEnabledOrganizationsConfigOutputReference":
        return typing.cast("EnterpriseActionsPermissionsEnabledOrganizationsConfigOutputReference", jsii.get(self, "enabledOrganizationsConfig"))

    @builtins.property
    @jsii.member(jsii_name="allowedActionsConfigInput")
    def allowed_actions_config_input(
        self,
    ) -> typing.Optional["EnterpriseActionsPermissionsAllowedActionsConfig"]:
        return typing.cast(typing.Optional["EnterpriseActionsPermissionsAllowedActionsConfig"], jsii.get(self, "allowedActionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedActionsInput")
    def allowed_actions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledOrganizationsConfigInput")
    def enabled_organizations_config_input(
        self,
    ) -> typing.Optional["EnterpriseActionsPermissionsEnabledOrganizationsConfig"]:
        return typing.cast(typing.Optional["EnterpriseActionsPermissionsEnabledOrganizationsConfig"], jsii.get(self, "enabledOrganizationsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledOrganizationsInput")
    def enabled_organizations_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enabledOrganizationsInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseSlugInput")
    def enterprise_slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseSlugInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0965b19fca362c1844ee8a87e5a052a9fcbb943cf33a69b970f03f9de2a3c6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabledOrganizations")
    def enabled_organizations(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enabledOrganizations"))

    @enabled_organizations.setter
    def enabled_organizations(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99532ccbe302c9bbcd14159789ad89bb81f584198fe31c810e84d644a40e6836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledOrganizations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enterpriseSlug")
    def enterprise_slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseSlug"))

    @enterprise_slug.setter
    def enterprise_slug(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466210f2435522f0e7102e8efbd4756a0d2907b463e9c2fbeaee70e5f09a8d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseSlug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99534b7129a37c9c898207a97dfe348aa0b395d2b0124bc312093ebb6361607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.enterpriseActionsPermissions.EnterpriseActionsPermissionsAllowedActionsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "github_owned_allowed": "githubOwnedAllowed",
        "patterns_allowed": "patternsAllowed",
        "verified_allowed": "verifiedAllowed",
    },
)
class EnterpriseActionsPermissionsAllowedActionsConfig:
    def __init__(
        self,
        *,
        github_owned_allowed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        patterns_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        verified_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param github_owned_allowed: Whether GitHub-owned actions are allowed in the enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#github_owned_allowed EnterpriseActionsPermissions#github_owned_allowed}
        :param patterns_allowed: Specifies a list of string-matching patterns to allow specific action(s). Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#patterns_allowed EnterpriseActionsPermissions#patterns_allowed}
        :param verified_allowed: Whether actions in GitHub Marketplace from verified creators are allowed. Set to 'true' to allow all GitHub Marketplace actions by verified creators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#verified_allowed EnterpriseActionsPermissions#verified_allowed}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03bd8fc8ab0f15b96cdc33b6f602f4aa9adc3cfd894e242b7b3d2ee3a12e8f06)
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
        '''Whether GitHub-owned actions are allowed in the enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#github_owned_allowed EnterpriseActionsPermissions#github_owned_allowed}
        '''
        result = self._values.get("github_owned_allowed")
        assert result is not None, "Required property 'github_owned_allowed' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def patterns_allowed(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of string-matching patterns to allow specific action(s).

        Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#patterns_allowed EnterpriseActionsPermissions#patterns_allowed}
        '''
        result = self._values.get("patterns_allowed")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verified_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether actions in GitHub Marketplace from verified creators are allowed.

        Set to 'true' to allow all GitHub Marketplace actions by verified creators.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#verified_allowed EnterpriseActionsPermissions#verified_allowed}
        '''
        result = self._values.get("verified_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseActionsPermissionsAllowedActionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseActionsPermissionsAllowedActionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.enterpriseActionsPermissions.EnterpriseActionsPermissionsAllowedActionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d87906c08a238ff6aff373f5c807deb50f0e42968918924048d402b8c4c13ce0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7366fb00237466d391beb0693b8bfdf2a3237026a80d002bd40e28f140d5c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubOwnedAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternsAllowed")
    def patterns_allowed(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "patternsAllowed"))

    @patterns_allowed.setter
    def patterns_allowed(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ce04ebd143b107d73fad2713148d56e1a68d5133da405151fb28c8f465bc80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb5dabd15065753f7d180c19bac24bbe598f9bbaa8fbde0a31069c5ef729cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifiedAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EnterpriseActionsPermissionsAllowedActionsConfig]:
        return typing.cast(typing.Optional[EnterpriseActionsPermissionsAllowedActionsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnterpriseActionsPermissionsAllowedActionsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696167f827bb36db1f18cc2a89bef7ea337c8124183b772490970d3d98ee6c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.enterpriseActionsPermissions.EnterpriseActionsPermissionsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled_organizations": "enabledOrganizations",
        "enterprise_slug": "enterpriseSlug",
        "allowed_actions": "allowedActions",
        "allowed_actions_config": "allowedActionsConfig",
        "enabled_organizations_config": "enabledOrganizationsConfig",
        "id": "id",
    },
)
class EnterpriseActionsPermissionsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enabled_organizations: builtins.str,
        enterprise_slug: builtins.str,
        allowed_actions: typing.Optional[builtins.str] = None,
        allowed_actions_config: typing.Optional[typing.Union[EnterpriseActionsPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        enabled_organizations_config: typing.Optional[typing.Union["EnterpriseActionsPermissionsEnabledOrganizationsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param enabled_organizations: The policy that controls the organizations in the enterprise that are allowed to run GitHub Actions. Can be one of: 'all', 'none', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enabled_organizations EnterpriseActionsPermissions#enabled_organizations}
        :param enterprise_slug: The slug of the enterprise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enterprise_slug EnterpriseActionsPermissions#enterprise_slug}
        :param allowed_actions: The permissions policy that controls the actions that are allowed to run. Can be one of: 'all', 'local_only', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#allowed_actions EnterpriseActionsPermissions#allowed_actions}
        :param allowed_actions_config: allowed_actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#allowed_actions_config EnterpriseActionsPermissions#allowed_actions_config}
        :param enabled_organizations_config: enabled_organizations_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enabled_organizations_config EnterpriseActionsPermissions#enabled_organizations_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#id EnterpriseActionsPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(allowed_actions_config, dict):
            allowed_actions_config = EnterpriseActionsPermissionsAllowedActionsConfig(**allowed_actions_config)
        if isinstance(enabled_organizations_config, dict):
            enabled_organizations_config = EnterpriseActionsPermissionsEnabledOrganizationsConfig(**enabled_organizations_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d37d2c2eec7a2b1ba1697adb9b47ec6677f632c906a41ba84735dddb852f57)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled_organizations", value=enabled_organizations, expected_type=type_hints["enabled_organizations"])
            check_type(argname="argument enterprise_slug", value=enterprise_slug, expected_type=type_hints["enterprise_slug"])
            check_type(argname="argument allowed_actions", value=allowed_actions, expected_type=type_hints["allowed_actions"])
            check_type(argname="argument allowed_actions_config", value=allowed_actions_config, expected_type=type_hints["allowed_actions_config"])
            check_type(argname="argument enabled_organizations_config", value=enabled_organizations_config, expected_type=type_hints["enabled_organizations_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled_organizations": enabled_organizations,
            "enterprise_slug": enterprise_slug,
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
        if enabled_organizations_config is not None:
            self._values["enabled_organizations_config"] = enabled_organizations_config
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
    def enabled_organizations(self) -> builtins.str:
        '''The policy that controls the organizations in the enterprise that are allowed to run GitHub Actions.

        Can be one of: 'all', 'none', or 'selected'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enabled_organizations EnterpriseActionsPermissions#enabled_organizations}
        '''
        result = self._values.get("enabled_organizations")
        assert result is not None, "Required property 'enabled_organizations' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enterprise_slug(self) -> builtins.str:
        '''The slug of the enterprise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enterprise_slug EnterpriseActionsPermissions#enterprise_slug}
        '''
        result = self._values.get("enterprise_slug")
        assert result is not None, "Required property 'enterprise_slug' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_actions(self) -> typing.Optional[builtins.str]:
        '''The permissions policy that controls the actions that are allowed to run.

        Can be one of: 'all', 'local_only', or 'selected'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#allowed_actions EnterpriseActionsPermissions#allowed_actions}
        '''
        result = self._values.get("allowed_actions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_actions_config(
        self,
    ) -> typing.Optional[EnterpriseActionsPermissionsAllowedActionsConfig]:
        '''allowed_actions_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#allowed_actions_config EnterpriseActionsPermissions#allowed_actions_config}
        '''
        result = self._values.get("allowed_actions_config")
        return typing.cast(typing.Optional[EnterpriseActionsPermissionsAllowedActionsConfig], result)

    @builtins.property
    def enabled_organizations_config(
        self,
    ) -> typing.Optional["EnterpriseActionsPermissionsEnabledOrganizationsConfig"]:
        '''enabled_organizations_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#enabled_organizations_config EnterpriseActionsPermissions#enabled_organizations_config}
        '''
        result = self._values.get("enabled_organizations_config")
        return typing.cast(typing.Optional["EnterpriseActionsPermissionsEnabledOrganizationsConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#id EnterpriseActionsPermissions#id}.

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
        return "EnterpriseActionsPermissionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.enterpriseActionsPermissions.EnterpriseActionsPermissionsEnabledOrganizationsConfig",
    jsii_struct_bases=[],
    name_mapping={"organization_ids": "organizationIds"},
)
class EnterpriseActionsPermissionsEnabledOrganizationsConfig:
    def __init__(self, *, organization_ids: typing.Sequence[jsii.Number]) -> None:
        '''
        :param organization_ids: List of organization IDs to enable for GitHub Actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#organization_ids EnterpriseActionsPermissions#organization_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6cdd4436e15202dd67c69dc08ff5682b026e0e78da1549563003a9981385b98)
            check_type(argname="argument organization_ids", value=organization_ids, expected_type=type_hints["organization_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "organization_ids": organization_ids,
        }

    @builtins.property
    def organization_ids(self) -> typing.List[jsii.Number]:
        '''List of organization IDs to enable for GitHub Actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/enterprise_actions_permissions#organization_ids EnterpriseActionsPermissions#organization_ids}
        '''
        result = self._values.get("organization_ids")
        assert result is not None, "Required property 'organization_ids' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseActionsPermissionsEnabledOrganizationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseActionsPermissionsEnabledOrganizationsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.enterpriseActionsPermissions.EnterpriseActionsPermissionsEnabledOrganizationsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e93d020fffadb048e1be026e22a7abc121276fc5ba3721c90fef8e356cfd9fbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="organizationIdsInput")
    def organization_ids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "organizationIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationIds")
    def organization_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "organizationIds"))

    @organization_ids.setter
    def organization_ids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b978eb290469a5bc2cbfddc9687e6044bb24f03b6223a89b60c37be9f3f60ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EnterpriseActionsPermissionsEnabledOrganizationsConfig]:
        return typing.cast(typing.Optional[EnterpriseActionsPermissionsEnabledOrganizationsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnterpriseActionsPermissionsEnabledOrganizationsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2945a4b906cf79a240561bad42e029c56515407c3964457039e2883e76e5366e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EnterpriseActionsPermissions",
    "EnterpriseActionsPermissionsAllowedActionsConfig",
    "EnterpriseActionsPermissionsAllowedActionsConfigOutputReference",
    "EnterpriseActionsPermissionsConfig",
    "EnterpriseActionsPermissionsEnabledOrganizationsConfig",
    "EnterpriseActionsPermissionsEnabledOrganizationsConfigOutputReference",
]

publication.publish()

def _typecheckingstub__d513abaf652d4ca2ba7531d0ffecf6aedfa65db0ba77fa427a7a678f2647936c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled_organizations: builtins.str,
    enterprise_slug: builtins.str,
    allowed_actions: typing.Optional[builtins.str] = None,
    allowed_actions_config: typing.Optional[typing.Union[EnterpriseActionsPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled_organizations_config: typing.Optional[typing.Union[EnterpriseActionsPermissionsEnabledOrganizationsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__638d1ce434d9b22f848273a6484f32d79aed50bb5855ac504d20288b236346d5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0965b19fca362c1844ee8a87e5a052a9fcbb943cf33a69b970f03f9de2a3c6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99532ccbe302c9bbcd14159789ad89bb81f584198fe31c810e84d644a40e6836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466210f2435522f0e7102e8efbd4756a0d2907b463e9c2fbeaee70e5f09a8d01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99534b7129a37c9c898207a97dfe348aa0b395d2b0124bc312093ebb6361607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03bd8fc8ab0f15b96cdc33b6f602f4aa9adc3cfd894e242b7b3d2ee3a12e8f06(
    *,
    github_owned_allowed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    patterns_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
    verified_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87906c08a238ff6aff373f5c807deb50f0e42968918924048d402b8c4c13ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7366fb00237466d391beb0693b8bfdf2a3237026a80d002bd40e28f140d5c19(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ce04ebd143b107d73fad2713148d56e1a68d5133da405151fb28c8f465bc80(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb5dabd15065753f7d180c19bac24bbe598f9bbaa8fbde0a31069c5ef729cf5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696167f827bb36db1f18cc2a89bef7ea337c8124183b772490970d3d98ee6c9a(
    value: typing.Optional[EnterpriseActionsPermissionsAllowedActionsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d37d2c2eec7a2b1ba1697adb9b47ec6677f632c906a41ba84735dddb852f57(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled_organizations: builtins.str,
    enterprise_slug: builtins.str,
    allowed_actions: typing.Optional[builtins.str] = None,
    allowed_actions_config: typing.Optional[typing.Union[EnterpriseActionsPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled_organizations_config: typing.Optional[typing.Union[EnterpriseActionsPermissionsEnabledOrganizationsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6cdd4436e15202dd67c69dc08ff5682b026e0e78da1549563003a9981385b98(
    *,
    organization_ids: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93d020fffadb048e1be026e22a7abc121276fc5ba3721c90fef8e356cfd9fbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b978eb290469a5bc2cbfddc9687e6044bb24f03b6223a89b60c37be9f3f60ace(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2945a4b906cf79a240561bad42e029c56515407c3964457039e2883e76e5366e(
    value: typing.Optional[EnterpriseActionsPermissionsEnabledOrganizationsConfig],
) -> None:
    """Type checking stubs"""
    pass
