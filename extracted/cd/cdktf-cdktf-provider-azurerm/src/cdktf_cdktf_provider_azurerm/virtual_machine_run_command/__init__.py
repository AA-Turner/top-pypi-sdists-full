r'''
# `azurerm_virtual_machine_run_command`

Refer to the Terraform Registry for docs: [`azurerm_virtual_machine_run_command`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command).
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


class VirtualMachineRunCommand(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommand",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command azurerm_virtual_machine_run_command}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        source: typing.Union["VirtualMachineRunCommandSource", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_id: builtins.str,
        error_blob_managed_identity: typing.Optional[typing.Union["VirtualMachineRunCommandErrorBlobManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        error_blob_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        output_blob_managed_identity: typing.Optional[typing.Union["VirtualMachineRunCommandOutputBlobManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        output_blob_uri: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineRunCommandParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        protected_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineRunCommandProtectedParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        run_as_password: typing.Optional[builtins.str] = None,
        run_as_user: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualMachineRunCommandTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command azurerm_virtual_machine_run_command} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#location VirtualMachineRunCommand#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#name VirtualMachineRunCommand#name}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#source VirtualMachineRunCommand#source}
        :param virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#virtual_machine_id VirtualMachineRunCommand#virtual_machine_id}.
        :param error_blob_managed_identity: error_blob_managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#error_blob_managed_identity VirtualMachineRunCommand#error_blob_managed_identity}
        :param error_blob_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#error_blob_uri VirtualMachineRunCommand#error_blob_uri}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#id VirtualMachineRunCommand#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param output_blob_managed_identity: output_blob_managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#output_blob_managed_identity VirtualMachineRunCommand#output_blob_managed_identity}
        :param output_blob_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#output_blob_uri VirtualMachineRunCommand#output_blob_uri}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#parameter VirtualMachineRunCommand#parameter}
        :param protected_parameter: protected_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#protected_parameter VirtualMachineRunCommand#protected_parameter}
        :param run_as_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#run_as_password VirtualMachineRunCommand#run_as_password}.
        :param run_as_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#run_as_user VirtualMachineRunCommand#run_as_user}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#tags VirtualMachineRunCommand#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#timeouts VirtualMachineRunCommand#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a5fc5ebb4b0d2165d2ea6032fc5da4b439e27739c4212436c0386fa56c3fdf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualMachineRunCommandConfig(
            location=location,
            name=name,
            source=source,
            virtual_machine_id=virtual_machine_id,
            error_blob_managed_identity=error_blob_managed_identity,
            error_blob_uri=error_blob_uri,
            id=id,
            output_blob_managed_identity=output_blob_managed_identity,
            output_blob_uri=output_blob_uri,
            parameter=parameter,
            protected_parameter=protected_parameter,
            run_as_password=run_as_password,
            run_as_user=run_as_user,
            tags=tags,
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
        '''Generates CDKTF code for importing a VirtualMachineRunCommand resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VirtualMachineRunCommand to import.
        :param import_from_id: The id of the existing VirtualMachineRunCommand that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VirtualMachineRunCommand to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1979f46bb8790bed6c97be3b97458b7195463b84da027c6ce06981a1eb5cec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putErrorBlobManagedIdentity")
    def put_error_blob_managed_identity(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.
        '''
        value = VirtualMachineRunCommandErrorBlobManagedIdentity(
            client_id=client_id, object_id=object_id
        )

        return typing.cast(None, jsii.invoke(self, "putErrorBlobManagedIdentity", [value]))

    @jsii.member(jsii_name="putOutputBlobManagedIdentity")
    def put_output_blob_managed_identity(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.
        '''
        value = VirtualMachineRunCommandOutputBlobManagedIdentity(
            client_id=client_id, object_id=object_id
        )

        return typing.cast(None, jsii.invoke(self, "putOutputBlobManagedIdentity", [value]))

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineRunCommandParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d736d32853461d6305369267ad17b4c4911210c7f2ddd5651a0da511b22506ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="putProtectedParameter")
    def put_protected_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineRunCommandProtectedParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120d1e8bf01f36581105e8c0ed40a4cca103eca3abe0e71e413c5c9fa09619c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProtectedParameter", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        command_id: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
        script_uri: typing.Optional[builtins.str] = None,
        script_uri_managed_identity: typing.Optional[typing.Union["VirtualMachineRunCommandSourceScriptUriManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param command_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#command_id VirtualMachineRunCommand#command_id}.
        :param script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script VirtualMachineRunCommand#script}.
        :param script_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script_uri VirtualMachineRunCommand#script_uri}.
        :param script_uri_managed_identity: script_uri_managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script_uri_managed_identity VirtualMachineRunCommand#script_uri_managed_identity}
        '''
        value = VirtualMachineRunCommandSource(
            command_id=command_id,
            script=script,
            script_uri=script_uri,
            script_uri_managed_identity=script_uri_managed_identity,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#create VirtualMachineRunCommand#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#delete VirtualMachineRunCommand#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#read VirtualMachineRunCommand#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#update VirtualMachineRunCommand#update}.
        '''
        value = VirtualMachineRunCommandTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetErrorBlobManagedIdentity")
    def reset_error_blob_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorBlobManagedIdentity", []))

    @jsii.member(jsii_name="resetErrorBlobUri")
    def reset_error_blob_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorBlobUri", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOutputBlobManagedIdentity")
    def reset_output_blob_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputBlobManagedIdentity", []))

    @jsii.member(jsii_name="resetOutputBlobUri")
    def reset_output_blob_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputBlobUri", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetProtectedParameter")
    def reset_protected_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectedParameter", []))

    @jsii.member(jsii_name="resetRunAsPassword")
    def reset_run_as_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunAsPassword", []))

    @jsii.member(jsii_name="resetRunAsUser")
    def reset_run_as_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunAsUser", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="errorBlobManagedIdentity")
    def error_blob_managed_identity(
        self,
    ) -> "VirtualMachineRunCommandErrorBlobManagedIdentityOutputReference":
        return typing.cast("VirtualMachineRunCommandErrorBlobManagedIdentityOutputReference", jsii.get(self, "errorBlobManagedIdentity"))

    @builtins.property
    @jsii.member(jsii_name="instanceView")
    def instance_view(self) -> "VirtualMachineRunCommandInstanceViewList":
        return typing.cast("VirtualMachineRunCommandInstanceViewList", jsii.get(self, "instanceView"))

    @builtins.property
    @jsii.member(jsii_name="outputBlobManagedIdentity")
    def output_blob_managed_identity(
        self,
    ) -> "VirtualMachineRunCommandOutputBlobManagedIdentityOutputReference":
        return typing.cast("VirtualMachineRunCommandOutputBlobManagedIdentityOutputReference", jsii.get(self, "outputBlobManagedIdentity"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> "VirtualMachineRunCommandParameterList":
        return typing.cast("VirtualMachineRunCommandParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="protectedParameter")
    def protected_parameter(self) -> "VirtualMachineRunCommandProtectedParameterList":
        return typing.cast("VirtualMachineRunCommandProtectedParameterList", jsii.get(self, "protectedParameter"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "VirtualMachineRunCommandSourceOutputReference":
        return typing.cast("VirtualMachineRunCommandSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualMachineRunCommandTimeoutsOutputReference":
        return typing.cast("VirtualMachineRunCommandTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="errorBlobManagedIdentityInput")
    def error_blob_managed_identity_input(
        self,
    ) -> typing.Optional["VirtualMachineRunCommandErrorBlobManagedIdentity"]:
        return typing.cast(typing.Optional["VirtualMachineRunCommandErrorBlobManagedIdentity"], jsii.get(self, "errorBlobManagedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="errorBlobUriInput")
    def error_blob_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorBlobUriInput"))

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
    @jsii.member(jsii_name="outputBlobManagedIdentityInput")
    def output_blob_managed_identity_input(
        self,
    ) -> typing.Optional["VirtualMachineRunCommandOutputBlobManagedIdentity"]:
        return typing.cast(typing.Optional["VirtualMachineRunCommandOutputBlobManagedIdentity"], jsii.get(self, "outputBlobManagedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="outputBlobUriInput")
    def output_blob_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputBlobUriInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedParameterInput")
    def protected_parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandProtectedParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandProtectedParameter"]]], jsii.get(self, "protectedParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="runAsPasswordInput")
    def run_as_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runAsPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="runAsUserInput")
    def run_as_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runAsUserInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["VirtualMachineRunCommandSource"]:
        return typing.cast(typing.Optional["VirtualMachineRunCommandSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualMachineRunCommandTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualMachineRunCommandTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineIdInput")
    def virtual_machine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="errorBlobUri")
    def error_blob_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorBlobUri"))

    @error_blob_uri.setter
    def error_blob_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84f176c00808e2d13ce5ecc51839ea0ad540628cea4ea0b9c39364924be88b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorBlobUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7d0ae95fc7c3b1f92b0213bbc3ddc0666f29b3d21e84d6332c03998934e38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd0b31df5b552cd2c28922d780567fba0d6021ec027350e283984fd9a74d104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3f8c04dc0e9008daf84caafb828c913885912b84b7d0b954d3723ef75e8f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputBlobUri")
    def output_blob_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputBlobUri"))

    @output_blob_uri.setter
    def output_blob_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0febd02f04e760b57ee370023b381ec129a61e76adec7e7b1d2bc9db4344219a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputBlobUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runAsPassword")
    def run_as_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runAsPassword"))

    @run_as_password.setter
    def run_as_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82376833f2b24ac557938fa51d116593ec7920589d56e15dcc5455bfa1595ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runAsPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runAsUser")
    def run_as_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runAsUser"))

    @run_as_user.setter
    def run_as_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e534d6d628640cc7aeb73df14afb877eff94dca7bb56c84780b780a23bff83bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runAsUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce2da7c45246dba5ad71fdb0d7ef211331fd588601d19f8a0c2494f8cd783cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineId")
    def virtual_machine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineId"))

    @virtual_machine_id.setter
    def virtual_machine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e187c0d4d837d4b49b782706fb5209ffc74050a0373dde21ddda1b92799d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandConfig",
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
        "source": "source",
        "virtual_machine_id": "virtualMachineId",
        "error_blob_managed_identity": "errorBlobManagedIdentity",
        "error_blob_uri": "errorBlobUri",
        "id": "id",
        "output_blob_managed_identity": "outputBlobManagedIdentity",
        "output_blob_uri": "outputBlobUri",
        "parameter": "parameter",
        "protected_parameter": "protectedParameter",
        "run_as_password": "runAsPassword",
        "run_as_user": "runAsUser",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class VirtualMachineRunCommandConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        source: typing.Union["VirtualMachineRunCommandSource", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_id: builtins.str,
        error_blob_managed_identity: typing.Optional[typing.Union["VirtualMachineRunCommandErrorBlobManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        error_blob_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        output_blob_managed_identity: typing.Optional[typing.Union["VirtualMachineRunCommandOutputBlobManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        output_blob_uri: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineRunCommandParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        protected_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineRunCommandProtectedParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        run_as_password: typing.Optional[builtins.str] = None,
        run_as_user: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualMachineRunCommandTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#location VirtualMachineRunCommand#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#name VirtualMachineRunCommand#name}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#source VirtualMachineRunCommand#source}
        :param virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#virtual_machine_id VirtualMachineRunCommand#virtual_machine_id}.
        :param error_blob_managed_identity: error_blob_managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#error_blob_managed_identity VirtualMachineRunCommand#error_blob_managed_identity}
        :param error_blob_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#error_blob_uri VirtualMachineRunCommand#error_blob_uri}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#id VirtualMachineRunCommand#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param output_blob_managed_identity: output_blob_managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#output_blob_managed_identity VirtualMachineRunCommand#output_blob_managed_identity}
        :param output_blob_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#output_blob_uri VirtualMachineRunCommand#output_blob_uri}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#parameter VirtualMachineRunCommand#parameter}
        :param protected_parameter: protected_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#protected_parameter VirtualMachineRunCommand#protected_parameter}
        :param run_as_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#run_as_password VirtualMachineRunCommand#run_as_password}.
        :param run_as_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#run_as_user VirtualMachineRunCommand#run_as_user}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#tags VirtualMachineRunCommand#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#timeouts VirtualMachineRunCommand#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(source, dict):
            source = VirtualMachineRunCommandSource(**source)
        if isinstance(error_blob_managed_identity, dict):
            error_blob_managed_identity = VirtualMachineRunCommandErrorBlobManagedIdentity(**error_blob_managed_identity)
        if isinstance(output_blob_managed_identity, dict):
            output_blob_managed_identity = VirtualMachineRunCommandOutputBlobManagedIdentity(**output_blob_managed_identity)
        if isinstance(timeouts, dict):
            timeouts = VirtualMachineRunCommandTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6697e7b34e82df71e2406aaec164788a6ca00f5aeebc0b9c7911dd73be5c39)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument virtual_machine_id", value=virtual_machine_id, expected_type=type_hints["virtual_machine_id"])
            check_type(argname="argument error_blob_managed_identity", value=error_blob_managed_identity, expected_type=type_hints["error_blob_managed_identity"])
            check_type(argname="argument error_blob_uri", value=error_blob_uri, expected_type=type_hints["error_blob_uri"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument output_blob_managed_identity", value=output_blob_managed_identity, expected_type=type_hints["output_blob_managed_identity"])
            check_type(argname="argument output_blob_uri", value=output_blob_uri, expected_type=type_hints["output_blob_uri"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument protected_parameter", value=protected_parameter, expected_type=type_hints["protected_parameter"])
            check_type(argname="argument run_as_password", value=run_as_password, expected_type=type_hints["run_as_password"])
            check_type(argname="argument run_as_user", value=run_as_user, expected_type=type_hints["run_as_user"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "source": source,
            "virtual_machine_id": virtual_machine_id,
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
        if error_blob_managed_identity is not None:
            self._values["error_blob_managed_identity"] = error_blob_managed_identity
        if error_blob_uri is not None:
            self._values["error_blob_uri"] = error_blob_uri
        if id is not None:
            self._values["id"] = id
        if output_blob_managed_identity is not None:
            self._values["output_blob_managed_identity"] = output_blob_managed_identity
        if output_blob_uri is not None:
            self._values["output_blob_uri"] = output_blob_uri
        if parameter is not None:
            self._values["parameter"] = parameter
        if protected_parameter is not None:
            self._values["protected_parameter"] = protected_parameter
        if run_as_password is not None:
            self._values["run_as_password"] = run_as_password
        if run_as_user is not None:
            self._values["run_as_user"] = run_as_user
        if tags is not None:
            self._values["tags"] = tags
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#location VirtualMachineRunCommand#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#name VirtualMachineRunCommand#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "VirtualMachineRunCommandSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#source VirtualMachineRunCommand#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("VirtualMachineRunCommandSource", result)

    @builtins.property
    def virtual_machine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#virtual_machine_id VirtualMachineRunCommand#virtual_machine_id}.'''
        result = self._values.get("virtual_machine_id")
        assert result is not None, "Required property 'virtual_machine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_blob_managed_identity(
        self,
    ) -> typing.Optional["VirtualMachineRunCommandErrorBlobManagedIdentity"]:
        '''error_blob_managed_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#error_blob_managed_identity VirtualMachineRunCommand#error_blob_managed_identity}
        '''
        result = self._values.get("error_blob_managed_identity")
        return typing.cast(typing.Optional["VirtualMachineRunCommandErrorBlobManagedIdentity"], result)

    @builtins.property
    def error_blob_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#error_blob_uri VirtualMachineRunCommand#error_blob_uri}.'''
        result = self._values.get("error_blob_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#id VirtualMachineRunCommand#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_blob_managed_identity(
        self,
    ) -> typing.Optional["VirtualMachineRunCommandOutputBlobManagedIdentity"]:
        '''output_blob_managed_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#output_blob_managed_identity VirtualMachineRunCommand#output_blob_managed_identity}
        '''
        result = self._values.get("output_blob_managed_identity")
        return typing.cast(typing.Optional["VirtualMachineRunCommandOutputBlobManagedIdentity"], result)

    @builtins.property
    def output_blob_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#output_blob_uri VirtualMachineRunCommand#output_blob_uri}.'''
        result = self._values.get("output_blob_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#parameter VirtualMachineRunCommand#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandParameter"]]], result)

    @builtins.property
    def protected_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandProtectedParameter"]]]:
        '''protected_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#protected_parameter VirtualMachineRunCommand#protected_parameter}
        '''
        result = self._values.get("protected_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineRunCommandProtectedParameter"]]], result)

    @builtins.property
    def run_as_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#run_as_password VirtualMachineRunCommand#run_as_password}.'''
        result = self._values.get("run_as_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_as_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#run_as_user VirtualMachineRunCommand#run_as_user}.'''
        result = self._values.get("run_as_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#tags VirtualMachineRunCommand#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VirtualMachineRunCommandTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#timeouts VirtualMachineRunCommand#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VirtualMachineRunCommandTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandErrorBlobManagedIdentity",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "object_id": "objectId"},
)
class VirtualMachineRunCommandErrorBlobManagedIdentity:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54dce310e304069021b212302b73e891e7619e3e3bc3c32395805afed8d14204)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if object_id is not None:
            self._values["object_id"] = object_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.'''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandErrorBlobManagedIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandErrorBlobManagedIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandErrorBlobManagedIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29eddbfa632714ca09a8407a73588ed609167a99ffb648c9d433a910cb9b0147)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5517658564970d8183f215fa02824e0741978cdf979af41f3dc9718a81c08326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db2d45b78f3a89a86a88d72a3ba789be74afd64c35649712d0058198284ecf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualMachineRunCommandErrorBlobManagedIdentity]:
        return typing.cast(typing.Optional[VirtualMachineRunCommandErrorBlobManagedIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineRunCommandErrorBlobManagedIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fada36ff123d5d6f4ef22d5319f14ffdaddc4307f3988dcd9d19715bd3fe40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandInstanceView",
    jsii_struct_bases=[],
    name_mapping={},
)
class VirtualMachineRunCommandInstanceView:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandInstanceView(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandInstanceViewList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandInstanceViewList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24769d88fddc6108af8249560adc32cfe99c049e5682cfcb82fa81ce3973d8f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachineRunCommandInstanceViewOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec37ed4bac28a6b1a28d60d1ee259daa7a0c34b14f920e12f021eb9e4888b98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineRunCommandInstanceViewOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ecbd2d7d325775b28cf69fd958ba6c266134b81648e5d4450ee28132f8e2ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36de6b863bbeb40ddb74066875dffa7e3e8b4523e6e0c58a8b9d8bba7df3c70d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__056228776b07450d58d7093590653b86be13cf2161408cb493acbd268dde623c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VirtualMachineRunCommandInstanceViewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandInstanceViewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9c4a6660a0c7bf8a37984bef1618645f0fd9009392799ed068c5ad919b5a093)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="executionMessage")
    def execution_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionMessage"))

    @builtins.property
    @jsii.member(jsii_name="executionState")
    def execution_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionState"))

    @builtins.property
    @jsii.member(jsii_name="exitCode")
    def exit_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "exitCode"))

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "output"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VirtualMachineRunCommandInstanceView]:
        return typing.cast(typing.Optional[VirtualMachineRunCommandInstanceView], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineRunCommandInstanceView],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182ef26dc77d971ef7fc6521f716b9e98b1bac2de2106d436228bf178b690870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandOutputBlobManagedIdentity",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "object_id": "objectId"},
)
class VirtualMachineRunCommandOutputBlobManagedIdentity:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c1a8522e6e6fec4be2e13001c0f1260971ba7dcbc7f0c49ee7c0e89494e72e)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if object_id is not None:
            self._values["object_id"] = object_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.'''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandOutputBlobManagedIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandOutputBlobManagedIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandOutputBlobManagedIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2bd03c2e904080bd0b2a29e4163dd755ccc5a5e43fd07655a74dd1cff866b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5201f8aa75648d86eabce79dc39bbbc520376d9ead1a2fee16dbd05fc72e04e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7bf07d2f5ac22cded835c0b7346ded2604d709f0e566643dfdad706c0d5f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualMachineRunCommandOutputBlobManagedIdentity]:
        return typing.cast(typing.Optional[VirtualMachineRunCommandOutputBlobManagedIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineRunCommandOutputBlobManagedIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836b524a6f9b0ae79fc3b959078bae5acf0100f066e5f80e6adf8f46df5731ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class VirtualMachineRunCommandParameter:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#name VirtualMachineRunCommand#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#value VirtualMachineRunCommand#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f39c5aa2077306ae91e653d4e62e6fa3653c081b188497213c30c1403b11a6c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#name VirtualMachineRunCommand#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#value VirtualMachineRunCommand#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b29287e499dd9d748facac6b7c8ab838a00fd32e14db07d941eddd02eed4f21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachineRunCommandParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34dc6e94e2f0c81f6f5e6d4555286df21e347a3a0ac9e4db014159effc05a82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineRunCommandParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e10645f6107a0b772df2bd1e4b01c1e39ec552580cf0b518e7eb2341349468)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a03da39c69675e064870883a4e41f8005229438deb6c53cf0aedc4d0d97bd56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89b813ac0702063c48271037f158b90a21531d9f304884ef6146b3fcab084735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4f7fc6f45d49ba6cc8bef0385241f1de0401c8f3e458f298f13aef5c54433e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualMachineRunCommandParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83b831757c2af19031b42cddfdc3129e50afaec430c90fb6032e9f6e74341eed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dabb03799889fcdb6603fb6adbe8aec4af916d1c03e9056ad8dad8a192dbf3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de363d0ae080dce287c5e4a9be4a29ebae729c0b77134d36b840489acb37ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2c0942918b807366d055e99b57abd3595f8caf11dba660e5510746087e41f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandProtectedParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class VirtualMachineRunCommandProtectedParameter:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#name VirtualMachineRunCommand#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#value VirtualMachineRunCommand#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992822b7a87489c48dd1f7ec9ae8cd7f357f16b9067bebc0f2e7fd9e0c471b64)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#name VirtualMachineRunCommand#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#value VirtualMachineRunCommand#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandProtectedParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandProtectedParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandProtectedParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f493ac4ffdbbfd31da19e5a4f15d8dba226b89301b7366ce79081a694d1df340)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachineRunCommandProtectedParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219ef661a964f2e4cf11e4ca684d93be91eb017aae2bdf5ee0828980e007287e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineRunCommandProtectedParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0555b4a019066d4327ab4233121cb6bce9a212afc2b1ce21c1382346fea41a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea849f85bf9769aa43a689fbeead1f30685758284a5fbc4cef088659be338067)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06178adac0876cda146d9d2061ee966beec5b4f0ef2dbfbce1f401fdf5d0fc36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandProtectedParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandProtectedParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandProtectedParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb586489f43a7aa53f785c4baf8fd02f9d4c8b9a6bd20c728a4a003bfa2ef5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualMachineRunCommandProtectedParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandProtectedParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__893fe317f2111bdeabc6896767c022c577541e29e09301309c85116075085eda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fececc9bb023e2b0cff05324582c1bbd4e3821fafe4b836516618c0ffe5c6e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44d18b2a94ce8398a436b2ad6b63f1a13218d290ec0dc76aeff53245bf49daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandProtectedParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandProtectedParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandProtectedParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2982a13009df7c173254bf3b18ebb3e379e57eb5380b3f7814078f1f906bbd09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandSource",
    jsii_struct_bases=[],
    name_mapping={
        "command_id": "commandId",
        "script": "script",
        "script_uri": "scriptUri",
        "script_uri_managed_identity": "scriptUriManagedIdentity",
    },
)
class VirtualMachineRunCommandSource:
    def __init__(
        self,
        *,
        command_id: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
        script_uri: typing.Optional[builtins.str] = None,
        script_uri_managed_identity: typing.Optional[typing.Union["VirtualMachineRunCommandSourceScriptUriManagedIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param command_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#command_id VirtualMachineRunCommand#command_id}.
        :param script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script VirtualMachineRunCommand#script}.
        :param script_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script_uri VirtualMachineRunCommand#script_uri}.
        :param script_uri_managed_identity: script_uri_managed_identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script_uri_managed_identity VirtualMachineRunCommand#script_uri_managed_identity}
        '''
        if isinstance(script_uri_managed_identity, dict):
            script_uri_managed_identity = VirtualMachineRunCommandSourceScriptUriManagedIdentity(**script_uri_managed_identity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30265ded53a02f0c4be027347c46954aabb28a09c1957ea0c4958958a9b18f13)
            check_type(argname="argument command_id", value=command_id, expected_type=type_hints["command_id"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument script_uri", value=script_uri, expected_type=type_hints["script_uri"])
            check_type(argname="argument script_uri_managed_identity", value=script_uri_managed_identity, expected_type=type_hints["script_uri_managed_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command_id is not None:
            self._values["command_id"] = command_id
        if script is not None:
            self._values["script"] = script
        if script_uri is not None:
            self._values["script_uri"] = script_uri
        if script_uri_managed_identity is not None:
            self._values["script_uri_managed_identity"] = script_uri_managed_identity

    @builtins.property
    def command_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#command_id VirtualMachineRunCommand#command_id}.'''
        result = self._values.get("command_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script VirtualMachineRunCommand#script}.'''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script_uri VirtualMachineRunCommand#script_uri}.'''
        result = self._values.get("script_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_uri_managed_identity(
        self,
    ) -> typing.Optional["VirtualMachineRunCommandSourceScriptUriManagedIdentity"]:
        '''script_uri_managed_identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#script_uri_managed_identity VirtualMachineRunCommand#script_uri_managed_identity}
        '''
        result = self._values.get("script_uri_managed_identity")
        return typing.cast(typing.Optional["VirtualMachineRunCommandSourceScriptUriManagedIdentity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bc4f69c91322c03fba17ea2f37cecf4985ce9cf9b34e32b0c2910cc66f6924f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptUriManagedIdentity")
    def put_script_uri_managed_identity(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.
        '''
        value = VirtualMachineRunCommandSourceScriptUriManagedIdentity(
            client_id=client_id, object_id=object_id
        )

        return typing.cast(None, jsii.invoke(self, "putScriptUriManagedIdentity", [value]))

    @jsii.member(jsii_name="resetCommandId")
    def reset_command_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommandId", []))

    @jsii.member(jsii_name="resetScript")
    def reset_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScript", []))

    @jsii.member(jsii_name="resetScriptUri")
    def reset_script_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptUri", []))

    @jsii.member(jsii_name="resetScriptUriManagedIdentity")
    def reset_script_uri_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptUriManagedIdentity", []))

    @builtins.property
    @jsii.member(jsii_name="scriptUriManagedIdentity")
    def script_uri_managed_identity(
        self,
    ) -> "VirtualMachineRunCommandSourceScriptUriManagedIdentityOutputReference":
        return typing.cast("VirtualMachineRunCommandSourceScriptUriManagedIdentityOutputReference", jsii.get(self, "scriptUriManagedIdentity"))

    @builtins.property
    @jsii.member(jsii_name="commandIdInput")
    def command_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commandIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptUriInput")
    def script_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptUriInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptUriManagedIdentityInput")
    def script_uri_managed_identity_input(
        self,
    ) -> typing.Optional["VirtualMachineRunCommandSourceScriptUriManagedIdentity"]:
        return typing.cast(typing.Optional["VirtualMachineRunCommandSourceScriptUriManagedIdentity"], jsii.get(self, "scriptUriManagedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="commandId")
    def command_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commandId"))

    @command_id.setter
    def command_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93aafa7e700d99e7759357343eec298c45421b8fed2a89350a55c2b13da815a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commandId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb1dad37066ed9679ec830dc96dd89860a6245bac5097165bca94033883c042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptUri")
    def script_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptUri"))

    @script_uri.setter
    def script_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62b097791b21bf53b849f7c3d0fb16a627266c649f05d2dd385f4bb9e37f6bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VirtualMachineRunCommandSource]:
        return typing.cast(typing.Optional[VirtualMachineRunCommandSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineRunCommandSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1388d3b3c58f3c92cf8ef61b8d7dc22a7cdf2a2766ff57e94137e3cf1560e46a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandSourceScriptUriManagedIdentity",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "object_id": "objectId"},
)
class VirtualMachineRunCommandSourceScriptUriManagedIdentity:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f2a69567a0c6224da8854de7eb8cd842fd1d6ef17743299c50956da6270624)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if object_id is not None:
            self._values["object_id"] = object_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#client_id VirtualMachineRunCommand#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#object_id VirtualMachineRunCommand#object_id}.'''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandSourceScriptUriManagedIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandSourceScriptUriManagedIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandSourceScriptUriManagedIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b4e7c0061c753b414051cb8012e955f1c4ba8f275fa0cac527d19a7469eea57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f88ea2a27e870b8e535949180178b7e7c54bc4b44ae202e6e5b3a95ebade78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dd9a2da79ee66d2732cbcde056b11c99d6feeb6e8c60c6e2747c3de2d6948b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualMachineRunCommandSourceScriptUriManagedIdentity]:
        return typing.cast(typing.Optional[VirtualMachineRunCommandSourceScriptUriManagedIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineRunCommandSourceScriptUriManagedIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca11d0d80e331d56b7c1d0e8e98389231f25de66ec1e235d04df605f18c4dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VirtualMachineRunCommandTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#create VirtualMachineRunCommand#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#delete VirtualMachineRunCommand#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#read VirtualMachineRunCommand#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#update VirtualMachineRunCommand#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc025bd7199fd0c29f4150b49c43b4a82e5f5c2c3881f1ad39e8a648292cc88)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#create VirtualMachineRunCommand#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#delete VirtualMachineRunCommand#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#read VirtualMachineRunCommand#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_run_command#update VirtualMachineRunCommand#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineRunCommandTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineRunCommandTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineRunCommand.VirtualMachineRunCommandTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dec0f66d5354a65d2757675bbcd16364eee6de9b29204245470d5c8256b8aafb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6f988ccdf2ae30c7f54515e13aee59521b8162c796cf57c7348b85cabf091c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313ccb1086371dd0d4d7c189ec9992d84b77764ffd60afef1d4848a2cd5a79cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5778a247b952469e87e92247228877b58b02d87aeaa795c24989d37a2c72c33c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fc667b6c046d8704407e8aa2cc0973a7de1ce6437616258f237a089b9caec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc62736a50df155741299feac9fded42e5db5a1dbdff144c2d4c136e535b09f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VirtualMachineRunCommand",
    "VirtualMachineRunCommandConfig",
    "VirtualMachineRunCommandErrorBlobManagedIdentity",
    "VirtualMachineRunCommandErrorBlobManagedIdentityOutputReference",
    "VirtualMachineRunCommandInstanceView",
    "VirtualMachineRunCommandInstanceViewList",
    "VirtualMachineRunCommandInstanceViewOutputReference",
    "VirtualMachineRunCommandOutputBlobManagedIdentity",
    "VirtualMachineRunCommandOutputBlobManagedIdentityOutputReference",
    "VirtualMachineRunCommandParameter",
    "VirtualMachineRunCommandParameterList",
    "VirtualMachineRunCommandParameterOutputReference",
    "VirtualMachineRunCommandProtectedParameter",
    "VirtualMachineRunCommandProtectedParameterList",
    "VirtualMachineRunCommandProtectedParameterOutputReference",
    "VirtualMachineRunCommandSource",
    "VirtualMachineRunCommandSourceOutputReference",
    "VirtualMachineRunCommandSourceScriptUriManagedIdentity",
    "VirtualMachineRunCommandSourceScriptUriManagedIdentityOutputReference",
    "VirtualMachineRunCommandTimeouts",
    "VirtualMachineRunCommandTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__93a5fc5ebb4b0d2165d2ea6032fc5da4b439e27739c4212436c0386fa56c3fdf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    source: typing.Union[VirtualMachineRunCommandSource, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_id: builtins.str,
    error_blob_managed_identity: typing.Optional[typing.Union[VirtualMachineRunCommandErrorBlobManagedIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    error_blob_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    output_blob_managed_identity: typing.Optional[typing.Union[VirtualMachineRunCommandOutputBlobManagedIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    output_blob_uri: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineRunCommandParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    protected_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineRunCommandProtectedParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    run_as_password: typing.Optional[builtins.str] = None,
    run_as_user: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualMachineRunCommandTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7b1979f46bb8790bed6c97be3b97458b7195463b84da027c6ce06981a1eb5cec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d736d32853461d6305369267ad17b4c4911210c7f2ddd5651a0da511b22506ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineRunCommandParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120d1e8bf01f36581105e8c0ed40a4cca103eca3abe0e71e413c5c9fa09619c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineRunCommandProtectedParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84f176c00808e2d13ce5ecc51839ea0ad540628cea4ea0b9c39364924be88b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7d0ae95fc7c3b1f92b0213bbc3ddc0666f29b3d21e84d6332c03998934e38a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd0b31df5b552cd2c28922d780567fba0d6021ec027350e283984fd9a74d104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3f8c04dc0e9008daf84caafb828c913885912b84b7d0b954d3723ef75e8f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0febd02f04e760b57ee370023b381ec129a61e76adec7e7b1d2bc9db4344219a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82376833f2b24ac557938fa51d116593ec7920589d56e15dcc5455bfa1595ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e534d6d628640cc7aeb73df14afb877eff94dca7bb56c84780b780a23bff83bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce2da7c45246dba5ad71fdb0d7ef211331fd588601d19f8a0c2494f8cd783cb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e187c0d4d837d4b49b782706fb5209ffc74050a0373dde21ddda1b92799d47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6697e7b34e82df71e2406aaec164788a6ca00f5aeebc0b9c7911dd73be5c39(
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
    source: typing.Union[VirtualMachineRunCommandSource, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_id: builtins.str,
    error_blob_managed_identity: typing.Optional[typing.Union[VirtualMachineRunCommandErrorBlobManagedIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    error_blob_uri: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    output_blob_managed_identity: typing.Optional[typing.Union[VirtualMachineRunCommandOutputBlobManagedIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    output_blob_uri: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineRunCommandParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    protected_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineRunCommandProtectedParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    run_as_password: typing.Optional[builtins.str] = None,
    run_as_user: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualMachineRunCommandTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54dce310e304069021b212302b73e891e7619e3e3bc3c32395805afed8d14204(
    *,
    client_id: typing.Optional[builtins.str] = None,
    object_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29eddbfa632714ca09a8407a73588ed609167a99ffb648c9d433a910cb9b0147(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5517658564970d8183f215fa02824e0741978cdf979af41f3dc9718a81c08326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db2d45b78f3a89a86a88d72a3ba789be74afd64c35649712d0058198284ecf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fada36ff123d5d6f4ef22d5319f14ffdaddc4307f3988dcd9d19715bd3fe40(
    value: typing.Optional[VirtualMachineRunCommandErrorBlobManagedIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24769d88fddc6108af8249560adc32cfe99c049e5682cfcb82fa81ce3973d8f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec37ed4bac28a6b1a28d60d1ee259daa7a0c34b14f920e12f021eb9e4888b98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ecbd2d7d325775b28cf69fd958ba6c266134b81648e5d4450ee28132f8e2ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36de6b863bbeb40ddb74066875dffa7e3e8b4523e6e0c58a8b9d8bba7df3c70d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056228776b07450d58d7093590653b86be13cf2161408cb493acbd268dde623c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c4a6660a0c7bf8a37984bef1618645f0fd9009392799ed068c5ad919b5a093(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182ef26dc77d971ef7fc6521f716b9e98b1bac2de2106d436228bf178b690870(
    value: typing.Optional[VirtualMachineRunCommandInstanceView],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c1a8522e6e6fec4be2e13001c0f1260971ba7dcbc7f0c49ee7c0e89494e72e(
    *,
    client_id: typing.Optional[builtins.str] = None,
    object_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2bd03c2e904080bd0b2a29e4163dd755ccc5a5e43fd07655a74dd1cff866b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5201f8aa75648d86eabce79dc39bbbc520376d9ead1a2fee16dbd05fc72e04e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7bf07d2f5ac22cded835c0b7346ded2604d709f0e566643dfdad706c0d5f2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836b524a6f9b0ae79fc3b959078bae5acf0100f066e5f80e6adf8f46df5731ee(
    value: typing.Optional[VirtualMachineRunCommandOutputBlobManagedIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f39c5aa2077306ae91e653d4e62e6fa3653c081b188497213c30c1403b11a6c(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b29287e499dd9d748facac6b7c8ab838a00fd32e14db07d941eddd02eed4f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34dc6e94e2f0c81f6f5e6d4555286df21e347a3a0ac9e4db014159effc05a82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e10645f6107a0b772df2bd1e4b01c1e39ec552580cf0b518e7eb2341349468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a03da39c69675e064870883a4e41f8005229438deb6c53cf0aedc4d0d97bd56(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b813ac0702063c48271037f158b90a21531d9f304884ef6146b3fcab084735(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4f7fc6f45d49ba6cc8bef0385241f1de0401c8f3e458f298f13aef5c54433e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b831757c2af19031b42cddfdc3129e50afaec430c90fb6032e9f6e74341eed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabb03799889fcdb6603fb6adbe8aec4af916d1c03e9056ad8dad8a192dbf3dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de363d0ae080dce287c5e4a9be4a29ebae729c0b77134d36b840489acb37ef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2c0942918b807366d055e99b57abd3595f8caf11dba660e5510746087e41f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992822b7a87489c48dd1f7ec9ae8cd7f357f16b9067bebc0f2e7fd9e0c471b64(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f493ac4ffdbbfd31da19e5a4f15d8dba226b89301b7366ce79081a694d1df340(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219ef661a964f2e4cf11e4ca684d93be91eb017aae2bdf5ee0828980e007287e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0555b4a019066d4327ab4233121cb6bce9a212afc2b1ce21c1382346fea41a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea849f85bf9769aa43a689fbeead1f30685758284a5fbc4cef088659be338067(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06178adac0876cda146d9d2061ee966beec5b4f0ef2dbfbce1f401fdf5d0fc36(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb586489f43a7aa53f785c4baf8fd02f9d4c8b9a6bd20c728a4a003bfa2ef5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineRunCommandProtectedParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893fe317f2111bdeabc6896767c022c577541e29e09301309c85116075085eda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fececc9bb023e2b0cff05324582c1bbd4e3821fafe4b836516618c0ffe5c6e51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44d18b2a94ce8398a436b2ad6b63f1a13218d290ec0dc76aeff53245bf49daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2982a13009df7c173254bf3b18ebb3e379e57eb5380b3f7814078f1f906bbd09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandProtectedParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30265ded53a02f0c4be027347c46954aabb28a09c1957ea0c4958958a9b18f13(
    *,
    command_id: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
    script_uri: typing.Optional[builtins.str] = None,
    script_uri_managed_identity: typing.Optional[typing.Union[VirtualMachineRunCommandSourceScriptUriManagedIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc4f69c91322c03fba17ea2f37cecf4985ce9cf9b34e32b0c2910cc66f6924f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93aafa7e700d99e7759357343eec298c45421b8fed2a89350a55c2b13da815a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb1dad37066ed9679ec830dc96dd89860a6245bac5097165bca94033883c042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62b097791b21bf53b849f7c3d0fb16a627266c649f05d2dd385f4bb9e37f6bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1388d3b3c58f3c92cf8ef61b8d7dc22a7cdf2a2766ff57e94137e3cf1560e46a(
    value: typing.Optional[VirtualMachineRunCommandSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f2a69567a0c6224da8854de7eb8cd842fd1d6ef17743299c50956da6270624(
    *,
    client_id: typing.Optional[builtins.str] = None,
    object_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4e7c0061c753b414051cb8012e955f1c4ba8f275fa0cac527d19a7469eea57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f88ea2a27e870b8e535949180178b7e7c54bc4b44ae202e6e5b3a95ebade78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dd9a2da79ee66d2732cbcde056b11c99d6feeb6e8c60c6e2747c3de2d6948b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca11d0d80e331d56b7c1d0e8e98389231f25de66ec1e235d04df605f18c4dea(
    value: typing.Optional[VirtualMachineRunCommandSourceScriptUriManagedIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc025bd7199fd0c29f4150b49c43b4a82e5f5c2c3881f1ad39e8a648292cc88(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec0f66d5354a65d2757675bbcd16364eee6de9b29204245470d5c8256b8aafb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f988ccdf2ae30c7f54515e13aee59521b8162c796cf57c7348b85cabf091c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313ccb1086371dd0d4d7c189ec9992d84b77764ffd60afef1d4848a2cd5a79cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5778a247b952469e87e92247228877b58b02d87aeaa795c24989d37a2c72c33c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fc667b6c046d8704407e8aa2cc0973a7de1ce6437616258f237a089b9caec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc62736a50df155741299feac9fded42e5db5a1dbdff144c2d4c136e535b09f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineRunCommandTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
