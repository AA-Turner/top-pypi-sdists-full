r'''
# `azurerm_stack_hci_virtual_hard_disk`

Refer to the Terraform Registry for docs: [`azurerm_stack_hci_virtual_hard_disk`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk).
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


class StackHciVirtualHardDisk(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciVirtualHardDisk.StackHciVirtualHardDisk",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk azurerm_stack_hci_virtual_hard_disk}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        custom_location_id: builtins.str,
        disk_size_in_gb: jsii.Number,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        block_size_in_bytes: typing.Optional[jsii.Number] = None,
        disk_file_format: typing.Optional[builtins.str] = None,
        dynamic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hyperv_generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logical_sector_in_bytes: typing.Optional[jsii.Number] = None,
        physical_sector_in_bytes: typing.Optional[jsii.Number] = None,
        storage_path_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["StackHciVirtualHardDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk azurerm_stack_hci_virtual_hard_disk} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param custom_location_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#custom_location_id StackHciVirtualHardDisk#custom_location_id}.
        :param disk_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#disk_size_in_gb StackHciVirtualHardDisk#disk_size_in_gb}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#location StackHciVirtualHardDisk#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#name StackHciVirtualHardDisk#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#resource_group_name StackHciVirtualHardDisk#resource_group_name}.
        :param block_size_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#block_size_in_bytes StackHciVirtualHardDisk#block_size_in_bytes}.
        :param disk_file_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#disk_file_format StackHciVirtualHardDisk#disk_file_format}.
        :param dynamic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#dynamic_enabled StackHciVirtualHardDisk#dynamic_enabled}.
        :param hyperv_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#hyperv_generation StackHciVirtualHardDisk#hyperv_generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#id StackHciVirtualHardDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logical_sector_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#logical_sector_in_bytes StackHciVirtualHardDisk#logical_sector_in_bytes}.
        :param physical_sector_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#physical_sector_in_bytes StackHciVirtualHardDisk#physical_sector_in_bytes}.
        :param storage_path_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#storage_path_id StackHciVirtualHardDisk#storage_path_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#tags StackHciVirtualHardDisk#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#timeouts StackHciVirtualHardDisk#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747e55557ea7d27e0a8b683ad7d1e5c697ff59194dcc539c87fb74b92cfab401)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StackHciVirtualHardDiskConfig(
            custom_location_id=custom_location_id,
            disk_size_in_gb=disk_size_in_gb,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            block_size_in_bytes=block_size_in_bytes,
            disk_file_format=disk_file_format,
            dynamic_enabled=dynamic_enabled,
            hyperv_generation=hyperv_generation,
            id=id,
            logical_sector_in_bytes=logical_sector_in_bytes,
            physical_sector_in_bytes=physical_sector_in_bytes,
            storage_path_id=storage_path_id,
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
        '''Generates CDKTF code for importing a StackHciVirtualHardDisk resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StackHciVirtualHardDisk to import.
        :param import_from_id: The id of the existing StackHciVirtualHardDisk that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StackHciVirtualHardDisk to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b192427e072744b448ef7cfa785ec7eb402b53c95b0b5ac15d688a336019dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#create StackHciVirtualHardDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#delete StackHciVirtualHardDisk#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#read StackHciVirtualHardDisk#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#update StackHciVirtualHardDisk#update}.
        '''
        value = StackHciVirtualHardDiskTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBlockSizeInBytes")
    def reset_block_size_in_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockSizeInBytes", []))

    @jsii.member(jsii_name="resetDiskFileFormat")
    def reset_disk_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskFileFormat", []))

    @jsii.member(jsii_name="resetDynamicEnabled")
    def reset_dynamic_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicEnabled", []))

    @jsii.member(jsii_name="resetHypervGeneration")
    def reset_hyperv_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHypervGeneration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogicalSectorInBytes")
    def reset_logical_sector_in_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicalSectorInBytes", []))

    @jsii.member(jsii_name="resetPhysicalSectorInBytes")
    def reset_physical_sector_in_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalSectorInBytes", []))

    @jsii.member(jsii_name="resetStoragePathId")
    def reset_storage_path_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoragePathId", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StackHciVirtualHardDiskTimeoutsOutputReference":
        return typing.cast("StackHciVirtualHardDiskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="blockSizeInBytesInput")
    def block_size_in_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "blockSizeInBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="customLocationIdInput")
    def custom_location_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customLocationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskFileFormatInput")
    def disk_file_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskFileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeInGbInput")
    def disk_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicEnabledInput")
    def dynamic_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dynamicEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hypervGenerationInput")
    def hyperv_generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hypervGenerationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalSectorInBytesInput")
    def logical_sector_in_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logicalSectorInBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalSectorInBytesInput")
    def physical_sector_in_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "physicalSectorInBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePathIdInput")
    def storage_path_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePathIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StackHciVirtualHardDiskTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StackHciVirtualHardDiskTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="blockSizeInBytes")
    def block_size_in_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "blockSizeInBytes"))

    @block_size_in_bytes.setter
    def block_size_in_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4d63b315e1d8fa8e0b0860e66afd041847d04de2ed1bdd8e9b8ebf87f01a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockSizeInBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customLocationId")
    def custom_location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLocationId"))

    @custom_location_id.setter
    def custom_location_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9ab303ab3e652ebc383084bb924b2e7356fddaeff51461fbeffaabede2bf01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLocationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskFileFormat")
    def disk_file_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskFileFormat"))

    @disk_file_format.setter
    def disk_file_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f689c8450dab962febc480eba7ebae8dc75a47986b0ddc9171c246661368ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskFileFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeInGb")
    def disk_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeInGb"))

    @disk_size_in_gb.setter
    def disk_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ce2eb4810678b6d4f1f606cdb5f71c14bf98905adaf1e64ef08c55c832fa76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynamicEnabled")
    def dynamic_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dynamicEnabled"))

    @dynamic_enabled.setter
    def dynamic_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed26b31b1be452bb3feebf56101cb584f7af1bf9931a13616e729f593ed18e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hypervGeneration")
    def hyperv_generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hypervGeneration"))

    @hyperv_generation.setter
    def hyperv_generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102cf51964cbad41fda22c9b9c3ba9fc843bcc872e4be65fde25614869e6e43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hypervGeneration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46465f0a257d3ccc2efc6e8aae236f2e6b1d4ffbe6f02ddcd4911e957c4762b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b22b4c29526944f16df610c826f6d67d0769c7bcff12f4632b56fb8fd1ccdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicalSectorInBytes")
    def logical_sector_in_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logicalSectorInBytes"))

    @logical_sector_in_bytes.setter
    def logical_sector_in_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5519ca9f1310da6ce6008bf6717f840f1b46d526cf487811791fb19cf637d8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicalSectorInBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46cfaeefb4c76fd4b2fdd2e722cf04111d9a1ad2f39d4edf010206fc4da2b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="physicalSectorInBytes")
    def physical_sector_in_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "physicalSectorInBytes"))

    @physical_sector_in_bytes.setter
    def physical_sector_in_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a387694f34c652d4b7be01353a291d3f2ae0ddff376de691aaab475ff5712b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalSectorInBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bb0d43aecd35c87d9e4c137ed7372ee5be6a4efee73c9160229da4f59ec438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePathId")
    def storage_path_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePathId"))

    @storage_path_id.setter
    def storage_path_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09498b7942cdb16cd29d3c8b26d1735cb6c44245af7ad8f0e8ef4a65feaa8185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePathId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7b566170bcad8b7def39773f55b76a0ba29d4fef82a43b02082206859dda58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciVirtualHardDisk.StackHciVirtualHardDiskConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "custom_location_id": "customLocationId",
        "disk_size_in_gb": "diskSizeInGb",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "block_size_in_bytes": "blockSizeInBytes",
        "disk_file_format": "diskFileFormat",
        "dynamic_enabled": "dynamicEnabled",
        "hyperv_generation": "hypervGeneration",
        "id": "id",
        "logical_sector_in_bytes": "logicalSectorInBytes",
        "physical_sector_in_bytes": "physicalSectorInBytes",
        "storage_path_id": "storagePathId",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class StackHciVirtualHardDiskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_location_id: builtins.str,
        disk_size_in_gb: jsii.Number,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        block_size_in_bytes: typing.Optional[jsii.Number] = None,
        disk_file_format: typing.Optional[builtins.str] = None,
        dynamic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hyperv_generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logical_sector_in_bytes: typing.Optional[jsii.Number] = None,
        physical_sector_in_bytes: typing.Optional[jsii.Number] = None,
        storage_path_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["StackHciVirtualHardDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param custom_location_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#custom_location_id StackHciVirtualHardDisk#custom_location_id}.
        :param disk_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#disk_size_in_gb StackHciVirtualHardDisk#disk_size_in_gb}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#location StackHciVirtualHardDisk#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#name StackHciVirtualHardDisk#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#resource_group_name StackHciVirtualHardDisk#resource_group_name}.
        :param block_size_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#block_size_in_bytes StackHciVirtualHardDisk#block_size_in_bytes}.
        :param disk_file_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#disk_file_format StackHciVirtualHardDisk#disk_file_format}.
        :param dynamic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#dynamic_enabled StackHciVirtualHardDisk#dynamic_enabled}.
        :param hyperv_generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#hyperv_generation StackHciVirtualHardDisk#hyperv_generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#id StackHciVirtualHardDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logical_sector_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#logical_sector_in_bytes StackHciVirtualHardDisk#logical_sector_in_bytes}.
        :param physical_sector_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#physical_sector_in_bytes StackHciVirtualHardDisk#physical_sector_in_bytes}.
        :param storage_path_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#storage_path_id StackHciVirtualHardDisk#storage_path_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#tags StackHciVirtualHardDisk#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#timeouts StackHciVirtualHardDisk#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = StackHciVirtualHardDiskTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbea98b515760e7ec33a302daaf88a1971da45f58cb419fc25352f3ab0ed991)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument custom_location_id", value=custom_location_id, expected_type=type_hints["custom_location_id"])
            check_type(argname="argument disk_size_in_gb", value=disk_size_in_gb, expected_type=type_hints["disk_size_in_gb"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument block_size_in_bytes", value=block_size_in_bytes, expected_type=type_hints["block_size_in_bytes"])
            check_type(argname="argument disk_file_format", value=disk_file_format, expected_type=type_hints["disk_file_format"])
            check_type(argname="argument dynamic_enabled", value=dynamic_enabled, expected_type=type_hints["dynamic_enabled"])
            check_type(argname="argument hyperv_generation", value=hyperv_generation, expected_type=type_hints["hyperv_generation"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logical_sector_in_bytes", value=logical_sector_in_bytes, expected_type=type_hints["logical_sector_in_bytes"])
            check_type(argname="argument physical_sector_in_bytes", value=physical_sector_in_bytes, expected_type=type_hints["physical_sector_in_bytes"])
            check_type(argname="argument storage_path_id", value=storage_path_id, expected_type=type_hints["storage_path_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_location_id": custom_location_id,
            "disk_size_in_gb": disk_size_in_gb,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if block_size_in_bytes is not None:
            self._values["block_size_in_bytes"] = block_size_in_bytes
        if disk_file_format is not None:
            self._values["disk_file_format"] = disk_file_format
        if dynamic_enabled is not None:
            self._values["dynamic_enabled"] = dynamic_enabled
        if hyperv_generation is not None:
            self._values["hyperv_generation"] = hyperv_generation
        if id is not None:
            self._values["id"] = id
        if logical_sector_in_bytes is not None:
            self._values["logical_sector_in_bytes"] = logical_sector_in_bytes
        if physical_sector_in_bytes is not None:
            self._values["physical_sector_in_bytes"] = physical_sector_in_bytes
        if storage_path_id is not None:
            self._values["storage_path_id"] = storage_path_id
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
    def custom_location_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#custom_location_id StackHciVirtualHardDisk#custom_location_id}.'''
        result = self._values.get("custom_location_id")
        assert result is not None, "Required property 'custom_location_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_size_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#disk_size_in_gb StackHciVirtualHardDisk#disk_size_in_gb}.'''
        result = self._values.get("disk_size_in_gb")
        assert result is not None, "Required property 'disk_size_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#location StackHciVirtualHardDisk#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#name StackHciVirtualHardDisk#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#resource_group_name StackHciVirtualHardDisk#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_size_in_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#block_size_in_bytes StackHciVirtualHardDisk#block_size_in_bytes}.'''
        result = self._values.get("block_size_in_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_file_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#disk_file_format StackHciVirtualHardDisk#disk_file_format}.'''
        result = self._values.get("disk_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamic_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#dynamic_enabled StackHciVirtualHardDisk#dynamic_enabled}.'''
        result = self._values.get("dynamic_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hyperv_generation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#hyperv_generation StackHciVirtualHardDisk#hyperv_generation}.'''
        result = self._values.get("hyperv_generation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#id StackHciVirtualHardDisk#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logical_sector_in_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#logical_sector_in_bytes StackHciVirtualHardDisk#logical_sector_in_bytes}.'''
        result = self._values.get("logical_sector_in_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def physical_sector_in_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#physical_sector_in_bytes StackHciVirtualHardDisk#physical_sector_in_bytes}.'''
        result = self._values.get("physical_sector_in_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_path_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#storage_path_id StackHciVirtualHardDisk#storage_path_id}.'''
        result = self._values.get("storage_path_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#tags StackHciVirtualHardDisk#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StackHciVirtualHardDiskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#timeouts StackHciVirtualHardDisk#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StackHciVirtualHardDiskTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciVirtualHardDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciVirtualHardDisk.StackHciVirtualHardDiskTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class StackHciVirtualHardDiskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#create StackHciVirtualHardDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#delete StackHciVirtualHardDisk#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#read StackHciVirtualHardDisk#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#update StackHciVirtualHardDisk#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c0bc801ee122d1cac2bc047e7315e0c7f4f15b656a4d48bb750f75aa03087d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#create StackHciVirtualHardDisk#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#delete StackHciVirtualHardDisk#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#read StackHciVirtualHardDisk#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_virtual_hard_disk#update StackHciVirtualHardDisk#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciVirtualHardDiskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciVirtualHardDiskTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciVirtualHardDisk.StackHciVirtualHardDiskTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b56551c2b5ebb54c20f3e18e90f134a667b07a8698818aadfecca630370ffd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__470e7fc61b9395105743a324a9b69f6ab5065467edc3978e92a549e761232abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67095b14da6d7add3f1636029ee54f36d1a8dfe59d2b7ab7f71cdc4d83bf0a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589bc85ad79af6ca5bbffb6272ad4c9dff7d7333c1f6fac52a48e84479934ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b7222a8516541e96697e1785f0cda762543eb2be36b8b59b896ef118dcf922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciVirtualHardDiskTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciVirtualHardDiskTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciVirtualHardDiskTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9b22d395f479f05c7935b5a3781691e93dbe43d77bd7fecb3400f39cfc099d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StackHciVirtualHardDisk",
    "StackHciVirtualHardDiskConfig",
    "StackHciVirtualHardDiskTimeouts",
    "StackHciVirtualHardDiskTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__747e55557ea7d27e0a8b683ad7d1e5c697ff59194dcc539c87fb74b92cfab401(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    custom_location_id: builtins.str,
    disk_size_in_gb: jsii.Number,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    block_size_in_bytes: typing.Optional[jsii.Number] = None,
    disk_file_format: typing.Optional[builtins.str] = None,
    dynamic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hyperv_generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logical_sector_in_bytes: typing.Optional[jsii.Number] = None,
    physical_sector_in_bytes: typing.Optional[jsii.Number] = None,
    storage_path_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[StackHciVirtualHardDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__63b192427e072744b448ef7cfa785ec7eb402b53c95b0b5ac15d688a336019dd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4d63b315e1d8fa8e0b0860e66afd041847d04de2ed1bdd8e9b8ebf87f01a23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9ab303ab3e652ebc383084bb924b2e7356fddaeff51461fbeffaabede2bf01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f689c8450dab962febc480eba7ebae8dc75a47986b0ddc9171c246661368ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ce2eb4810678b6d4f1f606cdb5f71c14bf98905adaf1e64ef08c55c832fa76(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed26b31b1be452bb3feebf56101cb584f7af1bf9931a13616e729f593ed18e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102cf51964cbad41fda22c9b9c3ba9fc843bcc872e4be65fde25614869e6e43f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46465f0a257d3ccc2efc6e8aae236f2e6b1d4ffbe6f02ddcd4911e957c4762b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b22b4c29526944f16df610c826f6d67d0769c7bcff12f4632b56fb8fd1ccdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5519ca9f1310da6ce6008bf6717f840f1b46d526cf487811791fb19cf637d8fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46cfaeefb4c76fd4b2fdd2e722cf04111d9a1ad2f39d4edf010206fc4da2b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a387694f34c652d4b7be01353a291d3f2ae0ddff376de691aaab475ff5712b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bb0d43aecd35c87d9e4c137ed7372ee5be6a4efee73c9160229da4f59ec438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09498b7942cdb16cd29d3c8b26d1735cb6c44245af7ad8f0e8ef4a65feaa8185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7b566170bcad8b7def39773f55b76a0ba29d4fef82a43b02082206859dda58(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbea98b515760e7ec33a302daaf88a1971da45f58cb419fc25352f3ab0ed991(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_location_id: builtins.str,
    disk_size_in_gb: jsii.Number,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    block_size_in_bytes: typing.Optional[jsii.Number] = None,
    disk_file_format: typing.Optional[builtins.str] = None,
    dynamic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hyperv_generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logical_sector_in_bytes: typing.Optional[jsii.Number] = None,
    physical_sector_in_bytes: typing.Optional[jsii.Number] = None,
    storage_path_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[StackHciVirtualHardDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c0bc801ee122d1cac2bc047e7315e0c7f4f15b656a4d48bb750f75aa03087d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b56551c2b5ebb54c20f3e18e90f134a667b07a8698818aadfecca630370ffd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470e7fc61b9395105743a324a9b69f6ab5065467edc3978e92a549e761232abb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67095b14da6d7add3f1636029ee54f36d1a8dfe59d2b7ab7f71cdc4d83bf0a47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589bc85ad79af6ca5bbffb6272ad4c9dff7d7333c1f6fac52a48e84479934ac4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b7222a8516541e96697e1785f0cda762543eb2be36b8b59b896ef118dcf922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9b22d395f479f05c7935b5a3781691e93dbe43d77bd7fecb3400f39cfc099d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciVirtualHardDiskTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
