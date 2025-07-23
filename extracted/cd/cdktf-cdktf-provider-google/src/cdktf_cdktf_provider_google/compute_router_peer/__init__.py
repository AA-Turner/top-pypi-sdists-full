r'''
# `google_compute_router_peer`

Refer to the Terraform Registry for docs: [`google_compute_router_peer`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer).
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


class ComputeRouterPeer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer google_compute_router_peer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        interface: builtins.str,
        name: builtins.str,
        peer_asn: jsii.Number,
        router: builtins.str,
        advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterPeerAdvertisedIpRanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        advertised_route_priority: typing.Optional[jsii.Number] = None,
        advertise_mode: typing.Optional[builtins.str] = None,
        bfd: typing.Optional[typing.Union["ComputeRouterPeerBfd", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_learned_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterPeerCustomLearnedIpRanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_learned_route_priority: typing.Optional[jsii.Number] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        export_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        import_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ipv4_nexthop_address: typing.Optional[builtins.str] = None,
        ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        md5_authentication_key: typing.Optional[typing.Union["ComputeRouterPeerMd5AuthenticationKey", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_ip_address: typing.Optional[builtins.str] = None,
        peer_ipv4_nexthop_address: typing.Optional[builtins.str] = None,
        peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        router_appliance_instance: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouterPeerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zero_advertised_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_custom_learned_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer google_compute_router_peer} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param interface: Name of the interface the BGP peer is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#interface ComputeRouterPeer#interface}
        :param name: Name of this BGP peer. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#name ComputeRouterPeer#name}
        :param peer_asn: Peer BGP Autonomous System Number (ASN). Each BGP interface may use a different value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_asn ComputeRouterPeer#peer_asn}
        :param router: The name of the Cloud Router in which this BgpPeer will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#router ComputeRouterPeer#router}
        :param advertised_groups: User-specified list of prefix groups to advertise in custom mode, which currently supports the following option:. - 'ALL_SUBNETS': Advertises all of the router's own VPC subnets. This excludes any routes learned for subnets that use VPC Network Peering. Note that this field can only be populated if advertiseMode is 'CUSTOM' and overrides the list defined for the router (in the "bgp" message). These groups are advertised in addition to any specified prefixes. Leave this field blank to advertise no custom groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_groups ComputeRouterPeer#advertised_groups}
        :param advertised_ip_ranges: advertised_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_ip_ranges ComputeRouterPeer#advertised_ip_ranges}
        :param advertised_route_priority: The priority of routes advertised to this BGP peer. Where there is more than one matching route of maximum length, the routes with the lowest priority value win. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_route_priority ComputeRouterPeer#advertised_route_priority}
        :param advertise_mode: User-specified flag to indicate which mode to use for advertisement. Valid values of this enum field are: 'DEFAULT', 'CUSTOM' Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertise_mode ComputeRouterPeer#advertise_mode}
        :param bfd: bfd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#bfd ComputeRouterPeer#bfd}
        :param custom_learned_ip_ranges: custom_learned_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#custom_learned_ip_ranges ComputeRouterPeer#custom_learned_ip_ranges}
        :param custom_learned_route_priority: The user-defined custom learned route priority for a BGP session. This value is applied to all custom learned route ranges for the session. You can choose a value from 0 to 65335. If you don't provide a value, Google Cloud assigns a priority of 100 to the ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#custom_learned_route_priority ComputeRouterPeer#custom_learned_route_priority}
        :param enable: The status of the BGP peer connection. If set to false, any active session with the peer is terminated and all associated routing information is removed. If set to true, the peer connection can be established with routing information. The default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable ComputeRouterPeer#enable}
        :param enable_ipv4: Enable IPv4 traffic over BGP Peer. It is enabled by default if the peerIpAddress is version 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable_ipv4 ComputeRouterPeer#enable_ipv4}
        :param enable_ipv6: Enable IPv6 traffic over BGP Peer. If not specified, it is disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable_ipv6 ComputeRouterPeer#enable_ipv6}
        :param export_policies: routers.list of export policies applied to this peer, in the order they must be evaluated. The name must correspond to an existing policy that has ROUTE_POLICY_TYPE_EXPORT type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#export_policies ComputeRouterPeer#export_policies}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#id ComputeRouterPeer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_policies: routers.list of import policies applied to this peer, in the order they must be evaluated. The name must correspond to an existing policy that has ROUTE_POLICY_TYPE_IMPORT type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#import_policies ComputeRouterPeer#import_policies}
        :param ip_address: IP address of the interface inside Google Cloud Platform. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ip_address ComputeRouterPeer#ip_address}
        :param ipv4_nexthop_address: IPv4 address of the interface inside Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ipv4_nexthop_address ComputeRouterPeer#ipv4_nexthop_address}
        :param ipv6_nexthop_address: IPv6 address of the interface inside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ipv6_nexthop_address ComputeRouterPeer#ipv6_nexthop_address}
        :param md5_authentication_key: md5_authentication_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#md5_authentication_key ComputeRouterPeer#md5_authentication_key}
        :param peer_ip_address: IP address of the BGP interface outside Google Cloud Platform. Only IPv4 is supported. Required if 'ip_address' is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ip_address ComputeRouterPeer#peer_ip_address}
        :param peer_ipv4_nexthop_address: IPv4 address of the BGP interface outside Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ipv4_nexthop_address ComputeRouterPeer#peer_ipv4_nexthop_address}
        :param peer_ipv6_nexthop_address: IPv6 address of the BGP interface outside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ipv6_nexthop_address ComputeRouterPeer#peer_ipv6_nexthop_address}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#project ComputeRouterPeer#project}.
        :param region: Region where the router and BgpPeer reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#region ComputeRouterPeer#region}
        :param router_appliance_instance: The URI of the VM instance that is used as third-party router appliances such as Next Gen Firewalls, Virtual Routers, or Router Appliances. The VM instance must be located in zones contained in the same region as this Cloud Router. The VM instance is the peer side of the BGP session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#router_appliance_instance ComputeRouterPeer#router_appliance_instance}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#timeouts ComputeRouterPeer#timeouts}
        :param zero_advertised_route_priority: Force the advertised_route_priority to be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#zero_advertised_route_priority ComputeRouterPeer#zero_advertised_route_priority}
        :param zero_custom_learned_route_priority: Force the custom_learned_route_priority to be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#zero_custom_learned_route_priority ComputeRouterPeer#zero_custom_learned_route_priority}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42db39c65d77c39d57a1e757fba207ea507a585b22ecb04dc52326bd3f288b90)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRouterPeerConfig(
            interface=interface,
            name=name,
            peer_asn=peer_asn,
            router=router,
            advertised_groups=advertised_groups,
            advertised_ip_ranges=advertised_ip_ranges,
            advertised_route_priority=advertised_route_priority,
            advertise_mode=advertise_mode,
            bfd=bfd,
            custom_learned_ip_ranges=custom_learned_ip_ranges,
            custom_learned_route_priority=custom_learned_route_priority,
            enable=enable,
            enable_ipv4=enable_ipv4,
            enable_ipv6=enable_ipv6,
            export_policies=export_policies,
            id=id,
            import_policies=import_policies,
            ip_address=ip_address,
            ipv4_nexthop_address=ipv4_nexthop_address,
            ipv6_nexthop_address=ipv6_nexthop_address,
            md5_authentication_key=md5_authentication_key,
            peer_ip_address=peer_ip_address,
            peer_ipv4_nexthop_address=peer_ipv4_nexthop_address,
            peer_ipv6_nexthop_address=peer_ipv6_nexthop_address,
            project=project,
            region=region,
            router_appliance_instance=router_appliance_instance,
            timeouts=timeouts,
            zero_advertised_route_priority=zero_advertised_route_priority,
            zero_custom_learned_route_priority=zero_custom_learned_route_priority,
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
        '''Generates CDKTF code for importing a ComputeRouterPeer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRouterPeer to import.
        :param import_from_id: The id of the existing ComputeRouterPeer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRouterPeer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88a692d9c6351097aed055767060f262aec1cbcef50edfa046a00b66837ac77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvertisedIpRanges")
    def put_advertised_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterPeerAdvertisedIpRanges", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687b08699f1f8a9087ff13e0b297045942774b80f8c9431ceeb4cea261a48faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdvertisedIpRanges", [value]))

    @jsii.member(jsii_name="putBfd")
    def put_bfd(
        self,
        *,
        session_initialization_mode: builtins.str,
        min_receive_interval: typing.Optional[jsii.Number] = None,
        min_transmit_interval: typing.Optional[jsii.Number] = None,
        multiplier: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param session_initialization_mode: The BFD session initialization mode for this BGP peer. If set to 'ACTIVE', the Cloud Router will initiate the BFD session for this BGP peer. If set to 'PASSIVE', the Cloud Router will wait for the peer router to initiate the BFD session for this BGP peer. If set to 'DISABLED', BFD is disabled for this BGP peer. Possible values: ["ACTIVE", "DISABLED", "PASSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#session_initialization_mode ComputeRouterPeer#session_initialization_mode}
        :param min_receive_interval: The minimum interval, in milliseconds, between BFD control packets received from the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the transmit interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#min_receive_interval ComputeRouterPeer#min_receive_interval}
        :param min_transmit_interval: The minimum interval, in milliseconds, between BFD control packets transmitted to the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the corresponding receive interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#min_transmit_interval ComputeRouterPeer#min_transmit_interval}
        :param multiplier: The number of consecutive BFD packets that must be missed before BFD declares that a peer is unavailable. If set, the value must be a value between 5 and 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#multiplier ComputeRouterPeer#multiplier}
        '''
        value = ComputeRouterPeerBfd(
            session_initialization_mode=session_initialization_mode,
            min_receive_interval=min_receive_interval,
            min_transmit_interval=min_transmit_interval,
            multiplier=multiplier,
        )

        return typing.cast(None, jsii.invoke(self, "putBfd", [value]))

    @jsii.member(jsii_name="putCustomLearnedIpRanges")
    def put_custom_learned_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterPeerCustomLearnedIpRanges", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9361ee095a98d8f5eb2cb1a0261a17afdd308bd2ee1f5a3307004c01afb5192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomLearnedIpRanges", [value]))

    @jsii.member(jsii_name="putMd5AuthenticationKey")
    def put_md5_authentication_key(
        self,
        *,
        key: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param key: Value of the key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#key ComputeRouterPeer#key}
        :param name: [REQUIRED] Name used to identify the key. Must be unique within a router. Must be referenced by exactly one bgpPeer. Must comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#name ComputeRouterPeer#name}
        '''
        value = ComputeRouterPeerMd5AuthenticationKey(key=key, name=name)

        return typing.cast(None, jsii.invoke(self, "putMd5AuthenticationKey", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#create ComputeRouterPeer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#delete ComputeRouterPeer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#update ComputeRouterPeer#update}.
        '''
        value = ComputeRouterPeerTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvertisedGroups")
    def reset_advertised_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedGroups", []))

    @jsii.member(jsii_name="resetAdvertisedIpRanges")
    def reset_advertised_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedIpRanges", []))

    @jsii.member(jsii_name="resetAdvertisedRoutePriority")
    def reset_advertised_route_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedRoutePriority", []))

    @jsii.member(jsii_name="resetAdvertiseMode")
    def reset_advertise_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertiseMode", []))

    @jsii.member(jsii_name="resetBfd")
    def reset_bfd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBfd", []))

    @jsii.member(jsii_name="resetCustomLearnedIpRanges")
    def reset_custom_learned_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomLearnedIpRanges", []))

    @jsii.member(jsii_name="resetCustomLearnedRoutePriority")
    def reset_custom_learned_route_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomLearnedRoutePriority", []))

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetEnableIpv4")
    def reset_enable_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpv4", []))

    @jsii.member(jsii_name="resetEnableIpv6")
    def reset_enable_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpv6", []))

    @jsii.member(jsii_name="resetExportPolicies")
    def reset_export_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportPolicies", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportPolicies")
    def reset_import_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportPolicies", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetIpv4NexthopAddress")
    def reset_ipv4_nexthop_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4NexthopAddress", []))

    @jsii.member(jsii_name="resetIpv6NexthopAddress")
    def reset_ipv6_nexthop_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6NexthopAddress", []))

    @jsii.member(jsii_name="resetMd5AuthenticationKey")
    def reset_md5_authentication_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMd5AuthenticationKey", []))

    @jsii.member(jsii_name="resetPeerIpAddress")
    def reset_peer_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerIpAddress", []))

    @jsii.member(jsii_name="resetPeerIpv4NexthopAddress")
    def reset_peer_ipv4_nexthop_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerIpv4NexthopAddress", []))

    @jsii.member(jsii_name="resetPeerIpv6NexthopAddress")
    def reset_peer_ipv6_nexthop_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerIpv6NexthopAddress", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRouterApplianceInstance")
    def reset_router_appliance_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouterApplianceInstance", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZeroAdvertisedRoutePriority")
    def reset_zero_advertised_route_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZeroAdvertisedRoutePriority", []))

    @jsii.member(jsii_name="resetZeroCustomLearnedRoutePriority")
    def reset_zero_custom_learned_route_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZeroCustomLearnedRoutePriority", []))

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
    @jsii.member(jsii_name="advertisedIpRanges")
    def advertised_ip_ranges(self) -> "ComputeRouterPeerAdvertisedIpRangesList":
        return typing.cast("ComputeRouterPeerAdvertisedIpRangesList", jsii.get(self, "advertisedIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="bfd")
    def bfd(self) -> "ComputeRouterPeerBfdOutputReference":
        return typing.cast("ComputeRouterPeerBfdOutputReference", jsii.get(self, "bfd"))

    @builtins.property
    @jsii.member(jsii_name="customLearnedIpRanges")
    def custom_learned_ip_ranges(self) -> "ComputeRouterPeerCustomLearnedIpRangesList":
        return typing.cast("ComputeRouterPeerCustomLearnedIpRangesList", jsii.get(self, "customLearnedIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="isAdvertisedRoutePrioritySet")
    def is_advertised_route_priority_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isAdvertisedRoutePrioritySet"))

    @builtins.property
    @jsii.member(jsii_name="isCustomLearnedPrioritySet")
    def is_custom_learned_priority_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isCustomLearnedPrioritySet"))

    @builtins.property
    @jsii.member(jsii_name="managementType")
    def management_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managementType"))

    @builtins.property
    @jsii.member(jsii_name="md5AuthenticationKey")
    def md5_authentication_key(
        self,
    ) -> "ComputeRouterPeerMd5AuthenticationKeyOutputReference":
        return typing.cast("ComputeRouterPeerMd5AuthenticationKeyOutputReference", jsii.get(self, "md5AuthenticationKey"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRouterPeerTimeoutsOutputReference":
        return typing.cast("ComputeRouterPeerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advertisedGroupsInput")
    def advertised_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advertisedGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedIpRangesInput")
    def advertised_ip_ranges_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterPeerAdvertisedIpRanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterPeerAdvertisedIpRanges"]]], jsii.get(self, "advertisedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedRoutePriorityInput")
    def advertised_route_priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "advertisedRoutePriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="advertiseModeInput")
    def advertise_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "advertiseModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bfdInput")
    def bfd_input(self) -> typing.Optional["ComputeRouterPeerBfd"]:
        return typing.cast(typing.Optional["ComputeRouterPeerBfd"], jsii.get(self, "bfdInput"))

    @builtins.property
    @jsii.member(jsii_name="customLearnedIpRangesInput")
    def custom_learned_ip_ranges_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterPeerCustomLearnedIpRanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterPeerCustomLearnedIpRanges"]]], jsii.get(self, "customLearnedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="customLearnedRoutePriorityInput")
    def custom_learned_route_priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customLearnedRoutePriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpv4Input")
    def enable_ipv4_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpv4Input"))

    @builtins.property
    @jsii.member(jsii_name="enableIpv6Input")
    def enable_ipv6_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpv6Input"))

    @builtins.property
    @jsii.member(jsii_name="exportPoliciesInput")
    def export_policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exportPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importPoliciesInput")
    def import_policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "importPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4NexthopAddressInput")
    def ipv4_nexthop_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4NexthopAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6NexthopAddressInput")
    def ipv6_nexthop_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6NexthopAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="md5AuthenticationKeyInput")
    def md5_authentication_key_input(
        self,
    ) -> typing.Optional["ComputeRouterPeerMd5AuthenticationKey"]:
        return typing.cast(typing.Optional["ComputeRouterPeerMd5AuthenticationKey"], jsii.get(self, "md5AuthenticationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerAsnInput")
    def peer_asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "peerAsnInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIpAddressInput")
    def peer_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIpv4NexthopAddressInput")
    def peer_ipv4_nexthop_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIpv4NexthopAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIpv6NexthopAddressInput")
    def peer_ipv6_nexthop_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIpv6NexthopAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="routerApplianceInstanceInput")
    def router_appliance_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerApplianceInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="routerInput")
    def router_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouterPeerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouterPeerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zeroAdvertisedRoutePriorityInput")
    def zero_advertised_route_priority_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zeroAdvertisedRoutePriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="zeroCustomLearnedRoutePriorityInput")
    def zero_custom_learned_route_priority_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zeroCustomLearnedRoutePriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedGroups")
    def advertised_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advertisedGroups"))

    @advertised_groups.setter
    def advertised_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0515e14e0357ef24c2573a77fdc038e59f92b1bab80a2d3f5e59464cdf774b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advertisedRoutePriority")
    def advertised_route_priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "advertisedRoutePriority"))

    @advertised_route_priority.setter
    def advertised_route_priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fad905773bf8a255fe2c1b0443c17b14ef53899cf8b3cf3f54ccb57a7c42140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedRoutePriority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advertiseMode")
    def advertise_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "advertiseMode"))

    @advertise_mode.setter
    def advertise_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a79e40a5a45bd43bcf7e43eafb383e42ee2971aa5faa96e8dd71e115850da60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertiseMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customLearnedRoutePriority")
    def custom_learned_route_priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customLearnedRoutePriority"))

    @custom_learned_route_priority.setter
    def custom_learned_route_priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00c64341595645a0833edde1b460990314be1c1b3baaa789b8c1cd1f5860473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLearnedRoutePriority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52eb5988236a35be86a83851a033eab4031a1f84cd4b490b5b79e8a9d7552858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableIpv4")
    def enable_ipv4(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpv4"))

    @enable_ipv4.setter
    def enable_ipv4(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7bbb08815f80f6cde456a8fdf0b06fa5d60236b8a159e54631c78d5e35046a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpv4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableIpv6")
    def enable_ipv6(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpv6"))

    @enable_ipv6.setter
    def enable_ipv6(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9b229d6f74ee416335bbe68b933aee08a957927368d4582040148dfac0a9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpv6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exportPolicies")
    def export_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exportPolicies"))

    @export_policies.setter
    def export_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e08ed1a5657452edbfc7e456f1eeedfe20ac00cf53a7425bc4f7bd2b103eb76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exportPolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a97e557a1a38e5a3f54a7301b8dc145cf96fe937b46c9785ee535045f71f9e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importPolicies")
    def import_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "importPolicies"))

    @import_policies.setter
    def import_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bed6698e1ac24db53b85ae9e20193d6fb2cf2c3ebbe01ab37cfef17731b3266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importPolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c9fcc768f9b7f607e2817e330666df84bee3bc3820115e0ed1f800e36e7e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134764f8baece5d8374d8aaa4bbc1646b0902216a392f65d1c60cd7fd464f5e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4NexthopAddress")
    def ipv4_nexthop_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4NexthopAddress"))

    @ipv4_nexthop_address.setter
    def ipv4_nexthop_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa93bbffa91f88b57eaa25ea2dad922460858c79ee7997c2069855f81434b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4NexthopAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6NexthopAddress")
    def ipv6_nexthop_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6NexthopAddress"))

    @ipv6_nexthop_address.setter
    def ipv6_nexthop_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbdde41ad8f24bca30c69665d405eccb02bfa8aac4757c184059294fa6c4543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6NexthopAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924cf4987d952b4a9ddeeb257ab628c317761ab0c3368ad0f4c6a06b215dacbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerAsn")
    def peer_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "peerAsn"))

    @peer_asn.setter
    def peer_asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edaad33cd7d6406f19a2c905ebbc293c8424c1b12eddcfb45af0cbc13fcad8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerAsn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerIpAddress")
    def peer_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpAddress"))

    @peer_ip_address.setter
    def peer_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7105c10949de353d522b33a13b36fc8bb721539afe25453a3de6b6cc39845bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerIpv4NexthopAddress")
    def peer_ipv4_nexthop_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpv4NexthopAddress"))

    @peer_ipv4_nexthop_address.setter
    def peer_ipv4_nexthop_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e08c6d2ad8d7de7e385622552f2a96d0a8098897af9e8bddd45e9957ec304d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpv4NexthopAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerIpv6NexthopAddress")
    def peer_ipv6_nexthop_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpv6NexthopAddress"))

    @peer_ipv6_nexthop_address.setter
    def peer_ipv6_nexthop_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854dd1cd5ceb1b26c93849f73937201ddfd5d81d85591c3c3e296dcf480ec0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpv6NexthopAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4459c49dd20a47670f6453fae920a3b74ff816a7ab67ff365ce86400c3a7a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee27b12375f8c5ad7c4aa2273a862e8e1b640a49f2bf5154c014d6e06e8201df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "router"))

    @router.setter
    def router(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29766f20543accd7aaa1b410b314e2e9f05b2a5deccb889059d3126d99bf2e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "router", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routerApplianceInstance")
    def router_appliance_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routerApplianceInstance"))

    @router_appliance_instance.setter
    def router_appliance_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d4fbbd327c7c302d7bc0f861340eb35d14a40a099e08b394de62e8d457493a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routerApplianceInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zeroAdvertisedRoutePriority")
    def zero_advertised_route_priority(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zeroAdvertisedRoutePriority"))

    @zero_advertised_route_priority.setter
    def zero_advertised_route_priority(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b6465ca903935486b06ac7b39e342d3b23b896a1ef6f03c3116010d0d90dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroAdvertisedRoutePriority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zeroCustomLearnedRoutePriority")
    def zero_custom_learned_route_priority(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zeroCustomLearnedRoutePriority"))

    @zero_custom_learned_route_priority.setter
    def zero_custom_learned_route_priority(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c268a0ec045f31d1b210d900f17cda4bbd73c46d47cccc39133cda11f2fdfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroCustomLearnedRoutePriority", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerAdvertisedIpRanges",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "description": "description"},
)
class ComputeRouterPeerAdvertisedIpRanges:
    def __init__(
        self,
        *,
        range: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param range: The IP range to advertise. The value must be a CIDR-formatted string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#range ComputeRouterPeer#range}
        :param description: User-specified description for the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#description ComputeRouterPeer#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9eeb820686c63c226d2cd0c1d3ddd5b66aebbbfb834b9a00f3b37df44e2fea)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def range(self) -> builtins.str:
        '''The IP range to advertise. The value must be a CIDR-formatted string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#range ComputeRouterPeer#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-specified description for the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#description ComputeRouterPeer#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterPeerAdvertisedIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterPeerAdvertisedIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerAdvertisedIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a5e4e60c04c28cf69d7b8532669a55ac40e0d38c0f18328375ce73591c74c00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRouterPeerAdvertisedIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f735e4a4527e85afb802f46ff6f3ccf998d8f5cce16b4c8dc681a6eb4029c09a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouterPeerAdvertisedIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be486e537c0ec4a618caca313269fc4fc5cfdd56a36083f74f8022fb4d03dc56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31039921f2dfbc7c91b3b6899669f4aa9fdf9e2397aca9eacde5c1e954592672)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a91a77a27b7c63f426b93a60e80218dd36b9c4df7db8b08a92e7912b04025d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerAdvertisedIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerAdvertisedIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerAdvertisedIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29ad310af8c45f7d204e903e380325868d319b6b1114407c5f717850c6ca6eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterPeerAdvertisedIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerAdvertisedIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95befba4df0b08f7c5a836185161fefde0a887560ab048b7cb317cb13788696f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6be5323dfbda0aa8455a8990aa3aabc7f396133fc839819b9d33486d89b182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "range"))

    @range.setter
    def range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d2b02827ea696a0885758c25f55d6f17be8dad31e251d91776018b368c910c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "range", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerAdvertisedIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerAdvertisedIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerAdvertisedIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9bd5e277a85f5aece0edce93eec482f79fce801b361258cff1d92ee8070adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerBfd",
    jsii_struct_bases=[],
    name_mapping={
        "session_initialization_mode": "sessionInitializationMode",
        "min_receive_interval": "minReceiveInterval",
        "min_transmit_interval": "minTransmitInterval",
        "multiplier": "multiplier",
    },
)
class ComputeRouterPeerBfd:
    def __init__(
        self,
        *,
        session_initialization_mode: builtins.str,
        min_receive_interval: typing.Optional[jsii.Number] = None,
        min_transmit_interval: typing.Optional[jsii.Number] = None,
        multiplier: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param session_initialization_mode: The BFD session initialization mode for this BGP peer. If set to 'ACTIVE', the Cloud Router will initiate the BFD session for this BGP peer. If set to 'PASSIVE', the Cloud Router will wait for the peer router to initiate the BFD session for this BGP peer. If set to 'DISABLED', BFD is disabled for this BGP peer. Possible values: ["ACTIVE", "DISABLED", "PASSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#session_initialization_mode ComputeRouterPeer#session_initialization_mode}
        :param min_receive_interval: The minimum interval, in milliseconds, between BFD control packets received from the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the transmit interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#min_receive_interval ComputeRouterPeer#min_receive_interval}
        :param min_transmit_interval: The minimum interval, in milliseconds, between BFD control packets transmitted to the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the corresponding receive interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#min_transmit_interval ComputeRouterPeer#min_transmit_interval}
        :param multiplier: The number of consecutive BFD packets that must be missed before BFD declares that a peer is unavailable. If set, the value must be a value between 5 and 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#multiplier ComputeRouterPeer#multiplier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33561511d54c50aaa29e0592ccc2884bd4438f468333506f19eea932a0fe7ddf)
            check_type(argname="argument session_initialization_mode", value=session_initialization_mode, expected_type=type_hints["session_initialization_mode"])
            check_type(argname="argument min_receive_interval", value=min_receive_interval, expected_type=type_hints["min_receive_interval"])
            check_type(argname="argument min_transmit_interval", value=min_transmit_interval, expected_type=type_hints["min_transmit_interval"])
            check_type(argname="argument multiplier", value=multiplier, expected_type=type_hints["multiplier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "session_initialization_mode": session_initialization_mode,
        }
        if min_receive_interval is not None:
            self._values["min_receive_interval"] = min_receive_interval
        if min_transmit_interval is not None:
            self._values["min_transmit_interval"] = min_transmit_interval
        if multiplier is not None:
            self._values["multiplier"] = multiplier

    @builtins.property
    def session_initialization_mode(self) -> builtins.str:
        '''The BFD session initialization mode for this BGP peer.

        If set to 'ACTIVE', the Cloud Router will initiate the BFD session
        for this BGP peer. If set to 'PASSIVE', the Cloud Router will wait
        for the peer router to initiate the BFD session for this BGP peer.
        If set to 'DISABLED', BFD is disabled for this BGP peer. Possible values: ["ACTIVE", "DISABLED", "PASSIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#session_initialization_mode ComputeRouterPeer#session_initialization_mode}
        '''
        result = self._values.get("session_initialization_mode")
        assert result is not None, "Required property 'session_initialization_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def min_receive_interval(self) -> typing.Optional[jsii.Number]:
        '''The minimum interval, in milliseconds, between BFD control packets received from the peer router.

        The actual value is negotiated
        between the two routers and is equal to the greater of this value
        and the transmit interval of the other router. If set, this value
        must be between 1000 and 30000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#min_receive_interval ComputeRouterPeer#min_receive_interval}
        '''
        result = self._values.get("min_receive_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_transmit_interval(self) -> typing.Optional[jsii.Number]:
        '''The minimum interval, in milliseconds, between BFD control packets transmitted to the peer router.

        The actual value is negotiated
        between the two routers and is equal to the greater of this value
        and the corresponding receive interval of the other router. If set,
        this value must be between 1000 and 30000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#min_transmit_interval ComputeRouterPeer#min_transmit_interval}
        '''
        result = self._values.get("min_transmit_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def multiplier(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive BFD packets that must be missed before BFD declares that a peer is unavailable.

        If set, the value must
        be a value between 5 and 16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#multiplier ComputeRouterPeer#multiplier}
        '''
        result = self._values.get("multiplier")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterPeerBfd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterPeerBfdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerBfdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa6ad26883a06146d781dc0b56565f963228922e260df133a7d1fbb55ec7c08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinReceiveInterval")
    def reset_min_receive_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinReceiveInterval", []))

    @jsii.member(jsii_name="resetMinTransmitInterval")
    def reset_min_transmit_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTransmitInterval", []))

    @jsii.member(jsii_name="resetMultiplier")
    def reset_multiplier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiplier", []))

    @builtins.property
    @jsii.member(jsii_name="minReceiveIntervalInput")
    def min_receive_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReceiveIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="minTransmitIntervalInput")
    def min_transmit_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minTransmitIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="multiplierInput")
    def multiplier_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multiplierInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionInitializationModeInput")
    def session_initialization_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionInitializationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="minReceiveInterval")
    def min_receive_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReceiveInterval"))

    @min_receive_interval.setter
    def min_receive_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e22017362ea4e9e716a3b50743dca2d8ebd7a2543a6a0fd267ff8cf696e15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReceiveInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTransmitInterval")
    def min_transmit_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minTransmitInterval"))

    @min_transmit_interval.setter
    def min_transmit_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fa8826396726c4b1fbc97ad98a9643ed89ae879f3fb40f5016952d7a0e59b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTransmitInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiplier")
    def multiplier(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiplier"))

    @multiplier.setter
    def multiplier(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807b521f97e45ef8596631866739e1cd7c9e17943e63dbb22108930df134cb51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiplier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionInitializationMode")
    def session_initialization_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionInitializationMode"))

    @session_initialization_mode.setter
    def session_initialization_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a9d07284a991e211c5c321488d2010a134245c70c09a538671c193defe735d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionInitializationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouterPeerBfd]:
        return typing.cast(typing.Optional[ComputeRouterPeerBfd], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeRouterPeerBfd]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f2241354c6fada3a1cc1389959f44c7c6780ec519f0b0f5bc77f0492b7ca5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "interface": "interface",
        "name": "name",
        "peer_asn": "peerAsn",
        "router": "router",
        "advertised_groups": "advertisedGroups",
        "advertised_ip_ranges": "advertisedIpRanges",
        "advertised_route_priority": "advertisedRoutePriority",
        "advertise_mode": "advertiseMode",
        "bfd": "bfd",
        "custom_learned_ip_ranges": "customLearnedIpRanges",
        "custom_learned_route_priority": "customLearnedRoutePriority",
        "enable": "enable",
        "enable_ipv4": "enableIpv4",
        "enable_ipv6": "enableIpv6",
        "export_policies": "exportPolicies",
        "id": "id",
        "import_policies": "importPolicies",
        "ip_address": "ipAddress",
        "ipv4_nexthop_address": "ipv4NexthopAddress",
        "ipv6_nexthop_address": "ipv6NexthopAddress",
        "md5_authentication_key": "md5AuthenticationKey",
        "peer_ip_address": "peerIpAddress",
        "peer_ipv4_nexthop_address": "peerIpv4NexthopAddress",
        "peer_ipv6_nexthop_address": "peerIpv6NexthopAddress",
        "project": "project",
        "region": "region",
        "router_appliance_instance": "routerApplianceInstance",
        "timeouts": "timeouts",
        "zero_advertised_route_priority": "zeroAdvertisedRoutePriority",
        "zero_custom_learned_route_priority": "zeroCustomLearnedRoutePriority",
    },
)
class ComputeRouterPeerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        interface: builtins.str,
        name: builtins.str,
        peer_asn: jsii.Number,
        router: builtins.str,
        advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
        advertised_route_priority: typing.Optional[jsii.Number] = None,
        advertise_mode: typing.Optional[builtins.str] = None,
        bfd: typing.Optional[typing.Union[ComputeRouterPeerBfd, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_learned_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterPeerCustomLearnedIpRanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_learned_route_priority: typing.Optional[jsii.Number] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        export_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        import_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ipv4_nexthop_address: typing.Optional[builtins.str] = None,
        ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        md5_authentication_key: typing.Optional[typing.Union["ComputeRouterPeerMd5AuthenticationKey", typing.Dict[builtins.str, typing.Any]]] = None,
        peer_ip_address: typing.Optional[builtins.str] = None,
        peer_ipv4_nexthop_address: typing.Optional[builtins.str] = None,
        peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        router_appliance_instance: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouterPeerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zero_advertised_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_custom_learned_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param interface: Name of the interface the BGP peer is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#interface ComputeRouterPeer#interface}
        :param name: Name of this BGP peer. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#name ComputeRouterPeer#name}
        :param peer_asn: Peer BGP Autonomous System Number (ASN). Each BGP interface may use a different value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_asn ComputeRouterPeer#peer_asn}
        :param router: The name of the Cloud Router in which this BgpPeer will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#router ComputeRouterPeer#router}
        :param advertised_groups: User-specified list of prefix groups to advertise in custom mode, which currently supports the following option:. - 'ALL_SUBNETS': Advertises all of the router's own VPC subnets. This excludes any routes learned for subnets that use VPC Network Peering. Note that this field can only be populated if advertiseMode is 'CUSTOM' and overrides the list defined for the router (in the "bgp" message). These groups are advertised in addition to any specified prefixes. Leave this field blank to advertise no custom groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_groups ComputeRouterPeer#advertised_groups}
        :param advertised_ip_ranges: advertised_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_ip_ranges ComputeRouterPeer#advertised_ip_ranges}
        :param advertised_route_priority: The priority of routes advertised to this BGP peer. Where there is more than one matching route of maximum length, the routes with the lowest priority value win. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_route_priority ComputeRouterPeer#advertised_route_priority}
        :param advertise_mode: User-specified flag to indicate which mode to use for advertisement. Valid values of this enum field are: 'DEFAULT', 'CUSTOM' Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertise_mode ComputeRouterPeer#advertise_mode}
        :param bfd: bfd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#bfd ComputeRouterPeer#bfd}
        :param custom_learned_ip_ranges: custom_learned_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#custom_learned_ip_ranges ComputeRouterPeer#custom_learned_ip_ranges}
        :param custom_learned_route_priority: The user-defined custom learned route priority for a BGP session. This value is applied to all custom learned route ranges for the session. You can choose a value from 0 to 65335. If you don't provide a value, Google Cloud assigns a priority of 100 to the ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#custom_learned_route_priority ComputeRouterPeer#custom_learned_route_priority}
        :param enable: The status of the BGP peer connection. If set to false, any active session with the peer is terminated and all associated routing information is removed. If set to true, the peer connection can be established with routing information. The default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable ComputeRouterPeer#enable}
        :param enable_ipv4: Enable IPv4 traffic over BGP Peer. It is enabled by default if the peerIpAddress is version 4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable_ipv4 ComputeRouterPeer#enable_ipv4}
        :param enable_ipv6: Enable IPv6 traffic over BGP Peer. If not specified, it is disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable_ipv6 ComputeRouterPeer#enable_ipv6}
        :param export_policies: routers.list of export policies applied to this peer, in the order they must be evaluated. The name must correspond to an existing policy that has ROUTE_POLICY_TYPE_EXPORT type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#export_policies ComputeRouterPeer#export_policies}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#id ComputeRouterPeer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_policies: routers.list of import policies applied to this peer, in the order they must be evaluated. The name must correspond to an existing policy that has ROUTE_POLICY_TYPE_IMPORT type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#import_policies ComputeRouterPeer#import_policies}
        :param ip_address: IP address of the interface inside Google Cloud Platform. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ip_address ComputeRouterPeer#ip_address}
        :param ipv4_nexthop_address: IPv4 address of the interface inside Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ipv4_nexthop_address ComputeRouterPeer#ipv4_nexthop_address}
        :param ipv6_nexthop_address: IPv6 address of the interface inside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ipv6_nexthop_address ComputeRouterPeer#ipv6_nexthop_address}
        :param md5_authentication_key: md5_authentication_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#md5_authentication_key ComputeRouterPeer#md5_authentication_key}
        :param peer_ip_address: IP address of the BGP interface outside Google Cloud Platform. Only IPv4 is supported. Required if 'ip_address' is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ip_address ComputeRouterPeer#peer_ip_address}
        :param peer_ipv4_nexthop_address: IPv4 address of the BGP interface outside Google Cloud Platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ipv4_nexthop_address ComputeRouterPeer#peer_ipv4_nexthop_address}
        :param peer_ipv6_nexthop_address: IPv6 address of the BGP interface outside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ipv6_nexthop_address ComputeRouterPeer#peer_ipv6_nexthop_address}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#project ComputeRouterPeer#project}.
        :param region: Region where the router and BgpPeer reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#region ComputeRouterPeer#region}
        :param router_appliance_instance: The URI of the VM instance that is used as third-party router appliances such as Next Gen Firewalls, Virtual Routers, or Router Appliances. The VM instance must be located in zones contained in the same region as this Cloud Router. The VM instance is the peer side of the BGP session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#router_appliance_instance ComputeRouterPeer#router_appliance_instance}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#timeouts ComputeRouterPeer#timeouts}
        :param zero_advertised_route_priority: Force the advertised_route_priority to be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#zero_advertised_route_priority ComputeRouterPeer#zero_advertised_route_priority}
        :param zero_custom_learned_route_priority: Force the custom_learned_route_priority to be 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#zero_custom_learned_route_priority ComputeRouterPeer#zero_custom_learned_route_priority}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bfd, dict):
            bfd = ComputeRouterPeerBfd(**bfd)
        if isinstance(md5_authentication_key, dict):
            md5_authentication_key = ComputeRouterPeerMd5AuthenticationKey(**md5_authentication_key)
        if isinstance(timeouts, dict):
            timeouts = ComputeRouterPeerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b4c898e240899a3645de16178f921d31d29728f6594a09497b32e84bafab6b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peer_asn", value=peer_asn, expected_type=type_hints["peer_asn"])
            check_type(argname="argument router", value=router, expected_type=type_hints["router"])
            check_type(argname="argument advertised_groups", value=advertised_groups, expected_type=type_hints["advertised_groups"])
            check_type(argname="argument advertised_ip_ranges", value=advertised_ip_ranges, expected_type=type_hints["advertised_ip_ranges"])
            check_type(argname="argument advertised_route_priority", value=advertised_route_priority, expected_type=type_hints["advertised_route_priority"])
            check_type(argname="argument advertise_mode", value=advertise_mode, expected_type=type_hints["advertise_mode"])
            check_type(argname="argument bfd", value=bfd, expected_type=type_hints["bfd"])
            check_type(argname="argument custom_learned_ip_ranges", value=custom_learned_ip_ranges, expected_type=type_hints["custom_learned_ip_ranges"])
            check_type(argname="argument custom_learned_route_priority", value=custom_learned_route_priority, expected_type=type_hints["custom_learned_route_priority"])
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument enable_ipv4", value=enable_ipv4, expected_type=type_hints["enable_ipv4"])
            check_type(argname="argument enable_ipv6", value=enable_ipv6, expected_type=type_hints["enable_ipv6"])
            check_type(argname="argument export_policies", value=export_policies, expected_type=type_hints["export_policies"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_policies", value=import_policies, expected_type=type_hints["import_policies"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ipv4_nexthop_address", value=ipv4_nexthop_address, expected_type=type_hints["ipv4_nexthop_address"])
            check_type(argname="argument ipv6_nexthop_address", value=ipv6_nexthop_address, expected_type=type_hints["ipv6_nexthop_address"])
            check_type(argname="argument md5_authentication_key", value=md5_authentication_key, expected_type=type_hints["md5_authentication_key"])
            check_type(argname="argument peer_ip_address", value=peer_ip_address, expected_type=type_hints["peer_ip_address"])
            check_type(argname="argument peer_ipv4_nexthop_address", value=peer_ipv4_nexthop_address, expected_type=type_hints["peer_ipv4_nexthop_address"])
            check_type(argname="argument peer_ipv6_nexthop_address", value=peer_ipv6_nexthop_address, expected_type=type_hints["peer_ipv6_nexthop_address"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument router_appliance_instance", value=router_appliance_instance, expected_type=type_hints["router_appliance_instance"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zero_advertised_route_priority", value=zero_advertised_route_priority, expected_type=type_hints["zero_advertised_route_priority"])
            check_type(argname="argument zero_custom_learned_route_priority", value=zero_custom_learned_route_priority, expected_type=type_hints["zero_custom_learned_route_priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface": interface,
            "name": name,
            "peer_asn": peer_asn,
            "router": router,
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
        if advertised_groups is not None:
            self._values["advertised_groups"] = advertised_groups
        if advertised_ip_ranges is not None:
            self._values["advertised_ip_ranges"] = advertised_ip_ranges
        if advertised_route_priority is not None:
            self._values["advertised_route_priority"] = advertised_route_priority
        if advertise_mode is not None:
            self._values["advertise_mode"] = advertise_mode
        if bfd is not None:
            self._values["bfd"] = bfd
        if custom_learned_ip_ranges is not None:
            self._values["custom_learned_ip_ranges"] = custom_learned_ip_ranges
        if custom_learned_route_priority is not None:
            self._values["custom_learned_route_priority"] = custom_learned_route_priority
        if enable is not None:
            self._values["enable"] = enable
        if enable_ipv4 is not None:
            self._values["enable_ipv4"] = enable_ipv4
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if export_policies is not None:
            self._values["export_policies"] = export_policies
        if id is not None:
            self._values["id"] = id
        if import_policies is not None:
            self._values["import_policies"] = import_policies
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if ipv4_nexthop_address is not None:
            self._values["ipv4_nexthop_address"] = ipv4_nexthop_address
        if ipv6_nexthop_address is not None:
            self._values["ipv6_nexthop_address"] = ipv6_nexthop_address
        if md5_authentication_key is not None:
            self._values["md5_authentication_key"] = md5_authentication_key
        if peer_ip_address is not None:
            self._values["peer_ip_address"] = peer_ip_address
        if peer_ipv4_nexthop_address is not None:
            self._values["peer_ipv4_nexthop_address"] = peer_ipv4_nexthop_address
        if peer_ipv6_nexthop_address is not None:
            self._values["peer_ipv6_nexthop_address"] = peer_ipv6_nexthop_address
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if router_appliance_instance is not None:
            self._values["router_appliance_instance"] = router_appliance_instance
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zero_advertised_route_priority is not None:
            self._values["zero_advertised_route_priority"] = zero_advertised_route_priority
        if zero_custom_learned_route_priority is not None:
            self._values["zero_custom_learned_route_priority"] = zero_custom_learned_route_priority

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
    def interface(self) -> builtins.str:
        '''Name of the interface the BGP peer is associated with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#interface ComputeRouterPeer#interface}
        '''
        result = self._values.get("interface")
        assert result is not None, "Required property 'interface' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of this BGP peer.

        The name must be 1-63 characters long,
        and comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which
        means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#name ComputeRouterPeer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_asn(self) -> jsii.Number:
        '''Peer BGP Autonomous System Number (ASN). Each BGP interface may use a different value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_asn ComputeRouterPeer#peer_asn}
        '''
        result = self._values.get("peer_asn")
        assert result is not None, "Required property 'peer_asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def router(self) -> builtins.str:
        '''The name of the Cloud Router in which this BgpPeer will be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#router ComputeRouterPeer#router}
        '''
        result = self._values.get("router")
        assert result is not None, "Required property 'router' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advertised_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''User-specified list of prefix groups to advertise in custom mode, which currently supports the following option:.

        - 'ALL_SUBNETS': Advertises all of the router's own VPC subnets.
          This excludes any routes learned for subnets that use VPC Network
          Peering.

        Note that this field can only be populated if advertiseMode is 'CUSTOM'
        and overrides the list defined for the router (in the "bgp" message).
        These groups are advertised in addition to any specified prefixes.
        Leave this field blank to advertise no custom groups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_groups ComputeRouterPeer#advertised_groups}
        '''
        result = self._values.get("advertised_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def advertised_ip_ranges(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerAdvertisedIpRanges]]]:
        '''advertised_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_ip_ranges ComputeRouterPeer#advertised_ip_ranges}
        '''
        result = self._values.get("advertised_ip_ranges")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerAdvertisedIpRanges]]], result)

    @builtins.property
    def advertised_route_priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of routes advertised to this BGP peer.

        Where there is more than one matching route of maximum
        length, the routes with the lowest priority value win.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertised_route_priority ComputeRouterPeer#advertised_route_priority}
        '''
        result = self._values.get("advertised_route_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def advertise_mode(self) -> typing.Optional[builtins.str]:
        '''User-specified flag to indicate which mode to use for advertisement.

        Valid values of this enum field are: 'DEFAULT', 'CUSTOM' Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#advertise_mode ComputeRouterPeer#advertise_mode}
        '''
        result = self._values.get("advertise_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bfd(self) -> typing.Optional[ComputeRouterPeerBfd]:
        '''bfd block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#bfd ComputeRouterPeer#bfd}
        '''
        result = self._values.get("bfd")
        return typing.cast(typing.Optional[ComputeRouterPeerBfd], result)

    @builtins.property
    def custom_learned_ip_ranges(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterPeerCustomLearnedIpRanges"]]]:
        '''custom_learned_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#custom_learned_ip_ranges ComputeRouterPeer#custom_learned_ip_ranges}
        '''
        result = self._values.get("custom_learned_ip_ranges")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterPeerCustomLearnedIpRanges"]]], result)

    @builtins.property
    def custom_learned_route_priority(self) -> typing.Optional[jsii.Number]:
        '''The user-defined custom learned route priority for a BGP session.

        This value is applied to all custom learned route ranges for the session. You can choose a value
        from 0 to 65335. If you don't provide a value, Google Cloud assigns a priority of 100 to the ranges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#custom_learned_route_priority ComputeRouterPeer#custom_learned_route_priority}
        '''
        result = self._values.get("custom_learned_route_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The status of the BGP peer connection.

        If set to false, any active session
        with the peer is terminated and all associated routing information is removed.
        If set to true, the peer connection can be established with routing information.
        The default is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable ComputeRouterPeer#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ipv4(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable IPv4 traffic over BGP Peer. It is enabled by default if the peerIpAddress is version 4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable_ipv4 ComputeRouterPeer#enable_ipv4}
        '''
        result = self._values.get("enable_ipv4")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ipv6(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable IPv6 traffic over BGP Peer. If not specified, it is disabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#enable_ipv6 ComputeRouterPeer#enable_ipv6}
        '''
        result = self._values.get("enable_ipv6")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def export_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''routers.list of export policies applied to this peer, in the order they must be evaluated.  The name must correspond to an existing policy that has ROUTE_POLICY_TYPE_EXPORT type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#export_policies ComputeRouterPeer#export_policies}
        '''
        result = self._values.get("export_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#id ComputeRouterPeer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''routers.list of import policies applied to this peer, in the order they must be evaluated.  The name must correspond to an existing policy that has ROUTE_POLICY_TYPE_IMPORT type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#import_policies ComputeRouterPeer#import_policies}
        '''
        result = self._values.get("import_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''IP address of the interface inside Google Cloud Platform. Only IPv4 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ip_address ComputeRouterPeer#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_nexthop_address(self) -> typing.Optional[builtins.str]:
        '''IPv4 address of the interface inside Google Cloud Platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ipv4_nexthop_address ComputeRouterPeer#ipv4_nexthop_address}
        '''
        result = self._values.get("ipv4_nexthop_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_nexthop_address(self) -> typing.Optional[builtins.str]:
        '''IPv6 address of the interface inside Google Cloud Platform.

        The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64.
        If you do not specify the next hop addresses, Google Cloud automatically
        assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#ipv6_nexthop_address ComputeRouterPeer#ipv6_nexthop_address}
        '''
        result = self._values.get("ipv6_nexthop_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def md5_authentication_key(
        self,
    ) -> typing.Optional["ComputeRouterPeerMd5AuthenticationKey"]:
        '''md5_authentication_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#md5_authentication_key ComputeRouterPeer#md5_authentication_key}
        '''
        result = self._values.get("md5_authentication_key")
        return typing.cast(typing.Optional["ComputeRouterPeerMd5AuthenticationKey"], result)

    @builtins.property
    def peer_ip_address(self) -> typing.Optional[builtins.str]:
        '''IP address of the BGP interface outside Google Cloud Platform. Only IPv4 is supported. Required if 'ip_address' is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ip_address ComputeRouterPeer#peer_ip_address}
        '''
        result = self._values.get("peer_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_ipv4_nexthop_address(self) -> typing.Optional[builtins.str]:
        '''IPv4 address of the BGP interface outside Google Cloud Platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ipv4_nexthop_address ComputeRouterPeer#peer_ipv4_nexthop_address}
        '''
        result = self._values.get("peer_ipv4_nexthop_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_ipv6_nexthop_address(self) -> typing.Optional[builtins.str]:
        '''IPv6 address of the BGP interface outside Google Cloud Platform.

        The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64.
        If you do not specify the next hop addresses, Google Cloud automatically
        assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#peer_ipv6_nexthop_address ComputeRouterPeer#peer_ipv6_nexthop_address}
        '''
        result = self._values.get("peer_ipv6_nexthop_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#project ComputeRouterPeer#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the router and BgpPeer reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#region ComputeRouterPeer#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_appliance_instance(self) -> typing.Optional[builtins.str]:
        '''The URI of the VM instance that is used as third-party router appliances such as Next Gen Firewalls, Virtual Routers, or Router Appliances.

        The VM instance must be located in zones contained in the same region as
        this Cloud Router. The VM instance is the peer side of the BGP session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#router_appliance_instance ComputeRouterPeer#router_appliance_instance}
        '''
        result = self._values.get("router_appliance_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRouterPeerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#timeouts ComputeRouterPeer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRouterPeerTimeouts"], result)

    @builtins.property
    def zero_advertised_route_priority(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force the advertised_route_priority to be 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#zero_advertised_route_priority ComputeRouterPeer#zero_advertised_route_priority}
        '''
        result = self._values.get("zero_advertised_route_priority")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zero_custom_learned_route_priority(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force the custom_learned_route_priority to be 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#zero_custom_learned_route_priority ComputeRouterPeer#zero_custom_learned_route_priority}
        '''
        result = self._values.get("zero_custom_learned_route_priority")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterPeerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerCustomLearnedIpRanges",
    jsii_struct_bases=[],
    name_mapping={"range": "range"},
)
class ComputeRouterPeerCustomLearnedIpRanges:
    def __init__(self, *, range: builtins.str) -> None:
        '''
        :param range: The IP range to learn. The value must be a CIDR-formatted string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#range ComputeRouterPeer#range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85f6cadd700fe2a37eef022d171adfa4ab642a79e17eb62b370f9e0cb8ad0ab)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
        }

    @builtins.property
    def range(self) -> builtins.str:
        '''The IP range to learn. The value must be a CIDR-formatted string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#range ComputeRouterPeer#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterPeerCustomLearnedIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterPeerCustomLearnedIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerCustomLearnedIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8ba69f65a0ead3044e689b1b92cdc5eaf07c401208fbebb83510fc3a76dc4fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRouterPeerCustomLearnedIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299df5c34216f75ed3b00339fc62f9c63131c5181a1e68ea4a97bff40886aa4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouterPeerCustomLearnedIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddc235646f497a38627765f31cea16b0e337f8c4c499387f8edc3c91e6c727a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeb389784b069e3bf0c23088042b1585c16ed8a2c483c450c2faffa80a0d05de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6f957485fd6486798a6376d950d8f4ef0a05e7d118363e6dc50c68bfa5512b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerCustomLearnedIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerCustomLearnedIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerCustomLearnedIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d301d027e001dcdabca1524755222029abd2023463b6035a5551c98660307b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterPeerCustomLearnedIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerCustomLearnedIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e501b52255e54fcc9a37de1773fafcf8de3c602ccc07bbaf0f92e139efa9b8df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "range"))

    @range.setter
    def range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d09f45e8da88538fb7847f52cc344a853f8adaf63a3d87fa78872242509837d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "range", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerCustomLearnedIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerCustomLearnedIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerCustomLearnedIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17399d7897cbb23ca92423ccad29f5b6d0d273c179182bf54f1ea7181a04c7f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerMd5AuthenticationKey",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name"},
)
class ComputeRouterPeerMd5AuthenticationKey:
    def __init__(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: Value of the key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#key ComputeRouterPeer#key}
        :param name: [REQUIRED] Name used to identify the key. Must be unique within a router. Must be referenced by exactly one bgpPeer. Must comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#name ComputeRouterPeer#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec17d00c4fa0d6a1df8233992f3cac25c59effbcb6c9a9ce1e59d7f61d5f5e7)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "name": name,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Value of the key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#key ComputeRouterPeer#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''[REQUIRED] Name used to identify the key.

        Must be unique within a router. Must be referenced by exactly one bgpPeer. Must comply with RFC1035.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#name ComputeRouterPeer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterPeerMd5AuthenticationKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterPeerMd5AuthenticationKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerMd5AuthenticationKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3152d6312fe5ec160a6bfd720324493ebe31785e462f45eafea38ceaf5d2f986)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ebdf1ca5bf50627199b21698e8a9d960e82f35fb4bc9cf9396874ca701253c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37739ecc5985767f93ee11a3078a26f24be6bddca6301e4ac65fb2f6a16d7ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouterPeerMd5AuthenticationKey]:
        return typing.cast(typing.Optional[ComputeRouterPeerMd5AuthenticationKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRouterPeerMd5AuthenticationKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ea3ccb082dbb024995112c776e5407f6a250ab37077af460de31aacb2dd88a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRouterPeerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#create ComputeRouterPeer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#delete ComputeRouterPeer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#update ComputeRouterPeer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5999d1619705b0b7ac6e84b850269834b08dab7c9f11190e143bce8b4f83a9cc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#create ComputeRouterPeer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#delete ComputeRouterPeer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_peer#update ComputeRouterPeer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterPeerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterPeerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterPeer.ComputeRouterPeerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33d411c3a903352dcf71e207bf5234402aeb80536433fff0b474f1462e2a8d3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24c5ada3db134b456f54a6dc5b615b55ff48dc601b440d9976aa6c4f37c13f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797a704988e5848f70ecb9d443615e7b37cca666cdec300a769a579e8ec65950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c67ada5d07b3f48212c514a0b5be9c92bc7925f85c09eca56874ac4e53e44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2614fdda17f7c2846ba65a208e9b6d025a7b215100e46c003020d33440d2f39b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRouterPeer",
    "ComputeRouterPeerAdvertisedIpRanges",
    "ComputeRouterPeerAdvertisedIpRangesList",
    "ComputeRouterPeerAdvertisedIpRangesOutputReference",
    "ComputeRouterPeerBfd",
    "ComputeRouterPeerBfdOutputReference",
    "ComputeRouterPeerConfig",
    "ComputeRouterPeerCustomLearnedIpRanges",
    "ComputeRouterPeerCustomLearnedIpRangesList",
    "ComputeRouterPeerCustomLearnedIpRangesOutputReference",
    "ComputeRouterPeerMd5AuthenticationKey",
    "ComputeRouterPeerMd5AuthenticationKeyOutputReference",
    "ComputeRouterPeerTimeouts",
    "ComputeRouterPeerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__42db39c65d77c39d57a1e757fba207ea507a585b22ecb04dc52326bd3f288b90(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    interface: builtins.str,
    name: builtins.str,
    peer_asn: jsii.Number,
    router: builtins.str,
    advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    advertised_route_priority: typing.Optional[jsii.Number] = None,
    advertise_mode: typing.Optional[builtins.str] = None,
    bfd: typing.Optional[typing.Union[ComputeRouterPeerBfd, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_learned_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterPeerCustomLearnedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_learned_route_priority: typing.Optional[jsii.Number] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    export_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    import_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ipv4_nexthop_address: typing.Optional[builtins.str] = None,
    ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    md5_authentication_key: typing.Optional[typing.Union[ComputeRouterPeerMd5AuthenticationKey, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_ip_address: typing.Optional[builtins.str] = None,
    peer_ipv4_nexthop_address: typing.Optional[builtins.str] = None,
    peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    router_appliance_instance: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouterPeerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zero_advertised_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zero_custom_learned_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__d88a692d9c6351097aed055767060f262aec1cbcef50edfa046a00b66837ac77(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687b08699f1f8a9087ff13e0b297045942774b80f8c9431ceeb4cea261a48faf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9361ee095a98d8f5eb2cb1a0261a17afdd308bd2ee1f5a3307004c01afb5192(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterPeerCustomLearnedIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0515e14e0357ef24c2573a77fdc038e59f92b1bab80a2d3f5e59464cdf774b18(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fad905773bf8a255fe2c1b0443c17b14ef53899cf8b3cf3f54ccb57a7c42140(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a79e40a5a45bd43bcf7e43eafb383e42ee2971aa5faa96e8dd71e115850da60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00c64341595645a0833edde1b460990314be1c1b3baaa789b8c1cd1f5860473(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52eb5988236a35be86a83851a033eab4031a1f84cd4b490b5b79e8a9d7552858(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7bbb08815f80f6cde456a8fdf0b06fa5d60236b8a159e54631c78d5e35046a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9b229d6f74ee416335bbe68b933aee08a957927368d4582040148dfac0a9f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e08ed1a5657452edbfc7e456f1eeedfe20ac00cf53a7425bc4f7bd2b103eb76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a97e557a1a38e5a3f54a7301b8dc145cf96fe937b46c9785ee535045f71f9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bed6698e1ac24db53b85ae9e20193d6fb2cf2c3ebbe01ab37cfef17731b3266(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c9fcc768f9b7f607e2817e330666df84bee3bc3820115e0ed1f800e36e7e6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134764f8baece5d8374d8aaa4bbc1646b0902216a392f65d1c60cd7fd464f5e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa93bbffa91f88b57eaa25ea2dad922460858c79ee7997c2069855f81434b57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbdde41ad8f24bca30c69665d405eccb02bfa8aac4757c184059294fa6c4543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924cf4987d952b4a9ddeeb257ab628c317761ab0c3368ad0f4c6a06b215dacbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edaad33cd7d6406f19a2c905ebbc293c8424c1b12eddcfb45af0cbc13fcad8d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7105c10949de353d522b33a13b36fc8bb721539afe25453a3de6b6cc39845bcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e08c6d2ad8d7de7e385622552f2a96d0a8098897af9e8bddd45e9957ec304d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854dd1cd5ceb1b26c93849f73937201ddfd5d81d85591c3c3e296dcf480ec0f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4459c49dd20a47670f6453fae920a3b74ff816a7ab67ff365ce86400c3a7a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee27b12375f8c5ad7c4aa2273a862e8e1b640a49f2bf5154c014d6e06e8201df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29766f20543accd7aaa1b410b314e2e9f05b2a5deccb889059d3126d99bf2e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d4fbbd327c7c302d7bc0f861340eb35d14a40a099e08b394de62e8d457493a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b6465ca903935486b06ac7b39e342d3b23b896a1ef6f03c3116010d0d90dcc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c268a0ec045f31d1b210d900f17cda4bbd73c46d47cccc39133cda11f2fdfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9eeb820686c63c226d2cd0c1d3ddd5b66aebbbfb834b9a00f3b37df44e2fea(
    *,
    range: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5e4e60c04c28cf69d7b8532669a55ac40e0d38c0f18328375ce73591c74c00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f735e4a4527e85afb802f46ff6f3ccf998d8f5cce16b4c8dc681a6eb4029c09a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be486e537c0ec4a618caca313269fc4fc5cfdd56a36083f74f8022fb4d03dc56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31039921f2dfbc7c91b3b6899669f4aa9fdf9e2397aca9eacde5c1e954592672(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a91a77a27b7c63f426b93a60e80218dd36b9c4df7db8b08a92e7912b04025d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29ad310af8c45f7d204e903e380325868d319b6b1114407c5f717850c6ca6eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerAdvertisedIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95befba4df0b08f7c5a836185161fefde0a887560ab048b7cb317cb13788696f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6be5323dfbda0aa8455a8990aa3aabc7f396133fc839819b9d33486d89b182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d2b02827ea696a0885758c25f55d6f17be8dad31e251d91776018b368c910c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9bd5e277a85f5aece0edce93eec482f79fce801b361258cff1d92ee8070adb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerAdvertisedIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33561511d54c50aaa29e0592ccc2884bd4438f468333506f19eea932a0fe7ddf(
    *,
    session_initialization_mode: builtins.str,
    min_receive_interval: typing.Optional[jsii.Number] = None,
    min_transmit_interval: typing.Optional[jsii.Number] = None,
    multiplier: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa6ad26883a06146d781dc0b56565f963228922e260df133a7d1fbb55ec7c08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e22017362ea4e9e716a3b50743dca2d8ebd7a2543a6a0fd267ff8cf696e15f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fa8826396726c4b1fbc97ad98a9643ed89ae879f3fb40f5016952d7a0e59b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807b521f97e45ef8596631866739e1cd7c9e17943e63dbb22108930df134cb51(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a9d07284a991e211c5c321488d2010a134245c70c09a538671c193defe735d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f2241354c6fada3a1cc1389959f44c7c6780ec519f0b0f5bc77f0492b7ca5b(
    value: typing.Optional[ComputeRouterPeerBfd],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b4c898e240899a3645de16178f921d31d29728f6594a09497b32e84bafab6b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interface: builtins.str,
    name: builtins.str,
    peer_asn: jsii.Number,
    router: builtins.str,
    advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    advertised_route_priority: typing.Optional[jsii.Number] = None,
    advertise_mode: typing.Optional[builtins.str] = None,
    bfd: typing.Optional[typing.Union[ComputeRouterPeerBfd, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_learned_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterPeerCustomLearnedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_learned_route_priority: typing.Optional[jsii.Number] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    export_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    import_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ipv4_nexthop_address: typing.Optional[builtins.str] = None,
    ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    md5_authentication_key: typing.Optional[typing.Union[ComputeRouterPeerMd5AuthenticationKey, typing.Dict[builtins.str, typing.Any]]] = None,
    peer_ip_address: typing.Optional[builtins.str] = None,
    peer_ipv4_nexthop_address: typing.Optional[builtins.str] = None,
    peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    router_appliance_instance: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouterPeerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zero_advertised_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zero_custom_learned_route_priority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85f6cadd700fe2a37eef022d171adfa4ab642a79e17eb62b370f9e0cb8ad0ab(
    *,
    range: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ba69f65a0ead3044e689b1b92cdc5eaf07c401208fbebb83510fc3a76dc4fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299df5c34216f75ed3b00339fc62f9c63131c5181a1e68ea4a97bff40886aa4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddc235646f497a38627765f31cea16b0e337f8c4c499387f8edc3c91e6c727a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb389784b069e3bf0c23088042b1585c16ed8a2c483c450c2faffa80a0d05de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f957485fd6486798a6376d950d8f4ef0a05e7d118363e6dc50c68bfa5512b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d301d027e001dcdabca1524755222029abd2023463b6035a5551c98660307b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterPeerCustomLearnedIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e501b52255e54fcc9a37de1773fafcf8de3c602ccc07bbaf0f92e139efa9b8df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d09f45e8da88538fb7847f52cc344a853f8adaf63a3d87fa78872242509837d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17399d7897cbb23ca92423ccad29f5b6d0d273c179182bf54f1ea7181a04c7f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerCustomLearnedIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec17d00c4fa0d6a1df8233992f3cac25c59effbcb6c9a9ce1e59d7f61d5f5e7(
    *,
    key: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3152d6312fe5ec160a6bfd720324493ebe31785e462f45eafea38ceaf5d2f986(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ebdf1ca5bf50627199b21698e8a9d960e82f35fb4bc9cf9396874ca701253c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37739ecc5985767f93ee11a3078a26f24be6bddca6301e4ac65fb2f6a16d7ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ea3ccb082dbb024995112c776e5407f6a250ab37077af460de31aacb2dd88a(
    value: typing.Optional[ComputeRouterPeerMd5AuthenticationKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5999d1619705b0b7ac6e84b850269834b08dab7c9f11190e143bce8b4f83a9cc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d411c3a903352dcf71e207bf5234402aeb80536433fff0b474f1462e2a8d3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c5ada3db134b456f54a6dc5b615b55ff48dc601b440d9976aa6c4f37c13f4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797a704988e5848f70ecb9d443615e7b37cca666cdec300a769a579e8ec65950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c67ada5d07b3f48212c514a0b5be9c92bc7925f85c09eca56874ac4e53e44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2614fdda17f7c2846ba65a208e9b6d025a7b215100e46c003020d33440d2f39b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterPeerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
