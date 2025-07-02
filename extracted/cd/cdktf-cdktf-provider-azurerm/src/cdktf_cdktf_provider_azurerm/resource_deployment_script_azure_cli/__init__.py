r'''
# `azurerm_resource_deployment_script_azure_cli`

Refer to the Terraform Registry for docs: [`azurerm_resource_deployment_script_azure_cli`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli).
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


class ResourceDeploymentScriptAzureCli(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCli",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli azurerm_resource_deployment_script_azure_cli}.'''

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
        container: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ResourceDeploymentScriptAzureCliEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_update_tag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        primary_script_uri: typing.Optional[builtins.str] = None,
        script_content: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliStorageAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli azurerm_resource_deployment_script_azure_cli} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#location ResourceDeploymentScriptAzureCli#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#resource_group_name ResourceDeploymentScriptAzureCli#resource_group_name}.
        :param retention_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#retention_interval ResourceDeploymentScriptAzureCli#retention_interval}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#version ResourceDeploymentScriptAzureCli#version}.
        :param cleanup_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#cleanup_preference ResourceDeploymentScriptAzureCli#cleanup_preference}.
        :param command_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#command_line ResourceDeploymentScriptAzureCli#command_line}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#container ResourceDeploymentScriptAzureCli#container}
        :param environment_variable: environment_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#environment_variable ResourceDeploymentScriptAzureCli#environment_variable}
        :param force_update_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#force_update_tag ResourceDeploymentScriptAzureCli#force_update_tag}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#id ResourceDeploymentScriptAzureCli#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#identity ResourceDeploymentScriptAzureCli#identity}
        :param primary_script_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#primary_script_uri ResourceDeploymentScriptAzureCli#primary_script_uri}.
        :param script_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#script_content ResourceDeploymentScriptAzureCli#script_content}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#storage_account ResourceDeploymentScriptAzureCli#storage_account}
        :param supporting_script_uris: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#supporting_script_uris ResourceDeploymentScriptAzureCli#supporting_script_uris}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#tags ResourceDeploymentScriptAzureCli#tags}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#timeout ResourceDeploymentScriptAzureCli#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#timeouts ResourceDeploymentScriptAzureCli#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d8d985b012cce2537025301b89f86a3d969cf089480a09354313f26306f3c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ResourceDeploymentScriptAzureCliConfig(
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
        '''Generates CDKTF code for importing a ResourceDeploymentScriptAzureCli resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ResourceDeploymentScriptAzureCli to import.
        :param import_from_id: The id of the existing ResourceDeploymentScriptAzureCli that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ResourceDeploymentScriptAzureCli to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9badaf02fb31a95beb5629f5201cd756856ae78687290d3c08f81d47b57cb9a6)
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
        :param container_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#container_group_name ResourceDeploymentScriptAzureCli#container_group_name}.
        '''
        value = ResourceDeploymentScriptAzureCliContainer(
            container_group_name=container_group_name
        )

        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putEnvironmentVariable")
    def put_environment_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ResourceDeploymentScriptAzureCliEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e014155c43367e87c6c1bd4076c243a501e930033f7c2461a5ed9dc162883e7)
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
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#identity_ids ResourceDeploymentScriptAzureCli#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#type ResourceDeploymentScriptAzureCli#type}.
        '''
        value = ResourceDeploymentScriptAzureCliIdentity(
            identity_ids=identity_ids, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putStorageAccount")
    def put_storage_account(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#key ResourceDeploymentScriptAzureCli#key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.
        '''
        value = ResourceDeploymentScriptAzureCliStorageAccount(key=key, name=name)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#create ResourceDeploymentScriptAzureCli#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#delete ResourceDeploymentScriptAzureCli#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#read ResourceDeploymentScriptAzureCli#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#update ResourceDeploymentScriptAzureCli#update}.
        '''
        value = ResourceDeploymentScriptAzureCliTimeouts(
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
    def container(self) -> "ResourceDeploymentScriptAzureCliContainerOutputReference":
        return typing.cast("ResourceDeploymentScriptAzureCliContainerOutputReference", jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariable")
    def environment_variable(
        self,
    ) -> "ResourceDeploymentScriptAzureCliEnvironmentVariableList":
        return typing.cast("ResourceDeploymentScriptAzureCliEnvironmentVariableList", jsii.get(self, "environmentVariable"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ResourceDeploymentScriptAzureCliIdentityOutputReference":
        return typing.cast("ResourceDeploymentScriptAzureCliIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(
        self,
    ) -> "ResourceDeploymentScriptAzureCliStorageAccountOutputReference":
        return typing.cast("ResourceDeploymentScriptAzureCliStorageAccountOutputReference", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ResourceDeploymentScriptAzureCliTimeoutsOutputReference":
        return typing.cast("ResourceDeploymentScriptAzureCliTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ResourceDeploymentScriptAzureCliContainer"]:
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzureCliContainer"], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariableInput")
    def environment_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzureCliEnvironmentVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzureCliEnvironmentVariable"]]], jsii.get(self, "environmentVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateTagInput")
    def force_update_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forceUpdateTagInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzureCliIdentity"]:
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzureCliIdentity"], jsii.get(self, "identityInput"))

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
    ) -> typing.Optional["ResourceDeploymentScriptAzureCliStorageAccount"]:
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzureCliStorageAccount"], jsii.get(self, "storageAccountInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ResourceDeploymentScriptAzureCliTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ResourceDeploymentScriptAzureCliTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9392077587d8b4e2210c84931181321440e17e130d51662b1e64ae7f4c9b8b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cleanupPreference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commandLine")
    def command_line(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commandLine"))

    @command_line.setter
    def command_line(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec20c7b6095f66a215e15eede5d43098235763796056b510a1660080c6a989a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commandLine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdateTag")
    def force_update_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forceUpdateTag"))

    @force_update_tag.setter
    def force_update_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03471ea1d34311e4724a8bf4190d45a5dff5db5aa77612bf8cfb496a262c3b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdateTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc370d25d313cef6dd451c00f50c0c6a0ff870c3ca60202acc9c396516452bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af8701fa88270c4d1095e225374991cac067e3a4c59b5fdc33a4e878fc58754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e086c3dfc1ca58ea43e489c75728481d87fc7ff57c29fdbe1b248c848abb4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryScriptUri")
    def primary_script_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryScriptUri"))

    @primary_script_uri.setter
    def primary_script_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39f1204ad3526527c2e99242ac8ace1c49415534398f817c31dabacf80a5b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryScriptUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1748a7c181382c8cf6bf0c6d7add57602ba83e9b90e0560b425fc4e212984db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionInterval")
    def retention_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionInterval"))

    @retention_interval.setter
    def retention_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3934a7d7afd8006f4bd4f2a5ced9e85628fc95f7151d4de79e957b26495837d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptContent")
    def script_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptContent"))

    @script_content.setter
    def script_content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6641a108e17023010a833ac7f6e8d917a9fc46afdf39977f125b9c7c78fe8a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportingScriptUris")
    def supporting_script_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportingScriptUris"))

    @supporting_script_uris.setter
    def supporting_script_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b00796e8d2566944601e56e6a7d1cb1ea394163508335032533bfd82ab35aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportingScriptUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e19c8c52701d56649cf73b43cc9fec28150f920f3144a2d5b21acf227ec26b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d755c4c092fbfb25e862ad3e4f4252b15e461c2bcd8c85ee8105aa4e2bdea74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f637904f8a242fa8bc483449941eb9b8032f486f26795320b527e9bd2a5ec9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliConfig",
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
class ResourceDeploymentScriptAzureCliConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ResourceDeploymentScriptAzureCliEnvironmentVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        force_update_tag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        primary_script_uri: typing.Optional[builtins.str] = None,
        script_content: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliStorageAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ResourceDeploymentScriptAzureCliTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#location ResourceDeploymentScriptAzureCli#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#resource_group_name ResourceDeploymentScriptAzureCli#resource_group_name}.
        :param retention_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#retention_interval ResourceDeploymentScriptAzureCli#retention_interval}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#version ResourceDeploymentScriptAzureCli#version}.
        :param cleanup_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#cleanup_preference ResourceDeploymentScriptAzureCli#cleanup_preference}.
        :param command_line: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#command_line ResourceDeploymentScriptAzureCli#command_line}.
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#container ResourceDeploymentScriptAzureCli#container}
        :param environment_variable: environment_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#environment_variable ResourceDeploymentScriptAzureCli#environment_variable}
        :param force_update_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#force_update_tag ResourceDeploymentScriptAzureCli#force_update_tag}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#id ResourceDeploymentScriptAzureCli#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#identity ResourceDeploymentScriptAzureCli#identity}
        :param primary_script_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#primary_script_uri ResourceDeploymentScriptAzureCli#primary_script_uri}.
        :param script_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#script_content ResourceDeploymentScriptAzureCli#script_content}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#storage_account ResourceDeploymentScriptAzureCli#storage_account}
        :param supporting_script_uris: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#supporting_script_uris ResourceDeploymentScriptAzureCli#supporting_script_uris}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#tags ResourceDeploymentScriptAzureCli#tags}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#timeout ResourceDeploymentScriptAzureCli#timeout}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#timeouts ResourceDeploymentScriptAzureCli#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(container, dict):
            container = ResourceDeploymentScriptAzureCliContainer(**container)
        if isinstance(identity, dict):
            identity = ResourceDeploymentScriptAzureCliIdentity(**identity)
        if isinstance(storage_account, dict):
            storage_account = ResourceDeploymentScriptAzureCliStorageAccount(**storage_account)
        if isinstance(timeouts, dict):
            timeouts = ResourceDeploymentScriptAzureCliTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50466b302bac309aebc1cb96073543d7f6899da750e38ea6728f1e0863198e21)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#location ResourceDeploymentScriptAzureCli#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#resource_group_name ResourceDeploymentScriptAzureCli#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_interval(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#retention_interval ResourceDeploymentScriptAzureCli#retention_interval}.'''
        result = self._values.get("retention_interval")
        assert result is not None, "Required property 'retention_interval' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#version ResourceDeploymentScriptAzureCli#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cleanup_preference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#cleanup_preference ResourceDeploymentScriptAzureCli#cleanup_preference}.'''
        result = self._values.get("cleanup_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def command_line(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#command_line ResourceDeploymentScriptAzureCli#command_line}.'''
        result = self._values.get("command_line")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container(self) -> typing.Optional["ResourceDeploymentScriptAzureCliContainer"]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#container ResourceDeploymentScriptAzureCli#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzureCliContainer"], result)

    @builtins.property
    def environment_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzureCliEnvironmentVariable"]]]:
        '''environment_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#environment_variable ResourceDeploymentScriptAzureCli#environment_variable}
        '''
        result = self._values.get("environment_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ResourceDeploymentScriptAzureCliEnvironmentVariable"]]], result)

    @builtins.property
    def force_update_tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#force_update_tag ResourceDeploymentScriptAzureCli#force_update_tag}.'''
        result = self._values.get("force_update_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#id ResourceDeploymentScriptAzureCli#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["ResourceDeploymentScriptAzureCliIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#identity ResourceDeploymentScriptAzureCli#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzureCliIdentity"], result)

    @builtins.property
    def primary_script_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#primary_script_uri ResourceDeploymentScriptAzureCli#primary_script_uri}.'''
        result = self._values.get("primary_script_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_content(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#script_content ResourceDeploymentScriptAzureCli#script_content}.'''
        result = self._values.get("script_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional["ResourceDeploymentScriptAzureCliStorageAccount"]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#storage_account ResourceDeploymentScriptAzureCli#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzureCliStorageAccount"], result)

    @builtins.property
    def supporting_script_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#supporting_script_uris ResourceDeploymentScriptAzureCli#supporting_script_uris}.'''
        result = self._values.get("supporting_script_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#tags ResourceDeploymentScriptAzureCli#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#timeout ResourceDeploymentScriptAzureCli#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ResourceDeploymentScriptAzureCliTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#timeouts ResourceDeploymentScriptAzureCli#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ResourceDeploymentScriptAzureCliTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzureCliConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliContainer",
    jsii_struct_bases=[],
    name_mapping={"container_group_name": "containerGroupName"},
)
class ResourceDeploymentScriptAzureCliContainer:
    def __init__(
        self,
        *,
        container_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#container_group_name ResourceDeploymentScriptAzureCli#container_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7a818352d83d190deb3f9dbb087e837d8150acd62f7661aca94f5bdc4bbb53)
            check_type(argname="argument container_group_name", value=container_group_name, expected_type=type_hints["container_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_group_name is not None:
            self._values["container_group_name"] = container_group_name

    @builtins.property
    def container_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#container_group_name ResourceDeploymentScriptAzureCli#container_group_name}.'''
        result = self._values.get("container_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzureCliContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzureCliContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86dc464c4000e3cbb8f01fb50419b3c56535336240a0d0c5c531b06eb73c530b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21359ee6d539a11582cc7bb615243ab49d243e5867e41d2c01bcd0e19a30f89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ResourceDeploymentScriptAzureCliContainer]:
        return typing.cast(typing.Optional[ResourceDeploymentScriptAzureCliContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ResourceDeploymentScriptAzureCliContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f80a44137c2b068c7c07ad3b3f304cd10a33ef8831db8f41cb3e3d7074d24d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "secure_value": "secureValue", "value": "value"},
)
class ResourceDeploymentScriptAzureCliEnvironmentVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        secure_value: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.
        :param secure_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#secure_value ResourceDeploymentScriptAzureCli#secure_value}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#value ResourceDeploymentScriptAzureCli#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33dff4d2b202a313c5acf3120f5bb5a588e91ad323030d3ab6ace93db084eef)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secure_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#secure_value ResourceDeploymentScriptAzureCli#secure_value}.'''
        result = self._values.get("secure_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#value ResourceDeploymentScriptAzureCli#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzureCliEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzureCliEnvironmentVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliEnvironmentVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50ee0c62fdbb9cb8112a97cbe6fe55bcf1472c23dcec172b542c0182edfedbb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ResourceDeploymentScriptAzureCliEnvironmentVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008d2d0b24f2941171e88f6c4bd4188dc61eba6f0073ba1f04d239d71d726c2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ResourceDeploymentScriptAzureCliEnvironmentVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9726c26f1ff0dc4bc882f20ac657097dbbd74861259fa1b73719dcdc2a4de47d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee440a68a0b25d48fc5bf78e96fd66c8bc7d7bf3507a2096bb6461dbfbe77fef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49b27ac66230767e0c1f8e4cea7f7398c3aecd05dab5bf0e887f1fb36190f59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzureCliEnvironmentVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzureCliEnvironmentVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzureCliEnvironmentVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420cf38e12624a83de261ac75acf16b5fcc113710ca9d58a6aee2b822584a399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ResourceDeploymentScriptAzureCliEnvironmentVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliEnvironmentVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0901a6b25d1716b61bbd97f81912878b0dda70b195c4a1c1ab4e0f0cde20d80c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3b9137768bfed23d4ae98617c3c1da3521f97a96cf10e4a8614179100a2a2b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secureValue")
    def secure_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secureValue"))

    @secure_value.setter
    def secure_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191b37d616523d12f665afee642d14fc885db91ccfd3e34f4f9aac8a155ed112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2fdf29c7d5dda94e6e06bc6b4264b5e71882809396084cba6d175ab72060e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliEnvironmentVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliEnvironmentVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliEnvironmentVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e731f250bb4457a315a0407b11098058733027b61d837c25f5e74bf54d086b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class ResourceDeploymentScriptAzureCliIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#identity_ids ResourceDeploymentScriptAzureCli#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#type ResourceDeploymentScriptAzureCli#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2591faa521d81c4114adb3efdfa3be27e8350251d7c599e32281f6a7824fc2f)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#identity_ids ResourceDeploymentScriptAzureCli#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#type ResourceDeploymentScriptAzureCli#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzureCliIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzureCliIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75c3f078fab972305632f616627116ddd246054c352888f0dc5f2324554365a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35fdfc7599e724147195ce7463f65ee54772504962099719966a68536b851d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd80feac15577debedec1c61e190753d0716ce8044471b80d2d2a734d223d809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ResourceDeploymentScriptAzureCliIdentity]:
        return typing.cast(typing.Optional[ResourceDeploymentScriptAzureCliIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ResourceDeploymentScriptAzureCliIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7451236380b8552898a1975b892ef290e97ff136a4d24879f9e654bb457fae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliStorageAccount",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name"},
)
class ResourceDeploymentScriptAzureCliStorageAccount:
    def __init__(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#key ResourceDeploymentScriptAzureCli#key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b8cc393c47e3401ffce65bfa9f5ca42a8a1dde09929463034d2751b22d956a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "name": name,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#key ResourceDeploymentScriptAzureCli#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#name ResourceDeploymentScriptAzureCli#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzureCliStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzureCliStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliStorageAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__101fcd611f1d59091f3949a182ec8db8089325890dabbcf5b6dd3a60bb787e20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0fef1370a70fd385fec9ca46672dfd54be47a895872b74684cb11e85821ef38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91f8ed689c97167ca558cc85a5a9a07341930f17b48edaa0ddc7b98e9d44648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ResourceDeploymentScriptAzureCliStorageAccount]:
        return typing.cast(typing.Optional[ResourceDeploymentScriptAzureCliStorageAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ResourceDeploymentScriptAzureCliStorageAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f4911292bc4db5e318a38f1f4095ecc68253ea8b432ca0b30548cd1e519846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ResourceDeploymentScriptAzureCliTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#create ResourceDeploymentScriptAzureCli#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#delete ResourceDeploymentScriptAzureCli#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#read ResourceDeploymentScriptAzureCli#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#update ResourceDeploymentScriptAzureCli#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee94a9e98a917a32653ee31d16a19bd38dd02dc1eb0ac9c1b9c45d3b02bf47bc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#create ResourceDeploymentScriptAzureCli#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#delete ResourceDeploymentScriptAzureCli#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#read ResourceDeploymentScriptAzureCli#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_deployment_script_azure_cli#update ResourceDeploymentScriptAzureCli#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceDeploymentScriptAzureCliTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceDeploymentScriptAzureCliTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceDeploymentScriptAzureCli.ResourceDeploymentScriptAzureCliTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc25c17cd7ccd92d33744b7eb63c4921d864dd227738b1930f89b4a5bf44052)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1489de532287c9848990fea21664c5c1aebb681a3659be7055ed373451f247d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91cbe8cdc2434f6d890b8d9e1098f49035a38db7853fd3762368462fb6f4d4da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1c254eef8f1fc479f58472b41d9b7173d709a83ea2f0224ca4dafd616f755a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258472fb61f9b781d2cc3cf6ea8b5a43571cfe8be49672fc98d73cb8b6b81143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026c9bf91acbb5e9853badd04ccb4c975907999edb6f8563d5960d803f0b4205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ResourceDeploymentScriptAzureCli",
    "ResourceDeploymentScriptAzureCliConfig",
    "ResourceDeploymentScriptAzureCliContainer",
    "ResourceDeploymentScriptAzureCliContainerOutputReference",
    "ResourceDeploymentScriptAzureCliEnvironmentVariable",
    "ResourceDeploymentScriptAzureCliEnvironmentVariableList",
    "ResourceDeploymentScriptAzureCliEnvironmentVariableOutputReference",
    "ResourceDeploymentScriptAzureCliIdentity",
    "ResourceDeploymentScriptAzureCliIdentityOutputReference",
    "ResourceDeploymentScriptAzureCliStorageAccount",
    "ResourceDeploymentScriptAzureCliStorageAccountOutputReference",
    "ResourceDeploymentScriptAzureCliTimeouts",
    "ResourceDeploymentScriptAzureCliTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d7d8d985b012cce2537025301b89f86a3d969cf089480a09354313f26306f3c6(
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
    container: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ResourceDeploymentScriptAzureCliEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_update_tag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    primary_script_uri: typing.Optional[builtins.str] = None,
    script_content: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliStorageAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9badaf02fb31a95beb5629f5201cd756856ae78687290d3c08f81d47b57cb9a6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e014155c43367e87c6c1bd4076c243a501e930033f7c2461a5ed9dc162883e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ResourceDeploymentScriptAzureCliEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9392077587d8b4e2210c84931181321440e17e130d51662b1e64ae7f4c9b8b9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec20c7b6095f66a215e15eede5d43098235763796056b510a1660080c6a989a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03471ea1d34311e4724a8bf4190d45a5dff5db5aa77612bf8cfb496a262c3b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc370d25d313cef6dd451c00f50c0c6a0ff870c3ca60202acc9c396516452bae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af8701fa88270c4d1095e225374991cac067e3a4c59b5fdc33a4e878fc58754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e086c3dfc1ca58ea43e489c75728481d87fc7ff57c29fdbe1b248c848abb4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39f1204ad3526527c2e99242ac8ace1c49415534398f817c31dabacf80a5b6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1748a7c181382c8cf6bf0c6d7add57602ba83e9b90e0560b425fc4e212984db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3934a7d7afd8006f4bd4f2a5ced9e85628fc95f7151d4de79e957b26495837d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6641a108e17023010a833ac7f6e8d917a9fc46afdf39977f125b9c7c78fe8a5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b00796e8d2566944601e56e6a7d1cb1ea394163508335032533bfd82ab35aa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e19c8c52701d56649cf73b43cc9fec28150f920f3144a2d5b21acf227ec26b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d755c4c092fbfb25e862ad3e4f4252b15e461c2bcd8c85ee8105aa4e2bdea74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f637904f8a242fa8bc483449941eb9b8032f486f26795320b527e9bd2a5ec9fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50466b302bac309aebc1cb96073543d7f6899da750e38ea6728f1e0863198e21(
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
    container: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ResourceDeploymentScriptAzureCliEnvironmentVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    force_update_tag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    primary_script_uri: typing.Optional[builtins.str] = None,
    script_content: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliStorageAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    supporting_script_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ResourceDeploymentScriptAzureCliTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7a818352d83d190deb3f9dbb087e837d8150acd62f7661aca94f5bdc4bbb53(
    *,
    container_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86dc464c4000e3cbb8f01fb50419b3c56535336240a0d0c5c531b06eb73c530b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21359ee6d539a11582cc7bb615243ab49d243e5867e41d2c01bcd0e19a30f89d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f80a44137c2b068c7c07ad3b3f304cd10a33ef8831db8f41cb3e3d7074d24d6(
    value: typing.Optional[ResourceDeploymentScriptAzureCliContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33dff4d2b202a313c5acf3120f5bb5a588e91ad323030d3ab6ace93db084eef(
    *,
    name: builtins.str,
    secure_value: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ee0c62fdbb9cb8112a97cbe6fe55bcf1472c23dcec172b542c0182edfedbb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008d2d0b24f2941171e88f6c4bd4188dc61eba6f0073ba1f04d239d71d726c2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9726c26f1ff0dc4bc882f20ac657097dbbd74861259fa1b73719dcdc2a4de47d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee440a68a0b25d48fc5bf78e96fd66c8bc7d7bf3507a2096bb6461dbfbe77fef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b27ac66230767e0c1f8e4cea7f7398c3aecd05dab5bf0e887f1fb36190f59d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420cf38e12624a83de261ac75acf16b5fcc113710ca9d58a6aee2b822584a399(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ResourceDeploymentScriptAzureCliEnvironmentVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0901a6b25d1716b61bbd97f81912878b0dda70b195c4a1c1ab4e0f0cde20d80c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b9137768bfed23d4ae98617c3c1da3521f97a96cf10e4a8614179100a2a2b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191b37d616523d12f665afee642d14fc885db91ccfd3e34f4f9aac8a155ed112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2fdf29c7d5dda94e6e06bc6b4264b5e71882809396084cba6d175ab72060e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e731f250bb4457a315a0407b11098058733027b61d837c25f5e74bf54d086b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliEnvironmentVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2591faa521d81c4114adb3efdfa3be27e8350251d7c599e32281f6a7824fc2f(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c3f078fab972305632f616627116ddd246054c352888f0dc5f2324554365a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fdfc7599e724147195ce7463f65ee54772504962099719966a68536b851d05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd80feac15577debedec1c61e190753d0716ce8044471b80d2d2a734d223d809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7451236380b8552898a1975b892ef290e97ff136a4d24879f9e654bb457fae7(
    value: typing.Optional[ResourceDeploymentScriptAzureCliIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b8cc393c47e3401ffce65bfa9f5ca42a8a1dde09929463034d2751b22d956a(
    *,
    key: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101fcd611f1d59091f3949a182ec8db8089325890dabbcf5b6dd3a60bb787e20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fef1370a70fd385fec9ca46672dfd54be47a895872b74684cb11e85821ef38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91f8ed689c97167ca558cc85a5a9a07341930f17b48edaa0ddc7b98e9d44648(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f4911292bc4db5e318a38f1f4095ecc68253ea8b432ca0b30548cd1e519846(
    value: typing.Optional[ResourceDeploymentScriptAzureCliStorageAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee94a9e98a917a32653ee31d16a19bd38dd02dc1eb0ac9c1b9c45d3b02bf47bc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc25c17cd7ccd92d33744b7eb63c4921d864dd227738b1930f89b4a5bf44052(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1489de532287c9848990fea21664c5c1aebb681a3659be7055ed373451f247d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cbe8cdc2434f6d890b8d9e1098f49035a38db7853fd3762368462fb6f4d4da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1c254eef8f1fc479f58472b41d9b7173d709a83ea2f0224ca4dafd616f755a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258472fb61f9b781d2cc3cf6ea8b5a43571cfe8be49672fc98d73cb8b6b81143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026c9bf91acbb5e9853badd04ccb4c975907999edb6f8563d5960d803f0b4205(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceDeploymentScriptAzureCliTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
