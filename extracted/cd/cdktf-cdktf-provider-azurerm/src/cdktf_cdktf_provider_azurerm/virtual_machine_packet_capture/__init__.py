r'''
# `azurerm_virtual_machine_packet_capture`

Refer to the Terraform Registry for docs: [`azurerm_virtual_machine_packet_capture`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture).
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


class VirtualMachinePacketCapture(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCapture",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture azurerm_virtual_machine_packet_capture}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network_watcher_id: builtins.str,
        storage_location: typing.Union["VirtualMachinePacketCaptureStorageLocation", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_id: builtins.str,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachinePacketCaptureFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
        maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
        maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["VirtualMachinePacketCaptureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture azurerm_virtual_machine_packet_capture} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#name VirtualMachinePacketCapture#name}.
        :param network_watcher_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#network_watcher_id VirtualMachinePacketCapture#network_watcher_id}.
        :param storage_location: storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#storage_location VirtualMachinePacketCapture#storage_location}
        :param virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#virtual_machine_id VirtualMachinePacketCapture#virtual_machine_id}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#filter VirtualMachinePacketCapture#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#id VirtualMachinePacketCapture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_bytes_per_packet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_bytes_per_packet VirtualMachinePacketCapture#maximum_bytes_per_packet}.
        :param maximum_bytes_per_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_bytes_per_session VirtualMachinePacketCapture#maximum_bytes_per_session}.
        :param maximum_capture_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_capture_duration_in_seconds VirtualMachinePacketCapture#maximum_capture_duration_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#timeouts VirtualMachinePacketCapture#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee703cf7c436b049fa60b537cd9f683ac96b9b53c76bf69505bd567fa4030ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualMachinePacketCaptureConfig(
            name=name,
            network_watcher_id=network_watcher_id,
            storage_location=storage_location,
            virtual_machine_id=virtual_machine_id,
            filter=filter,
            id=id,
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
        '''Generates CDKTF code for importing a VirtualMachinePacketCapture resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VirtualMachinePacketCapture to import.
        :param import_from_id: The id of the existing VirtualMachinePacketCapture that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VirtualMachinePacketCapture to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b562a090c5f7f512af01c7befb2bfdb6a45effba18356041df112f7758262e7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachinePacketCaptureFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cd9c9b9dcdb49fa2cf5642193c388c1858a6872f5e5b2a4aef86168402d45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putStorageLocation")
    def put_storage_location(
        self,
        *,
        file_path: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#file_path VirtualMachinePacketCapture#file_path}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#storage_account_id VirtualMachinePacketCapture#storage_account_id}.
        '''
        value = VirtualMachinePacketCaptureStorageLocation(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#create VirtualMachinePacketCapture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#delete VirtualMachinePacketCapture#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#read VirtualMachinePacketCapture#read}.
        '''
        value = VirtualMachinePacketCaptureTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    def filter(self) -> "VirtualMachinePacketCaptureFilterList":
        return typing.cast("VirtualMachinePacketCaptureFilterList", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="storageLocation")
    def storage_location(
        self,
    ) -> "VirtualMachinePacketCaptureStorageLocationOutputReference":
        return typing.cast("VirtualMachinePacketCaptureStorageLocationOutputReference", jsii.get(self, "storageLocation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualMachinePacketCaptureTimeoutsOutputReference":
        return typing.cast("VirtualMachinePacketCaptureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePacketCaptureFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePacketCaptureFilter"]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    ) -> typing.Optional["VirtualMachinePacketCaptureStorageLocation"]:
        return typing.cast(typing.Optional["VirtualMachinePacketCaptureStorageLocation"], jsii.get(self, "storageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualMachinePacketCaptureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualMachinePacketCaptureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineIdInput")
    def virtual_machine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db4f115218bc6b148e6254a1034122dd43b6e749cfe72f94a1263dc06495827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBytesPerPacket")
    def maximum_bytes_per_packet(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBytesPerPacket"))

    @maximum_bytes_per_packet.setter
    def maximum_bytes_per_packet(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838cb80edd1d68f6eb86c2d63c605a4b5a0f34fc9c3b2a99c6a7e8f7273c9392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBytesPerPacket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumBytesPerSession")
    def maximum_bytes_per_session(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumBytesPerSession"))

    @maximum_bytes_per_session.setter
    def maximum_bytes_per_session(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b00388acf9c4e2a7a2cc8e604809b93dcdb544ead6536661079c4daa79683f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumBytesPerSession", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumCaptureDurationInSeconds")
    def maximum_capture_duration_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumCaptureDurationInSeconds"))

    @maximum_capture_duration_in_seconds.setter
    def maximum_capture_duration_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae9bea84a19be21fca63115c2d673c923824df48e4a7ac8c63ab1216b030cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumCaptureDurationInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce98f7dd107283934466764caf72c588215aa5fcfe31fcccb9d11e22e9026a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkWatcherId")
    def network_watcher_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkWatcherId"))

    @network_watcher_id.setter
    def network_watcher_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c701557d596b97a88f09c68527b12871068971a4dce09b50cebeedc50c400ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkWatcherId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineId")
    def virtual_machine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineId"))

    @virtual_machine_id.setter
    def virtual_machine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc66460941e9b18608a6c6b8195c75ec929fc24fee8c1da778356ed53ce625e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureConfig",
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
        "virtual_machine_id": "virtualMachineId",
        "filter": "filter",
        "id": "id",
        "maximum_bytes_per_packet": "maximumBytesPerPacket",
        "maximum_bytes_per_session": "maximumBytesPerSession",
        "maximum_capture_duration_in_seconds": "maximumCaptureDurationInSeconds",
        "timeouts": "timeouts",
    },
)
class VirtualMachinePacketCaptureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        storage_location: typing.Union["VirtualMachinePacketCaptureStorageLocation", typing.Dict[builtins.str, typing.Any]],
        virtual_machine_id: builtins.str,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachinePacketCaptureFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
        maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
        maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["VirtualMachinePacketCaptureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#name VirtualMachinePacketCapture#name}.
        :param network_watcher_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#network_watcher_id VirtualMachinePacketCapture#network_watcher_id}.
        :param storage_location: storage_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#storage_location VirtualMachinePacketCapture#storage_location}
        :param virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#virtual_machine_id VirtualMachinePacketCapture#virtual_machine_id}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#filter VirtualMachinePacketCapture#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#id VirtualMachinePacketCapture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_bytes_per_packet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_bytes_per_packet VirtualMachinePacketCapture#maximum_bytes_per_packet}.
        :param maximum_bytes_per_session: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_bytes_per_session VirtualMachinePacketCapture#maximum_bytes_per_session}.
        :param maximum_capture_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_capture_duration_in_seconds VirtualMachinePacketCapture#maximum_capture_duration_in_seconds}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#timeouts VirtualMachinePacketCapture#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(storage_location, dict):
            storage_location = VirtualMachinePacketCaptureStorageLocation(**storage_location)
        if isinstance(timeouts, dict):
            timeouts = VirtualMachinePacketCaptureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85950485412f46a0f0c799aaac4806ec43a81af1b067495444313071e8e6721)
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
            check_type(argname="argument virtual_machine_id", value=virtual_machine_id, expected_type=type_hints["virtual_machine_id"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maximum_bytes_per_packet", value=maximum_bytes_per_packet, expected_type=type_hints["maximum_bytes_per_packet"])
            check_type(argname="argument maximum_bytes_per_session", value=maximum_bytes_per_session, expected_type=type_hints["maximum_bytes_per_session"])
            check_type(argname="argument maximum_capture_duration_in_seconds", value=maximum_capture_duration_in_seconds, expected_type=type_hints["maximum_capture_duration_in_seconds"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network_watcher_id": network_watcher_id,
            "storage_location": storage_location,
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
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#name VirtualMachinePacketCapture#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_watcher_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#network_watcher_id VirtualMachinePacketCapture#network_watcher_id}.'''
        result = self._values.get("network_watcher_id")
        assert result is not None, "Required property 'network_watcher_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_location(self) -> "VirtualMachinePacketCaptureStorageLocation":
        '''storage_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#storage_location VirtualMachinePacketCapture#storage_location}
        '''
        result = self._values.get("storage_location")
        assert result is not None, "Required property 'storage_location' is missing"
        return typing.cast("VirtualMachinePacketCaptureStorageLocation", result)

    @builtins.property
    def virtual_machine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#virtual_machine_id VirtualMachinePacketCapture#virtual_machine_id}.'''
        result = self._values.get("virtual_machine_id")
        assert result is not None, "Required property 'virtual_machine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePacketCaptureFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#filter VirtualMachinePacketCapture#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePacketCaptureFilter"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#id VirtualMachinePacketCapture#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_bytes_per_packet(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_bytes_per_packet VirtualMachinePacketCapture#maximum_bytes_per_packet}.'''
        result = self._values.get("maximum_bytes_per_packet")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_bytes_per_session(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_bytes_per_session VirtualMachinePacketCapture#maximum_bytes_per_session}.'''
        result = self._values.get("maximum_bytes_per_session")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_capture_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#maximum_capture_duration_in_seconds VirtualMachinePacketCapture#maximum_capture_duration_in_seconds}.'''
        result = self._values.get("maximum_capture_duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VirtualMachinePacketCaptureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#timeouts VirtualMachinePacketCapture#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VirtualMachinePacketCaptureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachinePacketCaptureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureFilter",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "local_ip_address": "localIpAddress",
        "local_port": "localPort",
        "remote_ip_address": "remoteIpAddress",
        "remote_port": "remotePort",
    },
)
class VirtualMachinePacketCaptureFilter:
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
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#protocol VirtualMachinePacketCapture#protocol}.
        :param local_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#local_ip_address VirtualMachinePacketCapture#local_ip_address}.
        :param local_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#local_port VirtualMachinePacketCapture#local_port}.
        :param remote_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#remote_ip_address VirtualMachinePacketCapture#remote_ip_address}.
        :param remote_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#remote_port VirtualMachinePacketCapture#remote_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2af509e40aaf1dff2df5cd415544fff850347b5dbf3bad3cd7647acb871935d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#protocol VirtualMachinePacketCapture#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#local_ip_address VirtualMachinePacketCapture#local_ip_address}.'''
        result = self._values.get("local_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#local_port VirtualMachinePacketCapture#local_port}.'''
        result = self._values.get("local_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#remote_ip_address VirtualMachinePacketCapture#remote_ip_address}.'''
        result = self._values.get("remote_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#remote_port VirtualMachinePacketCapture#remote_port}.'''
        result = self._values.get("remote_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachinePacketCaptureFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachinePacketCaptureFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__318c6f91feae95241bed914cc5d882ecb0aeb9ac495fc196ac80102021f78d17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachinePacketCaptureFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a10b4080fdd60515e0eb0e69fc4341b26aef8eef9a86048f6e1d1e64e620e2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachinePacketCaptureFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174cbbf273652307646ec6410fba3872a4525d2a8af3d141fe0169dd48484931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f309a44557e3abf95b54fc478fcf680ae6863a9429813f00a675dc212e69a9d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__960fd57594361e03d9c4092d93772fa6643241d67180f6ef31c9a6e95d6cd860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePacketCaptureFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePacketCaptureFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePacketCaptureFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5eed7e547e4227d79f3173e70ceb840f44cbc0757f671cc1837b26ceac24abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualMachinePacketCaptureFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a940ea4a960b4826c4c82dbb6c8448eaa1a8753c48601c1da6fb00dc329084b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__291e413aaac713159afaeb16c0d41b8bbb374d07ae1819c17be5001886807fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPort")
    def local_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPort"))

    @local_port.setter
    def local_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5cb3dc8b1e36708b7903dde947bc404d78a1970130c47238519d86fe1f04d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc9c80dad32834d2aad36cc0061f56548e6322a5df3f78371343cee0b016f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteIpAddress")
    def remote_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteIpAddress"))

    @remote_ip_address.setter
    def remote_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda5653b5a6bdb2ba0f6f3cc63ad247825ef2480af38f918dde4cc7c762b06c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remotePort")
    def remote_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remotePort"))

    @remote_port.setter
    def remote_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6940e02df979adfc4f6bc153adda15be855fd3f7f272c30885aeee9a7ccdcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remotePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6c102f68d33d9283396cb32697d1d1d4d6a3411a18f823932ffcec1b78b380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureStorageLocation",
    jsii_struct_bases=[],
    name_mapping={"file_path": "filePath", "storage_account_id": "storageAccountId"},
)
class VirtualMachinePacketCaptureStorageLocation:
    def __init__(
        self,
        *,
        file_path: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#file_path VirtualMachinePacketCapture#file_path}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#storage_account_id VirtualMachinePacketCapture#storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba54e658169ecb71332db4f8296a5682b887999f09158e81dc15ab3eb700bdf2)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_path is not None:
            self._values["file_path"] = file_path
        if storage_account_id is not None:
            self._values["storage_account_id"] = storage_account_id

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#file_path VirtualMachinePacketCapture#file_path}.'''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#storage_account_id VirtualMachinePacketCapture#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachinePacketCaptureStorageLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachinePacketCaptureStorageLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureStorageLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bea643022e29bc7b9ce2b9179530850bfeff08eea43014523fb835bdd819a8f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a419da0cab311a64b840a663cf5c915b7d935499be8213996fa96eb2690cdf45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ffc73484c92e5384691eca4ab55b56cde0a7f866bea10805d63a068e8c7a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualMachinePacketCaptureStorageLocation]:
        return typing.cast(typing.Optional[VirtualMachinePacketCaptureStorageLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachinePacketCaptureStorageLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec74b75f67a5a342ddbee3de485f12ddd7ec0446e64e96c51b94a5544fadeb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class VirtualMachinePacketCaptureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#create VirtualMachinePacketCapture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#delete VirtualMachinePacketCapture#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#read VirtualMachinePacketCapture#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37666b57c2eb65b06f9ce90e26bfae95a3b57c3c6e37d844651134c723fdeccb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#create VirtualMachinePacketCapture#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#delete VirtualMachinePacketCapture#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_machine_packet_capture#read VirtualMachinePacketCapture#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachinePacketCaptureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachinePacketCaptureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualMachinePacketCapture.VirtualMachinePacketCaptureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9784138fdc0f353dcd9a1cb9eb846eee6c2a898ad612a181b24adbc0683c09f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1825d4eed2a4d4630236e6e0e474afdd48f3c3e318359ed77142e5a6b64f8cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65edfbda2fe73b06c20db00c65235d95254d51835623c935f97e7f99f3e17422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7240bc3e0a4c5e483f97f932a6d93a9105668cb21c08c35c4afb27d4fa743c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148496fb40af7f4e3fd1a02f38258a088839c80f37305ee22ab265799a7bf7ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VirtualMachinePacketCapture",
    "VirtualMachinePacketCaptureConfig",
    "VirtualMachinePacketCaptureFilter",
    "VirtualMachinePacketCaptureFilterList",
    "VirtualMachinePacketCaptureFilterOutputReference",
    "VirtualMachinePacketCaptureStorageLocation",
    "VirtualMachinePacketCaptureStorageLocationOutputReference",
    "VirtualMachinePacketCaptureTimeouts",
    "VirtualMachinePacketCaptureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dee703cf7c436b049fa60b537cd9f683ac96b9b53c76bf69505bd567fa4030ad(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network_watcher_id: builtins.str,
    storage_location: typing.Union[VirtualMachinePacketCaptureStorageLocation, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_id: builtins.str,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachinePacketCaptureFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
    maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
    maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[VirtualMachinePacketCaptureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b562a090c5f7f512af01c7befb2bfdb6a45effba18356041df112f7758262e7a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cd9c9b9dcdb49fa2cf5642193c388c1858a6872f5e5b2a4aef86168402d45d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachinePacketCaptureFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db4f115218bc6b148e6254a1034122dd43b6e749cfe72f94a1263dc06495827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838cb80edd1d68f6eb86c2d63c605a4b5a0f34fc9c3b2a99c6a7e8f7273c9392(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b00388acf9c4e2a7a2cc8e604809b93dcdb544ead6536661079c4daa79683f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae9bea84a19be21fca63115c2d673c923824df48e4a7ac8c63ab1216b030cc1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce98f7dd107283934466764caf72c588215aa5fcfe31fcccb9d11e22e9026a5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c701557d596b97a88f09c68527b12871068971a4dce09b50cebeedc50c400ef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc66460941e9b18608a6c6b8195c75ec929fc24fee8c1da778356ed53ce625e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85950485412f46a0f0c799aaac4806ec43a81af1b067495444313071e8e6721(
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
    storage_location: typing.Union[VirtualMachinePacketCaptureStorageLocation, typing.Dict[builtins.str, typing.Any]],
    virtual_machine_id: builtins.str,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachinePacketCaptureFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    maximum_bytes_per_packet: typing.Optional[jsii.Number] = None,
    maximum_bytes_per_session: typing.Optional[jsii.Number] = None,
    maximum_capture_duration_in_seconds: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[VirtualMachinePacketCaptureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2af509e40aaf1dff2df5cd415544fff850347b5dbf3bad3cd7647acb871935d(
    *,
    protocol: builtins.str,
    local_ip_address: typing.Optional[builtins.str] = None,
    local_port: typing.Optional[builtins.str] = None,
    remote_ip_address: typing.Optional[builtins.str] = None,
    remote_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318c6f91feae95241bed914cc5d882ecb0aeb9ac495fc196ac80102021f78d17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a10b4080fdd60515e0eb0e69fc4341b26aef8eef9a86048f6e1d1e64e620e2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174cbbf273652307646ec6410fba3872a4525d2a8af3d141fe0169dd48484931(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f309a44557e3abf95b54fc478fcf680ae6863a9429813f00a675dc212e69a9d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960fd57594361e03d9c4092d93772fa6643241d67180f6ef31c9a6e95d6cd860(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5eed7e547e4227d79f3173e70ceb840f44cbc0757f671cc1837b26ceac24abb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePacketCaptureFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a940ea4a960b4826c4c82dbb6c8448eaa1a8753c48601c1da6fb00dc329084b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291e413aaac713159afaeb16c0d41b8bbb374d07ae1819c17be5001886807fae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cb3dc8b1e36708b7903dde947bc404d78a1970130c47238519d86fe1f04d44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc9c80dad32834d2aad36cc0061f56548e6322a5df3f78371343cee0b016f3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda5653b5a6bdb2ba0f6f3cc63ad247825ef2480af38f918dde4cc7c762b06c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6940e02df979adfc4f6bc153adda15be855fd3f7f272c30885aeee9a7ccdcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6c102f68d33d9283396cb32697d1d1d4d6a3411a18f823932ffcec1b78b380(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba54e658169ecb71332db4f8296a5682b887999f09158e81dc15ab3eb700bdf2(
    *,
    file_path: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea643022e29bc7b9ce2b9179530850bfeff08eea43014523fb835bdd819a8f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a419da0cab311a64b840a663cf5c915b7d935499be8213996fa96eb2690cdf45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ffc73484c92e5384691eca4ab55b56cde0a7f866bea10805d63a068e8c7a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec74b75f67a5a342ddbee3de485f12ddd7ec0446e64e96c51b94a5544fadeb7(
    value: typing.Optional[VirtualMachinePacketCaptureStorageLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37666b57c2eb65b06f9ce90e26bfae95a3b57c3c6e37d844651134c723fdeccb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9784138fdc0f353dcd9a1cb9eb846eee6c2a898ad612a181b24adbc0683c09f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1825d4eed2a4d4630236e6e0e474afdd48f3c3e318359ed77142e5a6b64f8cca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65edfbda2fe73b06c20db00c65235d95254d51835623c935f97e7f99f3e17422(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7240bc3e0a4c5e483f97f932a6d93a9105668cb21c08c35c4afb27d4fa743c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148496fb40af7f4e3fd1a02f38258a088839c80f37305ee22ab265799a7bf7ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualMachinePacketCaptureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
