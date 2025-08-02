r'''
# `opentelekomcloud_networking_subnet_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_networking_subnet_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2).
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


class NetworkingSubnetV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2 opentelekomcloud_networking_subnet_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cidr: builtins.str,
        network_id: builtins.str,
        allocation_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingSubnetV2AllocationPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_nameservers: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway_ip: typing.Optional[builtins.str] = None,
        host_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingSubnetV2HostRoutes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        no_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkingSubnetV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2 opentelekomcloud_networking_subnet_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#cidr NetworkingSubnetV2#cidr}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#network_id NetworkingSubnetV2#network_id}.
        :param allocation_pools: allocation_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#allocation_pools NetworkingSubnetV2#allocation_pools}
        :param dns_nameservers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#dns_nameservers NetworkingSubnetV2#dns_nameservers}.
        :param enable_dhcp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#enable_dhcp NetworkingSubnetV2#enable_dhcp}.
        :param gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#gateway_ip NetworkingSubnetV2#gateway_ip}.
        :param host_routes: host_routes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#host_routes NetworkingSubnetV2#host_routes}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#id NetworkingSubnetV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#ip_version NetworkingSubnetV2#ip_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#name NetworkingSubnetV2#name}.
        :param no_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#no_gateway NetworkingSubnetV2#no_gateway}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#region NetworkingSubnetV2#region}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#tenant_id NetworkingSubnetV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#timeouts NetworkingSubnetV2#timeouts}
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#value_specs NetworkingSubnetV2#value_specs}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c9e4c8cb7f8290b0148f3b258c62c669085096eaed44056debca83fbc4449f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkingSubnetV2Config(
            cidr=cidr,
            network_id=network_id,
            allocation_pools=allocation_pools,
            dns_nameservers=dns_nameservers,
            enable_dhcp=enable_dhcp,
            gateway_ip=gateway_ip,
            host_routes=host_routes,
            id=id,
            ip_version=ip_version,
            name=name,
            no_gateway=no_gateway,
            region=region,
            tenant_id=tenant_id,
            timeouts=timeouts,
            value_specs=value_specs,
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
        '''Generates CDKTF code for importing a NetworkingSubnetV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkingSubnetV2 to import.
        :param import_from_id: The id of the existing NetworkingSubnetV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkingSubnetV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69d7b02419a5fafcd79a2e561af84982a54d6e9ce05ad1809dffad7388de89b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllocationPools")
    def put_allocation_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingSubnetV2AllocationPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e07e443607f8a1805377ac1439bd50cf28962a782134f84b4e4e61b6bbd483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllocationPools", [value]))

    @jsii.member(jsii_name="putHostRoutes")
    def put_host_routes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingSubnetV2HostRoutes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b142f01d55c7212c9a18616896d51f1ca079d67853e6c34d778fe0850a10fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHostRoutes", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#create NetworkingSubnetV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#delete NetworkingSubnetV2#delete}.
        '''
        value = NetworkingSubnetV2Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllocationPools")
    def reset_allocation_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocationPools", []))

    @jsii.member(jsii_name="resetDnsNameservers")
    def reset_dns_nameservers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsNameservers", []))

    @jsii.member(jsii_name="resetEnableDhcp")
    def reset_enable_dhcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDhcp", []))

    @jsii.member(jsii_name="resetGatewayIp")
    def reset_gateway_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayIp", []))

    @jsii.member(jsii_name="resetHostRoutes")
    def reset_host_routes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostRoutes", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpVersion")
    def reset_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpVersion", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNoGateway")
    def reset_no_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoGateway", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValueSpecs")
    def reset_value_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueSpecs", []))

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
    @jsii.member(jsii_name="allocationPools")
    def allocation_pools(self) -> "NetworkingSubnetV2AllocationPoolsList":
        return typing.cast("NetworkingSubnetV2AllocationPoolsList", jsii.get(self, "allocationPools"))

    @builtins.property
    @jsii.member(jsii_name="hostRoutes")
    def host_routes(self) -> "NetworkingSubnetV2HostRoutesList":
        return typing.cast("NetworkingSubnetV2HostRoutesList", jsii.get(self, "hostRoutes"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkingSubnetV2TimeoutsOutputReference":
        return typing.cast("NetworkingSubnetV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allocationPoolsInput")
    def allocation_pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingSubnetV2AllocationPools"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingSubnetV2AllocationPools"]]], jsii.get(self, "allocationPoolsInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrInput")
    def cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNameserversInput")
    def dns_nameservers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsNameserversInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDhcpInput")
    def enable_dhcp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDhcpInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpInput")
    def gateway_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIpInput"))

    @builtins.property
    @jsii.member(jsii_name="hostRoutesInput")
    def host_routes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingSubnetV2HostRoutes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingSubnetV2HostRoutes"]]], jsii.get(self, "hostRoutesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipVersionInput")
    def ip_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ipVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="noGatewayInput")
    def no_gateway_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkingSubnetV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkingSubnetV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueSpecsInput")
    def value_specs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "valueSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @cidr.setter
    def cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179d70efc4dc8ab695d6872da84924b68561500c269bd228aa20910eff2bda8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsNameservers")
    def dns_nameservers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsNameservers"))

    @dns_nameservers.setter
    def dns_nameservers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7eb7e2deaf64bf76a5c7a67c9ef6f28c3ca3d4d53774bc571e35d13bc36d0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsNameservers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDhcp")
    def enable_dhcp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDhcp"))

    @enable_dhcp.setter
    def enable_dhcp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1587b3b89aa82b16f38ceb18ec7c0bac376a37b1dd4741d17d3aed3f459923e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDhcp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayIp")
    def gateway_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayIp"))

    @gateway_ip.setter
    def gateway_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d143bac8126986f8a16cdb329a9512dffb0a9f4ea25895192274d3285a200cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92dfdd657139acd4faca02bc60c2b25532b09c4e0797086de804d4b0d3f61bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipVersion")
    def ip_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ipVersion"))

    @ip_version.setter
    def ip_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fd531ae15880ea648b587f5747107f066e56f9a0e3e7a5c42f9914e649e2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416160427ed6b293b3a100e2a7cd02712d8cf93cd8013603a378828707ddcb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db80fbafbb57b95cdbb5e07f696498f9cddd22b769de6de8075def604ca91bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noGateway")
    def no_gateway(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noGateway"))

    @no_gateway.setter
    def no_gateway(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a682bf0b171ef6156478de16da09f6116ea4066745cf17ec4d2e13dcbc363183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3dac68e7cb5018d1eec46a1a8586cd2fb3d67e85232a5245c22904e4ed2bb10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78955173b663aa01367c4619203585aaa27a7a9252b178551c5f766a127d3e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueSpecs")
    def value_specs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "valueSpecs"))

    @value_specs.setter
    def value_specs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a335412c571b821d6100344bd9952b92dde60eddd07730a8d0b602353bd16605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueSpecs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2AllocationPools",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class NetworkingSubnetV2AllocationPools:
    def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#end NetworkingSubnetV2#end}.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#start NetworkingSubnetV2#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b60d8a5251dfe2eaa253ae55d34427d43d17eeb83f21cc1786b412953997fab)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#end NetworkingSubnetV2#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#start NetworkingSubnetV2#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingSubnetV2AllocationPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkingSubnetV2AllocationPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2AllocationPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__855cd3eec52465add9f365a3093d0b6e3f243eb5eebc7d0d81bd65ff994a5977)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkingSubnetV2AllocationPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb4cc68f7a80f01deecc95eac84cd30d983f4b6097fdf3091ea3902631e00f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkingSubnetV2AllocationPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333a62e8aa8fc21bfe4d8fa1aa71f9a162cdf6967e9faed7d8195ad0f02c4bf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__180770136fd43fe420d0edbf7e990db3828f15b2c2cd0307c1f5dcbda7b45494)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d30695d6432a13c1303815cb76fa7adf6a9aed338d188c1f616e85c86d961587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2AllocationPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2AllocationPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2AllocationPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6599f2fa6905a16bab24ca0e8a729565c3ff2f4b7108f9777b9027bcaa53733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkingSubnetV2AllocationPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2AllocationPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80354a15ef29b079d5c94220443184ad8d85e69e54c06e6c56c4980d64102eeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d3653856e4d6bf7ee39e4e8802939b9077980058ed121bd8f7345cb90e7a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc884194c3411f65fc3b6b6b54dbcd8ed7a5f6856208dc2c79322d713729f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2AllocationPools]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2AllocationPools]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2AllocationPools]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34eee4016ea0e8ba6aac71eecacc3c977992d27663146f248ba39d63ea2e336e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cidr": "cidr",
        "network_id": "networkId",
        "allocation_pools": "allocationPools",
        "dns_nameservers": "dnsNameservers",
        "enable_dhcp": "enableDhcp",
        "gateway_ip": "gatewayIp",
        "host_routes": "hostRoutes",
        "id": "id",
        "ip_version": "ipVersion",
        "name": "name",
        "no_gateway": "noGateway",
        "region": "region",
        "tenant_id": "tenantId",
        "timeouts": "timeouts",
        "value_specs": "valueSpecs",
    },
)
class NetworkingSubnetV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cidr: builtins.str,
        network_id: builtins.str,
        allocation_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingSubnetV2AllocationPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_nameservers: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway_ip: typing.Optional[builtins.str] = None,
        host_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingSubnetV2HostRoutes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_version: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        no_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkingSubnetV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#cidr NetworkingSubnetV2#cidr}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#network_id NetworkingSubnetV2#network_id}.
        :param allocation_pools: allocation_pools block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#allocation_pools NetworkingSubnetV2#allocation_pools}
        :param dns_nameservers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#dns_nameservers NetworkingSubnetV2#dns_nameservers}.
        :param enable_dhcp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#enable_dhcp NetworkingSubnetV2#enable_dhcp}.
        :param gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#gateway_ip NetworkingSubnetV2#gateway_ip}.
        :param host_routes: host_routes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#host_routes NetworkingSubnetV2#host_routes}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#id NetworkingSubnetV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#ip_version NetworkingSubnetV2#ip_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#name NetworkingSubnetV2#name}.
        :param no_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#no_gateway NetworkingSubnetV2#no_gateway}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#region NetworkingSubnetV2#region}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#tenant_id NetworkingSubnetV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#timeouts NetworkingSubnetV2#timeouts}
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#value_specs NetworkingSubnetV2#value_specs}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkingSubnetV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b556ddb008aaf335ca5471b44ae7158ed236a64dfc33a365597ff683dc206ff)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument allocation_pools", value=allocation_pools, expected_type=type_hints["allocation_pools"])
            check_type(argname="argument dns_nameservers", value=dns_nameservers, expected_type=type_hints["dns_nameservers"])
            check_type(argname="argument enable_dhcp", value=enable_dhcp, expected_type=type_hints["enable_dhcp"])
            check_type(argname="argument gateway_ip", value=gateway_ip, expected_type=type_hints["gateway_ip"])
            check_type(argname="argument host_routes", value=host_routes, expected_type=type_hints["host_routes"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_version", value=ip_version, expected_type=type_hints["ip_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument no_gateway", value=no_gateway, expected_type=type_hints["no_gateway"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument value_specs", value=value_specs, expected_type=type_hints["value_specs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "network_id": network_id,
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
        if allocation_pools is not None:
            self._values["allocation_pools"] = allocation_pools
        if dns_nameservers is not None:
            self._values["dns_nameservers"] = dns_nameservers
        if enable_dhcp is not None:
            self._values["enable_dhcp"] = enable_dhcp
        if gateway_ip is not None:
            self._values["gateway_ip"] = gateway_ip
        if host_routes is not None:
            self._values["host_routes"] = host_routes
        if id is not None:
            self._values["id"] = id
        if ip_version is not None:
            self._values["ip_version"] = ip_version
        if name is not None:
            self._values["name"] = name
        if no_gateway is not None:
            self._values["no_gateway"] = no_gateway
        if region is not None:
            self._values["region"] = region
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if value_specs is not None:
            self._values["value_specs"] = value_specs

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
    def cidr(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#cidr NetworkingSubnetV2#cidr}.'''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#network_id NetworkingSubnetV2#network_id}.'''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allocation_pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2AllocationPools]]]:
        '''allocation_pools block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#allocation_pools NetworkingSubnetV2#allocation_pools}
        '''
        result = self._values.get("allocation_pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2AllocationPools]]], result)

    @builtins.property
    def dns_nameservers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#dns_nameservers NetworkingSubnetV2#dns_nameservers}.'''
        result = self._values.get("dns_nameservers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_dhcp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#enable_dhcp NetworkingSubnetV2#enable_dhcp}.'''
        result = self._values.get("enable_dhcp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gateway_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#gateway_ip NetworkingSubnetV2#gateway_ip}.'''
        result = self._values.get("gateway_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_routes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingSubnetV2HostRoutes"]]]:
        '''host_routes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#host_routes NetworkingSubnetV2#host_routes}
        '''
        result = self._values.get("host_routes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingSubnetV2HostRoutes"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#id NetworkingSubnetV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#ip_version NetworkingSubnetV2#ip_version}.'''
        result = self._values.get("ip_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#name NetworkingSubnetV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_gateway(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#no_gateway NetworkingSubnetV2#no_gateway}.'''
        result = self._values.get("no_gateway")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#region NetworkingSubnetV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#tenant_id NetworkingSubnetV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkingSubnetV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#timeouts NetworkingSubnetV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkingSubnetV2Timeouts"], result)

    @builtins.property
    def value_specs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#value_specs NetworkingSubnetV2#value_specs}.'''
        result = self._values.get("value_specs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingSubnetV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2HostRoutes",
    jsii_struct_bases=[],
    name_mapping={"destination_cidr": "destinationCidr", "next_hop": "nextHop"},
)
class NetworkingSubnetV2HostRoutes:
    def __init__(
        self,
        *,
        destination_cidr: builtins.str,
        next_hop: builtins.str,
    ) -> None:
        '''
        :param destination_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#destination_cidr NetworkingSubnetV2#destination_cidr}.
        :param next_hop: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#next_hop NetworkingSubnetV2#next_hop}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a487f2756d5848344397f0f871222fec76b63f7b1978a558c553ab48edd2fbbd)
            check_type(argname="argument destination_cidr", value=destination_cidr, expected_type=type_hints["destination_cidr"])
            check_type(argname="argument next_hop", value=next_hop, expected_type=type_hints["next_hop"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_cidr": destination_cidr,
            "next_hop": next_hop,
        }

    @builtins.property
    def destination_cidr(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#destination_cidr NetworkingSubnetV2#destination_cidr}.'''
        result = self._values.get("destination_cidr")
        assert result is not None, "Required property 'destination_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def next_hop(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#next_hop NetworkingSubnetV2#next_hop}.'''
        result = self._values.get("next_hop")
        assert result is not None, "Required property 'next_hop' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingSubnetV2HostRoutes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkingSubnetV2HostRoutesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2HostRoutesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfbc7854af6bdca1439a9e725bd0e0145ef7c59414aa1a61e9b0db527b17289b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkingSubnetV2HostRoutesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d4e077a6fb60fc83413ac8e0c601ea4c15b34074003799236ec1782ff84475)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkingSubnetV2HostRoutesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f0ac0797af9fa4110557a49dc739865d0291a27ca80b287b3f27fa61d3d643)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e5e4d1d6ee7ab60a68dcda2235c1ea6d3310e016636ffb0de62778d0511a77c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d12ad61cb927f77159bdc846dce4f7f27fab641ea303d7a2c3a8b48fc1ffd7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2HostRoutes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2HostRoutes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2HostRoutes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8016df6b741aa9ec6c56285135db529ced8c31ecca1769df54b0dcff7a389c53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkingSubnetV2HostRoutesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2HostRoutesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8122bc12b514fa8a5017a2f702004aa63cb8a092f5326807e089ca80a005f8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="destinationCidrInput")
    def destination_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopInput")
    def next_hop_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationCidr")
    def destination_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationCidr"))

    @destination_cidr.setter
    def destination_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c06a3320e793e47d347c5cbd54d3c2fa29084c3787ceac457d7b77820265229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHop")
    def next_hop(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHop"))

    @next_hop.setter
    def next_hop(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf6f54c0310b29711a12697ba645c58dbc3bee5b37da70293814329c34f310f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHop", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2HostRoutes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2HostRoutes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2HostRoutes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7eff9e74bf0c90fac7826777198c5a789f5fd5b8f6633294847e0dc0c461e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class NetworkingSubnetV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#create NetworkingSubnetV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#delete NetworkingSubnetV2#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283f71c05d658b82d51f2d1a83dacfd0d8cf1e58a8828188bfb9637b77e45fde)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#create NetworkingSubnetV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_subnet_v2#delete NetworkingSubnetV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingSubnetV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkingSubnetV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingSubnetV2.NetworkingSubnetV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6118328f39108b63a0a268098c89cf2efc19a0cd45062c0ea833ef621404f7be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5346f3f93f8efc148494cadc82fdf9dd05fa82d50fbe6157a85a13829b7f552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889b4e19ccd5d38f45d25b0fd875d8fe83fea91b1b739da2c97ca54fdd60900c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201a219746564dc61a64ff6b3bf4d45cf7911c4eb5de3f1d5342b6b3e9805512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkingSubnetV2",
    "NetworkingSubnetV2AllocationPools",
    "NetworkingSubnetV2AllocationPoolsList",
    "NetworkingSubnetV2AllocationPoolsOutputReference",
    "NetworkingSubnetV2Config",
    "NetworkingSubnetV2HostRoutes",
    "NetworkingSubnetV2HostRoutesList",
    "NetworkingSubnetV2HostRoutesOutputReference",
    "NetworkingSubnetV2Timeouts",
    "NetworkingSubnetV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e6c9e4c8cb7f8290b0148f3b258c62c669085096eaed44056debca83fbc4449f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cidr: builtins.str,
    network_id: builtins.str,
    allocation_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingSubnetV2AllocationPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_nameservers: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gateway_ip: typing.Optional[builtins.str] = None,
    host_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingSubnetV2HostRoutes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    no_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkingSubnetV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__c69d7b02419a5fafcd79a2e561af84982a54d6e9ce05ad1809dffad7388de89b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e07e443607f8a1805377ac1439bd50cf28962a782134f84b4e4e61b6bbd483(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingSubnetV2AllocationPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b142f01d55c7212c9a18616896d51f1ca079d67853e6c34d778fe0850a10fea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingSubnetV2HostRoutes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179d70efc4dc8ab695d6872da84924b68561500c269bd228aa20910eff2bda8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7eb7e2deaf64bf76a5c7a67c9ef6f28c3ca3d4d53774bc571e35d13bc36d0bd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1587b3b89aa82b16f38ceb18ec7c0bac376a37b1dd4741d17d3aed3f459923e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d143bac8126986f8a16cdb329a9512dffb0a9f4ea25895192274d3285a200cb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92dfdd657139acd4faca02bc60c2b25532b09c4e0797086de804d4b0d3f61bc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fd531ae15880ea648b587f5747107f066e56f9a0e3e7a5c42f9914e649e2e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416160427ed6b293b3a100e2a7cd02712d8cf93cd8013603a378828707ddcb26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db80fbafbb57b95cdbb5e07f696498f9cddd22b769de6de8075def604ca91bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a682bf0b171ef6156478de16da09f6116ea4066745cf17ec4d2e13dcbc363183(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3dac68e7cb5018d1eec46a1a8586cd2fb3d67e85232a5245c22904e4ed2bb10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78955173b663aa01367c4619203585aaa27a7a9252b178551c5f766a127d3e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a335412c571b821d6100344bd9952b92dde60eddd07730a8d0b602353bd16605(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b60d8a5251dfe2eaa253ae55d34427d43d17eeb83f21cc1786b412953997fab(
    *,
    end: builtins.str,
    start: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855cd3eec52465add9f365a3093d0b6e3f243eb5eebc7d0d81bd65ff994a5977(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb4cc68f7a80f01deecc95eac84cd30d983f4b6097fdf3091ea3902631e00f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333a62e8aa8fc21bfe4d8fa1aa71f9a162cdf6967e9faed7d8195ad0f02c4bf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180770136fd43fe420d0edbf7e990db3828f15b2c2cd0307c1f5dcbda7b45494(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30695d6432a13c1303815cb76fa7adf6a9aed338d188c1f616e85c86d961587(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6599f2fa6905a16bab24ca0e8a729565c3ff2f4b7108f9777b9027bcaa53733(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2AllocationPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80354a15ef29b079d5c94220443184ad8d85e69e54c06e6c56c4980d64102eeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d3653856e4d6bf7ee39e4e8802939b9077980058ed121bd8f7345cb90e7a47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc884194c3411f65fc3b6b6b54dbcd8ed7a5f6856208dc2c79322d713729f81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34eee4016ea0e8ba6aac71eecacc3c977992d27663146f248ba39d63ea2e336e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2AllocationPools]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b556ddb008aaf335ca5471b44ae7158ed236a64dfc33a365597ff683dc206ff(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cidr: builtins.str,
    network_id: builtins.str,
    allocation_pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingSubnetV2AllocationPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_nameservers: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gateway_ip: typing.Optional[builtins.str] = None,
    host_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingSubnetV2HostRoutes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_version: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    no_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkingSubnetV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a487f2756d5848344397f0f871222fec76b63f7b1978a558c553ab48edd2fbbd(
    *,
    destination_cidr: builtins.str,
    next_hop: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbc7854af6bdca1439a9e725bd0e0145ef7c59414aa1a61e9b0db527b17289b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d4e077a6fb60fc83413ac8e0c601ea4c15b34074003799236ec1782ff84475(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f0ac0797af9fa4110557a49dc739865d0291a27ca80b287b3f27fa61d3d643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5e4d1d6ee7ab60a68dcda2235c1ea6d3310e016636ffb0de62778d0511a77c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d12ad61cb927f77159bdc846dce4f7f27fab641ea303d7a2c3a8b48fc1ffd7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8016df6b741aa9ec6c56285135db529ced8c31ecca1769df54b0dcff7a389c53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingSubnetV2HostRoutes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8122bc12b514fa8a5017a2f702004aa63cb8a092f5326807e089ca80a005f8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c06a3320e793e47d347c5cbd54d3c2fa29084c3787ceac457d7b77820265229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf6f54c0310b29711a12697ba645c58dbc3bee5b37da70293814329c34f310f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7eff9e74bf0c90fac7826777198c5a789f5fd5b8f6633294847e0dc0c461e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2HostRoutes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283f71c05d658b82d51f2d1a83dacfd0d8cf1e58a8828188bfb9637b77e45fde(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6118328f39108b63a0a268098c89cf2efc19a0cd45062c0ea833ef621404f7be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5346f3f93f8efc148494cadc82fdf9dd05fa82d50fbe6157a85a13829b7f552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889b4e19ccd5d38f45d25b0fd875d8fe83fea91b1b739da2c97ca54fdd60900c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201a219746564dc61a64ff6b3bf4d45cf7911c4eb5de3f1d5342b6b3e9805512(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingSubnetV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
