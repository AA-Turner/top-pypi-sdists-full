r'''
# `opentelekomcloud_dc_virtual_interface_peer_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dc_virtual_interface_peer_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3).
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


class DcVirtualInterfacePeerV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfacePeerV3.DcVirtualInterfacePeerV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3 opentelekomcloud_dc_virtual_interface_peer_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        address_family: builtins.str,
        local_gateway_ip: builtins.str,
        name: builtins.str,
        remote_ep_group: typing.Sequence[builtins.str],
        remote_gateway_ip: builtins.str,
        vif_id: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        bgp_md5: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        route_mode: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3 opentelekomcloud_dc_virtual_interface_peer_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param address_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#address_family DcVirtualInterfacePeerV3#address_family}.
        :param local_gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#local_gateway_ip DcVirtualInterfacePeerV3#local_gateway_ip}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#name DcVirtualInterfacePeerV3#name}.
        :param remote_ep_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#remote_ep_group DcVirtualInterfacePeerV3#remote_ep_group}.
        :param remote_gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#remote_gateway_ip DcVirtualInterfacePeerV3#remote_gateway_ip}.
        :param vif_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#vif_id DcVirtualInterfacePeerV3#vif_id}.
        :param bgp_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#bgp_asn DcVirtualInterfacePeerV3#bgp_asn}.
        :param bgp_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#bgp_md5 DcVirtualInterfacePeerV3#bgp_md5}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#description DcVirtualInterfacePeerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#id DcVirtualInterfacePeerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param route_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#route_mode DcVirtualInterfacePeerV3#route_mode}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff08fcd1810c7a0f9f4b2831404595802247dccc77886ba78cb87fdf6f1d20b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DcVirtualInterfacePeerV3Config(
            address_family=address_family,
            local_gateway_ip=local_gateway_ip,
            name=name,
            remote_ep_group=remote_ep_group,
            remote_gateway_ip=remote_gateway_ip,
            vif_id=vif_id,
            bgp_asn=bgp_asn,
            bgp_md5=bgp_md5,
            description=description,
            id=id,
            route_mode=route_mode,
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
        '''Generates CDKTF code for importing a DcVirtualInterfacePeerV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DcVirtualInterfacePeerV3 to import.
        :param import_from_id: The id of the existing DcVirtualInterfacePeerV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DcVirtualInterfacePeerV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87233d919f968d0e4014fd46b3629bf6de6b50228e004bc195d0f3461aa420d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetBgpAsn")
    def reset_bgp_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpAsn", []))

    @jsii.member(jsii_name="resetBgpMd5")
    def reset_bgp_md5(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpMd5", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRouteMode")
    def reset_route_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteMode", []))

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
    @jsii.member(jsii_name="bgpRouteLimit")
    def bgp_route_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bgpRouteLimit"))

    @builtins.property
    @jsii.member(jsii_name="bgpStatus")
    def bgp_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpStatus"))

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
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="receiveRouteNum")
    def receive_route_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "receiveRouteNum"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="serviceEpGroup")
    def service_ep_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceEpGroup"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="addressFamilyInput")
    def address_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpAsnInput")
    def bgp_asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bgpAsnInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpMd5Input")
    def bgp_md5_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpMd5Input"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localGatewayIpInput")
    def local_gateway_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localGatewayIpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteEpGroupInput")
    def remote_ep_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "remoteEpGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayIpInput")
    def remote_gateway_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteGatewayIpInput"))

    @builtins.property
    @jsii.member(jsii_name="routeModeInput")
    def route_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="vifIdInput")
    def vif_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vifIdInput"))

    @builtins.property
    @jsii.member(jsii_name="addressFamily")
    def address_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressFamily"))

    @address_family.setter
    def address_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7767caac2b9cde91908530f2d17eeecca124553a0851d292669390171b991afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpAsn")
    def bgp_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bgpAsn"))

    @bgp_asn.setter
    def bgp_asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c65955f9892f82a3110714fe8d690515277dedccc8678c77c4a0fa994293836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpAsn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpMd5")
    def bgp_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpMd5"))

    @bgp_md5.setter
    def bgp_md5(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52f23eb9a62376ac19ddf7d3dc10c200013c563280be7331ae6eae91941c4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpMd5", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0baee4a4454ab48f01f8ca21edf3bd8c7265a7f086b1ea2617657b3854ac5172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b8d39d96067dda7d7436481445a6bbb97a1ea4139847c83a081101aa36693e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localGatewayIp")
    def local_gateway_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localGatewayIp"))

    @local_gateway_ip.setter
    def local_gateway_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d094243fbdfb592f03fae84d33a0839a76a1f420a7e9976051c9cd7716d8760b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localGatewayIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7b7965b9806f8f49a255699f58517cb27e9e69131dea198c431cea931a4e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteEpGroup")
    def remote_ep_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteEpGroup"))

    @remote_ep_group.setter
    def remote_ep_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190723d4a8ab284985fb318632730ee3b7cfbbcffa482b70eb456a734a547ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteEpGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayIp")
    def remote_gateway_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteGatewayIp"))

    @remote_gateway_ip.setter
    def remote_gateway_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13ef846ff87b356b9872c2adbf284594f9273010e8819748b6a6849365cd30a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteGatewayIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeMode")
    def route_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeMode"))

    @route_mode.setter
    def route_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3c56a32fcb99ca993c21d48f34874b545a9b23c9029e9d88e5b45e4fb28b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vifId")
    def vif_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vifId"))

    @vif_id.setter
    def vif_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e510e4f6e0a6e7a5545d411e15c06c12616bd5c3d3b0f0c0daad79b154cde8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vifId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfacePeerV3.DcVirtualInterfacePeerV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "address_family": "addressFamily",
        "local_gateway_ip": "localGatewayIp",
        "name": "name",
        "remote_ep_group": "remoteEpGroup",
        "remote_gateway_ip": "remoteGatewayIp",
        "vif_id": "vifId",
        "bgp_asn": "bgpAsn",
        "bgp_md5": "bgpMd5",
        "description": "description",
        "id": "id",
        "route_mode": "routeMode",
    },
)
class DcVirtualInterfacePeerV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        address_family: builtins.str,
        local_gateway_ip: builtins.str,
        name: builtins.str,
        remote_ep_group: typing.Sequence[builtins.str],
        remote_gateway_ip: builtins.str,
        vif_id: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        bgp_md5: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        route_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param address_family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#address_family DcVirtualInterfacePeerV3#address_family}.
        :param local_gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#local_gateway_ip DcVirtualInterfacePeerV3#local_gateway_ip}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#name DcVirtualInterfacePeerV3#name}.
        :param remote_ep_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#remote_ep_group DcVirtualInterfacePeerV3#remote_ep_group}.
        :param remote_gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#remote_gateway_ip DcVirtualInterfacePeerV3#remote_gateway_ip}.
        :param vif_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#vif_id DcVirtualInterfacePeerV3#vif_id}.
        :param bgp_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#bgp_asn DcVirtualInterfacePeerV3#bgp_asn}.
        :param bgp_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#bgp_md5 DcVirtualInterfacePeerV3#bgp_md5}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#description DcVirtualInterfacePeerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#id DcVirtualInterfacePeerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param route_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#route_mode DcVirtualInterfacePeerV3#route_mode}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b91a3d5e23f1f1b03e96728eaecaa2b9c64878f5bedb4f05f30b4968d1da1c1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument address_family", value=address_family, expected_type=type_hints["address_family"])
            check_type(argname="argument local_gateway_ip", value=local_gateway_ip, expected_type=type_hints["local_gateway_ip"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument remote_ep_group", value=remote_ep_group, expected_type=type_hints["remote_ep_group"])
            check_type(argname="argument remote_gateway_ip", value=remote_gateway_ip, expected_type=type_hints["remote_gateway_ip"])
            check_type(argname="argument vif_id", value=vif_id, expected_type=type_hints["vif_id"])
            check_type(argname="argument bgp_asn", value=bgp_asn, expected_type=type_hints["bgp_asn"])
            check_type(argname="argument bgp_md5", value=bgp_md5, expected_type=type_hints["bgp_md5"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument route_mode", value=route_mode, expected_type=type_hints["route_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_family": address_family,
            "local_gateway_ip": local_gateway_ip,
            "name": name,
            "remote_ep_group": remote_ep_group,
            "remote_gateway_ip": remote_gateway_ip,
            "vif_id": vif_id,
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
        if bgp_asn is not None:
            self._values["bgp_asn"] = bgp_asn
        if bgp_md5 is not None:
            self._values["bgp_md5"] = bgp_md5
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if route_mode is not None:
            self._values["route_mode"] = route_mode

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
    def address_family(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#address_family DcVirtualInterfacePeerV3#address_family}.'''
        result = self._values.get("address_family")
        assert result is not None, "Required property 'address_family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_gateway_ip(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#local_gateway_ip DcVirtualInterfacePeerV3#local_gateway_ip}.'''
        result = self._values.get("local_gateway_ip")
        assert result is not None, "Required property 'local_gateway_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#name DcVirtualInterfacePeerV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_ep_group(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#remote_ep_group DcVirtualInterfacePeerV3#remote_ep_group}.'''
        result = self._values.get("remote_ep_group")
        assert result is not None, "Required property 'remote_ep_group' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def remote_gateway_ip(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#remote_gateway_ip DcVirtualInterfacePeerV3#remote_gateway_ip}.'''
        result = self._values.get("remote_gateway_ip")
        assert result is not None, "Required property 'remote_gateway_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vif_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#vif_id DcVirtualInterfacePeerV3#vif_id}.'''
        result = self._values.get("vif_id")
        assert result is not None, "Required property 'vif_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bgp_asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#bgp_asn DcVirtualInterfacePeerV3#bgp_asn}.'''
        result = self._values.get("bgp_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bgp_md5(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#bgp_md5 DcVirtualInterfacePeerV3#bgp_md5}.'''
        result = self._values.get("bgp_md5")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#description DcVirtualInterfacePeerV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#id DcVirtualInterfacePeerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_peer_v3#route_mode DcVirtualInterfacePeerV3#route_mode}.'''
        result = self._values.get("route_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualInterfacePeerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DcVirtualInterfacePeerV3",
    "DcVirtualInterfacePeerV3Config",
]

publication.publish()

def _typecheckingstub__0ff08fcd1810c7a0f9f4b2831404595802247dccc77886ba78cb87fdf6f1d20b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    address_family: builtins.str,
    local_gateway_ip: builtins.str,
    name: builtins.str,
    remote_ep_group: typing.Sequence[builtins.str],
    remote_gateway_ip: builtins.str,
    vif_id: builtins.str,
    bgp_asn: typing.Optional[jsii.Number] = None,
    bgp_md5: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    route_mode: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__87233d919f968d0e4014fd46b3629bf6de6b50228e004bc195d0f3461aa420d4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7767caac2b9cde91908530f2d17eeecca124553a0851d292669390171b991afc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c65955f9892f82a3110714fe8d690515277dedccc8678c77c4a0fa994293836(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52f23eb9a62376ac19ddf7d3dc10c200013c563280be7331ae6eae91941c4ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baee4a4454ab48f01f8ca21edf3bd8c7265a7f086b1ea2617657b3854ac5172(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b8d39d96067dda7d7436481445a6bbb97a1ea4139847c83a081101aa36693e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d094243fbdfb592f03fae84d33a0839a76a1f420a7e9976051c9cd7716d8760b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7b7965b9806f8f49a255699f58517cb27e9e69131dea198c431cea931a4e68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190723d4a8ab284985fb318632730ee3b7cfbbcffa482b70eb456a734a547ecb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13ef846ff87b356b9872c2adbf284594f9273010e8819748b6a6849365cd30a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3c56a32fcb99ca993c21d48f34874b545a9b23c9029e9d88e5b45e4fb28b90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e510e4f6e0a6e7a5545d411e15c06c12616bd5c3d3b0f0c0daad79b154cde8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b91a3d5e23f1f1b03e96728eaecaa2b9c64878f5bedb4f05f30b4968d1da1c1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    address_family: builtins.str,
    local_gateway_ip: builtins.str,
    name: builtins.str,
    remote_ep_group: typing.Sequence[builtins.str],
    remote_gateway_ip: builtins.str,
    vif_id: builtins.str,
    bgp_asn: typing.Optional[jsii.Number] = None,
    bgp_md5: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    route_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
