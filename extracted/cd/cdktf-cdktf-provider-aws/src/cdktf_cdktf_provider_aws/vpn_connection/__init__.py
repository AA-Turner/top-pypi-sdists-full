r'''
# `aws_vpn_connection`

Refer to the Terraform Registry for docs: [`aws_vpn_connection`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection).
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


class VpnConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection aws_vpn_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        customer_gateway_id: builtins.str,
        type: builtins.str,
        enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        outside_ip_address_type: typing.Optional[builtins.str] = None,
        remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transit_gateway_id: typing.Optional[builtins.str] = None,
        transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel1_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_preshared_key: typing.Optional[builtins.str] = None,
        tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel1_startup_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel2_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_preshared_key: typing.Optional[builtins.str] = None,
        tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel2_startup_action: typing.Optional[builtins.str] = None,
        tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
        vpn_gateway_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection aws_vpn_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param customer_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#customer_gateway_id VpnConnection#customer_gateway_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#type VpnConnection#type}.
        :param enable_acceleration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#enable_acceleration VpnConnection#enable_acceleration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#id VpnConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#local_ipv4_network_cidr VpnConnection#local_ipv4_network_cidr}.
        :param local_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#local_ipv6_network_cidr VpnConnection#local_ipv6_network_cidr}.
        :param outside_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#outside_ip_address_type VpnConnection#outside_ip_address_type}.
        :param remote_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#remote_ipv4_network_cidr VpnConnection#remote_ipv4_network_cidr}.
        :param remote_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#remote_ipv6_network_cidr VpnConnection#remote_ipv6_network_cidr}.
        :param static_routes_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#static_routes_only VpnConnection#static_routes_only}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tags VpnConnection#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tags_all VpnConnection#tags_all}.
        :param transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#transit_gateway_id VpnConnection#transit_gateway_id}.
        :param transport_transit_gateway_attachment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#transport_transit_gateway_attachment_id VpnConnection#transport_transit_gateway_attachment_id}.
        :param tunnel1_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_action VpnConnection#tunnel1_dpd_timeout_action}.
        :param tunnel1_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_seconds VpnConnection#tunnel1_dpd_timeout_seconds}.
        :param tunnel1_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_enable_tunnel_lifecycle_control VpnConnection#tunnel1_enable_tunnel_lifecycle_control}.
        :param tunnel1_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_ike_versions VpnConnection#tunnel1_ike_versions}.
        :param tunnel1_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_inside_cidr VpnConnection#tunnel1_inside_cidr}.
        :param tunnel1_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_inside_ipv6_cidr VpnConnection#tunnel1_inside_ipv6_cidr}.
        :param tunnel1_log_options: tunnel1_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_log_options VpnConnection#tunnel1_log_options}
        :param tunnel1_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_dh_group_numbers VpnConnection#tunnel1_phase1_dh_group_numbers}.
        :param tunnel1_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_encryption_algorithms VpnConnection#tunnel1_phase1_encryption_algorithms}.
        :param tunnel1_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_integrity_algorithms VpnConnection#tunnel1_phase1_integrity_algorithms}.
        :param tunnel1_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_lifetime_seconds VpnConnection#tunnel1_phase1_lifetime_seconds}.
        :param tunnel1_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_dh_group_numbers VpnConnection#tunnel1_phase2_dh_group_numbers}.
        :param tunnel1_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_encryption_algorithms VpnConnection#tunnel1_phase2_encryption_algorithms}.
        :param tunnel1_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_integrity_algorithms VpnConnection#tunnel1_phase2_integrity_algorithms}.
        :param tunnel1_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_lifetime_seconds VpnConnection#tunnel1_phase2_lifetime_seconds}.
        :param tunnel1_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_preshared_key VpnConnection#tunnel1_preshared_key}.
        :param tunnel1_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_rekey_fuzz_percentage VpnConnection#tunnel1_rekey_fuzz_percentage}.
        :param tunnel1_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_rekey_margin_time_seconds VpnConnection#tunnel1_rekey_margin_time_seconds}.
        :param tunnel1_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_replay_window_size VpnConnection#tunnel1_replay_window_size}.
        :param tunnel1_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_startup_action VpnConnection#tunnel1_startup_action}.
        :param tunnel2_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_action VpnConnection#tunnel2_dpd_timeout_action}.
        :param tunnel2_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_seconds VpnConnection#tunnel2_dpd_timeout_seconds}.
        :param tunnel2_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_enable_tunnel_lifecycle_control VpnConnection#tunnel2_enable_tunnel_lifecycle_control}.
        :param tunnel2_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_ike_versions VpnConnection#tunnel2_ike_versions}.
        :param tunnel2_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_inside_cidr VpnConnection#tunnel2_inside_cidr}.
        :param tunnel2_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_inside_ipv6_cidr VpnConnection#tunnel2_inside_ipv6_cidr}.
        :param tunnel2_log_options: tunnel2_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_log_options VpnConnection#tunnel2_log_options}
        :param tunnel2_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_dh_group_numbers VpnConnection#tunnel2_phase1_dh_group_numbers}.
        :param tunnel2_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_encryption_algorithms VpnConnection#tunnel2_phase1_encryption_algorithms}.
        :param tunnel2_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_integrity_algorithms VpnConnection#tunnel2_phase1_integrity_algorithms}.
        :param tunnel2_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_lifetime_seconds VpnConnection#tunnel2_phase1_lifetime_seconds}.
        :param tunnel2_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_dh_group_numbers VpnConnection#tunnel2_phase2_dh_group_numbers}.
        :param tunnel2_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_encryption_algorithms VpnConnection#tunnel2_phase2_encryption_algorithms}.
        :param tunnel2_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_integrity_algorithms VpnConnection#tunnel2_phase2_integrity_algorithms}.
        :param tunnel2_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_lifetime_seconds VpnConnection#tunnel2_phase2_lifetime_seconds}.
        :param tunnel2_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_preshared_key VpnConnection#tunnel2_preshared_key}.
        :param tunnel2_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_rekey_fuzz_percentage VpnConnection#tunnel2_rekey_fuzz_percentage}.
        :param tunnel2_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_rekey_margin_time_seconds VpnConnection#tunnel2_rekey_margin_time_seconds}.
        :param tunnel2_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_replay_window_size VpnConnection#tunnel2_replay_window_size}.
        :param tunnel2_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_startup_action VpnConnection#tunnel2_startup_action}.
        :param tunnel_inside_ip_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel_inside_ip_version VpnConnection#tunnel_inside_ip_version}.
        :param vpn_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#vpn_gateway_id VpnConnection#vpn_gateway_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c837b21d9377340ba0b9ae12cf2e76d94617740e84d55b4fefcf3656c729b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VpnConnectionConfig(
            customer_gateway_id=customer_gateway_id,
            type=type,
            enable_acceleration=enable_acceleration,
            id=id,
            local_ipv4_network_cidr=local_ipv4_network_cidr,
            local_ipv6_network_cidr=local_ipv6_network_cidr,
            outside_ip_address_type=outside_ip_address_type,
            remote_ipv4_network_cidr=remote_ipv4_network_cidr,
            remote_ipv6_network_cidr=remote_ipv6_network_cidr,
            static_routes_only=static_routes_only,
            tags=tags,
            tags_all=tags_all,
            transit_gateway_id=transit_gateway_id,
            transport_transit_gateway_attachment_id=transport_transit_gateway_attachment_id,
            tunnel1_dpd_timeout_action=tunnel1_dpd_timeout_action,
            tunnel1_dpd_timeout_seconds=tunnel1_dpd_timeout_seconds,
            tunnel1_enable_tunnel_lifecycle_control=tunnel1_enable_tunnel_lifecycle_control,
            tunnel1_ike_versions=tunnel1_ike_versions,
            tunnel1_inside_cidr=tunnel1_inside_cidr,
            tunnel1_inside_ipv6_cidr=tunnel1_inside_ipv6_cidr,
            tunnel1_log_options=tunnel1_log_options,
            tunnel1_phase1_dh_group_numbers=tunnel1_phase1_dh_group_numbers,
            tunnel1_phase1_encryption_algorithms=tunnel1_phase1_encryption_algorithms,
            tunnel1_phase1_integrity_algorithms=tunnel1_phase1_integrity_algorithms,
            tunnel1_phase1_lifetime_seconds=tunnel1_phase1_lifetime_seconds,
            tunnel1_phase2_dh_group_numbers=tunnel1_phase2_dh_group_numbers,
            tunnel1_phase2_encryption_algorithms=tunnel1_phase2_encryption_algorithms,
            tunnel1_phase2_integrity_algorithms=tunnel1_phase2_integrity_algorithms,
            tunnel1_phase2_lifetime_seconds=tunnel1_phase2_lifetime_seconds,
            tunnel1_preshared_key=tunnel1_preshared_key,
            tunnel1_rekey_fuzz_percentage=tunnel1_rekey_fuzz_percentage,
            tunnel1_rekey_margin_time_seconds=tunnel1_rekey_margin_time_seconds,
            tunnel1_replay_window_size=tunnel1_replay_window_size,
            tunnel1_startup_action=tunnel1_startup_action,
            tunnel2_dpd_timeout_action=tunnel2_dpd_timeout_action,
            tunnel2_dpd_timeout_seconds=tunnel2_dpd_timeout_seconds,
            tunnel2_enable_tunnel_lifecycle_control=tunnel2_enable_tunnel_lifecycle_control,
            tunnel2_ike_versions=tunnel2_ike_versions,
            tunnel2_inside_cidr=tunnel2_inside_cidr,
            tunnel2_inside_ipv6_cidr=tunnel2_inside_ipv6_cidr,
            tunnel2_log_options=tunnel2_log_options,
            tunnel2_phase1_dh_group_numbers=tunnel2_phase1_dh_group_numbers,
            tunnel2_phase1_encryption_algorithms=tunnel2_phase1_encryption_algorithms,
            tunnel2_phase1_integrity_algorithms=tunnel2_phase1_integrity_algorithms,
            tunnel2_phase1_lifetime_seconds=tunnel2_phase1_lifetime_seconds,
            tunnel2_phase2_dh_group_numbers=tunnel2_phase2_dh_group_numbers,
            tunnel2_phase2_encryption_algorithms=tunnel2_phase2_encryption_algorithms,
            tunnel2_phase2_integrity_algorithms=tunnel2_phase2_integrity_algorithms,
            tunnel2_phase2_lifetime_seconds=tunnel2_phase2_lifetime_seconds,
            tunnel2_preshared_key=tunnel2_preshared_key,
            tunnel2_rekey_fuzz_percentage=tunnel2_rekey_fuzz_percentage,
            tunnel2_rekey_margin_time_seconds=tunnel2_rekey_margin_time_seconds,
            tunnel2_replay_window_size=tunnel2_replay_window_size,
            tunnel2_startup_action=tunnel2_startup_action,
            tunnel_inside_ip_version=tunnel_inside_ip_version,
            vpn_gateway_id=vpn_gateway_id,
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
        '''Generates CDKTF code for importing a VpnConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VpnConnection to import.
        :param import_from_id: The id of the existing VpnConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VpnConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfe8e658651598180faa7792178e757e1594cab1c5725d4bf79aa7cb299ad78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTunnel1LogOptions")
    def put_tunnel1_log_options(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        value = VpnConnectionTunnel1LogOptions(
            cloudwatch_log_options=cloudwatch_log_options
        )

        return typing.cast(None, jsii.invoke(self, "putTunnel1LogOptions", [value]))

    @jsii.member(jsii_name="putTunnel2LogOptions")
    def put_tunnel2_log_options(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        value = VpnConnectionTunnel2LogOptions(
            cloudwatch_log_options=cloudwatch_log_options
        )

        return typing.cast(None, jsii.invoke(self, "putTunnel2LogOptions", [value]))

    @jsii.member(jsii_name="resetEnableAcceleration")
    def reset_enable_acceleration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAcceleration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalIpv4NetworkCidr")
    def reset_local_ipv4_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalIpv4NetworkCidr", []))

    @jsii.member(jsii_name="resetLocalIpv6NetworkCidr")
    def reset_local_ipv6_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalIpv6NetworkCidr", []))

    @jsii.member(jsii_name="resetOutsideIpAddressType")
    def reset_outside_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutsideIpAddressType", []))

    @jsii.member(jsii_name="resetRemoteIpv4NetworkCidr")
    def reset_remote_ipv4_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteIpv4NetworkCidr", []))

    @jsii.member(jsii_name="resetRemoteIpv6NetworkCidr")
    def reset_remote_ipv6_network_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteIpv6NetworkCidr", []))

    @jsii.member(jsii_name="resetStaticRoutesOnly")
    def reset_static_routes_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticRoutesOnly", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTransitGatewayId")
    def reset_transit_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitGatewayId", []))

    @jsii.member(jsii_name="resetTransportTransitGatewayAttachmentId")
    def reset_transport_transit_gateway_attachment_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransportTransitGatewayAttachmentId", []))

    @jsii.member(jsii_name="resetTunnel1DpdTimeoutAction")
    def reset_tunnel1_dpd_timeout_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1DpdTimeoutAction", []))

    @jsii.member(jsii_name="resetTunnel1DpdTimeoutSeconds")
    def reset_tunnel1_dpd_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1DpdTimeoutSeconds", []))

    @jsii.member(jsii_name="resetTunnel1EnableTunnelLifecycleControl")
    def reset_tunnel1_enable_tunnel_lifecycle_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1EnableTunnelLifecycleControl", []))

    @jsii.member(jsii_name="resetTunnel1IkeVersions")
    def reset_tunnel1_ike_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1IkeVersions", []))

    @jsii.member(jsii_name="resetTunnel1InsideCidr")
    def reset_tunnel1_inside_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1InsideCidr", []))

    @jsii.member(jsii_name="resetTunnel1InsideIpv6Cidr")
    def reset_tunnel1_inside_ipv6_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1InsideIpv6Cidr", []))

    @jsii.member(jsii_name="resetTunnel1LogOptions")
    def reset_tunnel1_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1LogOptions", []))

    @jsii.member(jsii_name="resetTunnel1Phase1DhGroupNumbers")
    def reset_tunnel1_phase1_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel1Phase1EncryptionAlgorithms")
    def reset_tunnel1_phase1_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase1IntegrityAlgorithms")
    def reset_tunnel1_phase1_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase1LifetimeSeconds")
    def reset_tunnel1_phase1_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase1LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel1Phase2DhGroupNumbers")
    def reset_tunnel1_phase2_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel1Phase2EncryptionAlgorithms")
    def reset_tunnel1_phase2_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase2IntegrityAlgorithms")
    def reset_tunnel1_phase2_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel1Phase2LifetimeSeconds")
    def reset_tunnel1_phase2_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1Phase2LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel1PresharedKey")
    def reset_tunnel1_preshared_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1PresharedKey", []))

    @jsii.member(jsii_name="resetTunnel1RekeyFuzzPercentage")
    def reset_tunnel1_rekey_fuzz_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1RekeyFuzzPercentage", []))

    @jsii.member(jsii_name="resetTunnel1RekeyMarginTimeSeconds")
    def reset_tunnel1_rekey_margin_time_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1RekeyMarginTimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel1ReplayWindowSize")
    def reset_tunnel1_replay_window_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1ReplayWindowSize", []))

    @jsii.member(jsii_name="resetTunnel1StartupAction")
    def reset_tunnel1_startup_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel1StartupAction", []))

    @jsii.member(jsii_name="resetTunnel2DpdTimeoutAction")
    def reset_tunnel2_dpd_timeout_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2DpdTimeoutAction", []))

    @jsii.member(jsii_name="resetTunnel2DpdTimeoutSeconds")
    def reset_tunnel2_dpd_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2DpdTimeoutSeconds", []))

    @jsii.member(jsii_name="resetTunnel2EnableTunnelLifecycleControl")
    def reset_tunnel2_enable_tunnel_lifecycle_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2EnableTunnelLifecycleControl", []))

    @jsii.member(jsii_name="resetTunnel2IkeVersions")
    def reset_tunnel2_ike_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2IkeVersions", []))

    @jsii.member(jsii_name="resetTunnel2InsideCidr")
    def reset_tunnel2_inside_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2InsideCidr", []))

    @jsii.member(jsii_name="resetTunnel2InsideIpv6Cidr")
    def reset_tunnel2_inside_ipv6_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2InsideIpv6Cidr", []))

    @jsii.member(jsii_name="resetTunnel2LogOptions")
    def reset_tunnel2_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2LogOptions", []))

    @jsii.member(jsii_name="resetTunnel2Phase1DhGroupNumbers")
    def reset_tunnel2_phase1_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel2Phase1EncryptionAlgorithms")
    def reset_tunnel2_phase1_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase1IntegrityAlgorithms")
    def reset_tunnel2_phase1_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase1LifetimeSeconds")
    def reset_tunnel2_phase1_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase1LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel2Phase2DhGroupNumbers")
    def reset_tunnel2_phase2_dh_group_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2DhGroupNumbers", []))

    @jsii.member(jsii_name="resetTunnel2Phase2EncryptionAlgorithms")
    def reset_tunnel2_phase2_encryption_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2EncryptionAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase2IntegrityAlgorithms")
    def reset_tunnel2_phase2_integrity_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2IntegrityAlgorithms", []))

    @jsii.member(jsii_name="resetTunnel2Phase2LifetimeSeconds")
    def reset_tunnel2_phase2_lifetime_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2Phase2LifetimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel2PresharedKey")
    def reset_tunnel2_preshared_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2PresharedKey", []))

    @jsii.member(jsii_name="resetTunnel2RekeyFuzzPercentage")
    def reset_tunnel2_rekey_fuzz_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2RekeyFuzzPercentage", []))

    @jsii.member(jsii_name="resetTunnel2RekeyMarginTimeSeconds")
    def reset_tunnel2_rekey_margin_time_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2RekeyMarginTimeSeconds", []))

    @jsii.member(jsii_name="resetTunnel2ReplayWindowSize")
    def reset_tunnel2_replay_window_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2ReplayWindowSize", []))

    @jsii.member(jsii_name="resetTunnel2StartupAction")
    def reset_tunnel2_startup_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnel2StartupAction", []))

    @jsii.member(jsii_name="resetTunnelInsideIpVersion")
    def reset_tunnel_inside_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelInsideIpVersion", []))

    @jsii.member(jsii_name="resetVpnGatewayId")
    def reset_vpn_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnGatewayId", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkArn")
    def core_network_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkAttachmentArn")
    def core_network_attachment_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNetworkAttachmentArn"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayConfiguration")
    def customer_gateway_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> "VpnConnectionRoutesList":
        return typing.cast("VpnConnectionRoutesList", jsii.get(self, "routes"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Address")
    def tunnel1_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1Address"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1BgpAsn")
    def tunnel1_bgp_asn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1BgpAsn"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1BgpHoldtime")
    def tunnel1_bgp_holdtime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1BgpHoldtime"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1CgwInsideAddress")
    def tunnel1_cgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1CgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1LogOptions")
    def tunnel1_log_options(self) -> "VpnConnectionTunnel1LogOptionsOutputReference":
        return typing.cast("VpnConnectionTunnel1LogOptionsOutputReference", jsii.get(self, "tunnel1LogOptions"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1VgwInsideAddress")
    def tunnel1_vgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1VgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Address")
    def tunnel2_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2Address"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2BgpAsn")
    def tunnel2_bgp_asn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2BgpAsn"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2BgpHoldtime")
    def tunnel2_bgp_holdtime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2BgpHoldtime"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2CgwInsideAddress")
    def tunnel2_cgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2CgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2LogOptions")
    def tunnel2_log_options(self) -> "VpnConnectionTunnel2LogOptionsOutputReference":
        return typing.cast("VpnConnectionTunnel2LogOptionsOutputReference", jsii.get(self, "tunnel2LogOptions"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2VgwInsideAddress")
    def tunnel2_vgw_inside_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2VgwInsideAddress"))

    @builtins.property
    @jsii.member(jsii_name="vgwTelemetry")
    def vgw_telemetry(self) -> "VpnConnectionVgwTelemetryList":
        return typing.cast("VpnConnectionVgwTelemetryList", jsii.get(self, "vgwTelemetry"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayIdInput")
    def customer_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAccelerationInput")
    def enable_acceleration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAccelerationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localIpv4NetworkCidrInput")
    def local_ipv4_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIpv4NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="localIpv6NetworkCidrInput")
    def local_ipv6_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIpv6NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="outsideIpAddressTypeInput")
    def outside_ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outsideIpAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIpv4NetworkCidrInput")
    def remote_ipv4_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIpv4NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIpv6NetworkCidrInput")
    def remote_ipv6_network_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIpv6NetworkCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="staticRoutesOnlyInput")
    def static_routes_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "staticRoutesOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayIdInput")
    def transit_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="transportTransitGatewayAttachmentIdInput")
    def transport_transit_gateway_attachment_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transportTransitGatewayAttachmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutActionInput")
    def tunnel1_dpd_timeout_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1DpdTimeoutActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutSecondsInput")
    def tunnel1_dpd_timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1DpdTimeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1EnableTunnelLifecycleControlInput")
    def tunnel1_enable_tunnel_lifecycle_control_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tunnel1EnableTunnelLifecycleControlInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1IkeVersionsInput")
    def tunnel1_ike_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1IkeVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideCidrInput")
    def tunnel1_inside_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1InsideCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideIpv6CidrInput")
    def tunnel1_inside_ipv6_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1InsideIpv6CidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1LogOptionsInput")
    def tunnel1_log_options_input(
        self,
    ) -> typing.Optional["VpnConnectionTunnel1LogOptions"]:
        return typing.cast(typing.Optional["VpnConnectionTunnel1LogOptions"], jsii.get(self, "tunnel1LogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1DhGroupNumbersInput")
    def tunnel1_phase1_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel1Phase1DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1EncryptionAlgorithmsInput")
    def tunnel1_phase1_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase1EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1IntegrityAlgorithmsInput")
    def tunnel1_phase1_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase1IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1LifetimeSecondsInput")
    def tunnel1_phase1_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1Phase1LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2DhGroupNumbersInput")
    def tunnel1_phase2_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel1Phase2DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2EncryptionAlgorithmsInput")
    def tunnel1_phase2_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase2EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2IntegrityAlgorithmsInput")
    def tunnel1_phase2_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel1Phase2IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2LifetimeSecondsInput")
    def tunnel1_phase2_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1Phase2LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1PresharedKeyInput")
    def tunnel1_preshared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1PresharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyFuzzPercentageInput")
    def tunnel1_rekey_fuzz_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1RekeyFuzzPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyMarginTimeSecondsInput")
    def tunnel1_rekey_margin_time_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1RekeyMarginTimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1ReplayWindowSizeInput")
    def tunnel1_replay_window_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel1ReplayWindowSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel1StartupActionInput")
    def tunnel1_startup_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel1StartupActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutActionInput")
    def tunnel2_dpd_timeout_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2DpdTimeoutActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutSecondsInput")
    def tunnel2_dpd_timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2DpdTimeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2EnableTunnelLifecycleControlInput")
    def tunnel2_enable_tunnel_lifecycle_control_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tunnel2EnableTunnelLifecycleControlInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2IkeVersionsInput")
    def tunnel2_ike_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2IkeVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideCidrInput")
    def tunnel2_inside_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2InsideCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideIpv6CidrInput")
    def tunnel2_inside_ipv6_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2InsideIpv6CidrInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2LogOptionsInput")
    def tunnel2_log_options_input(
        self,
    ) -> typing.Optional["VpnConnectionTunnel2LogOptions"]:
        return typing.cast(typing.Optional["VpnConnectionTunnel2LogOptions"], jsii.get(self, "tunnel2LogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1DhGroupNumbersInput")
    def tunnel2_phase1_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel2Phase1DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1EncryptionAlgorithmsInput")
    def tunnel2_phase1_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase1EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1IntegrityAlgorithmsInput")
    def tunnel2_phase1_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase1IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1LifetimeSecondsInput")
    def tunnel2_phase1_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2Phase1LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2DhGroupNumbersInput")
    def tunnel2_phase2_dh_group_numbers_input(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "tunnel2Phase2DhGroupNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2EncryptionAlgorithmsInput")
    def tunnel2_phase2_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase2EncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2IntegrityAlgorithmsInput")
    def tunnel2_phase2_integrity_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnel2Phase2IntegrityAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2LifetimeSecondsInput")
    def tunnel2_phase2_lifetime_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2Phase2LifetimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2PresharedKeyInput")
    def tunnel2_preshared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2PresharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyFuzzPercentageInput")
    def tunnel2_rekey_fuzz_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2RekeyFuzzPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyMarginTimeSecondsInput")
    def tunnel2_rekey_margin_time_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2RekeyMarginTimeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2ReplayWindowSizeInput")
    def tunnel2_replay_window_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnel2ReplayWindowSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnel2StartupActionInput")
    def tunnel2_startup_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnel2StartupActionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelInsideIpVersionInput")
    def tunnel_inside_ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelInsideIpVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayIdInput")
    def vpn_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnGatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayId"))

    @customer_gateway_id.setter
    def customer_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abf9c46ed4bb3f47680d25cb3bdbf124803bd45f18081f9a4e54dc30d871d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerGatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAcceleration")
    def enable_acceleration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAcceleration"))

    @enable_acceleration.setter
    def enable_acceleration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a597a783571e1a63fd897483ba6e6dd77f08dde93b49b22375eb288c5417645a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAcceleration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a23050816328fa4eed3c02faeb29143aae2459e080b23c2f268f0c86ef29f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localIpv4NetworkCidr")
    def local_ipv4_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIpv4NetworkCidr"))

    @local_ipv4_network_cidr.setter
    def local_ipv4_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e7d198301a19bbc64e3e93c2c19007e0be82e9eeccd5440f09bfebd53c0d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpv4NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localIpv6NetworkCidr")
    def local_ipv6_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIpv6NetworkCidr"))

    @local_ipv6_network_cidr.setter
    def local_ipv6_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37751e859decdfb7116bb6022bd8bbd79cfb93898bf5c1ad46ffaef1e2f256a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpv6NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outsideIpAddressType")
    def outside_ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outsideIpAddressType"))

    @outside_ip_address_type.setter
    def outside_ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac41d1d16fba76525309ff68cf6c0d17aaf279402e148529dedf3600f150ef16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outsideIpAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteIpv4NetworkCidr")
    def remote_ipv4_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteIpv4NetworkCidr"))

    @remote_ipv4_network_cidr.setter
    def remote_ipv4_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f621abb5602035be632a73741ae13a1a8e5615164c90999e37fa70a4d6ea08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpv4NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteIpv6NetworkCidr")
    def remote_ipv6_network_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteIpv6NetworkCidr"))

    @remote_ipv6_network_cidr.setter
    def remote_ipv6_network_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34c6bd2a52f088022c7db1aa5877cdc3911a41303fd2fe55bdf1358ce89e88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpv6NetworkCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="staticRoutesOnly")
    def static_routes_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "staticRoutesOnly"))

    @static_routes_only.setter
    def static_routes_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c079d03293bfbcfb51756d8732ea359494671dc053dc7c84bea5b0ffeeb8425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticRoutesOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84c0e133cce209f66f010e62c6ef4bfd0da57a72e8d737f553dcc91a2142bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4dfaedbd380c34a5bb7674a1d0bac7674080311c5148fbcb6c1315df8a84ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayId"))

    @transit_gateway_id.setter
    def transit_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fa7f3fd69016fed4f0bf9b88c002c4d248d84afde7174f70ab37fe03ff59a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transportTransitGatewayAttachmentId")
    def transport_transit_gateway_attachment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transportTransitGatewayAttachmentId"))

    @transport_transit_gateway_attachment_id.setter
    def transport_transit_gateway_attachment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e45875e21ff17777c7b5d9b2e1691c72e20c852c6ddeb40ca98a1e0c90f8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transportTransitGatewayAttachmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutAction")
    def tunnel1_dpd_timeout_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1DpdTimeoutAction"))

    @tunnel1_dpd_timeout_action.setter
    def tunnel1_dpd_timeout_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c2a3dd896a72bbc0615a0d7a5cdcff5f2f3ad66beabeacb6a1f5e2d514a7ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1DpdTimeoutAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1DpdTimeoutSeconds")
    def tunnel1_dpd_timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1DpdTimeoutSeconds"))

    @tunnel1_dpd_timeout_seconds.setter
    def tunnel1_dpd_timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f3e38dba911e397ef5499f1315ec0227a65ecab0869de2a924d4363b7e8e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1DpdTimeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1EnableTunnelLifecycleControl")
    def tunnel1_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tunnel1EnableTunnelLifecycleControl"))

    @tunnel1_enable_tunnel_lifecycle_control.setter
    def tunnel1_enable_tunnel_lifecycle_control(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18ad954c568f82ca65ae709cd76eb6efe79d3669cfddd87986fc258aa03a328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1EnableTunnelLifecycleControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1IkeVersions")
    def tunnel1_ike_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1IkeVersions"))

    @tunnel1_ike_versions.setter
    def tunnel1_ike_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f5616456ccdb47e0cebbd7e45b37ea91bbb6f3fc9a2fc4f75f8a786676e146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1IkeVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideCidr")
    def tunnel1_inside_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1InsideCidr"))

    @tunnel1_inside_cidr.setter
    def tunnel1_inside_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af8c93af7b53282c10ff31d42c885e3f22979e92732d4521dd5f98a032bbccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1InsideCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1InsideIpv6Cidr")
    def tunnel1_inside_ipv6_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1InsideIpv6Cidr"))

    @tunnel1_inside_ipv6_cidr.setter
    def tunnel1_inside_ipv6_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b884d344dab61d67efb46657582a259df2175b743080585909478875136b1ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1InsideIpv6Cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1DhGroupNumbers")
    def tunnel1_phase1_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel1Phase1DhGroupNumbers"))

    @tunnel1_phase1_dh_group_numbers.setter
    def tunnel1_phase1_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3e7b09ea772631cadf3c061d52a97fba3eba5a67f1cdd55e3f7f92467e18bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1EncryptionAlgorithms")
    def tunnel1_phase1_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase1EncryptionAlgorithms"))

    @tunnel1_phase1_encryption_algorithms.setter
    def tunnel1_phase1_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6879b9f4f272d2675089bdef8423ba5c63d88f148f0a6c5d19d80b72fc6312ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1IntegrityAlgorithms")
    def tunnel1_phase1_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase1IntegrityAlgorithms"))

    @tunnel1_phase1_integrity_algorithms.setter
    def tunnel1_phase1_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04dfec2fc24831a67dd09a344f7bfa1580a4b431166bdb5f8c6eb227f6623b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase1LifetimeSeconds")
    def tunnel1_phase1_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1Phase1LifetimeSeconds"))

    @tunnel1_phase1_lifetime_seconds.setter
    def tunnel1_phase1_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937a07cbe33bb7a614a882a971d7878febfc6393b015dbd5314be3b1dde58a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase1LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2DhGroupNumbers")
    def tunnel1_phase2_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel1Phase2DhGroupNumbers"))

    @tunnel1_phase2_dh_group_numbers.setter
    def tunnel1_phase2_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd43922ca326ebaffd71b834ca7df4f287b0deecbd0c1282c7bf48e59cbb4ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2EncryptionAlgorithms")
    def tunnel1_phase2_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase2EncryptionAlgorithms"))

    @tunnel1_phase2_encryption_algorithms.setter
    def tunnel1_phase2_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d0f1e97372c504072607efa5c8c0e96119fe6aafa21a1408aa1234d749e9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2IntegrityAlgorithms")
    def tunnel1_phase2_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel1Phase2IntegrityAlgorithms"))

    @tunnel1_phase2_integrity_algorithms.setter
    def tunnel1_phase2_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250ffd79498403267529ba8b39da6fabc4812f977737db2a3e52b467cdbd3d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1Phase2LifetimeSeconds")
    def tunnel1_phase2_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1Phase2LifetimeSeconds"))

    @tunnel1_phase2_lifetime_seconds.setter
    def tunnel1_phase2_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd04ef500eeb50e34f25c6744c9d2429d5b7b9229a0e34237ac9ebbfbbc86c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1Phase2LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1PresharedKey")
    def tunnel1_preshared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1PresharedKey"))

    @tunnel1_preshared_key.setter
    def tunnel1_preshared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4591ec1cfc0e35cc36700a843cac4599d1847ebc2d29528b91dd6be5fe3849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1PresharedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyFuzzPercentage")
    def tunnel1_rekey_fuzz_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1RekeyFuzzPercentage"))

    @tunnel1_rekey_fuzz_percentage.setter
    def tunnel1_rekey_fuzz_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ee6ec2e74c01e4f8d655285c6aba68818f2a113b9a9d6f94ad2e100b0b1163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1RekeyFuzzPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1RekeyMarginTimeSeconds")
    def tunnel1_rekey_margin_time_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1RekeyMarginTimeSeconds"))

    @tunnel1_rekey_margin_time_seconds.setter
    def tunnel1_rekey_margin_time_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7ed9561de8f1c8a1744d0bc1ac78163ba1767db2f5266d4137f4f8e3c0b69a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1RekeyMarginTimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1ReplayWindowSize")
    def tunnel1_replay_window_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel1ReplayWindowSize"))

    @tunnel1_replay_window_size.setter
    def tunnel1_replay_window_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb69553aee12ca217627fec0c8f36327657b957fd668a336ce83f05e090b4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1ReplayWindowSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel1StartupAction")
    def tunnel1_startup_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel1StartupAction"))

    @tunnel1_startup_action.setter
    def tunnel1_startup_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946f72627e1e83225abc45f05ede98cb0ff169a5e09fd18320065702cb5cbdfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel1StartupAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutAction")
    def tunnel2_dpd_timeout_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2DpdTimeoutAction"))

    @tunnel2_dpd_timeout_action.setter
    def tunnel2_dpd_timeout_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618972dedb529a9c0ec020ef8e28356f28cb604c4c75ef9ab12adb750cbe9e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2DpdTimeoutAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2DpdTimeoutSeconds")
    def tunnel2_dpd_timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2DpdTimeoutSeconds"))

    @tunnel2_dpd_timeout_seconds.setter
    def tunnel2_dpd_timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68f03edb168bc91084054d1b8618b43c88f9aea9b60c3ac41ce9ce99bc28cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2DpdTimeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2EnableTunnelLifecycleControl")
    def tunnel2_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tunnel2EnableTunnelLifecycleControl"))

    @tunnel2_enable_tunnel_lifecycle_control.setter
    def tunnel2_enable_tunnel_lifecycle_control(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57df11479a5f8639103c4c5ec35adb578efc47d5b67f6240e16844aca2a5962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2EnableTunnelLifecycleControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2IkeVersions")
    def tunnel2_ike_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2IkeVersions"))

    @tunnel2_ike_versions.setter
    def tunnel2_ike_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4c20d9e98c6e2648755205970d5ef96940816bb16c12fa50a34946eaddf10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2IkeVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideCidr")
    def tunnel2_inside_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2InsideCidr"))

    @tunnel2_inside_cidr.setter
    def tunnel2_inside_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df74671191b758ce33375e2555b722967c5dfaf87de9adf880bfe9c17ffbaea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2InsideCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2InsideIpv6Cidr")
    def tunnel2_inside_ipv6_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2InsideIpv6Cidr"))

    @tunnel2_inside_ipv6_cidr.setter
    def tunnel2_inside_ipv6_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ae08efa74387ebbcaa10b1814c816ceb6735b7133e554f3707ce524d9403c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2InsideIpv6Cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1DhGroupNumbers")
    def tunnel2_phase1_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel2Phase1DhGroupNumbers"))

    @tunnel2_phase1_dh_group_numbers.setter
    def tunnel2_phase1_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c84ccff4902b168078a58d554f18f8c366b7878456505efd9195d9d448d37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1EncryptionAlgorithms")
    def tunnel2_phase1_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase1EncryptionAlgorithms"))

    @tunnel2_phase1_encryption_algorithms.setter
    def tunnel2_phase1_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57835d15862c4bd2b27e79613f6a696b7fbcc0a49ba5a38904a481c89bdb62e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1IntegrityAlgorithms")
    def tunnel2_phase1_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase1IntegrityAlgorithms"))

    @tunnel2_phase1_integrity_algorithms.setter
    def tunnel2_phase1_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97681b107754ed3c1d56bac733b35fc2feb8a5f3afe7bffdf2a802426e155777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase1LifetimeSeconds")
    def tunnel2_phase1_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2Phase1LifetimeSeconds"))

    @tunnel2_phase1_lifetime_seconds.setter
    def tunnel2_phase1_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53621394bc7eab682c533705cdd9066113e3976b6195f1d7a4b622747bca1f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase1LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2DhGroupNumbers")
    def tunnel2_phase2_dh_group_numbers(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "tunnel2Phase2DhGroupNumbers"))

    @tunnel2_phase2_dh_group_numbers.setter
    def tunnel2_phase2_dh_group_numbers(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7240c66d58db90e7c651eccc1b6d08d5a5450b306b952329dc6f28721553c3d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2DhGroupNumbers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2EncryptionAlgorithms")
    def tunnel2_phase2_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase2EncryptionAlgorithms"))

    @tunnel2_phase2_encryption_algorithms.setter
    def tunnel2_phase2_encryption_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ae841101600d0091df1038861773f42f15807c7a021a8bf47dc2515ff3c3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2EncryptionAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2IntegrityAlgorithms")
    def tunnel2_phase2_integrity_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnel2Phase2IntegrityAlgorithms"))

    @tunnel2_phase2_integrity_algorithms.setter
    def tunnel2_phase2_integrity_algorithms(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e15e85fa59ea62a1a8f3c61f65d3575b4eb34a1f1b7553b4b295d41a13a5230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2IntegrityAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2Phase2LifetimeSeconds")
    def tunnel2_phase2_lifetime_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2Phase2LifetimeSeconds"))

    @tunnel2_phase2_lifetime_seconds.setter
    def tunnel2_phase2_lifetime_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35eaf87fb0d4f8ff6127bb8e70afc777137b06ac8fb5502533e492f7c62e8fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2Phase2LifetimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2PresharedKey")
    def tunnel2_preshared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2PresharedKey"))

    @tunnel2_preshared_key.setter
    def tunnel2_preshared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1eaf598a6ba92896055e47a8f50efa039ccacac989610dea84554a0fdeea6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2PresharedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyFuzzPercentage")
    def tunnel2_rekey_fuzz_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2RekeyFuzzPercentage"))

    @tunnel2_rekey_fuzz_percentage.setter
    def tunnel2_rekey_fuzz_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e0b1601bf591857312374186b7092aa39babfa5e580774af7f1b9bc253105e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2RekeyFuzzPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2RekeyMarginTimeSeconds")
    def tunnel2_rekey_margin_time_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2RekeyMarginTimeSeconds"))

    @tunnel2_rekey_margin_time_seconds.setter
    def tunnel2_rekey_margin_time_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c65d06213747991f3ed316f20a710546f7eefc017ccb8abd2bf60122fb1b838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2RekeyMarginTimeSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2ReplayWindowSize")
    def tunnel2_replay_window_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnel2ReplayWindowSize"))

    @tunnel2_replay_window_size.setter
    def tunnel2_replay_window_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9f988ef712223bc561a84db1abf35611f79010d2a6260ffc507ebc0482fee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2ReplayWindowSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnel2StartupAction")
    def tunnel2_startup_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnel2StartupAction"))

    @tunnel2_startup_action.setter
    def tunnel2_startup_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17594096376b2b497777b66d44aab6cd8e8da35edd8ef533fd7f85255957e7f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnel2StartupAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnelInsideIpVersion")
    def tunnel_inside_ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelInsideIpVersion"))

    @tunnel_inside_ip_version.setter
    def tunnel_inside_ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c3ba8141afa1d83ef9d6e9a4866c51c8b5617a8777ee92c0376ae8ee9e897d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelInsideIpVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed913dd2c7d2d93cfeb82fef754f5c6e60fbe372d9a5490adac7beae7067a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnGatewayId"))

    @vpn_gateway_id.setter
    def vpn_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06e66c5a8423174e443b7a78e58c369716d7ae39425b203c9101d97bbc55534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnGatewayId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionConfig",
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
        "type": "type",
        "enable_acceleration": "enableAcceleration",
        "id": "id",
        "local_ipv4_network_cidr": "localIpv4NetworkCidr",
        "local_ipv6_network_cidr": "localIpv6NetworkCidr",
        "outside_ip_address_type": "outsideIpAddressType",
        "remote_ipv4_network_cidr": "remoteIpv4NetworkCidr",
        "remote_ipv6_network_cidr": "remoteIpv6NetworkCidr",
        "static_routes_only": "staticRoutesOnly",
        "tags": "tags",
        "tags_all": "tagsAll",
        "transit_gateway_id": "transitGatewayId",
        "transport_transit_gateway_attachment_id": "transportTransitGatewayAttachmentId",
        "tunnel1_dpd_timeout_action": "tunnel1DpdTimeoutAction",
        "tunnel1_dpd_timeout_seconds": "tunnel1DpdTimeoutSeconds",
        "tunnel1_enable_tunnel_lifecycle_control": "tunnel1EnableTunnelLifecycleControl",
        "tunnel1_ike_versions": "tunnel1IkeVersions",
        "tunnel1_inside_cidr": "tunnel1InsideCidr",
        "tunnel1_inside_ipv6_cidr": "tunnel1InsideIpv6Cidr",
        "tunnel1_log_options": "tunnel1LogOptions",
        "tunnel1_phase1_dh_group_numbers": "tunnel1Phase1DhGroupNumbers",
        "tunnel1_phase1_encryption_algorithms": "tunnel1Phase1EncryptionAlgorithms",
        "tunnel1_phase1_integrity_algorithms": "tunnel1Phase1IntegrityAlgorithms",
        "tunnel1_phase1_lifetime_seconds": "tunnel1Phase1LifetimeSeconds",
        "tunnel1_phase2_dh_group_numbers": "tunnel1Phase2DhGroupNumbers",
        "tunnel1_phase2_encryption_algorithms": "tunnel1Phase2EncryptionAlgorithms",
        "tunnel1_phase2_integrity_algorithms": "tunnel1Phase2IntegrityAlgorithms",
        "tunnel1_phase2_lifetime_seconds": "tunnel1Phase2LifetimeSeconds",
        "tunnel1_preshared_key": "tunnel1PresharedKey",
        "tunnel1_rekey_fuzz_percentage": "tunnel1RekeyFuzzPercentage",
        "tunnel1_rekey_margin_time_seconds": "tunnel1RekeyMarginTimeSeconds",
        "tunnel1_replay_window_size": "tunnel1ReplayWindowSize",
        "tunnel1_startup_action": "tunnel1StartupAction",
        "tunnel2_dpd_timeout_action": "tunnel2DpdTimeoutAction",
        "tunnel2_dpd_timeout_seconds": "tunnel2DpdTimeoutSeconds",
        "tunnel2_enable_tunnel_lifecycle_control": "tunnel2EnableTunnelLifecycleControl",
        "tunnel2_ike_versions": "tunnel2IkeVersions",
        "tunnel2_inside_cidr": "tunnel2InsideCidr",
        "tunnel2_inside_ipv6_cidr": "tunnel2InsideIpv6Cidr",
        "tunnel2_log_options": "tunnel2LogOptions",
        "tunnel2_phase1_dh_group_numbers": "tunnel2Phase1DhGroupNumbers",
        "tunnel2_phase1_encryption_algorithms": "tunnel2Phase1EncryptionAlgorithms",
        "tunnel2_phase1_integrity_algorithms": "tunnel2Phase1IntegrityAlgorithms",
        "tunnel2_phase1_lifetime_seconds": "tunnel2Phase1LifetimeSeconds",
        "tunnel2_phase2_dh_group_numbers": "tunnel2Phase2DhGroupNumbers",
        "tunnel2_phase2_encryption_algorithms": "tunnel2Phase2EncryptionAlgorithms",
        "tunnel2_phase2_integrity_algorithms": "tunnel2Phase2IntegrityAlgorithms",
        "tunnel2_phase2_lifetime_seconds": "tunnel2Phase2LifetimeSeconds",
        "tunnel2_preshared_key": "tunnel2PresharedKey",
        "tunnel2_rekey_fuzz_percentage": "tunnel2RekeyFuzzPercentage",
        "tunnel2_rekey_margin_time_seconds": "tunnel2RekeyMarginTimeSeconds",
        "tunnel2_replay_window_size": "tunnel2ReplayWindowSize",
        "tunnel2_startup_action": "tunnel2StartupAction",
        "tunnel_inside_ip_version": "tunnelInsideIpVersion",
        "vpn_gateway_id": "vpnGatewayId",
    },
)
class VpnConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        outside_ip_address_type: typing.Optional[builtins.str] = None,
        remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
        remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
        static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transit_gateway_id: typing.Optional[builtins.str] = None,
        transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel1_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_preshared_key: typing.Optional[builtins.str] = None,
        tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel1_startup_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
        tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
        tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
        tunnel2_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
        tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_preshared_key: typing.Optional[builtins.str] = None,
        tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
        tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
        tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
        tunnel2_startup_action: typing.Optional[builtins.str] = None,
        tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
        vpn_gateway_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param customer_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#customer_gateway_id VpnConnection#customer_gateway_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#type VpnConnection#type}.
        :param enable_acceleration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#enable_acceleration VpnConnection#enable_acceleration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#id VpnConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#local_ipv4_network_cidr VpnConnection#local_ipv4_network_cidr}.
        :param local_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#local_ipv6_network_cidr VpnConnection#local_ipv6_network_cidr}.
        :param outside_ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#outside_ip_address_type VpnConnection#outside_ip_address_type}.
        :param remote_ipv4_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#remote_ipv4_network_cidr VpnConnection#remote_ipv4_network_cidr}.
        :param remote_ipv6_network_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#remote_ipv6_network_cidr VpnConnection#remote_ipv6_network_cidr}.
        :param static_routes_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#static_routes_only VpnConnection#static_routes_only}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tags VpnConnection#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tags_all VpnConnection#tags_all}.
        :param transit_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#transit_gateway_id VpnConnection#transit_gateway_id}.
        :param transport_transit_gateway_attachment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#transport_transit_gateway_attachment_id VpnConnection#transport_transit_gateway_attachment_id}.
        :param tunnel1_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_action VpnConnection#tunnel1_dpd_timeout_action}.
        :param tunnel1_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_seconds VpnConnection#tunnel1_dpd_timeout_seconds}.
        :param tunnel1_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_enable_tunnel_lifecycle_control VpnConnection#tunnel1_enable_tunnel_lifecycle_control}.
        :param tunnel1_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_ike_versions VpnConnection#tunnel1_ike_versions}.
        :param tunnel1_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_inside_cidr VpnConnection#tunnel1_inside_cidr}.
        :param tunnel1_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_inside_ipv6_cidr VpnConnection#tunnel1_inside_ipv6_cidr}.
        :param tunnel1_log_options: tunnel1_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_log_options VpnConnection#tunnel1_log_options}
        :param tunnel1_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_dh_group_numbers VpnConnection#tunnel1_phase1_dh_group_numbers}.
        :param tunnel1_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_encryption_algorithms VpnConnection#tunnel1_phase1_encryption_algorithms}.
        :param tunnel1_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_integrity_algorithms VpnConnection#tunnel1_phase1_integrity_algorithms}.
        :param tunnel1_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_lifetime_seconds VpnConnection#tunnel1_phase1_lifetime_seconds}.
        :param tunnel1_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_dh_group_numbers VpnConnection#tunnel1_phase2_dh_group_numbers}.
        :param tunnel1_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_encryption_algorithms VpnConnection#tunnel1_phase2_encryption_algorithms}.
        :param tunnel1_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_integrity_algorithms VpnConnection#tunnel1_phase2_integrity_algorithms}.
        :param tunnel1_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_lifetime_seconds VpnConnection#tunnel1_phase2_lifetime_seconds}.
        :param tunnel1_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_preshared_key VpnConnection#tunnel1_preshared_key}.
        :param tunnel1_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_rekey_fuzz_percentage VpnConnection#tunnel1_rekey_fuzz_percentage}.
        :param tunnel1_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_rekey_margin_time_seconds VpnConnection#tunnel1_rekey_margin_time_seconds}.
        :param tunnel1_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_replay_window_size VpnConnection#tunnel1_replay_window_size}.
        :param tunnel1_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_startup_action VpnConnection#tunnel1_startup_action}.
        :param tunnel2_dpd_timeout_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_action VpnConnection#tunnel2_dpd_timeout_action}.
        :param tunnel2_dpd_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_seconds VpnConnection#tunnel2_dpd_timeout_seconds}.
        :param tunnel2_enable_tunnel_lifecycle_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_enable_tunnel_lifecycle_control VpnConnection#tunnel2_enable_tunnel_lifecycle_control}.
        :param tunnel2_ike_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_ike_versions VpnConnection#tunnel2_ike_versions}.
        :param tunnel2_inside_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_inside_cidr VpnConnection#tunnel2_inside_cidr}.
        :param tunnel2_inside_ipv6_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_inside_ipv6_cidr VpnConnection#tunnel2_inside_ipv6_cidr}.
        :param tunnel2_log_options: tunnel2_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_log_options VpnConnection#tunnel2_log_options}
        :param tunnel2_phase1_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_dh_group_numbers VpnConnection#tunnel2_phase1_dh_group_numbers}.
        :param tunnel2_phase1_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_encryption_algorithms VpnConnection#tunnel2_phase1_encryption_algorithms}.
        :param tunnel2_phase1_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_integrity_algorithms VpnConnection#tunnel2_phase1_integrity_algorithms}.
        :param tunnel2_phase1_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_lifetime_seconds VpnConnection#tunnel2_phase1_lifetime_seconds}.
        :param tunnel2_phase2_dh_group_numbers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_dh_group_numbers VpnConnection#tunnel2_phase2_dh_group_numbers}.
        :param tunnel2_phase2_encryption_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_encryption_algorithms VpnConnection#tunnel2_phase2_encryption_algorithms}.
        :param tunnel2_phase2_integrity_algorithms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_integrity_algorithms VpnConnection#tunnel2_phase2_integrity_algorithms}.
        :param tunnel2_phase2_lifetime_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_lifetime_seconds VpnConnection#tunnel2_phase2_lifetime_seconds}.
        :param tunnel2_preshared_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_preshared_key VpnConnection#tunnel2_preshared_key}.
        :param tunnel2_rekey_fuzz_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_rekey_fuzz_percentage VpnConnection#tunnel2_rekey_fuzz_percentage}.
        :param tunnel2_rekey_margin_time_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_rekey_margin_time_seconds VpnConnection#tunnel2_rekey_margin_time_seconds}.
        :param tunnel2_replay_window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_replay_window_size VpnConnection#tunnel2_replay_window_size}.
        :param tunnel2_startup_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_startup_action VpnConnection#tunnel2_startup_action}.
        :param tunnel_inside_ip_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel_inside_ip_version VpnConnection#tunnel_inside_ip_version}.
        :param vpn_gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#vpn_gateway_id VpnConnection#vpn_gateway_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(tunnel1_log_options, dict):
            tunnel1_log_options = VpnConnectionTunnel1LogOptions(**tunnel1_log_options)
        if isinstance(tunnel2_log_options, dict):
            tunnel2_log_options = VpnConnectionTunnel2LogOptions(**tunnel2_log_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1ff5171a739715b7a4605259904c2502c4c339a5fbc4f33a1eeec85564baf4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument customer_gateway_id", value=customer_gateway_id, expected_type=type_hints["customer_gateway_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument enable_acceleration", value=enable_acceleration, expected_type=type_hints["enable_acceleration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_ipv4_network_cidr", value=local_ipv4_network_cidr, expected_type=type_hints["local_ipv4_network_cidr"])
            check_type(argname="argument local_ipv6_network_cidr", value=local_ipv6_network_cidr, expected_type=type_hints["local_ipv6_network_cidr"])
            check_type(argname="argument outside_ip_address_type", value=outside_ip_address_type, expected_type=type_hints["outside_ip_address_type"])
            check_type(argname="argument remote_ipv4_network_cidr", value=remote_ipv4_network_cidr, expected_type=type_hints["remote_ipv4_network_cidr"])
            check_type(argname="argument remote_ipv6_network_cidr", value=remote_ipv6_network_cidr, expected_type=type_hints["remote_ipv6_network_cidr"])
            check_type(argname="argument static_routes_only", value=static_routes_only, expected_type=type_hints["static_routes_only"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
            check_type(argname="argument transport_transit_gateway_attachment_id", value=transport_transit_gateway_attachment_id, expected_type=type_hints["transport_transit_gateway_attachment_id"])
            check_type(argname="argument tunnel1_dpd_timeout_action", value=tunnel1_dpd_timeout_action, expected_type=type_hints["tunnel1_dpd_timeout_action"])
            check_type(argname="argument tunnel1_dpd_timeout_seconds", value=tunnel1_dpd_timeout_seconds, expected_type=type_hints["tunnel1_dpd_timeout_seconds"])
            check_type(argname="argument tunnel1_enable_tunnel_lifecycle_control", value=tunnel1_enable_tunnel_lifecycle_control, expected_type=type_hints["tunnel1_enable_tunnel_lifecycle_control"])
            check_type(argname="argument tunnel1_ike_versions", value=tunnel1_ike_versions, expected_type=type_hints["tunnel1_ike_versions"])
            check_type(argname="argument tunnel1_inside_cidr", value=tunnel1_inside_cidr, expected_type=type_hints["tunnel1_inside_cidr"])
            check_type(argname="argument tunnel1_inside_ipv6_cidr", value=tunnel1_inside_ipv6_cidr, expected_type=type_hints["tunnel1_inside_ipv6_cidr"])
            check_type(argname="argument tunnel1_log_options", value=tunnel1_log_options, expected_type=type_hints["tunnel1_log_options"])
            check_type(argname="argument tunnel1_phase1_dh_group_numbers", value=tunnel1_phase1_dh_group_numbers, expected_type=type_hints["tunnel1_phase1_dh_group_numbers"])
            check_type(argname="argument tunnel1_phase1_encryption_algorithms", value=tunnel1_phase1_encryption_algorithms, expected_type=type_hints["tunnel1_phase1_encryption_algorithms"])
            check_type(argname="argument tunnel1_phase1_integrity_algorithms", value=tunnel1_phase1_integrity_algorithms, expected_type=type_hints["tunnel1_phase1_integrity_algorithms"])
            check_type(argname="argument tunnel1_phase1_lifetime_seconds", value=tunnel1_phase1_lifetime_seconds, expected_type=type_hints["tunnel1_phase1_lifetime_seconds"])
            check_type(argname="argument tunnel1_phase2_dh_group_numbers", value=tunnel1_phase2_dh_group_numbers, expected_type=type_hints["tunnel1_phase2_dh_group_numbers"])
            check_type(argname="argument tunnel1_phase2_encryption_algorithms", value=tunnel1_phase2_encryption_algorithms, expected_type=type_hints["tunnel1_phase2_encryption_algorithms"])
            check_type(argname="argument tunnel1_phase2_integrity_algorithms", value=tunnel1_phase2_integrity_algorithms, expected_type=type_hints["tunnel1_phase2_integrity_algorithms"])
            check_type(argname="argument tunnel1_phase2_lifetime_seconds", value=tunnel1_phase2_lifetime_seconds, expected_type=type_hints["tunnel1_phase2_lifetime_seconds"])
            check_type(argname="argument tunnel1_preshared_key", value=tunnel1_preshared_key, expected_type=type_hints["tunnel1_preshared_key"])
            check_type(argname="argument tunnel1_rekey_fuzz_percentage", value=tunnel1_rekey_fuzz_percentage, expected_type=type_hints["tunnel1_rekey_fuzz_percentage"])
            check_type(argname="argument tunnel1_rekey_margin_time_seconds", value=tunnel1_rekey_margin_time_seconds, expected_type=type_hints["tunnel1_rekey_margin_time_seconds"])
            check_type(argname="argument tunnel1_replay_window_size", value=tunnel1_replay_window_size, expected_type=type_hints["tunnel1_replay_window_size"])
            check_type(argname="argument tunnel1_startup_action", value=tunnel1_startup_action, expected_type=type_hints["tunnel1_startup_action"])
            check_type(argname="argument tunnel2_dpd_timeout_action", value=tunnel2_dpd_timeout_action, expected_type=type_hints["tunnel2_dpd_timeout_action"])
            check_type(argname="argument tunnel2_dpd_timeout_seconds", value=tunnel2_dpd_timeout_seconds, expected_type=type_hints["tunnel2_dpd_timeout_seconds"])
            check_type(argname="argument tunnel2_enable_tunnel_lifecycle_control", value=tunnel2_enable_tunnel_lifecycle_control, expected_type=type_hints["tunnel2_enable_tunnel_lifecycle_control"])
            check_type(argname="argument tunnel2_ike_versions", value=tunnel2_ike_versions, expected_type=type_hints["tunnel2_ike_versions"])
            check_type(argname="argument tunnel2_inside_cidr", value=tunnel2_inside_cidr, expected_type=type_hints["tunnel2_inside_cidr"])
            check_type(argname="argument tunnel2_inside_ipv6_cidr", value=tunnel2_inside_ipv6_cidr, expected_type=type_hints["tunnel2_inside_ipv6_cidr"])
            check_type(argname="argument tunnel2_log_options", value=tunnel2_log_options, expected_type=type_hints["tunnel2_log_options"])
            check_type(argname="argument tunnel2_phase1_dh_group_numbers", value=tunnel2_phase1_dh_group_numbers, expected_type=type_hints["tunnel2_phase1_dh_group_numbers"])
            check_type(argname="argument tunnel2_phase1_encryption_algorithms", value=tunnel2_phase1_encryption_algorithms, expected_type=type_hints["tunnel2_phase1_encryption_algorithms"])
            check_type(argname="argument tunnel2_phase1_integrity_algorithms", value=tunnel2_phase1_integrity_algorithms, expected_type=type_hints["tunnel2_phase1_integrity_algorithms"])
            check_type(argname="argument tunnel2_phase1_lifetime_seconds", value=tunnel2_phase1_lifetime_seconds, expected_type=type_hints["tunnel2_phase1_lifetime_seconds"])
            check_type(argname="argument tunnel2_phase2_dh_group_numbers", value=tunnel2_phase2_dh_group_numbers, expected_type=type_hints["tunnel2_phase2_dh_group_numbers"])
            check_type(argname="argument tunnel2_phase2_encryption_algorithms", value=tunnel2_phase2_encryption_algorithms, expected_type=type_hints["tunnel2_phase2_encryption_algorithms"])
            check_type(argname="argument tunnel2_phase2_integrity_algorithms", value=tunnel2_phase2_integrity_algorithms, expected_type=type_hints["tunnel2_phase2_integrity_algorithms"])
            check_type(argname="argument tunnel2_phase2_lifetime_seconds", value=tunnel2_phase2_lifetime_seconds, expected_type=type_hints["tunnel2_phase2_lifetime_seconds"])
            check_type(argname="argument tunnel2_preshared_key", value=tunnel2_preshared_key, expected_type=type_hints["tunnel2_preshared_key"])
            check_type(argname="argument tunnel2_rekey_fuzz_percentage", value=tunnel2_rekey_fuzz_percentage, expected_type=type_hints["tunnel2_rekey_fuzz_percentage"])
            check_type(argname="argument tunnel2_rekey_margin_time_seconds", value=tunnel2_rekey_margin_time_seconds, expected_type=type_hints["tunnel2_rekey_margin_time_seconds"])
            check_type(argname="argument tunnel2_replay_window_size", value=tunnel2_replay_window_size, expected_type=type_hints["tunnel2_replay_window_size"])
            check_type(argname="argument tunnel2_startup_action", value=tunnel2_startup_action, expected_type=type_hints["tunnel2_startup_action"])
            check_type(argname="argument tunnel_inside_ip_version", value=tunnel_inside_ip_version, expected_type=type_hints["tunnel_inside_ip_version"])
            check_type(argname="argument vpn_gateway_id", value=vpn_gateway_id, expected_type=type_hints["vpn_gateway_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_gateway_id": customer_gateway_id,
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
        if enable_acceleration is not None:
            self._values["enable_acceleration"] = enable_acceleration
        if id is not None:
            self._values["id"] = id
        if local_ipv4_network_cidr is not None:
            self._values["local_ipv4_network_cidr"] = local_ipv4_network_cidr
        if local_ipv6_network_cidr is not None:
            self._values["local_ipv6_network_cidr"] = local_ipv6_network_cidr
        if outside_ip_address_type is not None:
            self._values["outside_ip_address_type"] = outside_ip_address_type
        if remote_ipv4_network_cidr is not None:
            self._values["remote_ipv4_network_cidr"] = remote_ipv4_network_cidr
        if remote_ipv6_network_cidr is not None:
            self._values["remote_ipv6_network_cidr"] = remote_ipv6_network_cidr
        if static_routes_only is not None:
            self._values["static_routes_only"] = static_routes_only
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if transit_gateway_id is not None:
            self._values["transit_gateway_id"] = transit_gateway_id
        if transport_transit_gateway_attachment_id is not None:
            self._values["transport_transit_gateway_attachment_id"] = transport_transit_gateway_attachment_id
        if tunnel1_dpd_timeout_action is not None:
            self._values["tunnel1_dpd_timeout_action"] = tunnel1_dpd_timeout_action
        if tunnel1_dpd_timeout_seconds is not None:
            self._values["tunnel1_dpd_timeout_seconds"] = tunnel1_dpd_timeout_seconds
        if tunnel1_enable_tunnel_lifecycle_control is not None:
            self._values["tunnel1_enable_tunnel_lifecycle_control"] = tunnel1_enable_tunnel_lifecycle_control
        if tunnel1_ike_versions is not None:
            self._values["tunnel1_ike_versions"] = tunnel1_ike_versions
        if tunnel1_inside_cidr is not None:
            self._values["tunnel1_inside_cidr"] = tunnel1_inside_cidr
        if tunnel1_inside_ipv6_cidr is not None:
            self._values["tunnel1_inside_ipv6_cidr"] = tunnel1_inside_ipv6_cidr
        if tunnel1_log_options is not None:
            self._values["tunnel1_log_options"] = tunnel1_log_options
        if tunnel1_phase1_dh_group_numbers is not None:
            self._values["tunnel1_phase1_dh_group_numbers"] = tunnel1_phase1_dh_group_numbers
        if tunnel1_phase1_encryption_algorithms is not None:
            self._values["tunnel1_phase1_encryption_algorithms"] = tunnel1_phase1_encryption_algorithms
        if tunnel1_phase1_integrity_algorithms is not None:
            self._values["tunnel1_phase1_integrity_algorithms"] = tunnel1_phase1_integrity_algorithms
        if tunnel1_phase1_lifetime_seconds is not None:
            self._values["tunnel1_phase1_lifetime_seconds"] = tunnel1_phase1_lifetime_seconds
        if tunnel1_phase2_dh_group_numbers is not None:
            self._values["tunnel1_phase2_dh_group_numbers"] = tunnel1_phase2_dh_group_numbers
        if tunnel1_phase2_encryption_algorithms is not None:
            self._values["tunnel1_phase2_encryption_algorithms"] = tunnel1_phase2_encryption_algorithms
        if tunnel1_phase2_integrity_algorithms is not None:
            self._values["tunnel1_phase2_integrity_algorithms"] = tunnel1_phase2_integrity_algorithms
        if tunnel1_phase2_lifetime_seconds is not None:
            self._values["tunnel1_phase2_lifetime_seconds"] = tunnel1_phase2_lifetime_seconds
        if tunnel1_preshared_key is not None:
            self._values["tunnel1_preshared_key"] = tunnel1_preshared_key
        if tunnel1_rekey_fuzz_percentage is not None:
            self._values["tunnel1_rekey_fuzz_percentage"] = tunnel1_rekey_fuzz_percentage
        if tunnel1_rekey_margin_time_seconds is not None:
            self._values["tunnel1_rekey_margin_time_seconds"] = tunnel1_rekey_margin_time_seconds
        if tunnel1_replay_window_size is not None:
            self._values["tunnel1_replay_window_size"] = tunnel1_replay_window_size
        if tunnel1_startup_action is not None:
            self._values["tunnel1_startup_action"] = tunnel1_startup_action
        if tunnel2_dpd_timeout_action is not None:
            self._values["tunnel2_dpd_timeout_action"] = tunnel2_dpd_timeout_action
        if tunnel2_dpd_timeout_seconds is not None:
            self._values["tunnel2_dpd_timeout_seconds"] = tunnel2_dpd_timeout_seconds
        if tunnel2_enable_tunnel_lifecycle_control is not None:
            self._values["tunnel2_enable_tunnel_lifecycle_control"] = tunnel2_enable_tunnel_lifecycle_control
        if tunnel2_ike_versions is not None:
            self._values["tunnel2_ike_versions"] = tunnel2_ike_versions
        if tunnel2_inside_cidr is not None:
            self._values["tunnel2_inside_cidr"] = tunnel2_inside_cidr
        if tunnel2_inside_ipv6_cidr is not None:
            self._values["tunnel2_inside_ipv6_cidr"] = tunnel2_inside_ipv6_cidr
        if tunnel2_log_options is not None:
            self._values["tunnel2_log_options"] = tunnel2_log_options
        if tunnel2_phase1_dh_group_numbers is not None:
            self._values["tunnel2_phase1_dh_group_numbers"] = tunnel2_phase1_dh_group_numbers
        if tunnel2_phase1_encryption_algorithms is not None:
            self._values["tunnel2_phase1_encryption_algorithms"] = tunnel2_phase1_encryption_algorithms
        if tunnel2_phase1_integrity_algorithms is not None:
            self._values["tunnel2_phase1_integrity_algorithms"] = tunnel2_phase1_integrity_algorithms
        if tunnel2_phase1_lifetime_seconds is not None:
            self._values["tunnel2_phase1_lifetime_seconds"] = tunnel2_phase1_lifetime_seconds
        if tunnel2_phase2_dh_group_numbers is not None:
            self._values["tunnel2_phase2_dh_group_numbers"] = tunnel2_phase2_dh_group_numbers
        if tunnel2_phase2_encryption_algorithms is not None:
            self._values["tunnel2_phase2_encryption_algorithms"] = tunnel2_phase2_encryption_algorithms
        if tunnel2_phase2_integrity_algorithms is not None:
            self._values["tunnel2_phase2_integrity_algorithms"] = tunnel2_phase2_integrity_algorithms
        if tunnel2_phase2_lifetime_seconds is not None:
            self._values["tunnel2_phase2_lifetime_seconds"] = tunnel2_phase2_lifetime_seconds
        if tunnel2_preshared_key is not None:
            self._values["tunnel2_preshared_key"] = tunnel2_preshared_key
        if tunnel2_rekey_fuzz_percentage is not None:
            self._values["tunnel2_rekey_fuzz_percentage"] = tunnel2_rekey_fuzz_percentage
        if tunnel2_rekey_margin_time_seconds is not None:
            self._values["tunnel2_rekey_margin_time_seconds"] = tunnel2_rekey_margin_time_seconds
        if tunnel2_replay_window_size is not None:
            self._values["tunnel2_replay_window_size"] = tunnel2_replay_window_size
        if tunnel2_startup_action is not None:
            self._values["tunnel2_startup_action"] = tunnel2_startup_action
        if tunnel_inside_ip_version is not None:
            self._values["tunnel_inside_ip_version"] = tunnel_inside_ip_version
        if vpn_gateway_id is not None:
            self._values["vpn_gateway_id"] = vpn_gateway_id

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#customer_gateway_id VpnConnection#customer_gateway_id}.'''
        result = self._values.get("customer_gateway_id")
        assert result is not None, "Required property 'customer_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#type VpnConnection#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_acceleration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#enable_acceleration VpnConnection#enable_acceleration}.'''
        result = self._values.get("enable_acceleration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#id VpnConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#local_ipv4_network_cidr VpnConnection#local_ipv4_network_cidr}.'''
        result = self._values.get("local_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ipv6_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#local_ipv6_network_cidr VpnConnection#local_ipv6_network_cidr}.'''
        result = self._values.get("local_ipv6_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outside_ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#outside_ip_address_type VpnConnection#outside_ip_address_type}.'''
        result = self._values.get("outside_ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_ipv4_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#remote_ipv4_network_cidr VpnConnection#remote_ipv4_network_cidr}.'''
        result = self._values.get("remote_ipv4_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_ipv6_network_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#remote_ipv6_network_cidr VpnConnection#remote_ipv6_network_cidr}.'''
        result = self._values.get("remote_ipv6_network_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_routes_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#static_routes_only VpnConnection#static_routes_only}.'''
        result = self._values.get("static_routes_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tags VpnConnection#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tags_all VpnConnection#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def transit_gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#transit_gateway_id VpnConnection#transit_gateway_id}.'''
        result = self._values.get("transit_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transport_transit_gateway_attachment_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#transport_transit_gateway_attachment_id VpnConnection#transport_transit_gateway_attachment_id}.'''
        result = self._values.get("transport_transit_gateway_attachment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_dpd_timeout_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_action VpnConnection#tunnel1_dpd_timeout_action}.'''
        result = self._values.get("tunnel1_dpd_timeout_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_dpd_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_dpd_timeout_seconds VpnConnection#tunnel1_dpd_timeout_seconds}.'''
        result = self._values.get("tunnel1_dpd_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_enable_tunnel_lifecycle_control VpnConnection#tunnel1_enable_tunnel_lifecycle_control}.'''
        result = self._values.get("tunnel1_enable_tunnel_lifecycle_control")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tunnel1_ike_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_ike_versions VpnConnection#tunnel1_ike_versions}.'''
        result = self._values.get("tunnel1_ike_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_inside_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_inside_cidr VpnConnection#tunnel1_inside_cidr}.'''
        result = self._values.get("tunnel1_inside_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_inside_ipv6_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_inside_ipv6_cidr VpnConnection#tunnel1_inside_ipv6_cidr}.'''
        result = self._values.get("tunnel1_inside_ipv6_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_log_options(self) -> typing.Optional["VpnConnectionTunnel1LogOptions"]:
        '''tunnel1_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_log_options VpnConnection#tunnel1_log_options}
        '''
        result = self._values.get("tunnel1_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel1LogOptions"], result)

    @builtins.property
    def tunnel1_phase1_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_dh_group_numbers VpnConnection#tunnel1_phase1_dh_group_numbers}.'''
        result = self._values.get("tunnel1_phase1_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel1_phase1_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_encryption_algorithms VpnConnection#tunnel1_phase1_encryption_algorithms}.'''
        result = self._values.get("tunnel1_phase1_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase1_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_integrity_algorithms VpnConnection#tunnel1_phase1_integrity_algorithms}.'''
        result = self._values.get("tunnel1_phase1_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase1_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase1_lifetime_seconds VpnConnection#tunnel1_phase1_lifetime_seconds}.'''
        result = self._values.get("tunnel1_phase1_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_phase2_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_dh_group_numbers VpnConnection#tunnel1_phase2_dh_group_numbers}.'''
        result = self._values.get("tunnel1_phase2_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel1_phase2_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_encryption_algorithms VpnConnection#tunnel1_phase2_encryption_algorithms}.'''
        result = self._values.get("tunnel1_phase2_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase2_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_integrity_algorithms VpnConnection#tunnel1_phase2_integrity_algorithms}.'''
        result = self._values.get("tunnel1_phase2_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel1_phase2_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_phase2_lifetime_seconds VpnConnection#tunnel1_phase2_lifetime_seconds}.'''
        result = self._values.get("tunnel1_phase2_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_preshared_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_preshared_key VpnConnection#tunnel1_preshared_key}.'''
        result = self._values.get("tunnel1_preshared_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel1_rekey_fuzz_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_rekey_fuzz_percentage VpnConnection#tunnel1_rekey_fuzz_percentage}.'''
        result = self._values.get("tunnel1_rekey_fuzz_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_rekey_margin_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_rekey_margin_time_seconds VpnConnection#tunnel1_rekey_margin_time_seconds}.'''
        result = self._values.get("tunnel1_rekey_margin_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_replay_window_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_replay_window_size VpnConnection#tunnel1_replay_window_size}.'''
        result = self._values.get("tunnel1_replay_window_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel1_startup_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel1_startup_action VpnConnection#tunnel1_startup_action}.'''
        result = self._values.get("tunnel1_startup_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_dpd_timeout_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_action VpnConnection#tunnel2_dpd_timeout_action}.'''
        result = self._values.get("tunnel2_dpd_timeout_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_dpd_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_dpd_timeout_seconds VpnConnection#tunnel2_dpd_timeout_seconds}.'''
        result = self._values.get("tunnel2_dpd_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_enable_tunnel_lifecycle_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_enable_tunnel_lifecycle_control VpnConnection#tunnel2_enable_tunnel_lifecycle_control}.'''
        result = self._values.get("tunnel2_enable_tunnel_lifecycle_control")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tunnel2_ike_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_ike_versions VpnConnection#tunnel2_ike_versions}.'''
        result = self._values.get("tunnel2_ike_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_inside_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_inside_cidr VpnConnection#tunnel2_inside_cidr}.'''
        result = self._values.get("tunnel2_inside_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_inside_ipv6_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_inside_ipv6_cidr VpnConnection#tunnel2_inside_ipv6_cidr}.'''
        result = self._values.get("tunnel2_inside_ipv6_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_log_options(self) -> typing.Optional["VpnConnectionTunnel2LogOptions"]:
        '''tunnel2_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_log_options VpnConnection#tunnel2_log_options}
        '''
        result = self._values.get("tunnel2_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel2LogOptions"], result)

    @builtins.property
    def tunnel2_phase1_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_dh_group_numbers VpnConnection#tunnel2_phase1_dh_group_numbers}.'''
        result = self._values.get("tunnel2_phase1_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel2_phase1_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_encryption_algorithms VpnConnection#tunnel2_phase1_encryption_algorithms}.'''
        result = self._values.get("tunnel2_phase1_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase1_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_integrity_algorithms VpnConnection#tunnel2_phase1_integrity_algorithms}.'''
        result = self._values.get("tunnel2_phase1_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase1_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase1_lifetime_seconds VpnConnection#tunnel2_phase1_lifetime_seconds}.'''
        result = self._values.get("tunnel2_phase1_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_phase2_dh_group_numbers(
        self,
    ) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_dh_group_numbers VpnConnection#tunnel2_phase2_dh_group_numbers}.'''
        result = self._values.get("tunnel2_phase2_dh_group_numbers")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def tunnel2_phase2_encryption_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_encryption_algorithms VpnConnection#tunnel2_phase2_encryption_algorithms}.'''
        result = self._values.get("tunnel2_phase2_encryption_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase2_integrity_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_integrity_algorithms VpnConnection#tunnel2_phase2_integrity_algorithms}.'''
        result = self._values.get("tunnel2_phase2_integrity_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel2_phase2_lifetime_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_phase2_lifetime_seconds VpnConnection#tunnel2_phase2_lifetime_seconds}.'''
        result = self._values.get("tunnel2_phase2_lifetime_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_preshared_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_preshared_key VpnConnection#tunnel2_preshared_key}.'''
        result = self._values.get("tunnel2_preshared_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel2_rekey_fuzz_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_rekey_fuzz_percentage VpnConnection#tunnel2_rekey_fuzz_percentage}.'''
        result = self._values.get("tunnel2_rekey_fuzz_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_rekey_margin_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_rekey_margin_time_seconds VpnConnection#tunnel2_rekey_margin_time_seconds}.'''
        result = self._values.get("tunnel2_rekey_margin_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_replay_window_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_replay_window_size VpnConnection#tunnel2_replay_window_size}.'''
        result = self._values.get("tunnel2_replay_window_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel2_startup_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel2_startup_action VpnConnection#tunnel2_startup_action}.'''
        result = self._values.get("tunnel2_startup_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel_inside_ip_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#tunnel_inside_ip_version VpnConnection#tunnel_inside_ip_version}.'''
        result = self._values.get("tunnel_inside_ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#vpn_gateway_id VpnConnection#vpn_gateway_id}.'''
        result = self._values.get("vpn_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionRoutes",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpnConnectionRoutes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionRoutes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionRoutesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionRoutesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__970e5749a84bc9ebc68139609bf8c29c93150e7cb5bd62d6203860809f36b62c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnConnectionRoutesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab13017741dafe587f172a9637f040a374914aa778ecaa65495bf9b780f6f12)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnConnectionRoutesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cdf97da856a68ff7c296b8b698c540d7a334f4029e4c8fa5bcd3d95a70da578)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda7514c58abac015a057ae177987dff0e83ddd1a2b3a94ad1b09cd927b1f7ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ed4eb64dc18f31603a9db5f34d6226000a2926d6435310444e001525d742175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VpnConnectionRoutesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionRoutesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c188828f615983f8d9f5c8c5216d5e0fa7cf08ae8b4c613b6652bc28d585939d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="destinationCidrBlock")
    def destination_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionRoutes]:
        return typing.cast(typing.Optional[VpnConnectionRoutes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VpnConnectionRoutes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdf94e5b268f70fc3681cdceae26303cc275872f31097da0a2a011dba0a2ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptions",
    jsii_struct_bases=[],
    name_mapping={"cloudwatch_log_options": "cloudwatchLogOptions"},
)
class VpnConnectionTunnel1LogOptions:
    def __init__(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        if isinstance(cloudwatch_log_options, dict):
            cloudwatch_log_options = VpnConnectionTunnel1LogOptionsCloudwatchLogOptions(**cloudwatch_log_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2987178142993d954c0b9fb8c3c1dc0aead090fbf7670bf0e2df9759e17821b1)
            check_type(argname="argument cloudwatch_log_options", value=cloudwatch_log_options, expected_type=type_hints["cloudwatch_log_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_log_options is not None:
            self._values["cloudwatch_log_options"] = cloudwatch_log_options

    @builtins.property
    def cloudwatch_log_options(
        self,
    ) -> typing.Optional["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions"]:
        '''cloudwatch_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        result = self._values.get("cloudwatch_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel1LogOptionsCloudwatchLogOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel1LogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptionsCloudwatchLogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "log_enabled": "logEnabled",
        "log_group_arn": "logGroupArn",
        "log_output_format": "logOutputFormat",
    },
)
class VpnConnectionTunnel1LogOptionsCloudwatchLogOptions:
    def __init__(
        self,
        *,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b428cdf57040466ff9e463429eb04d8967afd4f3062a33f5397ea359d413e33)
            check_type(argname="argument log_enabled", value=log_enabled, expected_type=type_hints["log_enabled"])
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            check_type(argname="argument log_output_format", value=log_output_format, expected_type=type_hints["log_output_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_enabled is not None:
            self._values["log_enabled"] = log_enabled
        if log_group_arn is not None:
            self._values["log_group_arn"] = log_group_arn
        if log_output_format is not None:
            self._values["log_output_format"] = log_output_format

    @builtins.property
    def log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.'''
        result = self._values.get("log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.'''
        result = self._values.get("log_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel1LogOptionsCloudwatchLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__835aff9933dc21765aa06eaa383b3763a6c5e10d4e647d0bc204c3c96e4bba56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogEnabled")
    def reset_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogEnabled", []))

    @jsii.member(jsii_name="resetLogGroupArn")
    def reset_log_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupArn", []))

    @jsii.member(jsii_name="resetLogOutputFormat")
    def reset_log_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogOutputFormat", []))

    @builtins.property
    @jsii.member(jsii_name="logEnabledInput")
    def log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logOutputFormatInput")
    def log_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="logEnabled")
    def log_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logEnabled"))

    @log_enabled.setter
    def log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d379abf8b6b5dbdb28504b9c14328d0fab0fb2963dfb80a7dfdfe1e91e73fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7557b3c80f3112000776b540ac3f7fe35c5c782620dc8ae4f2efa7d34871fac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logOutputFormat")
    def log_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logOutputFormat"))

    @log_output_format.setter
    def log_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1942316727f81d87140720de166f8760dd6b7bfb77f29381192d0d305ece8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634eaf648a9cf1218a8553b5c1e81cbc939ebf7d3773a8a87c0e5f69e5ec115d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnConnectionTunnel1LogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel1LogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__809cac86660fa0af7c13aaf88567bf05e7f81b789485baed699796acc30b7119)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogOptions")
    def put_cloudwatch_log_options(
        self,
        *,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        value = VpnConnectionTunnel1LogOptionsCloudwatchLogOptions(
            log_enabled=log_enabled,
            log_group_arn=log_group_arn,
            log_output_format=log_output_format,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogOptions", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogOptions")
    def reset_cloudwatch_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogOptions", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptions")
    def cloudwatch_log_options(
        self,
    ) -> VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference:
        return typing.cast(VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference, jsii.get(self, "cloudwatchLogOptions"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptionsInput")
    def cloudwatch_log_options_input(
        self,
    ) -> typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions], jsii.get(self, "cloudwatchLogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionTunnel1LogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel1LogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel1LogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e1ee8a8eb726df23ffe068b98a8e76899958f76ea8b5ef29bb1ed0c973c949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptions",
    jsii_struct_bases=[],
    name_mapping={"cloudwatch_log_options": "cloudwatchLogOptions"},
)
class VpnConnectionTunnel2LogOptions:
    def __init__(
        self,
        *,
        cloudwatch_log_options: typing.Optional[typing.Union["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_options: cloudwatch_log_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        if isinstance(cloudwatch_log_options, dict):
            cloudwatch_log_options = VpnConnectionTunnel2LogOptionsCloudwatchLogOptions(**cloudwatch_log_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c70a0cb4f28045d21c5df6238baa8f21a158c1ff05b04d09c3373ffce02ed84)
            check_type(argname="argument cloudwatch_log_options", value=cloudwatch_log_options, expected_type=type_hints["cloudwatch_log_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_log_options is not None:
            self._values["cloudwatch_log_options"] = cloudwatch_log_options

    @builtins.property
    def cloudwatch_log_options(
        self,
    ) -> typing.Optional["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions"]:
        '''cloudwatch_log_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#cloudwatch_log_options VpnConnection#cloudwatch_log_options}
        '''
        result = self._values.get("cloudwatch_log_options")
        return typing.cast(typing.Optional["VpnConnectionTunnel2LogOptionsCloudwatchLogOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel2LogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptionsCloudwatchLogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "log_enabled": "logEnabled",
        "log_group_arn": "logGroupArn",
        "log_output_format": "logOutputFormat",
    },
)
class VpnConnectionTunnel2LogOptionsCloudwatchLogOptions:
    def __init__(
        self,
        *,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83afa986daa56ec1bf87438375044ba4eec0772572289e758e7532249a69d7f8)
            check_type(argname="argument log_enabled", value=log_enabled, expected_type=type_hints["log_enabled"])
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            check_type(argname="argument log_output_format", value=log_output_format, expected_type=type_hints["log_output_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_enabled is not None:
            self._values["log_enabled"] = log_enabled
        if log_group_arn is not None:
            self._values["log_group_arn"] = log_group_arn
        if log_output_format is not None:
            self._values["log_output_format"] = log_output_format

    @builtins.property
    def log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.'''
        result = self._values.get("log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_output_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.'''
        result = self._values.get("log_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionTunnel2LogOptionsCloudwatchLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc0ff6bb9df7e14da341ac2e86c97346e8a7a7d42681749eea41203635615d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogEnabled")
    def reset_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogEnabled", []))

    @jsii.member(jsii_name="resetLogGroupArn")
    def reset_log_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupArn", []))

    @jsii.member(jsii_name="resetLogOutputFormat")
    def reset_log_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogOutputFormat", []))

    @builtins.property
    @jsii.member(jsii_name="logEnabledInput")
    def log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logOutputFormatInput")
    def log_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="logEnabled")
    def log_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logEnabled"))

    @log_enabled.setter
    def log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26e9466a7309d2f14244b4f6819179d30fb47012eeab748b216b6739c5bdf47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29962917b316d6260709a4e6930aa77d08bdb19edda5149e72132997f69e13da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logOutputFormat")
    def log_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logOutputFormat"))

    @log_output_format.setter
    def log_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895ec3a8050076e28d1a99e237e634182619e04c8e1c5a76a55b5654fd14c86a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c00effa68abdf2e3df61ef92c7990b2aeebd52e99854d2744be8735e9f3ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnConnectionTunnel2LogOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionTunnel2LogOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bdf76ce698b229adf8006678389de260036f2816a0541b260f9d83690b2abee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogOptions")
    def put_cloudwatch_log_options(
        self,
        *,
        log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_arn: typing.Optional[builtins.str] = None,
        log_output_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_enabled VpnConnection#log_enabled}.
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_group_arn VpnConnection#log_group_arn}.
        :param log_output_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/vpn_connection#log_output_format VpnConnection#log_output_format}.
        '''
        value = VpnConnectionTunnel2LogOptionsCloudwatchLogOptions(
            log_enabled=log_enabled,
            log_group_arn=log_group_arn,
            log_output_format=log_output_format,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogOptions", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogOptions")
    def reset_cloudwatch_log_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogOptions", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptions")
    def cloudwatch_log_options(
        self,
    ) -> VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference:
        return typing.cast(VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference, jsii.get(self, "cloudwatchLogOptions"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogOptionsInput")
    def cloudwatch_log_options_input(
        self,
    ) -> typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions], jsii.get(self, "cloudwatchLogOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionTunnel2LogOptions]:
        return typing.cast(typing.Optional[VpnConnectionTunnel2LogOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnConnectionTunnel2LogOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d697eabdfc95b926060acf53cfb77ceacee56a1a2dad822bebe518b456cabdaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionVgwTelemetry",
    jsii_struct_bases=[],
    name_mapping={},
)
class VpnConnectionVgwTelemetry:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionVgwTelemetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionVgwTelemetryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionVgwTelemetryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1426306bffb94832db23007e76f7a186fc98c329ee53d505f38bf224cdd4d2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnConnectionVgwTelemetryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6d01eb300b9c8b3e51c140694ed3a223ae4bb3cb6571decfb9240171412fa5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnConnectionVgwTelemetryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b500948a2c51e60bc64de7b061d1962291611dbeb37427e6f663ff3ffad849)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18ce0e7771243ef046a4788fdb43084e176ab5cf5d2fed179c225dc2f5d7db9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__766df6acd2423fcf3c25b98754ed3bef983b070186cbce96d79b1bad53f0531a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VpnConnectionVgwTelemetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.vpnConnection.VpnConnectionVgwTelemetryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2041da6c6d927bc6c8a96d73a7d98426769be549a3a82c157b433e870bd49a12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceptedRouteCount")
    def accepted_route_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceptedRouteCount"))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="lastStatusChange")
    def last_status_change(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastStatusChange"))

    @builtins.property
    @jsii.member(jsii_name="outsideIpAddress")
    def outside_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outsideIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusMessage")
    def status_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnConnectionVgwTelemetry]:
        return typing.cast(typing.Optional[VpnConnectionVgwTelemetry], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VpnConnectionVgwTelemetry]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27376639ea022fe7d206275b5a457191a782f904c62f564dcd84810035a7c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VpnConnection",
    "VpnConnectionConfig",
    "VpnConnectionRoutes",
    "VpnConnectionRoutesList",
    "VpnConnectionRoutesOutputReference",
    "VpnConnectionTunnel1LogOptions",
    "VpnConnectionTunnel1LogOptionsCloudwatchLogOptions",
    "VpnConnectionTunnel1LogOptionsCloudwatchLogOptionsOutputReference",
    "VpnConnectionTunnel1LogOptionsOutputReference",
    "VpnConnectionTunnel2LogOptions",
    "VpnConnectionTunnel2LogOptionsCloudwatchLogOptions",
    "VpnConnectionTunnel2LogOptionsCloudwatchLogOptionsOutputReference",
    "VpnConnectionTunnel2LogOptionsOutputReference",
    "VpnConnectionVgwTelemetry",
    "VpnConnectionVgwTelemetryList",
    "VpnConnectionVgwTelemetryOutputReference",
]

publication.publish()

def _typecheckingstub__53c837b21d9377340ba0b9ae12cf2e76d94617740e84d55b4fefcf3656c729b6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    customer_gateway_id: builtins.str,
    type: builtins.str,
    enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    outside_ip_address_type: typing.Optional[builtins.str] = None,
    remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transit_gateway_id: typing.Optional[builtins.str] = None,
    transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel1_log_options: typing.Optional[typing.Union[VpnConnectionTunnel1LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_preshared_key: typing.Optional[builtins.str] = None,
    tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel1_startup_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel2_log_options: typing.Optional[typing.Union[VpnConnectionTunnel2LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_preshared_key: typing.Optional[builtins.str] = None,
    tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel2_startup_action: typing.Optional[builtins.str] = None,
    tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
    vpn_gateway_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bbfe8e658651598180faa7792178e757e1594cab1c5725d4bf79aa7cb299ad78(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abf9c46ed4bb3f47680d25cb3bdbf124803bd45f18081f9a4e54dc30d871d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a597a783571e1a63fd897483ba6e6dd77f08dde93b49b22375eb288c5417645a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a23050816328fa4eed3c02faeb29143aae2459e080b23c2f268f0c86ef29f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e7d198301a19bbc64e3e93c2c19007e0be82e9eeccd5440f09bfebd53c0d5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37751e859decdfb7116bb6022bd8bbd79cfb93898bf5c1ad46ffaef1e2f256a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac41d1d16fba76525309ff68cf6c0d17aaf279402e148529dedf3600f150ef16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f621abb5602035be632a73741ae13a1a8e5615164c90999e37fa70a4d6ea08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34c6bd2a52f088022c7db1aa5877cdc3911a41303fd2fe55bdf1358ce89e88c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c079d03293bfbcfb51756d8732ea359494671dc053dc7c84bea5b0ffeeb8425(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84c0e133cce209f66f010e62c6ef4bfd0da57a72e8d737f553dcc91a2142bad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4dfaedbd380c34a5bb7674a1d0bac7674080311c5148fbcb6c1315df8a84ab(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fa7f3fd69016fed4f0bf9b88c002c4d248d84afde7174f70ab37fe03ff59a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e45875e21ff17777c7b5d9b2e1691c72e20c852c6ddeb40ca98a1e0c90f8e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c2a3dd896a72bbc0615a0d7a5cdcff5f2f3ad66beabeacb6a1f5e2d514a7ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f3e38dba911e397ef5499f1315ec0227a65ecab0869de2a924d4363b7e8e26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18ad954c568f82ca65ae709cd76eb6efe79d3669cfddd87986fc258aa03a328(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f5616456ccdb47e0cebbd7e45b37ea91bbb6f3fc9a2fc4f75f8a786676e146(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af8c93af7b53282c10ff31d42c885e3f22979e92732d4521dd5f98a032bbccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b884d344dab61d67efb46657582a259df2175b743080585909478875136b1ee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3e7b09ea772631cadf3c061d52a97fba3eba5a67f1cdd55e3f7f92467e18bd(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6879b9f4f272d2675089bdef8423ba5c63d88f148f0a6c5d19d80b72fc6312ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dfec2fc24831a67dd09a344f7bfa1580a4b431166bdb5f8c6eb227f6623b79(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937a07cbe33bb7a614a882a971d7878febfc6393b015dbd5314be3b1dde58a91(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd43922ca326ebaffd71b834ca7df4f287b0deecbd0c1282c7bf48e59cbb4ac7(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d0f1e97372c504072607efa5c8c0e96119fe6aafa21a1408aa1234d749e9af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250ffd79498403267529ba8b39da6fabc4812f977737db2a3e52b467cdbd3d35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd04ef500eeb50e34f25c6744c9d2429d5b7b9229a0e34237ac9ebbfbbc86c7a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4591ec1cfc0e35cc36700a843cac4599d1847ebc2d29528b91dd6be5fe3849(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ee6ec2e74c01e4f8d655285c6aba68818f2a113b9a9d6f94ad2e100b0b1163(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7ed9561de8f1c8a1744d0bc1ac78163ba1767db2f5266d4137f4f8e3c0b69a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb69553aee12ca217627fec0c8f36327657b957fd668a336ce83f05e090b4ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946f72627e1e83225abc45f05ede98cb0ff169a5e09fd18320065702cb5cbdfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618972dedb529a9c0ec020ef8e28356f28cb604c4c75ef9ab12adb750cbe9e4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68f03edb168bc91084054d1b8618b43c88f9aea9b60c3ac41ce9ce99bc28cce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57df11479a5f8639103c4c5ec35adb578efc47d5b67f6240e16844aca2a5962(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4c20d9e98c6e2648755205970d5ef96940816bb16c12fa50a34946eaddf10c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df74671191b758ce33375e2555b722967c5dfaf87de9adf880bfe9c17ffbaea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ae08efa74387ebbcaa10b1814c816ceb6735b7133e554f3707ce524d9403c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c84ccff4902b168078a58d554f18f8c366b7878456505efd9195d9d448d37d(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57835d15862c4bd2b27e79613f6a696b7fbcc0a49ba5a38904a481c89bdb62e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97681b107754ed3c1d56bac733b35fc2feb8a5f3afe7bffdf2a802426e155777(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53621394bc7eab682c533705cdd9066113e3976b6195f1d7a4b622747bca1f6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7240c66d58db90e7c651eccc1b6d08d5a5450b306b952329dc6f28721553c3d1(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ae841101600d0091df1038861773f42f15807c7a021a8bf47dc2515ff3c3f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e15e85fa59ea62a1a8f3c61f65d3575b4eb34a1f1b7553b4b295d41a13a5230(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35eaf87fb0d4f8ff6127bb8e70afc777137b06ac8fb5502533e492f7c62e8fbf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1eaf598a6ba92896055e47a8f50efa039ccacac989610dea84554a0fdeea6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e0b1601bf591857312374186b7092aa39babfa5e580774af7f1b9bc253105e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c65d06213747991f3ed316f20a710546f7eefc017ccb8abd2bf60122fb1b838(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9f988ef712223bc561a84db1abf35611f79010d2a6260ffc507ebc0482fee2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17594096376b2b497777b66d44aab6cd8e8da35edd8ef533fd7f85255957e7f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c3ba8141afa1d83ef9d6e9a4866c51c8b5617a8777ee92c0376ae8ee9e897d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed913dd2c7d2d93cfeb82fef754f5c6e60fbe372d9a5490adac7beae7067a4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06e66c5a8423174e443b7a78e58c369716d7ae39425b203c9101d97bbc55534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1ff5171a739715b7a4605259904c2502c4c339a5fbc4f33a1eeec85564baf4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    customer_gateway_id: builtins.str,
    type: builtins.str,
    enable_acceleration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    local_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    local_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    outside_ip_address_type: typing.Optional[builtins.str] = None,
    remote_ipv4_network_cidr: typing.Optional[builtins.str] = None,
    remote_ipv6_network_cidr: typing.Optional[builtins.str] = None,
    static_routes_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    transit_gateway_id: typing.Optional[builtins.str] = None,
    transport_transit_gateway_attachment_id: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel1_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel1_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel1_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel1_log_options: typing.Optional[typing.Union[VpnConnectionTunnel1LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel1_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel1_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel1_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_preshared_key: typing.Optional[builtins.str] = None,
    tunnel1_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel1_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel1_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel1_startup_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_action: typing.Optional[builtins.str] = None,
    tunnel2_dpd_timeout_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_enable_tunnel_lifecycle_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel2_ike_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_inside_cidr: typing.Optional[builtins.str] = None,
    tunnel2_inside_ipv6_cidr: typing.Optional[builtins.str] = None,
    tunnel2_log_options: typing.Optional[typing.Union[VpnConnectionTunnel2LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tunnel2_phase1_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase1_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase1_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_phase2_dh_group_numbers: typing.Optional[typing.Sequence[jsii.Number]] = None,
    tunnel2_phase2_encryption_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_integrity_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel2_phase2_lifetime_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_preshared_key: typing.Optional[builtins.str] = None,
    tunnel2_rekey_fuzz_percentage: typing.Optional[jsii.Number] = None,
    tunnel2_rekey_margin_time_seconds: typing.Optional[jsii.Number] = None,
    tunnel2_replay_window_size: typing.Optional[jsii.Number] = None,
    tunnel2_startup_action: typing.Optional[builtins.str] = None,
    tunnel_inside_ip_version: typing.Optional[builtins.str] = None,
    vpn_gateway_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970e5749a84bc9ebc68139609bf8c29c93150e7cb5bd62d6203860809f36b62c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab13017741dafe587f172a9637f040a374914aa778ecaa65495bf9b780f6f12(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdf97da856a68ff7c296b8b698c540d7a334f4029e4c8fa5bcd3d95a70da578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda7514c58abac015a057ae177987dff0e83ddd1a2b3a94ad1b09cd927b1f7ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed4eb64dc18f31603a9db5f34d6226000a2926d6435310444e001525d742175(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c188828f615983f8d9f5c8c5216d5e0fa7cf08ae8b4c613b6652bc28d585939d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdf94e5b268f70fc3681cdceae26303cc275872f31097da0a2a011dba0a2ad8(
    value: typing.Optional[VpnConnectionRoutes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2987178142993d954c0b9fb8c3c1dc0aead090fbf7670bf0e2df9759e17821b1(
    *,
    cloudwatch_log_options: typing.Optional[typing.Union[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b428cdf57040466ff9e463429eb04d8967afd4f3062a33f5397ea359d413e33(
    *,
    log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_arn: typing.Optional[builtins.str] = None,
    log_output_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835aff9933dc21765aa06eaa383b3763a6c5e10d4e647d0bc204c3c96e4bba56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d379abf8b6b5dbdb28504b9c14328d0fab0fb2963dfb80a7dfdfe1e91e73fe2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7557b3c80f3112000776b540ac3f7fe35c5c782620dc8ae4f2efa7d34871fac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1942316727f81d87140720de166f8760dd6b7bfb77f29381192d0d305ece8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634eaf648a9cf1218a8553b5c1e81cbc939ebf7d3773a8a87c0e5f69e5ec115d(
    value: typing.Optional[VpnConnectionTunnel1LogOptionsCloudwatchLogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809cac86660fa0af7c13aaf88567bf05e7f81b789485baed699796acc30b7119(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e1ee8a8eb726df23ffe068b98a8e76899958f76ea8b5ef29bb1ed0c973c949(
    value: typing.Optional[VpnConnectionTunnel1LogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c70a0cb4f28045d21c5df6238baa8f21a158c1ff05b04d09c3373ffce02ed84(
    *,
    cloudwatch_log_options: typing.Optional[typing.Union[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83afa986daa56ec1bf87438375044ba4eec0772572289e758e7532249a69d7f8(
    *,
    log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_arn: typing.Optional[builtins.str] = None,
    log_output_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc0ff6bb9df7e14da341ac2e86c97346e8a7a7d42681749eea41203635615d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26e9466a7309d2f14244b4f6819179d30fb47012eeab748b216b6739c5bdf47(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29962917b316d6260709a4e6930aa77d08bdb19edda5149e72132997f69e13da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895ec3a8050076e28d1a99e237e634182619e04c8e1c5a76a55b5654fd14c86a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c00effa68abdf2e3df61ef92c7990b2aeebd52e99854d2744be8735e9f3ab3(
    value: typing.Optional[VpnConnectionTunnel2LogOptionsCloudwatchLogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bdf76ce698b229adf8006678389de260036f2816a0541b260f9d83690b2abee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d697eabdfc95b926060acf53cfb77ceacee56a1a2dad822bebe518b456cabdaf(
    value: typing.Optional[VpnConnectionTunnel2LogOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1426306bffb94832db23007e76f7a186fc98c329ee53d505f38bf224cdd4d2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6d01eb300b9c8b3e51c140694ed3a223ae4bb3cb6571decfb9240171412fa5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b500948a2c51e60bc64de7b061d1962291611dbeb37427e6f663ff3ffad849(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ce0e7771243ef046a4788fdb43084e176ab5cf5d2fed179c225dc2f5d7db9e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766df6acd2423fcf3c25b98754ed3bef983b070186cbce96d79b1bad53f0531a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2041da6c6d927bc6c8a96d73a7d98426769be549a3a82c157b433e870bd49a12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27376639ea022fe7d206275b5a457191a782f904c62f564dcd84810035a7c0b(
    value: typing.Optional[VpnConnectionVgwTelemetry],
) -> None:
    """Type checking stubs"""
    pass
