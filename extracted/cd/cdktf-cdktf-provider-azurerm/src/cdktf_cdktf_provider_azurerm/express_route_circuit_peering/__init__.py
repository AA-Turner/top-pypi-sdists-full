r'''
# `azurerm_express_route_circuit_peering`

Refer to the Terraform Registry for docs: [`azurerm_express_route_circuit_peering`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering).
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


class ExpressRouteCircuitPeering(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeering",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering azurerm_express_route_circuit_peering}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        express_route_circuit_name: builtins.str,
        peering_type: builtins.str,
        resource_group_name: builtins.str,
        vlan_id: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv6: typing.Optional[typing.Union["ExpressRouteCircuitPeeringIpv6", typing.Dict[builtins.str, typing.Any]]] = None,
        microsoft_peering_config: typing.Optional[typing.Union["ExpressRouteCircuitPeeringMicrosoftPeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_asn: typing.Optional[jsii.Number] = None,
        primary_peer_address_prefix: typing.Optional[builtins.str] = None,
        route_filter_id: typing.Optional[builtins.str] = None,
        secondary_peer_address_prefix: typing.Optional[builtins.str] = None,
        shared_key: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ExpressRouteCircuitPeeringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering azurerm_express_route_circuit_peering} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param express_route_circuit_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#express_route_circuit_name ExpressRouteCircuitPeering#express_route_circuit_name}.
        :param peering_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#peering_type ExpressRouteCircuitPeering#peering_type}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#resource_group_name ExpressRouteCircuitPeering#resource_group_name}.
        :param vlan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#vlan_id ExpressRouteCircuitPeering#vlan_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#id ExpressRouteCircuitPeering#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ipv4_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#ipv4_enabled ExpressRouteCircuitPeering#ipv4_enabled}.
        :param ipv6: ipv6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#ipv6 ExpressRouteCircuitPeering#ipv6}
        :param microsoft_peering_config: microsoft_peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#microsoft_peering_config ExpressRouteCircuitPeering#microsoft_peering_config}
        :param peer_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#peer_asn ExpressRouteCircuitPeering#peer_asn}.
        :param primary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#primary_peer_address_prefix ExpressRouteCircuitPeering#primary_peer_address_prefix}.
        :param route_filter_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#route_filter_id ExpressRouteCircuitPeering#route_filter_id}.
        :param secondary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#secondary_peer_address_prefix ExpressRouteCircuitPeering#secondary_peer_address_prefix}.
        :param shared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#shared_key ExpressRouteCircuitPeering#shared_key}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#timeouts ExpressRouteCircuitPeering#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f122288abfe9d0f2b076a3e6d1b0cb2f6b479be1fc485610a506eb21c33c4aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExpressRouteCircuitPeeringConfig(
            express_route_circuit_name=express_route_circuit_name,
            peering_type=peering_type,
            resource_group_name=resource_group_name,
            vlan_id=vlan_id,
            id=id,
            ipv4_enabled=ipv4_enabled,
            ipv6=ipv6,
            microsoft_peering_config=microsoft_peering_config,
            peer_asn=peer_asn,
            primary_peer_address_prefix=primary_peer_address_prefix,
            route_filter_id=route_filter_id,
            secondary_peer_address_prefix=secondary_peer_address_prefix,
            shared_key=shared_key,
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
        '''Generates CDKTF code for importing a ExpressRouteCircuitPeering resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExpressRouteCircuitPeering to import.
        :param import_from_id: The id of the existing ExpressRouteCircuitPeering that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExpressRouteCircuitPeering to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca66a8136154e3e9318831ae724355d4f1cdc92d88c7dac70a3f67c4fcf4dac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIpv6")
    def put_ipv6(
        self,
        *,
        primary_peer_address_prefix: builtins.str,
        secondary_peer_address_prefix: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        microsoft_peering: typing.Optional[typing.Union["ExpressRouteCircuitPeeringIpv6MicrosoftPeering", typing.Dict[builtins.str, typing.Any]]] = None,
        route_filter_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param primary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#primary_peer_address_prefix ExpressRouteCircuitPeering#primary_peer_address_prefix}.
        :param secondary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#secondary_peer_address_prefix ExpressRouteCircuitPeering#secondary_peer_address_prefix}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#enabled ExpressRouteCircuitPeering#enabled}.
        :param microsoft_peering: microsoft_peering block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#microsoft_peering ExpressRouteCircuitPeering#microsoft_peering}
        :param route_filter_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#route_filter_id ExpressRouteCircuitPeering#route_filter_id}.
        '''
        value = ExpressRouteCircuitPeeringIpv6(
            primary_peer_address_prefix=primary_peer_address_prefix,
            secondary_peer_address_prefix=secondary_peer_address_prefix,
            enabled=enabled,
            microsoft_peering=microsoft_peering,
            route_filter_id=route_filter_id,
        )

        return typing.cast(None, jsii.invoke(self, "putIpv6", [value]))

    @jsii.member(jsii_name="putMicrosoftPeeringConfig")
    def put_microsoft_peering_config(
        self,
        *,
        advertised_public_prefixes: typing.Sequence[builtins.str],
        advertised_communities: typing.Optional[typing.Sequence[builtins.str]] = None,
        customer_asn: typing.Optional[jsii.Number] = None,
        routing_registry_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param advertised_public_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_public_prefixes ExpressRouteCircuitPeering#advertised_public_prefixes}.
        :param advertised_communities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_communities ExpressRouteCircuitPeering#advertised_communities}.
        :param customer_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#customer_asn ExpressRouteCircuitPeering#customer_asn}.
        :param routing_registry_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#routing_registry_name ExpressRouteCircuitPeering#routing_registry_name}.
        '''
        value = ExpressRouteCircuitPeeringMicrosoftPeeringConfig(
            advertised_public_prefixes=advertised_public_prefixes,
            advertised_communities=advertised_communities,
            customer_asn=customer_asn,
            routing_registry_name=routing_registry_name,
        )

        return typing.cast(None, jsii.invoke(self, "putMicrosoftPeeringConfig", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#create ExpressRouteCircuitPeering#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#delete ExpressRouteCircuitPeering#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#read ExpressRouteCircuitPeering#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#update ExpressRouteCircuitPeering#update}.
        '''
        value = ExpressRouteCircuitPeeringTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpv4Enabled")
    def reset_ipv4_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Enabled", []))

    @jsii.member(jsii_name="resetIpv6")
    def reset_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6", []))

    @jsii.member(jsii_name="resetMicrosoftPeeringConfig")
    def reset_microsoft_peering_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftPeeringConfig", []))

    @jsii.member(jsii_name="resetPeerAsn")
    def reset_peer_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerAsn", []))

    @jsii.member(jsii_name="resetPrimaryPeerAddressPrefix")
    def reset_primary_peer_address_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryPeerAddressPrefix", []))

    @jsii.member(jsii_name="resetRouteFilterId")
    def reset_route_filter_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteFilterId", []))

    @jsii.member(jsii_name="resetSecondaryPeerAddressPrefix")
    def reset_secondary_peer_address_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryPeerAddressPrefix", []))

    @jsii.member(jsii_name="resetSharedKey")
    def reset_shared_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedKey", []))

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
    @jsii.member(jsii_name="azureAsn")
    def azure_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "azureAsn"))

    @builtins.property
    @jsii.member(jsii_name="gatewayManagerEtag")
    def gateway_manager_etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayManagerEtag"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> "ExpressRouteCircuitPeeringIpv6OutputReference":
        return typing.cast("ExpressRouteCircuitPeeringIpv6OutputReference", jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="microsoftPeeringConfig")
    def microsoft_peering_config(
        self,
    ) -> "ExpressRouteCircuitPeeringMicrosoftPeeringConfigOutputReference":
        return typing.cast("ExpressRouteCircuitPeeringMicrosoftPeeringConfigOutputReference", jsii.get(self, "microsoftPeeringConfig"))

    @builtins.property
    @jsii.member(jsii_name="primaryAzurePort")
    def primary_azure_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryAzurePort"))

    @builtins.property
    @jsii.member(jsii_name="secondaryAzurePort")
    def secondary_azure_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryAzurePort"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ExpressRouteCircuitPeeringTimeoutsOutputReference":
        return typing.cast("ExpressRouteCircuitPeeringTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="expressRouteCircuitNameInput")
    def express_route_circuit_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressRouteCircuitNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4EnabledInput")
    def ipv4_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv4EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(self) -> typing.Optional["ExpressRouteCircuitPeeringIpv6"]:
        return typing.cast(typing.Optional["ExpressRouteCircuitPeeringIpv6"], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="microsoftPeeringConfigInput")
    def microsoft_peering_config_input(
        self,
    ) -> typing.Optional["ExpressRouteCircuitPeeringMicrosoftPeeringConfig"]:
        return typing.cast(typing.Optional["ExpressRouteCircuitPeeringMicrosoftPeeringConfig"], jsii.get(self, "microsoftPeeringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="peerAsnInput")
    def peer_asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "peerAsnInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringTypeInput")
    def peering_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeringTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryPeerAddressPrefixInput")
    def primary_peer_address_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryPeerAddressPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routeFilterIdInput")
    def route_filter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeFilterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryPeerAddressPrefixInput")
    def secondary_peer_address_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryPeerAddressPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedKeyInput")
    def shared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ExpressRouteCircuitPeeringTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ExpressRouteCircuitPeeringTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanIdInput")
    def vlan_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vlanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="expressRouteCircuitName")
    def express_route_circuit_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expressRouteCircuitName"))

    @express_route_circuit_name.setter
    def express_route_circuit_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ba0c6b77079f54a98fd4f7a0232eb66017e129b7fe0fa28e0978999296e76b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expressRouteCircuitName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60056476ff5d244b0cc3844bd42dd1d1fd8093a1992db5f01224a33b8fda4619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Enabled")
    def ipv4_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv4Enabled"))

    @ipv4_enabled.setter
    def ipv4_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d33265bdb04933a6475eea050849e90e02688eee1b3bee67a64ae8991d042b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerAsn")
    def peer_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "peerAsn"))

    @peer_asn.setter
    def peer_asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d5683c02abb18d4f3cff260f49cf562bc8e939eafba0bf1c6482d099edc774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerAsn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeringType")
    def peering_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeringType"))

    @peering_type.setter
    def peering_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0063c73d35fe5150bd63af66a4f521ef604dc929d7768e6407515460949492d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeringType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryPeerAddressPrefix")
    def primary_peer_address_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryPeerAddressPrefix"))

    @primary_peer_address_prefix.setter
    def primary_peer_address_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbbe93a9c0a255f8e0d3b5e40830513e7590612ecccb976173ef4f69da4bd2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryPeerAddressPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05aa39ad270d9d8c404ed0a492320467046ddf58293c277f2de9b55076efb063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeFilterId")
    def route_filter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeFilterId"))

    @route_filter_id.setter
    def route_filter_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50797301671c0713b7fae70c103d654068521028e8089161f1e452074aa1e3a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeFilterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryPeerAddressPrefix")
    def secondary_peer_address_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryPeerAddressPrefix"))

    @secondary_peer_address_prefix.setter
    def secondary_peer_address_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a9ee86bdff069abbcbe2645284397d49249fd2723367b83ef15cfd9451beae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryPeerAddressPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedKey")
    def shared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedKey"))

    @shared_key.setter
    def shared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1278d483c69302dc2d1e9d2d4be01010f5041c66aabd58a4b6948735d7ecba52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vlanId")
    def vlan_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlanId"))

    @vlan_id.setter
    def vlan_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6c9468a0fe5f4af2a399a74558853ff46e579b5790a2045b69bda303fa3dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlanId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "express_route_circuit_name": "expressRouteCircuitName",
        "peering_type": "peeringType",
        "resource_group_name": "resourceGroupName",
        "vlan_id": "vlanId",
        "id": "id",
        "ipv4_enabled": "ipv4Enabled",
        "ipv6": "ipv6",
        "microsoft_peering_config": "microsoftPeeringConfig",
        "peer_asn": "peerAsn",
        "primary_peer_address_prefix": "primaryPeerAddressPrefix",
        "route_filter_id": "routeFilterId",
        "secondary_peer_address_prefix": "secondaryPeerAddressPrefix",
        "shared_key": "sharedKey",
        "timeouts": "timeouts",
    },
)
class ExpressRouteCircuitPeeringConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        express_route_circuit_name: builtins.str,
        peering_type: builtins.str,
        resource_group_name: builtins.str,
        vlan_id: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv6: typing.Optional[typing.Union["ExpressRouteCircuitPeeringIpv6", typing.Dict[builtins.str, typing.Any]]] = None,
        microsoft_peering_config: typing.Optional[typing.Union["ExpressRouteCircuitPeeringMicrosoftPeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_asn: typing.Optional[jsii.Number] = None,
        primary_peer_address_prefix: typing.Optional[builtins.str] = None,
        route_filter_id: typing.Optional[builtins.str] = None,
        secondary_peer_address_prefix: typing.Optional[builtins.str] = None,
        shared_key: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ExpressRouteCircuitPeeringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param express_route_circuit_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#express_route_circuit_name ExpressRouteCircuitPeering#express_route_circuit_name}.
        :param peering_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#peering_type ExpressRouteCircuitPeering#peering_type}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#resource_group_name ExpressRouteCircuitPeering#resource_group_name}.
        :param vlan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#vlan_id ExpressRouteCircuitPeering#vlan_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#id ExpressRouteCircuitPeering#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ipv4_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#ipv4_enabled ExpressRouteCircuitPeering#ipv4_enabled}.
        :param ipv6: ipv6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#ipv6 ExpressRouteCircuitPeering#ipv6}
        :param microsoft_peering_config: microsoft_peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#microsoft_peering_config ExpressRouteCircuitPeering#microsoft_peering_config}
        :param peer_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#peer_asn ExpressRouteCircuitPeering#peer_asn}.
        :param primary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#primary_peer_address_prefix ExpressRouteCircuitPeering#primary_peer_address_prefix}.
        :param route_filter_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#route_filter_id ExpressRouteCircuitPeering#route_filter_id}.
        :param secondary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#secondary_peer_address_prefix ExpressRouteCircuitPeering#secondary_peer_address_prefix}.
        :param shared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#shared_key ExpressRouteCircuitPeering#shared_key}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#timeouts ExpressRouteCircuitPeering#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ipv6, dict):
            ipv6 = ExpressRouteCircuitPeeringIpv6(**ipv6)
        if isinstance(microsoft_peering_config, dict):
            microsoft_peering_config = ExpressRouteCircuitPeeringMicrosoftPeeringConfig(**microsoft_peering_config)
        if isinstance(timeouts, dict):
            timeouts = ExpressRouteCircuitPeeringTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5136550e07f51700ad7d027cc606afd95d175715ca8db78caa7bccbf2189b7f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument express_route_circuit_name", value=express_route_circuit_name, expected_type=type_hints["express_route_circuit_name"])
            check_type(argname="argument peering_type", value=peering_type, expected_type=type_hints["peering_type"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument vlan_id", value=vlan_id, expected_type=type_hints["vlan_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ipv4_enabled", value=ipv4_enabled, expected_type=type_hints["ipv4_enabled"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument microsoft_peering_config", value=microsoft_peering_config, expected_type=type_hints["microsoft_peering_config"])
            check_type(argname="argument peer_asn", value=peer_asn, expected_type=type_hints["peer_asn"])
            check_type(argname="argument primary_peer_address_prefix", value=primary_peer_address_prefix, expected_type=type_hints["primary_peer_address_prefix"])
            check_type(argname="argument route_filter_id", value=route_filter_id, expected_type=type_hints["route_filter_id"])
            check_type(argname="argument secondary_peer_address_prefix", value=secondary_peer_address_prefix, expected_type=type_hints["secondary_peer_address_prefix"])
            check_type(argname="argument shared_key", value=shared_key, expected_type=type_hints["shared_key"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "express_route_circuit_name": express_route_circuit_name,
            "peering_type": peering_type,
            "resource_group_name": resource_group_name,
            "vlan_id": vlan_id,
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
        if ipv4_enabled is not None:
            self._values["ipv4_enabled"] = ipv4_enabled
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if microsoft_peering_config is not None:
            self._values["microsoft_peering_config"] = microsoft_peering_config
        if peer_asn is not None:
            self._values["peer_asn"] = peer_asn
        if primary_peer_address_prefix is not None:
            self._values["primary_peer_address_prefix"] = primary_peer_address_prefix
        if route_filter_id is not None:
            self._values["route_filter_id"] = route_filter_id
        if secondary_peer_address_prefix is not None:
            self._values["secondary_peer_address_prefix"] = secondary_peer_address_prefix
        if shared_key is not None:
            self._values["shared_key"] = shared_key
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
    def express_route_circuit_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#express_route_circuit_name ExpressRouteCircuitPeering#express_route_circuit_name}.'''
        result = self._values.get("express_route_circuit_name")
        assert result is not None, "Required property 'express_route_circuit_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peering_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#peering_type ExpressRouteCircuitPeering#peering_type}.'''
        result = self._values.get("peering_type")
        assert result is not None, "Required property 'peering_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#resource_group_name ExpressRouteCircuitPeering#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vlan_id(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#vlan_id ExpressRouteCircuitPeering#vlan_id}.'''
        result = self._values.get("vlan_id")
        assert result is not None, "Required property 'vlan_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#id ExpressRouteCircuitPeering#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#ipv4_enabled ExpressRouteCircuitPeering#ipv4_enabled}.'''
        result = self._values.get("ipv4_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv6(self) -> typing.Optional["ExpressRouteCircuitPeeringIpv6"]:
        '''ipv6 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#ipv6 ExpressRouteCircuitPeering#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional["ExpressRouteCircuitPeeringIpv6"], result)

    @builtins.property
    def microsoft_peering_config(
        self,
    ) -> typing.Optional["ExpressRouteCircuitPeeringMicrosoftPeeringConfig"]:
        '''microsoft_peering_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#microsoft_peering_config ExpressRouteCircuitPeering#microsoft_peering_config}
        '''
        result = self._values.get("microsoft_peering_config")
        return typing.cast(typing.Optional["ExpressRouteCircuitPeeringMicrosoftPeeringConfig"], result)

    @builtins.property
    def peer_asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#peer_asn ExpressRouteCircuitPeering#peer_asn}.'''
        result = self._values.get("peer_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_peer_address_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#primary_peer_address_prefix ExpressRouteCircuitPeering#primary_peer_address_prefix}.'''
        result = self._values.get("primary_peer_address_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_filter_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#route_filter_id ExpressRouteCircuitPeering#route_filter_id}.'''
        result = self._values.get("route_filter_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_peer_address_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#secondary_peer_address_prefix ExpressRouteCircuitPeering#secondary_peer_address_prefix}.'''
        result = self._values.get("secondary_peer_address_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#shared_key ExpressRouteCircuitPeering#shared_key}.'''
        result = self._values.get("shared_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ExpressRouteCircuitPeeringTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#timeouts ExpressRouteCircuitPeering#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ExpressRouteCircuitPeeringTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteCircuitPeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringIpv6",
    jsii_struct_bases=[],
    name_mapping={
        "primary_peer_address_prefix": "primaryPeerAddressPrefix",
        "secondary_peer_address_prefix": "secondaryPeerAddressPrefix",
        "enabled": "enabled",
        "microsoft_peering": "microsoftPeering",
        "route_filter_id": "routeFilterId",
    },
)
class ExpressRouteCircuitPeeringIpv6:
    def __init__(
        self,
        *,
        primary_peer_address_prefix: builtins.str,
        secondary_peer_address_prefix: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        microsoft_peering: typing.Optional[typing.Union["ExpressRouteCircuitPeeringIpv6MicrosoftPeering", typing.Dict[builtins.str, typing.Any]]] = None,
        route_filter_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param primary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#primary_peer_address_prefix ExpressRouteCircuitPeering#primary_peer_address_prefix}.
        :param secondary_peer_address_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#secondary_peer_address_prefix ExpressRouteCircuitPeering#secondary_peer_address_prefix}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#enabled ExpressRouteCircuitPeering#enabled}.
        :param microsoft_peering: microsoft_peering block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#microsoft_peering ExpressRouteCircuitPeering#microsoft_peering}
        :param route_filter_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#route_filter_id ExpressRouteCircuitPeering#route_filter_id}.
        '''
        if isinstance(microsoft_peering, dict):
            microsoft_peering = ExpressRouteCircuitPeeringIpv6MicrosoftPeering(**microsoft_peering)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d0b40ea4a2874c7ee074106c5da3bd7d35cc44738a8e8f3ea396f3daed3bf8)
            check_type(argname="argument primary_peer_address_prefix", value=primary_peer_address_prefix, expected_type=type_hints["primary_peer_address_prefix"])
            check_type(argname="argument secondary_peer_address_prefix", value=secondary_peer_address_prefix, expected_type=type_hints["secondary_peer_address_prefix"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument microsoft_peering", value=microsoft_peering, expected_type=type_hints["microsoft_peering"])
            check_type(argname="argument route_filter_id", value=route_filter_id, expected_type=type_hints["route_filter_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_peer_address_prefix": primary_peer_address_prefix,
            "secondary_peer_address_prefix": secondary_peer_address_prefix,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if microsoft_peering is not None:
            self._values["microsoft_peering"] = microsoft_peering
        if route_filter_id is not None:
            self._values["route_filter_id"] = route_filter_id

    @builtins.property
    def primary_peer_address_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#primary_peer_address_prefix ExpressRouteCircuitPeering#primary_peer_address_prefix}.'''
        result = self._values.get("primary_peer_address_prefix")
        assert result is not None, "Required property 'primary_peer_address_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secondary_peer_address_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#secondary_peer_address_prefix ExpressRouteCircuitPeering#secondary_peer_address_prefix}.'''
        result = self._values.get("secondary_peer_address_prefix")
        assert result is not None, "Required property 'secondary_peer_address_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#enabled ExpressRouteCircuitPeering#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def microsoft_peering(
        self,
    ) -> typing.Optional["ExpressRouteCircuitPeeringIpv6MicrosoftPeering"]:
        '''microsoft_peering block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#microsoft_peering ExpressRouteCircuitPeering#microsoft_peering}
        '''
        result = self._values.get("microsoft_peering")
        return typing.cast(typing.Optional["ExpressRouteCircuitPeeringIpv6MicrosoftPeering"], result)

    @builtins.property
    def route_filter_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#route_filter_id ExpressRouteCircuitPeering#route_filter_id}.'''
        result = self._values.get("route_filter_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteCircuitPeeringIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringIpv6MicrosoftPeering",
    jsii_struct_bases=[],
    name_mapping={
        "advertised_communities": "advertisedCommunities",
        "advertised_public_prefixes": "advertisedPublicPrefixes",
        "customer_asn": "customerAsn",
        "routing_registry_name": "routingRegistryName",
    },
)
class ExpressRouteCircuitPeeringIpv6MicrosoftPeering:
    def __init__(
        self,
        *,
        advertised_communities: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_public_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        customer_asn: typing.Optional[jsii.Number] = None,
        routing_registry_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param advertised_communities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_communities ExpressRouteCircuitPeering#advertised_communities}.
        :param advertised_public_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_public_prefixes ExpressRouteCircuitPeering#advertised_public_prefixes}.
        :param customer_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#customer_asn ExpressRouteCircuitPeering#customer_asn}.
        :param routing_registry_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#routing_registry_name ExpressRouteCircuitPeering#routing_registry_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d3941113d6bb8e7e0a81d59a2c6b40d492be878e6afbae70d27d93e56cacf3f)
            check_type(argname="argument advertised_communities", value=advertised_communities, expected_type=type_hints["advertised_communities"])
            check_type(argname="argument advertised_public_prefixes", value=advertised_public_prefixes, expected_type=type_hints["advertised_public_prefixes"])
            check_type(argname="argument customer_asn", value=customer_asn, expected_type=type_hints["customer_asn"])
            check_type(argname="argument routing_registry_name", value=routing_registry_name, expected_type=type_hints["routing_registry_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advertised_communities is not None:
            self._values["advertised_communities"] = advertised_communities
        if advertised_public_prefixes is not None:
            self._values["advertised_public_prefixes"] = advertised_public_prefixes
        if customer_asn is not None:
            self._values["customer_asn"] = customer_asn
        if routing_registry_name is not None:
            self._values["routing_registry_name"] = routing_registry_name

    @builtins.property
    def advertised_communities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_communities ExpressRouteCircuitPeering#advertised_communities}.'''
        result = self._values.get("advertised_communities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def advertised_public_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_public_prefixes ExpressRouteCircuitPeering#advertised_public_prefixes}.'''
        result = self._values.get("advertised_public_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def customer_asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#customer_asn ExpressRouteCircuitPeering#customer_asn}.'''
        result = self._values.get("customer_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def routing_registry_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#routing_registry_name ExpressRouteCircuitPeering#routing_registry_name}.'''
        result = self._values.get("routing_registry_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteCircuitPeeringIpv6MicrosoftPeering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRouteCircuitPeeringIpv6MicrosoftPeeringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringIpv6MicrosoftPeeringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f79f6f7a09a61fb59a37f10eefbe9b11925fc967f5b07e8f0c89e92a4d0539c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdvertisedCommunities")
    def reset_advertised_communities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedCommunities", []))

    @jsii.member(jsii_name="resetAdvertisedPublicPrefixes")
    def reset_advertised_public_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedPublicPrefixes", []))

    @jsii.member(jsii_name="resetCustomerAsn")
    def reset_customer_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerAsn", []))

    @jsii.member(jsii_name="resetRoutingRegistryName")
    def reset_routing_registry_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingRegistryName", []))

    @builtins.property
    @jsii.member(jsii_name="advertisedCommunitiesInput")
    def advertised_communities_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advertisedCommunitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedPublicPrefixesInput")
    def advertised_public_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advertisedPublicPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="customerAsnInput")
    def customer_asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customerAsnInput"))

    @builtins.property
    @jsii.member(jsii_name="routingRegistryNameInput")
    def routing_registry_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingRegistryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedCommunities")
    def advertised_communities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advertisedCommunities"))

    @advertised_communities.setter
    def advertised_communities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d395f26b7b618b11301a6afd961711f80b9d8bfea76deb54cc498d64f1e7b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedCommunities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advertisedPublicPrefixes")
    def advertised_public_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advertisedPublicPrefixes"))

    @advertised_public_prefixes.setter
    def advertised_public_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19cd9c3121cca6f48feb3983f65dc0f629d842a6c0aa6a3e97d6676ff7ffc98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedPublicPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerAsn")
    def customer_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customerAsn"))

    @customer_asn.setter
    def customer_asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0339c5f3ae3eba28c6f9df91ab8236789bf4d485ac44b27b919e07dfc4cbae37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerAsn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingRegistryName")
    def routing_registry_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingRegistryName"))

    @routing_registry_name.setter
    def routing_registry_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e521c96568b21e5b55dde04b717888023e3b92a8cdd4f019a3c04b56807279f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingRegistryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ExpressRouteCircuitPeeringIpv6MicrosoftPeering]:
        return typing.cast(typing.Optional[ExpressRouteCircuitPeeringIpv6MicrosoftPeering], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExpressRouteCircuitPeeringIpv6MicrosoftPeering],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e580a29a502862620c1b05ec2d599a7ce26a71518eeacee15f84b860167b580a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ExpressRouteCircuitPeeringIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringIpv6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea057635a8ee21e89bc0a9b0f6ede6ae2fe8c005cfb4df0e10e27f7207646b61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMicrosoftPeering")
    def put_microsoft_peering(
        self,
        *,
        advertised_communities: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_public_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        customer_asn: typing.Optional[jsii.Number] = None,
        routing_registry_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param advertised_communities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_communities ExpressRouteCircuitPeering#advertised_communities}.
        :param advertised_public_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_public_prefixes ExpressRouteCircuitPeering#advertised_public_prefixes}.
        :param customer_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#customer_asn ExpressRouteCircuitPeering#customer_asn}.
        :param routing_registry_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#routing_registry_name ExpressRouteCircuitPeering#routing_registry_name}.
        '''
        value = ExpressRouteCircuitPeeringIpv6MicrosoftPeering(
            advertised_communities=advertised_communities,
            advertised_public_prefixes=advertised_public_prefixes,
            customer_asn=customer_asn,
            routing_registry_name=routing_registry_name,
        )

        return typing.cast(None, jsii.invoke(self, "putMicrosoftPeering", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMicrosoftPeering")
    def reset_microsoft_peering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftPeering", []))

    @jsii.member(jsii_name="resetRouteFilterId")
    def reset_route_filter_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteFilterId", []))

    @builtins.property
    @jsii.member(jsii_name="microsoftPeering")
    def microsoft_peering(
        self,
    ) -> ExpressRouteCircuitPeeringIpv6MicrosoftPeeringOutputReference:
        return typing.cast(ExpressRouteCircuitPeeringIpv6MicrosoftPeeringOutputReference, jsii.get(self, "microsoftPeering"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftPeeringInput")
    def microsoft_peering_input(
        self,
    ) -> typing.Optional[ExpressRouteCircuitPeeringIpv6MicrosoftPeering]:
        return typing.cast(typing.Optional[ExpressRouteCircuitPeeringIpv6MicrosoftPeering], jsii.get(self, "microsoftPeeringInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryPeerAddressPrefixInput")
    def primary_peer_address_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryPeerAddressPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="routeFilterIdInput")
    def route_filter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeFilterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryPeerAddressPrefixInput")
    def secondary_peer_address_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryPeerAddressPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b91a46a5d9a0b4c62c821232931ab1cf9e32043451d3a3cc4f34e3b741bae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryPeerAddressPrefix")
    def primary_peer_address_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryPeerAddressPrefix"))

    @primary_peer_address_prefix.setter
    def primary_peer_address_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09889082401aeacd165f91aadb1f384ca056ef111c7d8e97c2ede1661c1b2f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryPeerAddressPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeFilterId")
    def route_filter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeFilterId"))

    @route_filter_id.setter
    def route_filter_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace80e3b168ef6310a4c7e93e7ca1f9f1fb76f76b05bc90f5ef193335ebc4a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeFilterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryPeerAddressPrefix")
    def secondary_peer_address_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryPeerAddressPrefix"))

    @secondary_peer_address_prefix.setter
    def secondary_peer_address_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7af7f843dfeab90aea9b9ed7568bb1e19e4aff15870cc5b69d55d0ef7f91df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryPeerAddressPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExpressRouteCircuitPeeringIpv6]:
        return typing.cast(typing.Optional[ExpressRouteCircuitPeeringIpv6], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExpressRouteCircuitPeeringIpv6],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996dbc99f146bd5b6e6003baf9868b14e7df726cc2af64a930eb46f0ba515d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringMicrosoftPeeringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "advertised_public_prefixes": "advertisedPublicPrefixes",
        "advertised_communities": "advertisedCommunities",
        "customer_asn": "customerAsn",
        "routing_registry_name": "routingRegistryName",
    },
)
class ExpressRouteCircuitPeeringMicrosoftPeeringConfig:
    def __init__(
        self,
        *,
        advertised_public_prefixes: typing.Sequence[builtins.str],
        advertised_communities: typing.Optional[typing.Sequence[builtins.str]] = None,
        customer_asn: typing.Optional[jsii.Number] = None,
        routing_registry_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param advertised_public_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_public_prefixes ExpressRouteCircuitPeering#advertised_public_prefixes}.
        :param advertised_communities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_communities ExpressRouteCircuitPeering#advertised_communities}.
        :param customer_asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#customer_asn ExpressRouteCircuitPeering#customer_asn}.
        :param routing_registry_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#routing_registry_name ExpressRouteCircuitPeering#routing_registry_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dc058960ac80d219846416434e283f6d02588d78958ba33ba4fd6d5fc5fcbf)
            check_type(argname="argument advertised_public_prefixes", value=advertised_public_prefixes, expected_type=type_hints["advertised_public_prefixes"])
            check_type(argname="argument advertised_communities", value=advertised_communities, expected_type=type_hints["advertised_communities"])
            check_type(argname="argument customer_asn", value=customer_asn, expected_type=type_hints["customer_asn"])
            check_type(argname="argument routing_registry_name", value=routing_registry_name, expected_type=type_hints["routing_registry_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "advertised_public_prefixes": advertised_public_prefixes,
        }
        if advertised_communities is not None:
            self._values["advertised_communities"] = advertised_communities
        if customer_asn is not None:
            self._values["customer_asn"] = customer_asn
        if routing_registry_name is not None:
            self._values["routing_registry_name"] = routing_registry_name

    @builtins.property
    def advertised_public_prefixes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_public_prefixes ExpressRouteCircuitPeering#advertised_public_prefixes}.'''
        result = self._values.get("advertised_public_prefixes")
        assert result is not None, "Required property 'advertised_public_prefixes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def advertised_communities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#advertised_communities ExpressRouteCircuitPeering#advertised_communities}.'''
        result = self._values.get("advertised_communities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def customer_asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#customer_asn ExpressRouteCircuitPeering#customer_asn}.'''
        result = self._values.get("customer_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def routing_registry_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#routing_registry_name ExpressRouteCircuitPeering#routing_registry_name}.'''
        result = self._values.get("routing_registry_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteCircuitPeeringMicrosoftPeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRouteCircuitPeeringMicrosoftPeeringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringMicrosoftPeeringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43fe136169f90a007f988a2808120e12e0b9d12b070c7b6fcee98c6699731ee4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdvertisedCommunities")
    def reset_advertised_communities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedCommunities", []))

    @jsii.member(jsii_name="resetCustomerAsn")
    def reset_customer_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerAsn", []))

    @jsii.member(jsii_name="resetRoutingRegistryName")
    def reset_routing_registry_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingRegistryName", []))

    @builtins.property
    @jsii.member(jsii_name="advertisedCommunitiesInput")
    def advertised_communities_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advertisedCommunitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedPublicPrefixesInput")
    def advertised_public_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advertisedPublicPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="customerAsnInput")
    def customer_asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customerAsnInput"))

    @builtins.property
    @jsii.member(jsii_name="routingRegistryNameInput")
    def routing_registry_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingRegistryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedCommunities")
    def advertised_communities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advertisedCommunities"))

    @advertised_communities.setter
    def advertised_communities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1908327ced9f3ba3a436d2b41c38167b8151ae23df61170ee2950db7299a4a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedCommunities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advertisedPublicPrefixes")
    def advertised_public_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advertisedPublicPrefixes"))

    @advertised_public_prefixes.setter
    def advertised_public_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93976abcdc7bac32f9c894e300996a54e4ec7b79c66448d98a0d21df6b500477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedPublicPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerAsn")
    def customer_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customerAsn"))

    @customer_asn.setter
    def customer_asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5b33404320eba23682afe9fdfb99433708101390a9d8b1eea596f3ccb25b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerAsn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingRegistryName")
    def routing_registry_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingRegistryName"))

    @routing_registry_name.setter
    def routing_registry_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e5c686b813076de564270585191689ca9fac95baa339e94467f5cad796ecd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingRegistryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ExpressRouteCircuitPeeringMicrosoftPeeringConfig]:
        return typing.cast(typing.Optional[ExpressRouteCircuitPeeringMicrosoftPeeringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ExpressRouteCircuitPeeringMicrosoftPeeringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6aa1399aa98ae921f80564cf1ce50839fdfd2d44d79da82bb154c41d96cc210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ExpressRouteCircuitPeeringTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#create ExpressRouteCircuitPeering#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#delete ExpressRouteCircuitPeering#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#read ExpressRouteCircuitPeering#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#update ExpressRouteCircuitPeering#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85dbbd107c9ca703d4455b018e2d5f526c34a8455ce1906eaa6ca972ac15837)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#create ExpressRouteCircuitPeering#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#delete ExpressRouteCircuitPeering#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#read ExpressRouteCircuitPeering#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_circuit_peering#update ExpressRouteCircuitPeering#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRouteCircuitPeeringTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRouteCircuitPeeringTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRouteCircuitPeering.ExpressRouteCircuitPeeringTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a130e20540fc5decf6bc3769f8691c1dd5da5c1f044e367f04052bf5196761)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce8f2bc00b88dd254137c578e5f1981c6a79ee2ea97c765c0022d4eaadd2a41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce90202bc05cbcd4278338be63f8a90e2a1054dc140173bd8be4733034d2e2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f6b00ea203296432d4a3ecff477311221be0231f9773f2a1132b197587697c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721b5a89d7054d8f193e98b66a7206057cbb3d4ebe72a6efe8a03d08dfa157c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteCircuitPeeringTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteCircuitPeeringTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteCircuitPeeringTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade13aa6abaa9f21d81fd6396ffb140bf23d8820f4fa3b60ea3b95af3c17f765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ExpressRouteCircuitPeering",
    "ExpressRouteCircuitPeeringConfig",
    "ExpressRouteCircuitPeeringIpv6",
    "ExpressRouteCircuitPeeringIpv6MicrosoftPeering",
    "ExpressRouteCircuitPeeringIpv6MicrosoftPeeringOutputReference",
    "ExpressRouteCircuitPeeringIpv6OutputReference",
    "ExpressRouteCircuitPeeringMicrosoftPeeringConfig",
    "ExpressRouteCircuitPeeringMicrosoftPeeringConfigOutputReference",
    "ExpressRouteCircuitPeeringTimeouts",
    "ExpressRouteCircuitPeeringTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1f122288abfe9d0f2b076a3e6d1b0cb2f6b479be1fc485610a506eb21c33c4aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    express_route_circuit_name: builtins.str,
    peering_type: builtins.str,
    resource_group_name: builtins.str,
    vlan_id: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipv6: typing.Optional[typing.Union[ExpressRouteCircuitPeeringIpv6, typing.Dict[builtins.str, typing.Any]]] = None,
    microsoft_peering_config: typing.Optional[typing.Union[ExpressRouteCircuitPeeringMicrosoftPeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_asn: typing.Optional[jsii.Number] = None,
    primary_peer_address_prefix: typing.Optional[builtins.str] = None,
    route_filter_id: typing.Optional[builtins.str] = None,
    secondary_peer_address_prefix: typing.Optional[builtins.str] = None,
    shared_key: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ExpressRouteCircuitPeeringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8ca66a8136154e3e9318831ae724355d4f1cdc92d88c7dac70a3f67c4fcf4dac(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ba0c6b77079f54a98fd4f7a0232eb66017e129b7fe0fa28e0978999296e76b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60056476ff5d244b0cc3844bd42dd1d1fd8093a1992db5f01224a33b8fda4619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d33265bdb04933a6475eea050849e90e02688eee1b3bee67a64ae8991d042b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d5683c02abb18d4f3cff260f49cf562bc8e939eafba0bf1c6482d099edc774(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0063c73d35fe5150bd63af66a4f521ef604dc929d7768e6407515460949492d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbbe93a9c0a255f8e0d3b5e40830513e7590612ecccb976173ef4f69da4bd2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05aa39ad270d9d8c404ed0a492320467046ddf58293c277f2de9b55076efb063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50797301671c0713b7fae70c103d654068521028e8089161f1e452074aa1e3a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a9ee86bdff069abbcbe2645284397d49249fd2723367b83ef15cfd9451beae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1278d483c69302dc2d1e9d2d4be01010f5041c66aabd58a4b6948735d7ecba52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6c9468a0fe5f4af2a399a74558853ff46e579b5790a2045b69bda303fa3dca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5136550e07f51700ad7d027cc606afd95d175715ca8db78caa7bccbf2189b7f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    express_route_circuit_name: builtins.str,
    peering_type: builtins.str,
    resource_group_name: builtins.str,
    vlan_id: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipv6: typing.Optional[typing.Union[ExpressRouteCircuitPeeringIpv6, typing.Dict[builtins.str, typing.Any]]] = None,
    microsoft_peering_config: typing.Optional[typing.Union[ExpressRouteCircuitPeeringMicrosoftPeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_asn: typing.Optional[jsii.Number] = None,
    primary_peer_address_prefix: typing.Optional[builtins.str] = None,
    route_filter_id: typing.Optional[builtins.str] = None,
    secondary_peer_address_prefix: typing.Optional[builtins.str] = None,
    shared_key: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ExpressRouteCircuitPeeringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d0b40ea4a2874c7ee074106c5da3bd7d35cc44738a8e8f3ea396f3daed3bf8(
    *,
    primary_peer_address_prefix: builtins.str,
    secondary_peer_address_prefix: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    microsoft_peering: typing.Optional[typing.Union[ExpressRouteCircuitPeeringIpv6MicrosoftPeering, typing.Dict[builtins.str, typing.Any]]] = None,
    route_filter_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3941113d6bb8e7e0a81d59a2c6b40d492be878e6afbae70d27d93e56cacf3f(
    *,
    advertised_communities: typing.Optional[typing.Sequence[builtins.str]] = None,
    advertised_public_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    customer_asn: typing.Optional[jsii.Number] = None,
    routing_registry_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79f6f7a09a61fb59a37f10eefbe9b11925fc967f5b07e8f0c89e92a4d0539c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d395f26b7b618b11301a6afd961711f80b9d8bfea76deb54cc498d64f1e7b18(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19cd9c3121cca6f48feb3983f65dc0f629d842a6c0aa6a3e97d6676ff7ffc98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0339c5f3ae3eba28c6f9df91ab8236789bf4d485ac44b27b919e07dfc4cbae37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e521c96568b21e5b55dde04b717888023e3b92a8cdd4f019a3c04b56807279f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e580a29a502862620c1b05ec2d599a7ce26a71518eeacee15f84b860167b580a(
    value: typing.Optional[ExpressRouteCircuitPeeringIpv6MicrosoftPeering],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea057635a8ee21e89bc0a9b0f6ede6ae2fe8c005cfb4df0e10e27f7207646b61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b91a46a5d9a0b4c62c821232931ab1cf9e32043451d3a3cc4f34e3b741bae5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09889082401aeacd165f91aadb1f384ca056ef111c7d8e97c2ede1661c1b2f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace80e3b168ef6310a4c7e93e7ca1f9f1fb76f76b05bc90f5ef193335ebc4a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7af7f843dfeab90aea9b9ed7568bb1e19e4aff15870cc5b69d55d0ef7f91df6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996dbc99f146bd5b6e6003baf9868b14e7df726cc2af64a930eb46f0ba515d83(
    value: typing.Optional[ExpressRouteCircuitPeeringIpv6],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dc058960ac80d219846416434e283f6d02588d78958ba33ba4fd6d5fc5fcbf(
    *,
    advertised_public_prefixes: typing.Sequence[builtins.str],
    advertised_communities: typing.Optional[typing.Sequence[builtins.str]] = None,
    customer_asn: typing.Optional[jsii.Number] = None,
    routing_registry_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fe136169f90a007f988a2808120e12e0b9d12b070c7b6fcee98c6699731ee4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1908327ced9f3ba3a436d2b41c38167b8151ae23df61170ee2950db7299a4a44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93976abcdc7bac32f9c894e300996a54e4ec7b79c66448d98a0d21df6b500477(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5b33404320eba23682afe9fdfb99433708101390a9d8b1eea596f3ccb25b81(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e5c686b813076de564270585191689ca9fac95baa339e94467f5cad796ecd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6aa1399aa98ae921f80564cf1ce50839fdfd2d44d79da82bb154c41d96cc210(
    value: typing.Optional[ExpressRouteCircuitPeeringMicrosoftPeeringConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85dbbd107c9ca703d4455b018e2d5f526c34a8455ce1906eaa6ca972ac15837(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a130e20540fc5decf6bc3769f8691c1dd5da5c1f044e367f04052bf5196761(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8f2bc00b88dd254137c578e5f1981c6a79ee2ea97c765c0022d4eaadd2a41a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce90202bc05cbcd4278338be63f8a90e2a1054dc140173bd8be4733034d2e2e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f6b00ea203296432d4a3ecff477311221be0231f9773f2a1132b197587697c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721b5a89d7054d8f193e98b66a7206057cbb3d4ebe72a6efe8a03d08dfa157c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade13aa6abaa9f21d81fd6396ffb140bf23d8820f4fa3b60ea3b95af3c17f765(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRouteCircuitPeeringTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
