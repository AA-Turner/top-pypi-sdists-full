r'''
# `azurerm_app_service_source_control`

Refer to the Terraform Registry for docs: [`azurerm_app_service_source_control`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control).
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


class AppServiceSourceControlA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlA",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control azurerm_app_service_source_control}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        github_action_configuration: typing.Optional[typing.Union["AppServiceSourceControlGithubActionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        repo_url: typing.Optional[builtins.str] = None,
        rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AppServiceSourceControlTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_local_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_manual_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_mercurial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control azurerm_app_service_source_control} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_id: The ID of the Windows or Linux Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#app_id AppServiceSourceControlA#app_id}
        :param branch: The branch name to use for deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#branch AppServiceSourceControlA#branch}
        :param github_action_configuration: github_action_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#github_action_configuration AppServiceSourceControlA#github_action_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#id AppServiceSourceControlA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param repo_url: The URL for the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#repo_url AppServiceSourceControlA#repo_url}
        :param rollback_enabled: Should the Deployment Rollback be enabled? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#rollback_enabled AppServiceSourceControlA#rollback_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#timeouts AppServiceSourceControlA#timeouts}
        :param use_local_git: Should the App use local Git configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_local_git AppServiceSourceControlA#use_local_git}
        :param use_manual_integration: Should code be deployed manually. Set to ``false`` to enable continuous integration, such as webhooks into online repos such as GitHub. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_manual_integration AppServiceSourceControlA#use_manual_integration}
        :param use_mercurial: The repository specified is Mercurial. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_mercurial AppServiceSourceControlA#use_mercurial}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e10a1fdb224261867e2fc8d8ff3e4cab48622d4c944c9e0a99dd94ffcf155a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppServiceSourceControlAConfig(
            app_id=app_id,
            branch=branch,
            github_action_configuration=github_action_configuration,
            id=id,
            repo_url=repo_url,
            rollback_enabled=rollback_enabled,
            timeouts=timeouts,
            use_local_git=use_local_git,
            use_manual_integration=use_manual_integration,
            use_mercurial=use_mercurial,
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
        '''Generates CDKTF code for importing a AppServiceSourceControlA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppServiceSourceControlA to import.
        :param import_from_id: The id of the existing AppServiceSourceControlA that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppServiceSourceControlA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e504d9d248c5119437119f8d58916ffb35787f0baf3fd3fb59bca8ef27d652c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGithubActionConfiguration")
    def put_github_action_configuration(
        self,
        *,
        code_configuration: typing.Optional[typing.Union["AppServiceSourceControlGithubActionConfigurationCodeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        container_configuration: typing.Optional[typing.Union["AppServiceSourceControlGithubActionConfigurationContainerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        generate_workflow_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param code_configuration: code_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#code_configuration AppServiceSourceControlA#code_configuration}
        :param container_configuration: container_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#container_configuration AppServiceSourceControlA#container_configuration}
        :param generate_workflow_file: Should the service generate the GitHub Action Workflow file. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#generate_workflow_file AppServiceSourceControlA#generate_workflow_file}
        '''
        value = AppServiceSourceControlGithubActionConfiguration(
            code_configuration=code_configuration,
            container_configuration=container_configuration,
            generate_workflow_file=generate_workflow_file,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubActionConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#create AppServiceSourceControlA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#delete AppServiceSourceControlA#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#read AppServiceSourceControlA#read}.
        '''
        value = AppServiceSourceControlTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetGithubActionConfiguration")
    def reset_github_action_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubActionConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRepoUrl")
    def reset_repo_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepoUrl", []))

    @jsii.member(jsii_name="resetRollbackEnabled")
    def reset_rollback_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollbackEnabled", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUseLocalGit")
    def reset_use_local_git(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseLocalGit", []))

    @jsii.member(jsii_name="resetUseManualIntegration")
    def reset_use_manual_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseManualIntegration", []))

    @jsii.member(jsii_name="resetUseMercurial")
    def reset_use_mercurial(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseMercurial", []))

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
    @jsii.member(jsii_name="githubActionConfiguration")
    def github_action_configuration(
        self,
    ) -> "AppServiceSourceControlGithubActionConfigurationOutputReference":
        return typing.cast("AppServiceSourceControlGithubActionConfigurationOutputReference", jsii.get(self, "githubActionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="scmType")
    def scm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AppServiceSourceControlTimeoutsOutputReference":
        return typing.cast("AppServiceSourceControlTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="usesGithubAction")
    def uses_github_action(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "usesGithubAction"))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="githubActionConfigurationInput")
    def github_action_configuration_input(
        self,
    ) -> typing.Optional["AppServiceSourceControlGithubActionConfiguration"]:
        return typing.cast(typing.Optional["AppServiceSourceControlGithubActionConfiguration"], jsii.get(self, "githubActionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="repoUrlInput")
    def repo_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackEnabledInput")
    def rollback_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rollbackEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppServiceSourceControlTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppServiceSourceControlTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="useLocalGitInput")
    def use_local_git_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useLocalGitInput"))

    @builtins.property
    @jsii.member(jsii_name="useManualIntegrationInput")
    def use_manual_integration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useManualIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="useMercurialInput")
    def use_mercurial_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useMercurialInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17995229d373cf68ff03f5dbb13237c624dee9fad37628b63133927faa936c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99d8d9e5d2dd8c155111f9163994e10fa4c19e9494afa0d89b764ea0bcea077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81adfc2a7c241d25426180eaab6e576f0bcd82fe6b5912037f02fc556f5b823f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoUrl")
    def repo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoUrl"))

    @repo_url.setter
    def repo_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e845a02d08e71afb632cee17a10d053bb68443c9f43ed6e585b2cd6000f811a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rollbackEnabled")
    def rollback_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rollbackEnabled"))

    @rollback_enabled.setter
    def rollback_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9515c0e7a605f191578363fc3551c632ccd914d82e90c0d49aa71d264290dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rollbackEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useLocalGit")
    def use_local_git(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useLocalGit"))

    @use_local_git.setter
    def use_local_git(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96bc3768cd76540d3702ce07df5254d0f72ee136a2bb0d8189ff6f22ed51ca6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLocalGit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useManualIntegration")
    def use_manual_integration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useManualIntegration"))

    @use_manual_integration.setter
    def use_manual_integration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74796729dc8e753d5868de4ece468d7d4dc4eddc48107a6b6fb51bce2e7bd33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useManualIntegration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useMercurial")
    def use_mercurial(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useMercurial"))

    @use_mercurial.setter
    def use_mercurial(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b77235c0d87b0c4f3898b3dedd407167e4b3536eb939c098395088d9ed05f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useMercurial", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_id": "appId",
        "branch": "branch",
        "github_action_configuration": "githubActionConfiguration",
        "id": "id",
        "repo_url": "repoUrl",
        "rollback_enabled": "rollbackEnabled",
        "timeouts": "timeouts",
        "use_local_git": "useLocalGit",
        "use_manual_integration": "useManualIntegration",
        "use_mercurial": "useMercurial",
    },
)
class AppServiceSourceControlAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        github_action_configuration: typing.Optional[typing.Union["AppServiceSourceControlGithubActionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        repo_url: typing.Optional[builtins.str] = None,
        rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AppServiceSourceControlTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        use_local_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_manual_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_mercurial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_id: The ID of the Windows or Linux Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#app_id AppServiceSourceControlA#app_id}
        :param branch: The branch name to use for deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#branch AppServiceSourceControlA#branch}
        :param github_action_configuration: github_action_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#github_action_configuration AppServiceSourceControlA#github_action_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#id AppServiceSourceControlA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param repo_url: The URL for the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#repo_url AppServiceSourceControlA#repo_url}
        :param rollback_enabled: Should the Deployment Rollback be enabled? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#rollback_enabled AppServiceSourceControlA#rollback_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#timeouts AppServiceSourceControlA#timeouts}
        :param use_local_git: Should the App use local Git configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_local_git AppServiceSourceControlA#use_local_git}
        :param use_manual_integration: Should code be deployed manually. Set to ``false`` to enable continuous integration, such as webhooks into online repos such as GitHub. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_manual_integration AppServiceSourceControlA#use_manual_integration}
        :param use_mercurial: The repository specified is Mercurial. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_mercurial AppServiceSourceControlA#use_mercurial}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(github_action_configuration, dict):
            github_action_configuration = AppServiceSourceControlGithubActionConfiguration(**github_action_configuration)
        if isinstance(timeouts, dict):
            timeouts = AppServiceSourceControlTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4bbeb6848486f98657f49bcc531011eada105db6f4771be5deee91feb5f06fc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument github_action_configuration", value=github_action_configuration, expected_type=type_hints["github_action_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument repo_url", value=repo_url, expected_type=type_hints["repo_url"])
            check_type(argname="argument rollback_enabled", value=rollback_enabled, expected_type=type_hints["rollback_enabled"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument use_local_git", value=use_local_git, expected_type=type_hints["use_local_git"])
            check_type(argname="argument use_manual_integration", value=use_manual_integration, expected_type=type_hints["use_manual_integration"])
            check_type(argname="argument use_mercurial", value=use_mercurial, expected_type=type_hints["use_mercurial"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
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
        if branch is not None:
            self._values["branch"] = branch
        if github_action_configuration is not None:
            self._values["github_action_configuration"] = github_action_configuration
        if id is not None:
            self._values["id"] = id
        if repo_url is not None:
            self._values["repo_url"] = repo_url
        if rollback_enabled is not None:
            self._values["rollback_enabled"] = rollback_enabled
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if use_local_git is not None:
            self._values["use_local_git"] = use_local_git
        if use_manual_integration is not None:
            self._values["use_manual_integration"] = use_manual_integration
        if use_mercurial is not None:
            self._values["use_mercurial"] = use_mercurial

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
    def app_id(self) -> builtins.str:
        '''The ID of the Windows or Linux Web App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#app_id AppServiceSourceControlA#app_id}
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''The branch name to use for deployments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#branch AppServiceSourceControlA#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_action_configuration(
        self,
    ) -> typing.Optional["AppServiceSourceControlGithubActionConfiguration"]:
        '''github_action_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#github_action_configuration AppServiceSourceControlA#github_action_configuration}
        '''
        result = self._values.get("github_action_configuration")
        return typing.cast(typing.Optional["AppServiceSourceControlGithubActionConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#id AppServiceSourceControlA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo_url(self) -> typing.Optional[builtins.str]:
        '''The URL for the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#repo_url AppServiceSourceControlA#repo_url}
        '''
        result = self._values.get("repo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollback_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Deployment Rollback be enabled? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#rollback_enabled AppServiceSourceControlA#rollback_enabled}
        '''
        result = self._values.get("rollback_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppServiceSourceControlTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#timeouts AppServiceSourceControlA#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppServiceSourceControlTimeouts"], result)

    @builtins.property
    def use_local_git(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the App use local Git configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_local_git AppServiceSourceControlA#use_local_git}
        '''
        result = self._values.get("use_local_git")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_manual_integration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should code be deployed manually.

        Set to ``false`` to enable continuous integration, such as webhooks into online repos such as GitHub. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_manual_integration AppServiceSourceControlA#use_manual_integration}
        '''
        result = self._values.get("use_manual_integration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_mercurial(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The repository specified is Mercurial. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#use_mercurial AppServiceSourceControlA#use_mercurial}
        '''
        result = self._values.get("use_mercurial")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlGithubActionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "code_configuration": "codeConfiguration",
        "container_configuration": "containerConfiguration",
        "generate_workflow_file": "generateWorkflowFile",
    },
)
class AppServiceSourceControlGithubActionConfiguration:
    def __init__(
        self,
        *,
        code_configuration: typing.Optional[typing.Union["AppServiceSourceControlGithubActionConfigurationCodeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        container_configuration: typing.Optional[typing.Union["AppServiceSourceControlGithubActionConfigurationContainerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        generate_workflow_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param code_configuration: code_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#code_configuration AppServiceSourceControlA#code_configuration}
        :param container_configuration: container_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#container_configuration AppServiceSourceControlA#container_configuration}
        :param generate_workflow_file: Should the service generate the GitHub Action Workflow file. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#generate_workflow_file AppServiceSourceControlA#generate_workflow_file}
        '''
        if isinstance(code_configuration, dict):
            code_configuration = AppServiceSourceControlGithubActionConfigurationCodeConfiguration(**code_configuration)
        if isinstance(container_configuration, dict):
            container_configuration = AppServiceSourceControlGithubActionConfigurationContainerConfiguration(**container_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1883dfc909edbd0b5c90fa77aa8eeea64d1a327bb2f28a88c08dc9c31dd0f006)
            check_type(argname="argument code_configuration", value=code_configuration, expected_type=type_hints["code_configuration"])
            check_type(argname="argument container_configuration", value=container_configuration, expected_type=type_hints["container_configuration"])
            check_type(argname="argument generate_workflow_file", value=generate_workflow_file, expected_type=type_hints["generate_workflow_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_configuration is not None:
            self._values["code_configuration"] = code_configuration
        if container_configuration is not None:
            self._values["container_configuration"] = container_configuration
        if generate_workflow_file is not None:
            self._values["generate_workflow_file"] = generate_workflow_file

    @builtins.property
    def code_configuration(
        self,
    ) -> typing.Optional["AppServiceSourceControlGithubActionConfigurationCodeConfiguration"]:
        '''code_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#code_configuration AppServiceSourceControlA#code_configuration}
        '''
        result = self._values.get("code_configuration")
        return typing.cast(typing.Optional["AppServiceSourceControlGithubActionConfigurationCodeConfiguration"], result)

    @builtins.property
    def container_configuration(
        self,
    ) -> typing.Optional["AppServiceSourceControlGithubActionConfigurationContainerConfiguration"]:
        '''container_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#container_configuration AppServiceSourceControlA#container_configuration}
        '''
        result = self._values.get("container_configuration")
        return typing.cast(typing.Optional["AppServiceSourceControlGithubActionConfigurationContainerConfiguration"], result)

    @builtins.property
    def generate_workflow_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the service generate the GitHub Action Workflow file. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#generate_workflow_file AppServiceSourceControlA#generate_workflow_file}
        '''
        result = self._values.get("generate_workflow_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlGithubActionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlGithubActionConfigurationCodeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "runtime_stack": "runtimeStack",
        "runtime_version": "runtimeVersion",
    },
)
class AppServiceSourceControlGithubActionConfigurationCodeConfiguration:
    def __init__(
        self,
        *,
        runtime_stack: builtins.str,
        runtime_version: builtins.str,
    ) -> None:
        '''
        :param runtime_stack: The value to use for the Runtime Stack in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#runtime_stack AppServiceSourceControlA#runtime_stack}
        :param runtime_version: The value to use for the Runtime Version in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#runtime_version AppServiceSourceControlA#runtime_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca63367f0d389ffcee7a748d5bbca888809110581fc165124db7f3d6a4029c2)
            check_type(argname="argument runtime_stack", value=runtime_stack, expected_type=type_hints["runtime_stack"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime_stack": runtime_stack,
            "runtime_version": runtime_version,
        }

    @builtins.property
    def runtime_stack(self) -> builtins.str:
        '''The value to use for the Runtime Stack in the workflow file content for code base apps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#runtime_stack AppServiceSourceControlA#runtime_stack}
        '''
        result = self._values.get("runtime_stack")
        assert result is not None, "Required property 'runtime_stack' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''The value to use for the Runtime Version in the workflow file content for code base apps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#runtime_version AppServiceSourceControlA#runtime_version}
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlGithubActionConfigurationCodeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppServiceSourceControlGithubActionConfigurationCodeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlGithubActionConfigurationCodeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9f03ecdcabcedc12f74073d68fc85ce5f3bab1539b3a4b738fa31c41a914eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="runtimeStackInput")
    def runtime_stack_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeStackInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeStack")
    def runtime_stack(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeStack"))

    @runtime_stack.setter
    def runtime_stack(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee223e3b65af05797b02223a5aeb1144811f2ef3203ffe3459ee009e45a882c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeStack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed69d66085fa590774210883fe7b5e666008fa20318d1fd051d4959aa0fffff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppServiceSourceControlGithubActionConfigurationCodeConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlGithubActionConfigurationCodeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppServiceSourceControlGithubActionConfigurationCodeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f245b792c8564f6e0618164d45f512434a12c503d239fb9d2b339b6cbc8a191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlGithubActionConfigurationContainerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "image_name": "imageName",
        "registry_url": "registryUrl",
        "registry_password": "registryPassword",
        "registry_username": "registryUsername",
    },
)
class AppServiceSourceControlGithubActionConfigurationContainerConfiguration:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        registry_url: builtins.str,
        registry_password: typing.Optional[builtins.str] = None,
        registry_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_name: The image name for the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#image_name AppServiceSourceControlA#image_name}
        :param registry_url: The server URL for the container registry where the build will be hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_url AppServiceSourceControlA#registry_url}
        :param registry_password: The password used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_password AppServiceSourceControlA#registry_password}
        :param registry_username: The username used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_username AppServiceSourceControlA#registry_username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e5bd25a2f95a8e66ad8ceac3f9c668212a25b655790c1cb8bc2abc99cff194)
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument registry_url", value=registry_url, expected_type=type_hints["registry_url"])
            check_type(argname="argument registry_password", value=registry_password, expected_type=type_hints["registry_password"])
            check_type(argname="argument registry_username", value=registry_username, expected_type=type_hints["registry_username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_name": image_name,
            "registry_url": registry_url,
        }
        if registry_password is not None:
            self._values["registry_password"] = registry_password
        if registry_username is not None:
            self._values["registry_username"] = registry_username

    @builtins.property
    def image_name(self) -> builtins.str:
        '''The image name for the build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#image_name AppServiceSourceControlA#image_name}
        '''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_url(self) -> builtins.str:
        '''The server URL for the container registry where the build will be hosted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_url AppServiceSourceControlA#registry_url}
        '''
        result = self._values.get("registry_url")
        assert result is not None, "Required property 'registry_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_password(self) -> typing.Optional[builtins.str]:
        '''The password used to upload the image to the container registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_password AppServiceSourceControlA#registry_password}
        '''
        result = self._values.get("registry_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_username(self) -> typing.Optional[builtins.str]:
        '''The username used to upload the image to the container registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_username AppServiceSourceControlA#registry_username}
        '''
        result = self._values.get("registry_username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlGithubActionConfigurationContainerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppServiceSourceControlGithubActionConfigurationContainerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlGithubActionConfigurationContainerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d45012296cf605ace68aaf2cc0216ce9c644e938a2b00ad2eeb4f1f9f4c5e568)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRegistryPassword")
    def reset_registry_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryPassword", []))

    @jsii.member(jsii_name="resetRegistryUsername")
    def reset_registry_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryUsername", []))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="registryPasswordInput")
    def registry_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="registryUrlInput")
    def registry_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="registryUsernameInput")
    def registry_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a070584b4839738b3b9b8848fc19e49891fba7d869b3580e2e81f0c58b718b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryPassword")
    def registry_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryPassword"))

    @registry_password.setter
    def registry_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b04bea82e1f7740cf439f90d169fc2d836fa646954cef12465cc36c8044dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryUrl")
    def registry_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUrl"))

    @registry_url.setter
    def registry_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcac657f47dabb548a333a2598bf22d70c084e35e34715df6b257d7edc9a7bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryUsername")
    def registry_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUsername"))

    @registry_username.setter
    def registry_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb3d03e29c69354a14fa91fa15dbafc6490cbd73625b2a49c687361e66407bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppServiceSourceControlGithubActionConfigurationContainerConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlGithubActionConfigurationContainerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppServiceSourceControlGithubActionConfigurationContainerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4c3bdab5064fbc2f674161ac3b5a57f38e971199dc015c4c07548c1c5aed0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppServiceSourceControlGithubActionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlGithubActionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__244741aaa50b6dc941a54ddf90971b64b1c70b7002d18b98d57246d581fbdb4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeConfiguration")
    def put_code_configuration(
        self,
        *,
        runtime_stack: builtins.str,
        runtime_version: builtins.str,
    ) -> None:
        '''
        :param runtime_stack: The value to use for the Runtime Stack in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#runtime_stack AppServiceSourceControlA#runtime_stack}
        :param runtime_version: The value to use for the Runtime Version in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#runtime_version AppServiceSourceControlA#runtime_version}
        '''
        value = AppServiceSourceControlGithubActionConfigurationCodeConfiguration(
            runtime_stack=runtime_stack, runtime_version=runtime_version
        )

        return typing.cast(None, jsii.invoke(self, "putCodeConfiguration", [value]))

    @jsii.member(jsii_name="putContainerConfiguration")
    def put_container_configuration(
        self,
        *,
        image_name: builtins.str,
        registry_url: builtins.str,
        registry_password: typing.Optional[builtins.str] = None,
        registry_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_name: The image name for the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#image_name AppServiceSourceControlA#image_name}
        :param registry_url: The server URL for the container registry where the build will be hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_url AppServiceSourceControlA#registry_url}
        :param registry_password: The password used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_password AppServiceSourceControlA#registry_password}
        :param registry_username: The username used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#registry_username AppServiceSourceControlA#registry_username}
        '''
        value = AppServiceSourceControlGithubActionConfigurationContainerConfiguration(
            image_name=image_name,
            registry_url=registry_url,
            registry_password=registry_password,
            registry_username=registry_username,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerConfiguration", [value]))

    @jsii.member(jsii_name="resetCodeConfiguration")
    def reset_code_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeConfiguration", []))

    @jsii.member(jsii_name="resetContainerConfiguration")
    def reset_container_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerConfiguration", []))

    @jsii.member(jsii_name="resetGenerateWorkflowFile")
    def reset_generate_workflow_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerateWorkflowFile", []))

    @builtins.property
    @jsii.member(jsii_name="codeConfiguration")
    def code_configuration(
        self,
    ) -> AppServiceSourceControlGithubActionConfigurationCodeConfigurationOutputReference:
        return typing.cast(AppServiceSourceControlGithubActionConfigurationCodeConfigurationOutputReference, jsii.get(self, "codeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="containerConfiguration")
    def container_configuration(
        self,
    ) -> AppServiceSourceControlGithubActionConfigurationContainerConfigurationOutputReference:
        return typing.cast(AppServiceSourceControlGithubActionConfigurationContainerConfigurationOutputReference, jsii.get(self, "containerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="linuxAction")
    def linux_action(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "linuxAction"))

    @builtins.property
    @jsii.member(jsii_name="codeConfigurationInput")
    def code_configuration_input(
        self,
    ) -> typing.Optional[AppServiceSourceControlGithubActionConfigurationCodeConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlGithubActionConfigurationCodeConfiguration], jsii.get(self, "codeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="containerConfigurationInput")
    def container_configuration_input(
        self,
    ) -> typing.Optional[AppServiceSourceControlGithubActionConfigurationContainerConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlGithubActionConfigurationContainerConfiguration], jsii.get(self, "containerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="generateWorkflowFileInput")
    def generate_workflow_file_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "generateWorkflowFileInput"))

    @builtins.property
    @jsii.member(jsii_name="generateWorkflowFile")
    def generate_workflow_file(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "generateWorkflowFile"))

    @generate_workflow_file.setter
    def generate_workflow_file(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09eaf689f2a050817293b5e03e3a20257decce2d03c63301fe2232b20fd697a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateWorkflowFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppServiceSourceControlGithubActionConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlGithubActionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppServiceSourceControlGithubActionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d47810e132c253be83f3ab48f48ffd649f6e1bbdfc970dcc27ff0040c37a37f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class AppServiceSourceControlTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#create AppServiceSourceControlA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#delete AppServiceSourceControlA#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#read AppServiceSourceControlA#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b7754375cae1e6930905791fa204a3d8f1465b7f25946012dadd4b8d091ccf)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#create AppServiceSourceControlA#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#delete AppServiceSourceControlA#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control#read AppServiceSourceControlA#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppServiceSourceControlTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControl.AppServiceSourceControlTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a98ee7f72f8afac7915f59332f3513a6ff1ce5c697c1397b1a8960e2b72090b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7354eebb405a6cfcbcaa03b8a66c2c0991582c3306d13d746f075be483f990c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d0175d32396346d290755042a670a6dc4c713af6207650646bb9343451080f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c11187255f64a44223b6a2a7c9addcb85d30da4a55e8dfc935d0d91935c186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911fddbf94f02b1f8126cc4c93b7565e02faf908d4ae73e47ababc00c39cdfbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppServiceSourceControlA",
    "AppServiceSourceControlAConfig",
    "AppServiceSourceControlGithubActionConfiguration",
    "AppServiceSourceControlGithubActionConfigurationCodeConfiguration",
    "AppServiceSourceControlGithubActionConfigurationCodeConfigurationOutputReference",
    "AppServiceSourceControlGithubActionConfigurationContainerConfiguration",
    "AppServiceSourceControlGithubActionConfigurationContainerConfigurationOutputReference",
    "AppServiceSourceControlGithubActionConfigurationOutputReference",
    "AppServiceSourceControlTimeouts",
    "AppServiceSourceControlTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7e10a1fdb224261867e2fc8d8ff3e4cab48622d4c944c9e0a99dd94ffcf155a4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_id: builtins.str,
    branch: typing.Optional[builtins.str] = None,
    github_action_configuration: typing.Optional[typing.Union[AppServiceSourceControlGithubActionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    repo_url: typing.Optional[builtins.str] = None,
    rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AppServiceSourceControlTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_local_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_manual_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_mercurial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__5e504d9d248c5119437119f8d58916ffb35787f0baf3fd3fb59bca8ef27d652c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17995229d373cf68ff03f5dbb13237c624dee9fad37628b63133927faa936c70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99d8d9e5d2dd8c155111f9163994e10fa4c19e9494afa0d89b764ea0bcea077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81adfc2a7c241d25426180eaab6e576f0bcd82fe6b5912037f02fc556f5b823f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e845a02d08e71afb632cee17a10d053bb68443c9f43ed6e585b2cd6000f811a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9515c0e7a605f191578363fc3551c632ccd914d82e90c0d49aa71d264290dae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bc3768cd76540d3702ce07df5254d0f72ee136a2bb0d8189ff6f22ed51ca6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74796729dc8e753d5868de4ece468d7d4dc4eddc48107a6b6fb51bce2e7bd33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b77235c0d87b0c4f3898b3dedd407167e4b3536eb939c098395088d9ed05f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bbeb6848486f98657f49bcc531011eada105db6f4771be5deee91feb5f06fc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_id: builtins.str,
    branch: typing.Optional[builtins.str] = None,
    github_action_configuration: typing.Optional[typing.Union[AppServiceSourceControlGithubActionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    repo_url: typing.Optional[builtins.str] = None,
    rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AppServiceSourceControlTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_local_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_manual_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_mercurial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1883dfc909edbd0b5c90fa77aa8eeea64d1a327bb2f28a88c08dc9c31dd0f006(
    *,
    code_configuration: typing.Optional[typing.Union[AppServiceSourceControlGithubActionConfigurationCodeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    container_configuration: typing.Optional[typing.Union[AppServiceSourceControlGithubActionConfigurationContainerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    generate_workflow_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca63367f0d389ffcee7a748d5bbca888809110581fc165124db7f3d6a4029c2(
    *,
    runtime_stack: builtins.str,
    runtime_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f03ecdcabcedc12f74073d68fc85ce5f3bab1539b3a4b738fa31c41a914eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee223e3b65af05797b02223a5aeb1144811f2ef3203ffe3459ee009e45a882c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed69d66085fa590774210883fe7b5e666008fa20318d1fd051d4959aa0fffff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f245b792c8564f6e0618164d45f512434a12c503d239fb9d2b339b6cbc8a191(
    value: typing.Optional[AppServiceSourceControlGithubActionConfigurationCodeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e5bd25a2f95a8e66ad8ceac3f9c668212a25b655790c1cb8bc2abc99cff194(
    *,
    image_name: builtins.str,
    registry_url: builtins.str,
    registry_password: typing.Optional[builtins.str] = None,
    registry_username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45012296cf605ace68aaf2cc0216ce9c644e938a2b00ad2eeb4f1f9f4c5e568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a070584b4839738b3b9b8848fc19e49891fba7d869b3580e2e81f0c58b718b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b04bea82e1f7740cf439f90d169fc2d836fa646954cef12465cc36c8044dfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcac657f47dabb548a333a2598bf22d70c084e35e34715df6b257d7edc9a7bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3d03e29c69354a14fa91fa15dbafc6490cbd73625b2a49c687361e66407bec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4c3bdab5064fbc2f674161ac3b5a57f38e971199dc015c4c07548c1c5aed0a(
    value: typing.Optional[AppServiceSourceControlGithubActionConfigurationContainerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244741aaa50b6dc941a54ddf90971b64b1c70b7002d18b98d57246d581fbdb4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09eaf689f2a050817293b5e03e3a20257decce2d03c63301fe2232b20fd697a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d47810e132c253be83f3ab48f48ffd649f6e1bbdfc970dcc27ff0040c37a37f(
    value: typing.Optional[AppServiceSourceControlGithubActionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b7754375cae1e6930905791fa204a3d8f1465b7f25946012dadd4b8d091ccf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98ee7f72f8afac7915f59332f3513a6ff1ce5c697c1397b1a8960e2b72090b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7354eebb405a6cfcbcaa03b8a66c2c0991582c3306d13d746f075be483f990c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d0175d32396346d290755042a670a6dc4c713af6207650646bb9343451080f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c11187255f64a44223b6a2a7c9addcb85d30da4a55e8dfc935d0d91935c186(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911fddbf94f02b1f8126cc4c93b7565e02faf908d4ae73e47ababc00c39cdfbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
