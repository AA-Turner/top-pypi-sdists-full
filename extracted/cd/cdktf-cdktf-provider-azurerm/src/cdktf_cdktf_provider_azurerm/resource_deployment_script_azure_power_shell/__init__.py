r'''
# `azurerm_resource_deployment_script_azure_power_shell`

Refer to the Terraform Registry for docs: [`azurerm_resource_deployment_script_azure_power_shell`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell).
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


class ResourceDeploymentScriptAzurePowerShell(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShell",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell azurerm_resource_deployment_script_azure_power_shell}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        retention_interval: builtins.str,
        version: builtins.str,
        cleanup_preference: typing.Optional[builtins.str] = None,
        command_line: typing.Optional[builtins.str] = None,
        container: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ResourceDeploymentScriptAzurePowerShellEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_update_tag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        primary_script_uri: typing.Optional[builtins.str] = None,
        script_content: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellStorageAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell azurerm_resource_deployment_script_azure_power_shell} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#location ResourceDeploymentScriptAzurePowerShell#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#resource_group_name ResourceDeploymentScriptAzurePowerShell#resource_group_name}.
        :param retention_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#retention_interval ResourceDeploymentScriptAzurePowerShell#retention_interval}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#version ResourceDeploymentScriptAzurePowerShell#version}.
        :param cleanup_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#cleanup_preference ResourceDeploymentScriptAzurePowerShell#cleanup_preference}.
        :param command_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#command_line ResourceDeploymentScriptAzurePowerShell#command_line}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#container ResourceDeploymentScriptAzurePowerShell#container}
        :param environment_variable: environment_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#environment_variable ResourceDeploymentScriptAzurePowerShell#environment_variable}
        :param force_update_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#force_update_tag ResourceDeploymentScriptAzurePowerShell#force_update_tag}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#id ResourceDeploymentScriptAzurePowerShell#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#identity ResourceDeploymentScriptAzurePowerShell#identity}
        :param primary_script_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#primary_script_uri ResourceDeploymentScriptAzurePowerShell#primary_script_uri}.
        :param script_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#script_content ResourceDeploymentScriptAzurePowerShell#script_content}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#storage_account ResourceDeploymentScriptAzurePowerShell#storage_account}
        :param supporting_script_uris: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#supporting_script_uris ResourceDeploymentScriptAzurePowerShell#supporting_script_uris}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#tags ResourceDeploymentScriptAzurePowerShell#tags}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#timeout ResourceDeploymentScriptAzurePowerShell#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#timeouts ResourceDeploymentScriptAzurePowerShell#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5ab67fcf81fbd885d51f806c9e8449fb3248bcead967271d7d8646250f91db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ResourceDeploymentScriptAzurePowerShellConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            retention_interval=retention_interval,
            version=version,
            cleanup_preference=cleanup_preference,
            command_line=command_line,
            container=container,
            environment_variable=environment_variable,
            force_update_tag=force_update_tag,
            id=id,
            identity=identity,
            primary_script_uri=primary_script_uri,
            script_content=script_content,
            storage_account=storage_account,
            supporting_script_uris=supporting_script_uris,
            tags=tags,
            timeout=timeout,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a ResourceDeploymentScriptAzurePowerShell resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ResourceDeploymentScriptAzurePowerShell to import.
        :param import_from_id: The id of the existing ResourceDeploymentScriptAzurePowerShell that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ResourceDeploymentScriptAzurePowerShell to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d908dd1dceca5de46094eefb4429b20d9953a18a30d61583d28110c8351f15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContainer")
    def put_container(
        self,
        *,
        container_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#container_group_name ResourceDeploymentScriptAzurePowerShell#container_group_name}.
        '''
        value = ResourceDeploymentScriptAzurePowerShellContainer(
            container_group_name=container_group_name
        )

        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putEnvironmentVariable")
    def put_environment_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ResourceDeploymentScriptAzurePowerShellEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f762ac9f8c6c35382ee1f3fcae9f9b1f32acac31b313e4036cd269affd4855d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironmentVariable", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#identity_ids ResourceDeploymentScriptAzurePowerShell#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#type ResourceDeploymentScriptAzurePowerShell#type}.
        '''
        value = ResourceDeploymentScriptAzurePowerShellIdentity(
            identity_ids=identity_ids, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putStorageAccount")
    def put_storage_account(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#key ResourceDeploymentScriptAzurePowerShell#key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.
        '''
        value = ResourceDeploymentScriptAzurePowerShellStorageAccount(
            key=key, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStorageAccount", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#create ResourceDeploymentScriptAzurePowerShell#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#delete ResourceDeploymentScriptAzurePowerShell#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#read ResourceDeploymentScriptAzurePowerShell#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#update ResourceDeploymentScriptAzurePowerShell#update}.
        '''
        value = ResourceDeploymentScriptAzurePowerShellTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCleanupPreference")
    def reset_cleanup_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCleanupPreference", []))

    @jsii.member(jsii_name="resetCommandLine")
    def reset_command_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommandLine", []))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetEnvironmentVariable")
    def reset_environment_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariable", []))

    @jsii.member(jsii_name="resetForceUpdateTag")
    def reset_force_update_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdateTag", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetPrimaryScriptUri")
    def reset_primary_script_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryScriptUri", []))

    @jsii.member(jsii_name="resetScriptContent")
    def reset_script_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptContent", []))

    @jsii.member(jsii_name="resetStorageAccount")
    def reset_storage_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccount", []))

    @jsii.member(jsii_name="resetSupportingScriptUris")
    def reset_supporting_script_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportingScriptUris", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="container")
    def container(
        self,
    ) -> "ResourceDeploymentScriptAzurePowerShellContainerOutputReference":
        return typing.cast("ResourceDeploymentScriptAzurePowerShellContainerOutputReference", jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariable")
    def environment_variable(
        self,
    ) -> "ResourceDeploymentScriptAzurePowerShellEnvironmentVariableList":
        return typing.cast("ResourceDeploymentScriptAzurePowerShellEnvironmentVariableList", jsii.get(self, "environmentVariable"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(
        self,
    ) -> "ResourceDeploymentScriptAzurePowerShellIdentityOutputReference":
        return typing.cast("ResourceDeploymentScriptAzurePowerShellIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(
        self,
    ) -> "ResourceDeploymentScriptAzurePowerShellStorageAccountOutputReference":
        return typing.cast("ResourceDeploymentScriptAzurePowerShellStorageAccountOutputReference", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "ResourceDeploymentScriptAzurePowerShellTimeoutsOutputReference":
        return typing.cast("ResourceDeploymentScriptAzurePowerShellTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cleanupPreferenceInput")
    def cleanup_preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cleanupPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="commandLineInput")
    def command_line_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commandLineInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzurePowerShellContainer"]:
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzurePowerShellContainer"], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariableInput")
    def environment_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzurePowerShellEnvironmentVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzurePowerShellEnvironmentVariable"]]], jsii.get(self, "environmentVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateTagInput")
    def force_update_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forceUpdateTagInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzurePowerShellIdentity"]:
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzurePowerShellIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryScriptUriInput")
    def primary_script_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryScriptUriInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionIntervalInput")
    def retention_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptContentInput")
    def script_content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptContentInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzurePowerShellStorageAccount"]:
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzurePowerShellStorageAccount"], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="supportingScriptUrisInput")
    def supporting_script_uris_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "supportingScriptUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ResourceDeploymentScriptAzurePowerShellTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ResourceDeploymentScriptAzurePowerShellTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="cleanupPreference")
    def cleanup_preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cleanupPreference"))

    @cleanup_preference.setter
    def cleanup_preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455a42cbf669febbabc7667a75a37d13bc605982f8e44ae7cf3a577de265f0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cleanupPreference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commandLine")
    def command_line(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commandLine"))

    @command_line.setter
    def command_line(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0215a13c9f06515603758cbb03e82bdfde93da1d03a5927f75bd133fd0d59f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commandLine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdateTag")
    def force_update_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forceUpdateTag"))

    @force_update_tag.setter
    def force_update_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c61b1324cfed7d11b5408190eb344e861f5b8a4325da923db8904f3e6e0b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdateTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8914e0d1263633208c6aacdd4c5c8da12b984404e332f4495e4255336f3ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95458c6734b0e88758c94d95b526a8a443ac84d7ae53269b3ae27865382bfca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490dcf6c4343bb93b30132e9c1436c24f8e8c0441779eb212cdbdce4ac21b12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryScriptUri")
    def primary_script_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryScriptUri"))

    @primary_script_uri.setter
    def primary_script_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca007aa76d2c8da42b917c983158b2368465fe13ad30d7a82731c95a1494c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryScriptUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861156e486ec924f64f241182f286c8ffe6478cc36d9c142961fe9441f42dd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionInterval")
    def retention_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionInterval"))

    @retention_interval.setter
    def retention_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586a57dc98fa0c89e4dd37b1e76d36c4abd60a757515e4c6cf4e0b3b550e6cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptContent")
    def script_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptContent"))

    @script_content.setter
    def script_content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0430fead065b563824cd84b5d3af360d3203b12499f7db60078eef7de2f89b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportingScriptUris")
    def supporting_script_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportingScriptUris"))

    @supporting_script_uris.setter
    def supporting_script_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571b656ac06110e5a9db47c2e11f577c61cc1dfd25f09d747b286a0853fb6eb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportingScriptUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760a31d491f59d12fa6b224d1d222cffa60301794c2e051731897c8064d47743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aca7fd3b538bd27338c104e7414667571e90fc913cad927992289e5dbfe2e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9904a0a6cc6f23cd3dd46b46abf5593d8d50353c6c8528df57e3fed40317dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "retention_interval": "retentionInterval",
        "version": "version",
        "cleanup_preference": "cleanupPreference",
        "command_line": "commandLine",
        "container": "container",
        "environment_variable": "environmentVariable",
        "force_update_tag": "forceUpdateTag",
        "id": "id",
        "identity": "identity",
        "primary_script_uri": "primaryScriptUri",
        "script_content": "scriptContent",
        "storage_account": "storageAccount",
        "supporting_script_uris": "supportingScriptUris",
        "tags": "tags",
        "timeout": "timeout",
        "timeouts": "timeouts",
    },
)
class ResourceDeploymentScriptAzurePowerShellConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        retention_interval: builtins.str,
        version: builtins.str,
        cleanup_preference: typing.Optional[builtins.str] = None,
        command_line: typing.Optional[builtins.str] = None,
        container: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ResourceDeploymentScriptAzurePowerShellEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_update_tag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        primary_script_uri: typing.Optional[builtins.str] = None,
        script_content: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellStorageAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ResourceDeploymentScriptAzurePowerShellTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#location ResourceDeploymentScriptAzurePowerShell#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#resource_group_name ResourceDeploymentScriptAzurePowerShell#resource_group_name}.
        :param retention_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#retention_interval ResourceDeploymentScriptAzurePowerShell#retention_interval}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#version ResourceDeploymentScriptAzurePowerShell#version}.
        :param cleanup_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#cleanup_preference ResourceDeploymentScriptAzurePowerShell#cleanup_preference}.
        :param command_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#command_line ResourceDeploymentScriptAzurePowerShell#command_line}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#container ResourceDeploymentScriptAzurePowerShell#container}
        :param environment_variable: environment_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#environment_variable ResourceDeploymentScriptAzurePowerShell#environment_variable}
        :param force_update_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#force_update_tag ResourceDeploymentScriptAzurePowerShell#force_update_tag}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#id ResourceDeploymentScriptAzurePowerShell#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#identity ResourceDeploymentScriptAzurePowerShell#identity}
        :param primary_script_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#primary_script_uri ResourceDeploymentScriptAzurePowerShell#primary_script_uri}.
        :param script_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#script_content ResourceDeploymentScriptAzurePowerShell#script_content}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#storage_account ResourceDeploymentScriptAzurePowerShell#storage_account}
        :param supporting_script_uris: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#supporting_script_uris ResourceDeploymentScriptAzurePowerShell#supporting_script_uris}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#tags ResourceDeploymentScriptAzurePowerShell#tags}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#timeout ResourceDeploymentScriptAzurePowerShell#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#timeouts ResourceDeploymentScriptAzurePowerShell#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(container, dict):
            container = ResourceDeploymentScriptAzurePowerShellContainer(**container)
        if isinstance(identity, dict):
            identity = ResourceDeploymentScriptAzurePowerShellIdentity(**identity)
        if isinstance(storage_account, dict):
            storage_account = ResourceDeploymentScriptAzurePowerShellStorageAccount(**storage_account)
        if isinstance(timeouts, dict):
            timeouts = ResourceDeploymentScriptAzurePowerShellTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f5806ae2da54a29b401954c1f25712b49c6e415e5d87ecfdd46b62c129264e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument retention_interval", value=retention_interval, expected_type=type_hints["retention_interval"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument cleanup_preference", value=cleanup_preference, expected_type=type_hints["cleanup_preference"])
            check_type(argname="argument command_line", value=command_line, expected_type=type_hints["command_line"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument environment_variable", value=environment_variable, expected_type=type_hints["environment_variable"])
            check_type(argname="argument force_update_tag", value=force_update_tag, expected_type=type_hints["force_update_tag"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument primary_script_uri", value=primary_script_uri, expected_type=type_hints["primary_script_uri"])
            check_type(argname="argument script_content", value=script_content, expected_type=type_hints["script_content"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument supporting_script_uris", value=supporting_script_uris, expected_type=type_hints["supporting_script_uris"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "retention_interval": retention_interval,
            "version": version,
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
        if cleanup_preference is not None:
            self._values["cleanup_preference"] = cleanup_preference
        if command_line is not None:
            self._values["command_line"] = command_line
        if container is not None:
            self._values["container"] = container
        if environment_variable is not None:
            self._values["environment_variable"] = environment_variable
        if force_update_tag is not None:
            self._values["force_update_tag"] = force_update_tag
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if primary_script_uri is not None:
            self._values["primary_script_uri"] = primary_script_uri
        if script_content is not None:
            self._values["script_content"] = script_content
        if storage_account is not None:
            self._values["storage_account"] = storage_account
        if supporting_script_uris is not None:
            self._values["supporting_script_uris"] = supporting_script_uris
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#location ResourceDeploymentScriptAzurePowerShell#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#resource_group_name ResourceDeploymentScriptAzurePowerShell#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_interval(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#retention_interval ResourceDeploymentScriptAzurePowerShell#retention_interval}.'''
        result = self._values.get("retention_interval")
        assert result is not None, "Required property 'retention_interval' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#version ResourceDeploymentScriptAzurePowerShell#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cleanup_preference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#cleanup_preference ResourceDeploymentScriptAzurePowerShell#cleanup_preference}.'''
        result = self._values.get("cleanup_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def command_line(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#command_line ResourceDeploymentScriptAzurePowerShell#command_line}.'''
        result = self._values.get("command_line")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzurePowerShellContainer"]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#container ResourceDeploymentScriptAzurePowerShell#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzurePowerShellContainer"], result)

    @builtins.property
    def environment_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzurePowerShellEnvironmentVariable"]]]:
        '''environment_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#environment_variable ResourceDeploymentScriptAzurePowerShell#environment_variable}
        '''
        result = self._values.get("environment_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzurePowerShellEnvironmentVariable"]]], result)

    @builtins.property
    def force_update_tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#force_update_tag ResourceDeploymentScriptAzurePowerShell#force_update_tag}.'''
        result = self._values.get("force_update_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#id ResourceDeploymentScriptAzurePowerShell#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzurePowerShellIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#identity ResourceDeploymentScriptAzurePowerShell#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzurePowerShellIdentity"], result)

    @builtins.property
    def primary_script_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#primary_script_uri ResourceDeploymentScriptAzurePowerShell#primary_script_uri}.'''
        result = self._values.get("primary_script_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#script_content ResourceDeploymentScriptAzurePowerShell#script_content}.'''
        result = self._values.get("script_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzurePowerShellStorageAccount"]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#storage_account ResourceDeploymentScriptAzurePowerShell#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzurePowerShellStorageAccount"], result)

    @builtins.property
    def supporting_script_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#supporting_script_uris ResourceDeploymentScriptAzurePowerShell#supporting_script_uris}.'''
        result = self._values.get("supporting_script_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#tags ResourceDeploymentScriptAzurePowerShell#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#timeout ResourceDeploymentScriptAzurePowerShell#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzurePowerShellTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#timeouts ResourceDeploymentScriptAzurePowerShell#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzurePowerShellTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzurePowerShellConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellContainer",
    jsii_struct_bases=[],
    name_mapping={"container_group_name": "containerGroupName"},
)
class ResourceDeploymentScriptAzurePowerShellContainer:
    def __init__(
        self,
        *,
        container_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#container_group_name ResourceDeploymentScriptAzurePowerShell#container_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c511e8382366591f3d608b61f16d24ab255165290d301d86559a8e2f6f28ecc8)
            check_type(argname="argument container_group_name", value=container_group_name, expected_type=type_hints["container_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_group_name is not None:
            self._values["container_group_name"] = container_group_name

    @builtins.property
    def container_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#container_group_name ResourceDeploymentScriptAzurePowerShell#container_group_name}.'''
        result = self._values.get("container_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzurePowerShellContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzurePowerShellContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f191e9ca5bb3354c4f382656800ff4fc5ad723a4864af301adea37dc88b58bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerGroupName")
    def reset_container_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerGroupName", []))

    @builtins.property
    @jsii.member(jsii_name="containerGroupNameInput")
    def container_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerGroupName")
    def container_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerGroupName"))

    @container_group_name.setter
    def container_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4ccee8191234e7af512beed9b69abd0d8bcf83d39a485859fef883b7bc39d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ResourceDeploymentScriptAzurePowerShellContainer]:
        return typing.cast(typing.Optional[ResourceDeploymentScriptAzurePowerShellContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ResourceDeploymentScriptAzurePowerShellContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fbf822c7fbcf9b98d99f0993ab1ca135587e98926f0b069c684770472779ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "secure_value": "secureValue", "value": "value"},
)
class ResourceDeploymentScriptAzurePowerShellEnvironmentVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        secure_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.
        :param secure_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#secure_value ResourceDeploymentScriptAzurePowerShell#secure_value}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#value ResourceDeploymentScriptAzurePowerShell#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198ce98dca0783679c72d0da65c71bb45946fb12c31e9d0837bd977bb573614f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secure_value", value=secure_value, expected_type=type_hints["secure_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if secure_value is not None:
            self._values["secure_value"] = secure_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secure_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#secure_value ResourceDeploymentScriptAzurePowerShell#secure_value}.'''
        result = self._values.get("secure_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#value ResourceDeploymentScriptAzurePowerShell#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzurePowerShellEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzurePowerShellEnvironmentVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellEnvironmentVariableList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd78e6ea3189b6c46768eec0b6d08a1c1ebaf62b1d6f8fb7a9fc75fa07c6a9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ResourceDeploymentScriptAzurePowerShellEnvironmentVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7d261db76f775c502575fb506c3c23ab2e53e21916975df2703a6407a52a51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ResourceDeploymentScriptAzurePowerShellEnvironmentVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622ca9474c578d562dd6522f0699138498b9ebfb57007cdf0149544d8749257d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c598b15db80beed910fb5680fcf73d4cdfa9164ecd7bb1f6b644906cae338d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931d72becb293725ade9126729e46fb85ac4363255318532530b5e17ba899958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e5bd3d08badf10d3a2df7f2fa838737110927a88d43f74fa9f21256d1fffa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ResourceDeploymentScriptAzurePowerShellEnvironmentVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellEnvironmentVariableOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9031f153e70d276340e560e6eb08f6228e704e28f778a63275074bea3ecf7998)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecureValue")
    def reset_secure_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secureValueInput")
    def secure_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secureValueInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2ce88576485be29f838cb77ba3cd42f3c535036f728b30e7447ca42c51df14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secureValue")
    def secure_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secureValue"))

    @secure_value.setter
    def secure_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8602734d45f8bf1372d57bef699326f199c45ffc5e838c3cf766acdcff2d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72ba54f03b6bc2727476b858599c7bdc1777c246902b570701fadc3f0bdd478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d241712ed119d8cb0a7b66bc27662848c32d94b86d01ea228cb43f978ddccbe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class ResourceDeploymentScriptAzurePowerShellIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#identity_ids ResourceDeploymentScriptAzurePowerShell#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#type ResourceDeploymentScriptAzurePowerShell#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26977df9b5304119234a680bab3a0f66c108498cf13801b4dd26e3b4931ebca)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#identity_ids ResourceDeploymentScriptAzurePowerShell#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#type ResourceDeploymentScriptAzurePowerShell#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzurePowerShellIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzurePowerShellIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f7a3ab65e472966ad27ccadf1369dd011ff907f3784df64982716c20d98399d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce470f072b09da5fb0f2ec2c598b5b167ced8f8d6a616c5cc0a217139cda5854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a895d497627b280b0292778f6c6d46ba4725728708a04ef88d7b67d097e55d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ResourceDeploymentScriptAzurePowerShellIdentity]:
        return typing.cast(typing.Optional[ResourceDeploymentScriptAzurePowerShellIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ResourceDeploymentScriptAzurePowerShellIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7501950a1753982990114bce18c01b988b282342a85e9d7b5999312c0a23f53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellStorageAccount",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name"},
)
class ResourceDeploymentScriptAzurePowerShellStorageAccount:
    def __init__(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#key ResourceDeploymentScriptAzurePowerShell#key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__893be2506775de7424093ab4218dac9daba8de2943a216ce3cbdddc8541d1aff)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "name": name,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#key ResourceDeploymentScriptAzurePowerShell#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#name ResourceDeploymentScriptAzurePowerShell#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzurePowerShellStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzurePowerShellStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellStorageAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0be1db9d6d7d77287044c90522855f69a13983c26f0982e0b4c244bce7ee07c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895320c859d1251e64e717ce3ba4e7cf5636144d65cd10a6eb62b63061a9031c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc9d940f00aaa4945c723e2f09b02957dcd00a4f998674e23068150efbb3d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ResourceDeploymentScriptAzurePowerShellStorageAccount]:
        return typing.cast(typing.Optional[ResourceDeploymentScriptAzurePowerShellStorageAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ResourceDeploymentScriptAzurePowerShellStorageAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb596e053134392dfb70634cc74ace06d140a3a46ddffd72f82a597b4f3380f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ResourceDeploymentScriptAzurePowerShellTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#create ResourceDeploymentScriptAzurePowerShell#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#delete ResourceDeploymentScriptAzurePowerShell#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#read ResourceDeploymentScriptAzurePowerShell#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#update ResourceDeploymentScriptAzurePowerShell#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06764422a17fbaf1c6f9b1ea94c8513f87b3603d047accbc526f085dc37d5d90)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#create ResourceDeploymentScriptAzurePowerShell#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#delete ResourceDeploymentScriptAzurePowerShell#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#read ResourceDeploymentScriptAzurePowerShell#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_power_shell#update ResourceDeploymentScriptAzurePowerShell#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzurePowerShellTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzurePowerShellTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzurePowerShell.ResourceDeploymentScriptAzurePowerShellTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfb65a158f4530bd65a2255c25590e0dc2fedf078d1657ba8a14190628852d43)
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

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

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
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32476cde9fa40dd992f48feba007766721855f6ff1fbfa77307e0895fb6b578b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b133f80c4bae9727c59faebc64080b38bce33c80dd65dc93ed98631a1106597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a62bdcda45872e630b5a68c44590511b9781d123ac7cb42d294f7ee92e73e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2403893b5ecb13e6776695ae0698f58bcffc4094471683cf41bd827414c6a7fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ab199076436e4227b69c7fb3d8ead61960d1259dd51a52e61c17ded76eab84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ResourceDeploymentScriptAzurePowerShell",
    "ResourceDeploymentScriptAzurePowerShellConfig",
    "ResourceDeploymentScriptAzurePowerShellContainer",
    "ResourceDeploymentScriptAzurePowerShellContainerOutputReference",
    "ResourceDeploymentScriptAzurePowerShellEnvironmentVariable",
    "ResourceDeploymentScriptAzurePowerShellEnvironmentVariableList",
    "ResourceDeploymentScriptAzurePowerShellEnvironmentVariableOutputReference",
    "ResourceDeploymentScriptAzurePowerShellIdentity",
    "ResourceDeploymentScriptAzurePowerShellIdentityOutputReference",
    "ResourceDeploymentScriptAzurePowerShellStorageAccount",
    "ResourceDeploymentScriptAzurePowerShellStorageAccountOutputReference",
    "ResourceDeploymentScriptAzurePowerShellTimeouts",
    "ResourceDeploymentScriptAzurePowerShellTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6d5ab67fcf81fbd885d51f806c9e8449fb3248bcead967271d7d8646250f91db(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    retention_interval: builtins.str,
    version: builtins.str,
    cleanup_preference: typing.Optional[builtins.str] = None,
    command_line: typing.Optional[builtins.str] = None,
    container: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ResourceDeploymentScriptAzurePowerShellEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_update_tag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    primary_script_uri: typing.Optional[builtins.str] = None,
    script_content: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellStorageAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__74d908dd1dceca5de46094eefb4429b20d9953a18a30d61583d28110c8351f15(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f762ac9f8c6c35382ee1f3fcae9f9b1f32acac31b313e4036cd269affd4855d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ResourceDeploymentScriptAzurePowerShellEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455a42cbf669febbabc7667a75a37d13bc605982f8e44ae7cf3a577de265f0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0215a13c9f06515603758cbb03e82bdfde93da1d03a5927f75bd133fd0d59f09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c61b1324cfed7d11b5408190eb344e861f5b8a4325da923db8904f3e6e0b8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8914e0d1263633208c6aacdd4c5c8da12b984404e332f4495e4255336f3ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95458c6734b0e88758c94d95b526a8a443ac84d7ae53269b3ae27865382bfca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490dcf6c4343bb93b30132e9c1436c24f8e8c0441779eb212cdbdce4ac21b12a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca007aa76d2c8da42b917c983158b2368465fe13ad30d7a82731c95a1494c1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861156e486ec924f64f241182f286c8ffe6478cc36d9c142961fe9441f42dd70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586a57dc98fa0c89e4dd37b1e76d36c4abd60a757515e4c6cf4e0b3b550e6cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0430fead065b563824cd84b5d3af360d3203b12499f7db60078eef7de2f89b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571b656ac06110e5a9db47c2e11f577c61cc1dfd25f09d747b286a0853fb6eb1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760a31d491f59d12fa6b224d1d222cffa60301794c2e051731897c8064d47743(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aca7fd3b538bd27338c104e7414667571e90fc913cad927992289e5dbfe2e5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9904a0a6cc6f23cd3dd46b46abf5593d8d50353c6c8528df57e3fed40317dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f5806ae2da54a29b401954c1f25712b49c6e415e5d87ecfdd46b62c129264e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    retention_interval: builtins.str,
    version: builtins.str,
    cleanup_preference: typing.Optional[builtins.str] = None,
    command_line: typing.Optional[builtins.str] = None,
    container: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ResourceDeploymentScriptAzurePowerShellEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_update_tag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    primary_script_uri: typing.Optional[builtins.str] = None,
    script_content: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellStorageAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ResourceDeploymentScriptAzurePowerShellTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c511e8382366591f3d608b61f16d24ab255165290d301d86559a8e2f6f28ecc8(
    *,
    container_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f191e9ca5bb3354c4f382656800ff4fc5ad723a4864af301adea37dc88b58bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4ccee8191234e7af512beed9b69abd0d8bcf83d39a485859fef883b7bc39d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbf822c7fbcf9b98d99f0993ab1ca135587e98926f0b069c684770472779ad9(
    value: typing.Optional[ResourceDeploymentScriptAzurePowerShellContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198ce98dca0783679c72d0da65c71bb45946fb12c31e9d0837bd977bb573614f(
    *,
    name: builtins.str,
    secure_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd78e6ea3189b6c46768eec0b6d08a1c1ebaf62b1d6f8fb7a9fc75fa07c6a9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7d261db76f775c502575fb506c3c23ab2e53e21916975df2703a6407a52a51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622ca9474c578d562dd6522f0699138498b9ebfb57007cdf0149544d8749257d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c598b15db80beed910fb5680fcf73d4cdfa9164ecd7bb1f6b644906cae338d16(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931d72becb293725ade9126729e46fb85ac4363255318532530b5e17ba899958(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e5bd3d08badf10d3a2df7f2fa838737110927a88d43f74fa9f21256d1fffa6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9031f153e70d276340e560e6eb08f6228e704e28f778a63275074bea3ecf7998(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2ce88576485be29f838cb77ba3cd42f3c535036f728b30e7447ca42c51df14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8602734d45f8bf1372d57bef699326f199c45ffc5e838c3cf766acdcff2d57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72ba54f03b6bc2727476b858599c7bdc1777c246902b570701fadc3f0bdd478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d241712ed119d8cb0a7b66bc27662848c32d94b86d01ea228cb43f978ddccbe4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellEnvironmentVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26977df9b5304119234a680bab3a0f66c108498cf13801b4dd26e3b4931ebca(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7a3ab65e472966ad27ccadf1369dd011ff907f3784df64982716c20d98399d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce470f072b09da5fb0f2ec2c598b5b167ced8f8d6a616c5cc0a217139cda5854(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a895d497627b280b0292778f6c6d46ba4725728708a04ef88d7b67d097e55d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7501950a1753982990114bce18c01b988b282342a85e9d7b5999312c0a23f53e(
    value: typing.Optional[ResourceDeploymentScriptAzurePowerShellIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893be2506775de7424093ab4218dac9daba8de2943a216ce3cbdddc8541d1aff(
    *,
    key: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0be1db9d6d7d77287044c90522855f69a13983c26f0982e0b4c244bce7ee07c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895320c859d1251e64e717ce3ba4e7cf5636144d65cd10a6eb62b63061a9031c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc9d940f00aaa4945c723e2f09b02957dcd00a4f998674e23068150efbb3d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb596e053134392dfb70634cc74ace06d140a3a46ddffd72f82a597b4f3380f8(
    value: typing.Optional[ResourceDeploymentScriptAzurePowerShellStorageAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06764422a17fbaf1c6f9b1ea94c8513f87b3603d047accbc526f085dc37d5d90(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb65a158f4530bd65a2255c25590e0dc2fedf078d1657ba8a14190628852d43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32476cde9fa40dd992f48feba007766721855f6ff1fbfa77307e0895fb6b578b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b133f80c4bae9727c59faebc64080b38bce33c80dd65dc93ed98631a1106597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a62bdcda45872e630b5a68c44590511b9781d123ac7cb42d294f7ee92e73e26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2403893b5ecb13e6776695ae0698f58bcffc4094471683cf41bd827414c6a7fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ab199076436e4227b69c7fb3d8ead61960d1259dd51a52e61c17ded76eab84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzurePowerShellTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
