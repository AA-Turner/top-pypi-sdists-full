r'''
# `azurerm_virtual_hub_connection`

Refer to the Terraform Registry for docs: [`azurerm_virtual_hub_connection`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection).
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


class VirtualHubConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection azurerm_virtual_hub_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        remote_virtual_network_id: builtins.str,
        virtual_hub_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing: typing.Optional[typing.Union["VirtualHubConnectionRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["VirtualHubConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection azurerm_virtual_hub_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#name VirtualHubConnection#name}.
        :param remote_virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#remote_virtual_network_id VirtualHubConnection#remote_virtual_network_id}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#virtual_hub_id VirtualHubConnection#virtual_hub_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#id VirtualHubConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internet_security_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#internet_security_enabled VirtualHubConnection#internet_security_enabled}.
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#routing VirtualHubConnection#routing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#timeouts VirtualHubConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5807b7e6b8a2256711b7f5ef7b4f42c2648f5d5e6be37643756790c2af765e7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualHubConnectionConfig(
            name=name,
            remote_virtual_network_id=remote_virtual_network_id,
            virtual_hub_id=virtual_hub_id,
            id=id,
            internet_security_enabled=internet_security_enabled,
            routing=routing,
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
        '''Generates CDKTF code for importing a VirtualHubConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VirtualHubConnection to import.
        :param import_from_id: The id of the existing VirtualHubConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VirtualHubConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29822769f8ea80737aaa0cf39e996f8e0733fc86748b5b4cbcba0854f0b399e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRouting")
    def put_routing(
        self,
        *,
        associated_route_table_id: typing.Optional[builtins.str] = None,
        inbound_route_map_id: typing.Optional[builtins.str] = None,
        outbound_route_map_id: typing.Optional[builtins.str] = None,
        propagated_route_table: typing.Optional[typing.Union["VirtualHubConnectionRoutingPropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
        static_vnet_local_route_override_criteria: typing.Optional[builtins.str] = None,
        static_vnet_propagate_static_routes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_vnet_route: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualHubConnectionRoutingStaticVnetRoute", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param associated_route_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#associated_route_table_id VirtualHubConnection#associated_route_table_id}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#inbound_route_map_id VirtualHubConnection#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#outbound_route_map_id VirtualHubConnection#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#propagated_route_table VirtualHubConnection#propagated_route_table}
        :param static_vnet_local_route_override_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_local_route_override_criteria VirtualHubConnection#static_vnet_local_route_override_criteria}.
        :param static_vnet_propagate_static_routes_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_propagate_static_routes_enabled VirtualHubConnection#static_vnet_propagate_static_routes_enabled}.
        :param static_vnet_route: static_vnet_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_route VirtualHubConnection#static_vnet_route}
        '''
        value = VirtualHubConnectionRouting(
            associated_route_table_id=associated_route_table_id,
            inbound_route_map_id=inbound_route_map_id,
            outbound_route_map_id=outbound_route_map_id,
            propagated_route_table=propagated_route_table,
            static_vnet_local_route_override_criteria=static_vnet_local_route_override_criteria,
            static_vnet_propagate_static_routes_enabled=static_vnet_propagate_static_routes_enabled,
            static_vnet_route=static_vnet_route,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#create VirtualHubConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#delete VirtualHubConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#read VirtualHubConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#update VirtualHubConnection#update}.
        '''
        value = VirtualHubConnectionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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
    def routing(self) -> "VirtualHubConnectionRoutingOutputReference":
        return typing.cast("VirtualHubConnectionRoutingOutputReference", jsii.get(self, "routing"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualHubConnectionTimeoutsOutputReference":
        return typing.cast("VirtualHubConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="remoteVirtualNetworkIdInput")
    def remote_virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVirtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routingInput")
    def routing_input(self) -> typing.Optional["VirtualHubConnectionRouting"]:
        return typing.cast(typing.Optional["VirtualHubConnectionRouting"], jsii.get(self, "routingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualHubConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualHubConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualHubIdInput")
    def virtual_hub_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualHubIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9f6194664ce697a8e148bb2851b0eb17694505c5fe64e552e8195a34fb8389)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf313e85751a244eec73ecbc58f10913d3e32c8a0ba1433dc3d3660898b16229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internetSecurityEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6686f2459d4551717e7a244c48f771884318ebf61e4bf21265ca33e812ed7b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteVirtualNetworkId")
    def remote_virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVirtualNetworkId"))

    @remote_virtual_network_id.setter
    def remote_virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61fe410f8abf780647da0171a629c003f9806227dee89aac79579284ea9d539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVirtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualHubId")
    def virtual_hub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualHubId"))

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d7056289c443c890dfe7bd4ec23acd25440971671d290abac0824f2b540ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualHubId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionConfig",
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
        "remote_virtual_network_id": "remoteVirtualNetworkId",
        "virtual_hub_id": "virtualHubId",
        "id": "id",
        "internet_security_enabled": "internetSecurityEnabled",
        "routing": "routing",
        "timeouts": "timeouts",
    },
)
class VirtualHubConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        remote_virtual_network_id: builtins.str,
        virtual_hub_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing: typing.Optional[typing.Union["VirtualHubConnectionRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["VirtualHubConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#name VirtualHubConnection#name}.
        :param remote_virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#remote_virtual_network_id VirtualHubConnection#remote_virtual_network_id}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#virtual_hub_id VirtualHubConnection#virtual_hub_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#id VirtualHubConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internet_security_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#internet_security_enabled VirtualHubConnection#internet_security_enabled}.
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#routing VirtualHubConnection#routing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#timeouts VirtualHubConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing, dict):
            routing = VirtualHubConnectionRouting(**routing)
        if isinstance(timeouts, dict):
            timeouts = VirtualHubConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0bf00b17e2cd44eb7f916e9f9cd6da746ffab632bbc8210da040523c63a9df)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument remote_virtual_network_id", value=remote_virtual_network_id, expected_type=type_hints["remote_virtual_network_id"])
            check_type(argname="argument virtual_hub_id", value=virtual_hub_id, expected_type=type_hints["virtual_hub_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument internet_security_enabled", value=internet_security_enabled, expected_type=type_hints["internet_security_enabled"])
            check_type(argname="argument routing", value=routing, expected_type=type_hints["routing"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "remote_virtual_network_id": remote_virtual_network_id,
            "virtual_hub_id": virtual_hub_id,
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#name VirtualHubConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_virtual_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#remote_virtual_network_id VirtualHubConnection#remote_virtual_network_id}.'''
        result = self._values.get("remote_virtual_network_id")
        assert result is not None, "Required property 'remote_virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_hub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#virtual_hub_id VirtualHubConnection#virtual_hub_id}.'''
        result = self._values.get("virtual_hub_id")
        assert result is not None, "Required property 'virtual_hub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#id VirtualHubConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_security_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#internet_security_enabled VirtualHubConnection#internet_security_enabled}.'''
        result = self._values.get("internet_security_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def routing(self) -> typing.Optional["VirtualHubConnectionRouting"]:
        '''routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#routing VirtualHubConnection#routing}
        '''
        result = self._values.get("routing")
        return typing.cast(typing.Optional["VirtualHubConnectionRouting"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VirtualHubConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#timeouts VirtualHubConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VirtualHubConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualHubConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionRouting",
    jsii_struct_bases=[],
    name_mapping={
        "associated_route_table_id": "associatedRouteTableId",
        "inbound_route_map_id": "inboundRouteMapId",
        "outbound_route_map_id": "outboundRouteMapId",
        "propagated_route_table": "propagatedRouteTable",
        "static_vnet_local_route_override_criteria": "staticVnetLocalRouteOverrideCriteria",
        "static_vnet_propagate_static_routes_enabled": "staticVnetPropagateStaticRoutesEnabled",
        "static_vnet_route": "staticVnetRoute",
    },
)
class VirtualHubConnectionRouting:
    def __init__(
        self,
        *,
        associated_route_table_id: typing.Optional[builtins.str] = None,
        inbound_route_map_id: typing.Optional[builtins.str] = None,
        outbound_route_map_id: typing.Optional[builtins.str] = None,
        propagated_route_table: typing.Optional[typing.Union["VirtualHubConnectionRoutingPropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
        static_vnet_local_route_override_criteria: typing.Optional[builtins.str] = None,
        static_vnet_propagate_static_routes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        static_vnet_route: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualHubConnectionRoutingStaticVnetRoute", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param associated_route_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#associated_route_table_id VirtualHubConnection#associated_route_table_id}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#inbound_route_map_id VirtualHubConnection#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#outbound_route_map_id VirtualHubConnection#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#propagated_route_table VirtualHubConnection#propagated_route_table}
        :param static_vnet_local_route_override_criteria: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_local_route_override_criteria VirtualHubConnection#static_vnet_local_route_override_criteria}.
        :param static_vnet_propagate_static_routes_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_propagate_static_routes_enabled VirtualHubConnection#static_vnet_propagate_static_routes_enabled}.
        :param static_vnet_route: static_vnet_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_route VirtualHubConnection#static_vnet_route}
        '''
        if isinstance(propagated_route_table, dict):
            propagated_route_table = VirtualHubConnectionRoutingPropagatedRouteTable(**propagated_route_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ee447f1a5b5b620ee64896b84c6d123b6adbe2155cae1542868ab0694d311a)
            check_type(argname="argument associated_route_table_id", value=associated_route_table_id, expected_type=type_hints["associated_route_table_id"])
            check_type(argname="argument inbound_route_map_id", value=inbound_route_map_id, expected_type=type_hints["inbound_route_map_id"])
            check_type(argname="argument outbound_route_map_id", value=outbound_route_map_id, expected_type=type_hints["outbound_route_map_id"])
            check_type(argname="argument propagated_route_table", value=propagated_route_table, expected_type=type_hints["propagated_route_table"])
            check_type(argname="argument static_vnet_local_route_override_criteria", value=static_vnet_local_route_override_criteria, expected_type=type_hints["static_vnet_local_route_override_criteria"])
            check_type(argname="argument static_vnet_propagate_static_routes_enabled", value=static_vnet_propagate_static_routes_enabled, expected_type=type_hints["static_vnet_propagate_static_routes_enabled"])
            check_type(argname="argument static_vnet_route", value=static_vnet_route, expected_type=type_hints["static_vnet_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associated_route_table_id is not None:
            self._values["associated_route_table_id"] = associated_route_table_id
        if inbound_route_map_id is not None:
            self._values["inbound_route_map_id"] = inbound_route_map_id
        if outbound_route_map_id is not None:
            self._values["outbound_route_map_id"] = outbound_route_map_id
        if propagated_route_table is not None:
            self._values["propagated_route_table"] = propagated_route_table
        if static_vnet_local_route_override_criteria is not None:
            self._values["static_vnet_local_route_override_criteria"] = static_vnet_local_route_override_criteria
        if static_vnet_propagate_static_routes_enabled is not None:
            self._values["static_vnet_propagate_static_routes_enabled"] = static_vnet_propagate_static_routes_enabled
        if static_vnet_route is not None:
            self._values["static_vnet_route"] = static_vnet_route

    @builtins.property
    def associated_route_table_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#associated_route_table_id VirtualHubConnection#associated_route_table_id}.'''
        result = self._values.get("associated_route_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#inbound_route_map_id VirtualHubConnection#inbound_route_map_id}.'''
        result = self._values.get("inbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#outbound_route_map_id VirtualHubConnection#outbound_route_map_id}.'''
        result = self._values.get("outbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagated_route_table(
        self,
    ) -> typing.Optional["VirtualHubConnectionRoutingPropagatedRouteTable"]:
        '''propagated_route_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#propagated_route_table VirtualHubConnection#propagated_route_table}
        '''
        result = self._values.get("propagated_route_table")
        return typing.cast(typing.Optional["VirtualHubConnectionRoutingPropagatedRouteTable"], result)

    @builtins.property
    def static_vnet_local_route_override_criteria(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_local_route_override_criteria VirtualHubConnection#static_vnet_local_route_override_criteria}.'''
        result = self._values.get("static_vnet_local_route_override_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_vnet_propagate_static_routes_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_propagate_static_routes_enabled VirtualHubConnection#static_vnet_propagate_static_routes_enabled}.'''
        result = self._values.get("static_vnet_propagate_static_routes_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def static_vnet_route(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualHubConnectionRoutingStaticVnetRoute"]]]:
        '''static_vnet_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#static_vnet_route VirtualHubConnection#static_vnet_route}
        '''
        result = self._values.get("static_vnet_route")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualHubConnectionRoutingStaticVnetRoute"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualHubConnectionRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualHubConnectionRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2866da895f6cbc585bc1a588f45edeef2df9b683304ec73d83fdd38c1f73dd62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPropagatedRouteTable")
    def put_propagated_route_table(
        self,
        *,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#labels VirtualHubConnection#labels}.
        :param route_table_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#route_table_ids VirtualHubConnection#route_table_ids}.
        '''
        value = VirtualHubConnectionRoutingPropagatedRouteTable(
            labels=labels, route_table_ids=route_table_ids
        )

        return typing.cast(None, jsii.invoke(self, "putPropagatedRouteTable", [value]))

    @jsii.member(jsii_name="putStaticVnetRoute")
    def put_static_vnet_route(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualHubConnectionRoutingStaticVnetRoute", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969a3dd9c9b0abf81a36c15413ef4e1111bf2e5119db9bbe60b9ef5ffc55c063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStaticVnetRoute", [value]))

    @jsii.member(jsii_name="resetAssociatedRouteTableId")
    def reset_associated_route_table_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssociatedRouteTableId", []))

    @jsii.member(jsii_name="resetInboundRouteMapId")
    def reset_inbound_route_map_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInboundRouteMapId", []))

    @jsii.member(jsii_name="resetOutboundRouteMapId")
    def reset_outbound_route_map_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundRouteMapId", []))

    @jsii.member(jsii_name="resetPropagatedRouteTable")
    def reset_propagated_route_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagatedRouteTable", []))

    @jsii.member(jsii_name="resetStaticVnetLocalRouteOverrideCriteria")
    def reset_static_vnet_local_route_override_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticVnetLocalRouteOverrideCriteria", []))

    @jsii.member(jsii_name="resetStaticVnetPropagateStaticRoutesEnabled")
    def reset_static_vnet_propagate_static_routes_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticVnetPropagateStaticRoutesEnabled", []))

    @jsii.member(jsii_name="resetStaticVnetRoute")
    def reset_static_vnet_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticVnetRoute", []))

    @builtins.property
    @jsii.member(jsii_name="propagatedRouteTable")
    def propagated_route_table(
        self,
    ) -> "VirtualHubConnectionRoutingPropagatedRouteTableOutputReference":
        return typing.cast("VirtualHubConnectionRoutingPropagatedRouteTableOutputReference", jsii.get(self, "propagatedRouteTable"))

    @builtins.property
    @jsii.member(jsii_name="staticVnetRoute")
    def static_vnet_route(self) -> "VirtualHubConnectionRoutingStaticVnetRouteList":
        return typing.cast("VirtualHubConnectionRoutingStaticVnetRouteList", jsii.get(self, "staticVnetRoute"))

    @builtins.property
    @jsii.member(jsii_name="associatedRouteTableIdInput")
    def associated_route_table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associatedRouteTableIdInput"))

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
    ) -> typing.Optional["VirtualHubConnectionRoutingPropagatedRouteTable"]:
        return typing.cast(typing.Optional["VirtualHubConnectionRoutingPropagatedRouteTable"], jsii.get(self, "propagatedRouteTableInput"))

    @builtins.property
    @jsii.member(jsii_name="staticVnetLocalRouteOverrideCriteriaInput")
    def static_vnet_local_route_override_criteria_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "staticVnetLocalRouteOverrideCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="staticVnetPropagateStaticRoutesEnabledInput")
    def static_vnet_propagate_static_routes_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "staticVnetPropagateStaticRoutesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="staticVnetRouteInput")
    def static_vnet_route_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualHubConnectionRoutingStaticVnetRoute"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualHubConnectionRoutingStaticVnetRoute"]]], jsii.get(self, "staticVnetRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedRouteTableId")
    def associated_route_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associatedRouteTableId"))

    @associated_route_table_id.setter
    def associated_route_table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74e0d18e6a539e201066e6ab6c60df500e7554955ed86fe955e3d20f6baf75c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedRouteTableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundRouteMapId")
    def inbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inboundRouteMapId"))

    @inbound_route_map_id.setter
    def inbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81732414cfc6e7ddb1a4a6f9609e486c85d1b5418635b6641fd04ea58da9d0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outboundRouteMapId")
    def outbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundRouteMapId"))

    @outbound_route_map_id.setter
    def outbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84e2c1ae6457c01319fac7840250a85d0629f92c04a5cad07f4fc4f5169b24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="staticVnetLocalRouteOverrideCriteria")
    def static_vnet_local_route_override_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "staticVnetLocalRouteOverrideCriteria"))

    @static_vnet_local_route_override_criteria.setter
    def static_vnet_local_route_override_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f14c238c7e6fe080232bd4f62d6673674047a4eafc87f31a03a34424c2a563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticVnetLocalRouteOverrideCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="staticVnetPropagateStaticRoutesEnabled")
    def static_vnet_propagate_static_routes_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "staticVnetPropagateStaticRoutesEnabled"))

    @static_vnet_propagate_static_routes_enabled.setter
    def static_vnet_propagate_static_routes_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddad5da941085e4d69e52841ff88d64a2d65feff7cb16ae9455819874edf35c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticVnetPropagateStaticRoutesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VirtualHubConnectionRouting]:
        return typing.cast(typing.Optional[VirtualHubConnectionRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualHubConnectionRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b2909c0d1d0eb2f0dd66a3547a26e54d736dbce8bdb030d1ac445432eb2d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionRoutingPropagatedRouteTable",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "route_table_ids": "routeTableIds"},
)
class VirtualHubConnectionRoutingPropagatedRouteTable:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#labels VirtualHubConnection#labels}.
        :param route_table_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#route_table_ids VirtualHubConnection#route_table_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15f729244bb4c0b51f4fa5013ba88e63abf1667f148cd78893395917ad0fb12)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument route_table_ids", value=route_table_ids, expected_type=type_hints["route_table_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if route_table_ids is not None:
            self._values["route_table_ids"] = route_table_ids

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#labels VirtualHubConnection#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def route_table_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#route_table_ids VirtualHubConnection#route_table_ids}.'''
        result = self._values.get("route_table_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualHubConnectionRoutingPropagatedRouteTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualHubConnectionRoutingPropagatedRouteTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionRoutingPropagatedRouteTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab55686e477b145d3c4bcdde4a3ccf17d2d22dbb7dba69ad8f629f365db0fdcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetRouteTableIds")
    def reset_route_table_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteTableIds", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f676ff5f1ccd105ac8a55911a710019daca65071b7e6669d7c860d087e22711f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTableIds")
    def route_table_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "routeTableIds"))

    @route_table_ids.setter
    def route_table_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b458707639d78bdb6c9422043d0ec905193cd4b2e0ca0bbd374f09f01a9cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTableIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualHubConnectionRoutingPropagatedRouteTable]:
        return typing.cast(typing.Optional[VirtualHubConnectionRoutingPropagatedRouteTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualHubConnectionRoutingPropagatedRouteTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9d540553ebb0f61f3922a51131003eb70d3255848226c0c51c53d005173f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionRoutingStaticVnetRoute",
    jsii_struct_bases=[],
    name_mapping={
        "address_prefixes": "addressPrefixes",
        "name": "name",
        "next_hop_ip_address": "nextHopIpAddress",
    },
)
class VirtualHubConnectionRoutingStaticVnetRoute:
    def __init__(
        self,
        *,
        address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        next_hop_ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#address_prefixes VirtualHubConnection#address_prefixes}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#name VirtualHubConnection#name}.
        :param next_hop_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#next_hop_ip_address VirtualHubConnection#next_hop_ip_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ca4f4f2923c4db8b95042484b317d158448265e118758974d9b1ffac15968d)
            check_type(argname="argument address_prefixes", value=address_prefixes, expected_type=type_hints["address_prefixes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument next_hop_ip_address", value=next_hop_ip_address, expected_type=type_hints["next_hop_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_prefixes is not None:
            self._values["address_prefixes"] = address_prefixes
        if name is not None:
            self._values["name"] = name
        if next_hop_ip_address is not None:
            self._values["next_hop_ip_address"] = next_hop_ip_address

    @builtins.property
    def address_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#address_prefixes VirtualHubConnection#address_prefixes}.'''
        result = self._values.get("address_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#name VirtualHubConnection#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_hop_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#next_hop_ip_address VirtualHubConnection#next_hop_ip_address}.'''
        result = self._values.get("next_hop_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualHubConnectionRoutingStaticVnetRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualHubConnectionRoutingStaticVnetRouteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionRoutingStaticVnetRouteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ff85d30586ba83c913b21b9ce7010c1298e966d19a4a9d60fa845b01aae753c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualHubConnectionRoutingStaticVnetRouteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e5767775ed89434d982f4990d4233b78350ea1468a9ac0a3f01747423c1936)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualHubConnectionRoutingStaticVnetRouteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487862e36a38dd7c6d164acef1e8f86064fa162b0b097b8e0c1b93548d6d0639)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b22caf645ff288e9e2a88457ce6a12d1d254c688779485a056682c442632ea15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21a7e14a0452d87589726de9e5cccef53fd0783fc080ec4efea255df8c29111a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualHubConnectionRoutingStaticVnetRoute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualHubConnectionRoutingStaticVnetRoute]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualHubConnectionRoutingStaticVnetRoute]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4395a028097f1ef5aa203e4315070b4ecfeeac7a0dcb00c3e61a9d8dfe5ea227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualHubConnectionRoutingStaticVnetRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionRoutingStaticVnetRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06d76847dc09c58729ea8d603c3cd1d7ca9a91f3c6cd384937c1b8279e24d470)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAddressPrefixes")
    def reset_address_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressPrefixes", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNextHopIpAddress")
    def reset_next_hop_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNextHopIpAddress", []))

    @builtins.property
    @jsii.member(jsii_name="addressPrefixesInput")
    def address_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nextHopIpAddressInput")
    def next_hop_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextHopIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="addressPrefixes")
    def address_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressPrefixes"))

    @address_prefixes.setter
    def address_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2898d14be4495ba7123ecda712aa41acd328f6164f6149fd12e49ff465bb35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7084ee5e9f771c8327278f97a04aacb20d7a84b92880cbf0fa9ef0ff85725e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nextHopIpAddress")
    def next_hop_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextHopIpAddress"))

    @next_hop_ip_address.setter
    def next_hop_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e547f615fb14dd08f26f66d15968258364318a0153b4969260eecf4c8e91240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextHopIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionRoutingStaticVnetRoute]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionRoutingStaticVnetRoute]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionRoutingStaticVnetRoute]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066587ab75c3e01b8eee05dae685b76d7d3bca9add2356e292d40c9824489336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VirtualHubConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#create VirtualHubConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#delete VirtualHubConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#read VirtualHubConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#update VirtualHubConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cc5613f0526137b56dd315732fac81c929a69a1a8be7309b75a0cced4dc72f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#create VirtualHubConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#delete VirtualHubConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#read VirtualHubConnection#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_hub_connection#update VirtualHubConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualHubConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualHubConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualHubConnection.VirtualHubConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71da2c1378791fa776aa52ccfb17c712a7a85eaaa32dbdd2cf665a8ca0d06da1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1765e70832cb8dcc47da82d56b330f63228046f55b4f615a9a538c1b9f7f7ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3e1fa1e50edc11e2f7d6485d270b8a62e424ad42ff30c79f03495792f6cd2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624a69a4b9b1d75a09bf5c532c69cf9849820b4b925a0f6b7da81a8fb9f2610b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92566edf544c0409cc8991cd96a0b53cfd3db36f93b7af99dc0c37a34282795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03af922bbe85b20adee60c57455f34041615599d6ddbd28acf84cebd33ca4e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VirtualHubConnection",
    "VirtualHubConnectionConfig",
    "VirtualHubConnectionRouting",
    "VirtualHubConnectionRoutingOutputReference",
    "VirtualHubConnectionRoutingPropagatedRouteTable",
    "VirtualHubConnectionRoutingPropagatedRouteTableOutputReference",
    "VirtualHubConnectionRoutingStaticVnetRoute",
    "VirtualHubConnectionRoutingStaticVnetRouteList",
    "VirtualHubConnectionRoutingStaticVnetRouteOutputReference",
    "VirtualHubConnectionTimeouts",
    "VirtualHubConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5807b7e6b8a2256711b7f5ef7b4f42c2648f5d5e6be37643756790c2af765e7a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    remote_virtual_network_id: builtins.str,
    virtual_hub_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing: typing.Optional[typing.Union[VirtualHubConnectionRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[VirtualHubConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__29822769f8ea80737aaa0cf39e996f8e0733fc86748b5b4cbcba0854f0b399e7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9f6194664ce697a8e148bb2851b0eb17694505c5fe64e552e8195a34fb8389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf313e85751a244eec73ecbc58f10913d3e32c8a0ba1433dc3d3660898b16229(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6686f2459d4551717e7a244c48f771884318ebf61e4bf21265ca33e812ed7b90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61fe410f8abf780647da0171a629c003f9806227dee89aac79579284ea9d539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d7056289c443c890dfe7bd4ec23acd25440971671d290abac0824f2b540ff0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0bf00b17e2cd44eb7f916e9f9cd6da746ffab632bbc8210da040523c63a9df(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    remote_virtual_network_id: builtins.str,
    virtual_hub_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing: typing.Optional[typing.Union[VirtualHubConnectionRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[VirtualHubConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ee447f1a5b5b620ee64896b84c6d123b6adbe2155cae1542868ab0694d311a(
    *,
    associated_route_table_id: typing.Optional[builtins.str] = None,
    inbound_route_map_id: typing.Optional[builtins.str] = None,
    outbound_route_map_id: typing.Optional[builtins.str] = None,
    propagated_route_table: typing.Optional[typing.Union[VirtualHubConnectionRoutingPropagatedRouteTable, typing.Dict[builtins.str, typing.Any]]] = None,
    static_vnet_local_route_override_criteria: typing.Optional[builtins.str] = None,
    static_vnet_propagate_static_routes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    static_vnet_route: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualHubConnectionRoutingStaticVnetRoute, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2866da895f6cbc585bc1a588f45edeef2df9b683304ec73d83fdd38c1f73dd62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969a3dd9c9b0abf81a36c15413ef4e1111bf2e5119db9bbe60b9ef5ffc55c063(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualHubConnectionRoutingStaticVnetRoute, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74e0d18e6a539e201066e6ab6c60df500e7554955ed86fe955e3d20f6baf75c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81732414cfc6e7ddb1a4a6f9609e486c85d1b5418635b6641fd04ea58da9d0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84e2c1ae6457c01319fac7840250a85d0629f92c04a5cad07f4fc4f5169b24d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f14c238c7e6fe080232bd4f62d6673674047a4eafc87f31a03a34424c2a563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddad5da941085e4d69e52841ff88d64a2d65feff7cb16ae9455819874edf35c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b2909c0d1d0eb2f0dd66a3547a26e54d736dbce8bdb030d1ac445432eb2d51(
    value: typing.Optional[VirtualHubConnectionRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15f729244bb4c0b51f4fa5013ba88e63abf1667f148cd78893395917ad0fb12(
    *,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab55686e477b145d3c4bcdde4a3ccf17d2d22dbb7dba69ad8f629f365db0fdcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f676ff5f1ccd105ac8a55911a710019daca65071b7e6669d7c860d087e22711f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b458707639d78bdb6c9422043d0ec905193cd4b2e0ca0bbd374f09f01a9cec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9d540553ebb0f61f3922a51131003eb70d3255848226c0c51c53d005173f5a(
    value: typing.Optional[VirtualHubConnectionRoutingPropagatedRouteTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ca4f4f2923c4db8b95042484b317d158448265e118758974d9b1ffac15968d(
    *,
    address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    next_hop_ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff85d30586ba83c913b21b9ce7010c1298e966d19a4a9d60fa845b01aae753c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e5767775ed89434d982f4990d4233b78350ea1468a9ac0a3f01747423c1936(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487862e36a38dd7c6d164acef1e8f86064fa162b0b097b8e0c1b93548d6d0639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22caf645ff288e9e2a88457ce6a12d1d254c688779485a056682c442632ea15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a7e14a0452d87589726de9e5cccef53fd0783fc080ec4efea255df8c29111a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4395a028097f1ef5aa203e4315070b4ecfeeac7a0dcb00c3e61a9d8dfe5ea227(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualHubConnectionRoutingStaticVnetRoute]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d76847dc09c58729ea8d603c3cd1d7ca9a91f3c6cd384937c1b8279e24d470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2898d14be4495ba7123ecda712aa41acd328f6164f6149fd12e49ff465bb35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7084ee5e9f771c8327278f97a04aacb20d7a84b92880cbf0fa9ef0ff85725e5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e547f615fb14dd08f26f66d15968258364318a0153b4969260eecf4c8e91240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066587ab75c3e01b8eee05dae685b76d7d3bca9add2356e292d40c9824489336(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionRoutingStaticVnetRoute]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cc5613f0526137b56dd315732fac81c929a69a1a8be7309b75a0cced4dc72f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71da2c1378791fa776aa52ccfb17c712a7a85eaaa32dbdd2cf665a8ca0d06da1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1765e70832cb8dcc47da82d56b330f63228046f55b4f615a9a538c1b9f7f7ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3e1fa1e50edc11e2f7d6485d270b8a62e424ad42ff30c79f03495792f6cd2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624a69a4b9b1d75a09bf5c532c69cf9849820b4b925a0f6b7da81a8fb9f2610b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92566edf544c0409cc8991cd96a0b53cfd3db36f93b7af99dc0c37a34282795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03af922bbe85b20adee60c57455f34041615599d6ddbd28acf84cebd33ca4e24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualHubConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
