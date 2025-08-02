r'''
# `opentelekomcloud_enterprise_vpn_gateway_v5`

Refer to the Terraform Registry for docs: [`opentelekomcloud_enterprise_vpn_gateway_v5`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5).
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


class EnterpriseVpnGatewayV5(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5 opentelekomcloud_enterprise_vpn_gateway_v5}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zones: typing.Sequence[builtins.str],
        name: builtins.str,
        access_private_ip1: typing.Optional[builtins.str] = None,
        access_private_ip2: typing.Optional[builtins.str] = None,
        access_subnet_id: typing.Optional[builtins.str] = None,
        access_vpc_id: typing.Optional[builtins.str] = None,
        asn: typing.Optional[jsii.Number] = None,
        attachment_type: typing.Optional[builtins.str] = None,
        connect_subnet: typing.Optional[builtins.str] = None,
        delete_eip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        eip1: typing.Optional[typing.Union["EnterpriseVpnGatewayV5Eip1", typing.Dict[builtins.str, typing.Any]]] = None,
        eip2: typing.Optional[typing.Union["EnterpriseVpnGatewayV5Eip2", typing.Dict[builtins.str, typing.Any]]] = None,
        er_id: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        ha_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EnterpriseVpnGatewayV5Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5 opentelekomcloud_enterprise_vpn_gateway_v5} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#availability_zones EnterpriseVpnGatewayV5#availability_zones}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#name EnterpriseVpnGatewayV5#name}.
        :param access_private_ip1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_private_ip_1 EnterpriseVpnGatewayV5#access_private_ip_1}.
        :param access_private_ip2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_private_ip_2 EnterpriseVpnGatewayV5#access_private_ip_2}.
        :param access_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_subnet_id EnterpriseVpnGatewayV5#access_subnet_id}.
        :param access_vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_vpc_id EnterpriseVpnGatewayV5#access_vpc_id}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#asn EnterpriseVpnGatewayV5#asn}.
        :param attachment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#attachment_type EnterpriseVpnGatewayV5#attachment_type}.
        :param connect_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#connect_subnet EnterpriseVpnGatewayV5#connect_subnet}.
        :param delete_eip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#delete_eip EnterpriseVpnGatewayV5#delete_eip}.
        :param eip1: eip1 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#eip1 EnterpriseVpnGatewayV5#eip1}
        :param eip2: eip2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#eip2 EnterpriseVpnGatewayV5#eip2}
        :param er_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#er_id EnterpriseVpnGatewayV5#er_id}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#flavor EnterpriseVpnGatewayV5#flavor}.
        :param ha_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#ha_mode EnterpriseVpnGatewayV5#ha_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#local_subnets EnterpriseVpnGatewayV5#local_subnets}.
        :param network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#network_type EnterpriseVpnGatewayV5#network_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#tags EnterpriseVpnGatewayV5#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#timeouts EnterpriseVpnGatewayV5#timeouts}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#vpc_id EnterpriseVpnGatewayV5#vpc_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cf953b342d24ac1a2e0190aad01e0bfc6ba63e932a13e4f806f49eac3d3bbb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EnterpriseVpnGatewayV5Config(
            availability_zones=availability_zones,
            name=name,
            access_private_ip1=access_private_ip1,
            access_private_ip2=access_private_ip2,
            access_subnet_id=access_subnet_id,
            access_vpc_id=access_vpc_id,
            asn=asn,
            attachment_type=attachment_type,
            connect_subnet=connect_subnet,
            delete_eip=delete_eip,
            eip1=eip1,
            eip2=eip2,
            er_id=er_id,
            flavor=flavor,
            ha_mode=ha_mode,
            id=id,
            local_subnets=local_subnets,
            network_type=network_type,
            tags=tags,
            timeouts=timeouts,
            vpc_id=vpc_id,
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
        '''Generates CDKTF code for importing a EnterpriseVpnGatewayV5 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EnterpriseVpnGatewayV5 to import.
        :param import_from_id: The id of the existing EnterpriseVpnGatewayV5 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EnterpriseVpnGatewayV5 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8748637b5eda4216616ba5727e5a102c9f26ae37f6aad1e1a4b959e25b3ffad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEip1")
    def put_eip1(
        self,
        *,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        charge_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_name EnterpriseVpnGatewayV5#bandwidth_name}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_size EnterpriseVpnGatewayV5#bandwidth_size}.
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#charge_mode EnterpriseVpnGatewayV5#charge_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#type EnterpriseVpnGatewayV5#type}.
        '''
        value = EnterpriseVpnGatewayV5Eip1(
            bandwidth_name=bandwidth_name,
            bandwidth_size=bandwidth_size,
            charge_mode=charge_mode,
            id=id,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putEip1", [value]))

    @jsii.member(jsii_name="putEip2")
    def put_eip2(
        self,
        *,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        charge_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_name EnterpriseVpnGatewayV5#bandwidth_name}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_size EnterpriseVpnGatewayV5#bandwidth_size}.
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#charge_mode EnterpriseVpnGatewayV5#charge_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#type EnterpriseVpnGatewayV5#type}.
        '''
        value = EnterpriseVpnGatewayV5Eip2(
            bandwidth_name=bandwidth_name,
            bandwidth_size=bandwidth_size,
            charge_mode=charge_mode,
            id=id,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putEip2", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#create EnterpriseVpnGatewayV5#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#delete EnterpriseVpnGatewayV5#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#update EnterpriseVpnGatewayV5#update}.
        '''
        value = EnterpriseVpnGatewayV5Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessPrivateIp1")
    def reset_access_private_ip1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessPrivateIp1", []))

    @jsii.member(jsii_name="resetAccessPrivateIp2")
    def reset_access_private_ip2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessPrivateIp2", []))

    @jsii.member(jsii_name="resetAccessSubnetId")
    def reset_access_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessSubnetId", []))

    @jsii.member(jsii_name="resetAccessVpcId")
    def reset_access_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessVpcId", []))

    @jsii.member(jsii_name="resetAsn")
    def reset_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsn", []))

    @jsii.member(jsii_name="resetAttachmentType")
    def reset_attachment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttachmentType", []))

    @jsii.member(jsii_name="resetConnectSubnet")
    def reset_connect_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectSubnet", []))

    @jsii.member(jsii_name="resetDeleteEip")
    def reset_delete_eip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteEip", []))

    @jsii.member(jsii_name="resetEip1")
    def reset_eip1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEip1", []))

    @jsii.member(jsii_name="resetEip2")
    def reset_eip2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEip2", []))

    @jsii.member(jsii_name="resetErId")
    def reset_er_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErId", []))

    @jsii.member(jsii_name="resetFlavor")
    def reset_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavor", []))

    @jsii.member(jsii_name="resetHaMode")
    def reset_ha_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalSubnets")
    def reset_local_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSubnets", []))

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVpcId")
    def reset_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcId", []))

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
    @jsii.member(jsii_name="eip1")
    def eip1(self) -> "EnterpriseVpnGatewayV5Eip1OutputReference":
        return typing.cast("EnterpriseVpnGatewayV5Eip1OutputReference", jsii.get(self, "eip1"))

    @builtins.property
    @jsii.member(jsii_name="eip2")
    def eip2(self) -> "EnterpriseVpnGatewayV5Eip2OutputReference":
        return typing.cast("EnterpriseVpnGatewayV5Eip2OutputReference", jsii.get(self, "eip2"))

    @builtins.property
    @jsii.member(jsii_name="erAttachmentId")
    def er_attachment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "erAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "EnterpriseVpnGatewayV5TimeoutsOutputReference":
        return typing.cast("EnterpriseVpnGatewayV5TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="usedConnectionGroup")
    def used_connection_group(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedConnectionGroup"))

    @builtins.property
    @jsii.member(jsii_name="usedConnectionNumber")
    def used_connection_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedConnectionNumber"))

    @builtins.property
    @jsii.member(jsii_name="accessPrivateIp1Input")
    def access_private_ip1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPrivateIp1Input"))

    @builtins.property
    @jsii.member(jsii_name="accessPrivateIp2Input")
    def access_private_ip2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPrivateIp2Input"))

    @builtins.property
    @jsii.member(jsii_name="accessSubnetIdInput")
    def access_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessVpcIdInput")
    def access_vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessVpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="attachmentTypeInput")
    def attachment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attachmentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectSubnetInput")
    def connect_subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectSubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteEipInput")
    def delete_eip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteEipInput"))

    @builtins.property
    @jsii.member(jsii_name="eip1Input")
    def eip1_input(self) -> typing.Optional["EnterpriseVpnGatewayV5Eip1"]:
        return typing.cast(typing.Optional["EnterpriseVpnGatewayV5Eip1"], jsii.get(self, "eip1Input"))

    @builtins.property
    @jsii.member(jsii_name="eip2Input")
    def eip2_input(self) -> typing.Optional["EnterpriseVpnGatewayV5Eip2"]:
        return typing.cast(typing.Optional["EnterpriseVpnGatewayV5Eip2"], jsii.get(self, "eip2Input"))

    @builtins.property
    @jsii.member(jsii_name="erIdInput")
    def er_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "erIdInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="haModeInput")
    def ha_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haModeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localSubnetsInput")
    def local_subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "localSubnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EnterpriseVpnGatewayV5Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EnterpriseVpnGatewayV5Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessPrivateIp1")
    def access_private_ip1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessPrivateIp1"))

    @access_private_ip1.setter
    def access_private_ip1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61cda79359ba2abcb659468771aa1f0beb0bf7fe8f6fe8f12ed65d3be936f735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPrivateIp1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessPrivateIp2")
    def access_private_ip2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessPrivateIp2"))

    @access_private_ip2.setter
    def access_private_ip2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710e00b74323e68a181e6106479cec7dcf2b0f60aeca1b904c8231b60a80e159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPrivateIp2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessSubnetId")
    def access_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessSubnetId"))

    @access_subnet_id.setter
    def access_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f123452a9908a0cfd4217a8ca7e0d048fe5c610e85b2635e252f9f4e384d9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessVpcId")
    def access_vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessVpcId"))

    @access_vpc_id.setter
    def access_vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3995b11f1bfdc5777201d624af627582f8e7247438b37974bfa861fcad4d4c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessVpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dffde3ed523c53895c6e62679d9dfdf32b90928471d3a9d2b8d09ba578e80e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attachmentType")
    def attachment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attachmentType"))

    @attachment_type.setter
    def attachment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103337f3e462f91aca6f7ebfa804866b770516754580388fa6affe80843c035a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attachmentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a234a56c60888c8039902ad9f3c49ea0b9920d1970f1660a2b2b365f1ce286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectSubnet")
    def connect_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectSubnet"))

    @connect_subnet.setter
    def connect_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb91fcc154007509d8c20fad3cc1ff96012cde0997583f18ddfc0d5283b6acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectSubnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteEip")
    def delete_eip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteEip"))

    @delete_eip.setter
    def delete_eip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f5fc42e663bd12b68452a4be870daa5e7ff27d4d3e5dcc59d944372e9db892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteEip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="erId")
    def er_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "erId"))

    @er_id.setter
    def er_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4719e613443520b87af6fd8fc74a842b5c3b59b1da1b289974e374224f145a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "erId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3873e05af5c894bf189a6abb24ce655c7e5389ea312aa715e208feb2ac67039d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="haMode")
    def ha_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haMode"))

    @ha_mode.setter
    def ha_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6132e1cec113b0a6b91e5b01a5d31d8c19a0a8945a74ee9c020ff5d68f04649a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883922ae58d4e9d9406703d42cda40fac0119e5f04b4d02b6bff53caa3242023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSubnets")
    def local_subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "localSubnets"))

    @local_subnets.setter
    def local_subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95a65f31231a95e07140da67fa39ee788351565826ece7d7563c14b5af87cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13aa61e010bdc48802a7426d22efcd4ccc33a0b5858fd33b28d22fa2f0d5e14d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d60ff1bb753408c3d5396bbafafa66bb7905a9e72df503019fa973f0c48e4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356268f0f8bb458cfbd090bea69c50259a616264faf07d8444661b0a3413c5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f881b860a905532ce2ca976c5c7c33a03e9abc242a1893eecfcfbc6ec1fb6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zones": "availabilityZones",
        "name": "name",
        "access_private_ip1": "accessPrivateIp1",
        "access_private_ip2": "accessPrivateIp2",
        "access_subnet_id": "accessSubnetId",
        "access_vpc_id": "accessVpcId",
        "asn": "asn",
        "attachment_type": "attachmentType",
        "connect_subnet": "connectSubnet",
        "delete_eip": "deleteEip",
        "eip1": "eip1",
        "eip2": "eip2",
        "er_id": "erId",
        "flavor": "flavor",
        "ha_mode": "haMode",
        "id": "id",
        "local_subnets": "localSubnets",
        "network_type": "networkType",
        "tags": "tags",
        "timeouts": "timeouts",
        "vpc_id": "vpcId",
    },
)
class EnterpriseVpnGatewayV5Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zones: typing.Sequence[builtins.str],
        name: builtins.str,
        access_private_ip1: typing.Optional[builtins.str] = None,
        access_private_ip2: typing.Optional[builtins.str] = None,
        access_subnet_id: typing.Optional[builtins.str] = None,
        access_vpc_id: typing.Optional[builtins.str] = None,
        asn: typing.Optional[jsii.Number] = None,
        attachment_type: typing.Optional[builtins.str] = None,
        connect_subnet: typing.Optional[builtins.str] = None,
        delete_eip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        eip1: typing.Optional[typing.Union["EnterpriseVpnGatewayV5Eip1", typing.Dict[builtins.str, typing.Any]]] = None,
        eip2: typing.Optional[typing.Union["EnterpriseVpnGatewayV5Eip2", typing.Dict[builtins.str, typing.Any]]] = None,
        er_id: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        ha_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EnterpriseVpnGatewayV5Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#availability_zones EnterpriseVpnGatewayV5#availability_zones}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#name EnterpriseVpnGatewayV5#name}.
        :param access_private_ip1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_private_ip_1 EnterpriseVpnGatewayV5#access_private_ip_1}.
        :param access_private_ip2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_private_ip_2 EnterpriseVpnGatewayV5#access_private_ip_2}.
        :param access_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_subnet_id EnterpriseVpnGatewayV5#access_subnet_id}.
        :param access_vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_vpc_id EnterpriseVpnGatewayV5#access_vpc_id}.
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#asn EnterpriseVpnGatewayV5#asn}.
        :param attachment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#attachment_type EnterpriseVpnGatewayV5#attachment_type}.
        :param connect_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#connect_subnet EnterpriseVpnGatewayV5#connect_subnet}.
        :param delete_eip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#delete_eip EnterpriseVpnGatewayV5#delete_eip}.
        :param eip1: eip1 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#eip1 EnterpriseVpnGatewayV5#eip1}
        :param eip2: eip2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#eip2 EnterpriseVpnGatewayV5#eip2}
        :param er_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#er_id EnterpriseVpnGatewayV5#er_id}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#flavor EnterpriseVpnGatewayV5#flavor}.
        :param ha_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#ha_mode EnterpriseVpnGatewayV5#ha_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#local_subnets EnterpriseVpnGatewayV5#local_subnets}.
        :param network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#network_type EnterpriseVpnGatewayV5#network_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#tags EnterpriseVpnGatewayV5#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#timeouts EnterpriseVpnGatewayV5#timeouts}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#vpc_id EnterpriseVpnGatewayV5#vpc_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(eip1, dict):
            eip1 = EnterpriseVpnGatewayV5Eip1(**eip1)
        if isinstance(eip2, dict):
            eip2 = EnterpriseVpnGatewayV5Eip2(**eip2)
        if isinstance(timeouts, dict):
            timeouts = EnterpriseVpnGatewayV5Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c733090f4c83204ed91f474a67458a34c07e021f81f010d99f6bc6b0939fb7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_private_ip1", value=access_private_ip1, expected_type=type_hints["access_private_ip1"])
            check_type(argname="argument access_private_ip2", value=access_private_ip2, expected_type=type_hints["access_private_ip2"])
            check_type(argname="argument access_subnet_id", value=access_subnet_id, expected_type=type_hints["access_subnet_id"])
            check_type(argname="argument access_vpc_id", value=access_vpc_id, expected_type=type_hints["access_vpc_id"])
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument attachment_type", value=attachment_type, expected_type=type_hints["attachment_type"])
            check_type(argname="argument connect_subnet", value=connect_subnet, expected_type=type_hints["connect_subnet"])
            check_type(argname="argument delete_eip", value=delete_eip, expected_type=type_hints["delete_eip"])
            check_type(argname="argument eip1", value=eip1, expected_type=type_hints["eip1"])
            check_type(argname="argument eip2", value=eip2, expected_type=type_hints["eip2"])
            check_type(argname="argument er_id", value=er_id, expected_type=type_hints["er_id"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument ha_mode", value=ha_mode, expected_type=type_hints["ha_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_subnets", value=local_subnets, expected_type=type_hints["local_subnets"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zones": availability_zones,
            "name": name,
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
        if access_private_ip1 is not None:
            self._values["access_private_ip1"] = access_private_ip1
        if access_private_ip2 is not None:
            self._values["access_private_ip2"] = access_private_ip2
        if access_subnet_id is not None:
            self._values["access_subnet_id"] = access_subnet_id
        if access_vpc_id is not None:
            self._values["access_vpc_id"] = access_vpc_id
        if asn is not None:
            self._values["asn"] = asn
        if attachment_type is not None:
            self._values["attachment_type"] = attachment_type
        if connect_subnet is not None:
            self._values["connect_subnet"] = connect_subnet
        if delete_eip is not None:
            self._values["delete_eip"] = delete_eip
        if eip1 is not None:
            self._values["eip1"] = eip1
        if eip2 is not None:
            self._values["eip2"] = eip2
        if er_id is not None:
            self._values["er_id"] = er_id
        if flavor is not None:
            self._values["flavor"] = flavor
        if ha_mode is not None:
            self._values["ha_mode"] = ha_mode
        if id is not None:
            self._values["id"] = id
        if local_subnets is not None:
            self._values["local_subnets"] = local_subnets
        if network_type is not None:
            self._values["network_type"] = network_type
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

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
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#availability_zones EnterpriseVpnGatewayV5#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#name EnterpriseVpnGatewayV5#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_private_ip1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_private_ip_1 EnterpriseVpnGatewayV5#access_private_ip_1}.'''
        result = self._values.get("access_private_ip1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_private_ip2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_private_ip_2 EnterpriseVpnGatewayV5#access_private_ip_2}.'''
        result = self._values.get("access_private_ip2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_subnet_id EnterpriseVpnGatewayV5#access_subnet_id}.'''
        result = self._values.get("access_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#access_vpc_id EnterpriseVpnGatewayV5#access_vpc_id}.'''
        result = self._values.get("access_vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#asn EnterpriseVpnGatewayV5#asn}.'''
        result = self._values.get("asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def attachment_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#attachment_type EnterpriseVpnGatewayV5#attachment_type}.'''
        result = self._values.get("attachment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_subnet(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#connect_subnet EnterpriseVpnGatewayV5#connect_subnet}.'''
        result = self._values.get("connect_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_eip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#delete_eip EnterpriseVpnGatewayV5#delete_eip}.'''
        result = self._values.get("delete_eip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def eip1(self) -> typing.Optional["EnterpriseVpnGatewayV5Eip1"]:
        '''eip1 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#eip1 EnterpriseVpnGatewayV5#eip1}
        '''
        result = self._values.get("eip1")
        return typing.cast(typing.Optional["EnterpriseVpnGatewayV5Eip1"], result)

    @builtins.property
    def eip2(self) -> typing.Optional["EnterpriseVpnGatewayV5Eip2"]:
        '''eip2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#eip2 EnterpriseVpnGatewayV5#eip2}
        '''
        result = self._values.get("eip2")
        return typing.cast(typing.Optional["EnterpriseVpnGatewayV5Eip2"], result)

    @builtins.property
    def er_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#er_id EnterpriseVpnGatewayV5#er_id}.'''
        result = self._values.get("er_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#flavor EnterpriseVpnGatewayV5#flavor}.'''
        result = self._values.get("flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#ha_mode EnterpriseVpnGatewayV5#ha_mode}.'''
        result = self._values.get("ha_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#local_subnets EnterpriseVpnGatewayV5#local_subnets}.'''
        result = self._values.get("local_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#network_type EnterpriseVpnGatewayV5#network_type}.'''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#tags EnterpriseVpnGatewayV5#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EnterpriseVpnGatewayV5Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#timeouts EnterpriseVpnGatewayV5#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EnterpriseVpnGatewayV5Timeouts"], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#vpc_id EnterpriseVpnGatewayV5#vpc_id}.'''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnGatewayV5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5Eip1",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth_name": "bandwidthName",
        "bandwidth_size": "bandwidthSize",
        "charge_mode": "chargeMode",
        "id": "id",
        "type": "type",
    },
)
class EnterpriseVpnGatewayV5Eip1:
    def __init__(
        self,
        *,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        charge_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_name EnterpriseVpnGatewayV5#bandwidth_name}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_size EnterpriseVpnGatewayV5#bandwidth_size}.
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#charge_mode EnterpriseVpnGatewayV5#charge_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#type EnterpriseVpnGatewayV5#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec12cc7d8dca19984402265fb3573de6ec1f5cafe18f7f0aef771b7af359c53)
            check_type(argname="argument bandwidth_name", value=bandwidth_name, expected_type=type_hints["bandwidth_name"])
            check_type(argname="argument bandwidth_size", value=bandwidth_size, expected_type=type_hints["bandwidth_size"])
            check_type(argname="argument charge_mode", value=charge_mode, expected_type=type_hints["charge_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bandwidth_name is not None:
            self._values["bandwidth_name"] = bandwidth_name
        if bandwidth_size is not None:
            self._values["bandwidth_size"] = bandwidth_size
        if charge_mode is not None:
            self._values["charge_mode"] = charge_mode
        if id is not None:
            self._values["id"] = id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def bandwidth_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_name EnterpriseVpnGatewayV5#bandwidth_name}.'''
        result = self._values.get("bandwidth_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_size EnterpriseVpnGatewayV5#bandwidth_size}.'''
        result = self._values.get("bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def charge_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#charge_mode EnterpriseVpnGatewayV5#charge_mode}.'''
        result = self._values.get("charge_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#type EnterpriseVpnGatewayV5#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnGatewayV5Eip1(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpnGatewayV5Eip1OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5Eip1OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8092077a6dcc4c7140521b9aceafb7e82b12d5e63c0f35ee33640559605a073b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBandwidthName")
    def reset_bandwidth_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthName", []))

    @jsii.member(jsii_name="resetBandwidthSize")
    def reset_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthSize", []))

    @jsii.member(jsii_name="resetChargeMode")
    def reset_charge_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChargeMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="bandwidthId")
    def bandwidth_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthId"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ipVersion"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthNameInput")
    def bandwidth_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSizeInput")
    def bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="chargeModeInput")
    def charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthName")
    def bandwidth_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthName"))

    @bandwidth_name.setter
    def bandwidth_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f061c7c9a58bb27332c803f8a7db343a068d6b37fe0b0c0ce5c8b71783ef2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @bandwidth_size.setter
    def bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3e74101376b3f5614b285f1871450c56c9037fd673ee4c7cb45f58e445522e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chargeMode")
    def charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargeMode"))

    @charge_mode.setter
    def charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec00c46c981e5d3dfc8c6745be3c37f54897b4c0b4ce57ecc4a53fd34e82e796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chargeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d604678d4d0fe2ac75a9af4e0a880a46511981e6ed0a65df27205824bffb573a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed9e8038700ea2cf8132f220044b8fcfe2f71dc5b4e5ade7f5ef4c5ba2bf3c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnterpriseVpnGatewayV5Eip1]:
        return typing.cast(typing.Optional[EnterpriseVpnGatewayV5Eip1], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnterpriseVpnGatewayV5Eip1],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89ec976edf5b2e75ac17a290d4f363d9cd6d7c9d2b67854bf78cdac0133c548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5Eip2",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth_name": "bandwidthName",
        "bandwidth_size": "bandwidthSize",
        "charge_mode": "chargeMode",
        "id": "id",
        "type": "type",
    },
)
class EnterpriseVpnGatewayV5Eip2:
    def __init__(
        self,
        *,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        charge_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_name EnterpriseVpnGatewayV5#bandwidth_name}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_size EnterpriseVpnGatewayV5#bandwidth_size}.
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#charge_mode EnterpriseVpnGatewayV5#charge_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#type EnterpriseVpnGatewayV5#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49537a611d8b0e8e68c488afa20fc671c236d4c33c75e15bc4ab171686356ee7)
            check_type(argname="argument bandwidth_name", value=bandwidth_name, expected_type=type_hints["bandwidth_name"])
            check_type(argname="argument bandwidth_size", value=bandwidth_size, expected_type=type_hints["bandwidth_size"])
            check_type(argname="argument charge_mode", value=charge_mode, expected_type=type_hints["charge_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bandwidth_name is not None:
            self._values["bandwidth_name"] = bandwidth_name
        if bandwidth_size is not None:
            self._values["bandwidth_size"] = bandwidth_size
        if charge_mode is not None:
            self._values["charge_mode"] = charge_mode
        if id is not None:
            self._values["id"] = id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def bandwidth_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_name EnterpriseVpnGatewayV5#bandwidth_name}.'''
        result = self._values.get("bandwidth_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#bandwidth_size EnterpriseVpnGatewayV5#bandwidth_size}.'''
        result = self._values.get("bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def charge_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#charge_mode EnterpriseVpnGatewayV5#charge_mode}.'''
        result = self._values.get("charge_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#id EnterpriseVpnGatewayV5#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#type EnterpriseVpnGatewayV5#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnGatewayV5Eip2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpnGatewayV5Eip2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5Eip2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d70cc24519b5ff08694331953ac467fb8135e0e4b2e5bb814d90189c50c1865)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBandwidthName")
    def reset_bandwidth_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthName", []))

    @jsii.member(jsii_name="resetBandwidthSize")
    def reset_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthSize", []))

    @jsii.member(jsii_name="resetChargeMode")
    def reset_charge_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChargeMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="bandwidthId")
    def bandwidth_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthId"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ipVersion"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthNameInput")
    def bandwidth_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSizeInput")
    def bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="chargeModeInput")
    def charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthName")
    def bandwidth_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthName"))

    @bandwidth_name.setter
    def bandwidth_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378f93cb752f1e511503a655d9e8f1f4371fad9831b2f7dc6a8472c3a0655382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @bandwidth_size.setter
    def bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e0899bd665acca513315146cd61e7e8cda87e20478de9efc1c9ebd11d368f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chargeMode")
    def charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargeMode"))

    @charge_mode.setter
    def charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b59cebb40015229dc7a8199969f2fd254fff6368625f1606866ad7469f33a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chargeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a934a8dfc01e681b29a37594081d879c17ccc30885cb05414c8cda46e686e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e751739b6095721dbefc87218b40222992d753e5a7a901c4f47b4184344983c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnterpriseVpnGatewayV5Eip2]:
        return typing.cast(typing.Optional[EnterpriseVpnGatewayV5Eip2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnterpriseVpnGatewayV5Eip2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd0ab5e1254ff2ea924bbd74a7c299fc626089abadd3c19901a7e0b43f208bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EnterpriseVpnGatewayV5Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#create EnterpriseVpnGatewayV5#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#delete EnterpriseVpnGatewayV5#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#update EnterpriseVpnGatewayV5#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4f53b09521fc773590174cf3d7de04e868af2f717fac99c6fb822dd5879c11)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#create EnterpriseVpnGatewayV5#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#delete EnterpriseVpnGatewayV5#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_gateway_v5#update EnterpriseVpnGatewayV5#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnGatewayV5Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpnGatewayV5TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnGatewayV5.EnterpriseVpnGatewayV5TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d9e3871cdac8bdb0e65a5587c95913237d2a40e29cdd4e5a4262179c18d4600)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__48657d8e83a2581dd40f4e916de27df59ded19a5bfb68d999d610002b88625d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e0b06e050de11b6c47a70dae639977db5d71d36716999af34b3ba0135a25e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763a33ed34f8beefa3f521a32ec92a147272e915a5ebaf497610dfa4318edf28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnGatewayV5Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnGatewayV5Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnGatewayV5Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9c28d30491c2673fa6aa3e29d14e4226eb6e935b8d53a12689c98d2a4f2597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EnterpriseVpnGatewayV5",
    "EnterpriseVpnGatewayV5Config",
    "EnterpriseVpnGatewayV5Eip1",
    "EnterpriseVpnGatewayV5Eip1OutputReference",
    "EnterpriseVpnGatewayV5Eip2",
    "EnterpriseVpnGatewayV5Eip2OutputReference",
    "EnterpriseVpnGatewayV5Timeouts",
    "EnterpriseVpnGatewayV5TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__60cf953b342d24ac1a2e0190aad01e0bfc6ba63e932a13e4f806f49eac3d3bbb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zones: typing.Sequence[builtins.str],
    name: builtins.str,
    access_private_ip1: typing.Optional[builtins.str] = None,
    access_private_ip2: typing.Optional[builtins.str] = None,
    access_subnet_id: typing.Optional[builtins.str] = None,
    access_vpc_id: typing.Optional[builtins.str] = None,
    asn: typing.Optional[jsii.Number] = None,
    attachment_type: typing.Optional[builtins.str] = None,
    connect_subnet: typing.Optional[builtins.str] = None,
    delete_eip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    eip1: typing.Optional[typing.Union[EnterpriseVpnGatewayV5Eip1, typing.Dict[builtins.str, typing.Any]]] = None,
    eip2: typing.Optional[typing.Union[EnterpriseVpnGatewayV5Eip2, typing.Dict[builtins.str, typing.Any]]] = None,
    er_id: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    ha_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EnterpriseVpnGatewayV5Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f8748637b5eda4216616ba5727e5a102c9f26ae37f6aad1e1a4b959e25b3ffad(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cda79359ba2abcb659468771aa1f0beb0bf7fe8f6fe8f12ed65d3be936f735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710e00b74323e68a181e6106479cec7dcf2b0f60aeca1b904c8231b60a80e159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f123452a9908a0cfd4217a8ca7e0d048fe5c610e85b2635e252f9f4e384d9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3995b11f1bfdc5777201d624af627582f8e7247438b37974bfa861fcad4d4c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dffde3ed523c53895c6e62679d9dfdf32b90928471d3a9d2b8d09ba578e80e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103337f3e462f91aca6f7ebfa804866b770516754580388fa6affe80843c035a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a234a56c60888c8039902ad9f3c49ea0b9920d1970f1660a2b2b365f1ce286(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb91fcc154007509d8c20fad3cc1ff96012cde0997583f18ddfc0d5283b6acf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f5fc42e663bd12b68452a4be870daa5e7ff27d4d3e5dcc59d944372e9db892(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4719e613443520b87af6fd8fc74a842b5c3b59b1da1b289974e374224f145a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3873e05af5c894bf189a6abb24ce655c7e5389ea312aa715e208feb2ac67039d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6132e1cec113b0a6b91e5b01a5d31d8c19a0a8945a74ee9c020ff5d68f04649a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883922ae58d4e9d9406703d42cda40fac0119e5f04b4d02b6bff53caa3242023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95a65f31231a95e07140da67fa39ee788351565826ece7d7563c14b5af87cf4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13aa61e010bdc48802a7426d22efcd4ccc33a0b5858fd33b28d22fa2f0d5e14d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d60ff1bb753408c3d5396bbafafa66bb7905a9e72df503019fa973f0c48e4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356268f0f8bb458cfbd090bea69c50259a616264faf07d8444661b0a3413c5bb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f881b860a905532ce2ca976c5c7c33a03e9abc242a1893eecfcfbc6ec1fb6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c733090f4c83204ed91f474a67458a34c07e021f81f010d99f6bc6b0939fb7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zones: typing.Sequence[builtins.str],
    name: builtins.str,
    access_private_ip1: typing.Optional[builtins.str] = None,
    access_private_ip2: typing.Optional[builtins.str] = None,
    access_subnet_id: typing.Optional[builtins.str] = None,
    access_vpc_id: typing.Optional[builtins.str] = None,
    asn: typing.Optional[jsii.Number] = None,
    attachment_type: typing.Optional[builtins.str] = None,
    connect_subnet: typing.Optional[builtins.str] = None,
    delete_eip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    eip1: typing.Optional[typing.Union[EnterpriseVpnGatewayV5Eip1, typing.Dict[builtins.str, typing.Any]]] = None,
    eip2: typing.Optional[typing.Union[EnterpriseVpnGatewayV5Eip2, typing.Dict[builtins.str, typing.Any]]] = None,
    er_id: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    ha_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EnterpriseVpnGatewayV5Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec12cc7d8dca19984402265fb3573de6ec1f5cafe18f7f0aef771b7af359c53(
    *,
    bandwidth_name: typing.Optional[builtins.str] = None,
    bandwidth_size: typing.Optional[jsii.Number] = None,
    charge_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8092077a6dcc4c7140521b9aceafb7e82b12d5e63c0f35ee33640559605a073b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f061c7c9a58bb27332c803f8a7db343a068d6b37fe0b0c0ce5c8b71783ef2fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3e74101376b3f5614b285f1871450c56c9037fd673ee4c7cb45f58e445522e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec00c46c981e5d3dfc8c6745be3c37f54897b4c0b4ce57ecc4a53fd34e82e796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d604678d4d0fe2ac75a9af4e0a880a46511981e6ed0a65df27205824bffb573a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed9e8038700ea2cf8132f220044b8fcfe2f71dc5b4e5ade7f5ef4c5ba2bf3c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89ec976edf5b2e75ac17a290d4f363d9cd6d7c9d2b67854bf78cdac0133c548(
    value: typing.Optional[EnterpriseVpnGatewayV5Eip1],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49537a611d8b0e8e68c488afa20fc671c236d4c33c75e15bc4ab171686356ee7(
    *,
    bandwidth_name: typing.Optional[builtins.str] = None,
    bandwidth_size: typing.Optional[jsii.Number] = None,
    charge_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d70cc24519b5ff08694331953ac467fb8135e0e4b2e5bb814d90189c50c1865(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378f93cb752f1e511503a655d9e8f1f4371fad9831b2f7dc6a8472c3a0655382(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e0899bd665acca513315146cd61e7e8cda87e20478de9efc1c9ebd11d368f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b59cebb40015229dc7a8199969f2fd254fff6368625f1606866ad7469f33a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a934a8dfc01e681b29a37594081d879c17ccc30885cb05414c8cda46e686e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e751739b6095721dbefc87218b40222992d753e5a7a901c4f47b4184344983c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd0ab5e1254ff2ea924bbd74a7c299fc626089abadd3c19901a7e0b43f208bb(
    value: typing.Optional[EnterpriseVpnGatewayV5Eip2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4f53b09521fc773590174cf3d7de04e868af2f717fac99c6fb822dd5879c11(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9e3871cdac8bdb0e65a5587c95913237d2a40e29cdd4e5a4262179c18d4600(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48657d8e83a2581dd40f4e916de27df59ded19a5bfb68d999d610002b88625d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e0b06e050de11b6c47a70dae639977db5d71d36716999af34b3ba0135a25e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763a33ed34f8beefa3f521a32ec92a147272e915a5ebaf497610dfa4318edf28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9c28d30491c2673fa6aa3e29d14e4226eb6e935b8d53a12689c98d2a4f2597(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnGatewayV5Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
