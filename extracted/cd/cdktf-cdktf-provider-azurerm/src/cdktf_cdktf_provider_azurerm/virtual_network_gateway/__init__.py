r'''
# `azurerm_virtual_network_gateway`

Refer to the Terraform Registry for docs: [`azurerm_virtual_network_gateway`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway).
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


class VirtualNetworkGateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway azurerm_virtual_network_gateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: builtins.str,
        type: builtins.str,
        active_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_route_translation_for_nat_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_settings: typing.Optional[typing.Union["VirtualNetworkGatewayBgpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_route: typing.Optional[typing.Union["VirtualNetworkGatewayCustomRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        default_local_network_gateway_id: typing.Optional[builtins.str] = None,
        dns_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        enable_bgp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_sec_replay_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayPolicyGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        private_ip_address_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_vnet_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualNetworkGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_wan_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpn_client_configuration: typing.Optional[typing.Union["VirtualNetworkGatewayVpnClientConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        vpn_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway azurerm_virtual_network_gateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_configuration VirtualNetworkGateway#ip_configuration}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#location VirtualNetworkGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#resource_group_name VirtualNetworkGateway#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sku VirtualNetworkGateway#sku}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#type VirtualNetworkGateway#type}.
        :param active_active: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#active_active VirtualNetworkGateway#active_active}.
        :param bgp_route_translation_for_nat_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#bgp_route_translation_for_nat_enabled VirtualNetworkGateway#bgp_route_translation_for_nat_enabled}.
        :param bgp_settings: bgp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#bgp_settings VirtualNetworkGateway#bgp_settings}
        :param custom_route: custom_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#custom_route VirtualNetworkGateway#custom_route}
        :param default_local_network_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#default_local_network_gateway_id VirtualNetworkGateway#default_local_network_gateway_id}.
        :param dns_forwarding_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#dns_forwarding_enabled VirtualNetworkGateway#dns_forwarding_enabled}.
        :param edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#edge_zone VirtualNetworkGateway#edge_zone}.
        :param enable_bgp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#enable_bgp VirtualNetworkGateway#enable_bgp}.
        :param generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#generation VirtualNetworkGateway#generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#id VirtualNetworkGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_sec_replay_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_sec_replay_protection_enabled VirtualNetworkGateway#ip_sec_replay_protection_enabled}.
        :param policy_group: policy_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#policy_group VirtualNetworkGateway#policy_group}
        :param private_ip_address_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#private_ip_address_enabled VirtualNetworkGateway#private_ip_address_enabled}.
        :param remote_vnet_traffic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#remote_vnet_traffic_enabled VirtualNetworkGateway#remote_vnet_traffic_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#tags VirtualNetworkGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#timeouts VirtualNetworkGateway#timeouts}
        :param virtual_wan_traffic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#virtual_wan_traffic_enabled VirtualNetworkGateway#virtual_wan_traffic_enabled}.
        :param vpn_client_configuration: vpn_client_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_client_configuration VirtualNetworkGateway#vpn_client_configuration}
        :param vpn_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_type VirtualNetworkGateway#vpn_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48953827ec555ed2ade9040335a854e18bd38c848a8bf9c1c07f2877a70b35fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualNetworkGatewayConfig(
            ip_configuration=ip_configuration,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sku=sku,
            type=type,
            active_active=active_active,
            bgp_route_translation_for_nat_enabled=bgp_route_translation_for_nat_enabled,
            bgp_settings=bgp_settings,
            custom_route=custom_route,
            default_local_network_gateway_id=default_local_network_gateway_id,
            dns_forwarding_enabled=dns_forwarding_enabled,
            edge_zone=edge_zone,
            enable_bgp=enable_bgp,
            generation=generation,
            id=id,
            ip_sec_replay_protection_enabled=ip_sec_replay_protection_enabled,
            policy_group=policy_group,
            private_ip_address_enabled=private_ip_address_enabled,
            remote_vnet_traffic_enabled=remote_vnet_traffic_enabled,
            tags=tags,
            timeouts=timeouts,
            virtual_wan_traffic_enabled=virtual_wan_traffic_enabled,
            vpn_client_configuration=vpn_client_configuration,
            vpn_type=vpn_type,
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
        '''Generates CDKTF code for importing a VirtualNetworkGateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VirtualNetworkGateway to import.
        :param import_from_id: The id of the existing VirtualNetworkGateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VirtualNetworkGateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff00b2951af5962d6fe409a806ed4f4295c6d984858e952e6b728b1acce3576c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBgpSettings")
    def put_bgp_settings(
        self,
        *,
        asn: typing.Optional[jsii.Number] = None,
        peering_addresses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayBgpSettingsPeeringAddresses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        peer_weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#asn VirtualNetworkGateway#asn}.
        :param peering_addresses: peering_addresses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#peering_addresses VirtualNetworkGateway#peering_addresses}
        :param peer_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#peer_weight VirtualNetworkGateway#peer_weight}.
        '''
        value = VirtualNetworkGatewayBgpSettings(
            asn=asn, peering_addresses=peering_addresses, peer_weight=peer_weight
        )

        return typing.cast(None, jsii.invoke(self, "putBgpSettings", [value]))

    @jsii.member(jsii_name="putCustomRoute")
    def put_custom_route(
        self,
        *,
        address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_prefixes VirtualNetworkGateway#address_prefixes}.
        '''
        value = VirtualNetworkGatewayCustomRoute(address_prefixes=address_prefixes)

        return typing.cast(None, jsii.invoke(self, "putCustomRoute", [value]))

    @jsii.member(jsii_name="putIpConfiguration")
    def put_ip_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0e5077f9c33290cc4271d21b596bbaf36c40b478c75a181001a4554a4d9cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpConfiguration", [value]))

    @jsii.member(jsii_name="putPolicyGroup")
    def put_policy_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayPolicyGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50acfde923af101ec5b4b2a48a481f77e11b9e7a06225ec083556125241aadb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyGroup", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#create VirtualNetworkGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#delete VirtualNetworkGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#read VirtualNetworkGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#update VirtualNetworkGateway#update}.
        '''
        value = VirtualNetworkGatewayTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpnClientConfiguration")
    def put_vpn_client_configuration(
        self,
        *,
        address_space: typing.Sequence[builtins.str],
        aad_audience: typing.Optional[builtins.str] = None,
        aad_issuer: typing.Optional[builtins.str] = None,
        aad_tenant: typing.Optional[builtins.str] = None,
        ipsec_policy: typing.Optional[typing.Union["VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        radius_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRadiusServer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        radius_server_address: typing.Optional[builtins.str] = None,
        radius_server_secret: typing.Optional[builtins.str] = None,
        revoked_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        root_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRootCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        virtual_network_gateway_client_connection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpn_auth_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpn_client_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param address_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_space VirtualNetworkGateway#address_space}.
        :param aad_audience: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_audience VirtualNetworkGateway#aad_audience}.
        :param aad_issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_issuer VirtualNetworkGateway#aad_issuer}.
        :param aad_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_tenant VirtualNetworkGateway#aad_tenant}.
        :param ipsec_policy: ipsec_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_policy VirtualNetworkGateway#ipsec_policy}
        :param radius_server: radius_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server VirtualNetworkGateway#radius_server}
        :param radius_server_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server_address VirtualNetworkGateway#radius_server_address}.
        :param radius_server_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server_secret VirtualNetworkGateway#radius_server_secret}.
        :param revoked_certificate: revoked_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#revoked_certificate VirtualNetworkGateway#revoked_certificate}
        :param root_certificate: root_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#root_certificate VirtualNetworkGateway#root_certificate}
        :param virtual_network_gateway_client_connection: virtual_network_gateway_client_connection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#virtual_network_gateway_client_connection VirtualNetworkGateway#virtual_network_gateway_client_connection}
        :param vpn_auth_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_auth_types VirtualNetworkGateway#vpn_auth_types}.
        :param vpn_client_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_client_protocols VirtualNetworkGateway#vpn_client_protocols}.
        '''
        value = VirtualNetworkGatewayVpnClientConfiguration(
            address_space=address_space,
            aad_audience=aad_audience,
            aad_issuer=aad_issuer,
            aad_tenant=aad_tenant,
            ipsec_policy=ipsec_policy,
            radius_server=radius_server,
            radius_server_address=radius_server_address,
            radius_server_secret=radius_server_secret,
            revoked_certificate=revoked_certificate,
            root_certificate=root_certificate,
            virtual_network_gateway_client_connection=virtual_network_gateway_client_connection,
            vpn_auth_types=vpn_auth_types,
            vpn_client_protocols=vpn_client_protocols,
        )

        return typing.cast(None, jsii.invoke(self, "putVpnClientConfiguration", [value]))

    @jsii.member(jsii_name="resetActiveActive")
    def reset_active_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveActive", []))

    @jsii.member(jsii_name="resetBgpRouteTranslationForNatEnabled")
    def reset_bgp_route_translation_for_nat_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpRouteTranslationForNatEnabled", []))

    @jsii.member(jsii_name="resetBgpSettings")
    def reset_bgp_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpSettings", []))

    @jsii.member(jsii_name="resetCustomRoute")
    def reset_custom_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRoute", []))

    @jsii.member(jsii_name="resetDefaultLocalNetworkGatewayId")
    def reset_default_local_network_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLocalNetworkGatewayId", []))

    @jsii.member(jsii_name="resetDnsForwardingEnabled")
    def reset_dns_forwarding_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsForwardingEnabled", []))

    @jsii.member(jsii_name="resetEdgeZone")
    def reset_edge_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeZone", []))

    @jsii.member(jsii_name="resetEnableBgp")
    def reset_enable_bgp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableBgp", []))

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpSecReplayProtectionEnabled")
    def reset_ip_sec_replay_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpSecReplayProtectionEnabled", []))

    @jsii.member(jsii_name="resetPolicyGroup")
    def reset_policy_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyGroup", []))

    @jsii.member(jsii_name="resetPrivateIpAddressEnabled")
    def reset_private_ip_address_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAddressEnabled", []))

    @jsii.member(jsii_name="resetRemoteVnetTrafficEnabled")
    def reset_remote_vnet_traffic_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteVnetTrafficEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualWanTrafficEnabled")
    def reset_virtual_wan_traffic_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualWanTrafficEnabled", []))

    @jsii.member(jsii_name="resetVpnClientConfiguration")
    def reset_vpn_client_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnClientConfiguration", []))

    @jsii.member(jsii_name="resetVpnType")
    def reset_vpn_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnType", []))

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
    @jsii.member(jsii_name="bgpSettings")
    def bgp_settings(self) -> "VirtualNetworkGatewayBgpSettingsOutputReference":
        return typing.cast("VirtualNetworkGatewayBgpSettingsOutputReference", jsii.get(self, "bgpSettings"))

    @builtins.property
    @jsii.member(jsii_name="customRoute")
    def custom_route(self) -> "VirtualNetworkGatewayCustomRouteOutputReference":
        return typing.cast("VirtualNetworkGatewayCustomRouteOutputReference", jsii.get(self, "customRoute"))

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(self) -> "VirtualNetworkGatewayIpConfigurationList":
        return typing.cast("VirtualNetworkGatewayIpConfigurationList", jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="policyGroup")
    def policy_group(self) -> "VirtualNetworkGatewayPolicyGroupList":
        return typing.cast("VirtualNetworkGatewayPolicyGroupList", jsii.get(self, "policyGroup"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualNetworkGatewayTimeoutsOutputReference":
        return typing.cast("VirtualNetworkGatewayTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpnClientConfiguration")
    def vpn_client_configuration(
        self,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationOutputReference":
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationOutputReference", jsii.get(self, "vpnClientConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="activeActiveInput")
    def active_active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeActiveInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpRouteTranslationForNatEnabledInput")
    def bgp_route_translation_for_nat_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bgpRouteTranslationForNatEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpSettingsInput")
    def bgp_settings_input(self) -> typing.Optional["VirtualNetworkGatewayBgpSettings"]:
        return typing.cast(typing.Optional["VirtualNetworkGatewayBgpSettings"], jsii.get(self, "bgpSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="customRouteInput")
    def custom_route_input(self) -> typing.Optional["VirtualNetworkGatewayCustomRoute"]:
        return typing.cast(typing.Optional["VirtualNetworkGatewayCustomRoute"], jsii.get(self, "customRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLocalNetworkGatewayIdInput")
    def default_local_network_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLocalNetworkGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsForwardingEnabledInput")
    def dns_forwarding_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dnsForwardingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeZoneInput")
    def edge_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="enableBgpInput")
    def enable_bgp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableBgpInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayIpConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayIpConfiguration"]]], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSecReplayProtectionEnabledInput")
    def ip_sec_replay_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipSecReplayProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyGroupInput")
    def policy_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroup"]]], jsii.get(self, "policyGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressEnabledInput")
    def private_ip_address_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateIpAddressEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVnetTrafficEnabledInput")
    def remote_vnet_traffic_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "remoteVnetTrafficEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualNetworkGatewayTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualNetworkGatewayTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualWanTrafficEnabledInput")
    def virtual_wan_traffic_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "virtualWanTrafficEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnClientConfigurationInput")
    def vpn_client_configuration_input(
        self,
    ) -> typing.Optional["VirtualNetworkGatewayVpnClientConfiguration"]:
        return typing.cast(typing.Optional["VirtualNetworkGatewayVpnClientConfiguration"], jsii.get(self, "vpnClientConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnTypeInput")
    def vpn_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="activeActive")
    def active_active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "activeActive"))

    @active_active.setter
    def active_active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe3a72720183257abafcf181f6857c5d02b48d6bb224fc690aec2dd6e4538c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeActive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpRouteTranslationForNatEnabled")
    def bgp_route_translation_for_nat_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bgpRouteTranslationForNatEnabled"))

    @bgp_route_translation_for_nat_enabled.setter
    def bgp_route_translation_for_nat_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17726d73e9a2d733c5d6f24862f44ff1991494617aa43398ecab021521db2f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpRouteTranslationForNatEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLocalNetworkGatewayId")
    def default_local_network_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLocalNetworkGatewayId"))

    @default_local_network_gateway_id.setter
    def default_local_network_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e87b4fd6cd9fd2376b774502ab5824e5f155968223390434167f95b79587126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLocalNetworkGatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsForwardingEnabled")
    def dns_forwarding_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dnsForwardingEnabled"))

    @dns_forwarding_enabled.setter
    def dns_forwarding_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ebb7ca73b283cc3534a5a74173929fe065cb68df8679b3cf40041d35fccb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsForwardingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeZone")
    def edge_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeZone"))

    @edge_zone.setter
    def edge_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9adfb8eb2912f6e71eb6ae05caeec9965379930d028903ba87ae8b9beba30f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableBgp")
    def enable_bgp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableBgp"))

    @enable_bgp.setter
    def enable_bgp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f1eb717cfd9d4d4a5463fd286c4bf395595aa302388b89f35fa23285c8847b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBgp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0f16c9d3aff631060d3863bcd757757ffc3d328c29c0559e754ffe96f46851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecfcb9566093233315323e39518a9e073bbf2cdefd1f6437ca80d9c96ad13cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipSecReplayProtectionEnabled")
    def ip_sec_replay_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipSecReplayProtectionEnabled"))

    @ip_sec_replay_protection_enabled.setter
    def ip_sec_replay_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deadd2318116ae00073f4c7fb5d6bd327d5024fd3bd26458ba9983b18dcd1dcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSecReplayProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6818008462492304e4fc25ada0964c8c920e2b90c514ffcdf6aef491a2ec83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed06eea6f093e99e965f1676bc3c5c3fec51b8c3e80c70ced83348727f197b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressEnabled")
    def private_ip_address_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateIpAddressEnabled"))

    @private_ip_address_enabled.setter
    def private_ip_address_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5360c6e95b57967db895bb2093710553378a725c73f705ecf4b20ee80c605c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddressEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteVnetTrafficEnabled")
    def remote_vnet_traffic_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remoteVnetTrafficEnabled"))

    @remote_vnet_traffic_enabled.setter
    def remote_vnet_traffic_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e774f9e45d6742908e03c99476e66705ed6a85e7366c67c549a9b3bbe7330f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVnetTrafficEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f45ad6700ce0b670f1e189a594e4cd9cecf4f3144cfc3b3cfec8f015e80cfcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b46da206be18874c74ef3c93f1379195dfab2b47e2b25d9626d62e57d19e193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ca5a8253034355b37fb444a61e2063da3b5a9a56f42ca8c3e3f732109171c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d8d50f15a04d7d80a6aadc0c38b8f4fd8473efd2821eb15791b6da0522feae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualWanTrafficEnabled")
    def virtual_wan_traffic_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "virtualWanTrafficEnabled"))

    @virtual_wan_traffic_enabled.setter
    def virtual_wan_traffic_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4befd19b56043db5f8efcf1d2cecc750f1a0b2b472b0fbc4df267dc465b249a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualWanTrafficEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnType")
    def vpn_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnType"))

    @vpn_type.setter
    def vpn_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dff0705f371233906b88ba32007dfe9bbf68894fdd12b338daa8ddc5e0cc5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayBgpSettings",
    jsii_struct_bases=[],
    name_mapping={
        "asn": "asn",
        "peering_addresses": "peeringAddresses",
        "peer_weight": "peerWeight",
    },
)
class VirtualNetworkGatewayBgpSettings:
    def __init__(
        self,
        *,
        asn: typing.Optional[jsii.Number] = None,
        peering_addresses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayBgpSettingsPeeringAddresses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        peer_weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#asn VirtualNetworkGateway#asn}.
        :param peering_addresses: peering_addresses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#peering_addresses VirtualNetworkGateway#peering_addresses}
        :param peer_weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#peer_weight VirtualNetworkGateway#peer_weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b89d9fa883cefca5a312fb3160101ba319399c109101e3c061c718cb2d19bb)
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument peering_addresses", value=peering_addresses, expected_type=type_hints["peering_addresses"])
            check_type(argname="argument peer_weight", value=peer_weight, expected_type=type_hints["peer_weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asn is not None:
            self._values["asn"] = asn
        if peering_addresses is not None:
            self._values["peering_addresses"] = peering_addresses
        if peer_weight is not None:
            self._values["peer_weight"] = peer_weight

    @builtins.property
    def asn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#asn VirtualNetworkGateway#asn}.'''
        result = self._values.get("asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def peering_addresses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayBgpSettingsPeeringAddresses"]]]:
        '''peering_addresses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#peering_addresses VirtualNetworkGateway#peering_addresses}
        '''
        result = self._values.get("peering_addresses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayBgpSettingsPeeringAddresses"]]], result)

    @builtins.property
    def peer_weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#peer_weight VirtualNetworkGateway#peer_weight}.'''
        result = self._values.get("peer_weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayBgpSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayBgpSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayBgpSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3997b1229d903682925bc15abfd38be1e6b94d57bdacb1ad532f3e2c8732e42a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPeeringAddresses")
    def put_peering_addresses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayBgpSettingsPeeringAddresses", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2217caf9b4ca629d7db55a91a4b504b693b1767d5bf0838963fdbafdbba31ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPeeringAddresses", [value]))

    @jsii.member(jsii_name="resetAsn")
    def reset_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsn", []))

    @jsii.member(jsii_name="resetPeeringAddresses")
    def reset_peering_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeeringAddresses", []))

    @jsii.member(jsii_name="resetPeerWeight")
    def reset_peer_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerWeight", []))

    @builtins.property
    @jsii.member(jsii_name="peeringAddresses")
    def peering_addresses(
        self,
    ) -> "VirtualNetworkGatewayBgpSettingsPeeringAddressesList":
        return typing.cast("VirtualNetworkGatewayBgpSettingsPeeringAddressesList", jsii.get(self, "peeringAddresses"))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringAddressesInput")
    def peering_addresses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayBgpSettingsPeeringAddresses"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayBgpSettingsPeeringAddresses"]]], jsii.get(self, "peeringAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="peerWeightInput")
    def peer_weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "peerWeightInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abfb7040a1e5160439b927ab75ecabfb6c5fdad2656579f8d3f59bb3ab71d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerWeight")
    def peer_weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "peerWeight"))

    @peer_weight.setter
    def peer_weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7006ed9dafe979164164b7fc681284237c55c4e345e28a412e14bb807c30fc15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerWeight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VirtualNetworkGatewayBgpSettings]:
        return typing.cast(typing.Optional[VirtualNetworkGatewayBgpSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualNetworkGatewayBgpSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d47d545b4575fc12efdaa4d352f4f47e76a9018beebde1eac07200338a090ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayBgpSettingsPeeringAddresses",
    jsii_struct_bases=[],
    name_mapping={
        "apipa_addresses": "apipaAddresses",
        "ip_configuration_name": "ipConfigurationName",
    },
)
class VirtualNetworkGatewayBgpSettingsPeeringAddresses:
    def __init__(
        self,
        *,
        apipa_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_configuration_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param apipa_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#apipa_addresses VirtualNetworkGateway#apipa_addresses}.
        :param ip_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_configuration_name VirtualNetworkGateway#ip_configuration_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ead08f321aab8832793574a545799989d2022c1fb9164edfe10fca3b0bbeed)
            check_type(argname="argument apipa_addresses", value=apipa_addresses, expected_type=type_hints["apipa_addresses"])
            check_type(argname="argument ip_configuration_name", value=ip_configuration_name, expected_type=type_hints["ip_configuration_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apipa_addresses is not None:
            self._values["apipa_addresses"] = apipa_addresses
        if ip_configuration_name is not None:
            self._values["ip_configuration_name"] = ip_configuration_name

    @builtins.property
    def apipa_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#apipa_addresses VirtualNetworkGateway#apipa_addresses}.'''
        result = self._values.get("apipa_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_configuration_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_configuration_name VirtualNetworkGateway#ip_configuration_name}.'''
        result = self._values.get("ip_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayBgpSettingsPeeringAddresses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayBgpSettingsPeeringAddressesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayBgpSettingsPeeringAddressesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8157c713bae26bd28312210519ffc89e0f2b858691e2fab14eed06e88a5c187f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayBgpSettingsPeeringAddressesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01f118d9b59dce6359ef6f526160877f031ea2cc9607bdb5dd8e12e2748d144)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayBgpSettingsPeeringAddressesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a6418c52af2fe098279c504861322aa8cd3f110c3244772b6174b5028cdd3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4442757e43a67c90c718185fb23c65cd408a12cfd83e084bd3ec44d13d5bb1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de2f350bb5f65f5a3edccf8f2ec194cfe9aa02ac779f35f8021dd901744e3fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayBgpSettingsPeeringAddresses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayBgpSettingsPeeringAddresses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayBgpSettingsPeeringAddresses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8271f2ca8173eb90069ca42e73df376caca3afe200e02f932a01272b997239b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayBgpSettingsPeeringAddressesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayBgpSettingsPeeringAddressesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ca5035b06ec078436d06f667af12ca7400e91383bf9487159fbbb65b43aa6ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetApipaAddresses")
    def reset_apipa_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApipaAddresses", []))

    @jsii.member(jsii_name="resetIpConfigurationName")
    def reset_ip_configuration_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpConfigurationName", []))

    @builtins.property
    @jsii.member(jsii_name="defaultAddresses")
    def default_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultAddresses"))

    @builtins.property
    @jsii.member(jsii_name="tunnelIpAddresses")
    def tunnel_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnelIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="apipaAddressesInput")
    def apipa_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apipaAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationNameInput")
    def ip_configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="apipaAddresses")
    def apipa_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apipaAddresses"))

    @apipa_addresses.setter
    def apipa_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ffb5debe920f14078f9dc934500d0d73f1cc3ca45bf31c0b7e158661be1dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apipaAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationName")
    def ip_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipConfigurationName"))

    @ip_configuration_name.setter
    def ip_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1624ff33f7cf01ed1d57badbdf1f1fe48d6169c38e3347a5c67ac3514c88477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipConfigurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayBgpSettingsPeeringAddresses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayBgpSettingsPeeringAddresses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayBgpSettingsPeeringAddresses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e658addeecd95b09eddc4f5c36f91ebde33ed3d0499079502a9467943cf8522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "ip_configuration": "ipConfiguration",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sku": "sku",
        "type": "type",
        "active_active": "activeActive",
        "bgp_route_translation_for_nat_enabled": "bgpRouteTranslationForNatEnabled",
        "bgp_settings": "bgpSettings",
        "custom_route": "customRoute",
        "default_local_network_gateway_id": "defaultLocalNetworkGatewayId",
        "dns_forwarding_enabled": "dnsForwardingEnabled",
        "edge_zone": "edgeZone",
        "enable_bgp": "enableBgp",
        "generation": "generation",
        "id": "id",
        "ip_sec_replay_protection_enabled": "ipSecReplayProtectionEnabled",
        "policy_group": "policyGroup",
        "private_ip_address_enabled": "privateIpAddressEnabled",
        "remote_vnet_traffic_enabled": "remoteVnetTrafficEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
        "virtual_wan_traffic_enabled": "virtualWanTrafficEnabled",
        "vpn_client_configuration": "vpnClientConfiguration",
        "vpn_type": "vpnType",
    },
)
class VirtualNetworkGatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: builtins.str,
        type: builtins.str,
        active_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_route_translation_for_nat_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_settings: typing.Optional[typing.Union[VirtualNetworkGatewayBgpSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_route: typing.Optional[typing.Union["VirtualNetworkGatewayCustomRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        default_local_network_gateway_id: typing.Optional[builtins.str] = None,
        dns_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        enable_bgp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        generation: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_sec_replay_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayPolicyGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        private_ip_address_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_vnet_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualNetworkGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_wan_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpn_client_configuration: typing.Optional[typing.Union["VirtualNetworkGatewayVpnClientConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        vpn_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_configuration VirtualNetworkGateway#ip_configuration}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#location VirtualNetworkGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#resource_group_name VirtualNetworkGateway#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sku VirtualNetworkGateway#sku}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#type VirtualNetworkGateway#type}.
        :param active_active: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#active_active VirtualNetworkGateway#active_active}.
        :param bgp_route_translation_for_nat_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#bgp_route_translation_for_nat_enabled VirtualNetworkGateway#bgp_route_translation_for_nat_enabled}.
        :param bgp_settings: bgp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#bgp_settings VirtualNetworkGateway#bgp_settings}
        :param custom_route: custom_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#custom_route VirtualNetworkGateway#custom_route}
        :param default_local_network_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#default_local_network_gateway_id VirtualNetworkGateway#default_local_network_gateway_id}.
        :param dns_forwarding_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#dns_forwarding_enabled VirtualNetworkGateway#dns_forwarding_enabled}.
        :param edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#edge_zone VirtualNetworkGateway#edge_zone}.
        :param enable_bgp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#enable_bgp VirtualNetworkGateway#enable_bgp}.
        :param generation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#generation VirtualNetworkGateway#generation}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#id VirtualNetworkGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_sec_replay_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_sec_replay_protection_enabled VirtualNetworkGateway#ip_sec_replay_protection_enabled}.
        :param policy_group: policy_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#policy_group VirtualNetworkGateway#policy_group}
        :param private_ip_address_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#private_ip_address_enabled VirtualNetworkGateway#private_ip_address_enabled}.
        :param remote_vnet_traffic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#remote_vnet_traffic_enabled VirtualNetworkGateway#remote_vnet_traffic_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#tags VirtualNetworkGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#timeouts VirtualNetworkGateway#timeouts}
        :param virtual_wan_traffic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#virtual_wan_traffic_enabled VirtualNetworkGateway#virtual_wan_traffic_enabled}.
        :param vpn_client_configuration: vpn_client_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_client_configuration VirtualNetworkGateway#vpn_client_configuration}
        :param vpn_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_type VirtualNetworkGateway#vpn_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bgp_settings, dict):
            bgp_settings = VirtualNetworkGatewayBgpSettings(**bgp_settings)
        if isinstance(custom_route, dict):
            custom_route = VirtualNetworkGatewayCustomRoute(**custom_route)
        if isinstance(timeouts, dict):
            timeouts = VirtualNetworkGatewayTimeouts(**timeouts)
        if isinstance(vpn_client_configuration, dict):
            vpn_client_configuration = VirtualNetworkGatewayVpnClientConfiguration(**vpn_client_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c246c68e1ae81b3e553e2bb185120d38bb957f8535ac32bf7b117ee28f4f69)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument active_active", value=active_active, expected_type=type_hints["active_active"])
            check_type(argname="argument bgp_route_translation_for_nat_enabled", value=bgp_route_translation_for_nat_enabled, expected_type=type_hints["bgp_route_translation_for_nat_enabled"])
            check_type(argname="argument bgp_settings", value=bgp_settings, expected_type=type_hints["bgp_settings"])
            check_type(argname="argument custom_route", value=custom_route, expected_type=type_hints["custom_route"])
            check_type(argname="argument default_local_network_gateway_id", value=default_local_network_gateway_id, expected_type=type_hints["default_local_network_gateway_id"])
            check_type(argname="argument dns_forwarding_enabled", value=dns_forwarding_enabled, expected_type=type_hints["dns_forwarding_enabled"])
            check_type(argname="argument edge_zone", value=edge_zone, expected_type=type_hints["edge_zone"])
            check_type(argname="argument enable_bgp", value=enable_bgp, expected_type=type_hints["enable_bgp"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_sec_replay_protection_enabled", value=ip_sec_replay_protection_enabled, expected_type=type_hints["ip_sec_replay_protection_enabled"])
            check_type(argname="argument policy_group", value=policy_group, expected_type=type_hints["policy_group"])
            check_type(argname="argument private_ip_address_enabled", value=private_ip_address_enabled, expected_type=type_hints["private_ip_address_enabled"])
            check_type(argname="argument remote_vnet_traffic_enabled", value=remote_vnet_traffic_enabled, expected_type=type_hints["remote_vnet_traffic_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_wan_traffic_enabled", value=virtual_wan_traffic_enabled, expected_type=type_hints["virtual_wan_traffic_enabled"])
            check_type(argname="argument vpn_client_configuration", value=vpn_client_configuration, expected_type=type_hints["vpn_client_configuration"])
            check_type(argname="argument vpn_type", value=vpn_type, expected_type=type_hints["vpn_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_configuration": ip_configuration,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku": sku,
            "type": type,
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
        if active_active is not None:
            self._values["active_active"] = active_active
        if bgp_route_translation_for_nat_enabled is not None:
            self._values["bgp_route_translation_for_nat_enabled"] = bgp_route_translation_for_nat_enabled
        if bgp_settings is not None:
            self._values["bgp_settings"] = bgp_settings
        if custom_route is not None:
            self._values["custom_route"] = custom_route
        if default_local_network_gateway_id is not None:
            self._values["default_local_network_gateway_id"] = default_local_network_gateway_id
        if dns_forwarding_enabled is not None:
            self._values["dns_forwarding_enabled"] = dns_forwarding_enabled
        if edge_zone is not None:
            self._values["edge_zone"] = edge_zone
        if enable_bgp is not None:
            self._values["enable_bgp"] = enable_bgp
        if generation is not None:
            self._values["generation"] = generation
        if id is not None:
            self._values["id"] = id
        if ip_sec_replay_protection_enabled is not None:
            self._values["ip_sec_replay_protection_enabled"] = ip_sec_replay_protection_enabled
        if policy_group is not None:
            self._values["policy_group"] = policy_group
        if private_ip_address_enabled is not None:
            self._values["private_ip_address_enabled"] = private_ip_address_enabled
        if remote_vnet_traffic_enabled is not None:
            self._values["remote_vnet_traffic_enabled"] = remote_vnet_traffic_enabled
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_wan_traffic_enabled is not None:
            self._values["virtual_wan_traffic_enabled"] = virtual_wan_traffic_enabled
        if vpn_client_configuration is not None:
            self._values["vpn_client_configuration"] = vpn_client_configuration
        if vpn_type is not None:
            self._values["vpn_type"] = vpn_type

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
    def ip_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayIpConfiguration"]]:
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_configuration VirtualNetworkGateway#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        assert result is not None, "Required property 'ip_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayIpConfiguration"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#location VirtualNetworkGateway#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#resource_group_name VirtualNetworkGateway#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sku VirtualNetworkGateway#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#type VirtualNetworkGateway#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#active_active VirtualNetworkGateway#active_active}.'''
        result = self._values.get("active_active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_route_translation_for_nat_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#bgp_route_translation_for_nat_enabled VirtualNetworkGateway#bgp_route_translation_for_nat_enabled}.'''
        result = self._values.get("bgp_route_translation_for_nat_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_settings(self) -> typing.Optional[VirtualNetworkGatewayBgpSettings]:
        '''bgp_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#bgp_settings VirtualNetworkGateway#bgp_settings}
        '''
        result = self._values.get("bgp_settings")
        return typing.cast(typing.Optional[VirtualNetworkGatewayBgpSettings], result)

    @builtins.property
    def custom_route(self) -> typing.Optional["VirtualNetworkGatewayCustomRoute"]:
        '''custom_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#custom_route VirtualNetworkGateway#custom_route}
        '''
        result = self._values.get("custom_route")
        return typing.cast(typing.Optional["VirtualNetworkGatewayCustomRoute"], result)

    @builtins.property
    def default_local_network_gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#default_local_network_gateway_id VirtualNetworkGateway#default_local_network_gateway_id}.'''
        result = self._values.get("default_local_network_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_forwarding_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#dns_forwarding_enabled VirtualNetworkGateway#dns_forwarding_enabled}.'''
        result = self._values.get("dns_forwarding_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def edge_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#edge_zone VirtualNetworkGateway#edge_zone}.'''
        result = self._values.get("edge_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_bgp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#enable_bgp VirtualNetworkGateway#enable_bgp}.'''
        result = self._values.get("enable_bgp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#generation VirtualNetworkGateway#generation}.'''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#id VirtualNetworkGateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_sec_replay_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ip_sec_replay_protection_enabled VirtualNetworkGateway#ip_sec_replay_protection_enabled}.'''
        result = self._values.get("ip_sec_replay_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroup"]]]:
        '''policy_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#policy_group VirtualNetworkGateway#policy_group}
        '''
        result = self._values.get("policy_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroup"]]], result)

    @builtins.property
    def private_ip_address_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#private_ip_address_enabled VirtualNetworkGateway#private_ip_address_enabled}.'''
        result = self._values.get("private_ip_address_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remote_vnet_traffic_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#remote_vnet_traffic_enabled VirtualNetworkGateway#remote_vnet_traffic_enabled}.'''
        result = self._values.get("remote_vnet_traffic_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#tags VirtualNetworkGateway#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VirtualNetworkGatewayTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#timeouts VirtualNetworkGateway#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VirtualNetworkGatewayTimeouts"], result)

    @builtins.property
    def virtual_wan_traffic_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#virtual_wan_traffic_enabled VirtualNetworkGateway#virtual_wan_traffic_enabled}.'''
        result = self._values.get("virtual_wan_traffic_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vpn_client_configuration(
        self,
    ) -> typing.Optional["VirtualNetworkGatewayVpnClientConfiguration"]:
        '''vpn_client_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_client_configuration VirtualNetworkGateway#vpn_client_configuration}
        '''
        result = self._values.get("vpn_client_configuration")
        return typing.cast(typing.Optional["VirtualNetworkGatewayVpnClientConfiguration"], result)

    @builtins.property
    def vpn_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_type VirtualNetworkGateway#vpn_type}.'''
        result = self._values.get("vpn_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayCustomRoute",
    jsii_struct_bases=[],
    name_mapping={"address_prefixes": "addressPrefixes"},
)
class VirtualNetworkGatewayCustomRoute:
    def __init__(
        self,
        *,
        address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_prefixes VirtualNetworkGateway#address_prefixes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94269eb0a0d1621124eada5695625751947511de51cdd029d8aa5f1da24ee39)
            check_type(argname="argument address_prefixes", value=address_prefixes, expected_type=type_hints["address_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address_prefixes is not None:
            self._values["address_prefixes"] = address_prefixes

    @builtins.property
    def address_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_prefixes VirtualNetworkGateway#address_prefixes}.'''
        result = self._values.get("address_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayCustomRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayCustomRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayCustomRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e567be0dc02fa61f843631bbc3d6d96da5ff26ca31d544c9e2c8bd1da4a3b3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressPrefixes")
    def reset_address_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressPrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="addressPrefixesInput")
    def address_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="addressPrefixes")
    def address_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressPrefixes"))

    @address_prefixes.setter
    def address_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d991d30ffff410fd4103089fbd2922719598c8ef727ba4dc83a75c891221034e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VirtualNetworkGatewayCustomRoute]:
        return typing.cast(typing.Optional[VirtualNetworkGatewayCustomRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualNetworkGatewayCustomRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9c2c87ce093bae0be8715dfb3a0dedce9cc8c84c8a57653133d30d2130b1f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_id": "subnetId",
        "name": "name",
        "private_ip_address_allocation": "privateIpAddressAllocation",
        "public_ip_address_id": "publicIpAddressId",
    },
)
class VirtualNetworkGatewayIpConfiguration:
    def __init__(
        self,
        *,
        subnet_id: builtins.str,
        name: typing.Optional[builtins.str] = None,
        private_ip_address_allocation: typing.Optional[builtins.str] = None,
        public_ip_address_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#subnet_id VirtualNetworkGateway#subnet_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param private_ip_address_allocation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#private_ip_address_allocation VirtualNetworkGateway#private_ip_address_allocation}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#public_ip_address_id VirtualNetworkGateway#public_ip_address_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e60357e7f9f9a4cbd9739f5e6861b86f79145ce4101fba054227d06456ef791)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument private_ip_address_allocation", value=private_ip_address_allocation, expected_type=type_hints["private_ip_address_allocation"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }
        if name is not None:
            self._values["name"] = name
        if private_ip_address_allocation is not None:
            self._values["private_ip_address_allocation"] = private_ip_address_allocation
        if public_ip_address_id is not None:
            self._values["public_ip_address_id"] = public_ip_address_id

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#subnet_id VirtualNetworkGateway#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_address_allocation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#private_ip_address_allocation VirtualNetworkGateway#private_ip_address_allocation}.'''
        result = self._values.get("private_ip_address_allocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ip_address_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#public_ip_address_id VirtualNetworkGateway#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayIpConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayIpConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5edda96bdb259f9e148e1c14ce7ed80a7f6c141e69cb6c20d52cd32febed46b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayIpConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d9d862f5283aadb9dd5ffcf813b7a37e64ce7c20c29ecc330d70c6cba85d70)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayIpConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76acf8c3928e0347c6771de278946e5f738235dcb75925d80c36a6b509d694b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb1bc5861cf27c9d91863fdc0cc45888afa913942afb0cc2466aae7805c86372)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9bf10c871687a3274d0fbce14245452355a76894ad574f9c684fc5cf9a24d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayIpConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayIpConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16deca02606b65c61a23dcb3bb4c2b21c047a186a06ce2e2e7b89c5d2e752ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bff8503cb64940744e5798a441de1152a4ddf5082815a0e9b5633a701c481e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPrivateIpAddressAllocation")
    def reset_private_ip_address_allocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAddressAllocation", []))

    @jsii.member(jsii_name="resetPublicIpAddressId")
    def reset_public_ip_address_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpAddressId", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocationInput")
    def private_ip_address_allocation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressAllocationInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIdInput")
    def public_ip_address_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpAddressIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ece67b7ba42fa2ee7138f30d1726fde6b0ea4c5554522a0948bc61a58d4f25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddressAllocation"))

    @private_ip_address_allocation.setter
    def private_ip_address_allocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd42336cad67bd5efc8660e3807b5484c61b590e6f46d040ad475cbad1aab1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddressAllocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb5bd46ed489c81ed81a84bcc5517b22f2729ccbbe00f214c7966e2af99b35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c310bb738a42717b232bd3c17af732566695020bca7307b8ed9fbe2c693b0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayIpConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayIpConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayIpConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1176efb9bffc085472cd282a63bae88dcf6036c645f4e1260eba32470d5728e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayPolicyGroup",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "policy_member": "policyMember",
        "is_default": "isDefault",
        "priority": "priority",
    },
)
class VirtualNetworkGatewayPolicyGroup:
    def __init__(
        self,
        *,
        name: builtins.str,
        policy_member: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayPolicyGroupPolicyMember", typing.Dict[builtins.str, typing.Any]]]],
        is_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param policy_member: policy_member block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#policy_member VirtualNetworkGateway#policy_member}
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#is_default VirtualNetworkGateway#is_default}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#priority VirtualNetworkGateway#priority}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d1b01f119eb72eb8869ab62743a92ec4a52204e8eb7fd9e9190d8612ac83c9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_member", value=policy_member, expected_type=type_hints["policy_member"])
            check_type(argname="argument is_default", value=is_default, expected_type=type_hints["is_default"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_member": policy_member,
        }
        if is_default is not None:
            self._values["is_default"] = is_default
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_member(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroupPolicyMember"]]:
        '''policy_member block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#policy_member VirtualNetworkGateway#policy_member}
        '''
        result = self._values.get("policy_member")
        assert result is not None, "Required property 'policy_member' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroupPolicyMember"]], result)

    @builtins.property
    def is_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#is_default VirtualNetworkGateway#is_default}.'''
        result = self._values.get("is_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#priority VirtualNetworkGateway#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayPolicyGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayPolicyGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayPolicyGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb01333399ecfd3c38493882d6db94611ea41fbfdc6ffeaa6834e4398b3507c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayPolicyGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67733d05e9522bea8b62922eb73bdaa83a21246cfe9fd50496825ef7fa8870c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayPolicyGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c68dc75c186f11761dc7af976adab3f8f8ea8e889d535593f3c185cebbb75d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90b9e00a411652b8e5327c3c4f596caafbe4b0ec2c937882db07c682dcfda577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99788ecaaed3d124ea9540e164e8a72b6fd01fbce5cf757be69d7f74dd256969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2390ad8f48d9226d40e18e2463e64d18f4abdf2accfc06e654bd79ea9c592b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayPolicyGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayPolicyGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e4b995bfe53eb8d7275cdf55ca7e2532294be9364ff2dd25d4148f163dde47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicyMember")
    def put_policy_member(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayPolicyGroupPolicyMember", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a288f44584d8b12e33dd21cec40caa31c8747ab3a0a821c8233fe5d7f5051370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyMember", [value]))

    @jsii.member(jsii_name="resetIsDefault")
    def reset_is_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsDefault", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @builtins.property
    @jsii.member(jsii_name="policyMember")
    def policy_member(self) -> "VirtualNetworkGatewayPolicyGroupPolicyMemberList":
        return typing.cast("VirtualNetworkGatewayPolicyGroupPolicyMemberList", jsii.get(self, "policyMember"))

    @builtins.property
    @jsii.member(jsii_name="isDefaultInput")
    def is_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyMemberInput")
    def policy_member_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroupPolicyMember"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayPolicyGroupPolicyMember"]]], jsii.get(self, "policyMemberInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDefault"))

    @is_default.setter
    def is_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04f14441c1e8b9d30184a9ef41f473099c3fd14ae00a883dbc7ebfd0ada953d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d701776b9495e52de73fe94280ce9c695dd047b09e2482d07782def3cab97662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483d9a33b1751622aaee570a05393e80b895e4584f507a9a361c78126c299431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f2aa5544664cff0ddc4daf1d645d6df1fde62eba0a4b268af3bc817edd0529a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayPolicyGroupPolicyMember",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "value": "value"},
)
class VirtualNetworkGatewayPolicyGroupPolicyMember:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#type VirtualNetworkGateway#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#value VirtualNetworkGateway#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d3f01716772c2bcbbca28f81b85129df0404e1de317c55b30dea703e73ce02)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#type VirtualNetworkGateway#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#value VirtualNetworkGateway#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayPolicyGroupPolicyMember(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayPolicyGroupPolicyMemberList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayPolicyGroupPolicyMemberList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25d7ce40424c51769078584a309c3171cb94b2ba1713b43842874db9d67712ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayPolicyGroupPolicyMemberOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af27bce9c617ecbf3e983bdcaa565b119e47fd3c643c4f0473475ffc5751541)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayPolicyGroupPolicyMemberOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce3c6464b91d630b93caa909b618f91904e04c63ad242742522f05523ca4e74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ce4ba3918740e7dcc44d70476c42500eef59559ab4c25d56fb1b8849bcb1a9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a793dfd702d86a804a6d9c7f5ba2edb04182508f93c94a6e33f24a075ba157cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroupPolicyMember]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroupPolicyMember]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroupPolicyMember]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abea69bfb2debc7ddd58b3a0c25988c6dac8310e10df59e74a4e9ec87e47b6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayPolicyGroupPolicyMemberOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayPolicyGroupPolicyMemberOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a75d1b373baf8ed0be420804d1e991d973409aab61396acc94dcca4fb2220b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e957853ab36faf589abd69045f25da93608c5a41d8ecee6e9d2e3327f6a17eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6caa508a911f94b69891c24f81ea07904a9b24c7e548291868134c859460e0e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a474fdb4dde58f9e328529d4652b4e07b32ad07d999c7f821e8e2bf3ce147e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroupPolicyMember]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroupPolicyMember]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroupPolicyMember]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321b5b72acdeb364c1faf12e7a591510e0d02731f2369221d37b39931c7fb4f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VirtualNetworkGatewayTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#create VirtualNetworkGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#delete VirtualNetworkGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#read VirtualNetworkGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#update VirtualNetworkGateway#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedab3d10c3d9b2a32302d2ae0238eabe16448f95b70dd6cb003177134695a08)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#create VirtualNetworkGateway#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#delete VirtualNetworkGateway#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#read VirtualNetworkGateway#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#update VirtualNetworkGateway#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf4c00f44afc23539473cac33f5edbc7034584844c4f419db1dc946591342740)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ab56d48c9c9dd31ecbc0bcfcdfd05a50d826378beab08802640c79ee845f15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0970f1a592e5b8977d9d4455639df496c4ab76271e8d64b7f767bfc37200b543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49529f7258a4f0890739aa31b4f00c422f962f8de3b54b4ba2ac5b37b7946284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da567105ce95c82476336d3d3f2b90bd61ac8756cbc19ec749b7d454e2e2211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6b1ba47c60f318392e2f61bedb40583ba57dd9f28b27c489fa05212061a0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "address_space": "addressSpace",
        "aad_audience": "aadAudience",
        "aad_issuer": "aadIssuer",
        "aad_tenant": "aadTenant",
        "ipsec_policy": "ipsecPolicy",
        "radius_server": "radiusServer",
        "radius_server_address": "radiusServerAddress",
        "radius_server_secret": "radiusServerSecret",
        "revoked_certificate": "revokedCertificate",
        "root_certificate": "rootCertificate",
        "virtual_network_gateway_client_connection": "virtualNetworkGatewayClientConnection",
        "vpn_auth_types": "vpnAuthTypes",
        "vpn_client_protocols": "vpnClientProtocols",
    },
)
class VirtualNetworkGatewayVpnClientConfiguration:
    def __init__(
        self,
        *,
        address_space: typing.Sequence[builtins.str],
        aad_audience: typing.Optional[builtins.str] = None,
        aad_issuer: typing.Optional[builtins.str] = None,
        aad_tenant: typing.Optional[builtins.str] = None,
        ipsec_policy: typing.Optional[typing.Union["VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        radius_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRadiusServer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        radius_server_address: typing.Optional[builtins.str] = None,
        radius_server_secret: typing.Optional[builtins.str] = None,
        revoked_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        root_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRootCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        virtual_network_gateway_client_connection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpn_auth_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpn_client_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param address_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_space VirtualNetworkGateway#address_space}.
        :param aad_audience: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_audience VirtualNetworkGateway#aad_audience}.
        :param aad_issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_issuer VirtualNetworkGateway#aad_issuer}.
        :param aad_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_tenant VirtualNetworkGateway#aad_tenant}.
        :param ipsec_policy: ipsec_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_policy VirtualNetworkGateway#ipsec_policy}
        :param radius_server: radius_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server VirtualNetworkGateway#radius_server}
        :param radius_server_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server_address VirtualNetworkGateway#radius_server_address}.
        :param radius_server_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server_secret VirtualNetworkGateway#radius_server_secret}.
        :param revoked_certificate: revoked_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#revoked_certificate VirtualNetworkGateway#revoked_certificate}
        :param root_certificate: root_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#root_certificate VirtualNetworkGateway#root_certificate}
        :param virtual_network_gateway_client_connection: virtual_network_gateway_client_connection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#virtual_network_gateway_client_connection VirtualNetworkGateway#virtual_network_gateway_client_connection}
        :param vpn_auth_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_auth_types VirtualNetworkGateway#vpn_auth_types}.
        :param vpn_client_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_client_protocols VirtualNetworkGateway#vpn_client_protocols}.
        '''
        if isinstance(ipsec_policy, dict):
            ipsec_policy = VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy(**ipsec_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff55421c4ce9d5094966f80d343acc35417dd9b91afb9e683ef97afc828fef9f)
            check_type(argname="argument address_space", value=address_space, expected_type=type_hints["address_space"])
            check_type(argname="argument aad_audience", value=aad_audience, expected_type=type_hints["aad_audience"])
            check_type(argname="argument aad_issuer", value=aad_issuer, expected_type=type_hints["aad_issuer"])
            check_type(argname="argument aad_tenant", value=aad_tenant, expected_type=type_hints["aad_tenant"])
            check_type(argname="argument ipsec_policy", value=ipsec_policy, expected_type=type_hints["ipsec_policy"])
            check_type(argname="argument radius_server", value=radius_server, expected_type=type_hints["radius_server"])
            check_type(argname="argument radius_server_address", value=radius_server_address, expected_type=type_hints["radius_server_address"])
            check_type(argname="argument radius_server_secret", value=radius_server_secret, expected_type=type_hints["radius_server_secret"])
            check_type(argname="argument revoked_certificate", value=revoked_certificate, expected_type=type_hints["revoked_certificate"])
            check_type(argname="argument root_certificate", value=root_certificate, expected_type=type_hints["root_certificate"])
            check_type(argname="argument virtual_network_gateway_client_connection", value=virtual_network_gateway_client_connection, expected_type=type_hints["virtual_network_gateway_client_connection"])
            check_type(argname="argument vpn_auth_types", value=vpn_auth_types, expected_type=type_hints["vpn_auth_types"])
            check_type(argname="argument vpn_client_protocols", value=vpn_client_protocols, expected_type=type_hints["vpn_client_protocols"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_space": address_space,
        }
        if aad_audience is not None:
            self._values["aad_audience"] = aad_audience
        if aad_issuer is not None:
            self._values["aad_issuer"] = aad_issuer
        if aad_tenant is not None:
            self._values["aad_tenant"] = aad_tenant
        if ipsec_policy is not None:
            self._values["ipsec_policy"] = ipsec_policy
        if radius_server is not None:
            self._values["radius_server"] = radius_server
        if radius_server_address is not None:
            self._values["radius_server_address"] = radius_server_address
        if radius_server_secret is not None:
            self._values["radius_server_secret"] = radius_server_secret
        if revoked_certificate is not None:
            self._values["revoked_certificate"] = revoked_certificate
        if root_certificate is not None:
            self._values["root_certificate"] = root_certificate
        if virtual_network_gateway_client_connection is not None:
            self._values["virtual_network_gateway_client_connection"] = virtual_network_gateway_client_connection
        if vpn_auth_types is not None:
            self._values["vpn_auth_types"] = vpn_auth_types
        if vpn_client_protocols is not None:
            self._values["vpn_client_protocols"] = vpn_client_protocols

    @builtins.property
    def address_space(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_space VirtualNetworkGateway#address_space}.'''
        result = self._values.get("address_space")
        assert result is not None, "Required property 'address_space' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def aad_audience(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_audience VirtualNetworkGateway#aad_audience}.'''
        result = self._values.get("aad_audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aad_issuer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_issuer VirtualNetworkGateway#aad_issuer}.'''
        result = self._values.get("aad_issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aad_tenant(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#aad_tenant VirtualNetworkGateway#aad_tenant}.'''
        result = self._values.get("aad_tenant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipsec_policy(
        self,
    ) -> typing.Optional["VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy"]:
        '''ipsec_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_policy VirtualNetworkGateway#ipsec_policy}
        '''
        result = self._values.get("ipsec_policy")
        return typing.cast(typing.Optional["VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy"], result)

    @builtins.property
    def radius_server(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRadiusServer"]]]:
        '''radius_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server VirtualNetworkGateway#radius_server}
        '''
        result = self._values.get("radius_server")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRadiusServer"]]], result)

    @builtins.property
    def radius_server_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server_address VirtualNetworkGateway#radius_server_address}.'''
        result = self._values.get("radius_server_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def radius_server_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#radius_server_secret VirtualNetworkGateway#radius_server_secret}.'''
        result = self._values.get("radius_server_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revoked_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate"]]]:
        '''revoked_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#revoked_certificate VirtualNetworkGateway#revoked_certificate}
        '''
        result = self._values.get("revoked_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate"]]], result)

    @builtins.property
    def root_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRootCertificate"]]]:
        '''root_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#root_certificate VirtualNetworkGateway#root_certificate}
        '''
        result = self._values.get("root_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRootCertificate"]]], result)

    @builtins.property
    def virtual_network_gateway_client_connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection"]]]:
        '''virtual_network_gateway_client_connection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#virtual_network_gateway_client_connection VirtualNetworkGateway#virtual_network_gateway_client_connection}
        '''
        result = self._values.get("virtual_network_gateway_client_connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection"]]], result)

    @builtins.property
    def vpn_auth_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_auth_types VirtualNetworkGateway#vpn_auth_types}.'''
        result = self._values.get("vpn_auth_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpn_client_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#vpn_client_protocols VirtualNetworkGateway#vpn_client_protocols}.'''
        result = self._values.get("vpn_client_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayVpnClientConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "dh_group": "dhGroup",
        "ike_encryption": "ikeEncryption",
        "ike_integrity": "ikeIntegrity",
        "ipsec_encryption": "ipsecEncryption",
        "ipsec_integrity": "ipsecIntegrity",
        "pfs_group": "pfsGroup",
        "sa_data_size_in_kilobytes": "saDataSizeInKilobytes",
        "sa_lifetime_in_seconds": "saLifetimeInSeconds",
    },
)
class VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy:
    def __init__(
        self,
        *,
        dh_group: builtins.str,
        ike_encryption: builtins.str,
        ike_integrity: builtins.str,
        ipsec_encryption: builtins.str,
        ipsec_integrity: builtins.str,
        pfs_group: builtins.str,
        sa_data_size_in_kilobytes: jsii.Number,
        sa_lifetime_in_seconds: jsii.Number,
    ) -> None:
        '''
        :param dh_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#dh_group VirtualNetworkGateway#dh_group}.
        :param ike_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ike_encryption VirtualNetworkGateway#ike_encryption}.
        :param ike_integrity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ike_integrity VirtualNetworkGateway#ike_integrity}.
        :param ipsec_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_encryption VirtualNetworkGateway#ipsec_encryption}.
        :param ipsec_integrity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_integrity VirtualNetworkGateway#ipsec_integrity}.
        :param pfs_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#pfs_group VirtualNetworkGateway#pfs_group}.
        :param sa_data_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sa_data_size_in_kilobytes VirtualNetworkGateway#sa_data_size_in_kilobytes}.
        :param sa_lifetime_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sa_lifetime_in_seconds VirtualNetworkGateway#sa_lifetime_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47305235420e91bf95271cde88593f6c67aa4d2fa2e99b7aedda59acace3e13)
            check_type(argname="argument dh_group", value=dh_group, expected_type=type_hints["dh_group"])
            check_type(argname="argument ike_encryption", value=ike_encryption, expected_type=type_hints["ike_encryption"])
            check_type(argname="argument ike_integrity", value=ike_integrity, expected_type=type_hints["ike_integrity"])
            check_type(argname="argument ipsec_encryption", value=ipsec_encryption, expected_type=type_hints["ipsec_encryption"])
            check_type(argname="argument ipsec_integrity", value=ipsec_integrity, expected_type=type_hints["ipsec_integrity"])
            check_type(argname="argument pfs_group", value=pfs_group, expected_type=type_hints["pfs_group"])
            check_type(argname="argument sa_data_size_in_kilobytes", value=sa_data_size_in_kilobytes, expected_type=type_hints["sa_data_size_in_kilobytes"])
            check_type(argname="argument sa_lifetime_in_seconds", value=sa_lifetime_in_seconds, expected_type=type_hints["sa_lifetime_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dh_group": dh_group,
            "ike_encryption": ike_encryption,
            "ike_integrity": ike_integrity,
            "ipsec_encryption": ipsec_encryption,
            "ipsec_integrity": ipsec_integrity,
            "pfs_group": pfs_group,
            "sa_data_size_in_kilobytes": sa_data_size_in_kilobytes,
            "sa_lifetime_in_seconds": sa_lifetime_in_seconds,
        }

    @builtins.property
    def dh_group(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#dh_group VirtualNetworkGateway#dh_group}.'''
        result = self._values.get("dh_group")
        assert result is not None, "Required property 'dh_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ike_encryption(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ike_encryption VirtualNetworkGateway#ike_encryption}.'''
        result = self._values.get("ike_encryption")
        assert result is not None, "Required property 'ike_encryption' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ike_integrity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ike_integrity VirtualNetworkGateway#ike_integrity}.'''
        result = self._values.get("ike_integrity")
        assert result is not None, "Required property 'ike_integrity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipsec_encryption(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_encryption VirtualNetworkGateway#ipsec_encryption}.'''
        result = self._values.get("ipsec_encryption")
        assert result is not None, "Required property 'ipsec_encryption' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipsec_integrity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_integrity VirtualNetworkGateway#ipsec_integrity}.'''
        result = self._values.get("ipsec_integrity")
        assert result is not None, "Required property 'ipsec_integrity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pfs_group(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#pfs_group VirtualNetworkGateway#pfs_group}.'''
        result = self._values.get("pfs_group")
        assert result is not None, "Required property 'pfs_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sa_data_size_in_kilobytes(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sa_data_size_in_kilobytes VirtualNetworkGateway#sa_data_size_in_kilobytes}.'''
        result = self._values.get("sa_data_size_in_kilobytes")
        assert result is not None, "Required property 'sa_data_size_in_kilobytes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sa_lifetime_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sa_lifetime_in_seconds VirtualNetworkGateway#sa_lifetime_in_seconds}.'''
        result = self._values.get("sa_lifetime_in_seconds")
        assert result is not None, "Required property 'sa_lifetime_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayVpnClientConfigurationIpsecPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationIpsecPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d948ba8c0281659acaeeff419fd97992bb9b0a8dc599ff3dadff4758b0779e60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dhGroupInput")
    def dh_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dhGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeEncryptionInput")
    def ike_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ikeEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeIntegrityInput")
    def ike_integrity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ikeIntegrityInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsecEncryptionInput")
    def ipsec_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipsecEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsecIntegrityInput")
    def ipsec_integrity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipsecIntegrityInput"))

    @builtins.property
    @jsii.member(jsii_name="pfsGroupInput")
    def pfs_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pfsGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="saDataSizeInKilobytesInput")
    def sa_data_size_in_kilobytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "saDataSizeInKilobytesInput"))

    @builtins.property
    @jsii.member(jsii_name="saLifetimeInSecondsInput")
    def sa_lifetime_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "saLifetimeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="dhGroup")
    def dh_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dhGroup"))

    @dh_group.setter
    def dh_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccb27d448a45d9086d80426a028eceec4325e8ca6ff3e0af9b23c6d5774b2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dhGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ikeEncryption")
    def ike_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeEncryption"))

    @ike_encryption.setter
    def ike_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8adc1d94e2df7428e47b11e569b4e71e2d00588fc9c7ad8a272e79891c4a52f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ikeIntegrity")
    def ike_integrity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeIntegrity"))

    @ike_integrity.setter
    def ike_integrity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4869b79b94e69b9dd8b0fbccfe08a6ee0ff0c3d9178e666b12ffd7130a5f1e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeIntegrity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipsecEncryption")
    def ipsec_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipsecEncryption"))

    @ipsec_encryption.setter
    def ipsec_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273faf93913e72fd084023a397d09dc7061d7f009a86d197e6736eefbc55e2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipsecEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipsecIntegrity")
    def ipsec_integrity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipsecIntegrity"))

    @ipsec_integrity.setter
    def ipsec_integrity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7193b6ea1d675bdef7567fe9bd1b2af9e5770c9958d13c943c689db4ba4379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipsecIntegrity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pfsGroup")
    def pfs_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pfsGroup"))

    @pfs_group.setter
    def pfs_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb51b5a329816e8dc2373e0c8bc2c5a18c24f72a3b6a084c7f2c85b8b6c1942f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pfsGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saDataSizeInKilobytes")
    def sa_data_size_in_kilobytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "saDataSizeInKilobytes"))

    @sa_data_size_in_kilobytes.setter
    def sa_data_size_in_kilobytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda0e86236fc939d3e695491318809932f8b58e198a3f17e45a7df085a11ae68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saDataSizeInKilobytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saLifetimeInSeconds")
    def sa_lifetime_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "saLifetimeInSeconds"))

    @sa_lifetime_in_seconds.setter
    def sa_lifetime_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f60d27e00b857ff3a7b8024a128db74cd72f77ad60ca80bf0876db04163fad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saLifetimeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy]:
        return typing.cast(typing.Optional[VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4077d02273a7709977fd49fb0c46ae657d383be277a5f7e42013f41af541e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayVpnClientConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbfdee106a19e96f7ef0b3266d3966083011a91b2e871294d87a632a766c2dce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpsecPolicy")
    def put_ipsec_policy(
        self,
        *,
        dh_group: builtins.str,
        ike_encryption: builtins.str,
        ike_integrity: builtins.str,
        ipsec_encryption: builtins.str,
        ipsec_integrity: builtins.str,
        pfs_group: builtins.str,
        sa_data_size_in_kilobytes: jsii.Number,
        sa_lifetime_in_seconds: jsii.Number,
    ) -> None:
        '''
        :param dh_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#dh_group VirtualNetworkGateway#dh_group}.
        :param ike_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ike_encryption VirtualNetworkGateway#ike_encryption}.
        :param ike_integrity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ike_integrity VirtualNetworkGateway#ike_integrity}.
        :param ipsec_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_encryption VirtualNetworkGateway#ipsec_encryption}.
        :param ipsec_integrity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#ipsec_integrity VirtualNetworkGateway#ipsec_integrity}.
        :param pfs_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#pfs_group VirtualNetworkGateway#pfs_group}.
        :param sa_data_size_in_kilobytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sa_data_size_in_kilobytes VirtualNetworkGateway#sa_data_size_in_kilobytes}.
        :param sa_lifetime_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#sa_lifetime_in_seconds VirtualNetworkGateway#sa_lifetime_in_seconds}.
        '''
        value = VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy(
            dh_group=dh_group,
            ike_encryption=ike_encryption,
            ike_integrity=ike_integrity,
            ipsec_encryption=ipsec_encryption,
            ipsec_integrity=ipsec_integrity,
            pfs_group=pfs_group,
            sa_data_size_in_kilobytes=sa_data_size_in_kilobytes,
            sa_lifetime_in_seconds=sa_lifetime_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putIpsecPolicy", [value]))

    @jsii.member(jsii_name="putRadiusServer")
    def put_radius_server(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRadiusServer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe61dbdf7791699d6ea19c4f7cf28fc65b2d91a584642746d0a07df3058973d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRadiusServer", [value]))

    @jsii.member(jsii_name="putRevokedCertificate")
    def put_revoked_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297df67cf4746af56933f13f6dbb22d42b076a7cfd3c366f97fc857c1eaa42c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRevokedCertificate", [value]))

    @jsii.member(jsii_name="putRootCertificate")
    def put_root_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationRootCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05be996eca6b0d84740253462645f6a8ed9774a07898299caba3ae19f6147007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRootCertificate", [value]))

    @jsii.member(jsii_name="putVirtualNetworkGatewayClientConnection")
    def put_virtual_network_gateway_client_connection(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c6dccc4ebaa4030ee95e412c56a0d325e1a1754801c806bacabf0d55cec4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVirtualNetworkGatewayClientConnection", [value]))

    @jsii.member(jsii_name="resetAadAudience")
    def reset_aad_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAadAudience", []))

    @jsii.member(jsii_name="resetAadIssuer")
    def reset_aad_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAadIssuer", []))

    @jsii.member(jsii_name="resetAadTenant")
    def reset_aad_tenant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAadTenant", []))

    @jsii.member(jsii_name="resetIpsecPolicy")
    def reset_ipsec_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpsecPolicy", []))

    @jsii.member(jsii_name="resetRadiusServer")
    def reset_radius_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRadiusServer", []))

    @jsii.member(jsii_name="resetRadiusServerAddress")
    def reset_radius_server_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRadiusServerAddress", []))

    @jsii.member(jsii_name="resetRadiusServerSecret")
    def reset_radius_server_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRadiusServerSecret", []))

    @jsii.member(jsii_name="resetRevokedCertificate")
    def reset_revoked_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevokedCertificate", []))

    @jsii.member(jsii_name="resetRootCertificate")
    def reset_root_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootCertificate", []))

    @jsii.member(jsii_name="resetVirtualNetworkGatewayClientConnection")
    def reset_virtual_network_gateway_client_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkGatewayClientConnection", []))

    @jsii.member(jsii_name="resetVpnAuthTypes")
    def reset_vpn_auth_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnAuthTypes", []))

    @jsii.member(jsii_name="resetVpnClientProtocols")
    def reset_vpn_client_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnClientProtocols", []))

    @builtins.property
    @jsii.member(jsii_name="ipsecPolicy")
    def ipsec_policy(
        self,
    ) -> VirtualNetworkGatewayVpnClientConfigurationIpsecPolicyOutputReference:
        return typing.cast(VirtualNetworkGatewayVpnClientConfigurationIpsecPolicyOutputReference, jsii.get(self, "ipsecPolicy"))

    @builtins.property
    @jsii.member(jsii_name="radiusServer")
    def radius_server(
        self,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationRadiusServerList":
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationRadiusServerList", jsii.get(self, "radiusServer"))

    @builtins.property
    @jsii.member(jsii_name="revokedCertificate")
    def revoked_certificate(
        self,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateList":
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateList", jsii.get(self, "revokedCertificate"))

    @builtins.property
    @jsii.member(jsii_name="rootCertificate")
    def root_certificate(
        self,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationRootCertificateList":
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationRootCertificateList", jsii.get(self, "rootCertificate"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkGatewayClientConnection")
    def virtual_network_gateway_client_connection(
        self,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionList":
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionList", jsii.get(self, "virtualNetworkGatewayClientConnection"))

    @builtins.property
    @jsii.member(jsii_name="aadAudienceInput")
    def aad_audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aadAudienceInput"))

    @builtins.property
    @jsii.member(jsii_name="aadIssuerInput")
    def aad_issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aadIssuerInput"))

    @builtins.property
    @jsii.member(jsii_name="aadTenantInput")
    def aad_tenant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aadTenantInput"))

    @builtins.property
    @jsii.member(jsii_name="addressSpaceInput")
    def address_space_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressSpaceInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsecPolicyInput")
    def ipsec_policy_input(
        self,
    ) -> typing.Optional[VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy]:
        return typing.cast(typing.Optional[VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy], jsii.get(self, "ipsecPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="radiusServerAddressInput")
    def radius_server_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "radiusServerAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="radiusServerInput")
    def radius_server_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRadiusServer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRadiusServer"]]], jsii.get(self, "radiusServerInput"))

    @builtins.property
    @jsii.member(jsii_name="radiusServerSecretInput")
    def radius_server_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "radiusServerSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="revokedCertificateInput")
    def revoked_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate"]]], jsii.get(self, "revokedCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="rootCertificateInput")
    def root_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRootCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationRootCertificate"]]], jsii.get(self, "rootCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkGatewayClientConnectionInput")
    def virtual_network_gateway_client_connection_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection"]]], jsii.get(self, "virtualNetworkGatewayClientConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnAuthTypesInput")
    def vpn_auth_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpnAuthTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnClientProtocolsInput")
    def vpn_client_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpnClientProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="aadAudience")
    def aad_audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aadAudience"))

    @aad_audience.setter
    def aad_audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091c25d06e28b6cf2d56a2b494b94146fde835078d37b1328ec731d673cb48ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aadAudience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aadIssuer")
    def aad_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aadIssuer"))

    @aad_issuer.setter
    def aad_issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35078ef57a72f736820efcd6bcb52d5037d66602d2c65e2c9595befa737e34c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aadIssuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aadTenant")
    def aad_tenant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aadTenant"))

    @aad_tenant.setter
    def aad_tenant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9871be7cb90ad6235fab9c56768787909ec81d6221c741add371a9ce5f563e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aadTenant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressSpace")
    def address_space(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressSpace"))

    @address_space.setter
    def address_space(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa1d3e210baf3d390125a64b8666b603c475412b2b75fd76f5032481c8420f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressSpace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="radiusServerAddress")
    def radius_server_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "radiusServerAddress"))

    @radius_server_address.setter
    def radius_server_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29dff5fd51cfc30de2ca10d375cc8525767545968b6d62059ed3dc26fe99a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "radiusServerAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="radiusServerSecret")
    def radius_server_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "radiusServerSecret"))

    @radius_server_secret.setter
    def radius_server_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d199f7307fedfe2897ce7b77ee64648c2a424a177ca6ac7b15f5aa263608f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "radiusServerSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnAuthTypes")
    def vpn_auth_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpnAuthTypes"))

    @vpn_auth_types.setter
    def vpn_auth_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c284caabe62b5ee4f2df7311abcd18d8412dc45316762a75362d0224a1811d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnAuthTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnClientProtocols")
    def vpn_client_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpnClientProtocols"))

    @vpn_client_protocols.setter
    def vpn_client_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c797ac2ff6c5c56b375912adf20ffd3080140ed793c750635ce1ea755c45066a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnClientProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualNetworkGatewayVpnClientConfiguration]:
        return typing.cast(typing.Optional[VirtualNetworkGatewayVpnClientConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualNetworkGatewayVpnClientConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e6386cf66bc5f0a9845792885375cc11add39a0024eb5ac84613db9b82be8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRadiusServer",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "score": "score", "secret": "secret"},
)
class VirtualNetworkGatewayVpnClientConfigurationRadiusServer:
    def __init__(
        self,
        *,
        address: builtins.str,
        score: jsii.Number,
        secret: builtins.str,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address VirtualNetworkGateway#address}.
        :param score: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#score VirtualNetworkGateway#score}.
        :param secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#secret VirtualNetworkGateway#secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5025d56e1344ffcf4ae4b4899a1a907090b8f71e95f707e9f19e40d437a4e0f9)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "score": score,
            "secret": secret,
        }

    @builtins.property
    def address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address VirtualNetworkGateway#address}.'''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def score(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#score VirtualNetworkGateway#score}.'''
        result = self._values.get("score")
        assert result is not None, "Required property 'score' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#secret VirtualNetworkGateway#secret}.'''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayVpnClientConfigurationRadiusServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayVpnClientConfigurationRadiusServerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRadiusServerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63e4c2c49a6a101e14ebe855faa8a6cd3acd40d823eed6308ba4486c4da55bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationRadiusServerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5ad59eb42c02d5537c155a0be41b0c54907e62c5ec91b395cee32d8a999805)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationRadiusServerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e760bc3e098e548af0de4a4b87bf36af81a90eec6b8d3516f3f5e82a82d7909)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2992d7733c62ab72a32f3b45d5ce41701544d68eb78fe5144a2724f603475eed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f69a47e470755c2799ddc7252ac81fe9d5a4d96c169d51e884e032dca940ead6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRadiusServer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRadiusServer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRadiusServer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478a4dfa0e25fc0bcb63a7a9e789f52d93b0d50296a8206935be838543499802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayVpnClientConfigurationRadiusServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRadiusServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af7fa3cb84c892ca8df555cce40ddf056b96da16c9d952efc433ad8f3c38bd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105031ad20d676361e7aad463f707252a477dfe3300f794798a1bdff86c2ef34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "score"))

    @score.setter
    def score(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7077b9a6b391444f268355db6e0acf413102a5b54eb5380618784e9b6131a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd52f27d3be986cc7676922032f417dd2aa6e0495b89c38dc5fa6d2c34f9eabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRadiusServer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRadiusServer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRadiusServer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f00047097db75f7092394fa51e5b5ccedb183d8d164a4cc16b624d5cfa4bab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "thumbprint": "thumbprint"},
)
class VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate:
    def __init__(self, *, name: builtins.str, thumbprint: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#thumbprint VirtualNetworkGateway#thumbprint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8f7e63a6ffbab29fedec9bab96395eaa61afce693eb8a428e29fbd5672d929)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "thumbprint": thumbprint,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def thumbprint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#thumbprint VirtualNetworkGateway#thumbprint}.'''
        result = self._values.get("thumbprint")
        assert result is not None, "Required property 'thumbprint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12acf5fe13af21c1e1ad8ae96a8adb554499d714e9d4c49eb496ff6c0cd53379)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28bc6f33ac20bb0cff1a282b252cb96a771aa2833a95984b4fdad99665f70d73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea56519a41403e5fa13fb5c4baf9a1bb4e006261006d62286529ab09740a8132)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3477c13f9f2c71febb60eddf97e35f73ade3962cc9f2dbb8207cc31e0be7500)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed7b5dd280cb20c98112029039d3e57c1e79cb3d94ce797b29d804d10761a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c9f5e49e61fce7fd41a944d9f26b0c0eb076320e5662a37f1b2b6016fa543f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97c97b447288c29301058acb6a72ed399ce81bf324c3f30242a2079b6cc70b11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98f9ba1f21a54466e197a572b9e9808a671f74b00564028e85f31cdf27240eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91665f1fd80564c1247035dc4794ca5ebe655e39693ebda310240ab10581dcd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2345e60a0a78bef6509e23d4925bb440cc7a9ff1ff8dd0b44538ab092509149a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRootCertificate",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "public_cert_data": "publicCertData"},
)
class VirtualNetworkGatewayVpnClientConfigurationRootCertificate:
    def __init__(self, *, name: builtins.str, public_cert_data: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param public_cert_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#public_cert_data VirtualNetworkGateway#public_cert_data}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6a3d8dc27ba7957603268de4e7875549709277fd6a9469d1a2d7e339afae3e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_cert_data", value=public_cert_data, expected_type=type_hints["public_cert_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "public_cert_data": public_cert_data,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public_cert_data(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#public_cert_data VirtualNetworkGateway#public_cert_data}.'''
        result = self._values.get("public_cert_data")
        assert result is not None, "Required property 'public_cert_data' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayVpnClientConfigurationRootCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayVpnClientConfigurationRootCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRootCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b5735c09e0e3236e65ce87977912291e175cbb3730b17bb8e2bca44e6b8bb66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationRootCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544f0ebbfee4838bad254a3fe041fcf0668d359420f0aa5450368188188306ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationRootCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685d0b8cfdd8bbdb35242414ed7f4fa848e8f4e389189828b1aca287f3ff262a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df825e2417b6df3c02c6e2c023fd0bf14b92fbaf7107ee904d6da7e4ae2880b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f4aae125df40016af6502d5e8d42990cdd4dc778121b7c533914421fdf0516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRootCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRootCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRootCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de36b4c0454010955bb9b362417aeb5a7d16b1f5a9a5d23884bb9b4986657ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayVpnClientConfigurationRootCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationRootCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb26ece8ea8bff05fc255b2c27d1b255d951aec1a822a0bfb7b23a7fd410a6db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicCertDataInput")
    def public_cert_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicCertDataInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279e88189f9fe530fdb3a90f6d75de39dd3eb0bd524829bc257ec178f1f31af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicCertData")
    def public_cert_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicCertData"))

    @public_cert_data.setter
    def public_cert_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536cf7854b31583527d5871a6830d2e7102b7064a5035818580e7d82f0893025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicCertData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRootCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRootCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRootCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a49cd9a179e971cbf2d43e7d2e7dee3b7cf77ab1c37010cd841cdf12b228193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection",
    jsii_struct_bases=[],
    name_mapping={
        "address_prefixes": "addressPrefixes",
        "name": "name",
        "policy_group_names": "policyGroupNames",
    },
)
class VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection:
    def __init__(
        self,
        *,
        address_prefixes: typing.Sequence[builtins.str],
        name: builtins.str,
        policy_group_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_prefixes VirtualNetworkGateway#address_prefixes}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.
        :param policy_group_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#policy_group_names VirtualNetworkGateway#policy_group_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1651b55fccca9b4b7d2aa974e6387667eb4c53b73e2cd1b59f1e5029e969f0)
            check_type(argname="argument address_prefixes", value=address_prefixes, expected_type=type_hints["address_prefixes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_group_names", value=policy_group_names, expected_type=type_hints["policy_group_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_prefixes": address_prefixes,
            "name": name,
            "policy_group_names": policy_group_names,
        }

    @builtins.property
    def address_prefixes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#address_prefixes VirtualNetworkGateway#address_prefixes}.'''
        result = self._values.get("address_prefixes")
        assert result is not None, "Required property 'address_prefixes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#name VirtualNetworkGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_group_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_network_gateway#policy_group_names VirtualNetworkGateway#policy_group_names}.'''
        result = self._values.get("policy_group_names")
        assert result is not None, "Required property 'policy_group_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1b84ec6c55ca6424e2833c86d3072aec87e33cb3d1fbe0f640c8b674aaa21a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f180fbebba969839d89caf421e58e66d06d1b50c7273032ca359282fae088ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7be43a1f7545e7d8f84e25a2413a5edb14fb0d4b92d689ceea805cd797f702)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eb2942d15995de0e03335306c0fea4eea218d8befa5fc2e5e49e4e909f4215f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6a9d2304cb857afdb356ba03793a4b1732648050c29075ae6f7d026daf48a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffaf4b6e8ba62f2978b26e358269eae00db82754738e7595ff5de9623f1e1f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualNetworkGateway.VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e9cf4cbefae455df6d2dc61c88b0bb8451f5288a542d39b2b1ba0db1e392eee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="addressPrefixesInput")
    def address_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyGroupNamesInput")
    def policy_group_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "policyGroupNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="addressPrefixes")
    def address_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressPrefixes"))

    @address_prefixes.setter
    def address_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662f72c4495c85b8034fd56d91d14b08a2c1623c94efbed3e99d551c848f994f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ce7b4dc6c73cb6973b18c4c7f48649c2f149dc1be8aeb9a40b1f38121ac133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyGroupNames")
    def policy_group_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "policyGroupNames"))

    @policy_group_names.setter
    def policy_group_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc64ed0611a33607d66354ae16d189102c52f472e888b3f033176ac56f9ac45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyGroupNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ed36754ead22c8f82b4cfe824e625c11a1b94c6f131ab7df1c36550bef81fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VirtualNetworkGateway",
    "VirtualNetworkGatewayBgpSettings",
    "VirtualNetworkGatewayBgpSettingsOutputReference",
    "VirtualNetworkGatewayBgpSettingsPeeringAddresses",
    "VirtualNetworkGatewayBgpSettingsPeeringAddressesList",
    "VirtualNetworkGatewayBgpSettingsPeeringAddressesOutputReference",
    "VirtualNetworkGatewayConfig",
    "VirtualNetworkGatewayCustomRoute",
    "VirtualNetworkGatewayCustomRouteOutputReference",
    "VirtualNetworkGatewayIpConfiguration",
    "VirtualNetworkGatewayIpConfigurationList",
    "VirtualNetworkGatewayIpConfigurationOutputReference",
    "VirtualNetworkGatewayPolicyGroup",
    "VirtualNetworkGatewayPolicyGroupList",
    "VirtualNetworkGatewayPolicyGroupOutputReference",
    "VirtualNetworkGatewayPolicyGroupPolicyMember",
    "VirtualNetworkGatewayPolicyGroupPolicyMemberList",
    "VirtualNetworkGatewayPolicyGroupPolicyMemberOutputReference",
    "VirtualNetworkGatewayTimeouts",
    "VirtualNetworkGatewayTimeoutsOutputReference",
    "VirtualNetworkGatewayVpnClientConfiguration",
    "VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy",
    "VirtualNetworkGatewayVpnClientConfigurationIpsecPolicyOutputReference",
    "VirtualNetworkGatewayVpnClientConfigurationOutputReference",
    "VirtualNetworkGatewayVpnClientConfigurationRadiusServer",
    "VirtualNetworkGatewayVpnClientConfigurationRadiusServerList",
    "VirtualNetworkGatewayVpnClientConfigurationRadiusServerOutputReference",
    "VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate",
    "VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateList",
    "VirtualNetworkGatewayVpnClientConfigurationRevokedCertificateOutputReference",
    "VirtualNetworkGatewayVpnClientConfigurationRootCertificate",
    "VirtualNetworkGatewayVpnClientConfigurationRootCertificateList",
    "VirtualNetworkGatewayVpnClientConfigurationRootCertificateOutputReference",
    "VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection",
    "VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionList",
    "VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnectionOutputReference",
]

publication.publish()

def _typecheckingstub__48953827ec555ed2ade9040335a854e18bd38c848a8bf9c1c07f2877a70b35fd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: builtins.str,
    type: builtins.str,
    active_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_route_translation_for_nat_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_settings: typing.Optional[typing.Union[VirtualNetworkGatewayBgpSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_route: typing.Optional[typing.Union[VirtualNetworkGatewayCustomRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    default_local_network_gateway_id: typing.Optional[builtins.str] = None,
    dns_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    enable_bgp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_sec_replay_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayPolicyGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    private_ip_address_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remote_vnet_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualNetworkGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_wan_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpn_client_configuration: typing.Optional[typing.Union[VirtualNetworkGatewayVpnClientConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    vpn_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ff00b2951af5962d6fe409a806ed4f4295c6d984858e952e6b728b1acce3576c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0e5077f9c33290cc4271d21b596bbaf36c40b478c75a181001a4554a4d9cf4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50acfde923af101ec5b4b2a48a481f77e11b9e7a06225ec083556125241aadb0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayPolicyGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe3a72720183257abafcf181f6857c5d02b48d6bb224fc690aec2dd6e4538c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17726d73e9a2d733c5d6f24862f44ff1991494617aa43398ecab021521db2f34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e87b4fd6cd9fd2376b774502ab5824e5f155968223390434167f95b79587126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ebb7ca73b283cc3534a5a74173929fe065cb68df8679b3cf40041d35fccb36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9adfb8eb2912f6e71eb6ae05caeec9965379930d028903ba87ae8b9beba30f93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f1eb717cfd9d4d4a5463fd286c4bf395595aa302388b89f35fa23285c8847b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0f16c9d3aff631060d3863bcd757757ffc3d328c29c0559e754ffe96f46851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecfcb9566093233315323e39518a9e073bbf2cdefd1f6437ca80d9c96ad13cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deadd2318116ae00073f4c7fb5d6bd327d5024fd3bd26458ba9983b18dcd1dcb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6818008462492304e4fc25ada0964c8c920e2b90c514ffcdf6aef491a2ec83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed06eea6f093e99e965f1676bc3c5c3fec51b8c3e80c70ced83348727f197b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5360c6e95b57967db895bb2093710553378a725c73f705ecf4b20ee80c605c7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e774f9e45d6742908e03c99476e66705ed6a85e7366c67c549a9b3bbe7330f01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f45ad6700ce0b670f1e189a594e4cd9cecf4f3144cfc3b3cfec8f015e80cfcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b46da206be18874c74ef3c93f1379195dfab2b47e2b25d9626d62e57d19e193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ca5a8253034355b37fb444a61e2063da3b5a9a56f42ca8c3e3f732109171c8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d8d50f15a04d7d80a6aadc0c38b8f4fd8473efd2821eb15791b6da0522feae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4befd19b56043db5f8efcf1d2cecc750f1a0b2b472b0fbc4df267dc465b249a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dff0705f371233906b88ba32007dfe9bbf68894fdd12b338daa8ddc5e0cc5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b89d9fa883cefca5a312fb3160101ba319399c109101e3c061c718cb2d19bb(
    *,
    asn: typing.Optional[jsii.Number] = None,
    peering_addresses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayBgpSettingsPeeringAddresses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    peer_weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3997b1229d903682925bc15abfd38be1e6b94d57bdacb1ad532f3e2c8732e42a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2217caf9b4ca629d7db55a91a4b504b693b1767d5bf0838963fdbafdbba31ca4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayBgpSettingsPeeringAddresses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abfb7040a1e5160439b927ab75ecabfb6c5fdad2656579f8d3f59bb3ab71d28(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7006ed9dafe979164164b7fc681284237c55c4e345e28a412e14bb807c30fc15(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d47d545b4575fc12efdaa4d352f4f47e76a9018beebde1eac07200338a090ba(
    value: typing.Optional[VirtualNetworkGatewayBgpSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ead08f321aab8832793574a545799989d2022c1fb9164edfe10fca3b0bbeed(
    *,
    apipa_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_configuration_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8157c713bae26bd28312210519ffc89e0f2b858691e2fab14eed06e88a5c187f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01f118d9b59dce6359ef6f526160877f031ea2cc9607bdb5dd8e12e2748d144(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a6418c52af2fe098279c504861322aa8cd3f110c3244772b6174b5028cdd3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4442757e43a67c90c718185fb23c65cd408a12cfd83e084bd3ec44d13d5bb1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2f350bb5f65f5a3edccf8f2ec194cfe9aa02ac779f35f8021dd901744e3fc2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8271f2ca8173eb90069ca42e73df376caca3afe200e02f932a01272b997239b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayBgpSettingsPeeringAddresses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca5035b06ec078436d06f667af12ca7400e91383bf9487159fbbb65b43aa6ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ffb5debe920f14078f9dc934500d0d73f1cc3ca45bf31c0b7e158661be1dbe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1624ff33f7cf01ed1d57badbdf1f1fe48d6169c38e3347a5c67ac3514c88477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e658addeecd95b09eddc4f5c36f91ebde33ed3d0499079502a9467943cf8522(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayBgpSettingsPeeringAddresses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c246c68e1ae81b3e553e2bb185120d38bb957f8535ac32bf7b117ee28f4f69(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: builtins.str,
    type: builtins.str,
    active_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_route_translation_for_nat_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_settings: typing.Optional[typing.Union[VirtualNetworkGatewayBgpSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_route: typing.Optional[typing.Union[VirtualNetworkGatewayCustomRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    default_local_network_gateway_id: typing.Optional[builtins.str] = None,
    dns_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    enable_bgp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    generation: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_sec_replay_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayPolicyGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    private_ip_address_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remote_vnet_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualNetworkGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_wan_traffic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpn_client_configuration: typing.Optional[typing.Union[VirtualNetworkGatewayVpnClientConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    vpn_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94269eb0a0d1621124eada5695625751947511de51cdd029d8aa5f1da24ee39(
    *,
    address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e567be0dc02fa61f843631bbc3d6d96da5ff26ca31d544c9e2c8bd1da4a3b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d991d30ffff410fd4103089fbd2922719598c8ef727ba4dc83a75c891221034e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9c2c87ce093bae0be8715dfb3a0dedce9cc8c84c8a57653133d30d2130b1f2(
    value: typing.Optional[VirtualNetworkGatewayCustomRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e60357e7f9f9a4cbd9739f5e6861b86f79145ce4101fba054227d06456ef791(
    *,
    subnet_id: builtins.str,
    name: typing.Optional[builtins.str] = None,
    private_ip_address_allocation: typing.Optional[builtins.str] = None,
    public_ip_address_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edda96bdb259f9e148e1c14ce7ed80a7f6c141e69cb6c20d52cd32febed46b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d9d862f5283aadb9dd5ffcf813b7a37e64ce7c20c29ecc330d70c6cba85d70(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76acf8c3928e0347c6771de278946e5f738235dcb75925d80c36a6b509d694b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1bc5861cf27c9d91863fdc0cc45888afa913942afb0cc2466aae7805c86372(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bf10c871687a3274d0fbce14245452355a76894ad574f9c684fc5cf9a24d4e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16deca02606b65c61a23dcb3bb4c2b21c047a186a06ce2e2e7b89c5d2e752ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayIpConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bff8503cb64940744e5798a441de1152a4ddf5082815a0e9b5633a701c481e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ece67b7ba42fa2ee7138f30d1726fde6b0ea4c5554522a0948bc61a58d4f25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd42336cad67bd5efc8660e3807b5484c61b590e6f46d040ad475cbad1aab1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb5bd46ed489c81ed81a84bcc5517b22f2729ccbbe00f214c7966e2af99b35f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c310bb738a42717b232bd3c17af732566695020bca7307b8ed9fbe2c693b0d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1176efb9bffc085472cd282a63bae88dcf6036c645f4e1260eba32470d5728e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayIpConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d1b01f119eb72eb8869ab62743a92ec4a52204e8eb7fd9e9190d8612ac83c9(
    *,
    name: builtins.str,
    policy_member: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayPolicyGroupPolicyMember, typing.Dict[builtins.str, typing.Any]]]],
    is_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb01333399ecfd3c38493882d6db94611ea41fbfdc6ffeaa6834e4398b3507c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67733d05e9522bea8b62922eb73bdaa83a21246cfe9fd50496825ef7fa8870c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c68dc75c186f11761dc7af976adab3f8f8ea8e889d535593f3c185cebbb75d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b9e00a411652b8e5327c3c4f596caafbe4b0ec2c937882db07c682dcfda577(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99788ecaaed3d124ea9540e164e8a72b6fd01fbce5cf757be69d7f74dd256969(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2390ad8f48d9226d40e18e2463e64d18f4abdf2accfc06e654bd79ea9c592b96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e4b995bfe53eb8d7275cdf55ca7e2532294be9364ff2dd25d4148f163dde47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a288f44584d8b12e33dd21cec40caa31c8747ab3a0a821c8233fe5d7f5051370(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayPolicyGroupPolicyMember, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04f14441c1e8b9d30184a9ef41f473099c3fd14ae00a883dbc7ebfd0ada953d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d701776b9495e52de73fe94280ce9c695dd047b09e2482d07782def3cab97662(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483d9a33b1751622aaee570a05393e80b895e4584f507a9a361c78126c299431(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2aa5544664cff0ddc4daf1d645d6df1fde62eba0a4b268af3bc817edd0529a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d3f01716772c2bcbbca28f81b85129df0404e1de317c55b30dea703e73ce02(
    *,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d7ce40424c51769078584a309c3171cb94b2ba1713b43842874db9d67712ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af27bce9c617ecbf3e983bdcaa565b119e47fd3c643c4f0473475ffc5751541(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce3c6464b91d630b93caa909b618f91904e04c63ad242742522f05523ca4e74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce4ba3918740e7dcc44d70476c42500eef59559ab4c25d56fb1b8849bcb1a9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a793dfd702d86a804a6d9c7f5ba2edb04182508f93c94a6e33f24a075ba157cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abea69bfb2debc7ddd58b3a0c25988c6dac8310e10df59e74a4e9ec87e47b6df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayPolicyGroupPolicyMember]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a75d1b373baf8ed0be420804d1e991d973409aab61396acc94dcca4fb2220b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e957853ab36faf589abd69045f25da93608c5a41d8ecee6e9d2e3327f6a17eaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6caa508a911f94b69891c24f81ea07904a9b24c7e548291868134c859460e0e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a474fdb4dde58f9e328529d4652b4e07b32ad07d999c7f821e8e2bf3ce147e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321b5b72acdeb364c1faf12e7a591510e0d02731f2369221d37b39931c7fb4f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayPolicyGroupPolicyMember]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedab3d10c3d9b2a32302d2ae0238eabe16448f95b70dd6cb003177134695a08(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4c00f44afc23539473cac33f5edbc7034584844c4f419db1dc946591342740(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab56d48c9c9dd31ecbc0bcfcdfd05a50d826378beab08802640c79ee845f15e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0970f1a592e5b8977d9d4455639df496c4ab76271e8d64b7f767bfc37200b543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49529f7258a4f0890739aa31b4f00c422f962f8de3b54b4ba2ac5b37b7946284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da567105ce95c82476336d3d3f2b90bd61ac8756cbc19ec749b7d454e2e2211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6b1ba47c60f318392e2f61bedb40583ba57dd9f28b27c489fa05212061a0e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff55421c4ce9d5094966f80d343acc35417dd9b91afb9e683ef97afc828fef9f(
    *,
    address_space: typing.Sequence[builtins.str],
    aad_audience: typing.Optional[builtins.str] = None,
    aad_issuer: typing.Optional[builtins.str] = None,
    aad_tenant: typing.Optional[builtins.str] = None,
    ipsec_policy: typing.Optional[typing.Union[VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    radius_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationRadiusServer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    radius_server_address: typing.Optional[builtins.str] = None,
    radius_server_secret: typing.Optional[builtins.str] = None,
    revoked_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    root_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationRootCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    virtual_network_gateway_client_connection: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vpn_auth_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpn_client_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47305235420e91bf95271cde88593f6c67aa4d2fa2e99b7aedda59acace3e13(
    *,
    dh_group: builtins.str,
    ike_encryption: builtins.str,
    ike_integrity: builtins.str,
    ipsec_encryption: builtins.str,
    ipsec_integrity: builtins.str,
    pfs_group: builtins.str,
    sa_data_size_in_kilobytes: jsii.Number,
    sa_lifetime_in_seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d948ba8c0281659acaeeff419fd97992bb9b0a8dc599ff3dadff4758b0779e60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccb27d448a45d9086d80426a028eceec4325e8ca6ff3e0af9b23c6d5774b2dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8adc1d94e2df7428e47b11e569b4e71e2d00588fc9c7ad8a272e79891c4a52f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4869b79b94e69b9dd8b0fbccfe08a6ee0ff0c3d9178e666b12ffd7130a5f1e18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273faf93913e72fd084023a397d09dc7061d7f009a86d197e6736eefbc55e2eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7193b6ea1d675bdef7567fe9bd1b2af9e5770c9958d13c943c689db4ba4379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb51b5a329816e8dc2373e0c8bc2c5a18c24f72a3b6a084c7f2c85b8b6c1942f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda0e86236fc939d3e695491318809932f8b58e198a3f17e45a7df085a11ae68(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f60d27e00b857ff3a7b8024a128db74cd72f77ad60ca80bf0876db04163fad4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4077d02273a7709977fd49fb0c46ae657d383be277a5f7e42013f41af541e4(
    value: typing.Optional[VirtualNetworkGatewayVpnClientConfigurationIpsecPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfdee106a19e96f7ef0b3266d3966083011a91b2e871294d87a632a766c2dce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe61dbdf7791699d6ea19c4f7cf28fc65b2d91a584642746d0a07df3058973d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationRadiusServer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297df67cf4746af56933f13f6dbb22d42b076a7cfd3c366f97fc857c1eaa42c4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05be996eca6b0d84740253462645f6a8ed9774a07898299caba3ae19f6147007(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationRootCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c6dccc4ebaa4030ee95e412c56a0d325e1a1754801c806bacabf0d55cec4e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091c25d06e28b6cf2d56a2b494b94146fde835078d37b1328ec731d673cb48ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35078ef57a72f736820efcd6bcb52d5037d66602d2c65e2c9595befa737e34c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9871be7cb90ad6235fab9c56768787909ec81d6221c741add371a9ce5f563e4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa1d3e210baf3d390125a64b8666b603c475412b2b75fd76f5032481c8420f2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29dff5fd51cfc30de2ca10d375cc8525767545968b6d62059ed3dc26fe99a94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d199f7307fedfe2897ce7b77ee64648c2a424a177ca6ac7b15f5aa263608f4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c284caabe62b5ee4f2df7311abcd18d8412dc45316762a75362d0224a1811d06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c797ac2ff6c5c56b375912adf20ffd3080140ed793c750635ce1ea755c45066a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e6386cf66bc5f0a9845792885375cc11add39a0024eb5ac84613db9b82be8d(
    value: typing.Optional[VirtualNetworkGatewayVpnClientConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5025d56e1344ffcf4ae4b4899a1a907090b8f71e95f707e9f19e40d437a4e0f9(
    *,
    address: builtins.str,
    score: jsii.Number,
    secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63e4c2c49a6a101e14ebe855faa8a6cd3acd40d823eed6308ba4486c4da55bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5ad59eb42c02d5537c155a0be41b0c54907e62c5ec91b395cee32d8a999805(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e760bc3e098e548af0de4a4b87bf36af81a90eec6b8d3516f3f5e82a82d7909(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2992d7733c62ab72a32f3b45d5ce41701544d68eb78fe5144a2724f603475eed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69a47e470755c2799ddc7252ac81fe9d5a4d96c169d51e884e032dca940ead6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478a4dfa0e25fc0bcb63a7a9e789f52d93b0d50296a8206935be838543499802(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRadiusServer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af7fa3cb84c892ca8df555cce40ddf056b96da16c9d952efc433ad8f3c38bd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105031ad20d676361e7aad463f707252a477dfe3300f794798a1bdff86c2ef34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7077b9a6b391444f268355db6e0acf413102a5b54eb5380618784e9b6131a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd52f27d3be986cc7676922032f417dd2aa6e0495b89c38dc5fa6d2c34f9eabf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f00047097db75f7092394fa51e5b5ccedb183d8d164a4cc16b624d5cfa4bab3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRadiusServer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8f7e63a6ffbab29fedec9bab96395eaa61afce693eb8a428e29fbd5672d929(
    *,
    name: builtins.str,
    thumbprint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12acf5fe13af21c1e1ad8ae96a8adb554499d714e9d4c49eb496ff6c0cd53379(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28bc6f33ac20bb0cff1a282b252cb96a771aa2833a95984b4fdad99665f70d73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea56519a41403e5fa13fb5c4baf9a1bb4e006261006d62286529ab09740a8132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3477c13f9f2c71febb60eddf97e35f73ade3962cc9f2dbb8207cc31e0be7500(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed7b5dd280cb20c98112029039d3e57c1e79cb3d94ce797b29d804d10761a5c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c9f5e49e61fce7fd41a944d9f26b0c0eb076320e5662a37f1b2b6016fa543f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c97b447288c29301058acb6a72ed399ce81bf324c3f30242a2079b6cc70b11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98f9ba1f21a54466e197a572b9e9808a671f74b00564028e85f31cdf27240eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91665f1fd80564c1247035dc4794ca5ebe655e39693ebda310240ab10581dcd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2345e60a0a78bef6509e23d4925bb440cc7a9ff1ff8dd0b44538ab092509149a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRevokedCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6a3d8dc27ba7957603268de4e7875549709277fd6a9469d1a2d7e339afae3e(
    *,
    name: builtins.str,
    public_cert_data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5735c09e0e3236e65ce87977912291e175cbb3730b17bb8e2bca44e6b8bb66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544f0ebbfee4838bad254a3fe041fcf0668d359420f0aa5450368188188306ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685d0b8cfdd8bbdb35242414ed7f4fa848e8f4e389189828b1aca287f3ff262a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df825e2417b6df3c02c6e2c023fd0bf14b92fbaf7107ee904d6da7e4ae2880b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f4aae125df40016af6502d5e8d42990cdd4dc778121b7c533914421fdf0516(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de36b4c0454010955bb9b362417aeb5a7d16b1f5a9a5d23884bb9b4986657ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationRootCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb26ece8ea8bff05fc255b2c27d1b255d951aec1a822a0bfb7b23a7fd410a6db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279e88189f9fe530fdb3a90f6d75de39dd3eb0bd524829bc257ec178f1f31af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536cf7854b31583527d5871a6830d2e7102b7064a5035818580e7d82f0893025(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a49cd9a179e971cbf2d43e7d2e7dee3b7cf77ab1c37010cd841cdf12b228193(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationRootCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1651b55fccca9b4b7d2aa974e6387667eb4c53b73e2cd1b59f1e5029e969f0(
    *,
    address_prefixes: typing.Sequence[builtins.str],
    name: builtins.str,
    policy_group_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b84ec6c55ca6424e2833c86d3072aec87e33cb3d1fbe0f640c8b674aaa21a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f180fbebba969839d89caf421e58e66d06d1b50c7273032ca359282fae088ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7be43a1f7545e7d8f84e25a2413a5edb14fb0d4b92d689ceea805cd797f702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb2942d15995de0e03335306c0fea4eea218d8befa5fc2e5e49e4e909f4215f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6a9d2304cb857afdb356ba03793a4b1732648050c29075ae6f7d026daf48a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffaf4b6e8ba62f2978b26e358269eae00db82754738e7595ff5de9623f1e1f6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9cf4cbefae455df6d2dc61c88b0bb8451f5288a542d39b2b1ba0db1e392eee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662f72c4495c85b8034fd56d91d14b08a2c1623c94efbed3e99d551c848f994f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ce7b4dc6c73cb6973b18c4c7f48649c2f149dc1be8aeb9a40b1f38121ac133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc64ed0611a33607d66354ae16d189102c52f472e888b3f033176ac56f9ac45c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ed36754ead22c8f82b4cfe824e625c11a1b94c6f131ab7df1c36550bef81fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualNetworkGatewayVpnClientConfigurationVirtualNetworkGatewayClientConnection]],
) -> None:
    """Type checking stubs"""
    pass
