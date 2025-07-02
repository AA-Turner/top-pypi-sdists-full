r'''
# `azurerm_mobile_network_attached_data_network`

Refer to the Terraform Registry for docs: [`azurerm_mobile_network_attached_data_network`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network).
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


class MobileNetworkAttachedDataNetwork(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network azurerm_mobile_network_attached_data_network}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dns_addresses: typing.Sequence[builtins.str],
        location: builtins.str,
        mobile_network_data_network_name: builtins.str,
        mobile_network_packet_core_data_plane_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        network_address_port_translation: typing.Optional[typing.Union["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkAttachedDataNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_equipment_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_equipment_static_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
        user_plane_access_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network azurerm_mobile_network_attached_data_network} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dns_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#dns_addresses MobileNetworkAttachedDataNetwork#dns_addresses}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#location MobileNetworkAttachedDataNetwork#location}.
        :param mobile_network_data_network_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#mobile_network_data_network_name MobileNetworkAttachedDataNetwork#mobile_network_data_network_name}.
        :param mobile_network_packet_core_data_plane_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#mobile_network_packet_core_data_plane_id MobileNetworkAttachedDataNetwork#mobile_network_packet_core_data_plane_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#id MobileNetworkAttachedDataNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_address_port_translation: network_address_port_translation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#network_address_port_translation MobileNetworkAttachedDataNetwork#network_address_port_translation}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tags MobileNetworkAttachedDataNetwork#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#timeouts MobileNetworkAttachedDataNetwork#timeouts}
        :param user_equipment_address_pool_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_equipment_address_pool_prefixes MobileNetworkAttachedDataNetwork#user_equipment_address_pool_prefixes}.
        :param user_equipment_static_address_pool_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_equipment_static_address_pool_prefixes MobileNetworkAttachedDataNetwork#user_equipment_static_address_pool_prefixes}.
        :param user_plane_access_ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_address MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_address}.
        :param user_plane_access_ipv4_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_gateway MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_gateway}.
        :param user_plane_access_ipv4_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_subnet MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_subnet}.
        :param user_plane_access_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_name MobileNetworkAttachedDataNetwork#user_plane_access_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f25d040a198e58f47cecd1af41518065258c2626a0c978db51ba2dbb9dce34b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MobileNetworkAttachedDataNetworkConfig(
            dns_addresses=dns_addresses,
            location=location,
            mobile_network_data_network_name=mobile_network_data_network_name,
            mobile_network_packet_core_data_plane_id=mobile_network_packet_core_data_plane_id,
            id=id,
            network_address_port_translation=network_address_port_translation,
            tags=tags,
            timeouts=timeouts,
            user_equipment_address_pool_prefixes=user_equipment_address_pool_prefixes,
            user_equipment_static_address_pool_prefixes=user_equipment_static_address_pool_prefixes,
            user_plane_access_ipv4_address=user_plane_access_ipv4_address,
            user_plane_access_ipv4_gateway=user_plane_access_ipv4_gateway,
            user_plane_access_ipv4_subnet=user_plane_access_ipv4_subnet,
            user_plane_access_name=user_plane_access_name,
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
        '''Generates CDKTF code for importing a MobileNetworkAttachedDataNetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MobileNetworkAttachedDataNetwork to import.
        :param import_from_id: The id of the existing MobileNetworkAttachedDataNetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MobileNetworkAttachedDataNetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851dd2b94a31828a434cdfb5844854da67db76dff25ea846b426dcf47c552abc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNetworkAddressPortTranslation")
    def put_network_address_port_translation(
        self,
        *,
        icmp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        pinhole_maximum_number: typing.Optional[jsii.Number] = None,
        port_range: typing.Optional[typing.Union["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        tcp_port_reuse_minimum_hold_time_in_seconds: typing.Optional[jsii.Number] = None,
        udp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        udp_port_reuse_minimum_hold_time_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param icmp_pinhole_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#icmp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#icmp_pinhole_timeout_in_seconds}.
        :param pinhole_maximum_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#pinhole_maximum_number MobileNetworkAttachedDataNetwork#pinhole_maximum_number}.
        :param port_range: port_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#port_range MobileNetworkAttachedDataNetwork#port_range}
        :param tcp_pinhole_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tcp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#tcp_pinhole_timeout_in_seconds}.
        :param tcp_port_reuse_minimum_hold_time_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tcp_port_reuse_minimum_hold_time_in_seconds MobileNetworkAttachedDataNetwork#tcp_port_reuse_minimum_hold_time_in_seconds}.
        :param udp_pinhole_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#udp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#udp_pinhole_timeout_in_seconds}.
        :param udp_port_reuse_minimum_hold_time_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#udp_port_reuse_minimum_hold_time_in_seconds MobileNetworkAttachedDataNetwork#udp_port_reuse_minimum_hold_time_in_seconds}.
        '''
        value = MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation(
            icmp_pinhole_timeout_in_seconds=icmp_pinhole_timeout_in_seconds,
            pinhole_maximum_number=pinhole_maximum_number,
            port_range=port_range,
            tcp_pinhole_timeout_in_seconds=tcp_pinhole_timeout_in_seconds,
            tcp_port_reuse_minimum_hold_time_in_seconds=tcp_port_reuse_minimum_hold_time_in_seconds,
            udp_pinhole_timeout_in_seconds=udp_pinhole_timeout_in_seconds,
            udp_port_reuse_minimum_hold_time_in_seconds=udp_port_reuse_minimum_hold_time_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkAddressPortTranslation", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#create MobileNetworkAttachedDataNetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#delete MobileNetworkAttachedDataNetwork#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#read MobileNetworkAttachedDataNetwork#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#update MobileNetworkAttachedDataNetwork#update}.
        '''
        value = MobileNetworkAttachedDataNetworkTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworkAddressPortTranslation")
    def reset_network_address_port_translation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAddressPortTranslation", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserEquipmentAddressPoolPrefixes")
    def reset_user_equipment_address_pool_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserEquipmentAddressPoolPrefixes", []))

    @jsii.member(jsii_name="resetUserEquipmentStaticAddressPoolPrefixes")
    def reset_user_equipment_static_address_pool_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserEquipmentStaticAddressPoolPrefixes", []))

    @jsii.member(jsii_name="resetUserPlaneAccessIpv4Address")
    def reset_user_plane_access_ipv4_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessIpv4Address", []))

    @jsii.member(jsii_name="resetUserPlaneAccessIpv4Gateway")
    def reset_user_plane_access_ipv4_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessIpv4Gateway", []))

    @jsii.member(jsii_name="resetUserPlaneAccessIpv4Subnet")
    def reset_user_plane_access_ipv4_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessIpv4Subnet", []))

    @jsii.member(jsii_name="resetUserPlaneAccessName")
    def reset_user_plane_access_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessName", []))

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
    @jsii.member(jsii_name="networkAddressPortTranslation")
    def network_address_port_translation(
        self,
    ) -> "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference":
        return typing.cast("MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference", jsii.get(self, "networkAddressPortTranslation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MobileNetworkAttachedDataNetworkTimeoutsOutputReference":
        return typing.cast("MobileNetworkAttachedDataNetworkTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dnsAddressesInput")
    def dns_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

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
    @jsii.member(jsii_name="networkAddressPortTranslationInput")
    def network_address_port_translation_input(
        self,
    ) -> typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation"]:
        return typing.cast(typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation"], jsii.get(self, "networkAddressPortTranslationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkAttachedDataNetworkTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkAttachedDataNetworkTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userEquipmentAddressPoolPrefixesInput")
    def user_equipment_address_pool_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userEquipmentAddressPoolPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="userEquipmentStaticAddressPoolPrefixesInput")
    def user_equipment_static_address_pool_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userEquipmentStaticAddressPoolPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4AddressInput")
    def user_plane_access_ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessIpv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4GatewayInput")
    def user_plane_access_ipv4_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessIpv4GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4SubnetInput")
    def user_plane_access_ipv4_subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessIpv4SubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessNameInput")
    def user_plane_access_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsAddresses")
    def dns_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsAddresses"))

    @dns_addresses.setter
    def dns_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59935fda4eaf15de28e5eae108a94e52328682478f72fdb041150524514cde82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1159ebac7d593906642841b7fa4d3ebd24d6c259dada2c4921aaf5a7503251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158298e9bf41ba4331e05f7833cf9c4217cc7b9df9625c79bfcbe565fb3ec5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkDataNetworkName")
    def mobile_network_data_network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkDataNetworkName"))

    @mobile_network_data_network_name.setter
    def mobile_network_data_network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac333c5923fcb16a2ca0ec30627b90679fe11c8b9ddb00f54937b2fe7086ea2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkDataNetworkName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkPacketCoreDataPlaneId")
    def mobile_network_packet_core_data_plane_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkPacketCoreDataPlaneId"))

    @mobile_network_packet_core_data_plane_id.setter
    def mobile_network_packet_core_data_plane_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4056bc446e234b7ef8d0b6917d0d3c348107299ab8d2c95c31b10467010c6b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkPacketCoreDataPlaneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1424feda530bf3affb63e8ff9e6dd658165d1bffd41ee416169a6197680d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userEquipmentAddressPoolPrefixes")
    def user_equipment_address_pool_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userEquipmentAddressPoolPrefixes"))

    @user_equipment_address_pool_prefixes.setter
    def user_equipment_address_pool_prefixes(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f883c5dd8948650474eb7dd0381e0fbe98467bab899bd2b1294fab87b80e504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEquipmentAddressPoolPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userEquipmentStaticAddressPoolPrefixes")
    def user_equipment_static_address_pool_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userEquipmentStaticAddressPoolPrefixes"))

    @user_equipment_static_address_pool_prefixes.setter
    def user_equipment_static_address_pool_prefixes(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9aca20a0b16aece39c9bf37bf7c571884b6fb8ac69354f074d75e9af8081dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEquipmentStaticAddressPoolPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Address")
    def user_plane_access_ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Address"))

    @user_plane_access_ipv4_address.setter
    def user_plane_access_ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b703d5d4d7339a044da5d71412557ca9b38b63aa82c8bf6bee9af1c79f6b1f69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessIpv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Gateway")
    def user_plane_access_ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Gateway"))

    @user_plane_access_ipv4_gateway.setter
    def user_plane_access_ipv4_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5bddfb9c7e82de1b88abcbb21fe483fd4837631388223d12ba04c3bce8959ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessIpv4Gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Subnet")
    def user_plane_access_ipv4_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Subnet"))

    @user_plane_access_ipv4_subnet.setter
    def user_plane_access_ipv4_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f7a0ad3ccee8857f1df7764136331e91573befaca9855e76a1982a88a3836d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessIpv4Subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessName")
    def user_plane_access_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessName"))

    @user_plane_access_name.setter
    def user_plane_access_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81ce2842a9960d99f06fe83c2c172a7a42be16c722c507a4cb8389c72e8468e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dns_addresses": "dnsAddresses",
        "location": "location",
        "mobile_network_data_network_name": "mobileNetworkDataNetworkName",
        "mobile_network_packet_core_data_plane_id": "mobileNetworkPacketCoreDataPlaneId",
        "id": "id",
        "network_address_port_translation": "networkAddressPortTranslation",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_equipment_address_pool_prefixes": "userEquipmentAddressPoolPrefixes",
        "user_equipment_static_address_pool_prefixes": "userEquipmentStaticAddressPoolPrefixes",
        "user_plane_access_ipv4_address": "userPlaneAccessIpv4Address",
        "user_plane_access_ipv4_gateway": "userPlaneAccessIpv4Gateway",
        "user_plane_access_ipv4_subnet": "userPlaneAccessIpv4Subnet",
        "user_plane_access_name": "userPlaneAccessName",
    },
)
class MobileNetworkAttachedDataNetworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dns_addresses: typing.Sequence[builtins.str],
        location: builtins.str,
        mobile_network_data_network_name: builtins.str,
        mobile_network_packet_core_data_plane_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        network_address_port_translation: typing.Optional[typing.Union["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkAttachedDataNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_equipment_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_equipment_static_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
        user_plane_access_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dns_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#dns_addresses MobileNetworkAttachedDataNetwork#dns_addresses}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#location MobileNetworkAttachedDataNetwork#location}.
        :param mobile_network_data_network_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#mobile_network_data_network_name MobileNetworkAttachedDataNetwork#mobile_network_data_network_name}.
        :param mobile_network_packet_core_data_plane_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#mobile_network_packet_core_data_plane_id MobileNetworkAttachedDataNetwork#mobile_network_packet_core_data_plane_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#id MobileNetworkAttachedDataNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_address_port_translation: network_address_port_translation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#network_address_port_translation MobileNetworkAttachedDataNetwork#network_address_port_translation}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tags MobileNetworkAttachedDataNetwork#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#timeouts MobileNetworkAttachedDataNetwork#timeouts}
        :param user_equipment_address_pool_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_equipment_address_pool_prefixes MobileNetworkAttachedDataNetwork#user_equipment_address_pool_prefixes}.
        :param user_equipment_static_address_pool_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_equipment_static_address_pool_prefixes MobileNetworkAttachedDataNetwork#user_equipment_static_address_pool_prefixes}.
        :param user_plane_access_ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_address MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_address}.
        :param user_plane_access_ipv4_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_gateway MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_gateway}.
        :param user_plane_access_ipv4_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_subnet MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_subnet}.
        :param user_plane_access_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_name MobileNetworkAttachedDataNetwork#user_plane_access_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_address_port_translation, dict):
            network_address_port_translation = MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation(**network_address_port_translation)
        if isinstance(timeouts, dict):
            timeouts = MobileNetworkAttachedDataNetworkTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40af82315de432cf31a69019708e66122f766330acaeba188affe7d36f74af44)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dns_addresses", value=dns_addresses, expected_type=type_hints["dns_addresses"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mobile_network_data_network_name", value=mobile_network_data_network_name, expected_type=type_hints["mobile_network_data_network_name"])
            check_type(argname="argument mobile_network_packet_core_data_plane_id", value=mobile_network_packet_core_data_plane_id, expected_type=type_hints["mobile_network_packet_core_data_plane_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_address_port_translation", value=network_address_port_translation, expected_type=type_hints["network_address_port_translation"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_equipment_address_pool_prefixes", value=user_equipment_address_pool_prefixes, expected_type=type_hints["user_equipment_address_pool_prefixes"])
            check_type(argname="argument user_equipment_static_address_pool_prefixes", value=user_equipment_static_address_pool_prefixes, expected_type=type_hints["user_equipment_static_address_pool_prefixes"])
            check_type(argname="argument user_plane_access_ipv4_address", value=user_plane_access_ipv4_address, expected_type=type_hints["user_plane_access_ipv4_address"])
            check_type(argname="argument user_plane_access_ipv4_gateway", value=user_plane_access_ipv4_gateway, expected_type=type_hints["user_plane_access_ipv4_gateway"])
            check_type(argname="argument user_plane_access_ipv4_subnet", value=user_plane_access_ipv4_subnet, expected_type=type_hints["user_plane_access_ipv4_subnet"])
            check_type(argname="argument user_plane_access_name", value=user_plane_access_name, expected_type=type_hints["user_plane_access_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_addresses": dns_addresses,
            "location": location,
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
        if network_address_port_translation is not None:
            self._values["network_address_port_translation"] = network_address_port_translation
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_equipment_address_pool_prefixes is not None:
            self._values["user_equipment_address_pool_prefixes"] = user_equipment_address_pool_prefixes
        if user_equipment_static_address_pool_prefixes is not None:
            self._values["user_equipment_static_address_pool_prefixes"] = user_equipment_static_address_pool_prefixes
        if user_plane_access_ipv4_address is not None:
            self._values["user_plane_access_ipv4_address"] = user_plane_access_ipv4_address
        if user_plane_access_ipv4_gateway is not None:
            self._values["user_plane_access_ipv4_gateway"] = user_plane_access_ipv4_gateway
        if user_plane_access_ipv4_subnet is not None:
            self._values["user_plane_access_ipv4_subnet"] = user_plane_access_ipv4_subnet
        if user_plane_access_name is not None:
            self._values["user_plane_access_name"] = user_plane_access_name

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
    def dns_addresses(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#dns_addresses MobileNetworkAttachedDataNetwork#dns_addresses}.'''
        result = self._values.get("dns_addresses")
        assert result is not None, "Required property 'dns_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#location MobileNetworkAttachedDataNetwork#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mobile_network_data_network_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#mobile_network_data_network_name MobileNetworkAttachedDataNetwork#mobile_network_data_network_name}.'''
        result = self._values.get("mobile_network_data_network_name")
        assert result is not None, "Required property 'mobile_network_data_network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mobile_network_packet_core_data_plane_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#mobile_network_packet_core_data_plane_id MobileNetworkAttachedDataNetwork#mobile_network_packet_core_data_plane_id}.'''
        result = self._values.get("mobile_network_packet_core_data_plane_id")
        assert result is not None, "Required property 'mobile_network_packet_core_data_plane_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#id MobileNetworkAttachedDataNetwork#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_address_port_translation(
        self,
    ) -> typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation"]:
        '''network_address_port_translation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#network_address_port_translation MobileNetworkAttachedDataNetwork#network_address_port_translation}
        '''
        result = self._values.get("network_address_port_translation")
        return typing.cast(typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tags MobileNetworkAttachedDataNetwork#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MobileNetworkAttachedDataNetworkTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#timeouts MobileNetworkAttachedDataNetwork#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MobileNetworkAttachedDataNetworkTimeouts"], result)

    @builtins.property
    def user_equipment_address_pool_prefixes(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_equipment_address_pool_prefixes MobileNetworkAttachedDataNetwork#user_equipment_address_pool_prefixes}.'''
        result = self._values.get("user_equipment_address_pool_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_equipment_static_address_pool_prefixes(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_equipment_static_address_pool_prefixes MobileNetworkAttachedDataNetwork#user_equipment_static_address_pool_prefixes}.'''
        result = self._values.get("user_equipment_static_address_pool_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_plane_access_ipv4_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_address MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_address}.'''
        result = self._values.get("user_plane_access_ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_plane_access_ipv4_gateway(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_gateway MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_gateway}.'''
        result = self._values.get("user_plane_access_ipv4_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_plane_access_ipv4_subnet(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_ipv4_subnet MobileNetworkAttachedDataNetwork#user_plane_access_ipv4_subnet}.'''
        result = self._values.get("user_plane_access_ipv4_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_plane_access_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#user_plane_access_name MobileNetworkAttachedDataNetwork#user_plane_access_name}.'''
        result = self._values.get("user_plane_access_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkAttachedDataNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation",
    jsii_struct_bases=[],
    name_mapping={
        "icmp_pinhole_timeout_in_seconds": "icmpPinholeTimeoutInSeconds",
        "pinhole_maximum_number": "pinholeMaximumNumber",
        "port_range": "portRange",
        "tcp_pinhole_timeout_in_seconds": "tcpPinholeTimeoutInSeconds",
        "tcp_port_reuse_minimum_hold_time_in_seconds": "tcpPortReuseMinimumHoldTimeInSeconds",
        "udp_pinhole_timeout_in_seconds": "udpPinholeTimeoutInSeconds",
        "udp_port_reuse_minimum_hold_time_in_seconds": "udpPortReuseMinimumHoldTimeInSeconds",
    },
)
class MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation:
    def __init__(
        self,
        *,
        icmp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        pinhole_maximum_number: typing.Optional[jsii.Number] = None,
        port_range: typing.Optional[typing.Union["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange", typing.Dict[builtins.str, typing.Any]]] = None,
        tcp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        tcp_port_reuse_minimum_hold_time_in_seconds: typing.Optional[jsii.Number] = None,
        udp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        udp_port_reuse_minimum_hold_time_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param icmp_pinhole_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#icmp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#icmp_pinhole_timeout_in_seconds}.
        :param pinhole_maximum_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#pinhole_maximum_number MobileNetworkAttachedDataNetwork#pinhole_maximum_number}.
        :param port_range: port_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#port_range MobileNetworkAttachedDataNetwork#port_range}
        :param tcp_pinhole_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tcp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#tcp_pinhole_timeout_in_seconds}.
        :param tcp_port_reuse_minimum_hold_time_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tcp_port_reuse_minimum_hold_time_in_seconds MobileNetworkAttachedDataNetwork#tcp_port_reuse_minimum_hold_time_in_seconds}.
        :param udp_pinhole_timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#udp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#udp_pinhole_timeout_in_seconds}.
        :param udp_port_reuse_minimum_hold_time_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#udp_port_reuse_minimum_hold_time_in_seconds MobileNetworkAttachedDataNetwork#udp_port_reuse_minimum_hold_time_in_seconds}.
        '''
        if isinstance(port_range, dict):
            port_range = MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange(**port_range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb05a5edf17a6d278f430989d7c83dd3d1f3a611261b255835b5325adb487ee)
            check_type(argname="argument icmp_pinhole_timeout_in_seconds", value=icmp_pinhole_timeout_in_seconds, expected_type=type_hints["icmp_pinhole_timeout_in_seconds"])
            check_type(argname="argument pinhole_maximum_number", value=pinhole_maximum_number, expected_type=type_hints["pinhole_maximum_number"])
            check_type(argname="argument port_range", value=port_range, expected_type=type_hints["port_range"])
            check_type(argname="argument tcp_pinhole_timeout_in_seconds", value=tcp_pinhole_timeout_in_seconds, expected_type=type_hints["tcp_pinhole_timeout_in_seconds"])
            check_type(argname="argument tcp_port_reuse_minimum_hold_time_in_seconds", value=tcp_port_reuse_minimum_hold_time_in_seconds, expected_type=type_hints["tcp_port_reuse_minimum_hold_time_in_seconds"])
            check_type(argname="argument udp_pinhole_timeout_in_seconds", value=udp_pinhole_timeout_in_seconds, expected_type=type_hints["udp_pinhole_timeout_in_seconds"])
            check_type(argname="argument udp_port_reuse_minimum_hold_time_in_seconds", value=udp_port_reuse_minimum_hold_time_in_seconds, expected_type=type_hints["udp_port_reuse_minimum_hold_time_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if icmp_pinhole_timeout_in_seconds is not None:
            self._values["icmp_pinhole_timeout_in_seconds"] = icmp_pinhole_timeout_in_seconds
        if pinhole_maximum_number is not None:
            self._values["pinhole_maximum_number"] = pinhole_maximum_number
        if port_range is not None:
            self._values["port_range"] = port_range
        if tcp_pinhole_timeout_in_seconds is not None:
            self._values["tcp_pinhole_timeout_in_seconds"] = tcp_pinhole_timeout_in_seconds
        if tcp_port_reuse_minimum_hold_time_in_seconds is not None:
            self._values["tcp_port_reuse_minimum_hold_time_in_seconds"] = tcp_port_reuse_minimum_hold_time_in_seconds
        if udp_pinhole_timeout_in_seconds is not None:
            self._values["udp_pinhole_timeout_in_seconds"] = udp_pinhole_timeout_in_seconds
        if udp_port_reuse_minimum_hold_time_in_seconds is not None:
            self._values["udp_port_reuse_minimum_hold_time_in_seconds"] = udp_port_reuse_minimum_hold_time_in_seconds

    @builtins.property
    def icmp_pinhole_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#icmp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#icmp_pinhole_timeout_in_seconds}.'''
        result = self._values.get("icmp_pinhole_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pinhole_maximum_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#pinhole_maximum_number MobileNetworkAttachedDataNetwork#pinhole_maximum_number}.'''
        result = self._values.get("pinhole_maximum_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_range(
        self,
    ) -> typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange"]:
        '''port_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#port_range MobileNetworkAttachedDataNetwork#port_range}
        '''
        result = self._values.get("port_range")
        return typing.cast(typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange"], result)

    @builtins.property
    def tcp_pinhole_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tcp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#tcp_pinhole_timeout_in_seconds}.'''
        result = self._values.get("tcp_pinhole_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_port_reuse_minimum_hold_time_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#tcp_port_reuse_minimum_hold_time_in_seconds MobileNetworkAttachedDataNetwork#tcp_port_reuse_minimum_hold_time_in_seconds}.'''
        result = self._values.get("tcp_port_reuse_minimum_hold_time_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def udp_pinhole_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#udp_pinhole_timeout_in_seconds MobileNetworkAttachedDataNetwork#udp_pinhole_timeout_in_seconds}.'''
        result = self._values.get("udp_pinhole_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def udp_port_reuse_minimum_hold_time_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#udp_port_reuse_minimum_hold_time_in_seconds MobileNetworkAttachedDataNetwork#udp_port_reuse_minimum_hold_time_in_seconds}.'''
        result = self._values.get("udp_port_reuse_minimum_hold_time_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28a86bbcca4f4177265f5adc8ce2d824d5142b1ccd8aba2f679190dec1523f1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPortRange")
    def put_port_range(
        self,
        *,
        maximum: typing.Optional[jsii.Number] = None,
        minimum: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#maximum MobileNetworkAttachedDataNetwork#maximum}.
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#minimum MobileNetworkAttachedDataNetwork#minimum}.
        '''
        value = MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange(
            maximum=maximum, minimum=minimum
        )

        return typing.cast(None, jsii.invoke(self, "putPortRange", [value]))

    @jsii.member(jsii_name="resetIcmpPinholeTimeoutInSeconds")
    def reset_icmp_pinhole_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcmpPinholeTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetPinholeMaximumNumber")
    def reset_pinhole_maximum_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPinholeMaximumNumber", []))

    @jsii.member(jsii_name="resetPortRange")
    def reset_port_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortRange", []))

    @jsii.member(jsii_name="resetTcpPinholeTimeoutInSeconds")
    def reset_tcp_pinhole_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpPinholeTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetTcpPortReuseMinimumHoldTimeInSeconds")
    def reset_tcp_port_reuse_minimum_hold_time_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpPortReuseMinimumHoldTimeInSeconds", []))

    @jsii.member(jsii_name="resetUdpPinholeTimeoutInSeconds")
    def reset_udp_pinhole_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUdpPinholeTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetUdpPortReuseMinimumHoldTimeInSeconds")
    def reset_udp_port_reuse_minimum_hold_time_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUdpPortReuseMinimumHoldTimeInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="portRange")
    def port_range(
        self,
    ) -> "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference":
        return typing.cast("MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference", jsii.get(self, "portRange"))

    @builtins.property
    @jsii.member(jsii_name="icmpPinholeTimeoutInSecondsInput")
    def icmp_pinhole_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "icmpPinholeTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pinholeMaximumNumberInput")
    def pinhole_maximum_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pinholeMaximumNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="portRangeInput")
    def port_range_input(
        self,
    ) -> typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange"]:
        return typing.cast(typing.Optional["MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange"], jsii.get(self, "portRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpPinholeTimeoutInSecondsInput")
    def tcp_pinhole_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tcpPinholeTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpPortReuseMinimumHoldTimeInSecondsInput")
    def tcp_port_reuse_minimum_hold_time_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tcpPortReuseMinimumHoldTimeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="udpPinholeTimeoutInSecondsInput")
    def udp_pinhole_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "udpPinholeTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="udpPortReuseMinimumHoldTimeInSecondsInput")
    def udp_port_reuse_minimum_hold_time_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "udpPortReuseMinimumHoldTimeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="icmpPinholeTimeoutInSeconds")
    def icmp_pinhole_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "icmpPinholeTimeoutInSeconds"))

    @icmp_pinhole_timeout_in_seconds.setter
    def icmp_pinhole_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957239f5f8e3928389a5b4fe64bf4e4f33063150b4b61c41d4d425512be92b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icmpPinholeTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pinholeMaximumNumber")
    def pinhole_maximum_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pinholeMaximumNumber"))

    @pinhole_maximum_number.setter
    def pinhole_maximum_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5f8f072c71978bb9438738a7d256a18f441e2543335382acaac75e23036da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pinholeMaximumNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpPinholeTimeoutInSeconds")
    def tcp_pinhole_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpPinholeTimeoutInSeconds"))

    @tcp_pinhole_timeout_in_seconds.setter
    def tcp_pinhole_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f941c9b9ddd28ca77ba323ec11c848d0451930dd0f48b09553150d4544bf3179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpPinholeTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpPortReuseMinimumHoldTimeInSeconds")
    def tcp_port_reuse_minimum_hold_time_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpPortReuseMinimumHoldTimeInSeconds"))

    @tcp_port_reuse_minimum_hold_time_in_seconds.setter
    def tcp_port_reuse_minimum_hold_time_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a118ade605cc97e4976fc662f0a865a96d1ec39c3279015708b7795f1597522b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpPortReuseMinimumHoldTimeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="udpPinholeTimeoutInSeconds")
    def udp_pinhole_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "udpPinholeTimeoutInSeconds"))

    @udp_pinhole_timeout_in_seconds.setter
    def udp_pinhole_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a690a6af137b946038fcf73a13d09fd54c4868507a5afb2482142f8e88c795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "udpPinholeTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="udpPortReuseMinimumHoldTimeInSeconds")
    def udp_port_reuse_minimum_hold_time_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "udpPortReuseMinimumHoldTimeInSeconds"))

    @udp_port_reuse_minimum_hold_time_in_seconds.setter
    def udp_port_reuse_minimum_hold_time_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119fac12bc9143401aab009284e4ac596f2ecdc8ba0ffa7d3c00354d2779a8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "udpPortReuseMinimumHoldTimeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation]:
        return typing.cast(typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ff5587e2a24d031d545f225a155c5467b1321ad547e7e6d144cbdc1aa2ae50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange",
    jsii_struct_bases=[],
    name_mapping={"maximum": "maximum", "minimum": "minimum"},
)
class MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange:
    def __init__(
        self,
        *,
        maximum: typing.Optional[jsii.Number] = None,
        minimum: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#maximum MobileNetworkAttachedDataNetwork#maximum}.
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#minimum MobileNetworkAttachedDataNetwork#minimum}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381f8e187421dff1e634e31d46ef1e7f6d6326638973b9029ae2053f1d17b1a4)
            check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum is not None:
            self._values["maximum"] = maximum
        if minimum is not None:
            self._values["minimum"] = minimum

    @builtins.property
    def maximum(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#maximum MobileNetworkAttachedDataNetwork#maximum}.'''
        result = self._values.get("maximum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#minimum MobileNetworkAttachedDataNetwork#minimum}.'''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca01f420ffbf5a1a6c5323841311280ba4e1f3ab5024896c098f1cec1e21ebed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaximum")
    def reset_maximum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximum", []))

    @jsii.member(jsii_name="resetMinimum")
    def reset_minimum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimum", []))

    @builtins.property
    @jsii.member(jsii_name="maximumInput")
    def maximum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumInput")
    def minimum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumInput"))

    @builtins.property
    @jsii.member(jsii_name="maximum")
    def maximum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximum"))

    @maximum.setter
    def maximum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35f174fc388e6f1fbc234f25fa5f085a5572a67013352b60da06fb78aca65f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimum")
    def minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimum"))

    @minimum.setter
    def minimum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6fdc3d7726360c232d90b2e3370dce1c0bbaa97be9f1626fc4e16299d2ef040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange]:
        return typing.cast(typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06a23ee72ec07269fde953325380e9c54e9f6bebb5eb15fa5ff9a7ffd7b377a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetworkTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MobileNetworkAttachedDataNetworkTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#create MobileNetworkAttachedDataNetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#delete MobileNetworkAttachedDataNetwork#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#read MobileNetworkAttachedDataNetwork#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#update MobileNetworkAttachedDataNetwork#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd1a34a86df941f15d3d07552e9d109523877309e4922456cf0b823804cc5c9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#create MobileNetworkAttachedDataNetwork#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#delete MobileNetworkAttachedDataNetwork#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#read MobileNetworkAttachedDataNetwork#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_attached_data_network#update MobileNetworkAttachedDataNetwork#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkAttachedDataNetworkTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkAttachedDataNetworkTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkAttachedDataNetwork.MobileNetworkAttachedDataNetworkTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb32da253810c6a1dd6741343a902e83394f0933aba369ba33bb93c818fb2bb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc59e5b6764d6149f8172de7eb209c7a9437fd7e9495f712e48ee53266f600e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5577e8f7c52fddee6a6ae835bc3b9894eb1e157585d753c380548e45ab0854e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d987833322fd44ed8fbc8bdb01f97465d401bce697525658741c02c409e06edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd5b12afadca10b8446dbaa17b708d1409350c2510ed234427c265c0834884f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkAttachedDataNetworkTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkAttachedDataNetworkTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkAttachedDataNetworkTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf947617ac6dde167144ba0d2b70d0e25d9f6a8ca142ab570009c8e83b61aab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MobileNetworkAttachedDataNetwork",
    "MobileNetworkAttachedDataNetworkConfig",
    "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation",
    "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationOutputReference",
    "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange",
    "MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRangeOutputReference",
    "MobileNetworkAttachedDataNetworkTimeouts",
    "MobileNetworkAttachedDataNetworkTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7f25d040a198e58f47cecd1af41518065258c2626a0c978db51ba2dbb9dce34b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dns_addresses: typing.Sequence[builtins.str],
    location: builtins.str,
    mobile_network_data_network_name: builtins.str,
    mobile_network_packet_core_data_plane_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    network_address_port_translation: typing.Optional[typing.Union[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkAttachedDataNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_equipment_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_equipment_static_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
    user_plane_access_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__851dd2b94a31828a434cdfb5844854da67db76dff25ea846b426dcf47c552abc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59935fda4eaf15de28e5eae108a94e52328682478f72fdb041150524514cde82(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1159ebac7d593906642841b7fa4d3ebd24d6c259dada2c4921aaf5a7503251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158298e9bf41ba4331e05f7833cf9c4217cc7b9df9625c79bfcbe565fb3ec5f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac333c5923fcb16a2ca0ec30627b90679fe11c8b9ddb00f54937b2fe7086ea2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4056bc446e234b7ef8d0b6917d0d3c348107299ab8d2c95c31b10467010c6b57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1424feda530bf3affb63e8ff9e6dd658165d1bffd41ee416169a6197680d6a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f883c5dd8948650474eb7dd0381e0fbe98467bab899bd2b1294fab87b80e504(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9aca20a0b16aece39c9bf37bf7c571884b6fb8ac69354f074d75e9af8081dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b703d5d4d7339a044da5d71412557ca9b38b63aa82c8bf6bee9af1c79f6b1f69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5bddfb9c7e82de1b88abcbb21fe483fd4837631388223d12ba04c3bce8959ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f7a0ad3ccee8857f1df7764136331e91573befaca9855e76a1982a88a3836d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81ce2842a9960d99f06fe83c2c172a7a42be16c722c507a4cb8389c72e8468e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40af82315de432cf31a69019708e66122f766330acaeba188affe7d36f74af44(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_addresses: typing.Sequence[builtins.str],
    location: builtins.str,
    mobile_network_data_network_name: builtins.str,
    mobile_network_packet_core_data_plane_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    network_address_port_translation: typing.Optional[typing.Union[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkAttachedDataNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_equipment_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_equipment_static_address_pool_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
    user_plane_access_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb05a5edf17a6d278f430989d7c83dd3d1f3a611261b255835b5325adb487ee(
    *,
    icmp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    pinhole_maximum_number: typing.Optional[jsii.Number] = None,
    port_range: typing.Optional[typing.Union[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange, typing.Dict[builtins.str, typing.Any]]] = None,
    tcp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    tcp_port_reuse_minimum_hold_time_in_seconds: typing.Optional[jsii.Number] = None,
    udp_pinhole_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    udp_port_reuse_minimum_hold_time_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a86bbcca4f4177265f5adc8ce2d824d5142b1ccd8aba2f679190dec1523f1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957239f5f8e3928389a5b4fe64bf4e4f33063150b4b61c41d4d425512be92b21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5f8f072c71978bb9438738a7d256a18f441e2543335382acaac75e23036da9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f941c9b9ddd28ca77ba323ec11c848d0451930dd0f48b09553150d4544bf3179(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a118ade605cc97e4976fc662f0a865a96d1ec39c3279015708b7795f1597522b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a690a6af137b946038fcf73a13d09fd54c4868507a5afb2482142f8e88c795(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119fac12bc9143401aab009284e4ac596f2ecdc8ba0ffa7d3c00354d2779a8fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ff5587e2a24d031d545f225a155c5467b1321ad547e7e6d144cbdc1aa2ae50(
    value: typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381f8e187421dff1e634e31d46ef1e7f6d6326638973b9029ae2053f1d17b1a4(
    *,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca01f420ffbf5a1a6c5323841311280ba4e1f3ab5024896c098f1cec1e21ebed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35f174fc388e6f1fbc234f25fa5f085a5572a67013352b60da06fb78aca65f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fdc3d7726360c232d90b2e3370dce1c0bbaa97be9f1626fc4e16299d2ef040(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06a23ee72ec07269fde953325380e9c54e9f6bebb5eb15fa5ff9a7ffd7b377a(
    value: typing.Optional[MobileNetworkAttachedDataNetworkNetworkAddressPortTranslationPortRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd1a34a86df941f15d3d07552e9d109523877309e4922456cf0b823804cc5c9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb32da253810c6a1dd6741343a902e83394f0933aba369ba33bb93c818fb2bb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc59e5b6764d6149f8172de7eb209c7a9437fd7e9495f712e48ee53266f600e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5577e8f7c52fddee6a6ae835bc3b9894eb1e157585d753c380548e45ab0854e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d987833322fd44ed8fbc8bdb01f97465d401bce697525658741c02c409e06edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd5b12afadca10b8446dbaa17b708d1409350c2510ed234427c265c0834884f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf947617ac6dde167144ba0d2b70d0e25d9f6a8ca142ab570009c8e83b61aab4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkAttachedDataNetworkTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
