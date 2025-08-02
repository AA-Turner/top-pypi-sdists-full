r'''
# `opentelekomcloud_enterprise_vpn_connection_v5`

Refer to the Terraform Registry for docs: [`opentelekomcloud_enterprise_vpn_connection_v5`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5).
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


class EnterpriseVpnConnectionV5(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5 opentelekomcloud_enterprise_vpn_connection_v5}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        customer_gateway_id: builtins.str,
        gateway_id: builtins.str,
        gateway_ip: builtins.str,
        name: builtins.str,
        psk: builtins.str,
        vpn_type: builtins.str,
        enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_role: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ikepolicy: typing.Optional[typing.Union["EnterpriseVpnConnectionV5Ikepolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        ipsecpolicy: typing.Optional[typing.Union["EnterpriseVpnConnectionV5Ipsecpolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        policy_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnterpriseVpnConnectionV5PolicyRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EnterpriseVpnConnectionV5Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel_local_address: typing.Optional[builtins.str] = None,
        tunnel_peer_address: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5 opentelekomcloud_enterprise_vpn_connection_v5} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param customer_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#customer_gateway_id EnterpriseVpnConnectionV5#customer_gateway_id}.
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#gateway_id EnterpriseVpnConnectionV5#gateway_id}.
        :param gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#gateway_ip EnterpriseVpnConnectionV5#gateway_ip}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#name EnterpriseVpnConnectionV5#name}.
        :param psk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#psk EnterpriseVpnConnectionV5#psk}.
        :param vpn_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#vpn_type EnterpriseVpnConnectionV5#vpn_type}.
        :param enable_nqa: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#enable_nqa EnterpriseVpnConnectionV5#enable_nqa}.
        :param ha_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ha_role EnterpriseVpnConnectionV5#ha_role}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#id EnterpriseVpnConnectionV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ikepolicy: ikepolicy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ikepolicy EnterpriseVpnConnectionV5#ikepolicy}
        :param ipsecpolicy: ipsecpolicy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ipsecpolicy EnterpriseVpnConnectionV5#ipsecpolicy}
        :param peer_subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_subnets EnterpriseVpnConnectionV5#peer_subnets}.
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#policy_rules EnterpriseVpnConnectionV5#policy_rules}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tags EnterpriseVpnConnectionV5#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#timeouts EnterpriseVpnConnectionV5#timeouts}
        :param tunnel_local_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tunnel_local_address EnterpriseVpnConnectionV5#tunnel_local_address}.
        :param tunnel_peer_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tunnel_peer_address EnterpriseVpnConnectionV5#tunnel_peer_address}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33e29d1898cd2903a0147dde3242302c835f0dc8d6fc5b9a8f985408530bb57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EnterpriseVpnConnectionV5Config(
            customer_gateway_id=customer_gateway_id,
            gateway_id=gateway_id,
            gateway_ip=gateway_ip,
            name=name,
            psk=psk,
            vpn_type=vpn_type,
            enable_nqa=enable_nqa,
            ha_role=ha_role,
            id=id,
            ikepolicy=ikepolicy,
            ipsecpolicy=ipsecpolicy,
            peer_subnets=peer_subnets,
            policy_rules=policy_rules,
            tags=tags,
            timeouts=timeouts,
            tunnel_local_address=tunnel_local_address,
            tunnel_peer_address=tunnel_peer_address,
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
        '''Generates CDKTF code for importing a EnterpriseVpnConnectionV5 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EnterpriseVpnConnectionV5 to import.
        :param import_from_id: The id of the existing EnterpriseVpnConnectionV5 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EnterpriseVpnConnectionV5 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8296ddcd4f76f5d2f23482fdf12242203473064de223689aec71e0e7510667c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIkepolicy")
    def put_ikepolicy(
        self,
        *,
        authentication_algorithm: typing.Optional[builtins.str] = None,
        authentication_method: typing.Optional[builtins.str] = None,
        dh_group: typing.Optional[builtins.str] = None,
        dpd: typing.Optional[typing.Union["EnterpriseVpnConnectionV5IkepolicyDpd", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        ike_version: typing.Optional[builtins.str] = None,
        lifetime_seconds: typing.Optional[jsii.Number] = None,
        local_id: typing.Optional[builtins.str] = None,
        local_id_type: typing.Optional[builtins.str] = None,
        peer_id: typing.Optional[builtins.str] = None,
        peer_id_type: typing.Optional[builtins.str] = None,
        phase_one_negotiation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_algorithm EnterpriseVpnConnectionV5#authentication_algorithm}.
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_method EnterpriseVpnConnectionV5#authentication_method}.
        :param dh_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#dh_group EnterpriseVpnConnectionV5#dh_group}.
        :param dpd: dpd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#dpd EnterpriseVpnConnectionV5#dpd}
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encryption_algorithm EnterpriseVpnConnectionV5#encryption_algorithm}.
        :param ike_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ike_version EnterpriseVpnConnectionV5#ike_version}.
        :param lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#lifetime_seconds EnterpriseVpnConnectionV5#lifetime_seconds}.
        :param local_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#local_id EnterpriseVpnConnectionV5#local_id}.
        :param local_id_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#local_id_type EnterpriseVpnConnectionV5#local_id_type}.
        :param peer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_id EnterpriseVpnConnectionV5#peer_id}.
        :param peer_id_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_id_type EnterpriseVpnConnectionV5#peer_id_type}.
        :param phase_one_negotiation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#phase_one_negotiation_mode EnterpriseVpnConnectionV5#phase_one_negotiation_mode}.
        '''
        value = EnterpriseVpnConnectionV5Ikepolicy(
            authentication_algorithm=authentication_algorithm,
            authentication_method=authentication_method,
            dh_group=dh_group,
            dpd=dpd,
            encryption_algorithm=encryption_algorithm,
            ike_version=ike_version,
            lifetime_seconds=lifetime_seconds,
            local_id=local_id,
            local_id_type=local_id_type,
            peer_id=peer_id,
            peer_id_type=peer_id_type,
            phase_one_negotiation_mode=phase_one_negotiation_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putIkepolicy", [value]))

    @jsii.member(jsii_name="putIpsecpolicy")
    def put_ipsecpolicy(
        self,
        *,
        authentication_algorithm: typing.Optional[builtins.str] = None,
        encapsulation_mode: typing.Optional[builtins.str] = None,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        lifetime_seconds: typing.Optional[jsii.Number] = None,
        pfs: typing.Optional[builtins.str] = None,
        transform_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_algorithm EnterpriseVpnConnectionV5#authentication_algorithm}.
        :param encapsulation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encapsulation_mode EnterpriseVpnConnectionV5#encapsulation_mode}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encryption_algorithm EnterpriseVpnConnectionV5#encryption_algorithm}.
        :param lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#lifetime_seconds EnterpriseVpnConnectionV5#lifetime_seconds}.
        :param pfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#pfs EnterpriseVpnConnectionV5#pfs}.
        :param transform_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#transform_protocol EnterpriseVpnConnectionV5#transform_protocol}.
        '''
        value = EnterpriseVpnConnectionV5Ipsecpolicy(
            authentication_algorithm=authentication_algorithm,
            encapsulation_mode=encapsulation_mode,
            encryption_algorithm=encryption_algorithm,
            lifetime_seconds=lifetime_seconds,
            pfs=pfs,
            transform_protocol=transform_protocol,
        )

        return typing.cast(None, jsii.invoke(self, "putIpsecpolicy", [value]))

    @jsii.member(jsii_name="putPolicyRules")
    def put_policy_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnterpriseVpnConnectionV5PolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b32ec56ae6e2afae50f659d2d661350b6e010052d0e0bb44386fb2bb1555956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyRules", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#create EnterpriseVpnConnectionV5#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#delete EnterpriseVpnConnectionV5#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#update EnterpriseVpnConnectionV5#update}.
        '''
        value = EnterpriseVpnConnectionV5Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEnableNqa")
    def reset_enable_nqa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNqa", []))

    @jsii.member(jsii_name="resetHaRole")
    def reset_ha_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaRole", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIkepolicy")
    def reset_ikepolicy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIkepolicy", []))

    @jsii.member(jsii_name="resetIpsecpolicy")
    def reset_ipsecpolicy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpsecpolicy", []))

    @jsii.member(jsii_name="resetPeerSubnets")
    def reset_peer_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerSubnets", []))

    @jsii.member(jsii_name="resetPolicyRules")
    def reset_policy_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyRules", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTunnelLocalAddress")
    def reset_tunnel_local_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelLocalAddress", []))

    @jsii.member(jsii_name="resetTunnelPeerAddress")
    def reset_tunnel_peer_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelPeerAddress", []))

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
    @jsii.member(jsii_name="ikepolicy")
    def ikepolicy(self) -> "EnterpriseVpnConnectionV5IkepolicyOutputReference":
        return typing.cast("EnterpriseVpnConnectionV5IkepolicyOutputReference", jsii.get(self, "ikepolicy"))

    @builtins.property
    @jsii.member(jsii_name="ipsecpolicy")
    def ipsecpolicy(self) -> "EnterpriseVpnConnectionV5IpsecpolicyOutputReference":
        return typing.cast("EnterpriseVpnConnectionV5IpsecpolicyOutputReference", jsii.get(self, "ipsecpolicy"))

    @builtins.property
    @jsii.member(jsii_name="policyRules")
    def policy_rules(self) -> "EnterpriseVpnConnectionV5PolicyRulesList":
        return typing.cast("EnterpriseVpnConnectionV5PolicyRulesList", jsii.get(self, "policyRules"))

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
    def timeouts(self) -> "EnterpriseVpnConnectionV5TimeoutsOutputReference":
        return typing.cast("EnterpriseVpnConnectionV5TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayIdInput")
    def customer_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNqaInput")
    def enable_nqa_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNqaInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIdInput")
    def gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpInput")
    def gateway_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIpInput"))

    @builtins.property
    @jsii.member(jsii_name="haRoleInput")
    def ha_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ikepolicyInput")
    def ikepolicy_input(self) -> typing.Optional["EnterpriseVpnConnectionV5Ikepolicy"]:
        return typing.cast(typing.Optional["EnterpriseVpnConnectionV5Ikepolicy"], jsii.get(self, "ikepolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="ipsecpolicyInput")
    def ipsecpolicy_input(
        self,
    ) -> typing.Optional["EnterpriseVpnConnectionV5Ipsecpolicy"]:
        return typing.cast(typing.Optional["EnterpriseVpnConnectionV5Ipsecpolicy"], jsii.get(self, "ipsecpolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerSubnetsInput")
    def peer_subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "peerSubnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyRulesInput")
    def policy_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnterpriseVpnConnectionV5PolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnterpriseVpnConnectionV5PolicyRules"]]], jsii.get(self, "policyRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="pskInput")
    def psk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pskInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EnterpriseVpnConnectionV5Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "EnterpriseVpnConnectionV5Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelLocalAddressInput")
    def tunnel_local_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelLocalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelPeerAddressInput")
    def tunnel_peer_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelPeerAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnTypeInput")
    def vpn_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayId"))

    @customer_gateway_id.setter
    def customer_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a180eae6a4c88e550a8998125c8749fcd75b4bf3993e888bb8a38b359df3ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerGatewayId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__405e04f4df62fdeb4a6722e38660601db4957230004d33a86627e4c3a1d0d35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNqa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @gateway_id.setter
    def gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e9374520f7eba91a368cee38c37833ee306ff06a8e739920c22276b8c83d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayIp")
    def gateway_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayIp"))

    @gateway_ip.setter
    def gateway_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4789198a7bb1bc9c3ddff6ece2273c2be28e6a2d004cb125b74be40b6faa7c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="haRole")
    def ha_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haRole"))

    @ha_role.setter
    def ha_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e836abb2bdfde92d7f202237b6305758a201d5889404054139456d3ae484b412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9999c85fbe454fefe2dcd6f2851f3c2e29f409a5d25806039aa497c5977d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0c0e199f4bf7698b86c8951e6c57febb9e20211e0294255717653cb29675b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerSubnets")
    def peer_subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "peerSubnets"))

    @peer_subnets.setter
    def peer_subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b824860456046db1c65b9fb999c8d2661a30cbf7817af82f98b0888aeef13eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="psk")
    def psk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "psk"))

    @psk.setter
    def psk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ff10ef61b1ebc58c8bcdbd2ea664154c7a31098782ef5ffc204cc1f3eb5d91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "psk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec029bd6e7430bd3515ba08db88d43b6b1eba9c3a23953526a2f0bf1c4dc636d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnelLocalAddress")
    def tunnel_local_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelLocalAddress"))

    @tunnel_local_address.setter
    def tunnel_local_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f7c7f39c1b47a8e6fffbd61eb364e1d6ede7672d56f1601cfbb1d94c167ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelLocalAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnelPeerAddress")
    def tunnel_peer_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelPeerAddress"))

    @tunnel_peer_address.setter
    def tunnel_peer_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90acc804493177ea2213c72fd5cac64764fdded59e7c36f56a2f53ab32edd87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelPeerAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnType")
    def vpn_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnType"))

    @vpn_type.setter
    def vpn_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7663df606f986f9f36a74377cea62fc8b8a81a36aac08c8cc52f1159a2a42aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "customer_gateway_id": "customerGatewayId",
        "gateway_id": "gatewayId",
        "gateway_ip": "gatewayIp",
        "name": "name",
        "psk": "psk",
        "vpn_type": "vpnType",
        "enable_nqa": "enableNqa",
        "ha_role": "haRole",
        "id": "id",
        "ikepolicy": "ikepolicy",
        "ipsecpolicy": "ipsecpolicy",
        "peer_subnets": "peerSubnets",
        "policy_rules": "policyRules",
        "tags": "tags",
        "timeouts": "timeouts",
        "tunnel_local_address": "tunnelLocalAddress",
        "tunnel_peer_address": "tunnelPeerAddress",
    },
)
class EnterpriseVpnConnectionV5Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        customer_gateway_id: builtins.str,
        gateway_id: builtins.str,
        gateway_ip: builtins.str,
        name: builtins.str,
        psk: builtins.str,
        vpn_type: builtins.str,
        enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_role: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ikepolicy: typing.Optional[typing.Union["EnterpriseVpnConnectionV5Ikepolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        ipsecpolicy: typing.Optional[typing.Union["EnterpriseVpnConnectionV5Ipsecpolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        policy_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnterpriseVpnConnectionV5PolicyRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["EnterpriseVpnConnectionV5Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel_local_address: typing.Optional[builtins.str] = None,
        tunnel_peer_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param customer_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#customer_gateway_id EnterpriseVpnConnectionV5#customer_gateway_id}.
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#gateway_id EnterpriseVpnConnectionV5#gateway_id}.
        :param gateway_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#gateway_ip EnterpriseVpnConnectionV5#gateway_ip}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#name EnterpriseVpnConnectionV5#name}.
        :param psk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#psk EnterpriseVpnConnectionV5#psk}.
        :param vpn_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#vpn_type EnterpriseVpnConnectionV5#vpn_type}.
        :param enable_nqa: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#enable_nqa EnterpriseVpnConnectionV5#enable_nqa}.
        :param ha_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ha_role EnterpriseVpnConnectionV5#ha_role}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#id EnterpriseVpnConnectionV5#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ikepolicy: ikepolicy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ikepolicy EnterpriseVpnConnectionV5#ikepolicy}
        :param ipsecpolicy: ipsecpolicy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ipsecpolicy EnterpriseVpnConnectionV5#ipsecpolicy}
        :param peer_subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_subnets EnterpriseVpnConnectionV5#peer_subnets}.
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#policy_rules EnterpriseVpnConnectionV5#policy_rules}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tags EnterpriseVpnConnectionV5#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#timeouts EnterpriseVpnConnectionV5#timeouts}
        :param tunnel_local_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tunnel_local_address EnterpriseVpnConnectionV5#tunnel_local_address}.
        :param tunnel_peer_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tunnel_peer_address EnterpriseVpnConnectionV5#tunnel_peer_address}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ikepolicy, dict):
            ikepolicy = EnterpriseVpnConnectionV5Ikepolicy(**ikepolicy)
        if isinstance(ipsecpolicy, dict):
            ipsecpolicy = EnterpriseVpnConnectionV5Ipsecpolicy(**ipsecpolicy)
        if isinstance(timeouts, dict):
            timeouts = EnterpriseVpnConnectionV5Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c511d4507ea580aeddbc319b323ff746cd6a1db830d8f5105a7869d69bc33ed)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument customer_gateway_id", value=customer_gateway_id, expected_type=type_hints["customer_gateway_id"])
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument gateway_ip", value=gateway_ip, expected_type=type_hints["gateway_ip"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument psk", value=psk, expected_type=type_hints["psk"])
            check_type(argname="argument vpn_type", value=vpn_type, expected_type=type_hints["vpn_type"])
            check_type(argname="argument enable_nqa", value=enable_nqa, expected_type=type_hints["enable_nqa"])
            check_type(argname="argument ha_role", value=ha_role, expected_type=type_hints["ha_role"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ikepolicy", value=ikepolicy, expected_type=type_hints["ikepolicy"])
            check_type(argname="argument ipsecpolicy", value=ipsecpolicy, expected_type=type_hints["ipsecpolicy"])
            check_type(argname="argument peer_subnets", value=peer_subnets, expected_type=type_hints["peer_subnets"])
            check_type(argname="argument policy_rules", value=policy_rules, expected_type=type_hints["policy_rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tunnel_local_address", value=tunnel_local_address, expected_type=type_hints["tunnel_local_address"])
            check_type(argname="argument tunnel_peer_address", value=tunnel_peer_address, expected_type=type_hints["tunnel_peer_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_gateway_id": customer_gateway_id,
            "gateway_id": gateway_id,
            "gateway_ip": gateway_ip,
            "name": name,
            "psk": psk,
            "vpn_type": vpn_type,
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
        if enable_nqa is not None:
            self._values["enable_nqa"] = enable_nqa
        if ha_role is not None:
            self._values["ha_role"] = ha_role
        if id is not None:
            self._values["id"] = id
        if ikepolicy is not None:
            self._values["ikepolicy"] = ikepolicy
        if ipsecpolicy is not None:
            self._values["ipsecpolicy"] = ipsecpolicy
        if peer_subnets is not None:
            self._values["peer_subnets"] = peer_subnets
        if policy_rules is not None:
            self._values["policy_rules"] = policy_rules
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tunnel_local_address is not None:
            self._values["tunnel_local_address"] = tunnel_local_address
        if tunnel_peer_address is not None:
            self._values["tunnel_peer_address"] = tunnel_peer_address

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
    def customer_gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#customer_gateway_id EnterpriseVpnConnectionV5#customer_gateway_id}.'''
        result = self._values.get("customer_gateway_id")
        assert result is not None, "Required property 'customer_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#gateway_id EnterpriseVpnConnectionV5#gateway_id}.'''
        result = self._values.get("gateway_id")
        assert result is not None, "Required property 'gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_ip(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#gateway_ip EnterpriseVpnConnectionV5#gateway_ip}.'''
        result = self._values.get("gateway_ip")
        assert result is not None, "Required property 'gateway_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#name EnterpriseVpnConnectionV5#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def psk(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#psk EnterpriseVpnConnectionV5#psk}.'''
        result = self._values.get("psk")
        assert result is not None, "Required property 'psk' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpn_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#vpn_type EnterpriseVpnConnectionV5#vpn_type}.'''
        result = self._values.get("vpn_type")
        assert result is not None, "Required property 'vpn_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_nqa(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#enable_nqa EnterpriseVpnConnectionV5#enable_nqa}.'''
        result = self._values.get("enable_nqa")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ha_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ha_role EnterpriseVpnConnectionV5#ha_role}.'''
        result = self._values.get("ha_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#id EnterpriseVpnConnectionV5#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ikepolicy(self) -> typing.Optional["EnterpriseVpnConnectionV5Ikepolicy"]:
        '''ikepolicy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ikepolicy EnterpriseVpnConnectionV5#ikepolicy}
        '''
        result = self._values.get("ikepolicy")
        return typing.cast(typing.Optional["EnterpriseVpnConnectionV5Ikepolicy"], result)

    @builtins.property
    def ipsecpolicy(self) -> typing.Optional["EnterpriseVpnConnectionV5Ipsecpolicy"]:
        '''ipsecpolicy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ipsecpolicy EnterpriseVpnConnectionV5#ipsecpolicy}
        '''
        result = self._values.get("ipsecpolicy")
        return typing.cast(typing.Optional["EnterpriseVpnConnectionV5Ipsecpolicy"], result)

    @builtins.property
    def peer_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_subnets EnterpriseVpnConnectionV5#peer_subnets}.'''
        result = self._values.get("peer_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def policy_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnterpriseVpnConnectionV5PolicyRules"]]]:
        '''policy_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#policy_rules EnterpriseVpnConnectionV5#policy_rules}
        '''
        result = self._values.get("policy_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnterpriseVpnConnectionV5PolicyRules"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tags EnterpriseVpnConnectionV5#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["EnterpriseVpnConnectionV5Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#timeouts EnterpriseVpnConnectionV5#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["EnterpriseVpnConnectionV5Timeouts"], result)

    @builtins.property
    def tunnel_local_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tunnel_local_address EnterpriseVpnConnectionV5#tunnel_local_address}.'''
        result = self._values.get("tunnel_local_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel_peer_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#tunnel_peer_address EnterpriseVpnConnectionV5#tunnel_peer_address}.'''
        result = self._values.get("tunnel_peer_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnConnectionV5Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5Ikepolicy",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_algorithm": "authenticationAlgorithm",
        "authentication_method": "authenticationMethod",
        "dh_group": "dhGroup",
        "dpd": "dpd",
        "encryption_algorithm": "encryptionAlgorithm",
        "ike_version": "ikeVersion",
        "lifetime_seconds": "lifetimeSeconds",
        "local_id": "localId",
        "local_id_type": "localIdType",
        "peer_id": "peerId",
        "peer_id_type": "peerIdType",
        "phase_one_negotiation_mode": "phaseOneNegotiationMode",
    },
)
class EnterpriseVpnConnectionV5Ikepolicy:
    def __init__(
        self,
        *,
        authentication_algorithm: typing.Optional[builtins.str] = None,
        authentication_method: typing.Optional[builtins.str] = None,
        dh_group: typing.Optional[builtins.str] = None,
        dpd: typing.Optional[typing.Union["EnterpriseVpnConnectionV5IkepolicyDpd", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        ike_version: typing.Optional[builtins.str] = None,
        lifetime_seconds: typing.Optional[jsii.Number] = None,
        local_id: typing.Optional[builtins.str] = None,
        local_id_type: typing.Optional[builtins.str] = None,
        peer_id: typing.Optional[builtins.str] = None,
        peer_id_type: typing.Optional[builtins.str] = None,
        phase_one_negotiation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_algorithm EnterpriseVpnConnectionV5#authentication_algorithm}.
        :param authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_method EnterpriseVpnConnectionV5#authentication_method}.
        :param dh_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#dh_group EnterpriseVpnConnectionV5#dh_group}.
        :param dpd: dpd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#dpd EnterpriseVpnConnectionV5#dpd}
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encryption_algorithm EnterpriseVpnConnectionV5#encryption_algorithm}.
        :param ike_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ike_version EnterpriseVpnConnectionV5#ike_version}.
        :param lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#lifetime_seconds EnterpriseVpnConnectionV5#lifetime_seconds}.
        :param local_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#local_id EnterpriseVpnConnectionV5#local_id}.
        :param local_id_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#local_id_type EnterpriseVpnConnectionV5#local_id_type}.
        :param peer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_id EnterpriseVpnConnectionV5#peer_id}.
        :param peer_id_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_id_type EnterpriseVpnConnectionV5#peer_id_type}.
        :param phase_one_negotiation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#phase_one_negotiation_mode EnterpriseVpnConnectionV5#phase_one_negotiation_mode}.
        '''
        if isinstance(dpd, dict):
            dpd = EnterpriseVpnConnectionV5IkepolicyDpd(**dpd)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215c5334ff511b43f15db0c3618baa3f7fe14f74dfc1161907898c08e17ec764)
            check_type(argname="argument authentication_algorithm", value=authentication_algorithm, expected_type=type_hints["authentication_algorithm"])
            check_type(argname="argument authentication_method", value=authentication_method, expected_type=type_hints["authentication_method"])
            check_type(argname="argument dh_group", value=dh_group, expected_type=type_hints["dh_group"])
            check_type(argname="argument dpd", value=dpd, expected_type=type_hints["dpd"])
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument ike_version", value=ike_version, expected_type=type_hints["ike_version"])
            check_type(argname="argument lifetime_seconds", value=lifetime_seconds, expected_type=type_hints["lifetime_seconds"])
            check_type(argname="argument local_id", value=local_id, expected_type=type_hints["local_id"])
            check_type(argname="argument local_id_type", value=local_id_type, expected_type=type_hints["local_id_type"])
            check_type(argname="argument peer_id", value=peer_id, expected_type=type_hints["peer_id"])
            check_type(argname="argument peer_id_type", value=peer_id_type, expected_type=type_hints["peer_id_type"])
            check_type(argname="argument phase_one_negotiation_mode", value=phase_one_negotiation_mode, expected_type=type_hints["phase_one_negotiation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_algorithm is not None:
            self._values["authentication_algorithm"] = authentication_algorithm
        if authentication_method is not None:
            self._values["authentication_method"] = authentication_method
        if dh_group is not None:
            self._values["dh_group"] = dh_group
        if dpd is not None:
            self._values["dpd"] = dpd
        if encryption_algorithm is not None:
            self._values["encryption_algorithm"] = encryption_algorithm
        if ike_version is not None:
            self._values["ike_version"] = ike_version
        if lifetime_seconds is not None:
            self._values["lifetime_seconds"] = lifetime_seconds
        if local_id is not None:
            self._values["local_id"] = local_id
        if local_id_type is not None:
            self._values["local_id_type"] = local_id_type
        if peer_id is not None:
            self._values["peer_id"] = peer_id
        if peer_id_type is not None:
            self._values["peer_id_type"] = peer_id_type
        if phase_one_negotiation_mode is not None:
            self._values["phase_one_negotiation_mode"] = phase_one_negotiation_mode

    @builtins.property
    def authentication_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_algorithm EnterpriseVpnConnectionV5#authentication_algorithm}.'''
        result = self._values.get("authentication_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_method EnterpriseVpnConnectionV5#authentication_method}.'''
        result = self._values.get("authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dh_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#dh_group EnterpriseVpnConnectionV5#dh_group}.'''
        result = self._values.get("dh_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dpd(self) -> typing.Optional["EnterpriseVpnConnectionV5IkepolicyDpd"]:
        '''dpd block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#dpd EnterpriseVpnConnectionV5#dpd}
        '''
        result = self._values.get("dpd")
        return typing.cast(typing.Optional["EnterpriseVpnConnectionV5IkepolicyDpd"], result)

    @builtins.property
    def encryption_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encryption_algorithm EnterpriseVpnConnectionV5#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ike_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#ike_version EnterpriseVpnConnectionV5#ike_version}.'''
        result = self._values.get("ike_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#lifetime_seconds EnterpriseVpnConnectionV5#lifetime_seconds}.'''
        result = self._values.get("lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def local_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#local_id EnterpriseVpnConnectionV5#local_id}.'''
        result = self._values.get("local_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_id_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#local_id_type EnterpriseVpnConnectionV5#local_id_type}.'''
        result = self._values.get("local_id_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_id EnterpriseVpnConnectionV5#peer_id}.'''
        result = self._values.get("peer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_id_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#peer_id_type EnterpriseVpnConnectionV5#peer_id_type}.'''
        result = self._values.get("peer_id_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phase_one_negotiation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#phase_one_negotiation_mode EnterpriseVpnConnectionV5#phase_one_negotiation_mode}.'''
        result = self._values.get("phase_one_negotiation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnConnectionV5Ikepolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5IkepolicyDpd",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "msg": "msg", "timeout": "timeout"},
)
class EnterpriseVpnConnectionV5IkepolicyDpd:
    def __init__(
        self,
        *,
        interval: typing.Optional[jsii.Number] = None,
        msg: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#interval EnterpriseVpnConnectionV5#interval}.
        :param msg: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#msg EnterpriseVpnConnectionV5#msg}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#timeout EnterpriseVpnConnectionV5#timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a78c49931ea4dee71c20c187a99405048901004bd87899530504b31f176ec19)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument msg", value=msg, expected_type=type_hints["msg"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interval is not None:
            self._values["interval"] = interval
        if msg is not None:
            self._values["msg"] = msg
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#interval EnterpriseVpnConnectionV5#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def msg(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#msg EnterpriseVpnConnectionV5#msg}.'''
        result = self._values.get("msg")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#timeout EnterpriseVpnConnectionV5#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnConnectionV5IkepolicyDpd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpnConnectionV5IkepolicyDpdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5IkepolicyDpdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd2851731872ca495399d09baa38bfaba74443f353f31fe79ba398b5fb0287a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetMsg")
    def reset_msg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMsg", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="msgInput")
    def msg_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msgInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07979a0f08300207ba4cab8118d8e03adb35130850c1297e4747200b1b82847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msg")
    def msg(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "msg"))

    @msg.setter
    def msg(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528b26992e7fa7f8a8a903167b10a28d0977dec8853bc49d1c135c5ca9960f43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msg", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a28c32887a2df7316cde007627e4ae4d2a75124c7adf47532b5a134fd377a953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnterpriseVpnConnectionV5IkepolicyDpd]:
        return typing.cast(typing.Optional[EnterpriseVpnConnectionV5IkepolicyDpd], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnterpriseVpnConnectionV5IkepolicyDpd],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad27d7032bb6261f464dcd703290860571b30f8e6ba1d2d0ea6f4b63fc014cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EnterpriseVpnConnectionV5IkepolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5IkepolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a23f359da122e72e19a101611a51275bb66b43e9172bdf5c352824b8e13148)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDpd")
    def put_dpd(
        self,
        *,
        interval: typing.Optional[jsii.Number] = None,
        msg: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#interval EnterpriseVpnConnectionV5#interval}.
        :param msg: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#msg EnterpriseVpnConnectionV5#msg}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#timeout EnterpriseVpnConnectionV5#timeout}.
        '''
        value = EnterpriseVpnConnectionV5IkepolicyDpd(
            interval=interval, msg=msg, timeout=timeout
        )

        return typing.cast(None, jsii.invoke(self, "putDpd", [value]))

    @jsii.member(jsii_name="resetAuthenticationAlgorithm")
    def reset_authentication_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationAlgorithm", []))

    @jsii.member(jsii_name="resetAuthenticationMethod")
    def reset_authentication_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMethod", []))

    @jsii.member(jsii_name="resetDhGroup")
    def reset_dh_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhGroup", []))

    @jsii.member(jsii_name="resetDpd")
    def reset_dpd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpd", []))

    @jsii.member(jsii_name="resetEncryptionAlgorithm")
    def reset_encryption_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAlgorithm", []))

    @jsii.member(jsii_name="resetIkeVersion")
    def reset_ike_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIkeVersion", []))

    @jsii.member(jsii_name="resetLifetimeSeconds")
    def reset_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetimeSeconds", []))

    @jsii.member(jsii_name="resetLocalId")
    def reset_local_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalId", []))

    @jsii.member(jsii_name="resetLocalIdType")
    def reset_local_id_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalIdType", []))

    @jsii.member(jsii_name="resetPeerId")
    def reset_peer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerId", []))

    @jsii.member(jsii_name="resetPeerIdType")
    def reset_peer_id_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerIdType", []))

    @jsii.member(jsii_name="resetPhaseOneNegotiationMode")
    def reset_phase_one_negotiation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhaseOneNegotiationMode", []))

    @builtins.property
    @jsii.member(jsii_name="dpd")
    def dpd(self) -> EnterpriseVpnConnectionV5IkepolicyDpdOutputReference:
        return typing.cast(EnterpriseVpnConnectionV5IkepolicyDpdOutputReference, jsii.get(self, "dpd"))

    @builtins.property
    @jsii.member(jsii_name="authenticationAlgorithmInput")
    def authentication_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMethodInput")
    def authentication_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="dhGroupInput")
    def dh_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dhGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="dpdInput")
    def dpd_input(self) -> typing.Optional[EnterpriseVpnConnectionV5IkepolicyDpd]:
        return typing.cast(typing.Optional[EnterpriseVpnConnectionV5IkepolicyDpd], jsii.get(self, "dpdInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithmInput")
    def encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeVersionInput")
    def ike_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ikeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetimeSecondsInput")
    def lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="localIdInput")
    def local_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIdInput"))

    @builtins.property
    @jsii.member(jsii_name="localIdTypeInput")
    def local_id_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIdInput")
    def peer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIdTypeInput")
    def peer_id_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIdTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="phaseOneNegotiationModeInput")
    def phase_one_negotiation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phaseOneNegotiationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationAlgorithm")
    def authentication_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationAlgorithm"))

    @authentication_algorithm.setter
    def authentication_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228b02a830dd2ad3cd590abf62e2b1c3d3fc36d2c29c47d8f24a9005343e8d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationMethod")
    def authentication_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMethod"))

    @authentication_method.setter
    def authentication_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ac2fb95fb3a1b9715ddfeee253d6b996877fc399f4584f0eee61e6d042d8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dhGroup")
    def dh_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dhGroup"))

    @dh_group.setter
    def dh_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef2694cf665b6bb5da6dc91db0d95a41ed62469f2b2d80a08c1254b9d731e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dhGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithm")
    def encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAlgorithm"))

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffb9ff2ea1feed858dfa24c86215d7146dc26bc9c250d389fdc345dd7c063f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ikeVersion")
    def ike_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeVersion"))

    @ike_version.setter
    def ike_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60f697b291a2be57c4d9b6a867d5ea14f0de41e0f47b1a554c64d325e708a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lifetimeSeconds")
    def lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lifetimeSeconds"))

    @lifetime_seconds.setter
    def lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f027b79363ad619c0f9a1fd688ad4ebefc7a8b6db55e69cdf799a97b4b69c96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localId")
    def local_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localId"))

    @local_id.setter
    def local_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d7366225a6561261c41ec5be32022a0dd70647edda497cdbca791703430336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localIdType")
    def local_id_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIdType"))

    @local_id_type.setter
    def local_id_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3125ed112093de52aadd74b03964ce9eb172b40bde2c906d2abd947c19d61fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerId")
    def peer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerId"))

    @peer_id.setter
    def peer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a0c4071747b46adac19ae1ba3681581a546fb9687857ca66227f1a0f847e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerIdType")
    def peer_id_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIdType"))

    @peer_id_type.setter
    def peer_id_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36bdc65e43af6a91457ba09915b002128085d6dc52887f36e19766c483eaf91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIdType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phaseOneNegotiationMode")
    def phase_one_negotiation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phaseOneNegotiationMode"))

    @phase_one_negotiation_mode.setter
    def phase_one_negotiation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510ba0fa0be49e5057db85463099df3e216ec5fa6afbdbe4aea39bbe62124cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phaseOneNegotiationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnterpriseVpnConnectionV5Ikepolicy]:
        return typing.cast(typing.Optional[EnterpriseVpnConnectionV5Ikepolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnterpriseVpnConnectionV5Ikepolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50aba0ee9f3c06888dd38fed16272df8ba9aef17a8515260e738f1b70cf7bec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5Ipsecpolicy",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_algorithm": "authenticationAlgorithm",
        "encapsulation_mode": "encapsulationMode",
        "encryption_algorithm": "encryptionAlgorithm",
        "lifetime_seconds": "lifetimeSeconds",
        "pfs": "pfs",
        "transform_protocol": "transformProtocol",
    },
)
class EnterpriseVpnConnectionV5Ipsecpolicy:
    def __init__(
        self,
        *,
        authentication_algorithm: typing.Optional[builtins.str] = None,
        encapsulation_mode: typing.Optional[builtins.str] = None,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        lifetime_seconds: typing.Optional[jsii.Number] = None,
        pfs: typing.Optional[builtins.str] = None,
        transform_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_algorithm EnterpriseVpnConnectionV5#authentication_algorithm}.
        :param encapsulation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encapsulation_mode EnterpriseVpnConnectionV5#encapsulation_mode}.
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encryption_algorithm EnterpriseVpnConnectionV5#encryption_algorithm}.
        :param lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#lifetime_seconds EnterpriseVpnConnectionV5#lifetime_seconds}.
        :param pfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#pfs EnterpriseVpnConnectionV5#pfs}.
        :param transform_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#transform_protocol EnterpriseVpnConnectionV5#transform_protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7dfe1d64ac677630076ff1bb1f345bae8779c62f1b940662afcf6120861ecc3)
            check_type(argname="argument authentication_algorithm", value=authentication_algorithm, expected_type=type_hints["authentication_algorithm"])
            check_type(argname="argument encapsulation_mode", value=encapsulation_mode, expected_type=type_hints["encapsulation_mode"])
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument lifetime_seconds", value=lifetime_seconds, expected_type=type_hints["lifetime_seconds"])
            check_type(argname="argument pfs", value=pfs, expected_type=type_hints["pfs"])
            check_type(argname="argument transform_protocol", value=transform_protocol, expected_type=type_hints["transform_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_algorithm is not None:
            self._values["authentication_algorithm"] = authentication_algorithm
        if encapsulation_mode is not None:
            self._values["encapsulation_mode"] = encapsulation_mode
        if encryption_algorithm is not None:
            self._values["encryption_algorithm"] = encryption_algorithm
        if lifetime_seconds is not None:
            self._values["lifetime_seconds"] = lifetime_seconds
        if pfs is not None:
            self._values["pfs"] = pfs
        if transform_protocol is not None:
            self._values["transform_protocol"] = transform_protocol

    @builtins.property
    def authentication_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#authentication_algorithm EnterpriseVpnConnectionV5#authentication_algorithm}.'''
        result = self._values.get("authentication_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encapsulation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encapsulation_mode EnterpriseVpnConnectionV5#encapsulation_mode}.'''
        result = self._values.get("encapsulation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#encryption_algorithm EnterpriseVpnConnectionV5#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#lifetime_seconds EnterpriseVpnConnectionV5#lifetime_seconds}.'''
        result = self._values.get("lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pfs(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#pfs EnterpriseVpnConnectionV5#pfs}.'''
        result = self._values.get("pfs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transform_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#transform_protocol EnterpriseVpnConnectionV5#transform_protocol}.'''
        result = self._values.get("transform_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnConnectionV5Ipsecpolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpnConnectionV5IpsecpolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5IpsecpolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5942fffd85cf1069b3597a905fe3dfff1abbb56b83020907ae3719355ce7dfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationAlgorithm")
    def reset_authentication_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationAlgorithm", []))

    @jsii.member(jsii_name="resetEncapsulationMode")
    def reset_encapsulation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncapsulationMode", []))

    @jsii.member(jsii_name="resetEncryptionAlgorithm")
    def reset_encryption_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAlgorithm", []))

    @jsii.member(jsii_name="resetLifetimeSeconds")
    def reset_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetimeSeconds", []))

    @jsii.member(jsii_name="resetPfs")
    def reset_pfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPfs", []))

    @jsii.member(jsii_name="resetTransformProtocol")
    def reset_transform_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationAlgorithmInput")
    def authentication_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="encapsulationModeInput")
    def encapsulation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encapsulationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithmInput")
    def encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetimeSecondsInput")
    def lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pfsInput")
    def pfs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pfsInput"))

    @builtins.property
    @jsii.member(jsii_name="transformProtocolInput")
    def transform_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transformProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationAlgorithm")
    def authentication_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationAlgorithm"))

    @authentication_algorithm.setter
    def authentication_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54bf316a5b3265ab6c62af7de671fd1db42a00616b143cbc3836bed0c51f44cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encapsulationMode")
    def encapsulation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encapsulationMode"))

    @encapsulation_mode.setter
    def encapsulation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9116ad4b1c2607e348f61918bc6617d99259b898ce272b9322068205a2f2cff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encapsulationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithm")
    def encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAlgorithm"))

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1756f792515f8e103bd1839e3f9b816cc8004e71384a447789775923edbd7827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lifetimeSeconds")
    def lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lifetimeSeconds"))

    @lifetime_seconds.setter
    def lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257495ee7c9cac8a4e6f2f5f9a8f15bb666e25eb4ca6cd25b47880b6f7cc9e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pfs")
    def pfs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pfs"))

    @pfs.setter
    def pfs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4d58b280bace16ced29d4aa0f54d88e232ffd877b2b5d3d1543298fc8e6c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pfs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transformProtocol")
    def transform_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transformProtocol"))

    @transform_protocol.setter
    def transform_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9878cd62d6e0e2f42db42216dff8e2cecbdb0779b51d052607f750f9b741c00e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnterpriseVpnConnectionV5Ipsecpolicy]:
        return typing.cast(typing.Optional[EnterpriseVpnConnectionV5Ipsecpolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnterpriseVpnConnectionV5Ipsecpolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1321599581f793261159fc3b277df882ba656138c18c14b9b97340c32a65737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5PolicyRules",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "rule_index": "ruleIndex",
        "source": "source",
    },
)
class EnterpriseVpnConnectionV5PolicyRules:
    def __init__(
        self,
        *,
        destination: typing.Optional[typing.Sequence[builtins.str]] = None,
        rule_index: typing.Optional[jsii.Number] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#destination EnterpriseVpnConnectionV5#destination}.
        :param rule_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#rule_index EnterpriseVpnConnectionV5#rule_index}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#source EnterpriseVpnConnectionV5#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa9988e58c25e2f1f77b22b8de60b3bba8701c5d011b10e2b5fe27346c8b8f5)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument rule_index", value=rule_index, expected_type=type_hints["rule_index"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if rule_index is not None:
            self._values["rule_index"] = rule_index
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def destination(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#destination EnterpriseVpnConnectionV5#destination}.'''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rule_index(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#rule_index EnterpriseVpnConnectionV5#rule_index}.'''
        result = self._values.get("rule_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#source EnterpriseVpnConnectionV5#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnConnectionV5PolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpnConnectionV5PolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5PolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd745b5091d33e32933d63ddf87a49b18475f1093f69a896277fc547497cc15f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EnterpriseVpnConnectionV5PolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d077929b4688a527569c1ed567449e753e11615d1659264b4ccc913220c34fc9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EnterpriseVpnConnectionV5PolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27f49bc66a69e7b78cd88f22ea79241ab970ee5f7b1e0a332c94fd84c265479)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d10f24a3767429feaea9c1340a6b92d90f754bb11874f5ba759c5feb916cb4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b73375c2a1822e4656b383dcd1655a3ef2a6b3182299136f03565fc8fb7c9620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnterpriseVpnConnectionV5PolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnterpriseVpnConnectionV5PolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnterpriseVpnConnectionV5PolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e481d7cee4849148abd8b6bb253259109a89ef61231f4371c3d3db6f7ed358f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EnterpriseVpnConnectionV5PolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5PolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__095e19e056e1f365db68e53fdc995b010364a37cea0b53cf6951d25c60a3addb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @jsii.member(jsii_name="resetRuleIndex")
    def reset_rule_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleIndex", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIndexInput")
    def rule_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96397f0ce8f2ad2d6a44bc0d5ded3c9335d888621622c154141a0eb7e68e0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleIndex")
    def rule_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleIndex"))

    @rule_index.setter
    def rule_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ffbdeb392999c9c226e88ec9a7c05812245db3df1b7bd34ff2d13b0d03a571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9597790804913a8c995b1611b826f9d8bb30e2627b616f4ee0f57da876a2f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5PolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5PolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5PolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67db52a4e674d6ac3501ef415f64ea27ac8caed6e7076e82809698611abbfed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class EnterpriseVpnConnectionV5Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#create EnterpriseVpnConnectionV5#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#delete EnterpriseVpnConnectionV5#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#update EnterpriseVpnConnectionV5#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590af6c1fe566ea164940e8ee047855c45c32ca41f949b1ad309ee1c34828c23)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#create EnterpriseVpnConnectionV5#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#delete EnterpriseVpnConnectionV5#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/enterprise_vpn_connection_v5#update EnterpriseVpnConnectionV5#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnterpriseVpnConnectionV5Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnterpriseVpnConnectionV5TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.enterpriseVpnConnectionV5.EnterpriseVpnConnectionV5TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b16e90c82e4ebaa6c55c44685caffae3936fb1d31058b5cdf0cdf24b201334)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2001e070c35bd3afa7a62d62b8516118696939f3038886a2b03c01222839956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e39eb8ff7c306ca2ef07c15cdf41798299819e8ddffb00da84e16a9d225841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cce14dd309b5165f6391902518703fa5e409aaf5fdc58742f97d5f7762d9adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacf5cf576a8ea12da5fa0ddc2387aefa1d9b2221916724b08a5cfca37e32697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EnterpriseVpnConnectionV5",
    "EnterpriseVpnConnectionV5Config",
    "EnterpriseVpnConnectionV5Ikepolicy",
    "EnterpriseVpnConnectionV5IkepolicyDpd",
    "EnterpriseVpnConnectionV5IkepolicyDpdOutputReference",
    "EnterpriseVpnConnectionV5IkepolicyOutputReference",
    "EnterpriseVpnConnectionV5Ipsecpolicy",
    "EnterpriseVpnConnectionV5IpsecpolicyOutputReference",
    "EnterpriseVpnConnectionV5PolicyRules",
    "EnterpriseVpnConnectionV5PolicyRulesList",
    "EnterpriseVpnConnectionV5PolicyRulesOutputReference",
    "EnterpriseVpnConnectionV5Timeouts",
    "EnterpriseVpnConnectionV5TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b33e29d1898cd2903a0147dde3242302c835f0dc8d6fc5b9a8f985408530bb57(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    customer_gateway_id: builtins.str,
    gateway_id: builtins.str,
    gateway_ip: builtins.str,
    name: builtins.str,
    psk: builtins.str,
    vpn_type: builtins.str,
    enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_role: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ikepolicy: typing.Optional[typing.Union[EnterpriseVpnConnectionV5Ikepolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ipsecpolicy: typing.Optional[typing.Union[EnterpriseVpnConnectionV5Ipsecpolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnterpriseVpnConnectionV5PolicyRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EnterpriseVpnConnectionV5Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel_local_address: typing.Optional[builtins.str] = None,
    tunnel_peer_address: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8296ddcd4f76f5d2f23482fdf12242203473064de223689aec71e0e7510667c5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b32ec56ae6e2afae50f659d2d661350b6e010052d0e0bb44386fb2bb1555956(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnterpriseVpnConnectionV5PolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a180eae6a4c88e550a8998125c8749fcd75b4bf3993e888bb8a38b359df3ee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405e04f4df62fdeb4a6722e38660601db4957230004d33a86627e4c3a1d0d35b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e9374520f7eba91a368cee38c37833ee306ff06a8e739920c22276b8c83d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4789198a7bb1bc9c3ddff6ece2273c2be28e6a2d004cb125b74be40b6faa7c02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e836abb2bdfde92d7f202237b6305758a201d5889404054139456d3ae484b412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9999c85fbe454fefe2dcd6f2851f3c2e29f409a5d25806039aa497c5977d77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0c0e199f4bf7698b86c8951e6c57febb9e20211e0294255717653cb29675b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b824860456046db1c65b9fb999c8d2661a30cbf7817af82f98b0888aeef13eb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ff10ef61b1ebc58c8bcdbd2ea664154c7a31098782ef5ffc204cc1f3eb5d91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec029bd6e7430bd3515ba08db88d43b6b1eba9c3a23953526a2f0bf1c4dc636d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f7c7f39c1b47a8e6fffbd61eb364e1d6ede7672d56f1601cfbb1d94c167ef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90acc804493177ea2213c72fd5cac64764fdded59e7c36f56a2f53ab32edd87c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7663df606f986f9f36a74377cea62fc8b8a81a36aac08c8cc52f1159a2a42aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c511d4507ea580aeddbc319b323ff746cd6a1db830d8f5105a7869d69bc33ed(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    customer_gateway_id: builtins.str,
    gateway_id: builtins.str,
    gateway_ip: builtins.str,
    name: builtins.str,
    psk: builtins.str,
    vpn_type: builtins.str,
    enable_nqa: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_role: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ikepolicy: typing.Optional[typing.Union[EnterpriseVpnConnectionV5Ikepolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    ipsecpolicy: typing.Optional[typing.Union[EnterpriseVpnConnectionV5Ipsecpolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnterpriseVpnConnectionV5PolicyRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[EnterpriseVpnConnectionV5Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel_local_address: typing.Optional[builtins.str] = None,
    tunnel_peer_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215c5334ff511b43f15db0c3618baa3f7fe14f74dfc1161907898c08e17ec764(
    *,
    authentication_algorithm: typing.Optional[builtins.str] = None,
    authentication_method: typing.Optional[builtins.str] = None,
    dh_group: typing.Optional[builtins.str] = None,
    dpd: typing.Optional[typing.Union[EnterpriseVpnConnectionV5IkepolicyDpd, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    ike_version: typing.Optional[builtins.str] = None,
    lifetime_seconds: typing.Optional[jsii.Number] = None,
    local_id: typing.Optional[builtins.str] = None,
    local_id_type: typing.Optional[builtins.str] = None,
    peer_id: typing.Optional[builtins.str] = None,
    peer_id_type: typing.Optional[builtins.str] = None,
    phase_one_negotiation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a78c49931ea4dee71c20c187a99405048901004bd87899530504b31f176ec19(
    *,
    interval: typing.Optional[jsii.Number] = None,
    msg: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd2851731872ca495399d09baa38bfaba74443f353f31fe79ba398b5fb0287a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07979a0f08300207ba4cab8118d8e03adb35130850c1297e4747200b1b82847(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528b26992e7fa7f8a8a903167b10a28d0977dec8853bc49d1c135c5ca9960f43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28c32887a2df7316cde007627e4ae4d2a75124c7adf47532b5a134fd377a953(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad27d7032bb6261f464dcd703290860571b30f8e6ba1d2d0ea6f4b63fc014cc6(
    value: typing.Optional[EnterpriseVpnConnectionV5IkepolicyDpd],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a23f359da122e72e19a101611a51275bb66b43e9172bdf5c352824b8e13148(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228b02a830dd2ad3cd590abf62e2b1c3d3fc36d2c29c47d8f24a9005343e8d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ac2fb95fb3a1b9715ddfeee253d6b996877fc399f4584f0eee61e6d042d8e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef2694cf665b6bb5da6dc91db0d95a41ed62469f2b2d80a08c1254b9d731e1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffb9ff2ea1feed858dfa24c86215d7146dc26bc9c250d389fdc345dd7c063f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60f697b291a2be57c4d9b6a867d5ea14f0de41e0f47b1a554c64d325e708a45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f027b79363ad619c0f9a1fd688ad4ebefc7a8b6db55e69cdf799a97b4b69c96d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d7366225a6561261c41ec5be32022a0dd70647edda497cdbca791703430336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3125ed112093de52aadd74b03964ce9eb172b40bde2c906d2abd947c19d61fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a0c4071747b46adac19ae1ba3681581a546fb9687857ca66227f1a0f847e4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36bdc65e43af6a91457ba09915b002128085d6dc52887f36e19766c483eaf91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510ba0fa0be49e5057db85463099df3e216ec5fa6afbdbe4aea39bbe62124cd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50aba0ee9f3c06888dd38fed16272df8ba9aef17a8515260e738f1b70cf7bec2(
    value: typing.Optional[EnterpriseVpnConnectionV5Ikepolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dfe1d64ac677630076ff1bb1f345bae8779c62f1b940662afcf6120861ecc3(
    *,
    authentication_algorithm: typing.Optional[builtins.str] = None,
    encapsulation_mode: typing.Optional[builtins.str] = None,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    lifetime_seconds: typing.Optional[jsii.Number] = None,
    pfs: typing.Optional[builtins.str] = None,
    transform_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5942fffd85cf1069b3597a905fe3dfff1abbb56b83020907ae3719355ce7dfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bf316a5b3265ab6c62af7de671fd1db42a00616b143cbc3836bed0c51f44cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9116ad4b1c2607e348f61918bc6617d99259b898ce272b9322068205a2f2cff9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1756f792515f8e103bd1839e3f9b816cc8004e71384a447789775923edbd7827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257495ee7c9cac8a4e6f2f5f9a8f15bb666e25eb4ca6cd25b47880b6f7cc9e23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4d58b280bace16ced29d4aa0f54d88e232ffd877b2b5d3d1543298fc8e6c8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9878cd62d6e0e2f42db42216dff8e2cecbdb0779b51d052607f750f9b741c00e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1321599581f793261159fc3b277df882ba656138c18c14b9b97340c32a65737(
    value: typing.Optional[EnterpriseVpnConnectionV5Ipsecpolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa9988e58c25e2f1f77b22b8de60b3bba8701c5d011b10e2b5fe27346c8b8f5(
    *,
    destination: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_index: typing.Optional[jsii.Number] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd745b5091d33e32933d63ddf87a49b18475f1093f69a896277fc547497cc15f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d077929b4688a527569c1ed567449e753e11615d1659264b4ccc913220c34fc9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27f49bc66a69e7b78cd88f22ea79241ab970ee5f7b1e0a332c94fd84c265479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d10f24a3767429feaea9c1340a6b92d90f754bb11874f5ba759c5feb916cb4a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73375c2a1822e4656b383dcd1655a3ef2a6b3182299136f03565fc8fb7c9620(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e481d7cee4849148abd8b6bb253259109a89ef61231f4371c3d3db6f7ed358f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnterpriseVpnConnectionV5PolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095e19e056e1f365db68e53fdc995b010364a37cea0b53cf6951d25c60a3addb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96397f0ce8f2ad2d6a44bc0d5ded3c9335d888621622c154141a0eb7e68e0a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ffbdeb392999c9c226e88ec9a7c05812245db3df1b7bd34ff2d13b0d03a571(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9597790804913a8c995b1611b826f9d8bb30e2627b616f4ee0f57da876a2f63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67db52a4e674d6ac3501ef415f64ea27ac8caed6e7076e82809698611abbfed7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5PolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590af6c1fe566ea164940e8ee047855c45c32ca41f949b1ad309ee1c34828c23(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b16e90c82e4ebaa6c55c44685caffae3936fb1d31058b5cdf0cdf24b201334(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2001e070c35bd3afa7a62d62b8516118696939f3038886a2b03c01222839956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e39eb8ff7c306ca2ef07c15cdf41798299819e8ddffb00da84e16a9d225841(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cce14dd309b5165f6391902518703fa5e409aaf5fdc58742f97d5f7762d9adb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacf5cf576a8ea12da5fa0ddc2387aefa1d9b2221916724b08a5cfca37e32697(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnterpriseVpnConnectionV5Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
