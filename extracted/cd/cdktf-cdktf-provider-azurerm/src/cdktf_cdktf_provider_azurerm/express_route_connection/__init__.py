r'''
# `azurerm_express_route_connection`

Refer to the Terraform Registry for docs: [`azurerm_express_route_connection`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection).
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


class ExpressRouteConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection azurerm_express_route_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        express_route_circuit_peering_id: builtins.str,
        express_route_gateway_id: builtins.str,
        name: builtins.str,
        authorization_key: typing.Optional[builtins.str] = None,
        enable_internet_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        express_route_gateway_bypass_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        private_link_fast_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing: typing.Optional[typing.Union["ExpressRouteConnectionRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        routing_weight: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ExpressRouteConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection azurerm_express_route_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param express_route_circuit_peering_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_circuit_peering_id ExpressRouteConnection#express_route_circuit_peering_id}.
        :param express_route_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_gateway_id ExpressRouteConnection#express_route_gateway_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#name ExpressRouteConnection#name}.
        :param authorization_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#authorization_key ExpressRouteConnection#authorization_key}.
        :param enable_internet_security: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#enable_internet_security ExpressRouteConnection#enable_internet_security}.
        :param express_route_gateway_bypass_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_gateway_bypass_enabled ExpressRouteConnection#express_route_gateway_bypass_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#id ExpressRouteConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param private_link_fast_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#private_link_fast_path_enabled ExpressRouteConnection#private_link_fast_path_enabled}.
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#routing ExpressRouteConnection#routing}
        :param routing_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#routing_weight ExpressRouteConnection#routing_weight}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#timeouts ExpressRouteConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b366587a858957de23ffd31189cf885c5830c32acd7396e7d24f3aff25ecc64)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExpressRouteConnectionConfig(
            express_route_circuit_peering_id=express_route_circuit_peering_id,
            express_route_gateway_id=express_route_gateway_id,
            name=name,
            authorization_key=authorization_key,
            enable_internet_security=enable_internet_security,
            express_route_gateway_bypass_enabled=express_route_gateway_bypass_enabled,
            id=id,
            private_link_fast_path_enabled=private_link_fast_path_enabled,
            routing=routing,
            routing_weight=routing_weight,
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
        '''Generates CDKTF code for importing a ExpressRouteConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExpressRouteConnection to import.
        :param import_from_id: The id of the existing ExpressRouteConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExpressRouteConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1c5478c42ade3f3f215b774d94fdb5c1dba2678225cd138e57948dc10c2d98)
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
        propagated_route_table: typing.Optional[typing.Union["ExpressRouteConnectionRoutingPropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param associated_route_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#associated_route_table_id ExpressRouteConnection#associated_route_table_id}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#inbound_route_map_id ExpressRouteConnection#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#outbound_route_map_id ExpressRouteConnection#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#propagated_route_table ExpressRouteConnection#propagated_route_table}
        '''
        value = ExpressRouteConnectionRouting(
            associated_route_table_id=associated_route_table_id,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#create ExpressRouteConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#delete ExpressRouteConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#read ExpressRouteConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#update ExpressRouteConnection#update}.
        '''
        value = ExpressRouteConnectionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthorizationKey")
    def reset_authorization_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationKey", []))

    @jsii.member(jsii_name="resetEnableInternetSecurity")
    def reset_enable_internet_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInternetSecurity", []))

    @jsii.member(jsii_name="resetExpressRouteGatewayBypassEnabled")
    def reset_express_route_gateway_bypass_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpressRouteGatewayBypassEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrivateLinkFastPathEnabled")
    def reset_private_link_fast_path_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkFastPathEnabled", []))

    @jsii.member(jsii_name="resetRouting")
    def reset_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouting", []))

    @jsii.member(jsii_name="resetRoutingWeight")
    def reset_routing_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingWeight", []))

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
    def routing(self) -> "ExpressRouteConnectionRoutingOutputReference":
        return typing.cast("ExpressRouteConnectionRoutingOutputReference", jsii.get(self, "routing"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ExpressRouteConnectionTimeoutsOutputReference":
        return typing.cast("ExpressRouteConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authorizationKeyInput")
    def authorization_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInternetSecurityInput")
    def enable_internet_security_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInternetSecurityInput"))

    @builtins.property
    @jsii.member(jsii_name="expressRouteCircuitPeeringIdInput")
    def express_route_circuit_peering_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressRouteCircuitPeeringIdInput"))

    @builtins.property
    @jsii.member(jsii_name="expressRouteGatewayBypassEnabledInput")
    def express_route_gateway_bypass_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "expressRouteGatewayBypassEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="expressRouteGatewayIdInput")
    def express_route_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressRouteGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkFastPathEnabledInput")
    def private_link_fast_path_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateLinkFastPathEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="routingInput")
    def routing_input(self) -> typing.Optional["ExpressRouteConnectionRouting"]:
        return typing.cast(typing.Optional["ExpressRouteConnectionRouting"], jsii.get(self, "routingInput"))

    @builtins.property
    @jsii.member(jsii_name="routingWeightInput")
    def routing_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "routingWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ExpressRouteConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ExpressRouteConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationKey")
    def authorization_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationKey"))

    @authorization_key.setter
    def authorization_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9524c12fd121fd568cd08c497169d3d8fec1838259f76f7c2c9375d1d88b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableInternetSecurity")
    def enable_internet_security(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInternetSecurity"))

    @enable_internet_security.setter
    def enable_internet_security(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c745b6cb3a5849b9f72d6f7d804151d7cdcdb975abcad7e548c7cfc5ac5d5f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInternetSecurity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expressRouteCircuitPeeringId")
    def express_route_circuit_peering_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expressRouteCircuitPeeringId"))

    @express_route_circuit_peering_id.setter
    def express_route_circuit_peering_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9612e62502733154f139cc97f7474faa97352060b401865ac93dfdb7d9d0cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expressRouteCircuitPeeringId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expressRouteGatewayBypassEnabled")
    def express_route_gateway_bypass_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "expressRouteGatewayBypassEnabled"))

    @express_route_gateway_bypass_enabled.setter
    def express_route_gateway_bypass_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9173c94021fb3fa1ce60d0ae3767ecb1a0e764ecbde43a4496a54d8b8d96b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expressRouteGatewayBypassEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expressRouteGatewayId")
    def express_route_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expressRouteGatewayId"))

    @express_route_gateway_id.setter
    def express_route_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58525dafa7bdc813104cee33530f4c61d135151abe5602a4b6f06cf815e9a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expressRouteGatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b170409a3f99ebd58532264593d46459677f84fcf6930fbd11a2eb4e82ebb77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d3316fa5289e31778ccae9b3141cfb79e859768380a6054729958d72eb3fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateLinkFastPathEnabled")
    def private_link_fast_path_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateLinkFastPathEnabled"))

    @private_link_fast_path_enabled.setter
    def private_link_fast_path_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b233058771241538a7041ca9adb20914c5e4e5a24a67d81bf95d8d229509fec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkFastPathEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingWeight")
    def routing_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "routingWeight"))

    @routing_weight.setter
    def routing_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6057c62bc25eb890dea152df9ba59fb445a16c98660fa41f166c69639ae7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingWeight", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "express_route_circuit_peering_id": "expressRouteCircuitPeeringId",
        "express_route_gateway_id": "expressRouteGatewayId",
        "name": "name",
        "authorization_key": "authorizationKey",
        "enable_internet_security": "enableInternetSecurity",
        "express_route_gateway_bypass_enabled": "expressRouteGatewayBypassEnabled",
        "id": "id",
        "private_link_fast_path_enabled": "privateLinkFastPathEnabled",
        "routing": "routing",
        "routing_weight": "routingWeight",
        "timeouts": "timeouts",
    },
)
class ExpressRouteConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        express_route_circuit_peering_id: builtins.str,
        express_route_gateway_id: builtins.str,
        name: builtins.str,
        authorization_key: typing.Optional[builtins.str] = None,
        enable_internet_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        express_route_gateway_bypass_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        private_link_fast_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        routing: typing.Optional[typing.Union["ExpressRouteConnectionRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        routing_weight: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ExpressRouteConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param express_route_circuit_peering_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_circuit_peering_id ExpressRouteConnection#express_route_circuit_peering_id}.
        :param express_route_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_gateway_id ExpressRouteConnection#express_route_gateway_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#name ExpressRouteConnection#name}.
        :param authorization_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#authorization_key ExpressRouteConnection#authorization_key}.
        :param enable_internet_security: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#enable_internet_security ExpressRouteConnection#enable_internet_security}.
        :param express_route_gateway_bypass_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_gateway_bypass_enabled ExpressRouteConnection#express_route_gateway_bypass_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#id ExpressRouteConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param private_link_fast_path_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#private_link_fast_path_enabled ExpressRouteConnection#private_link_fast_path_enabled}.
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#routing ExpressRouteConnection#routing}
        :param routing_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#routing_weight ExpressRouteConnection#routing_weight}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#timeouts ExpressRouteConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing, dict):
            routing = ExpressRouteConnectionRouting(**routing)
        if isinstance(timeouts, dict):
            timeouts = ExpressRouteConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0565c3baaa120ad4de476b7f4e173e34675485fab2c673cacf9fa8cde08e36b3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument express_route_circuit_peering_id", value=express_route_circuit_peering_id, expected_type=type_hints["express_route_circuit_peering_id"])
            check_type(argname="argument express_route_gateway_id", value=express_route_gateway_id, expected_type=type_hints["express_route_gateway_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authorization_key", value=authorization_key, expected_type=type_hints["authorization_key"])
            check_type(argname="argument enable_internet_security", value=enable_internet_security, expected_type=type_hints["enable_internet_security"])
            check_type(argname="argument express_route_gateway_bypass_enabled", value=express_route_gateway_bypass_enabled, expected_type=type_hints["express_route_gateway_bypass_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument private_link_fast_path_enabled", value=private_link_fast_path_enabled, expected_type=type_hints["private_link_fast_path_enabled"])
            check_type(argname="argument routing", value=routing, expected_type=type_hints["routing"])
            check_type(argname="argument routing_weight", value=routing_weight, expected_type=type_hints["routing_weight"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "express_route_circuit_peering_id": express_route_circuit_peering_id,
            "express_route_gateway_id": express_route_gateway_id,
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
        if authorization_key is not None:
            self._values["authorization_key"] = authorization_key
        if enable_internet_security is not None:
            self._values["enable_internet_security"] = enable_internet_security
        if express_route_gateway_bypass_enabled is not None:
            self._values["express_route_gateway_bypass_enabled"] = express_route_gateway_bypass_enabled
        if id is not None:
            self._values["id"] = id
        if private_link_fast_path_enabled is not None:
            self._values["private_link_fast_path_enabled"] = private_link_fast_path_enabled
        if routing is not None:
            self._values["routing"] = routing
        if routing_weight is not None:
            self._values["routing_weight"] = routing_weight
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
    def express_route_circuit_peering_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_circuit_peering_id ExpressRouteConnection#express_route_circuit_peering_id}.'''
        result = self._values.get("express_route_circuit_peering_id")
        assert result is not None, "Required property 'express_route_circuit_peering_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def express_route_gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_gateway_id ExpressRouteConnection#express_route_gateway_id}.'''
        result = self._values.get("express_route_gateway_id")
        assert result is not None, "Required property 'express_route_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#name ExpressRouteConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#authorization_key ExpressRouteConnection#authorization_key}.'''
        result = self._values.get("authorization_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_internet_security(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#enable_internet_security ExpressRouteConnection#enable_internet_security}.'''
        result = self._values.get("enable_internet_security")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def express_route_gateway_bypass_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#express_route_gateway_bypass_enabled ExpressRouteConnection#express_route_gateway_bypass_enabled}.'''
        result = self._values.get("express_route_gateway_bypass_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#id ExpressRouteConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_fast_path_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#private_link_fast_path_enabled ExpressRouteConnection#private_link_fast_path_enabled}.'''
        result = self._values.get("private_link_fast_path_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def routing(self) -> typing.Optional["ExpressRouteConnectionRouting"]:
        '''routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#routing ExpressRouteConnection#routing}
        '''
        result = self._values.get("routing")
        return typing.cast(typing.Optional["ExpressRouteConnectionRouting"], result)

    @builtins.property
    def routing_weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#routing_weight ExpressRouteConnection#routing_weight}.'''
        result = self._values.get("routing_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ExpressRouteConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#timeouts ExpressRouteConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ExpressRouteConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnectionRouting",
    jsii_struct_bases=[],
    name_mapping={
        "associated_route_table_id": "associatedRouteTableId",
        "inbound_route_map_id": "inboundRouteMapId",
        "outbound_route_map_id": "outboundRouteMapId",
        "propagated_route_table": "propagatedRouteTable",
    },
)
class ExpressRouteConnectionRouting:
    def __init__(
        self,
        *,
        associated_route_table_id: typing.Optional[builtins.str] = None,
        inbound_route_map_id: typing.Optional[builtins.str] = None,
        outbound_route_map_id: typing.Optional[builtins.str] = None,
        propagated_route_table: typing.Optional[typing.Union["ExpressRouteConnectionRoutingPropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param associated_route_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#associated_route_table_id ExpressRouteConnection#associated_route_table_id}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#inbound_route_map_id ExpressRouteConnection#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#outbound_route_map_id ExpressRouteConnection#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#propagated_route_table ExpressRouteConnection#propagated_route_table}
        '''
        if isinstance(propagated_route_table, dict):
            propagated_route_table = ExpressRouteConnectionRoutingPropagatedRouteTable(**propagated_route_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54311290af45aba0df7904e8f2aa0899280060a579d4e0adf5676eb50f7b1e4)
            check_type(argname="argument associated_route_table_id", value=associated_route_table_id, expected_type=type_hints["associated_route_table_id"])
            check_type(argname="argument inbound_route_map_id", value=inbound_route_map_id, expected_type=type_hints["inbound_route_map_id"])
            check_type(argname="argument outbound_route_map_id", value=outbound_route_map_id, expected_type=type_hints["outbound_route_map_id"])
            check_type(argname="argument propagated_route_table", value=propagated_route_table, expected_type=type_hints["propagated_route_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associated_route_table_id is not None:
            self._values["associated_route_table_id"] = associated_route_table_id
        if inbound_route_map_id is not None:
            self._values["inbound_route_map_id"] = inbound_route_map_id
        if outbound_route_map_id is not None:
            self._values["outbound_route_map_id"] = outbound_route_map_id
        if propagated_route_table is not None:
            self._values["propagated_route_table"] = propagated_route_table

    @builtins.property
    def associated_route_table_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#associated_route_table_id ExpressRouteConnection#associated_route_table_id}.'''
        result = self._values.get("associated_route_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#inbound_route_map_id ExpressRouteConnection#inbound_route_map_id}.'''
        result = self._values.get("inbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#outbound_route_map_id ExpressRouteConnection#outbound_route_map_id}.'''
        result = self._values.get("outbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagated_route_table(
        self,
    ) -> typing.Optional["ExpressRouteConnectionRoutingPropagatedRouteTable"]:
        '''propagated_route_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#propagated_route_table ExpressRouteConnection#propagated_route_table}
        '''
        result = self._values.get("propagated_route_table")
        return typing.cast(typing.Optional["ExpressRouteConnectionRoutingPropagatedRouteTable"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteConnectionRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRouteConnectionRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnectionRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2f948252ea639ce431b068e34ddfe0395fe3e4bc1dd401f72f62e9bc2a22ce7)
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
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#labels ExpressRouteConnection#labels}.
        :param route_table_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#route_table_ids ExpressRouteConnection#route_table_ids}.
        '''
        value = ExpressRouteConnectionRoutingPropagatedRouteTable(
            labels=labels, route_table_ids=route_table_ids
        )

        return typing.cast(None, jsii.invoke(self, "putPropagatedRouteTable", [value]))

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

    @builtins.property
    @jsii.member(jsii_name="propagatedRouteTable")
    def propagated_route_table(
        self,
    ) -> "ExpressRouteConnectionRoutingPropagatedRouteTableOutputReference":
        return typing.cast("ExpressRouteConnectionRoutingPropagatedRouteTableOutputReference", jsii.get(self, "propagatedRouteTable"))

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
    ) -> typing.Optional["ExpressRouteConnectionRoutingPropagatedRouteTable"]:
        return typing.cast(typing.Optional["ExpressRouteConnectionRoutingPropagatedRouteTable"], jsii.get(self, "propagatedRouteTableInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedRouteTableId")
    def associated_route_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associatedRouteTableId"))

    @associated_route_table_id.setter
    def associated_route_table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e4eb173dbd4227e86b1d5880a0cfe31f9f9f4f07fb44c91c57b2b89ee7b7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedRouteTableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundRouteMapId")
    def inbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inboundRouteMapId"))

    @inbound_route_map_id.setter
    def inbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fc8d2c51e51e94bc8815678724e8e4b09c20769f2da46781847fc90f9e8d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outboundRouteMapId")
    def outbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundRouteMapId"))

    @outbound_route_map_id.setter
    def outbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9385f0fc75117b35c91bec8bf7c32aeb43f12eb64bb80818163a7d278344717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExpressRouteConnectionRouting]:
        return typing.cast(typing.Optional[ExpressRouteConnectionRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExpressRouteConnectionRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce28a0c5fc104624bd704d9dd0f0d01272bdf3587ab7d0a76762fff9a755406f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnectionRoutingPropagatedRouteTable",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "route_table_ids": "routeTableIds"},
)
class ExpressRouteConnectionRoutingPropagatedRouteTable:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#labels ExpressRouteConnection#labels}.
        :param route_table_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#route_table_ids ExpressRouteConnection#route_table_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e941f0c8e3072ffc3c9fe04ef0cfc3a5113106bb800171011e5ee2c8450ff86)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument route_table_ids", value=route_table_ids, expected_type=type_hints["route_table_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if route_table_ids is not None:
            self._values["route_table_ids"] = route_table_ids

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#labels ExpressRouteConnection#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def route_table_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#route_table_ids ExpressRouteConnection#route_table_ids}.'''
        result = self._values.get("route_table_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteConnectionRoutingPropagatedRouteTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRouteConnectionRoutingPropagatedRouteTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnectionRoutingPropagatedRouteTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77302c4f5d904a1858aa5adf7f10a29ab0e4929882db31f98259e9e5fc96f361)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03985b26b2add50cd1dbc091d98702b3a78229766d8b070aa289d74d4e0cf4fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTableIds")
    def route_table_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "routeTableIds"))

    @route_table_ids.setter
    def route_table_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f930be87daa98287a62965479e2d347caa8d35918493e8af1fb8f65e7821d5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTableIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ExpressRouteConnectionRoutingPropagatedRouteTable]:
        return typing.cast(typing.Optional[ExpressRouteConnectionRoutingPropagatedRouteTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExpressRouteConnectionRoutingPropagatedRouteTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66eaeff60661c6327352da0edf4dee6d08f515b1d14aa2af4f5520dc0b984c35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ExpressRouteConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#create ExpressRouteConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#delete ExpressRouteConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#read ExpressRouteConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#update ExpressRouteConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d684327119a255c395d5ed13fe68382cfed9211b2149f19579196d88519a434)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#create ExpressRouteConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#delete ExpressRouteConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#read ExpressRouteConnection#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_connection#update ExpressRouteConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRouteConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteConnection.ExpressRouteConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf0893b0c5fd6b8bbf65627ef50de12760bb40c14a047dfe4c7cb401d2551e03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e737ba12f61e685bbcacb6404f9c083e463eb8100de912ceca910e2231b4324b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79aed0f3098db0ab9ca6d2fdf0b9212daa7eece52d07aa9be60a292f97a74b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862bef85b2dcadbc9a9f63be865e51f580a7809b30bfebc6563c031630e8e391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e705a304eaf0d1293f38cd34f667ffae51f96dd272b52526d2c8899c4afce08a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f37f59681b6be81a91b2452dc8fa1ad6a4c9a85c40740008c41d346253842d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ExpressRouteConnection",
    "ExpressRouteConnectionConfig",
    "ExpressRouteConnectionRouting",
    "ExpressRouteConnectionRoutingOutputReference",
    "ExpressRouteConnectionRoutingPropagatedRouteTable",
    "ExpressRouteConnectionRoutingPropagatedRouteTableOutputReference",
    "ExpressRouteConnectionTimeouts",
    "ExpressRouteConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3b366587a858957de23ffd31189cf885c5830c32acd7396e7d24f3aff25ecc64(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    express_route_circuit_peering_id: builtins.str,
    express_route_gateway_id: builtins.str,
    name: builtins.str,
    authorization_key: typing.Optional[builtins.str] = None,
    enable_internet_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    express_route_gateway_bypass_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    private_link_fast_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing: typing.Optional[typing.Union[ExpressRouteConnectionRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    routing_weight: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ExpressRouteConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aa1c5478c42ade3f3f215b774d94fdb5c1dba2678225cd138e57948dc10c2d98(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9524c12fd121fd568cd08c497169d3d8fec1838259f76f7c2c9375d1d88b48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c745b6cb3a5849b9f72d6f7d804151d7cdcdb975abcad7e548c7cfc5ac5d5f33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9612e62502733154f139cc97f7474faa97352060b401865ac93dfdb7d9d0cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9173c94021fb3fa1ce60d0ae3767ecb1a0e764ecbde43a4496a54d8b8d96b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58525dafa7bdc813104cee33530f4c61d135151abe5602a4b6f06cf815e9a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b170409a3f99ebd58532264593d46459677f84fcf6930fbd11a2eb4e82ebb77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d3316fa5289e31778ccae9b3141cfb79e859768380a6054729958d72eb3fa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b233058771241538a7041ca9adb20914c5e4e5a24a67d81bf95d8d229509fec3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6057c62bc25eb890dea152df9ba59fb445a16c98660fa41f166c69639ae7ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0565c3baaa120ad4de476b7f4e173e34675485fab2c673cacf9fa8cde08e36b3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    express_route_circuit_peering_id: builtins.str,
    express_route_gateway_id: builtins.str,
    name: builtins.str,
    authorization_key: typing.Optional[builtins.str] = None,
    enable_internet_security: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    express_route_gateway_bypass_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    private_link_fast_path_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    routing: typing.Optional[typing.Union[ExpressRouteConnectionRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    routing_weight: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ExpressRouteConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54311290af45aba0df7904e8f2aa0899280060a579d4e0adf5676eb50f7b1e4(
    *,
    associated_route_table_id: typing.Optional[builtins.str] = None,
    inbound_route_map_id: typing.Optional[builtins.str] = None,
    outbound_route_map_id: typing.Optional[builtins.str] = None,
    propagated_route_table: typing.Optional[typing.Union[ExpressRouteConnectionRoutingPropagatedRouteTable, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f948252ea639ce431b068e34ddfe0395fe3e4bc1dd401f72f62e9bc2a22ce7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e4eb173dbd4227e86b1d5880a0cfe31f9f9f4f07fb44c91c57b2b89ee7b7e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fc8d2c51e51e94bc8815678724e8e4b09c20769f2da46781847fc90f9e8d3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9385f0fc75117b35c91bec8bf7c32aeb43f12eb64bb80818163a7d278344717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce28a0c5fc104624bd704d9dd0f0d01272bdf3587ab7d0a76762fff9a755406f(
    value: typing.Optional[ExpressRouteConnectionRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e941f0c8e3072ffc3c9fe04ef0cfc3a5113106bb800171011e5ee2c8450ff86(
    *,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77302c4f5d904a1858aa5adf7f10a29ab0e4929882db31f98259e9e5fc96f361(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03985b26b2add50cd1dbc091d98702b3a78229766d8b070aa289d74d4e0cf4fc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f930be87daa98287a62965479e2d347caa8d35918493e8af1fb8f65e7821d5a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66eaeff60661c6327352da0edf4dee6d08f515b1d14aa2af4f5520dc0b984c35(
    value: typing.Optional[ExpressRouteConnectionRoutingPropagatedRouteTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d684327119a255c395d5ed13fe68382cfed9211b2149f19579196d88519a434(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0893b0c5fd6b8bbf65627ef50de12760bb40c14a047dfe4c7cb401d2551e03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e737ba12f61e685bbcacb6404f9c083e463eb8100de912ceca910e2231b4324b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79aed0f3098db0ab9ca6d2fdf0b9212daa7eece52d07aa9be60a292f97a74b0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862bef85b2dcadbc9a9f63be865e51f580a7809b30bfebc6563c031630e8e391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e705a304eaf0d1293f38cd34f667ffae51f96dd272b52526d2c8899c4afce08a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f37f59681b6be81a91b2452dc8fa1ad6a4c9a85c40740008c41d346253842d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
