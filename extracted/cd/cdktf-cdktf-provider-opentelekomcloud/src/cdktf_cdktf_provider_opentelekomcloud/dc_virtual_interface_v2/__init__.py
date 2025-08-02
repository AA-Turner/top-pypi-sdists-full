r'''
# `opentelekomcloud_dc_virtual_interface_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dc_virtual_interface_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2).
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


class DcVirtualInterfaceV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV2.DcVirtualInterfaceV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2 opentelekomcloud_dc_virtual_interface_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bandwidth: jsii.Number,
        direct_connect_id: builtins.str,
        name: builtins.str,
        remote_ep_group: typing.Union["DcVirtualInterfaceV2RemoteEpGroup", typing.Dict[builtins.str, typing.Any]],
        route_mode: builtins.str,
        service_type: builtins.str,
        type: builtins.str,
        virtual_gateway_id: builtins.str,
        vlan: jsii.Number,
        asn: typing.Optional[jsii.Number] = None,
        bgp_md5: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lag_id: typing.Optional[builtins.str] = None,
        local_gateway_v4_ip: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2 opentelekomcloud_dc_virtual_interface_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#bandwidth DcVirtualInterfaceV2#bandwidth}.
        :param direct_connect_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#direct_connect_id DcVirtualInterfaceV2#direct_connect_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#name DcVirtualInterfaceV2#name}.
        :param remote_ep_group: remote_ep_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#remote_ep_group DcVirtualInterfaceV2#remote_ep_group}
        :param route_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#route_mode DcVirtualInterfaceV2#route_mode}.
        :param service_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#service_type DcVirtualInterfaceV2#service_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#type DcVirtualInterfaceV2#type}.
        :param virtual_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#virtual_gateway_id DcVirtualInterfaceV2#virtual_gateway_id}.
        :param vlan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#vlan DcVirtualInterfaceV2#vlan}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#asn DcVirtualInterfaceV2#asn}.
        :param bgp_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#bgp_md5 DcVirtualInterfaceV2#bgp_md5}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#description DcVirtualInterfaceV2#description}.
        :param enable_bfd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#enable_bfd DcVirtualInterfaceV2#enable_bfd}.
        :param enable_nqa: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#enable_nqa DcVirtualInterfaceV2#enable_nqa}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#id DcVirtualInterfaceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lag_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#lag_id DcVirtualInterfaceV2#lag_id}.
        :param local_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#local_gateway_v4_ip DcVirtualInterfaceV2#local_gateway_v4_ip}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#project_id DcVirtualInterfaceV2#project_id}.
        :param remote_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#remote_gateway_v4_ip DcVirtualInterfaceV2#remote_gateway_v4_ip}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a540aa6744b332a5e5e7811dcb71c318cf3d9bc4b2a292dc6d4c727449e81c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DcVirtualInterfaceV2Config(
            bandwidth=bandwidth,
            direct_connect_id=direct_connect_id,
            name=name,
            remote_ep_group=remote_ep_group,
            route_mode=route_mode,
            service_type=service_type,
            type=type,
            virtual_gateway_id=virtual_gateway_id,
            vlan=vlan,
            asn=asn,
            bgp_md5=bgp_md5,
            description=description,
            enable_bfd=enable_bfd,
            enable_nqa=enable_nqa,
            id=id,
            lag_id=lag_id,
            local_gateway_v4_ip=local_gateway_v4_ip,
            project_id=project_id,
            remote_gateway_v4_ip=remote_gateway_v4_ip,
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
        '''Generates CDKTF code for importing a DcVirtualInterfaceV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DcVirtualInterfaceV2 to import.
        :param import_from_id: The id of the existing DcVirtualInterfaceV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DcVirtualInterfaceV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbbdf28ac1fea27dd248953fb2a61c4e45c47e31a48a6d436ce7965b22bedf1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRemoteEpGroup")
    def put_remote_ep_group(
        self,
        *,
        endpoints: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#endpoints DcVirtualInterfaceV2#endpoints}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#description DcVirtualInterfaceV2#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#name DcVirtualInterfaceV2#name}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#project_id DcVirtualInterfaceV2#project_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#type DcVirtualInterfaceV2#type}.
        '''
        value = DcVirtualInterfaceV2RemoteEpGroup(
            endpoints=endpoints,
            description=description,
            name=name,
            project_id=project_id,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putRemoteEpGroup", [value]))

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

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRemoteGatewayV4Ip")
    def reset_remote_gateway_v4_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteGatewayV4Ip", []))

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
    @jsii.member(jsii_name="remoteEpGroup")
    def remote_ep_group(self) -> "DcVirtualInterfaceV2RemoteEpGroupOutputReference":
        return typing.cast("DcVirtualInterfaceV2RemoteEpGroupOutputReference", jsii.get(self, "remoteEpGroup"))

    @builtins.property
    @jsii.member(jsii_name="remoteEpGroupId")
    def remote_ep_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteEpGroupId"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteEpGroupInput")
    def remote_ep_group_input(
        self,
    ) -> typing.Optional["DcVirtualInterfaceV2RemoteEpGroup"]:
        return typing.cast(typing.Optional["DcVirtualInterfaceV2RemoteEpGroup"], jsii.get(self, "remoteEpGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayV4IpInput")
    def remote_gateway_v4_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteGatewayV4IpInput"))

    @builtins.property
    @jsii.member(jsii_name="routeModeInput")
    def route_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTypeInput")
    def service_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualGatewayIdInput")
    def virtual_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanInput")
    def vlan_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vlanInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cddbdfeae6840d97ed1f9e277d58d7b9f11db28aa3664c0130e618ae4cb8704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a1c90c08d41bc3c5db88ac686f61efd8e166f72af0fd9ca9966d2476457ad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpMd5")
    def bgp_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpMd5"))

    @bgp_md5.setter
    def bgp_md5(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02db0f41bdeb7f9857efd4cf24b8e4ec52d7b526ddd76caff4135909db77161a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpMd5", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a08979288207b51ade1b7710bb5266b36f26ea1276385e5b9885a761a8d03b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directConnectId")
    def direct_connect_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directConnectId"))

    @direct_connect_id.setter
    def direct_connect_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2084f3efcd1a125aea852903ce0c8e8439a57c8e1890f854206bb3db9b9284dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f708948b3223444bcd344e1c3337ac199374dc775ec4fc268eb351b0a27803)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bc2dfb4b49a32c31266dc39b96129291ad28631b908bbb0fd53634c796524e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNqa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a50b8d942e8da88e87fe491ccf474b9c7eb0603b4bef1603321a5debd84656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lagId")
    def lag_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lagId"))

    @lag_id.setter
    def lag_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f27af530734647f311f296e6bbb59d04228bcc72ae2c27780bb5a0356d6cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lagId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localGatewayV4Ip")
    def local_gateway_v4_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localGatewayV4Ip"))

    @local_gateway_v4_ip.setter
    def local_gateway_v4_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5cc8eb381f265f89bfc25ebbbf9bc8c164e853f19a18ebdc2e42483ced591ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localGatewayV4Ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea902cc830ed1d1acaf0cfa706985af1541605bcd33213d47224189bf5701ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd43d6c64bd8b0cdd9b03831c769a77fadb0c1ac6ff4e9201b86a61edc1749c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteGatewayV4Ip")
    def remote_gateway_v4_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteGatewayV4Ip"))

    @remote_gateway_v4_ip.setter
    def remote_gateway_v4_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f50f1c6816bd5435d3edeb9f8b7fa69a12613362f6a83731c9e7514da70be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteGatewayV4Ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeMode")
    def route_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeMode"))

    @route_mode.setter
    def route_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf574d4933993575e2294b1b4ac323f897a4c9810ece8a82d0b4d3cdc44af7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceType")
    def service_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceType"))

    @service_type.setter
    def service_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5fc8a679593ca18549238af68e875d0323932d4f932ad2a7a6d765c2796fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3642a0a307e030c95968af9b60816d938d67639b2329ccee9b2f52b0e95dc885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualGatewayId")
    def virtual_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayId"))

    @virtual_gateway_id.setter
    def virtual_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d250f0356115463402ab53f938d0d119c5838a0450d7425153f69f6669d8f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualGatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vlan")
    def vlan(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlan"))

    @vlan.setter
    def vlan(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01225565498a486ac9bcfbc74ae1a8ba091a1fd4ec87ea904e4f97e67f163c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlan", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV2.DcVirtualInterfaceV2Config",
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
        "service_type": "serviceType",
        "type": "type",
        "virtual_gateway_id": "virtualGatewayId",
        "vlan": "vlan",
        "asn": "asn",
        "bgp_md5": "bgpMd5",
        "description": "description",
        "enable_bfd": "enableBfd",
        "enable_nqa": "enableNqa",
        "id": "id",
        "lag_id": "lagId",
        "local_gateway_v4_ip": "localGatewayV4Ip",
        "project_id": "projectId",
        "remote_gateway_v4_ip": "remoteGatewayV4Ip",
    },
)
class DcVirtualInterfaceV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        remote_ep_group: typing.Union["DcVirtualInterfaceV2RemoteEpGroup", typing.Dict[builtins.str, typing.Any]],
        route_mode: builtins.str,
        service_type: builtins.str,
        type: builtins.str,
        virtual_gateway_id: builtins.str,
        vlan: jsii.Number,
        asn: typing.Optional[jsii.Number] = None,
        bgp_md5: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        lag_id: typing.Optional[builtins.str] = None,
        local_gateway_v4_ip: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#bandwidth DcVirtualInterfaceV2#bandwidth}.
        :param direct_connect_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#direct_connect_id DcVirtualInterfaceV2#direct_connect_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#name DcVirtualInterfaceV2#name}.
        :param remote_ep_group: remote_ep_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#remote_ep_group DcVirtualInterfaceV2#remote_ep_group}
        :param route_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#route_mode DcVirtualInterfaceV2#route_mode}.
        :param service_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#service_type DcVirtualInterfaceV2#service_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#type DcVirtualInterfaceV2#type}.
        :param virtual_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#virtual_gateway_id DcVirtualInterfaceV2#virtual_gateway_id}.
        :param vlan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#vlan DcVirtualInterfaceV2#vlan}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#asn DcVirtualInterfaceV2#asn}.
        :param bgp_md5: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#bgp_md5 DcVirtualInterfaceV2#bgp_md5}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#description DcVirtualInterfaceV2#description}.
        :param enable_bfd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#enable_bfd DcVirtualInterfaceV2#enable_bfd}.
        :param enable_nqa: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#enable_nqa DcVirtualInterfaceV2#enable_nqa}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#id DcVirtualInterfaceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lag_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#lag_id DcVirtualInterfaceV2#lag_id}.
        :param local_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#local_gateway_v4_ip DcVirtualInterfaceV2#local_gateway_v4_ip}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#project_id DcVirtualInterfaceV2#project_id}.
        :param remote_gateway_v4_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#remote_gateway_v4_ip DcVirtualInterfaceV2#remote_gateway_v4_ip}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(remote_ep_group, dict):
            remote_ep_group = DcVirtualInterfaceV2RemoteEpGroup(**remote_ep_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b762171ad98ee46eaf2b7e0733b232f931d853877973e05ca154119885e9d56)
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
            check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument virtual_gateway_id", value=virtual_gateway_id, expected_type=type_hints["virtual_gateway_id"])
            check_type(argname="argument vlan", value=vlan, expected_type=type_hints["vlan"])
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument bgp_md5", value=bgp_md5, expected_type=type_hints["bgp_md5"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_bfd", value=enable_bfd, expected_type=type_hints["enable_bfd"])
            check_type(argname="argument enable_nqa", value=enable_nqa, expected_type=type_hints["enable_nqa"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lag_id", value=lag_id, expected_type=type_hints["lag_id"])
            check_type(argname="argument local_gateway_v4_ip", value=local_gateway_v4_ip, expected_type=type_hints["local_gateway_v4_ip"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument remote_gateway_v4_ip", value=remote_gateway_v4_ip, expected_type=type_hints["remote_gateway_v4_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bandwidth": bandwidth,
            "direct_connect_id": direct_connect_id,
            "name": name,
            "remote_ep_group": remote_ep_group,
            "route_mode": route_mode,
            "service_type": service_type,
            "type": type,
            "virtual_gateway_id": virtual_gateway_id,
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
        if project_id is not None:
            self._values["project_id"] = project_id
        if remote_gateway_v4_ip is not None:
            self._values["remote_gateway_v4_ip"] = remote_gateway_v4_ip

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#bandwidth DcVirtualInterfaceV2#bandwidth}.'''
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def direct_connect_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#direct_connect_id DcVirtualInterfaceV2#direct_connect_id}.'''
        result = self._values.get("direct_connect_id")
        assert result is not None, "Required property 'direct_connect_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#name DcVirtualInterfaceV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_ep_group(self) -> "DcVirtualInterfaceV2RemoteEpGroup":
        '''remote_ep_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#remote_ep_group DcVirtualInterfaceV2#remote_ep_group}
        '''
        result = self._values.get("remote_ep_group")
        assert result is not None, "Required property 'remote_ep_group' is missing"
        return typing.cast("DcVirtualInterfaceV2RemoteEpGroup", result)

    @builtins.property
    def route_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#route_mode DcVirtualInterfaceV2#route_mode}.'''
        result = self._values.get("route_mode")
        assert result is not None, "Required property 'route_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#service_type DcVirtualInterfaceV2#service_type}.'''
        result = self._values.get("service_type")
        assert result is not None, "Required property 'service_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#type DcVirtualInterfaceV2#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#virtual_gateway_id DcVirtualInterfaceV2#virtual_gateway_id}.'''
        result = self._values.get("virtual_gateway_id")
        assert result is not None, "Required property 'virtual_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vlan(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#vlan DcVirtualInterfaceV2#vlan}.'''
        result = self._values.get("vlan")
        assert result is not None, "Required property 'vlan' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#asn DcVirtualInterfaceV2#asn}.'''
        result = self._values.get("asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bgp_md5(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#bgp_md5 DcVirtualInterfaceV2#bgp_md5}.'''
        result = self._values.get("bgp_md5")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#description DcVirtualInterfaceV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_bfd(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#enable_bfd DcVirtualInterfaceV2#enable_bfd}.'''
        result = self._values.get("enable_bfd")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_nqa(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#enable_nqa DcVirtualInterfaceV2#enable_nqa}.'''
        result = self._values.get("enable_nqa")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#id DcVirtualInterfaceV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lag_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#lag_id DcVirtualInterfaceV2#lag_id}.'''
        result = self._values.get("lag_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_gateway_v4_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#local_gateway_v4_ip DcVirtualInterfaceV2#local_gateway_v4_ip}.'''
        result = self._values.get("local_gateway_v4_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#project_id DcVirtualInterfaceV2#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_gateway_v4_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#remote_gateway_v4_ip DcVirtualInterfaceV2#remote_gateway_v4_ip}.'''
        result = self._values.get("remote_gateway_v4_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualInterfaceV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV2.DcVirtualInterfaceV2RemoteEpGroup",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints": "endpoints",
        "description": "description",
        "name": "name",
        "project_id": "projectId",
        "type": "type",
    },
)
class DcVirtualInterfaceV2RemoteEpGroup:
    def __init__(
        self,
        *,
        endpoints: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#endpoints DcVirtualInterfaceV2#endpoints}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#description DcVirtualInterfaceV2#description}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#name DcVirtualInterfaceV2#name}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#project_id DcVirtualInterfaceV2#project_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#type DcVirtualInterfaceV2#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e273a03433e9016077187ea56c2a6229c3a35a573e8a460daf4c0df94821fe9)
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoints": endpoints,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if project_id is not None:
            self._values["project_id"] = project_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def endpoints(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#endpoints DcVirtualInterfaceV2#endpoints}.'''
        result = self._values.get("endpoints")
        assert result is not None, "Required property 'endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#description DcVirtualInterfaceV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#name DcVirtualInterfaceV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#project_id DcVirtualInterfaceV2#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dc_virtual_interface_v2#type DcVirtualInterfaceV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcVirtualInterfaceV2RemoteEpGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcVirtualInterfaceV2RemoteEpGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcVirtualInterfaceV2.DcVirtualInterfaceV2RemoteEpGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__584d15dac75e936322486f969b547114ae5726bf24bbcebce9fa995c3431f1eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2bd1e900cc974e4541318ac8174bd85dda82c441b43903eaf7c6d3b10e8910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "endpoints"))

    @endpoints.setter
    def endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42466aac9a93ac8549947477c0b2a4b49ea9797fe2790102438992f03d2a247a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64ce5af769f3af19328f83b811dea50d760a3f66281ec394a106f9e675252b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c511cacd63ba054f3e57cb3ba008c832b49d62cd106cecca4755653160b8106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64d759ad7ccd0d2664ca902b620df57f9af2ab9e1c7f6b72e706e61fd478311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DcVirtualInterfaceV2RemoteEpGroup]:
        return typing.cast(typing.Optional[DcVirtualInterfaceV2RemoteEpGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DcVirtualInterfaceV2RemoteEpGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee87d385f1b04e820900ef609bcda09f5525239f5134fbc2d77af4a2338a68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DcVirtualInterfaceV2",
    "DcVirtualInterfaceV2Config",
    "DcVirtualInterfaceV2RemoteEpGroup",
    "DcVirtualInterfaceV2RemoteEpGroupOutputReference",
]

publication.publish()

def _typecheckingstub__8a540aa6744b332a5e5e7811dcb71c318cf3d9bc4b2a292dc6d4c727449e81c2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bandwidth: jsii.Number,
    direct_connect_id: builtins.str,
    name: builtins.str,
    remote_ep_group: typing.Union[DcVirtualInterfaceV2RemoteEpGroup, typing.Dict[builtins.str, typing.Any]],
    route_mode: builtins.str,
    service_type: builtins.str,
    type: builtins.str,
    virtual_gateway_id: builtins.str,
    vlan: jsii.Number,
    asn: typing.Optional[jsii.Number] = None,
    bgp_md5: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lag_id: typing.Optional[builtins.str] = None,
    local_gateway_v4_ip: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3dbbdf28ac1fea27dd248953fb2a61c4e45c47e31a48a6d436ce7965b22bedf1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cddbdfeae6840d97ed1f9e277d58d7b9f11db28aa3664c0130e618ae4cb8704(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a1c90c08d41bc3c5db88ac686f61efd8e166f72af0fd9ca9966d2476457ad6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02db0f41bdeb7f9857efd4cf24b8e4ec52d7b526ddd76caff4135909db77161a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a08979288207b51ade1b7710bb5266b36f26ea1276385e5b9885a761a8d03b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2084f3efcd1a125aea852903ce0c8e8439a57c8e1890f854206bb3db9b9284dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f708948b3223444bcd344e1c3337ac199374dc775ec4fc268eb351b0a27803(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc2dfb4b49a32c31266dc39b96129291ad28631b908bbb0fd53634c796524e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a50b8d942e8da88e87fe491ccf474b9c7eb0603b4bef1603321a5debd84656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f27af530734647f311f296e6bbb59d04228bcc72ae2c27780bb5a0356d6cb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cc8eb381f265f89bfc25ebbbf9bc8c164e853f19a18ebdc2e42483ced591ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea902cc830ed1d1acaf0cfa706985af1541605bcd33213d47224189bf5701ebd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd43d6c64bd8b0cdd9b03831c769a77fadb0c1ac6ff4e9201b86a61edc1749c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f50f1c6816bd5435d3edeb9f8b7fa69a12613362f6a83731c9e7514da70be3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf574d4933993575e2294b1b4ac323f897a4c9810ece8a82d0b4d3cdc44af7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5fc8a679593ca18549238af68e875d0323932d4f932ad2a7a6d765c2796fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3642a0a307e030c95968af9b60816d938d67639b2329ccee9b2f52b0e95dc885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d250f0356115463402ab53f938d0d119c5838a0450d7425153f69f6669d8f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01225565498a486ac9bcfbc74ae1a8ba091a1fd4ec87ea904e4f97e67f163c58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b762171ad98ee46eaf2b7e0733b232f931d853877973e05ca154119885e9d56(
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
    remote_ep_group: typing.Union[DcVirtualInterfaceV2RemoteEpGroup, typing.Dict[builtins.str, typing.Any]],
    route_mode: builtins.str,
    service_type: builtins.str,
    type: builtins.str,
    virtual_gateway_id: builtins.str,
    vlan: jsii.Number,
    asn: typing.Optional[jsii.Number] = None,
    bgp_md5: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_bfd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    lag_id: typing.Optional[builtins.str] = None,
    local_gateway_v4_ip: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    remote_gateway_v4_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e273a03433e9016077187ea56c2a6229c3a35a573e8a460daf4c0df94821fe9(
    *,
    endpoints: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584d15dac75e936322486f969b547114ae5726bf24bbcebce9fa995c3431f1eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2bd1e900cc974e4541318ac8174bd85dda82c441b43903eaf7c6d3b10e8910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42466aac9a93ac8549947477c0b2a4b49ea9797fe2790102438992f03d2a247a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64ce5af769f3af19328f83b811dea50d760a3f66281ec394a106f9e675252b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c511cacd63ba054f3e57cb3ba008c832b49d62cd106cecca4755653160b8106(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64d759ad7ccd0d2664ca902b620df57f9af2ab9e1c7f6b72e706e61fd478311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee87d385f1b04e820900ef609bcda09f5525239f5134fbc2d77af4a2338a68f(
    value: typing.Optional[DcVirtualInterfaceV2RemoteEpGroup],
) -> None:
    """Type checking stubs"""
    pass
