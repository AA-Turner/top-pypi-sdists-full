r'''
# `opentelekomcloud_dc_virtual_interface_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dc_virtual_interface_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3).
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


class DcVirtualInterfaceV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV3.DcVirtualInterfaceV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3 opentelekomcloud_dc_virtual_interface_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bandwidth: jsii.Number,
        direct_connect_id: builtins.str,
        name: builtins.str,
        remote_ep_group: typing.Sequence[builtins.str],
        route_mode: builtins.str,
        type: builtins.str,
        vgw_id: builtins.str,
        vlan: jsii.Number,
        address_family: typing.Optional[builtins.str] = None,
        asn: typing.Optional[jsii.Number] = None,
        bgp_md5: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lag_id: typing.Optional[builtins.str] = None,
        local_gateway_v4_ip: typing.Optional[builtins.str] = None,
        local_gateway_v6_ip: typing.Optional[builtins.str] = None,
        remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
        remote_gateway_v6_ip: typing.Optional[builtins.str] = None,
        resource_tenant_id: typing.Optional[builtins.str] = None,
        service_ep_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3 opentelekomcloud_dc_virtual_interface_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#bandwidth DcVirtualInterfaceV3#bandwidth}.
        :param direct_connect_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#direct_connect_id DcVirtualInterfaceV3#direct_connect_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#name DcVirtualInterfaceV3#name}.
        :param remote_ep_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_ep_group DcVirtualInterfaceV3#remote_ep_group}.
        :param route_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#route_mode DcVirtualInterfaceV3#route_mode}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#type DcVirtualInterfaceV3#type}.
        :param vgw_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#vgw_id DcVirtualInterfaceV3#vgw_id}.
        :param vlan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#vlan DcVirtualInterfaceV3#vlan}.
        :param address_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#address_family DcVirtualInterfaceV3#address_family}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#asn DcVirtualInterfaceV3#asn}.
        :param bgp_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#bgp_md5 DcVirtualInterfaceV3#bgp_md5}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#description DcVirtualInterfaceV3#description}.
        :param enable_bfd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#enable_bfd DcVirtualInterfaceV3#enable_bfd}.
        :param enable_nqa: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#enable_nqa DcVirtualInterfaceV3#enable_nqa}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#id DcVirtualInterfaceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lag_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#lag_id DcVirtualInterfaceV3#lag_id}.
        :param local_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#local_gateway_v4_ip DcVirtualInterfaceV3#local_gateway_v4_ip}.
        :param local_gateway_v6_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#local_gateway_v6_ip DcVirtualInterfaceV3#local_gateway_v6_ip}.
        :param remote_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_gateway_v4_ip DcVirtualInterfaceV3#remote_gateway_v4_ip}.
        :param remote_gateway_v6_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_gateway_v6_ip DcVirtualInterfaceV3#remote_gateway_v6_ip}.
        :param resource_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#resource_tenant_id DcVirtualInterfaceV3#resource_tenant_id}.
        :param service_ep_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#service_ep_group DcVirtualInterfaceV3#service_ep_group}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eab2369ac7b89bae3002cb15266e8bdd87f112a23eb24fbf2bb3774a8739ece)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DcVirtualInterfaceV3Config(
            bandwidth=bandwidth,
            direct_connect_id=direct_connect_id,
            name=name,
            remote_ep_group=remote_ep_group,
            route_mode=route_mode,
            type=type,
            vgw_id=vgw_id,
            vlan=vlan,
            address_family=address_family,
            asn=asn,
            bgp_md5=bgp_md5,
            description=description,
            enable_bfd=enable_bfd,
            enable_nqa=enable_nqa,
            id=id,
            lag_id=lag_id,
            local_gateway_v4_ip=local_gateway_v4_ip,
            local_gateway_v6_ip=local_gateway_v6_ip,
            remote_gateway_v4_ip=remote_gateway_v4_ip,
            remote_gateway_v6_ip=remote_gateway_v6_ip,
            resource_tenant_id=resource_tenant_id,
            service_ep_group=service_ep_group,
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
        '''Generates CDKTF code for importing a DcVirtualInterfaceV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DcVirtualInterfaceV3 to import.
        :param import_from_id: The id of the existing DcVirtualInterfaceV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DcVirtualInterfaceV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829267cadfa905ffa38ae1a68af9c3f587c9fec37ab4e8a668840e7f5b36150a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAddressFamily")
    def reset_address_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressFamily", []))

    @jsii.member(jsii_name="resetAsn")
    def reset_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsn", []))

    @jsii.member(jsii_name="resetBgpMd5")
    def reset_bgp_md5(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpMd5", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableBfd")
    def reset_enable_bfd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableBfd", []))

    @jsii.member(jsii_name="resetEnableNqa")
    def reset_enable_nqa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNqa", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLagId")
    def reset_lag_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLagId", []))

    @jsii.member(jsii_name="resetLocalGatewayV4Ip")
    def reset_local_gateway_v4_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalGatewayV4Ip", []))

    @jsii.member(jsii_name="resetLocalGatewayV6Ip")
    def reset_local_gateway_v6_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalGatewayV6Ip", []))

    @jsii.member(jsii_name="resetRemoteGatewayV4Ip")
    def reset_remote_gateway_v4_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteGatewayV4Ip", []))

    @jsii.member(jsii_name="resetRemoteGatewayV6Ip")
    def reset_remote_gateway_v6_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteGatewayV6Ip", []))

    @jsii.member(jsii_name="resetResourceTenantId")
    def reset_resource_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTenantId", []))

    @jsii.member(jsii_name="resetServiceEpGroup")
    def reset_service_ep_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceEpGroup", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="vifPeers")
    def vif_peers(self) -> "DcVirtualInterfaceV3VifPeersList":
        return typing.cast("DcVirtualInterfaceV3VifPeersList", jsii.get(self, "vifPeers"))

    @builtins.property
    @jsii.member(jsii_name="addressFamilyInput")
    def address_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInput")
    def bandwidth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpMd5Input")
    def bgp_md5_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpMd5Input"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="directConnectIdInput")
    def direct_connect_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directConnectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableBfdInput")
    def enable_bfd_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableBfdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNqaInput")
    def enable_nqa_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNqaInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lagIdInput")
    def lag_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lagIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localGatewayV4IpInput")
    def local_gateway_v4_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localGatewayV4IpInput"))

    @builtins.property
    @jsii.member(jsii_name="localGatewayV6IpInput")
    def local_gateway_v6_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localGatewayV6IpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteEpGroupInput")
    def remote_ep_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "remoteEpGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayV4IpInput")
    def remote_gateway_v4_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteGatewayV4IpInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayV6IpInput")
    def remote_gateway_v6_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteGatewayV6IpInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTenantIdInput")
    def resource_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routeModeInput")
    def route_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceEpGroupInput")
    def service_ep_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceEpGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vgwIdInput")
    def vgw_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vgwIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanInput")
    def vlan_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vlanInput"))

    @builtins.property
    @jsii.member(jsii_name="addressFamily")
    def address_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressFamily"))

    @address_family.setter
    def address_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444e0343060d5efcade72e05b97b46208769de8974ac0b24ec883cc091462d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077d368f375496bb922b592be6f1a9459913c85aa86a12b9c94250205b5d9285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dac45c5b6ed3614b828a6f172fa2fedc9805288c2067684e23bdff7b5ad4910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpMd5")
    def bgp_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpMd5"))

    @bgp_md5.setter
    def bgp_md5(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e53edf538965d54ff598d1a8d42585456422b719113509da0fb7fb127c10e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpMd5", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4fc578a6259844172e21aa18a3877964c2584eb266772e38d222b7b45220e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directConnectId")
    def direct_connect_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directConnectId"))

    @direct_connect_id.setter
    def direct_connect_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e76f55b891f0653c123e28dd6428969569eb181d8975b928efab8bab7254ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directConnectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableBfd")
    def enable_bfd(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableBfd"))

    @enable_bfd.setter
    def enable_bfd(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4f98f799afe23a7bbfb9b4325580d0072d955ffce0ff769cd1b4afa15766d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBfd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableNqa")
    def enable_nqa(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNqa"))

    @enable_nqa.setter
    def enable_nqa(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d4b120abd494f0af598f0f1ed4f7f13f1738a469feaddea39dffce5b4f1ba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNqa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8626001e2bda9dd26d2b4f6022279947af483ff31bd7969a3a922f221d6ae76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lagId")
    def lag_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lagId"))

    @lag_id.setter
    def lag_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565fd3d50d211a9e0d697f16451e63bdd2e16a2ffdf3bfd49819f1924dddf5de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lagId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localGatewayV4Ip")
    def local_gateway_v4_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localGatewayV4Ip"))

    @local_gateway_v4_ip.setter
    def local_gateway_v4_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c990ce1bef2dd63bfac40f33ccd3b10ed4e11c4843d856e5c3fe82bcef91e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localGatewayV4Ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localGatewayV6Ip")
    def local_gateway_v6_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localGatewayV6Ip"))

    @local_gateway_v6_ip.setter
    def local_gateway_v6_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0e2df91fddb53b2c15b10ab3907a55b9fb34254276886fea6f3223053155ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localGatewayV6Ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5c5df6a07ad51e6276c4e6a558ba57a984771de5b3bb04b42867df8f6c090a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteEpGroup")
    def remote_ep_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteEpGroup"))

    @remote_ep_group.setter
    def remote_ep_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7c3f344c374e1914a7934724a577e2eb977a9e0a855eb8dd4952854629ef7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteEpGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayV4Ip")
    def remote_gateway_v4_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteGatewayV4Ip"))

    @remote_gateway_v4_ip.setter
    def remote_gateway_v4_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc9aca507f6ec71a3c55bf56a1a61b15a376641493095480a80db72ef8b0956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteGatewayV4Ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayV6Ip")
    def remote_gateway_v6_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteGatewayV6Ip"))

    @remote_gateway_v6_ip.setter
    def remote_gateway_v6_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eade78280e711f0337eac010dc1a7bc2c9695730b84c43dfa845ce01a7e721a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteGatewayV6Ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTenantId")
    def resource_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceTenantId"))

    @resource_tenant_id.setter
    def resource_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d0a108e0d83b1640a67320971ab192c6b19215fe5152131f683d84dbd9e5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeMode")
    def route_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeMode"))

    @route_mode.setter
    def route_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e51ba1be2a9be179182ca49ff057ed72ad24bd9610f4f99a254643149785102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceEpGroup")
    def service_ep_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceEpGroup"))

    @service_ep_group.setter
    def service_ep_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1063930769fc0500ec9887d1877c1227c25ea422a8456594338d342cd632e3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceEpGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2852fdfb166f7300464be31dabf3f2d04926a993ead5e8ae1d45685312ea53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vgwId")
    def vgw_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vgwId"))

    @vgw_id.setter
    def vgw_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8664dfd4f5f6f72dbdc377338eddeff3fc7dbbe3fc4cc894dbf49e658fc2031a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vgwId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vlan")
    def vlan(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlan"))

    @vlan.setter
    def vlan(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8332673b40996214a207e3a3980e2b31a3172c2cad331efaef9a5ed7d9a8db5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlan", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV3.DcVirtualInterfaceV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bandwidth": "bandwidth",
        "direct_connect_id": "directConnectId",
        "name": "name",
        "remote_ep_group": "remoteEpGroup",
        "route_mode": "routeMode",
        "type": "type",
        "vgw_id": "vgwId",
        "vlan": "vlan",
        "address_family": "addressFamily",
        "asn": "asn",
        "bgp_md5": "bgpMd5",
        "description": "description",
        "enable_bfd": "enableBfd",
        "enable_nqa": "enableNqa",
        "id": "id",
        "lag_id": "lagId",
        "local_gateway_v4_ip": "localGatewayV4Ip",
        "local_gateway_v6_ip": "localGatewayV6Ip",
        "remote_gateway_v4_ip": "remoteGatewayV4Ip",
        "remote_gateway_v6_ip": "remoteGatewayV6Ip",
        "resource_tenant_id": "resourceTenantId",
        "service_ep_group": "serviceEpGroup",
    },
)
class DcVirtualInterfaceV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bandwidth: jsii.Number,
        direct_connect_id: builtins.str,
        name: builtins.str,
        remote_ep_group: typing.Sequence[builtins.str],
        route_mode: builtins.str,
        type: builtins.str,
        vgw_id: builtins.str,
        vlan: jsii.Number,
        address_family: typing.Optional[builtins.str] = None,
        asn: typing.Optional[jsii.Number] = None,
        bgp_md5: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lag_id: typing.Optional[builtins.str] = None,
        local_gateway_v4_ip: typing.Optional[builtins.str] = None,
        local_gateway_v6_ip: typing.Optional[builtins.str] = None,
        remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
        remote_gateway_v6_ip: typing.Optional[builtins.str] = None,
        resource_tenant_id: typing.Optional[builtins.str] = None,
        service_ep_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#bandwidth DcVirtualInterfaceV3#bandwidth}.
        :param direct_connect_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#direct_connect_id DcVirtualInterfaceV3#direct_connect_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#name DcVirtualInterfaceV3#name}.
        :param remote_ep_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_ep_group DcVirtualInterfaceV3#remote_ep_group}.
        :param route_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#route_mode DcVirtualInterfaceV3#route_mode}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#type DcVirtualInterfaceV3#type}.
        :param vgw_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#vgw_id DcVirtualInterfaceV3#vgw_id}.
        :param vlan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#vlan DcVirtualInterfaceV3#vlan}.
        :param address_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#address_family DcVirtualInterfaceV3#address_family}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#asn DcVirtualInterfaceV3#asn}.
        :param bgp_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#bgp_md5 DcVirtualInterfaceV3#bgp_md5}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#description DcVirtualInterfaceV3#description}.
        :param enable_bfd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#enable_bfd DcVirtualInterfaceV3#enable_bfd}.
        :param enable_nqa: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#enable_nqa DcVirtualInterfaceV3#enable_nqa}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#id DcVirtualInterfaceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lag_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#lag_id DcVirtualInterfaceV3#lag_id}.
        :param local_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#local_gateway_v4_ip DcVirtualInterfaceV3#local_gateway_v4_ip}.
        :param local_gateway_v6_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#local_gateway_v6_ip DcVirtualInterfaceV3#local_gateway_v6_ip}.
        :param remote_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_gateway_v4_ip DcVirtualInterfaceV3#remote_gateway_v4_ip}.
        :param remote_gateway_v6_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_gateway_v6_ip DcVirtualInterfaceV3#remote_gateway_v6_ip}.
        :param resource_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#resource_tenant_id DcVirtualInterfaceV3#resource_tenant_id}.
        :param service_ep_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#service_ep_group DcVirtualInterfaceV3#service_ep_group}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ea08e2348d2dc6b31568bd5f794e0e220115c0363720d9413aa5f02c2ab4d1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument direct_connect_id", value=direct_connect_id, expected_type=type_hints["direct_connect_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument remote_ep_group", value=remote_ep_group, expected_type=type_hints["remote_ep_group"])
            check_type(argname="argument route_mode", value=route_mode, expected_type=type_hints["route_mode"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vgw_id", value=vgw_id, expected_type=type_hints["vgw_id"])
            check_type(argname="argument vlan", value=vlan, expected_type=type_hints["vlan"])
            check_type(argname="argument address_family", value=address_family, expected_type=type_hints["address_family"])
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument bgp_md5", value=bgp_md5, expected_type=type_hints["bgp_md5"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_bfd", value=enable_bfd, expected_type=type_hints["enable_bfd"])
            check_type(argname="argument enable_nqa", value=enable_nqa, expected_type=type_hints["enable_nqa"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lag_id", value=lag_id, expected_type=type_hints["lag_id"])
            check_type(argname="argument local_gateway_v4_ip", value=local_gateway_v4_ip, expected_type=type_hints["local_gateway_v4_ip"])
            check_type(argname="argument local_gateway_v6_ip", value=local_gateway_v6_ip, expected_type=type_hints["local_gateway_v6_ip"])
            check_type(argname="argument remote_gateway_v4_ip", value=remote_gateway_v4_ip, expected_type=type_hints["remote_gateway_v4_ip"])
            check_type(argname="argument remote_gateway_v6_ip", value=remote_gateway_v6_ip, expected_type=type_hints["remote_gateway_v6_ip"])
            check_type(argname="argument resource_tenant_id", value=resource_tenant_id, expected_type=type_hints["resource_tenant_id"])
            check_type(argname="argument service_ep_group", value=service_ep_group, expected_type=type_hints["service_ep_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bandwidth": bandwidth,
            "direct_connect_id": direct_connect_id,
            "name": name,
            "remote_ep_group": remote_ep_group,
            "route_mode": route_mode,
            "type": type,
            "vgw_id": vgw_id,
            "vlan": vlan,
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
        if address_family is not None:
            self._values["address_family"] = address_family
        if asn is not None:
            self._values["asn"] = asn
        if bgp_md5 is not None:
            self._values["bgp_md5"] = bgp_md5
        if description is not None:
            self._values["description"] = description
        if enable_bfd is not None:
            self._values["enable_bfd"] = enable_bfd
        if enable_nqa is not None:
            self._values["enable_nqa"] = enable_nqa
        if id is not None:
            self._values["id"] = id
        if lag_id is not None:
            self._values["lag_id"] = lag_id
        if local_gateway_v4_ip is not None:
            self._values["local_gateway_v4_ip"] = local_gateway_v4_ip
        if local_gateway_v6_ip is not None:
            self._values["local_gateway_v6_ip"] = local_gateway_v6_ip
        if remote_gateway_v4_ip is not None:
            self._values["remote_gateway_v4_ip"] = remote_gateway_v4_ip
        if remote_gateway_v6_ip is not None:
            self._values["remote_gateway_v6_ip"] = remote_gateway_v6_ip
        if resource_tenant_id is not None:
            self._values["resource_tenant_id"] = resource_tenant_id
        if service_ep_group is not None:
            self._values["service_ep_group"] = service_ep_group

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
    def bandwidth(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#bandwidth DcVirtualInterfaceV3#bandwidth}.'''
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def direct_connect_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#direct_connect_id DcVirtualInterfaceV3#direct_connect_id}.'''
        result = self._values.get("direct_connect_id")
        assert result is not None, "Required property 'direct_connect_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#name DcVirtualInterfaceV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_ep_group(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_ep_group DcVirtualInterfaceV3#remote_ep_group}.'''
        result = self._values.get("remote_ep_group")
        assert result is not None, "Required property 'remote_ep_group' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def route_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#route_mode DcVirtualInterfaceV3#route_mode}.'''
        result = self._values.get("route_mode")
        assert result is not None, "Required property 'route_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#type DcVirtualInterfaceV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vgw_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#vgw_id DcVirtualInterfaceV3#vgw_id}.'''
        result = self._values.get("vgw_id")
        assert result is not None, "Required property 'vgw_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vlan(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#vlan DcVirtualInterfaceV3#vlan}.'''
        result = self._values.get("vlan")
        assert result is not None, "Required property 'vlan' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def address_family(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#address_family DcVirtualInterfaceV3#address_family}.'''
        result = self._values.get("address_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#asn DcVirtualInterfaceV3#asn}.'''
        result = self._values.get("asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bgp_md5(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#bgp_md5 DcVirtualInterfaceV3#bgp_md5}.'''
        result = self._values.get("bgp_md5")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#description DcVirtualInterfaceV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_bfd(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#enable_bfd DcVirtualInterfaceV3#enable_bfd}.'''
        result = self._values.get("enable_bfd")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_nqa(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#enable_nqa DcVirtualInterfaceV3#enable_nqa}.'''
        result = self._values.get("enable_nqa")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#id DcVirtualInterfaceV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lag_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#lag_id DcVirtualInterfaceV3#lag_id}.'''
        result = self._values.get("lag_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_gateway_v4_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#local_gateway_v4_ip DcVirtualInterfaceV3#local_gateway_v4_ip}.'''
        result = self._values.get("local_gateway_v4_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_gateway_v6_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#local_gateway_v6_ip DcVirtualInterfaceV3#local_gateway_v6_ip}.'''
        result = self._values.get("local_gateway_v6_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_gateway_v4_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_gateway_v4_ip DcVirtualInterfaceV3#remote_gateway_v4_ip}.'''
        result = self._values.get("remote_gateway_v4_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_gateway_v6_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#remote_gateway_v6_ip DcVirtualInterfaceV3#remote_gateway_v6_ip}.'''
        result = self._values.get("remote_gateway_v6_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#resource_tenant_id DcVirtualInterfaceV3#resource_tenant_id}.'''
        result = self._values.get("resource_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_ep_group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v3#service_ep_group DcVirtualInterfaceV3#service_ep_group}.'''
        result = self._values.get("service_ep_group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualInterfaceV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV3.DcVirtualInterfaceV3VifPeers",
    jsii_struct_bases=[],
    name_mapping={},
)
class DcVirtualInterfaceV3VifPeers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualInterfaceV3VifPeers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcVirtualInterfaceV3VifPeersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV3.DcVirtualInterfaceV3VifPeersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86b3b1b2d1c248f9e89d484b71cc2f7e0d5df90b50ab86f71d7c0ad34819d306)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DcVirtualInterfaceV3VifPeersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb7ebf8fb446293d355fa2078c32f17657fbc4c1386e801b17cb1f54868dcc4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DcVirtualInterfaceV3VifPeersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3959605765eb51744e448ed3fa11d86e5216cc85aa24976d70bfc90f474257a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e50126b3bb1c4633673d340153783fc3cc14853aacb82684a181513bfbc76bb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f3438593bd8f3d798248e9c47d7e7e381cab8301f7b2b1064311d9baaebc031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DcVirtualInterfaceV3VifPeersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV3.DcVirtualInterfaceV3VifPeersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f9a5d07a38562c221511aeac19b0dcb48d177d55b78204ca626d3d59ddaba68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="addressFamily")
    def address_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressFamily"))

    @builtins.property
    @jsii.member(jsii_name="bgpAsn")
    def bgp_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bgpAsn"))

    @builtins.property
    @jsii.member(jsii_name="bgpMd5")
    def bgp_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpMd5"))

    @builtins.property
    @jsii.member(jsii_name="bgpRouteLimit")
    def bgp_route_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bgpRouteLimit"))

    @builtins.property
    @jsii.member(jsii_name="bgpStatus")
    def bgp_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpStatus"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @builtins.property
    @jsii.member(jsii_name="enableBfd")
    def enable_bfd(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableBfd"))

    @builtins.property
    @jsii.member(jsii_name="enableNqa")
    def enable_nqa(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableNqa"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="localGatewayIp")
    def local_gateway_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localGatewayIp"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="receiveRouteNum")
    def receive_route_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "receiveRouteNum"))

    @builtins.property
    @jsii.member(jsii_name="remoteEpGroup")
    def remote_ep_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteEpGroup"))

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayIp")
    def remote_gateway_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteGatewayIp"))

    @builtins.property
    @jsii.member(jsii_name="routeMode")
    def route_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeMode"))

    @builtins.property
    @jsii.member(jsii_name="serviceEpGroup")
    def service_ep_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceEpGroup"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="vifId")
    def vif_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vifId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DcVirtualInterfaceV3VifPeers]:
        return typing.cast(typing.Optional[DcVirtualInterfaceV3VifPeers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DcVirtualInterfaceV3VifPeers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e332bd3df4bd17d7246d96205c7bf7e354575448014e0025bccdd15e8927641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DcVirtualInterfaceV3",
    "DcVirtualInterfaceV3Config",
    "DcVirtualInterfaceV3VifPeers",
    "DcVirtualInterfaceV3VifPeersList",
    "DcVirtualInterfaceV3VifPeersOutputReference",
]

publication.publish()

def _typecheckingstub__4eab2369ac7b89bae3002cb15266e8bdd87f112a23eb24fbf2bb3774a8739ece(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bandwidth: jsii.Number,
    direct_connect_id: builtins.str,
    name: builtins.str,
    remote_ep_group: typing.Sequence[builtins.str],
    route_mode: builtins.str,
    type: builtins.str,
    vgw_id: builtins.str,
    vlan: jsii.Number,
    address_family: typing.Optional[builtins.str] = None,
    asn: typing.Optional[jsii.Number] = None,
    bgp_md5: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lag_id: typing.Optional[builtins.str] = None,
    local_gateway_v4_ip: typing.Optional[builtins.str] = None,
    local_gateway_v6_ip: typing.Optional[builtins.str] = None,
    remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
    remote_gateway_v6_ip: typing.Optional[builtins.str] = None,
    resource_tenant_id: typing.Optional[builtins.str] = None,
    service_ep_group: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__829267cadfa905ffa38ae1a68af9c3f587c9fec37ab4e8a668840e7f5b36150a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444e0343060d5efcade72e05b97b46208769de8974ac0b24ec883cc091462d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077d368f375496bb922b592be6f1a9459913c85aa86a12b9c94250205b5d9285(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dac45c5b6ed3614b828a6f172fa2fedc9805288c2067684e23bdff7b5ad4910(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e53edf538965d54ff598d1a8d42585456422b719113509da0fb7fb127c10e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4fc578a6259844172e21aa18a3877964c2584eb266772e38d222b7b45220e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e76f55b891f0653c123e28dd6428969569eb181d8975b928efab8bab7254ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4f98f799afe23a7bbfb9b4325580d0072d955ffce0ff769cd1b4afa15766d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d4b120abd494f0af598f0f1ed4f7f13f1738a469feaddea39dffce5b4f1ba6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8626001e2bda9dd26d2b4f6022279947af483ff31bd7969a3a922f221d6ae76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565fd3d50d211a9e0d697f16451e63bdd2e16a2ffdf3bfd49819f1924dddf5de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c990ce1bef2dd63bfac40f33ccd3b10ed4e11c4843d856e5c3fe82bcef91e87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0e2df91fddb53b2c15b10ab3907a55b9fb34254276886fea6f3223053155ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5c5df6a07ad51e6276c4e6a558ba57a984771de5b3bb04b42867df8f6c090a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7c3f344c374e1914a7934724a577e2eb977a9e0a855eb8dd4952854629ef7e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc9aca507f6ec71a3c55bf56a1a61b15a376641493095480a80db72ef8b0956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eade78280e711f0337eac010dc1a7bc2c9695730b84c43dfa845ce01a7e721a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d0a108e0d83b1640a67320971ab192c6b19215fe5152131f683d84dbd9e5d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e51ba1be2a9be179182ca49ff057ed72ad24bd9610f4f99a254643149785102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1063930769fc0500ec9887d1877c1227c25ea422a8456594338d342cd632e3d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2852fdfb166f7300464be31dabf3f2d04926a993ead5e8ae1d45685312ea53e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8664dfd4f5f6f72dbdc377338eddeff3fc7dbbe3fc4cc894dbf49e658fc2031a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8332673b40996214a207e3a3980e2b31a3172c2cad331efaef9a5ed7d9a8db5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ea08e2348d2dc6b31568bd5f794e0e220115c0363720d9413aa5f02c2ab4d1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bandwidth: jsii.Number,
    direct_connect_id: builtins.str,
    name: builtins.str,
    remote_ep_group: typing.Sequence[builtins.str],
    route_mode: builtins.str,
    type: builtins.str,
    vgw_id: builtins.str,
    vlan: jsii.Number,
    address_family: typing.Optional[builtins.str] = None,
    asn: typing.Optional[jsii.Number] = None,
    bgp_md5: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lag_id: typing.Optional[builtins.str] = None,
    local_gateway_v4_ip: typing.Optional[builtins.str] = None,
    local_gateway_v6_ip: typing.Optional[builtins.str] = None,
    remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
    remote_gateway_v6_ip: typing.Optional[builtins.str] = None,
    resource_tenant_id: typing.Optional[builtins.str] = None,
    service_ep_group: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b3b1b2d1c248f9e89d484b71cc2f7e0d5df90b50ab86f71d7c0ad34819d306(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb7ebf8fb446293d355fa2078c32f17657fbc4c1386e801b17cb1f54868dcc4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3959605765eb51744e448ed3fa11d86e5216cc85aa24976d70bfc90f474257a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50126b3bb1c4633673d340153783fc3cc14853aacb82684a181513bfbc76bb4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3438593bd8f3d798248e9c47d7e7e381cab8301f7b2b1064311d9baaebc031(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9a5d07a38562c221511aeac19b0dcb48d177d55b78204ca626d3d59ddaba68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e332bd3df4bd17d7246d96205c7bf7e354575448014e0025bccdd15e8927641(
    value: typing.Optional[DcVirtualInterfaceV3VifPeers],
) -> None:
    """Type checking stubs"""
    pass
