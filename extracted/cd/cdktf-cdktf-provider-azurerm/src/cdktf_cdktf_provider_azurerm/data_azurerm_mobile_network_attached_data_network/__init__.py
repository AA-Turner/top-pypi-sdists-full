r'''
# `data_azurerm_mobile_network_attached_data_network`

Refer to the Terraform Registry for docs: [`data_azurerm_mobile_network_attached_data_network`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network).
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


class DataAzurermMobileNetworkAttachedDataNetwork(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network azurerm_mobile_network_attached_data_network}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        mobile_network_data_network_name: builtins.str,
        mobile_network_packet_core_data_plane_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzurermMobileNetworkAttachedDataNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network azurerm_mobile_network_attached_data_network} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param mobile_network_data_network_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#mobile_network_data_network_name DataAzurermMobileNetworkAttachedDataNetwork#mobile_network_data_network_name}.
        :param mobile_network_packet_core_data_plane_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#mobile_network_packet_core_data_plane_id DataAzurermMobileNetworkAttachedDataNetwork#mobile_network_packet_core_data_plane_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#id DataAzurermMobileNetworkAttachedDataNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#timeouts DataAzurermMobileNetworkAttachedDataNetwork#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32bc4530fa7faeced3c2e0dc7d29cd3928b6c39bfbb5e6f6317feb95591ae962)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAzurermMobileNetworkAttachedDataNetworkConfig(
            mobile_network_data_network_name=mobile_network_data_network_name,
            mobile_network_packet_core_data_plane_id=mobile_network_packet_core_data_plane_id,
            id=id,
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
        '''Generates CDKTF code for importing a DataAzurermMobileNetworkAttachedDataNetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataAzurermMobileNetworkAttachedDataNetwork to import.
        :param import_from_id: The id of the existing DataAzurermMobileNetworkAttachedDataNetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataAzurermMobileNetworkAttachedDataNetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03b09d69509b5cddeb3441a9fc5ca61b8314c8ebe36adf022262ef209fdaadc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#read DataAzurermMobileNetworkAttachedDataNetwork#read}.
        '''
        value = DataAzurermMobileNetworkAttachedDataNetworkTimeouts(read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="dnsAddresses")
    def dns_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsAddresses"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="networkAddressPortTranslation")
    def network_address_port_translation(
        self,
    ) -> "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationList":
        return typing.cast("DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationList", jsii.get(self, "networkAddressPortTranslation"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataAzurermMobileNetworkAttachedDataNetworkTimeoutsOutputReference":
        return typing.cast("DataAzurermMobileNetworkAttachedDataNetworkTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userEquipmentAddressPoolPrefixes")
    def user_equipment_address_pool_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userEquipmentAddressPoolPrefixes"))

    @builtins.property
    @jsii.member(jsii_name="userEquipmentStaticAddressPoolPrefixes")
    def user_equipment_static_address_pool_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userEquipmentStaticAddressPoolPrefixes"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Address")
    def user_plane_access_ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Address"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Gateway")
    def user_plane_access_ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Gateway"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Subnet")
    def user_plane_access_ipv4_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Subnet"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessName")
    def user_plane_access_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessName"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkDataNetworkNameInput")
    def mobile_network_data_network_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobileNetworkDataNetworkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkPacketCoreDataPlaneIdInput")
    def mobile_network_packet_core_data_plane_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobileNetworkPacketCoreDataPlaneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAzurermMobileNetworkAttachedDataNetworkTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAzurermMobileNetworkAttachedDataNetworkTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a5d845c2610b0e761f7f98c79f2ce96330f138689c75d5691a3728f9a7b5ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkDataNetworkName")
    def mobile_network_data_network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkDataNetworkName"))

    @mobile_network_data_network_name.setter
    def mobile_network_data_network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf2739375625e42a5b8dfc3ef1e28e906a3a171794f126fa9d0a88b3649436b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkDataNetworkName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkPacketCoreDataPlaneId")
    def mobile_network_packet_core_data_plane_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkPacketCoreDataPlaneId"))

    @mobile_network_packet_core_data_plane_id.setter
    def mobile_network_packet_core_data_plane_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f10875ed08945a3f301eb21018e32f60a6244a3cfd5f41d062de275155175c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkPacketCoreDataPlaneId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "mobile_network_data_network_name": "mobileNetworkDataNetworkName",
        "mobile_network_packet_core_data_plane_id": "mobileNetworkPacketCoreDataPlaneId",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DataAzurermMobileNetworkAttachedDataNetworkConfig(
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
        mobile_network_data_network_name: builtins.str,
        mobile_network_packet_core_data_plane_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzurermMobileNetworkAttachedDataNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param mobile_network_data_network_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#mobile_network_data_network_name DataAzurermMobileNetworkAttachedDataNetwork#mobile_network_data_network_name}.
        :param mobile_network_packet_core_data_plane_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#mobile_network_packet_core_data_plane_id DataAzurermMobileNetworkAttachedDataNetwork#mobile_network_packet_core_data_plane_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#id DataAzurermMobileNetworkAttachedDataNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#timeouts DataAzurermMobileNetworkAttachedDataNetwork#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataAzurermMobileNetworkAttachedDataNetworkTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae20a20cbb2228829587dc70906e51b7c20b9a3fdd3f51c2d5bead944ad5f1f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument mobile_network_data_network_name", value=mobile_network_data_network_name, expected_type=type_hints["mobile_network_data_network_name"])
            check_type(argname="argument mobile_network_packet_core_data_plane_id", value=mobile_network_packet_core_data_plane_id, expected_type=type_hints["mobile_network_packet_core_data_plane_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mobile_network_data_network_name": mobile_network_data_network_name,
            "mobile_network_packet_core_data_plane_id": mobile_network_packet_core_data_plane_id,
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
        if id is not None:
            self._values["id"] = id
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
    def mobile_network_data_network_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#mobile_network_data_network_name DataAzurermMobileNetworkAttachedDataNetwork#mobile_network_data_network_name}.'''
        result = self._values.get("mobile_network_data_network_name")
        assert result is not None, "Required property 'mobile_network_data_network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mobile_network_packet_core_data_plane_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#mobile_network_packet_core_data_plane_id DataAzurermMobileNetworkAttachedDataNetwork#mobile_network_packet_core_data_plane_id}.'''
        result = self._values.get("mobile_network_packet_core_data_plane_id")
        assert result is not None, "Required property 'mobile_network_packet_core_data_plane_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#id DataAzurermMobileNetworkAttachedDataNetwork#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataAzurermMobileNetworkAttachedDataNetworkTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#timeouts DataAzurermMobileNetworkAttachedDataNetwork#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataAzurermMobileNetworkAttachedDataNetworkTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermMobileNetworkAttachedDataNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17aac40ef63c0482f0e1f9b108e4365ca7d61f3cbc656525c24c2c7bb95317cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a56d66fb6dbd27640ae3ab74092034789454ca49d320b42c81b9a243aba94d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51012b6bddb2216f321f3b53e3b8a9315dba2641dad3336e7af9af6dc27279ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__daa941119514c45645918c8728db031a2a0feadaedbad6c0b9b5e39c56154d74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a557b925a19e3ce9fb5c078834c2a642cdc781d814a3713e998fea872601807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7507a9632268d9ea297c291f51c4edc242399b95c659face01c4705eb32dcfd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="icmpPinholeTimeoutInSeconds")
    def icmp_pinhole_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "icmpPinholeTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="pinholeMaximumNumber")
    def pinhole_maximum_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pinholeMaximumNumber"))

    @builtins.property
    @jsii.member(jsii_name="portRange")
    def port_range(
        self,
    ) -> "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeList":
        return typing.cast("DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeList", jsii.get(self, "portRange"))

    @builtins.property
    @jsii.member(jsii_name="tcpPinholeTimeoutInSeconds")
    def tcp_pinhole_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpPinholeTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="tcpPortReuseMinimumHoldTimeInSeconds")
    def tcp_port_reuse_minimum_hold_time_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpPortReuseMinimumHoldTimeInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="udpPinholeTimeoutInSeconds")
    def udp_pinhole_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "udpPinholeTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="udpPortReuseMinimumHoldTimeInSeconds")
    def udp_port_reuse_minimum_hold_time_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "udpPortReuseMinimumHoldTimeInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation]:
        return typing.cast(typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703b687e6acec667532b5e344e15dd1fee65f01a5d6f9f0cb81259b11f2bfad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96067b67e5a5cd58e37dcec76c5caa6977af9f4e47ab8d2d2d1254ddc4446586)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee98a840d0ff33df77f272cddb5f0bc5ad8a2eec954ac63322025a4e8e45863)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8b13dde95ca6015b100421ecb68f7dbb33d7d726e85a85cfb61939c00cf1d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f217b4be45afdf0d0f9f0d4b1298e26b4a3106d6b0ffdb87103a1e93037b95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab4bb1611cdf52300ebe50ee110bdd9aa8140efaa6aea2efc3d661a48ce67fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f323324abe41c97a6178c716d4ad7173238f9496f9bca4b3e20ffdd0460dda01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maximum")
    def maximum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximum"))

    @builtins.property
    @jsii.member(jsii_name="minimum")
    def minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimum"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange]:
        return typing.cast(typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d5ff84e8637ce104e2580858378f558aa9e2fc431c95f549fcd8a852955dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkTimeouts",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class DataAzurermMobileNetworkAttachedDataNetworkTimeouts:
    def __init__(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#read DataAzurermMobileNetworkAttachedDataNetwork#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de42ab6c702d5aa411633cf0452fa625cac45a059ff91d6f163fd719ffcbc96)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/mobile_network_attached_data_network#read DataAzurermMobileNetworkAttachedDataNetwork#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermMobileNetworkAttachedDataNetworkTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermMobileNetworkAttachedDataNetworkTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermMobileNetworkAttachedDataNetwork.DataAzurermMobileNetworkAttachedDataNetworkTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3baaaf752a99191eb6e5de69e9775bc777e241c38f52daee8d565ee9f558b85c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c8052efc0903fe4c63180a22dd28b443bd0a6485e98009a437be7ea4353c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermMobileNetworkAttachedDataNetworkTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermMobileNetworkAttachedDataNetworkTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermMobileNetworkAttachedDataNetworkTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bbaba23d2e3e5625dfb36cc76355c4dcee1e1fbed874b6f45c9c4a3260749a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataAzurermMobileNetworkAttachedDataNetwork",
    "DataAzurermMobileNetworkAttachedDataNetworkConfig",
    "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation",
    "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationList",
    "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference",
    "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange",
    "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeList",
    "DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference",
    "DataAzurermMobileNetworkAttachedDataNetworkTimeouts",
    "DataAzurermMobileNetworkAttachedDataNetworkTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__32bc4530fa7faeced3c2e0dc7d29cd3928b6c39bfbb5e6f6317feb95591ae962(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    mobile_network_data_network_name: builtins.str,
    mobile_network_packet_core_data_plane_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzurermMobileNetworkAttachedDataNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f03b09d69509b5cddeb3441a9fc5ca61b8314c8ebe36adf022262ef209fdaadc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a5d845c2610b0e761f7f98c79f2ce96330f138689c75d5691a3728f9a7b5ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf2739375625e42a5b8dfc3ef1e28e906a3a171794f126fa9d0a88b3649436b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f10875ed08945a3f301eb21018e32f60a6244a3cfd5f41d062de275155175c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae20a20cbb2228829587dc70906e51b7c20b9a3fdd3f51c2d5bead944ad5f1f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mobile_network_data_network_name: builtins.str,
    mobile_network_packet_core_data_plane_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzurermMobileNetworkAttachedDataNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aac40ef63c0482f0e1f9b108e4365ca7d61f3cbc656525c24c2c7bb95317cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a56d66fb6dbd27640ae3ab74092034789454ca49d320b42c81b9a243aba94d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51012b6bddb2216f321f3b53e3b8a9315dba2641dad3336e7af9af6dc27279ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa941119514c45645918c8728db031a2a0feadaedbad6c0b9b5e39c56154d74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a557b925a19e3ce9fb5c078834c2a642cdc781d814a3713e998fea872601807(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7507a9632268d9ea297c291f51c4edc242399b95c659face01c4705eb32dcfd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703b687e6acec667532b5e344e15dd1fee65f01a5d6f9f0cb81259b11f2bfad9(
    value: typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96067b67e5a5cd58e37dcec76c5caa6977af9f4e47ab8d2d2d1254ddc4446586(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee98a840d0ff33df77f272cddb5f0bc5ad8a2eec954ac63322025a4e8e45863(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8b13dde95ca6015b100421ecb68f7dbb33d7d726e85a85cfb61939c00cf1d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f217b4be45afdf0d0f9f0d4b1298e26b4a3106d6b0ffdb87103a1e93037b95(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4bb1611cdf52300ebe50ee110bdd9aa8140efaa6aea2efc3d661a48ce67fd2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f323324abe41c97a6178c716d4ad7173238f9496f9bca4b3e20ffdd0460dda01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d5ff84e8637ce104e2580858378f558aa9e2fc431c95f549fcd8a852955dc7(
    value: typing.Optional[DataAzurermMobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de42ab6c702d5aa411633cf0452fa625cac45a059ff91d6f163fd719ffcbc96(
    *,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baaaf752a99191eb6e5de69e9775bc777e241c38f52daee8d565ee9f558b85c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c8052efc0903fe4c63180a22dd28b443bd0a6485e98009a437be7ea4353c95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bbaba23d2e3e5625dfb36cc76355c4dcee1e1fbed874b6f45c9c4a3260749a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermMobileNetworkAttachedDataNetworkTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
