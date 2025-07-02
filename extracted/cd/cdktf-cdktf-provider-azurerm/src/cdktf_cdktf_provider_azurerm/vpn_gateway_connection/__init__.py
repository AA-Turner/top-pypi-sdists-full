r'''
# `azurerm_vpn_gateway_connection`

Refer to the Terraform Registry for docs: [`azurerm_vpn_gateway_connection`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection).
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


class VpnGatewayConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection azurerm_vpn_gateway_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        remote_vpn_site_id: builtins.str,
        vpn_gateway_id: builtins.str,
        vpn_link: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionVpnLink", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing: typing.Optional[typing.Union["VpnGatewayConnectionRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["VpnGatewayConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_selector_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionTrafficSelectorPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection azurerm_vpn_gateway_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#name VpnGatewayConnection#name}.
        :param remote_vpn_site_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#remote_vpn_site_id VpnGatewayConnection#remote_vpn_site_id}.
        :param vpn_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_gateway_id VpnGatewayConnection#vpn_gateway_id}.
        :param vpn_link: vpn_link block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_link VpnGatewayConnection#vpn_link}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#id VpnGatewayConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internet_security_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#internet_security_enabled VpnGatewayConnection#internet_security_enabled}.
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#routing VpnGatewayConnection#routing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#timeouts VpnGatewayConnection#timeouts}
        :param traffic_selector_policy: traffic_selector_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#traffic_selector_policy VpnGatewayConnection#traffic_selector_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66839de53f6cd750154f5e88ed7d6452b697d981211373c2aa18b40103376a0d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VpnGatewayConnectionConfig(
            name=name,
            remote_vpn_site_id=remote_vpn_site_id,
            vpn_gateway_id=vpn_gateway_id,
            vpn_link=vpn_link,
            id=id,
            internet_security_enabled=internet_security_enabled,
            routing=routing,
            timeouts=timeouts,
            traffic_selector_policy=traffic_selector_policy,
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
        '''Generates CDKTF code for importing a VpnGatewayConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VpnGatewayConnection to import.
        :param import_from_id: The id of the existing VpnGatewayConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VpnGatewayConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84066471d2f29c3693c1e37b28e3459aad335dd21404b3acaffb781e8d0e48b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRouting")
    def put_routing(
        self,
        *,
        associated_route_table: builtins.str,
        inbound_route_map_id: typing.Optional[builtins.str] = None,
        outbound_route_map_id: typing.Optional[builtins.str] = None,
        propagated_route_table: typing.Optional[typing.Union["VpnGatewayConnectionRoutingPropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param associated_route_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#associated_route_table VpnGatewayConnection#associated_route_table}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#inbound_route_map_id VpnGatewayConnection#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#outbound_route_map_id VpnGatewayConnection#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#propagated_route_table VpnGatewayConnection#propagated_route_table}
        '''
        value = VpnGatewayConnectionRouting(
            associated_route_table=associated_route_table,
            inbound_route_map_id=inbound_route_map_id,
            outbound_route_map_id=outbound_route_map_id,
            propagated_route_table=propagated_route_table,
        )

        return typing.cast(None, jsii.invoke(self, "putRouting", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#create VpnGatewayConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#delete VpnGatewayConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#read VpnGatewayConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#update VpnGatewayConnection#update}.
        '''
        value = VpnGatewayConnectionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTrafficSelectorPolicy")
    def put_traffic_selector_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionTrafficSelectorPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d3b9d7ee401bfb245129f2986633111983c9552c59d2862185076dfac15048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrafficSelectorPolicy", [value]))

    @jsii.member(jsii_name="putVpnLink")
    def put_vpn_link(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionVpnLink", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e210e0b66f6e39c83eacb3f280fe5da77adfc2d6e6d5096d392fbf1c144f7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVpnLink", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInternetSecurityEnabled")
    def reset_internet_security_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternetSecurityEnabled", []))

    @jsii.member(jsii_name="resetRouting")
    def reset_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouting", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrafficSelectorPolicy")
    def reset_traffic_selector_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficSelectorPolicy", []))

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
    @jsii.member(jsii_name="routing")
    def routing(self) -> "VpnGatewayConnectionRoutingOutputReference":
        return typing.cast("VpnGatewayConnectionRoutingOutputReference", jsii.get(self, "routing"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VpnGatewayConnectionTimeoutsOutputReference":
        return typing.cast("VpnGatewayConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trafficSelectorPolicy")
    def traffic_selector_policy(
        self,
    ) -> "VpnGatewayConnectionTrafficSelectorPolicyList":
        return typing.cast("VpnGatewayConnectionTrafficSelectorPolicyList", jsii.get(self, "trafficSelectorPolicy"))

    @builtins.property
    @jsii.member(jsii_name="vpnLink")
    def vpn_link(self) -> "VpnGatewayConnectionVpnLinkList":
        return typing.cast("VpnGatewayConnectionVpnLinkList", jsii.get(self, "vpnLink"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="internetSecurityEnabledInput")
    def internet_security_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internetSecurityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVpnSiteIdInput")
    def remote_vpn_site_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVpnSiteIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routingInput")
    def routing_input(self) -> typing.Optional["VpnGatewayConnectionRouting"]:
        return typing.cast(typing.Optional["VpnGatewayConnectionRouting"], jsii.get(self, "routingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnGatewayConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnGatewayConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficSelectorPolicyInput")
    def traffic_selector_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionTrafficSelectorPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionTrafficSelectorPolicy"]]], jsii.get(self, "trafficSelectorPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayIdInput")
    def vpn_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnLinkInput")
    def vpn_link_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLink"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLink"]]], jsii.get(self, "vpnLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b4950463ef3753fca305ba8bee2ad27d1b9e13985f6a9ce2aefb23018c014a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internetSecurityEnabled")
    def internet_security_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internetSecurityEnabled"))

    @internet_security_enabled.setter
    def internet_security_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5e5f35fcc774453e42df9da77b9dc9244ec530e0b741faf54721313a14e85f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internetSecurityEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cf5a938d959dd26175164d5f41c86a11f7784f6a16e440693e1f439a36f862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteVpnSiteId")
    def remote_vpn_site_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVpnSiteId"))

    @remote_vpn_site_id.setter
    def remote_vpn_site_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9486d6fb36b0567bc05d6661ad8acfeba393a8db1990aede93879afc17c49cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVpnSiteId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnGatewayId"))

    @vpn_gateway_id.setter
    def vpn_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2b8e16ccb4297b111025f17bb22f44361210e2400188a4f5d223125c2a4c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnGatewayId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionConfig",
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
        "remote_vpn_site_id": "remoteVpnSiteId",
        "vpn_gateway_id": "vpnGatewayId",
        "vpn_link": "vpnLink",
        "id": "id",
        "internet_security_enabled": "internetSecurityEnabled",
        "routing": "routing",
        "timeouts": "timeouts",
        "traffic_selector_policy": "trafficSelectorPolicy",
    },
)
class VpnGatewayConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        remote_vpn_site_id: builtins.str,
        vpn_gateway_id: builtins.str,
        vpn_link: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionVpnLink", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing: typing.Optional[typing.Union["VpnGatewayConnectionRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["VpnGatewayConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_selector_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionTrafficSelectorPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#name VpnGatewayConnection#name}.
        :param remote_vpn_site_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#remote_vpn_site_id VpnGatewayConnection#remote_vpn_site_id}.
        :param vpn_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_gateway_id VpnGatewayConnection#vpn_gateway_id}.
        :param vpn_link: vpn_link block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_link VpnGatewayConnection#vpn_link}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#id VpnGatewayConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internet_security_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#internet_security_enabled VpnGatewayConnection#internet_security_enabled}.
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#routing VpnGatewayConnection#routing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#timeouts VpnGatewayConnection#timeouts}
        :param traffic_selector_policy: traffic_selector_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#traffic_selector_policy VpnGatewayConnection#traffic_selector_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing, dict):
            routing = VpnGatewayConnectionRouting(**routing)
        if isinstance(timeouts, dict):
            timeouts = VpnGatewayConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05e6f0751a2aa2e1a82b95c342c612d07ec9af10eecbe0a2aca4f7a9b92dba0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument remote_vpn_site_id", value=remote_vpn_site_id, expected_type=type_hints["remote_vpn_site_id"])
            check_type(argname="argument vpn_gateway_id", value=vpn_gateway_id, expected_type=type_hints["vpn_gateway_id"])
            check_type(argname="argument vpn_link", value=vpn_link, expected_type=type_hints["vpn_link"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument internet_security_enabled", value=internet_security_enabled, expected_type=type_hints["internet_security_enabled"])
            check_type(argname="argument routing", value=routing, expected_type=type_hints["routing"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument traffic_selector_policy", value=traffic_selector_policy, expected_type=type_hints["traffic_selector_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "remote_vpn_site_id": remote_vpn_site_id,
            "vpn_gateway_id": vpn_gateway_id,
            "vpn_link": vpn_link,
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
        if internet_security_enabled is not None:
            self._values["internet_security_enabled"] = internet_security_enabled
        if routing is not None:
            self._values["routing"] = routing
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if traffic_selector_policy is not None:
            self._values["traffic_selector_policy"] = traffic_selector_policy

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#name VpnGatewayConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_vpn_site_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#remote_vpn_site_id VpnGatewayConnection#remote_vpn_site_id}.'''
        result = self._values.get("remote_vpn_site_id")
        assert result is not None, "Required property 'remote_vpn_site_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpn_gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_gateway_id VpnGatewayConnection#vpn_gateway_id}.'''
        result = self._values.get("vpn_gateway_id")
        assert result is not None, "Required property 'vpn_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpn_link(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLink"]]:
        '''vpn_link block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_link VpnGatewayConnection#vpn_link}
        '''
        result = self._values.get("vpn_link")
        assert result is not None, "Required property 'vpn_link' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLink"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#id VpnGatewayConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_security_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#internet_security_enabled VpnGatewayConnection#internet_security_enabled}.'''
        result = self._values.get("internet_security_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def routing(self) -> typing.Optional["VpnGatewayConnectionRouting"]:
        '''routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#routing VpnGatewayConnection#routing}
        '''
        result = self._values.get("routing")
        return typing.cast(typing.Optional["VpnGatewayConnectionRouting"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VpnGatewayConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#timeouts VpnGatewayConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VpnGatewayConnectionTimeouts"], result)

    @builtins.property
    def traffic_selector_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionTrafficSelectorPolicy"]]]:
        '''traffic_selector_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#traffic_selector_policy VpnGatewayConnection#traffic_selector_policy}
        '''
        result = self._values.get("traffic_selector_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionTrafficSelectorPolicy"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionRouting",
    jsii_struct_bases=[],
    name_mapping={
        "associated_route_table": "associatedRouteTable",
        "inbound_route_map_id": "inboundRouteMapId",
        "outbound_route_map_id": "outboundRouteMapId",
        "propagated_route_table": "propagatedRouteTable",
    },
)
class VpnGatewayConnectionRouting:
    def __init__(
        self,
        *,
        associated_route_table: builtins.str,
        inbound_route_map_id: typing.Optional[builtins.str] = None,
        outbound_route_map_id: typing.Optional[builtins.str] = None,
        propagated_route_table: typing.Optional[typing.Union["VpnGatewayConnectionRoutingPropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param associated_route_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#associated_route_table VpnGatewayConnection#associated_route_table}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#inbound_route_map_id VpnGatewayConnection#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#outbound_route_map_id VpnGatewayConnection#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#propagated_route_table VpnGatewayConnection#propagated_route_table}
        '''
        if isinstance(propagated_route_table, dict):
            propagated_route_table = VpnGatewayConnectionRoutingPropagatedRouteTable(**propagated_route_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fd813c4870523dc0278d3c8aafca2c4922935b4ae06ef1eeb519fec1ee3a5c)
            check_type(argname="argument associated_route_table", value=associated_route_table, expected_type=type_hints["associated_route_table"])
            check_type(argname="argument inbound_route_map_id", value=inbound_route_map_id, expected_type=type_hints["inbound_route_map_id"])
            check_type(argname="argument outbound_route_map_id", value=outbound_route_map_id, expected_type=type_hints["outbound_route_map_id"])
            check_type(argname="argument propagated_route_table", value=propagated_route_table, expected_type=type_hints["propagated_route_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "associated_route_table": associated_route_table,
        }
        if inbound_route_map_id is not None:
            self._values["inbound_route_map_id"] = inbound_route_map_id
        if outbound_route_map_id is not None:
            self._values["outbound_route_map_id"] = outbound_route_map_id
        if propagated_route_table is not None:
            self._values["propagated_route_table"] = propagated_route_table

    @builtins.property
    def associated_route_table(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#associated_route_table VpnGatewayConnection#associated_route_table}.'''
        result = self._values.get("associated_route_table")
        assert result is not None, "Required property 'associated_route_table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#inbound_route_map_id VpnGatewayConnection#inbound_route_map_id}.'''
        result = self._values.get("inbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#outbound_route_map_id VpnGatewayConnection#outbound_route_map_id}.'''
        result = self._values.get("outbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagated_route_table(
        self,
    ) -> typing.Optional["VpnGatewayConnectionRoutingPropagatedRouteTable"]:
        '''propagated_route_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#propagated_route_table VpnGatewayConnection#propagated_route_table}
        '''
        result = self._values.get("propagated_route_table")
        return typing.cast(typing.Optional["VpnGatewayConnectionRoutingPropagatedRouteTable"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnGatewayConnectionRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1cab903fbf7ff07080088d403543f99dfdaea17748956681b3522caaa6e3419)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPropagatedRouteTable")
    def put_propagated_route_table(
        self,
        *,
        route_table_ids: typing.Sequence[builtins.str],
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param route_table_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#route_table_ids VpnGatewayConnection#route_table_ids}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#labels VpnGatewayConnection#labels}.
        '''
        value = VpnGatewayConnectionRoutingPropagatedRouteTable(
            route_table_ids=route_table_ids, labels=labels
        )

        return typing.cast(None, jsii.invoke(self, "putPropagatedRouteTable", [value]))

    @jsii.member(jsii_name="resetInboundRouteMapId")
    def reset_inbound_route_map_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInboundRouteMapId", []))

    @jsii.member(jsii_name="resetOutboundRouteMapId")
    def reset_outbound_route_map_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundRouteMapId", []))

    @jsii.member(jsii_name="resetPropagatedRouteTable")
    def reset_propagated_route_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagatedRouteTable", []))

    @builtins.property
    @jsii.member(jsii_name="propagatedRouteTable")
    def propagated_route_table(
        self,
    ) -> "VpnGatewayConnectionRoutingPropagatedRouteTableOutputReference":
        return typing.cast("VpnGatewayConnectionRoutingPropagatedRouteTableOutputReference", jsii.get(self, "propagatedRouteTable"))

    @builtins.property
    @jsii.member(jsii_name="associatedRouteTableInput")
    def associated_route_table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associatedRouteTableInput"))

    @builtins.property
    @jsii.member(jsii_name="inboundRouteMapIdInput")
    def inbound_route_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inboundRouteMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundRouteMapIdInput")
    def outbound_route_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outboundRouteMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="propagatedRouteTableInput")
    def propagated_route_table_input(
        self,
    ) -> typing.Optional["VpnGatewayConnectionRoutingPropagatedRouteTable"]:
        return typing.cast(typing.Optional["VpnGatewayConnectionRoutingPropagatedRouteTable"], jsii.get(self, "propagatedRouteTableInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedRouteTable")
    def associated_route_table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associatedRouteTable"))

    @associated_route_table.setter
    def associated_route_table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17df1c90979f7e9d2db3b11e2a9f0e066a421c069daafc61e5b9e5701047263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedRouteTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundRouteMapId")
    def inbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inboundRouteMapId"))

    @inbound_route_map_id.setter
    def inbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ab40916568b2ab27fcc7a358be803bed8aa59a083c774582b09377d49f6ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outboundRouteMapId")
    def outbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundRouteMapId"))

    @outbound_route_map_id.setter
    def outbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340da0b4c9bceea3e07e49f12e3e4115974eb2b2a8ce6b2028638bc96737c725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnGatewayConnectionRouting]:
        return typing.cast(typing.Optional[VpnGatewayConnectionRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnGatewayConnectionRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7299d33dac661c958ffd25df29f24accbf90c6e3840dd2d386b71a3c2502fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionRoutingPropagatedRouteTable",
    jsii_struct_bases=[],
    name_mapping={"route_table_ids": "routeTableIds", "labels": "labels"},
)
class VpnGatewayConnectionRoutingPropagatedRouteTable:
    def __init__(
        self,
        *,
        route_table_ids: typing.Sequence[builtins.str],
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param route_table_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#route_table_ids VpnGatewayConnection#route_table_ids}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#labels VpnGatewayConnection#labels}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669c6d63293b891185bf3b8d9fbe3114a59f84bd72e25f48e8b270db672dc7e4)
            check_type(argname="argument route_table_ids", value=route_table_ids, expected_type=type_hints["route_table_ids"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "route_table_ids": route_table_ids,
        }
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def route_table_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#route_table_ids VpnGatewayConnection#route_table_ids}.'''
        result = self._values.get("route_table_ids")
        assert result is not None, "Required property 'route_table_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#labels VpnGatewayConnection#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionRoutingPropagatedRouteTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnGatewayConnectionRoutingPropagatedRouteTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionRoutingPropagatedRouteTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c6fda737a27817897f1990f64b213b79c2ca75537e5b21fda98edf1f02228c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="routeTableIdsInput")
    def route_table_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "routeTableIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d75387e11071e4a09cd82d4c02d597e47eff344a97b36f7ad56de4a0a1ce6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTableIds")
    def route_table_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "routeTableIds"))

    @route_table_ids.setter
    def route_table_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae3136af98529047a4dd06b9e2eb39c0eda66484f4ca063af80b9f636565b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTableIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpnGatewayConnectionRoutingPropagatedRouteTable]:
        return typing.cast(typing.Optional[VpnGatewayConnectionRoutingPropagatedRouteTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnGatewayConnectionRoutingPropagatedRouteTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d6ca7602e91fac48605b7f6ed609919f53c30f276bd2e4c669fb9855e45c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VpnGatewayConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#create VpnGatewayConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#delete VpnGatewayConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#read VpnGatewayConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#update VpnGatewayConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606289fe1ec967f65c0cbae68778ba08df3956a0954cff7c049e01251df4b760)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#create VpnGatewayConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#delete VpnGatewayConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#read VpnGatewayConnection#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#update VpnGatewayConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnGatewayConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eccd7d947a501b1b0d9d13520ca4456a3a9254c36fb6eace8e656e668a298ef1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__292877638b96d009978e0af708876c232a8340d0655775549d84fa4d530c4141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc32796b21ddff958ba66dd9fb4a11f6508cc2f88cef0ab658ceeb95aca4255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ca6055d31c4c168e7aa420ada75bdd20a0ce9512084262bed2ff43cd36b22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ab99f1c060581dd38bbb71fffc71271da6d94d656b112066ff72a59a646db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fc71a42c63448feaad2a4bd58816a527aa364cff5e1c20946f7748abc41d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionTrafficSelectorPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "local_address_ranges": "localAddressRanges",
        "remote_address_ranges": "remoteAddressRanges",
    },
)
class VpnGatewayConnectionTrafficSelectorPolicy:
    def __init__(
        self,
        *,
        local_address_ranges: typing.Sequence[builtins.str],
        remote_address_ranges: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param local_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#local_address_ranges VpnGatewayConnection#local_address_ranges}.
        :param remote_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#remote_address_ranges VpnGatewayConnection#remote_address_ranges}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9f17669918468e70fd5888582a305f868c44fb7f9f96403ce35b29e90df3e6)
            check_type(argname="argument local_address_ranges", value=local_address_ranges, expected_type=type_hints["local_address_ranges"])
            check_type(argname="argument remote_address_ranges", value=remote_address_ranges, expected_type=type_hints["remote_address_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_address_ranges": local_address_ranges,
            "remote_address_ranges": remote_address_ranges,
        }

    @builtins.property
    def local_address_ranges(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#local_address_ranges VpnGatewayConnection#local_address_ranges}.'''
        result = self._values.get("local_address_ranges")
        assert result is not None, "Required property 'local_address_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def remote_address_ranges(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#remote_address_ranges VpnGatewayConnection#remote_address_ranges}.'''
        result = self._values.get("remote_address_ranges")
        assert result is not None, "Required property 'remote_address_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionTrafficSelectorPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnGatewayConnectionTrafficSelectorPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionTrafficSelectorPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e30357505c0f99bc6f2127e076b823d34fa446e6fb44acd5946132222f8021ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VpnGatewayConnectionTrafficSelectorPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22dbfadbb6311b4dcb74753dbb6058543252e99e5543e4ef39f9c6b2dccc244)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnGatewayConnectionTrafficSelectorPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145d2f0e3b9ec47f7537bf916c5ab97be48013959cf166af2322f1869e69677f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05a1f9f04a29ee741627ff30463098276cecb6ae64414e0f55df88a91699c833)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fb816303dcd501cfbc40f599fea538bae850a46c296655e49a28c49d759ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionTrafficSelectorPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionTrafficSelectorPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionTrafficSelectorPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c71773b720e8dea7ad58a3c0c53b8a71b795b38efde865ac26c03799a5bf68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnGatewayConnectionTrafficSelectorPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionTrafficSelectorPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba4f87b789dae7a7508f9d5929c4f4822fe437a1c29bb5b6cde971e5099131e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="localAddressRangesInput")
    def local_address_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "localAddressRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteAddressRangesInput")
    def remote_address_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "remoteAddressRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="localAddressRanges")
    def local_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "localAddressRanges"))

    @local_address_ranges.setter
    def local_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07b9c0e3fece50124c905e807cee4c24573482fbafe1fda85d53a8a2fe604e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteAddressRanges")
    def remote_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteAddressRanges"))

    @remote_address_ranges.setter
    def remote_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d09dbd75e738d14c4c1fff085b842238244167ab295d684945847f52412d726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTrafficSelectorPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTrafficSelectorPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTrafficSelectorPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d39fb8f1ecf18a0faacb76a2f801264b77d597e5f5eb7f0e5573cdbd6121766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLink",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "vpn_site_link_id": "vpnSiteLinkId",
        "bandwidth_mbps": "bandwidthMbps",
        "bgp_enabled": "bgpEnabled",
        "connection_mode": "connectionMode",
        "custom_bgp_address": "customBgpAddress",
        "egress_nat_rule_ids": "egressNatRuleIds",
        "ingress_nat_rule_ids": "ingressNatRuleIds",
        "ipsec_policy": "ipsecPolicy",
        "local_azure_ip_address_enabled": "localAzureIpAddressEnabled",
        "policy_based_traffic_selector_enabled": "policyBasedTrafficSelectorEnabled",
        "protocol": "protocol",
        "ratelimit_enabled": "ratelimitEnabled",
        "route_weight": "routeWeight",
        "shared_key": "sharedKey",
    },
)
class VpnGatewayConnectionVpnLink:
    def __init__(
        self,
        *,
        name: builtins.str,
        vpn_site_link_id: builtins.str,
        bandwidth_mbps: typing.Optional[jsii.Number] = None,
        bgp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection_mode: typing.Optional[builtins.str] = None,
        custom_bgp_address: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionVpnLinkCustomBgpAddress", typing.Dict[builtins.str, typing.Any]]]]] = None,
        egress_nat_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ingress_nat_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ipsec_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnGatewayConnectionVpnLinkIpsecPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        local_azure_ip_address_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_based_traffic_selector_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol: typing.Optional[builtins.str] = None,
        ratelimit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        route_weight: typing.Optional[jsii.Number] = None,
        shared_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#name VpnGatewayConnection#name}.
        :param vpn_site_link_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_site_link_id VpnGatewayConnection#vpn_site_link_id}.
        :param bandwidth_mbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#bandwidth_mbps VpnGatewayConnection#bandwidth_mbps}.
        :param bgp_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#bgp_enabled VpnGatewayConnection#bgp_enabled}.
        :param connection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#connection_mode VpnGatewayConnection#connection_mode}.
        :param custom_bgp_address: custom_bgp_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#custom_bgp_address VpnGatewayConnection#custom_bgp_address}
        :param egress_nat_rule_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#egress_nat_rule_ids VpnGatewayConnection#egress_nat_rule_ids}.
        :param ingress_nat_rule_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ingress_nat_rule_ids VpnGatewayConnection#ingress_nat_rule_ids}.
        :param ipsec_policy: ipsec_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ipsec_policy VpnGatewayConnection#ipsec_policy}
        :param local_azure_ip_address_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#local_azure_ip_address_enabled VpnGatewayConnection#local_azure_ip_address_enabled}.
        :param policy_based_traffic_selector_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#policy_based_traffic_selector_enabled VpnGatewayConnection#policy_based_traffic_selector_enabled}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#protocol VpnGatewayConnection#protocol}.
        :param ratelimit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ratelimit_enabled VpnGatewayConnection#ratelimit_enabled}.
        :param route_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#route_weight VpnGatewayConnection#route_weight}.
        :param shared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#shared_key VpnGatewayConnection#shared_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0fc820debee847678fe8b586b88fb18c28db46def8f686ef5170b8c407be5d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vpn_site_link_id", value=vpn_site_link_id, expected_type=type_hints["vpn_site_link_id"])
            check_type(argname="argument bandwidth_mbps", value=bandwidth_mbps, expected_type=type_hints["bandwidth_mbps"])
            check_type(argname="argument bgp_enabled", value=bgp_enabled, expected_type=type_hints["bgp_enabled"])
            check_type(argname="argument connection_mode", value=connection_mode, expected_type=type_hints["connection_mode"])
            check_type(argname="argument custom_bgp_address", value=custom_bgp_address, expected_type=type_hints["custom_bgp_address"])
            check_type(argname="argument egress_nat_rule_ids", value=egress_nat_rule_ids, expected_type=type_hints["egress_nat_rule_ids"])
            check_type(argname="argument ingress_nat_rule_ids", value=ingress_nat_rule_ids, expected_type=type_hints["ingress_nat_rule_ids"])
            check_type(argname="argument ipsec_policy", value=ipsec_policy, expected_type=type_hints["ipsec_policy"])
            check_type(argname="argument local_azure_ip_address_enabled", value=local_azure_ip_address_enabled, expected_type=type_hints["local_azure_ip_address_enabled"])
            check_type(argname="argument policy_based_traffic_selector_enabled", value=policy_based_traffic_selector_enabled, expected_type=type_hints["policy_based_traffic_selector_enabled"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument ratelimit_enabled", value=ratelimit_enabled, expected_type=type_hints["ratelimit_enabled"])
            check_type(argname="argument route_weight", value=route_weight, expected_type=type_hints["route_weight"])
            check_type(argname="argument shared_key", value=shared_key, expected_type=type_hints["shared_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vpn_site_link_id": vpn_site_link_id,
        }
        if bandwidth_mbps is not None:
            self._values["bandwidth_mbps"] = bandwidth_mbps
        if bgp_enabled is not None:
            self._values["bgp_enabled"] = bgp_enabled
        if connection_mode is not None:
            self._values["connection_mode"] = connection_mode
        if custom_bgp_address is not None:
            self._values["custom_bgp_address"] = custom_bgp_address
        if egress_nat_rule_ids is not None:
            self._values["egress_nat_rule_ids"] = egress_nat_rule_ids
        if ingress_nat_rule_ids is not None:
            self._values["ingress_nat_rule_ids"] = ingress_nat_rule_ids
        if ipsec_policy is not None:
            self._values["ipsec_policy"] = ipsec_policy
        if local_azure_ip_address_enabled is not None:
            self._values["local_azure_ip_address_enabled"] = local_azure_ip_address_enabled
        if policy_based_traffic_selector_enabled is not None:
            self._values["policy_based_traffic_selector_enabled"] = policy_based_traffic_selector_enabled
        if protocol is not None:
            self._values["protocol"] = protocol
        if ratelimit_enabled is not None:
            self._values["ratelimit_enabled"] = ratelimit_enabled
        if route_weight is not None:
            self._values["route_weight"] = route_weight
        if shared_key is not None:
            self._values["shared_key"] = shared_key

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#name VpnGatewayConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpn_site_link_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#vpn_site_link_id VpnGatewayConnection#vpn_site_link_id}.'''
        result = self._values.get("vpn_site_link_id")
        assert result is not None, "Required property 'vpn_site_link_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bandwidth_mbps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#bandwidth_mbps VpnGatewayConnection#bandwidth_mbps}.'''
        result = self._values.get("bandwidth_mbps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bgp_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#bgp_enabled VpnGatewayConnection#bgp_enabled}.'''
        result = self._values.get("bgp_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def connection_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#connection_mode VpnGatewayConnection#connection_mode}.'''
        result = self._values.get("connection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_bgp_address(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLinkCustomBgpAddress"]]]:
        '''custom_bgp_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#custom_bgp_address VpnGatewayConnection#custom_bgp_address}
        '''
        result = self._values.get("custom_bgp_address")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLinkCustomBgpAddress"]]], result)

    @builtins.property
    def egress_nat_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#egress_nat_rule_ids VpnGatewayConnection#egress_nat_rule_ids}.'''
        result = self._values.get("egress_nat_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ingress_nat_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ingress_nat_rule_ids VpnGatewayConnection#ingress_nat_rule_ids}.'''
        result = self._values.get("ingress_nat_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ipsec_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLinkIpsecPolicy"]]]:
        '''ipsec_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ipsec_policy VpnGatewayConnection#ipsec_policy}
        '''
        result = self._values.get("ipsec_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnGatewayConnectionVpnLinkIpsecPolicy"]]], result)

    @builtins.property
    def local_azure_ip_address_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#local_azure_ip_address_enabled VpnGatewayConnection#local_azure_ip_address_enabled}.'''
        result = self._values.get("local_azure_ip_address_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_based_traffic_selector_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#policy_based_traffic_selector_enabled VpnGatewayConnection#policy_based_traffic_selector_enabled}.'''
        result = self._values.get("policy_based_traffic_selector_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#protocol VpnGatewayConnection#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ratelimit_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ratelimit_enabled VpnGatewayConnection#ratelimit_enabled}.'''
        result = self._values.get("ratelimit_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def route_weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#route_weight VpnGatewayConnection#route_weight}.'''
        result = self._values.get("route_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shared_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#shared_key VpnGatewayConnection#shared_key}.'''
        result = self._values.get("shared_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionVpnLink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkCustomBgpAddress",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_configuration_id": "ipConfigurationId",
    },
)
class VpnGatewayConnectionVpnLinkCustomBgpAddress:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_configuration_id: builtins.str,
    ) -> None:
        '''
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ip_address VpnGatewayConnection#ip_address}.
        :param ip_configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ip_configuration_id VpnGatewayConnection#ip_configuration_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66d51a6faf5c5fcde5b9ec0c8d19b928824245cab4619acf93afff742ba0c12)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_configuration_id", value=ip_configuration_id, expected_type=type_hints["ip_configuration_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address": ip_address,
            "ip_configuration_id": ip_configuration_id,
        }

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ip_address VpnGatewayConnection#ip_address}.'''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_configuration_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ip_configuration_id VpnGatewayConnection#ip_configuration_id}.'''
        result = self._values.get("ip_configuration_id")
        assert result is not None, "Required property 'ip_configuration_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionVpnLinkCustomBgpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnGatewayConnectionVpnLinkCustomBgpAddressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkCustomBgpAddressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dadd3f51ed117a306bd2fea6944311899e7f927f0e274113ea79db0195a1e01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VpnGatewayConnectionVpnLinkCustomBgpAddressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f33d9f363b27953c685a6f99e29038d9f2a71a793ca6580ca36aa37324b803)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnGatewayConnectionVpnLinkCustomBgpAddressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9b0d2c026afc6b1f1b37d6e95f331770a1e957231a2ccf2e7362497ae3204e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e799d7119b82b0cc01a9225df6d7927408cf1fca03beae0f357927f249d03e08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd2ed25897270700ce2b6dc44cc5dacfe4fbf3243d3a830f405aa6078672b90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkCustomBgpAddress]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkCustomBgpAddress]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkCustomBgpAddress]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead0a9b26ebe59bc1718eee9c314aa3690fdd80f61eea1a540c72af0faf05ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnGatewayConnectionVpnLinkCustomBgpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkCustomBgpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__395666230c72f19dbfa7dd0a7fe357e32b74d9e8e2e4063bbda0d1c38690d437)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationIdInput")
    def ip_configuration_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipConfigurationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99e1c059b48a9badc19d76e2259587f381b75e458cfae1cbf89897d26db724f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationId")
    def ip_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipConfigurationId"))

    @ip_configuration_id.setter
    def ip_configuration_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ba2ffb0c9651587bfd25160bb764512909ff0e48628f0ac5c618de14f69d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipConfigurationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkCustomBgpAddress]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkCustomBgpAddress]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkCustomBgpAddress]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db27e5f624a71af8f5e7ceb40bf4e08af7155bb555bee64d4af4d3effb3588b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkIpsecPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "dh_group": "dhGroup",
        "encryption_algorithm": "encryptionAlgorithm",
        "ike_encryption_algorithm": "ikeEncryptionAlgorithm",
        "ike_integrity_algorithm": "ikeIntegrityAlgorithm",
        "integrity_algorithm": "integrityAlgorithm",
        "pfs_group": "pfsGroup",
        "sa_data_size_kb": "saDataSizeKb",
        "sa_lifetime_sec": "saLifetimeSec",
    },
)
class VpnGatewayConnectionVpnLinkIpsecPolicy:
    def __init__(
        self,
        *,
        dh_group: builtins.str,
        encryption_algorithm: builtins.str,
        ike_encryption_algorithm: builtins.str,
        ike_integrity_algorithm: builtins.str,
        integrity_algorithm: builtins.str,
        pfs_group: builtins.str,
        sa_data_size_kb: jsii.Number,
        sa_lifetime_sec: jsii.Number,
    ) -> None:
        '''
        :param dh_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#dh_group VpnGatewayConnection#dh_group}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#encryption_algorithm VpnGatewayConnection#encryption_algorithm}.
        :param ike_encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ike_encryption_algorithm VpnGatewayConnection#ike_encryption_algorithm}.
        :param ike_integrity_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ike_integrity_algorithm VpnGatewayConnection#ike_integrity_algorithm}.
        :param integrity_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#integrity_algorithm VpnGatewayConnection#integrity_algorithm}.
        :param pfs_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#pfs_group VpnGatewayConnection#pfs_group}.
        :param sa_data_size_kb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#sa_data_size_kb VpnGatewayConnection#sa_data_size_kb}.
        :param sa_lifetime_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#sa_lifetime_sec VpnGatewayConnection#sa_lifetime_sec}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647f10d943e536d23661ae392f039ff46d3b1d6eea6a629b7b8f00f1369df9bb)
            check_type(argname="argument dh_group", value=dh_group, expected_type=type_hints["dh_group"])
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument ike_encryption_algorithm", value=ike_encryption_algorithm, expected_type=type_hints["ike_encryption_algorithm"])
            check_type(argname="argument ike_integrity_algorithm", value=ike_integrity_algorithm, expected_type=type_hints["ike_integrity_algorithm"])
            check_type(argname="argument integrity_algorithm", value=integrity_algorithm, expected_type=type_hints["integrity_algorithm"])
            check_type(argname="argument pfs_group", value=pfs_group, expected_type=type_hints["pfs_group"])
            check_type(argname="argument sa_data_size_kb", value=sa_data_size_kb, expected_type=type_hints["sa_data_size_kb"])
            check_type(argname="argument sa_lifetime_sec", value=sa_lifetime_sec, expected_type=type_hints["sa_lifetime_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dh_group": dh_group,
            "encryption_algorithm": encryption_algorithm,
            "ike_encryption_algorithm": ike_encryption_algorithm,
            "ike_integrity_algorithm": ike_integrity_algorithm,
            "integrity_algorithm": integrity_algorithm,
            "pfs_group": pfs_group,
            "sa_data_size_kb": sa_data_size_kb,
            "sa_lifetime_sec": sa_lifetime_sec,
        }

    @builtins.property
    def dh_group(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#dh_group VpnGatewayConnection#dh_group}.'''
        result = self._values.get("dh_group")
        assert result is not None, "Required property 'dh_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#encryption_algorithm VpnGatewayConnection#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        assert result is not None, "Required property 'encryption_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ike_encryption_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ike_encryption_algorithm VpnGatewayConnection#ike_encryption_algorithm}.'''
        result = self._values.get("ike_encryption_algorithm")
        assert result is not None, "Required property 'ike_encryption_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ike_integrity_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#ike_integrity_algorithm VpnGatewayConnection#ike_integrity_algorithm}.'''
        result = self._values.get("ike_integrity_algorithm")
        assert result is not None, "Required property 'ike_integrity_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integrity_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#integrity_algorithm VpnGatewayConnection#integrity_algorithm}.'''
        result = self._values.get("integrity_algorithm")
        assert result is not None, "Required property 'integrity_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pfs_group(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#pfs_group VpnGatewayConnection#pfs_group}.'''
        result = self._values.get("pfs_group")
        assert result is not None, "Required property 'pfs_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sa_data_size_kb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#sa_data_size_kb VpnGatewayConnection#sa_data_size_kb}.'''
        result = self._values.get("sa_data_size_kb")
        assert result is not None, "Required property 'sa_data_size_kb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sa_lifetime_sec(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_gateway_connection#sa_lifetime_sec VpnGatewayConnection#sa_lifetime_sec}.'''
        result = self._values.get("sa_lifetime_sec")
        assert result is not None, "Required property 'sa_lifetime_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnGatewayConnectionVpnLinkIpsecPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnGatewayConnectionVpnLinkIpsecPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkIpsecPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1553dd575d28ab5396b5b149c67f9fe6e073de6af0206ae681f3c08d8b8a0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VpnGatewayConnectionVpnLinkIpsecPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d69d5c56f1e105390307a23aa3bf27ab76e3c42c150043526cf7df23d1943c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnGatewayConnectionVpnLinkIpsecPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1c216d4870a191a81eb03fc71c66ed97f42771a1703c9b98af3812eef63947)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e8d29aa212225c02e93a33f49ce2664e295dd83207fb7674cf78ec60fa0f691)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc872c4b0f848575255d2824fb34fee0bc305bd8ca5a4a50be745ea1446ebd3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkIpsecPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkIpsecPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkIpsecPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679f3bec31496782758290340649fdbec5be20d3869658b1b7e7eb3dddb4d6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnGatewayConnectionVpnLinkIpsecPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkIpsecPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1c5619d047fe8d3be3062d14092f00654862a14a3ef9b5a1d0e1bec0751ea55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dhGroupInput")
    def dh_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dhGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithmInput")
    def encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeEncryptionAlgorithmInput")
    def ike_encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ikeEncryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeIntegrityAlgorithmInput")
    def ike_integrity_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ikeIntegrityAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="integrityAlgorithmInput")
    def integrity_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrityAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="pfsGroupInput")
    def pfs_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pfsGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="saDataSizeKbInput")
    def sa_data_size_kb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "saDataSizeKbInput"))

    @builtins.property
    @jsii.member(jsii_name="saLifetimeSecInput")
    def sa_lifetime_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "saLifetimeSecInput"))

    @builtins.property
    @jsii.member(jsii_name="dhGroup")
    def dh_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dhGroup"))

    @dh_group.setter
    def dh_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602382e64619a3f571f53a12d1adb6ad575498e944491c2756da69cbbc639283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dhGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithm")
    def encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAlgorithm"))

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb4dcd84f4f2b09545a42527ae1e6ce634c687c5082b6037281cb749aac02a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ikeEncryptionAlgorithm")
    def ike_encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeEncryptionAlgorithm"))

    @ike_encryption_algorithm.setter
    def ike_encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329123dd2925bbd1b90699adc11dec790ef0a63b788ce9c94151ff83ea4550fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeEncryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ikeIntegrityAlgorithm")
    def ike_integrity_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeIntegrityAlgorithm"))

    @ike_integrity_algorithm.setter
    def ike_integrity_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87804271866436250a0a8ce8910c21380ba2d800326e00e05a4e380f512ff8ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeIntegrityAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrityAlgorithm")
    def integrity_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrityAlgorithm"))

    @integrity_algorithm.setter
    def integrity_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4bd85cc8a5a5bc8a79cc652ee8692c9a7197705d36f37c7e4e172a3fb24989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrityAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pfsGroup")
    def pfs_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pfsGroup"))

    @pfs_group.setter
    def pfs_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b7dc57c42d4a016cf17453b9fffbdaecd610e07ac297ff3b1d71010a4c0da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pfsGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saDataSizeKb")
    def sa_data_size_kb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "saDataSizeKb"))

    @sa_data_size_kb.setter
    def sa_data_size_kb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b84a6fe38317a11ba99c26c3a8516b029ecd609b56185ddd56f5ab0e17d8177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saDataSizeKb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saLifetimeSec")
    def sa_lifetime_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "saLifetimeSec"))

    @sa_lifetime_sec.setter
    def sa_lifetime_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed9e060266d73c52232d750e8cd474e4feeb4145d4bb6211414e2cf0051bf93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saLifetimeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkIpsecPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkIpsecPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkIpsecPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd340a25dea073b69145459599e13d5cecd454fd87cf14f0eedb4050ed9d53b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnGatewayConnectionVpnLinkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbf98d0ed15d3f31cd73494438896faf8e8f4f558766c094eed92ff4599dd10c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnGatewayConnectionVpnLinkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac58dbb9109ac046de651b08036eb832e62821a3f3ef3b94e403f9561ca70e6a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnGatewayConnectionVpnLinkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b26cf5435adc0991c282ecd0d30904eaa9b2165acf064972a20d32ede34c908)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eb3fb08552d38e560fa1b40ac3b965bc202d3681f284740ceb291237a9330ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__624182ef7e6a894a2f87bafe941e982abc3928d401f3af9d9b43cbaf37f6ff6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLink]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLink]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLink]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032d6f31fc05654ee4b66ae97afb2c2cad2253dfb65ddbf372cf68533db212ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnGatewayConnectionVpnLinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnGatewayConnection.VpnGatewayConnectionVpnLinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a92667eb4c10f50bfcb2c75626b46b3c14a7020cc2e3038694074d50745f3d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomBgpAddress")
    def put_custom_bgp_address(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLinkCustomBgpAddress, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b4f9adda0d5e5bfd3627789d0a9f612976336d3a19183aa5ab9b9c161dbd01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomBgpAddress", [value]))

    @jsii.member(jsii_name="putIpsecPolicy")
    def put_ipsec_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLinkIpsecPolicy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32512344d69c4488af722219b6ed12d11cd72b184c6fad80fa64ad3a2481bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpsecPolicy", [value]))

    @jsii.member(jsii_name="resetBandwidthMbps")
    def reset_bandwidth_mbps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthMbps", []))

    @jsii.member(jsii_name="resetBgpEnabled")
    def reset_bgp_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpEnabled", []))

    @jsii.member(jsii_name="resetConnectionMode")
    def reset_connection_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionMode", []))

    @jsii.member(jsii_name="resetCustomBgpAddress")
    def reset_custom_bgp_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomBgpAddress", []))

    @jsii.member(jsii_name="resetEgressNatRuleIds")
    def reset_egress_nat_rule_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressNatRuleIds", []))

    @jsii.member(jsii_name="resetIngressNatRuleIds")
    def reset_ingress_nat_rule_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressNatRuleIds", []))

    @jsii.member(jsii_name="resetIpsecPolicy")
    def reset_ipsec_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpsecPolicy", []))

    @jsii.member(jsii_name="resetLocalAzureIpAddressEnabled")
    def reset_local_azure_ip_address_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAzureIpAddressEnabled", []))

    @jsii.member(jsii_name="resetPolicyBasedTrafficSelectorEnabled")
    def reset_policy_based_traffic_selector_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyBasedTrafficSelectorEnabled", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRatelimitEnabled")
    def reset_ratelimit_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRatelimitEnabled", []))

    @jsii.member(jsii_name="resetRouteWeight")
    def reset_route_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteWeight", []))

    @jsii.member(jsii_name="resetSharedKey")
    def reset_shared_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedKey", []))

    @builtins.property
    @jsii.member(jsii_name="customBgpAddress")
    def custom_bgp_address(self) -> VpnGatewayConnectionVpnLinkCustomBgpAddressList:
        return typing.cast(VpnGatewayConnectionVpnLinkCustomBgpAddressList, jsii.get(self, "customBgpAddress"))

    @builtins.property
    @jsii.member(jsii_name="ipsecPolicy")
    def ipsec_policy(self) -> VpnGatewayConnectionVpnLinkIpsecPolicyList:
        return typing.cast(VpnGatewayConnectionVpnLinkIpsecPolicyList, jsii.get(self, "ipsecPolicy"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthMbpsInput")
    def bandwidth_mbps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthMbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpEnabledInput")
    def bgp_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bgpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionModeInput")
    def connection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="customBgpAddressInput")
    def custom_bgp_address_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkCustomBgpAddress]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkCustomBgpAddress]]], jsii.get(self, "customBgpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="egressNatRuleIdsInput")
    def egress_nat_rule_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "egressNatRuleIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressNatRuleIdsInput")
    def ingress_nat_rule_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ingressNatRuleIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsecPolicyInput")
    def ipsec_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkIpsecPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkIpsecPolicy]]], jsii.get(self, "ipsecPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="localAzureIpAddressEnabledInput")
    def local_azure_ip_address_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localAzureIpAddressEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyBasedTrafficSelectorEnabledInput")
    def policy_based_traffic_selector_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "policyBasedTrafficSelectorEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="ratelimitEnabledInput")
    def ratelimit_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ratelimitEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="routeWeightInput")
    def route_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "routeWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedKeyInput")
    def shared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnSiteLinkIdInput")
    def vpn_site_link_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnSiteLinkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthMbps")
    def bandwidth_mbps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthMbps"))

    @bandwidth_mbps.setter
    def bandwidth_mbps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c602f148708b812930270369635ba90eecdf13d702eb4f488611d631aead93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthMbps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpEnabled")
    def bgp_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bgpEnabled"))

    @bgp_enabled.setter
    def bgp_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8129fb868874bc6a4740c76d7928fd929b4eb42b8d99809035e6c9568a3d1034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionMode")
    def connection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionMode"))

    @connection_mode.setter
    def connection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209273bc1a80148348482b6cc5fcfd371ec1038af7c1724d6e0efbb490a68770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="egressNatRuleIds")
    def egress_nat_rule_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "egressNatRuleIds"))

    @egress_nat_rule_ids.setter
    def egress_nat_rule_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33bd5443c2288ab6077bcce21ea5377012b5e8d4f700e8b90ac8d5019742f129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressNatRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressNatRuleIds")
    def ingress_nat_rule_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ingressNatRuleIds"))

    @ingress_nat_rule_ids.setter
    def ingress_nat_rule_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb849a50b3a4d23d50001fddcc9275a701f0d8b1a31727dfaf4c9de3c3582a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressNatRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAzureIpAddressEnabled")
    def local_azure_ip_address_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localAzureIpAddressEnabled"))

    @local_azure_ip_address_enabled.setter
    def local_azure_ip_address_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a705b9265012cc46a4439eaab682875d436032cc687154bec0a1140443b923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAzureIpAddressEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a655aa83676c2087a76a03b77300f24774aabb0d49775b47c3a62eac843c53d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyBasedTrafficSelectorEnabled")
    def policy_based_traffic_selector_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "policyBasedTrafficSelectorEnabled"))

    @policy_based_traffic_selector_enabled.setter
    def policy_based_traffic_selector_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11abc45c435a6f87b1ffc18200ea0564206c3b023f4dbc9e7fbbaceeb1237c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyBasedTrafficSelectorEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839d240716089842c74b1bccf051b72bd37db526c9ce89c3284ca000020ab149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ratelimitEnabled")
    def ratelimit_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ratelimitEnabled"))

    @ratelimit_enabled.setter
    def ratelimit_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314c3475a33a80cab1f5cb163fcf9c592d279c0101bb2bc9e892aa33ef2329fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ratelimitEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeWeight")
    def route_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "routeWeight"))

    @route_weight.setter
    def route_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84115297b43bf96642e43df8d238c377fc9b612c31f7b52a21a47796191a0967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeWeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedKey")
    def shared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedKey"))

    @shared_key.setter
    def shared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af45f3fa1f1900e3707b43578bd2572d0e7935723f660db2501c9a3c1bf2c20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnSiteLinkId")
    def vpn_site_link_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnSiteLinkId"))

    @vpn_site_link_id.setter
    def vpn_site_link_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492baa17148f16edf99697696803a15da5333500ac7c08679e58a0bd5aff5ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnSiteLinkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLink]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLink]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLink]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f101554a35c537627c593716619f6f31d0d0dd5b5795d3b4b7406515848e3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VpnGatewayConnection",
    "VpnGatewayConnectionConfig",
    "VpnGatewayConnectionRouting",
    "VpnGatewayConnectionRoutingOutputReference",
    "VpnGatewayConnectionRoutingPropagatedRouteTable",
    "VpnGatewayConnectionRoutingPropagatedRouteTableOutputReference",
    "VpnGatewayConnectionTimeouts",
    "VpnGatewayConnectionTimeoutsOutputReference",
    "VpnGatewayConnectionTrafficSelectorPolicy",
    "VpnGatewayConnectionTrafficSelectorPolicyList",
    "VpnGatewayConnectionTrafficSelectorPolicyOutputReference",
    "VpnGatewayConnectionVpnLink",
    "VpnGatewayConnectionVpnLinkCustomBgpAddress",
    "VpnGatewayConnectionVpnLinkCustomBgpAddressList",
    "VpnGatewayConnectionVpnLinkCustomBgpAddressOutputReference",
    "VpnGatewayConnectionVpnLinkIpsecPolicy",
    "VpnGatewayConnectionVpnLinkIpsecPolicyList",
    "VpnGatewayConnectionVpnLinkIpsecPolicyOutputReference",
    "VpnGatewayConnectionVpnLinkList",
    "VpnGatewayConnectionVpnLinkOutputReference",
]

publication.publish()

def _typecheckingstub__66839de53f6cd750154f5e88ed7d6452b697d981211373c2aa18b40103376a0d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    remote_vpn_site_id: builtins.str,
    vpn_gateway_id: builtins.str,
    vpn_link: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLink, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing: typing.Optional[typing.Union[VpnGatewayConnectionRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[VpnGatewayConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_selector_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionTrafficSelectorPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__f84066471d2f29c3693c1e37b28e3459aad335dd21404b3acaffb781e8d0e48b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d3b9d7ee401bfb245129f2986633111983c9552c59d2862185076dfac15048(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionTrafficSelectorPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e210e0b66f6e39c83eacb3f280fe5da77adfc2d6e6d5096d392fbf1c144f7a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLink, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b4950463ef3753fca305ba8bee2ad27d1b9e13985f6a9ce2aefb23018c014a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5e5f35fcc774453e42df9da77b9dc9244ec530e0b741faf54721313a14e85f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cf5a938d959dd26175164d5f41c86a11f7784f6a16e440693e1f439a36f862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9486d6fb36b0567bc05d6661ad8acfeba393a8db1990aede93879afc17c49cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2b8e16ccb4297b111025f17bb22f44361210e2400188a4f5d223125c2a4c8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05e6f0751a2aa2e1a82b95c342c612d07ec9af10eecbe0a2aca4f7a9b92dba0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    remote_vpn_site_id: builtins.str,
    vpn_gateway_id: builtins.str,
    vpn_link: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLink, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing: typing.Optional[typing.Union[VpnGatewayConnectionRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[VpnGatewayConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_selector_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionTrafficSelectorPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fd813c4870523dc0278d3c8aafca2c4922935b4ae06ef1eeb519fec1ee3a5c(
    *,
    associated_route_table: builtins.str,
    inbound_route_map_id: typing.Optional[builtins.str] = None,
    outbound_route_map_id: typing.Optional[builtins.str] = None,
    propagated_route_table: typing.Optional[typing.Union[VpnGatewayConnectionRoutingPropagatedRouteTable, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cab903fbf7ff07080088d403543f99dfdaea17748956681b3522caaa6e3419(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17df1c90979f7e9d2db3b11e2a9f0e066a421c069daafc61e5b9e5701047263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ab40916568b2ab27fcc7a358be803bed8aa59a083c774582b09377d49f6ae9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340da0b4c9bceea3e07e49f12e3e4115974eb2b2a8ce6b2028638bc96737c725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7299d33dac661c958ffd25df29f24accbf90c6e3840dd2d386b71a3c2502fa(
    value: typing.Optional[VpnGatewayConnectionRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669c6d63293b891185bf3b8d9fbe3114a59f84bd72e25f48e8b270db672dc7e4(
    *,
    route_table_ids: typing.Sequence[builtins.str],
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6fda737a27817897f1990f64b213b79c2ca75537e5b21fda98edf1f02228c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d75387e11071e4a09cd82d4c02d597e47eff344a97b36f7ad56de4a0a1ce6da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae3136af98529047a4dd06b9e2eb39c0eda66484f4ca063af80b9f636565b9a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d6ca7602e91fac48605b7f6ed609919f53c30f276bd2e4c669fb9855e45c92(
    value: typing.Optional[VpnGatewayConnectionRoutingPropagatedRouteTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606289fe1ec967f65c0cbae68778ba08df3956a0954cff7c049e01251df4b760(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccd7d947a501b1b0d9d13520ca4456a3a9254c36fb6eace8e656e668a298ef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292877638b96d009978e0af708876c232a8340d0655775549d84fa4d530c4141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc32796b21ddff958ba66dd9fb4a11f6508cc2f88cef0ab658ceeb95aca4255(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ca6055d31c4c168e7aa420ada75bdd20a0ce9512084262bed2ff43cd36b22e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ab99f1c060581dd38bbb71fffc71271da6d94d656b112066ff72a59a646db7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fc71a42c63448feaad2a4bd58816a527aa364cff5e1c20946f7748abc41d97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9f17669918468e70fd5888582a305f868c44fb7f9f96403ce35b29e90df3e6(
    *,
    local_address_ranges: typing.Sequence[builtins.str],
    remote_address_ranges: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30357505c0f99bc6f2127e076b823d34fa446e6fb44acd5946132222f8021ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22dbfadbb6311b4dcb74753dbb6058543252e99e5543e4ef39f9c6b2dccc244(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145d2f0e3b9ec47f7537bf916c5ab97be48013959cf166af2322f1869e69677f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a1f9f04a29ee741627ff30463098276cecb6ae64414e0f55df88a91699c833(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fb816303dcd501cfbc40f599fea538bae850a46c296655e49a28c49d759ddd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c71773b720e8dea7ad58a3c0c53b8a71b795b38efde865ac26c03799a5bf68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionTrafficSelectorPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4f87b789dae7a7508f9d5929c4f4822fe437a1c29bb5b6cde971e5099131e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07b9c0e3fece50124c905e807cee4c24573482fbafe1fda85d53a8a2fe604e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d09dbd75e738d14c4c1fff085b842238244167ab295d684945847f52412d726(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d39fb8f1ecf18a0faacb76a2f801264b77d597e5f5eb7f0e5573cdbd6121766(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionTrafficSelectorPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0fc820debee847678fe8b586b88fb18c28db46def8f686ef5170b8c407be5d(
    *,
    name: builtins.str,
    vpn_site_link_id: builtins.str,
    bandwidth_mbps: typing.Optional[jsii.Number] = None,
    bgp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection_mode: typing.Optional[builtins.str] = None,
    custom_bgp_address: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLinkCustomBgpAddress, typing.Dict[builtins.str, typing.Any]]]]] = None,
    egress_nat_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ingress_nat_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipsec_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLinkIpsecPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    local_azure_ip_address_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_based_traffic_selector_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol: typing.Optional[builtins.str] = None,
    ratelimit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    route_weight: typing.Optional[jsii.Number] = None,
    shared_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66d51a6faf5c5fcde5b9ec0c8d19b928824245cab4619acf93afff742ba0c12(
    *,
    ip_address: builtins.str,
    ip_configuration_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dadd3f51ed117a306bd2fea6944311899e7f927f0e274113ea79db0195a1e01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f33d9f363b27953c685a6f99e29038d9f2a71a793ca6580ca36aa37324b803(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9b0d2c026afc6b1f1b37d6e95f331770a1e957231a2ccf2e7362497ae3204e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e799d7119b82b0cc01a9225df6d7927408cf1fca03beae0f357927f249d03e08(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2ed25897270700ce2b6dc44cc5dacfe4fbf3243d3a830f405aa6078672b90d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead0a9b26ebe59bc1718eee9c314aa3690fdd80f61eea1a540c72af0faf05ee9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkCustomBgpAddress]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395666230c72f19dbfa7dd0a7fe357e32b74d9e8e2e4063bbda0d1c38690d437(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99e1c059b48a9badc19d76e2259587f381b75e458cfae1cbf89897d26db724f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ba2ffb0c9651587bfd25160bb764512909ff0e48628f0ac5c618de14f69d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db27e5f624a71af8f5e7ceb40bf4e08af7155bb555bee64d4af4d3effb3588b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkCustomBgpAddress]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647f10d943e536d23661ae392f039ff46d3b1d6eea6a629b7b8f00f1369df9bb(
    *,
    dh_group: builtins.str,
    encryption_algorithm: builtins.str,
    ike_encryption_algorithm: builtins.str,
    ike_integrity_algorithm: builtins.str,
    integrity_algorithm: builtins.str,
    pfs_group: builtins.str,
    sa_data_size_kb: jsii.Number,
    sa_lifetime_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1553dd575d28ab5396b5b149c67f9fe6e073de6af0206ae681f3c08d8b8a0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d69d5c56f1e105390307a23aa3bf27ab76e3c42c150043526cf7df23d1943c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1c216d4870a191a81eb03fc71c66ed97f42771a1703c9b98af3812eef63947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8d29aa212225c02e93a33f49ce2664e295dd83207fb7674cf78ec60fa0f691(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc872c4b0f848575255d2824fb34fee0bc305bd8ca5a4a50be745ea1446ebd3a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679f3bec31496782758290340649fdbec5be20d3869658b1b7e7eb3dddb4d6a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLinkIpsecPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c5619d047fe8d3be3062d14092f00654862a14a3ef9b5a1d0e1bec0751ea55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602382e64619a3f571f53a12d1adb6ad575498e944491c2756da69cbbc639283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb4dcd84f4f2b09545a42527ae1e6ce634c687c5082b6037281cb749aac02a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329123dd2925bbd1b90699adc11dec790ef0a63b788ce9c94151ff83ea4550fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87804271866436250a0a8ce8910c21380ba2d800326e00e05a4e380f512ff8ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4bd85cc8a5a5bc8a79cc652ee8692c9a7197705d36f37c7e4e172a3fb24989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b7dc57c42d4a016cf17453b9fffbdaecd610e07ac297ff3b1d71010a4c0da4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b84a6fe38317a11ba99c26c3a8516b029ecd609b56185ddd56f5ab0e17d8177(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed9e060266d73c52232d750e8cd474e4feeb4145d4bb6211414e2cf0051bf93(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd340a25dea073b69145459599e13d5cecd454fd87cf14f0eedb4050ed9d53b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLinkIpsecPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf98d0ed15d3f31cd73494438896faf8e8f4f558766c094eed92ff4599dd10c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac58dbb9109ac046de651b08036eb832e62821a3f3ef3b94e403f9561ca70e6a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b26cf5435adc0991c282ecd0d30904eaa9b2165acf064972a20d32ede34c908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb3fb08552d38e560fa1b40ac3b965bc202d3681f284740ceb291237a9330ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624182ef7e6a894a2f87bafe941e982abc3928d401f3af9d9b43cbaf37f6ff6f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032d6f31fc05654ee4b66ae97afb2c2cad2253dfb65ddbf372cf68533db212ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnGatewayConnectionVpnLink]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a92667eb4c10f50bfcb2c75626b46b3c14a7020cc2e3038694074d50745f3d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b4f9adda0d5e5bfd3627789d0a9f612976336d3a19183aa5ab9b9c161dbd01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLinkCustomBgpAddress, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32512344d69c4488af722219b6ed12d11cd72b184c6fad80fa64ad3a2481bec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnGatewayConnectionVpnLinkIpsecPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c602f148708b812930270369635ba90eecdf13d702eb4f488611d631aead93(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8129fb868874bc6a4740c76d7928fd929b4eb42b8d99809035e6c9568a3d1034(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209273bc1a80148348482b6cc5fcfd371ec1038af7c1724d6e0efbb490a68770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bd5443c2288ab6077bcce21ea5377012b5e8d4f700e8b90ac8d5019742f129(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb849a50b3a4d23d50001fddcc9275a701f0d8b1a31727dfaf4c9de3c3582a70(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a705b9265012cc46a4439eaab682875d436032cc687154bec0a1140443b923(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a655aa83676c2087a76a03b77300f24774aabb0d49775b47c3a62eac843c53d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11abc45c435a6f87b1ffc18200ea0564206c3b023f4dbc9e7fbbaceeb1237c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839d240716089842c74b1bccf051b72bd37db526c9ce89c3284ca000020ab149(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314c3475a33a80cab1f5cb163fcf9c592d279c0101bb2bc9e892aa33ef2329fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84115297b43bf96642e43df8d238c377fc9b612c31f7b52a21a47796191a0967(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af45f3fa1f1900e3707b43578bd2572d0e7935723f660db2501c9a3c1bf2c20b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492baa17148f16edf99697696803a15da5333500ac7c08679e58a0bd5aff5ab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f101554a35c537627c593716619f6f31d0d0dd5b5795d3b4b7406515848e3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnGatewayConnectionVpnLink]],
) -> None:
    """Type checking stubs"""
    pass
