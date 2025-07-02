r'''
# `azurerm_virtual_machine_scale_set_packet_capture`

Refer to the Terraform Registry for docs: [`azurerm_virtual_machine_scale_set_packet_capture`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture).
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


class VirtualMachineScaleSetPacketCapture(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCapture",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture azurerm_virtual_machine_scale_set_packet_capture}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network_watcher_id: builtins.str,
        storage_location: typing.Union["VirtualMachineScaleSetPacketCaptureStorageLocation", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_scale_set_id: builtins.str,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineScaleSetPacketCaptureFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        machine_scope: typing.Optional[typing.Union["VirtualMachineScaleSetPacketCaptureMachineScope", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
        maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
        maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["VirtualMachineScaleSetPacketCaptureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture azurerm_virtual_machine_scale_set_packet_capture} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#name VirtualMachineScaleSetPacketCapture#name}.
        :param network_watcher_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#network_watcher_id VirtualMachineScaleSetPacketCapture#network_watcher_id}.
        :param storage_location: storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#storage_location VirtualMachineScaleSetPacketCapture#storage_location}
        :param virtual_machine_scale_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#virtual_machine_scale_set_id VirtualMachineScaleSetPacketCapture#virtual_machine_scale_set_id}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#filter VirtualMachineScaleSetPacketCapture#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#id VirtualMachineScaleSetPacketCapture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param machine_scope: machine_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#machine_scope VirtualMachineScaleSetPacketCapture#machine_scope}
        :param maximum_bytes_per_packet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_bytes_per_packet VirtualMachineScaleSetPacketCapture#maximum_bytes_per_packet}.
        :param maximum_bytes_per_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_bytes_per_session VirtualMachineScaleSetPacketCapture#maximum_bytes_per_session}.
        :param maximum_capture_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_capture_duration_in_seconds VirtualMachineScaleSetPacketCapture#maximum_capture_duration_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#timeouts VirtualMachineScaleSetPacketCapture#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9bbe7bfc7f48ab067327684bdebf3b2d35dca7deff8e31f1933e6cbcffbf196)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualMachineScaleSetPacketCaptureConfig(
            name=name,
            network_watcher_id=network_watcher_id,
            storage_location=storage_location,
            virtual_machine_scale_set_id=virtual_machine_scale_set_id,
            filter=filter,
            id=id,
            machine_scope=machine_scope,
            maximum_bytes_per_packet=maximum_bytes_per_packet,
            maximum_bytes_per_session=maximum_bytes_per_session,
            maximum_capture_duration_in_seconds=maximum_capture_duration_in_seconds,
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
        '''Generates CDKTF code for importing a VirtualMachineScaleSetPacketCapture resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VirtualMachineScaleSetPacketCapture to import.
        :param import_from_id: The id of the existing VirtualMachineScaleSetPacketCapture that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VirtualMachineScaleSetPacketCapture to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc99ada46c99bcfafbaa58c56660e95e6d6f59b357a6461bbff87a560c11072)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineScaleSetPacketCaptureFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1e11e39129af4b95f4611a6adf1f52458d344764cecd1851dd0a9e827b1117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putMachineScope")
    def put_machine_scope(
        self,
        *,
        exclude_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_instance_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#exclude_instance_ids VirtualMachineScaleSetPacketCapture#exclude_instance_ids}.
        :param include_instance_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#include_instance_ids VirtualMachineScaleSetPacketCapture#include_instance_ids}.
        '''
        value = VirtualMachineScaleSetPacketCaptureMachineScope(
            exclude_instance_ids=exclude_instance_ids,
            include_instance_ids=include_instance_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putMachineScope", [value]))

    @jsii.member(jsii_name="putStorageLocation")
    def put_storage_location(
        self,
        *,
        file_path: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#file_path VirtualMachineScaleSetPacketCapture#file_path}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#storage_account_id VirtualMachineScaleSetPacketCapture#storage_account_id}.
        '''
        value = VirtualMachineScaleSetPacketCaptureStorageLocation(
            file_path=file_path, storage_account_id=storage_account_id
        )

        return typing.cast(None, jsii.invoke(self, "putStorageLocation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#create VirtualMachineScaleSetPacketCapture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#delete VirtualMachineScaleSetPacketCapture#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#read VirtualMachineScaleSetPacketCapture#read}.
        '''
        value = VirtualMachineScaleSetPacketCaptureTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMachineScope")
    def reset_machine_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineScope", []))

    @jsii.member(jsii_name="resetMaximumBytesPerPacket")
    def reset_maximum_bytes_per_packet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBytesPerPacket", []))

    @jsii.member(jsii_name="resetMaximumBytesPerSession")
    def reset_maximum_bytes_per_session(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumBytesPerSession", []))

    @jsii.member(jsii_name="resetMaximumCaptureDurationInSeconds")
    def reset_maximum_capture_duration_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumCaptureDurationInSeconds", []))

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
    @jsii.member(jsii_name="filter")
    def filter(self) -> "VirtualMachineScaleSetPacketCaptureFilterList":
        return typing.cast("VirtualMachineScaleSetPacketCaptureFilterList", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="machineScope")
    def machine_scope(
        self,
    ) -> "VirtualMachineScaleSetPacketCaptureMachineScopeOutputReference":
        return typing.cast("VirtualMachineScaleSetPacketCaptureMachineScopeOutputReference", jsii.get(self, "machineScope"))

    @builtins.property
    @jsii.member(jsii_name="storageLocation")
    def storage_location(
        self,
    ) -> "VirtualMachineScaleSetPacketCaptureStorageLocationOutputReference":
        return typing.cast("VirtualMachineScaleSetPacketCaptureStorageLocationOutputReference", jsii.get(self, "storageLocation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualMachineScaleSetPacketCaptureTimeoutsOutputReference":
        return typing.cast("VirtualMachineScaleSetPacketCaptureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineScaleSetPacketCaptureFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineScaleSetPacketCaptureFilter"]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="machineScopeInput")
    def machine_scope_input(
        self,
    ) -> typing.Optional["VirtualMachineScaleSetPacketCaptureMachineScope"]:
        return typing.cast(typing.Optional["VirtualMachineScaleSetPacketCaptureMachineScope"], jsii.get(self, "machineScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBytesPerPacketInput")
    def maximum_bytes_per_packet_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBytesPerPacketInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBytesPerSessionInput")
    def maximum_bytes_per_session_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumBytesPerSessionInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumCaptureDurationInSecondsInput")
    def maximum_capture_duration_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumCaptureDurationInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkWatcherIdInput")
    def network_watcher_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkWatcherIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocationInput")
    def storage_location_input(
        self,
    ) -> typing.Optional["VirtualMachineScaleSetPacketCaptureStorageLocation"]:
        return typing.cast(typing.Optional["VirtualMachineScaleSetPacketCaptureStorageLocation"], jsii.get(self, "storageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualMachineScaleSetPacketCaptureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualMachineScaleSetPacketCaptureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineScaleSetIdInput")
    def virtual_machine_scale_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineScaleSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e338fe2586846962b7e96de800d42a1992f4aecfc9c78da034425817bac2bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBytesPerPacket")
    def maximum_bytes_per_packet(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBytesPerPacket"))

    @maximum_bytes_per_packet.setter
    def maximum_bytes_per_packet(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1725dd0ad6c2289672898588bd9b001198af432a6b809a9911283fa4f3337fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBytesPerPacket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBytesPerSession")
    def maximum_bytes_per_session(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBytesPerSession"))

    @maximum_bytes_per_session.setter
    def maximum_bytes_per_session(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b109e0c915aa68e37afd5851310b107dd35e33fa73d7f82875ae2133cd4a28bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBytesPerSession", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumCaptureDurationInSeconds")
    def maximum_capture_duration_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumCaptureDurationInSeconds"))

    @maximum_capture_duration_in_seconds.setter
    def maximum_capture_duration_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba56ecd819dfe2604b616498ec9753c2d68f1fe8f412d0f1ec1c82aad9e6d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumCaptureDurationInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974a0df2389c94778dd63b2284129ebf987070c810bd1069f17d0b6e4e38c0e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkWatcherId")
    def network_watcher_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkWatcherId"))

    @network_watcher_id.setter
    def network_watcher_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df6d8c57d58267b0b743ab5a665e1bb22e639d8b62cf5f313351ab9b801df56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkWatcherId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineScaleSetId")
    def virtual_machine_scale_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineScaleSetId"))

    @virtual_machine_scale_set_id.setter
    def virtual_machine_scale_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964ed851e3f6453e95bf96e5458f066bc3c353fcba656f57a831f727b5707ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineScaleSetId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "network_watcher_id": "networkWatcherId",
        "storage_location": "storageLocation",
        "virtual_machine_scale_set_id": "virtualMachineScaleSetId",
        "filter": "filter",
        "id": "id",
        "machine_scope": "machineScope",
        "maximum_bytes_per_packet": "maximumBytesPerPacket",
        "maximum_bytes_per_session": "maximumBytesPerSession",
        "maximum_capture_duration_in_seconds": "maximumCaptureDurationInSeconds",
        "timeouts": "timeouts",
    },
)
class VirtualMachineScaleSetPacketCaptureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        network_watcher_id: builtins.str,
        storage_location: typing.Union["VirtualMachineScaleSetPacketCaptureStorageLocation", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_scale_set_id: builtins.str,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineScaleSetPacketCaptureFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        machine_scope: typing.Optional[typing.Union["VirtualMachineScaleSetPacketCaptureMachineScope", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
        maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
        maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["VirtualMachineScaleSetPacketCaptureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#name VirtualMachineScaleSetPacketCapture#name}.
        :param network_watcher_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#network_watcher_id VirtualMachineScaleSetPacketCapture#network_watcher_id}.
        :param storage_location: storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#storage_location VirtualMachineScaleSetPacketCapture#storage_location}
        :param virtual_machine_scale_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#virtual_machine_scale_set_id VirtualMachineScaleSetPacketCapture#virtual_machine_scale_set_id}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#filter VirtualMachineScaleSetPacketCapture#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#id VirtualMachineScaleSetPacketCapture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param machine_scope: machine_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#machine_scope VirtualMachineScaleSetPacketCapture#machine_scope}
        :param maximum_bytes_per_packet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_bytes_per_packet VirtualMachineScaleSetPacketCapture#maximum_bytes_per_packet}.
        :param maximum_bytes_per_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_bytes_per_session VirtualMachineScaleSetPacketCapture#maximum_bytes_per_session}.
        :param maximum_capture_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_capture_duration_in_seconds VirtualMachineScaleSetPacketCapture#maximum_capture_duration_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#timeouts VirtualMachineScaleSetPacketCapture#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(storage_location, dict):
            storage_location = VirtualMachineScaleSetPacketCaptureStorageLocation(**storage_location)
        if isinstance(machine_scope, dict):
            machine_scope = VirtualMachineScaleSetPacketCaptureMachineScope(**machine_scope)
        if isinstance(timeouts, dict):
            timeouts = VirtualMachineScaleSetPacketCaptureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f720f9f85b8dd685a37ffee68cc02a58b2e629b921bef2a9dec3e12fbab0c93)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_watcher_id", value=network_watcher_id, expected_type=type_hints["network_watcher_id"])
            check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            check_type(argname="argument virtual_machine_scale_set_id", value=virtual_machine_scale_set_id, expected_type=type_hints["virtual_machine_scale_set_id"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_scope", value=machine_scope, expected_type=type_hints["machine_scope"])
            check_type(argname="argument maximum_bytes_per_packet", value=maximum_bytes_per_packet, expected_type=type_hints["maximum_bytes_per_packet"])
            check_type(argname="argument maximum_bytes_per_session", value=maximum_bytes_per_session, expected_type=type_hints["maximum_bytes_per_session"])
            check_type(argname="argument maximum_capture_duration_in_seconds", value=maximum_capture_duration_in_seconds, expected_type=type_hints["maximum_capture_duration_in_seconds"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network_watcher_id": network_watcher_id,
            "storage_location": storage_location,
            "virtual_machine_scale_set_id": virtual_machine_scale_set_id,
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
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if machine_scope is not None:
            self._values["machine_scope"] = machine_scope
        if maximum_bytes_per_packet is not None:
            self._values["maximum_bytes_per_packet"] = maximum_bytes_per_packet
        if maximum_bytes_per_session is not None:
            self._values["maximum_bytes_per_session"] = maximum_bytes_per_session
        if maximum_capture_duration_in_seconds is not None:
            self._values["maximum_capture_duration_in_seconds"] = maximum_capture_duration_in_seconds
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#name VirtualMachineScaleSetPacketCapture#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_watcher_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#network_watcher_id VirtualMachineScaleSetPacketCapture#network_watcher_id}.'''
        result = self._values.get("network_watcher_id")
        assert result is not None, "Required property 'network_watcher_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_location(self) -> "VirtualMachineScaleSetPacketCaptureStorageLocation":
        '''storage_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#storage_location VirtualMachineScaleSetPacketCapture#storage_location}
        '''
        result = self._values.get("storage_location")
        assert result is not None, "Required property 'storage_location' is missing"
        return typing.cast("VirtualMachineScaleSetPacketCaptureStorageLocation", result)

    @builtins.property
    def virtual_machine_scale_set_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#virtual_machine_scale_set_id VirtualMachineScaleSetPacketCapture#virtual_machine_scale_set_id}.'''
        result = self._values.get("virtual_machine_scale_set_id")
        assert result is not None, "Required property 'virtual_machine_scale_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineScaleSetPacketCaptureFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#filter VirtualMachineScaleSetPacketCapture#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineScaleSetPacketCaptureFilter"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#id VirtualMachineScaleSetPacketCapture#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_scope(
        self,
    ) -> typing.Optional["VirtualMachineScaleSetPacketCaptureMachineScope"]:
        '''machine_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#machine_scope VirtualMachineScaleSetPacketCapture#machine_scope}
        '''
        result = self._values.get("machine_scope")
        return typing.cast(typing.Optional["VirtualMachineScaleSetPacketCaptureMachineScope"], result)

    @builtins.property
    def maximum_bytes_per_packet(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_bytes_per_packet VirtualMachineScaleSetPacketCapture#maximum_bytes_per_packet}.'''
        result = self._values.get("maximum_bytes_per_packet")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_bytes_per_session(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_bytes_per_session VirtualMachineScaleSetPacketCapture#maximum_bytes_per_session}.'''
        result = self._values.get("maximum_bytes_per_session")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_capture_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#maximum_capture_duration_in_seconds VirtualMachineScaleSetPacketCapture#maximum_capture_duration_in_seconds}.'''
        result = self._values.get("maximum_capture_duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["VirtualMachineScaleSetPacketCaptureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#timeouts VirtualMachineScaleSetPacketCapture#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VirtualMachineScaleSetPacketCaptureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineScaleSetPacketCaptureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureFilter",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "local_ip_address": "localIpAddress",
        "local_port": "localPort",
        "remote_ip_address": "remoteIpAddress",
        "remote_port": "remotePort",
    },
)
class VirtualMachineScaleSetPacketCaptureFilter:
    def __init__(
        self,
        *,
        protocol: builtins.str,
        local_ip_address: typing.Optional[builtins.str] = None,
        local_port: typing.Optional[builtins.str] = None,
        remote_ip_address: typing.Optional[builtins.str] = None,
        remote_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#protocol VirtualMachineScaleSetPacketCapture#protocol}.
        :param local_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#local_ip_address VirtualMachineScaleSetPacketCapture#local_ip_address}.
        :param local_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#local_port VirtualMachineScaleSetPacketCapture#local_port}.
        :param remote_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#remote_ip_address VirtualMachineScaleSetPacketCapture#remote_ip_address}.
        :param remote_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#remote_port VirtualMachineScaleSetPacketCapture#remote_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb707ca933cf3b5774511220e8e8caab2711671def449a18c20ef06a43e7db28)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument local_ip_address", value=local_ip_address, expected_type=type_hints["local_ip_address"])
            check_type(argname="argument local_port", value=local_port, expected_type=type_hints["local_port"])
            check_type(argname="argument remote_ip_address", value=remote_ip_address, expected_type=type_hints["remote_ip_address"])
            check_type(argname="argument remote_port", value=remote_port, expected_type=type_hints["remote_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol": protocol,
        }
        if local_ip_address is not None:
            self._values["local_ip_address"] = local_ip_address
        if local_port is not None:
            self._values["local_port"] = local_port
        if remote_ip_address is not None:
            self._values["remote_ip_address"] = remote_ip_address
        if remote_port is not None:
            self._values["remote_port"] = remote_port

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#protocol VirtualMachineScaleSetPacketCapture#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#local_ip_address VirtualMachineScaleSetPacketCapture#local_ip_address}.'''
        result = self._values.get("local_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#local_port VirtualMachineScaleSetPacketCapture#local_port}.'''
        result = self._values.get("local_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#remote_ip_address VirtualMachineScaleSetPacketCapture#remote_ip_address}.'''
        result = self._values.get("remote_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#remote_port VirtualMachineScaleSetPacketCapture#remote_port}.'''
        result = self._values.get("remote_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineScaleSetPacketCaptureFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineScaleSetPacketCaptureFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd23a1d8f008d469269cd58592eb0ea9e9b259ac97927a8b5de17823c3126a2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachineScaleSetPacketCaptureFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782c54b3e94cd945da51d6059ca2c85899a4223cb95ec7f55a041e2e4c86abe0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineScaleSetPacketCaptureFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb74e00f0beaec215cfdde3f11962eae8c215e3186fdf2997b004766ee125b6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__856b196f97ae3f5a15aa450323709b74f12ff27b97add2a15b1c5fc0065bd5bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eed823a27bf822daa204d937b2ebfab54d695b4d7c094ff40c3902c9de58b25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineScaleSetPacketCaptureFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineScaleSetPacketCaptureFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineScaleSetPacketCaptureFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af583d9a6ce7a656033797d14b4ad164bcc336ed16de9358104d1ebdee4d5b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualMachineScaleSetPacketCaptureFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf782da0e90234d810979ce99390b5990bb8dc3a99b36bf44010ef25756e7586)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLocalIpAddress")
    def reset_local_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalIpAddress", []))

    @jsii.member(jsii_name="resetLocalPort")
    def reset_local_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPort", []))

    @jsii.member(jsii_name="resetRemoteIpAddress")
    def reset_remote_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteIpAddress", []))

    @jsii.member(jsii_name="resetRemotePort")
    def reset_remote_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemotePort", []))

    @builtins.property
    @jsii.member(jsii_name="localIpAddressInput")
    def local_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="localPortInput")
    def local_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPortInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIpAddressInput")
    def remote_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="remotePortInput")
    def remote_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remotePortInput"))

    @builtins.property
    @jsii.member(jsii_name="localIpAddress")
    def local_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIpAddress"))

    @local_ip_address.setter
    def local_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b9d91c0c8ef9afd19d00b6d60ddea97947915126323a26bbaee8f2e80654fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPort")
    def local_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPort"))

    @local_port.setter
    def local_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744869b7d7d13081d8a7c42d7f5748e3a272e70db32cf1032c8bdc420bd36c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2da3d76153923d88153acd425b1029c2bc55e4302086ee95f5875f390beb00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteIpAddress")
    def remote_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteIpAddress"))

    @remote_ip_address.setter
    def remote_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0545ec63b0d34a434542fe5035a5eee71fe45d186956f8423487f2fd7c0968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remotePort")
    def remote_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remotePort"))

    @remote_port.setter
    def remote_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b1e4661b2b868433adad21dcb89fa5725f8f3d3158241d387f924cb4a8b2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remotePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11008ba4609d205a73436987ed318493a05fa187a07e9177db0518a45374362f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureMachineScope",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_instance_ids": "excludeInstanceIds",
        "include_instance_ids": "includeInstanceIds",
    },
)
class VirtualMachineScaleSetPacketCaptureMachineScope:
    def __init__(
        self,
        *,
        exclude_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_instance_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#exclude_instance_ids VirtualMachineScaleSetPacketCapture#exclude_instance_ids}.
        :param include_instance_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#include_instance_ids VirtualMachineScaleSetPacketCapture#include_instance_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58df8939a44b7ee1d8470b8213a6ce8b5c6e0e9774ae106630a048572822a64)
            check_type(argname="argument exclude_instance_ids", value=exclude_instance_ids, expected_type=type_hints["exclude_instance_ids"])
            check_type(argname="argument include_instance_ids", value=include_instance_ids, expected_type=type_hints["include_instance_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_instance_ids is not None:
            self._values["exclude_instance_ids"] = exclude_instance_ids
        if include_instance_ids is not None:
            self._values["include_instance_ids"] = include_instance_ids

    @builtins.property
    def exclude_instance_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#exclude_instance_ids VirtualMachineScaleSetPacketCapture#exclude_instance_ids}.'''
        result = self._values.get("exclude_instance_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_instance_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#include_instance_ids VirtualMachineScaleSetPacketCapture#include_instance_ids}.'''
        result = self._values.get("include_instance_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineScaleSetPacketCaptureMachineScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineScaleSetPacketCaptureMachineScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureMachineScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0efa7a3a77ee98a9981ba55ea7b72aad28d242596b4d37be994a5fe493f2400a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeInstanceIds")
    def reset_exclude_instance_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeInstanceIds", []))

    @jsii.member(jsii_name="resetIncludeInstanceIds")
    def reset_include_instance_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeInstanceIds", []))

    @builtins.property
    @jsii.member(jsii_name="excludeInstanceIdsInput")
    def exclude_instance_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeInstanceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInstanceIdsInput")
    def include_instance_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeInstanceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInstanceIds")
    def exclude_instance_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeInstanceIds"))

    @exclude_instance_ids.setter
    def exclude_instance_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218fdb954c8d68b79308fac443f53ee5fbd1779e0263af2e07921aa67a9c9b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeInstanceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeInstanceIds")
    def include_instance_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeInstanceIds"))

    @include_instance_ids.setter
    def include_instance_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52c494b2203796bfa2d43d14e653aff5af77750ebb7ed1babd658155d611691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeInstanceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualMachineScaleSetPacketCaptureMachineScope]:
        return typing.cast(typing.Optional[VirtualMachineScaleSetPacketCaptureMachineScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineScaleSetPacketCaptureMachineScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b8336579cb8f9f1802d5754cdf56dd91edf4ebca91dc2b27f33c9aad7fcafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureStorageLocation",
    jsii_struct_bases=[],
    name_mapping={"file_path": "filePath", "storage_account_id": "storageAccountId"},
)
class VirtualMachineScaleSetPacketCaptureStorageLocation:
    def __init__(
        self,
        *,
        file_path: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#file_path VirtualMachineScaleSetPacketCapture#file_path}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#storage_account_id VirtualMachineScaleSetPacketCapture#storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c60bd32e1ef519d761cf30b5cc257c069c46e96d75c4c593c8713314941fc4)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_path is not None:
            self._values["file_path"] = file_path
        if storage_account_id is not None:
            self._values["storage_account_id"] = storage_account_id

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#file_path VirtualMachineScaleSetPacketCapture#file_path}.'''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#storage_account_id VirtualMachineScaleSetPacketCapture#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineScaleSetPacketCaptureStorageLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineScaleSetPacketCaptureStorageLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureStorageLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbfe711e3f673180dba5dbb339627319eb32bfc566b7f51ff7e415dd06dea300)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilePath")
    def reset_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePath", []))

    @jsii.member(jsii_name="resetStorageAccountId")
    def reset_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="storagePath")
    def storage_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePath"))

    @builtins.property
    @jsii.member(jsii_name="filePathInput")
    def file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePathInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @file_path.setter
    def file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef96c39db426f4af398c0f4a69acede22f7186243b00ac2e7bbd6032194196e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d304d5ff98c6482879b6b39357006c985b010950f2437fad6681429b6d6b597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualMachineScaleSetPacketCaptureStorageLocation]:
        return typing.cast(typing.Optional[VirtualMachineScaleSetPacketCaptureStorageLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineScaleSetPacketCaptureStorageLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef6f33484a35c4a38f22c91cdd079fc3f8e8c7ca90b5f9f6af90c56b4899ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class VirtualMachineScaleSetPacketCaptureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#create VirtualMachineScaleSetPacketCapture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#delete VirtualMachineScaleSetPacketCapture#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#read VirtualMachineScaleSetPacketCapture#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b80b16079f98e97696656c1ed37c500bf118ae1674755fded5141b2c8e7bbd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#create VirtualMachineScaleSetPacketCapture#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#delete VirtualMachineScaleSetPacketCapture#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_scale_set_packet_capture#read VirtualMachineScaleSetPacketCapture#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineScaleSetPacketCaptureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineScaleSetPacketCaptureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachineScaleSetPacketCapture.VirtualMachineScaleSetPacketCaptureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb07737d0beb7e4b70f7115001f93782b9bb3afed71fa098807cf2d637cd1769)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31104aea26bd040cddf4a4728aca13b260097995bf211caa0edb405a895b12d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4252e8e82c864c8a8cd3ad354482120ec0a3f24895afb52a4d7167d2853913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7abeda1ab34bd6bad9f5fe65288a22fc04a6ca58cea39ae325bdc12a7ed6301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895852264a0a411782472321fe62c7554c0bdc16d0a83c5f9b4a99d718b9fa67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VirtualMachineScaleSetPacketCapture",
    "VirtualMachineScaleSetPacketCaptureConfig",
    "VirtualMachineScaleSetPacketCaptureFilter",
    "VirtualMachineScaleSetPacketCaptureFilterList",
    "VirtualMachineScaleSetPacketCaptureFilterOutputReference",
    "VirtualMachineScaleSetPacketCaptureMachineScope",
    "VirtualMachineScaleSetPacketCaptureMachineScopeOutputReference",
    "VirtualMachineScaleSetPacketCaptureStorageLocation",
    "VirtualMachineScaleSetPacketCaptureStorageLocationOutputReference",
    "VirtualMachineScaleSetPacketCaptureTimeouts",
    "VirtualMachineScaleSetPacketCaptureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c9bbe7bfc7f48ab067327684bdebf3b2d35dca7deff8e31f1933e6cbcffbf196(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network_watcher_id: builtins.str,
    storage_location: typing.Union[VirtualMachineScaleSetPacketCaptureStorageLocation, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_scale_set_id: builtins.str,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineScaleSetPacketCaptureFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    machine_scope: typing.Optional[typing.Union[VirtualMachineScaleSetPacketCaptureMachineScope, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
    maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
    maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[VirtualMachineScaleSetPacketCaptureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bdc99ada46c99bcfafbaa58c56660e95e6d6f59b357a6461bbff87a560c11072(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1e11e39129af4b95f4611a6adf1f52458d344764cecd1851dd0a9e827b1117(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineScaleSetPacketCaptureFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e338fe2586846962b7e96de800d42a1992f4aecfc9c78da034425817bac2bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1725dd0ad6c2289672898588bd9b001198af432a6b809a9911283fa4f3337fa0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b109e0c915aa68e37afd5851310b107dd35e33fa73d7f82875ae2133cd4a28bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba56ecd819dfe2604b616498ec9753c2d68f1fe8f412d0f1ec1c82aad9e6d60(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974a0df2389c94778dd63b2284129ebf987070c810bd1069f17d0b6e4e38c0e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df6d8c57d58267b0b743ab5a665e1bb22e639d8b62cf5f313351ab9b801df56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964ed851e3f6453e95bf96e5458f066bc3c353fcba656f57a831f727b5707ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f720f9f85b8dd685a37ffee68cc02a58b2e629b921bef2a9dec3e12fbab0c93(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network_watcher_id: builtins.str,
    storage_location: typing.Union[VirtualMachineScaleSetPacketCaptureStorageLocation, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_scale_set_id: builtins.str,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineScaleSetPacketCaptureFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    machine_scope: typing.Optional[typing.Union[VirtualMachineScaleSetPacketCaptureMachineScope, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
    maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
    maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[VirtualMachineScaleSetPacketCaptureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb707ca933cf3b5774511220e8e8caab2711671def449a18c20ef06a43e7db28(
    *,
    protocol: builtins.str,
    local_ip_address: typing.Optional[builtins.str] = None,
    local_port: typing.Optional[builtins.str] = None,
    remote_ip_address: typing.Optional[builtins.str] = None,
    remote_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd23a1d8f008d469269cd58592eb0ea9e9b259ac97927a8b5de17823c3126a2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782c54b3e94cd945da51d6059ca2c85899a4223cb95ec7f55a041e2e4c86abe0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb74e00f0beaec215cfdde3f11962eae8c215e3186fdf2997b004766ee125b6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856b196f97ae3f5a15aa450323709b74f12ff27b97add2a15b1c5fc0065bd5bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed823a27bf822daa204d937b2ebfab54d695b4d7c094ff40c3902c9de58b25d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af583d9a6ce7a656033797d14b4ad164bcc336ed16de9358104d1ebdee4d5b8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineScaleSetPacketCaptureFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf782da0e90234d810979ce99390b5990bb8dc3a99b36bf44010ef25756e7586(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b9d91c0c8ef9afd19d00b6d60ddea97947915126323a26bbaee8f2e80654fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744869b7d7d13081d8a7c42d7f5748e3a272e70db32cf1032c8bdc420bd36c81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2da3d76153923d88153acd425b1029c2bc55e4302086ee95f5875f390beb00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0545ec63b0d34a434542fe5035a5eee71fe45d186956f8423487f2fd7c0968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b1e4661b2b868433adad21dcb89fa5725f8f3d3158241d387f924cb4a8b2b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11008ba4609d205a73436987ed318493a05fa187a07e9177db0518a45374362f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58df8939a44b7ee1d8470b8213a6ce8b5c6e0e9774ae106630a048572822a64(
    *,
    exclude_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efa7a3a77ee98a9981ba55ea7b72aad28d242596b4d37be994a5fe493f2400a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218fdb954c8d68b79308fac443f53ee5fbd1779e0263af2e07921aa67a9c9b96(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52c494b2203796bfa2d43d14e653aff5af77750ebb7ed1babd658155d611691(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b8336579cb8f9f1802d5754cdf56dd91edf4ebca91dc2b27f33c9aad7fcafd(
    value: typing.Optional[VirtualMachineScaleSetPacketCaptureMachineScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c60bd32e1ef519d761cf30b5cc257c069c46e96d75c4c593c8713314941fc4(
    *,
    file_path: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfe711e3f673180dba5dbb339627319eb32bfc566b7f51ff7e415dd06dea300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef96c39db426f4af398c0f4a69acede22f7186243b00ac2e7bbd6032194196e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d304d5ff98c6482879b6b39357006c985b010950f2437fad6681429b6d6b597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef6f33484a35c4a38f22c91cdd079fc3f8e8c7ca90b5f9f6af90c56b4899ada(
    value: typing.Optional[VirtualMachineScaleSetPacketCaptureStorageLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b80b16079f98e97696656c1ed37c500bf118ae1674755fded5141b2c8e7bbd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb07737d0beb7e4b70f7115001f93782b9bb3afed71fa098807cf2d637cd1769(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31104aea26bd040cddf4a4728aca13b260097995bf211caa0edb405a895b12d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4252e8e82c864c8a8cd3ad354482120ec0a3f24895afb52a4d7167d2853913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7abeda1ab34bd6bad9f5fe65288a22fc04a6ca58cea39ae325bdc12a7ed6301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895852264a0a411782472321fe62c7554c0bdc16d0a83c5f9b4a99d718b9fa67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachineScaleSetPacketCaptureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
