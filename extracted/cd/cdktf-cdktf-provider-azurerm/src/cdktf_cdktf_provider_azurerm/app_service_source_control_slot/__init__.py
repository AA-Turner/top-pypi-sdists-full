r'''
# `azurerm_app_service_source_control_slot`

Refer to the Terraform Registry for docs: [`azurerm_app_service_source_control_slot`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot).
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


class AppServiceSourceControlSlot(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlot",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot azurerm_app_service_source_control_slot}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        slot_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        github_action_configuration: typing.Optional[typing.Union["AppServiceSourceControlSlotGithubActionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        repo_url: typing.Optional[builtins.str] = None,
        rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AppServiceSourceControlSlotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot azurerm_app_service_source_control_slot} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param slot_id: The ID of the Linux or Windows Web App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#slot_id AppServiceSourceControlSlot#slot_id}
        :param branch: The URL for the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#branch AppServiceSourceControlSlot#branch}
        :param github_action_configuration: github_action_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#github_action_configuration AppServiceSourceControlSlot#github_action_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#id AppServiceSourceControlSlot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param repo_url: The branch name to use for deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#repo_url AppServiceSourceControlSlot#repo_url}
        :param rollback_enabled: Should the Deployment Rollback be enabled? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#rollback_enabled AppServiceSourceControlSlot#rollback_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#timeouts AppServiceSourceControlSlot#timeouts}
        :param use_local_git: Should the Slot use local Git configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_local_git AppServiceSourceControlSlot#use_local_git}
        :param use_manual_integration: Should code be deployed manually. Set to ``true`` to disable continuous integration, such as webhooks into online repos such as GitHub. Defaults to ``false`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_manual_integration AppServiceSourceControlSlot#use_manual_integration}
        :param use_mercurial: The repository specified is Mercurial. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_mercurial AppServiceSourceControlSlot#use_mercurial}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cef5511315fe4fa5fd358848e36e91b8d4c50a353372685faf32ef36bbe7793)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppServiceSourceControlSlotConfig(
            slot_id=slot_id,
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
        '''Generates CDKTF code for importing a AppServiceSourceControlSlot resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppServiceSourceControlSlot to import.
        :param import_from_id: The id of the existing AppServiceSourceControlSlot that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppServiceSourceControlSlot to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2602909ff2c538783eeb54e8731d78ca8f04c3de48e33e871eb776cc03d924fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGithubActionConfiguration")
    def put_github_action_configuration(
        self,
        *,
        code_configuration: typing.Optional[typing.Union["AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        container_configuration: typing.Optional[typing.Union["AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        generate_workflow_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param code_configuration: code_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#code_configuration AppServiceSourceControlSlot#code_configuration}
        :param container_configuration: container_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#container_configuration AppServiceSourceControlSlot#container_configuration}
        :param generate_workflow_file: Should the service generate the GitHub Action Workflow file. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#generate_workflow_file AppServiceSourceControlSlot#generate_workflow_file}
        '''
        value = AppServiceSourceControlSlotGithubActionConfiguration(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#create AppServiceSourceControlSlot#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#delete AppServiceSourceControlSlot#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#read AppServiceSourceControlSlot#read}.
        '''
        value = AppServiceSourceControlSlotTimeouts(
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
    ) -> "AppServiceSourceControlSlotGithubActionConfigurationOutputReference":
        return typing.cast("AppServiceSourceControlSlotGithubActionConfigurationOutputReference", jsii.get(self, "githubActionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="scmType")
    def scm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AppServiceSourceControlSlotTimeoutsOutputReference":
        return typing.cast("AppServiceSourceControlSlotTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="usesGithubAction")
    def uses_github_action(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "usesGithubAction"))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="githubActionConfigurationInput")
    def github_action_configuration_input(
        self,
    ) -> typing.Optional["AppServiceSourceControlSlotGithubActionConfiguration"]:
        return typing.cast(typing.Optional["AppServiceSourceControlSlotGithubActionConfiguration"], jsii.get(self, "githubActionConfigurationInput"))

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
    @jsii.member(jsii_name="slotIdInput")
    def slot_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slotIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppServiceSourceControlSlotTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppServiceSourceControlSlotTimeouts"]], jsii.get(self, "timeoutsInput"))

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
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e92f7736f22d7b1d7528fd0e516cb63c0e61aa7f526f8d229de4c8e9b64812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68565256ebfbe3bdaa10d419e50c423ccb39d3e50d8ce307619b5ea27dc49aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repoUrl")
    def repo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoUrl"))

    @repo_url.setter
    def repo_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e9832aa6cad1b1552a3eed43a9137b40531393bb8bd82497d3873eb7e06f00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfb66850c35a6492211b5e25337f8257850c306215a60b6961092ff2cc39dc01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rollbackEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slotId")
    def slot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slotId"))

    @slot_id.setter
    def slot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3c8c6aa115a36aa6775614c935794b9f3a3f779336f9b43feb83a41e0a4dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slotId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__843cce4abe2eb09322a368c153423e9f04cfc6dd679249059e88069395c4edd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64cc4ed7a0c0315e6db3bf2d8e08fcc29b9cecb56ec176b5f8cf36d344dbbbf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e042cbfb774cf27c96a25b5bcabb85489ee7738cc49a601012bf4de563a62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useMercurial", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "slot_id": "slotId",
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
class AppServiceSourceControlSlotConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        slot_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        github_action_configuration: typing.Optional[typing.Union["AppServiceSourceControlSlotGithubActionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        repo_url: typing.Optional[builtins.str] = None,
        rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AppServiceSourceControlSlotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param slot_id: The ID of the Linux or Windows Web App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#slot_id AppServiceSourceControlSlot#slot_id}
        :param branch: The URL for the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#branch AppServiceSourceControlSlot#branch}
        :param github_action_configuration: github_action_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#github_action_configuration AppServiceSourceControlSlot#github_action_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#id AppServiceSourceControlSlot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param repo_url: The branch name to use for deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#repo_url AppServiceSourceControlSlot#repo_url}
        :param rollback_enabled: Should the Deployment Rollback be enabled? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#rollback_enabled AppServiceSourceControlSlot#rollback_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#timeouts AppServiceSourceControlSlot#timeouts}
        :param use_local_git: Should the Slot use local Git configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_local_git AppServiceSourceControlSlot#use_local_git}
        :param use_manual_integration: Should code be deployed manually. Set to ``true`` to disable continuous integration, such as webhooks into online repos such as GitHub. Defaults to ``false`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_manual_integration AppServiceSourceControlSlot#use_manual_integration}
        :param use_mercurial: The repository specified is Mercurial. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_mercurial AppServiceSourceControlSlot#use_mercurial}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(github_action_configuration, dict):
            github_action_configuration = AppServiceSourceControlSlotGithubActionConfiguration(**github_action_configuration)
        if isinstance(timeouts, dict):
            timeouts = AppServiceSourceControlSlotTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e9be3127ce640b57cc0bcc7398b59bf70fdc87777a5d3a296450d560e9d1be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument slot_id", value=slot_id, expected_type=type_hints["slot_id"])
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
            "slot_id": slot_id,
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
    def slot_id(self) -> builtins.str:
        '''The ID of the Linux or Windows Web App Slot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#slot_id AppServiceSourceControlSlot#slot_id}
        '''
        result = self._values.get("slot_id")
        assert result is not None, "Required property 'slot_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''The URL for the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#branch AppServiceSourceControlSlot#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_action_configuration(
        self,
    ) -> typing.Optional["AppServiceSourceControlSlotGithubActionConfiguration"]:
        '''github_action_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#github_action_configuration AppServiceSourceControlSlot#github_action_configuration}
        '''
        result = self._values.get("github_action_configuration")
        return typing.cast(typing.Optional["AppServiceSourceControlSlotGithubActionConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#id AppServiceSourceControlSlot#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo_url(self) -> typing.Optional[builtins.str]:
        '''The branch name to use for deployments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#repo_url AppServiceSourceControlSlot#repo_url}
        '''
        result = self._values.get("repo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollback_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Deployment Rollback be enabled? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#rollback_enabled AppServiceSourceControlSlot#rollback_enabled}
        '''
        result = self._values.get("rollback_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppServiceSourceControlSlotTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#timeouts AppServiceSourceControlSlot#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppServiceSourceControlSlotTimeouts"], result)

    @builtins.property
    def use_local_git(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Slot use local Git configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_local_git AppServiceSourceControlSlot#use_local_git}
        '''
        result = self._values.get("use_local_git")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_manual_integration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should code be deployed manually.

        Set to ``true`` to disable continuous integration, such as webhooks into online repos such as GitHub. Defaults to ``false``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_manual_integration AppServiceSourceControlSlot#use_manual_integration}
        '''
        result = self._values.get("use_manual_integration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_mercurial(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The repository specified is Mercurial. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#use_mercurial AppServiceSourceControlSlot#use_mercurial}
        '''
        result = self._values.get("use_mercurial")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlSlotConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotGithubActionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "code_configuration": "codeConfiguration",
        "container_configuration": "containerConfiguration",
        "generate_workflow_file": "generateWorkflowFile",
    },
)
class AppServiceSourceControlSlotGithubActionConfiguration:
    def __init__(
        self,
        *,
        code_configuration: typing.Optional[typing.Union["AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        container_configuration: typing.Optional[typing.Union["AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        generate_workflow_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param code_configuration: code_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#code_configuration AppServiceSourceControlSlot#code_configuration}
        :param container_configuration: container_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#container_configuration AppServiceSourceControlSlot#container_configuration}
        :param generate_workflow_file: Should the service generate the GitHub Action Workflow file. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#generate_workflow_file AppServiceSourceControlSlot#generate_workflow_file}
        '''
        if isinstance(code_configuration, dict):
            code_configuration = AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration(**code_configuration)
        if isinstance(container_configuration, dict):
            container_configuration = AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration(**container_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e604ed8d524374288914bba1f1ba9f15666473dbf6bc15abb26bb58586c2ab)
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
    ) -> typing.Optional["AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration"]:
        '''code_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#code_configuration AppServiceSourceControlSlot#code_configuration}
        '''
        result = self._values.get("code_configuration")
        return typing.cast(typing.Optional["AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration"], result)

    @builtins.property
    def container_configuration(
        self,
    ) -> typing.Optional["AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration"]:
        '''container_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#container_configuration AppServiceSourceControlSlot#container_configuration}
        '''
        result = self._values.get("container_configuration")
        return typing.cast(typing.Optional["AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration"], result)

    @builtins.property
    def generate_workflow_file(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the service generate the GitHub Action Workflow file. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#generate_workflow_file AppServiceSourceControlSlot#generate_workflow_file}
        '''
        result = self._values.get("generate_workflow_file")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlSlotGithubActionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "runtime_stack": "runtimeStack",
        "runtime_version": "runtimeVersion",
    },
)
class AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration:
    def __init__(
        self,
        *,
        runtime_stack: builtins.str,
        runtime_version: builtins.str,
    ) -> None:
        '''
        :param runtime_stack: The value to use for the Runtime Stack in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#runtime_stack AppServiceSourceControlSlot#runtime_stack}
        :param runtime_version: The value to use for the Runtime Version in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#runtime_version AppServiceSourceControlSlot#runtime_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7281c81b989c13acce2343f51b7dcae77bb5ff11fd4fa7cd003a7aa7f9f5a1)
            check_type(argname="argument runtime_stack", value=runtime_stack, expected_type=type_hints["runtime_stack"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime_stack": runtime_stack,
            "runtime_version": runtime_version,
        }

    @builtins.property
    def runtime_stack(self) -> builtins.str:
        '''The value to use for the Runtime Stack in the workflow file content for code base apps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#runtime_stack AppServiceSourceControlSlot#runtime_stack}
        '''
        result = self._values.get("runtime_stack")
        assert result is not None, "Required property 'runtime_stack' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''The value to use for the Runtime Version in the workflow file content for code base apps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#runtime_version AppServiceSourceControlSlot#runtime_version}
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppServiceSourceControlSlotGithubActionConfigurationCodeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotGithubActionConfigurationCodeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1148549b3b48ab3b3885a4b932f2ac02587c993e687277108c62df2adc8d124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7fbdd74161f50924a903fb9876c1a2f0a02c2cbbfef816b8e3ce2a688d019dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeStack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ada36762ce923b6bde89b9e3ea635c4a25d44db89a6dd36a862453ca545454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d764d63b6fddb79d428a79f250bf496ac15714c2247ee86e14479efffb055048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "image_name": "imageName",
        "registry_url": "registryUrl",
        "registry_password": "registryPassword",
        "registry_username": "registryUsername",
    },
)
class AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        registry_url: builtins.str,
        registry_password: typing.Optional[builtins.str] = None,
        registry_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_name: The image name for the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#image_name AppServiceSourceControlSlot#image_name}
        :param registry_url: The server URL for the container registry where the build will be hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_url AppServiceSourceControlSlot#registry_url}
        :param registry_password: The password used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_password AppServiceSourceControlSlot#registry_password}
        :param registry_username: The username used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_username AppServiceSourceControlSlot#registry_username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dacd5053d7494172d8b25b31f35621690b26341af32c556308bf80648e5e15f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#image_name AppServiceSourceControlSlot#image_name}
        '''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_url(self) -> builtins.str:
        '''The server URL for the container registry where the build will be hosted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_url AppServiceSourceControlSlot#registry_url}
        '''
        result = self._values.get("registry_url")
        assert result is not None, "Required property 'registry_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_password(self) -> typing.Optional[builtins.str]:
        '''The password used to upload the image to the container registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_password AppServiceSourceControlSlot#registry_password}
        '''
        result = self._values.get("registry_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_username(self) -> typing.Optional[builtins.str]:
        '''The username used to upload the image to the container registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_username AppServiceSourceControlSlot#registry_username}
        '''
        result = self._values.get("registry_username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppServiceSourceControlSlotGithubActionConfigurationContainerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotGithubActionConfigurationContainerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__237e3fd5815f42f029601dc2939d159a96e8df446474f14b387b36d5417cd6de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db9f8e57ecddfca7ce0d837dc0f2420cb862c1bb122ff3a781957e48a1f20440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryPassword")
    def registry_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryPassword"))

    @registry_password.setter
    def registry_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7a89ca6d33d58eb23115766340452ad6af027126da74f35f078b6c295feeab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryUrl")
    def registry_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUrl"))

    @registry_url.setter
    def registry_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e74e88e3e8e2ebcd926ac8b05832a02019dcbc56526fe58c4b5b78cd88e631d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryUsername")
    def registry_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUsername"))

    @registry_username.setter
    def registry_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c372b171b716689172ab740c03e1184b46be48d5100f1a09ae81c69990b30d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925f543ece88a9410f923947e02abca702e5cc2b3d32babc912ec48bd1f75bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppServiceSourceControlSlotGithubActionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotGithubActionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7a9211307d2b8fa8b2515e1789152232a7409dc7709392f8ce7d6593d513c22)
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
        :param runtime_stack: The value to use for the Runtime Stack in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#runtime_stack AppServiceSourceControlSlot#runtime_stack}
        :param runtime_version: The value to use for the Runtime Version in the workflow file content for code base apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#runtime_version AppServiceSourceControlSlot#runtime_version}
        '''
        value = AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration(
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
        :param image_name: The image name for the build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#image_name AppServiceSourceControlSlot#image_name}
        :param registry_url: The server URL for the container registry where the build will be hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_url AppServiceSourceControlSlot#registry_url}
        :param registry_password: The password used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_password AppServiceSourceControlSlot#registry_password}
        :param registry_username: The username used to upload the image to the container registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#registry_username AppServiceSourceControlSlot#registry_username}
        '''
        value = AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration(
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
    ) -> AppServiceSourceControlSlotGithubActionConfigurationCodeConfigurationOutputReference:
        return typing.cast(AppServiceSourceControlSlotGithubActionConfigurationCodeConfigurationOutputReference, jsii.get(self, "codeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="containerConfiguration")
    def container_configuration(
        self,
    ) -> AppServiceSourceControlSlotGithubActionConfigurationContainerConfigurationOutputReference:
        return typing.cast(AppServiceSourceControlSlotGithubActionConfigurationContainerConfigurationOutputReference, jsii.get(self, "containerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="linuxAction")
    def linux_action(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "linuxAction"))

    @builtins.property
    @jsii.member(jsii_name="codeConfigurationInput")
    def code_configuration_input(
        self,
    ) -> typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration], jsii.get(self, "codeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="containerConfigurationInput")
    def container_configuration_input(
        self,
    ) -> typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration], jsii.get(self, "containerConfigurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__76d7f6009b611a8ea02e1f286e51d0d0a97b490fbfeede0a7c1df08915aeddfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateWorkflowFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppServiceSourceControlSlotGithubActionConfiguration]:
        return typing.cast(typing.Optional[AppServiceSourceControlSlotGithubActionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppServiceSourceControlSlotGithubActionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b5e176f0dbcccc269f9ff5a5e00aad0dc1ef5da398ee922fe2b26aed025ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class AppServiceSourceControlSlotTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#create AppServiceSourceControlSlot#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#delete AppServiceSourceControlSlot#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#read AppServiceSourceControlSlot#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcf0f6d493fab1e407e88af6de2e7d313ae74558b4ef2f33428a6990795a127)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#create AppServiceSourceControlSlot#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#delete AppServiceSourceControlSlot#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/app_service_source_control_slot#read AppServiceSourceControlSlot#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppServiceSourceControlSlotTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppServiceSourceControlSlotTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.appServiceSourceControlSlot.AppServiceSourceControlSlotTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c0848e36ee6a8adef9cae3f5fef458e56260c90dac79dc17b9939b846b7b6b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8181e7e52cd30a585c29060a80d4e98d83f31cb3313ba167ef838afe1cd5be79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d564ecc761573ff9c0196ff1158b165a62de98c1abaff5b35d74e3b616066d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367546e9dfc743536751513208a65c3d7c60b15d13a021df956915537bf8d31e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlSlotTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlSlotTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlSlotTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9de1e389bab653e05e88d01a3be6eeb7bdb3e97b5d18030893e82f383aa08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppServiceSourceControlSlot",
    "AppServiceSourceControlSlotConfig",
    "AppServiceSourceControlSlotGithubActionConfiguration",
    "AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration",
    "AppServiceSourceControlSlotGithubActionConfigurationCodeConfigurationOutputReference",
    "AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration",
    "AppServiceSourceControlSlotGithubActionConfigurationContainerConfigurationOutputReference",
    "AppServiceSourceControlSlotGithubActionConfigurationOutputReference",
    "AppServiceSourceControlSlotTimeouts",
    "AppServiceSourceControlSlotTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3cef5511315fe4fa5fd358848e36e91b8d4c50a353372685faf32ef36bbe7793(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    slot_id: builtins.str,
    branch: typing.Optional[builtins.str] = None,
    github_action_configuration: typing.Optional[typing.Union[AppServiceSourceControlSlotGithubActionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    repo_url: typing.Optional[builtins.str] = None,
    rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AppServiceSourceControlSlotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2602909ff2c538783eeb54e8731d78ca8f04c3de48e33e871eb776cc03d924fb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e92f7736f22d7b1d7528fd0e516cb63c0e61aa7f526f8d229de4c8e9b64812(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68565256ebfbe3bdaa10d419e50c423ccb39d3e50d8ce307619b5ea27dc49aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e9832aa6cad1b1552a3eed43a9137b40531393bb8bd82497d3873eb7e06f00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb66850c35a6492211b5e25337f8257850c306215a60b6961092ff2cc39dc01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3c8c6aa115a36aa6775614c935794b9f3a3f779336f9b43feb83a41e0a4dac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843cce4abe2eb09322a368c153423e9f04cfc6dd679249059e88069395c4edd6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cc4ed7a0c0315e6db3bf2d8e08fcc29b9cecb56ec176b5f8cf36d344dbbbf4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e042cbfb774cf27c96a25b5bcabb85489ee7738cc49a601012bf4de563a62f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e9be3127ce640b57cc0bcc7398b59bf70fdc87777a5d3a296450d560e9d1be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    slot_id: builtins.str,
    branch: typing.Optional[builtins.str] = None,
    github_action_configuration: typing.Optional[typing.Union[AppServiceSourceControlSlotGithubActionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    repo_url: typing.Optional[builtins.str] = None,
    rollback_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AppServiceSourceControlSlotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    use_local_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_manual_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_mercurial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e604ed8d524374288914bba1f1ba9f15666473dbf6bc15abb26bb58586c2ab(
    *,
    code_configuration: typing.Optional[typing.Union[AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    container_configuration: typing.Optional[typing.Union[AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    generate_workflow_file: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7281c81b989c13acce2343f51b7dcae77bb5ff11fd4fa7cd003a7aa7f9f5a1(
    *,
    runtime_stack: builtins.str,
    runtime_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1148549b3b48ab3b3885a4b932f2ac02587c993e687277108c62df2adc8d124(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fbdd74161f50924a903fb9876c1a2f0a02c2cbbfef816b8e3ce2a688d019dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ada36762ce923b6bde89b9e3ea635c4a25d44db89a6dd36a862453ca545454(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d764d63b6fddb79d428a79f250bf496ac15714c2247ee86e14479efffb055048(
    value: typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationCodeConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dacd5053d7494172d8b25b31f35621690b26341af32c556308bf80648e5e15f(
    *,
    image_name: builtins.str,
    registry_url: builtins.str,
    registry_password: typing.Optional[builtins.str] = None,
    registry_username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237e3fd5815f42f029601dc2939d159a96e8df446474f14b387b36d5417cd6de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9f8e57ecddfca7ce0d837dc0f2420cb862c1bb122ff3a781957e48a1f20440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7a89ca6d33d58eb23115766340452ad6af027126da74f35f078b6c295feeab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e74e88e3e8e2ebcd926ac8b05832a02019dcbc56526fe58c4b5b78cd88e631d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c372b171b716689172ab740c03e1184b46be48d5100f1a09ae81c69990b30d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925f543ece88a9410f923947e02abca702e5cc2b3d32babc912ec48bd1f75bc6(
    value: typing.Optional[AppServiceSourceControlSlotGithubActionConfigurationContainerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a9211307d2b8fa8b2515e1789152232a7409dc7709392f8ce7d6593d513c22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d7f6009b611a8ea02e1f286e51d0d0a97b490fbfeede0a7c1df08915aeddfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b5e176f0dbcccc269f9ff5a5e00aad0dc1ef5da398ee922fe2b26aed025ad9(
    value: typing.Optional[AppServiceSourceControlSlotGithubActionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcf0f6d493fab1e407e88af6de2e7d313ae74558b4ef2f33428a6990795a127(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0848e36ee6a8adef9cae3f5fef458e56260c90dac79dc17b9939b846b7b6b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8181e7e52cd30a585c29060a80d4e98d83f31cb3313ba167ef838afe1cd5be79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d564ecc761573ff9c0196ff1158b165a62de98c1abaff5b35d74e3b616066d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367546e9dfc743536751513208a65c3d7c60b15d13a021df956915537bf8d31e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9de1e389bab653e05e88d01a3be6eeb7bdb3e97b5d18030893e82f383aa08d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppServiceSourceControlSlotTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
