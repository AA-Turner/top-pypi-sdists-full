r'''
# `github_actions_repository_permissions`

Refer to the Terraform Registry for docs: [`github_actions_repository_permissions`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions).
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


class ActionsRepositoryPermissions(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsRepositoryPermissions.ActionsRepositoryPermissions",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions github_actions_repository_permissions}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        repository: builtins.str,
        allowed_actions: typing.Optional[builtins.str] = None,
        allowed_actions_config: typing.Optional[typing.Union["ActionsRepositoryPermissionsAllowedActionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions github_actions_repository_permissions} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param repository: The GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#repository ActionsRepositoryPermissions#repository}
        :param allowed_actions: The permissions policy that controls the actions that are allowed to run. Can be one of: 'all', 'local_only', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#allowed_actions ActionsRepositoryPermissions#allowed_actions}
        :param allowed_actions_config: allowed_actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#allowed_actions_config ActionsRepositoryPermissions#allowed_actions_config}
        :param enabled: Should GitHub actions be enabled on this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#enabled ActionsRepositoryPermissions#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#id ActionsRepositoryPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee850e3d83453bfe0da6438e07616f5a87ad452f0ce139c822f0c1792aca94a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ActionsRepositoryPermissionsConfig(
            repository=repository,
            allowed_actions=allowed_actions,
            allowed_actions_config=allowed_actions_config,
            enabled=enabled,
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
        '''Generates CDKTF code for importing a ActionsRepositoryPermissions resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ActionsRepositoryPermissions to import.
        :param import_from_id: The id of the existing ActionsRepositoryPermissions that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ActionsRepositoryPermissions to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df53ea32bb60b492963d23a73201b84cc22628b7d907368e0d091d0dba535bbe)
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
        :param github_owned_allowed: Whether GitHub-owned actions are allowed in the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#github_owned_allowed ActionsRepositoryPermissions#github_owned_allowed}
        :param patterns_allowed: Specifies a list of string-matching patterns to allow specific action(s). Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#patterns_allowed ActionsRepositoryPermissions#patterns_allowed}
        :param verified_allowed: Whether actions in GitHub Marketplace from verified creators are allowed. Set to 'true' to allow all GitHub Marketplace actions by verified creators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#verified_allowed ActionsRepositoryPermissions#verified_allowed}
        '''
        value = ActionsRepositoryPermissionsAllowedActionsConfig(
            github_owned_allowed=github_owned_allowed,
            patterns_allowed=patterns_allowed,
            verified_allowed=verified_allowed,
        )

        return typing.cast(None, jsii.invoke(self, "putAllowedActionsConfig", [value]))

    @jsii.member(jsii_name="resetAllowedActions")
    def reset_allowed_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedActions", []))

    @jsii.member(jsii_name="resetAllowedActionsConfig")
    def reset_allowed_actions_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedActionsConfig", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
    ) -> "ActionsRepositoryPermissionsAllowedActionsConfigOutputReference":
        return typing.cast("ActionsRepositoryPermissionsAllowedActionsConfigOutputReference", jsii.get(self, "allowedActionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="allowedActionsConfigInput")
    def allowed_actions_config_input(
        self,
    ) -> typing.Optional["ActionsRepositoryPermissionsAllowedActionsConfig"]:
        return typing.cast(typing.Optional["ActionsRepositoryPermissionsAllowedActionsConfig"], jsii.get(self, "allowedActionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedActionsInput")
    def allowed_actions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedActions")
    def allowed_actions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedActions"))

    @allowed_actions.setter
    def allowed_actions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7277b1d979f001d9a38d558e2b6dcef896846ef56265c8c83df6f66fc3331e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118ca2b45f5e70172d01e9026eb8fa5f864cb060b2f6256d9e244b448ac65da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb56ad8d2ba81c2f0a31f3b7c47b46b0ac8f98a3936cfa9ffdea8ae75f59cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd08c7ddea151d27c6a00260a1be28a7f5353662e62ffb3a1c00beeb2d4c171a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsRepositoryPermissions.ActionsRepositoryPermissionsAllowedActionsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "github_owned_allowed": "githubOwnedAllowed",
        "patterns_allowed": "patternsAllowed",
        "verified_allowed": "verifiedAllowed",
    },
)
class ActionsRepositoryPermissionsAllowedActionsConfig:
    def __init__(
        self,
        *,
        github_owned_allowed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        patterns_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
        verified_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param github_owned_allowed: Whether GitHub-owned actions are allowed in the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#github_owned_allowed ActionsRepositoryPermissions#github_owned_allowed}
        :param patterns_allowed: Specifies a list of string-matching patterns to allow specific action(s). Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#patterns_allowed ActionsRepositoryPermissions#patterns_allowed}
        :param verified_allowed: Whether actions in GitHub Marketplace from verified creators are allowed. Set to 'true' to allow all GitHub Marketplace actions by verified creators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#verified_allowed ActionsRepositoryPermissions#verified_allowed}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f506c64ab5b99bfd8d6170495dd8f8d8d49b469916acb895d9e53f8ebc3a094b)
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
        '''Whether GitHub-owned actions are allowed in the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#github_owned_allowed ActionsRepositoryPermissions#github_owned_allowed}
        '''
        result = self._values.get("github_owned_allowed")
        assert result is not None, "Required property 'github_owned_allowed' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def patterns_allowed(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of string-matching patterns to allow specific action(s).

        Wildcards, tags, and SHAs are allowed. For example, 'monalisa/octocat@', 'monalisa/octocat@v2', 'monalisa/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#patterns_allowed ActionsRepositoryPermissions#patterns_allowed}
        '''
        result = self._values.get("patterns_allowed")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verified_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether actions in GitHub Marketplace from verified creators are allowed.

        Set to 'true' to allow all GitHub Marketplace actions by verified creators.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#verified_allowed ActionsRepositoryPermissions#verified_allowed}
        '''
        result = self._values.get("verified_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsRepositoryPermissionsAllowedActionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsRepositoryPermissionsAllowedActionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsRepositoryPermissions.ActionsRepositoryPermissionsAllowedActionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf1dcc1191031a8962b8d5aff6a59659240934d2b392b55f47366527e8972b62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11290cb9793aa89e78c38fa18929bd2fb442f1e5a86f2e1df52c68e63d50bbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubOwnedAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="patternsAllowed")
    def patterns_allowed(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "patternsAllowed"))

    @patterns_allowed.setter
    def patterns_allowed(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d31d83dae33f5f5dd0152dd37d2c6ec245552edb7170b1ea3df054dbf4d399)
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
            type_hints = typing.get_type_hints(_typecheckingstub__244404a517fedb6e6a72e58d0a947a67114204b474e078c1e2f1a54b8a800144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifiedAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ActionsRepositoryPermissionsAllowedActionsConfig]:
        return typing.cast(typing.Optional[ActionsRepositoryPermissionsAllowedActionsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActionsRepositoryPermissionsAllowedActionsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3963dcc4ed6c254157d7f970e62ddecb5b4f2a0dca7ac7c1142a6c23054732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsRepositoryPermissions.ActionsRepositoryPermissionsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "repository": "repository",
        "allowed_actions": "allowedActions",
        "allowed_actions_config": "allowedActionsConfig",
        "enabled": "enabled",
        "id": "id",
    },
)
class ActionsRepositoryPermissionsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        repository: builtins.str,
        allowed_actions: typing.Optional[builtins.str] = None,
        allowed_actions_config: typing.Optional[typing.Union[ActionsRepositoryPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param repository: The GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#repository ActionsRepositoryPermissions#repository}
        :param allowed_actions: The permissions policy that controls the actions that are allowed to run. Can be one of: 'all', 'local_only', or 'selected'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#allowed_actions ActionsRepositoryPermissions#allowed_actions}
        :param allowed_actions_config: allowed_actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#allowed_actions_config ActionsRepositoryPermissions#allowed_actions_config}
        :param enabled: Should GitHub actions be enabled on this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#enabled ActionsRepositoryPermissions#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#id ActionsRepositoryPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(allowed_actions_config, dict):
            allowed_actions_config = ActionsRepositoryPermissionsAllowedActionsConfig(**allowed_actions_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56e4cba9083e092710fb2012a3a450c0e6ae4e0dd0fd263ea74cb149465205c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument allowed_actions", value=allowed_actions, expected_type=type_hints["allowed_actions"])
            check_type(argname="argument allowed_actions_config", value=allowed_actions_config, expected_type=type_hints["allowed_actions_config"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
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
        if enabled is not None:
            self._values["enabled"] = enabled
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
    def repository(self) -> builtins.str:
        '''The GitHub repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#repository ActionsRepositoryPermissions#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_actions(self) -> typing.Optional[builtins.str]:
        '''The permissions policy that controls the actions that are allowed to run.

        Can be one of: 'all', 'local_only', or 'selected'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#allowed_actions ActionsRepositoryPermissions#allowed_actions}
        '''
        result = self._values.get("allowed_actions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_actions_config(
        self,
    ) -> typing.Optional[ActionsRepositoryPermissionsAllowedActionsConfig]:
        '''allowed_actions_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#allowed_actions_config ActionsRepositoryPermissions#allowed_actions_config}
        '''
        result = self._values.get("allowed_actions_config")
        return typing.cast(typing.Optional[ActionsRepositoryPermissionsAllowedActionsConfig], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should GitHub actions be enabled on this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#enabled ActionsRepositoryPermissions#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/actions_repository_permissions#id ActionsRepositoryPermissions#id}.

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
        return "ActionsRepositoryPermissionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ActionsRepositoryPermissions",
    "ActionsRepositoryPermissionsAllowedActionsConfig",
    "ActionsRepositoryPermissionsAllowedActionsConfigOutputReference",
    "ActionsRepositoryPermissionsConfig",
]

publication.publish()

def _typecheckingstub__3ee850e3d83453bfe0da6438e07616f5a87ad452f0ce139c822f0c1792aca94a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    repository: builtins.str,
    allowed_actions: typing.Optional[builtins.str] = None,
    allowed_actions_config: typing.Optional[typing.Union[ActionsRepositoryPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__df53ea32bb60b492963d23a73201b84cc22628b7d907368e0d091d0dba535bbe(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7277b1d979f001d9a38d558e2b6dcef896846ef56265c8c83df6f66fc3331e7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118ca2b45f5e70172d01e9026eb8fa5f864cb060b2f6256d9e244b448ac65da4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb56ad8d2ba81c2f0a31f3b7c47b46b0ac8f98a3936cfa9ffdea8ae75f59cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd08c7ddea151d27c6a00260a1be28a7f5353662e62ffb3a1c00beeb2d4c171a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f506c64ab5b99bfd8d6170495dd8f8d8d49b469916acb895d9e53f8ebc3a094b(
    *,
    github_owned_allowed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    patterns_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
    verified_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1dcc1191031a8962b8d5aff6a59659240934d2b392b55f47366527e8972b62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11290cb9793aa89e78c38fa18929bd2fb442f1e5a86f2e1df52c68e63d50bbef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d31d83dae33f5f5dd0152dd37d2c6ec245552edb7170b1ea3df054dbf4d399(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244404a517fedb6e6a72e58d0a947a67114204b474e078c1e2f1a54b8a800144(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3963dcc4ed6c254157d7f970e62ddecb5b4f2a0dca7ac7c1142a6c23054732(
    value: typing.Optional[ActionsRepositoryPermissionsAllowedActionsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56e4cba9083e092710fb2012a3a450c0e6ae4e0dd0fd263ea74cb149465205c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    repository: builtins.str,
    allowed_actions: typing.Optional[builtins.str] = None,
    allowed_actions_config: typing.Optional[typing.Union[ActionsRepositoryPermissionsAllowedActionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
