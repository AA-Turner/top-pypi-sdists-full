""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/bgp
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class BgpNeighborConditionaladvertiseItem(TypedDict, total=False):
    """Nested item for neighbor.conditional-advertise field."""
    advertise_routemap: str
    condition_routemap: str | list[str]
    condition_type: Literal["exist", "non-exist"]


class BgpNeighborConditionaladvertise6Item(TypedDict, total=False):
    """Nested item for neighbor.conditional-advertise6 field."""
    advertise_routemap: str
    condition_routemap: str | list[str]
    condition_type: Literal["exist", "non-exist"]


class BgpVrfExportrtItem(TypedDict, total=False):
    """Nested item for vrf.export-rt field."""
    route_target: str


class BgpVrfImportrtItem(TypedDict, total=False):
    """Nested item for vrf.import-rt field."""
    route_target: str


class BgpVrfLeaktargetItem(TypedDict, total=False):
    """Nested item for vrf.leak-target field."""
    vrf: str
    route_map: str
    interface: str


class BgpVrf6ExportrtItem(TypedDict, total=False):
    """Nested item for vrf6.export-rt field."""
    route_target: str


class BgpVrf6ImportrtItem(TypedDict, total=False):
    """Nested item for vrf6.import-rt field."""
    route_target: str


class BgpVrf6LeaktargetItem(TypedDict, total=False):
    """Nested item for vrf6.leak-target field."""
    vrf: str
    route_map: str
    interface: str


class BgpConfederationpeersItem(TypedDict, total=False):
    """Nested item for confederation-peers field."""
    peer: str


class BgpAggregateaddressItem(TypedDict, total=False):
    """Nested item for aggregate-address field."""
    id: int
    prefix: str
    as_set: Literal["enable", "disable"]
    summary_only: Literal["enable", "disable"]


class BgpAggregateaddress6Item(TypedDict, total=False):
    """Nested item for aggregate-address6 field."""
    id: int
    prefix6: str
    as_set: Literal["enable", "disable"]
    summary_only: Literal["enable", "disable"]


class BgpNeighborItem(TypedDict, total=False):
    """Nested item for neighbor field."""
    ip: str
    advertisement_interval: int
    allowas_in_enable: Literal["enable", "disable"]
    allowas_in_enable6: Literal["enable", "disable"]
    allowas_in_enable_vpnv4: Literal["enable", "disable"]
    allowas_in_enable_vpnv6: Literal["enable", "disable"]
    allowas_in_enable_evpn: Literal["enable", "disable"]
    allowas_in: int
    allowas_in6: int
    allowas_in_vpnv4: int
    allowas_in_vpnv6: int
    allowas_in_evpn: int
    attribute_unchanged: Literal["as-path", "med", "next-hop"]
    attribute_unchanged6: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv4: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv6: Literal["as-path", "med", "next-hop"]
    activate: Literal["enable", "disable"]
    activate6: Literal["enable", "disable"]
    activate_vpnv4: Literal["enable", "disable"]
    activate_vpnv6: Literal["enable", "disable"]
    activate_evpn: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]
    capability_dynamic: Literal["enable", "disable"]
    capability_orf: Literal["none", "receive", "send", "both"]
    capability_orf6: Literal["none", "receive", "send", "both"]
    capability_graceful_restart: Literal["enable", "disable"]
    capability_graceful_restart6: Literal["enable", "disable"]
    capability_graceful_restart_vpnv4: Literal["enable", "disable"]
    capability_graceful_restart_vpnv6: Literal["enable", "disable"]
    capability_graceful_restart_evpn: Literal["enable", "disable"]
    capability_route_refresh: Literal["enable", "disable"]
    capability_default_originate: Literal["enable", "disable"]
    capability_default_originate6: Literal["enable", "disable"]
    dont_capability_negotiate: Literal["enable", "disable"]
    ebgp_enforce_multihop: Literal["enable", "disable"]
    link_down_failover: Literal["enable", "disable"]
    stale_route: Literal["enable", "disable"]
    next_hop_self: Literal["enable", "disable"]
    next_hop_self6: Literal["enable", "disable"]
    next_hop_self_rr: Literal["enable", "disable"]
    next_hop_self_rr6: Literal["enable", "disable"]
    next_hop_self_vpnv4: Literal["enable", "disable"]
    next_hop_self_vpnv6: Literal["enable", "disable"]
    override_capability: Literal["enable", "disable"]
    passive: Literal["enable", "disable"]
    remove_private_as: Literal["enable", "disable"]
    remove_private_as6: Literal["enable", "disable"]
    remove_private_as_vpnv4: Literal["enable", "disable"]
    remove_private_as_vpnv6: Literal["enable", "disable"]
    remove_private_as_evpn: Literal["enable", "disable"]
    route_reflector_client: Literal["enable", "disable"]
    route_reflector_client6: Literal["enable", "disable"]
    route_reflector_client_vpnv4: Literal["enable", "disable"]
    route_reflector_client_vpnv6: Literal["enable", "disable"]
    route_reflector_client_evpn: Literal["enable", "disable"]
    route_server_client: Literal["enable", "disable"]
    route_server_client6: Literal["enable", "disable"]
    route_server_client_vpnv4: Literal["enable", "disable"]
    route_server_client_vpnv6: Literal["enable", "disable"]
    route_server_client_evpn: Literal["enable", "disable"]
    rr_attr_allow_change: Literal["enable", "disable"]
    rr_attr_allow_change6: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv4: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv6: Literal["enable", "disable"]
    rr_attr_allow_change_evpn: Literal["enable", "disable"]
    shutdown: Literal["enable", "disable"]
    soft_reconfiguration: Literal["enable", "disable"]
    soft_reconfiguration6: Literal["enable", "disable"]
    soft_reconfiguration_vpnv4: Literal["enable", "disable"]
    soft_reconfiguration_vpnv6: Literal["enable", "disable"]
    soft_reconfiguration_evpn: Literal["enable", "disable"]
    as_override: Literal["enable", "disable"]
    as_override6: Literal["enable", "disable"]
    strict_capability_match: Literal["enable", "disable"]
    default_originate_routemap: str
    default_originate_routemap6: str
    description: str
    distribute_list_in: str
    distribute_list_in6: str
    distribute_list_in_vpnv4: str
    distribute_list_in_vpnv6: str
    distribute_list_out: str
    distribute_list_out6: str
    distribute_list_out_vpnv4: str
    distribute_list_out_vpnv6: str
    ebgp_multihop_ttl: int
    filter_list_in: str
    filter_list_in6: str
    filter_list_in_vpnv4: str
    filter_list_in_vpnv6: str
    filter_list_out: str
    filter_list_out6: str
    filter_list_out_vpnv4: str
    filter_list_out_vpnv6: str
    interface: str
    maximum_prefix: int
    maximum_prefix6: int
    maximum_prefix_vpnv4: int
    maximum_prefix_vpnv6: int
    maximum_prefix_evpn: int
    maximum_prefix_threshold: int
    maximum_prefix_threshold6: int
    maximum_prefix_threshold_vpnv4: int
    maximum_prefix_threshold_vpnv6: int
    maximum_prefix_threshold_evpn: int
    maximum_prefix_warning_only: Literal["enable", "disable"]
    maximum_prefix_warning_only6: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv4: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv6: Literal["enable", "disable"]
    maximum_prefix_warning_only_evpn: Literal["enable", "disable"]
    prefix_list_in: str
    prefix_list_in6: str
    prefix_list_in_vpnv4: str
    prefix_list_in_vpnv6: str
    prefix_list_out: str
    prefix_list_out6: str
    prefix_list_out_vpnv4: str
    prefix_list_out_vpnv6: str
    remote_as: str
    local_as: str
    local_as_no_prepend: Literal["enable", "disable"]
    local_as_replace_as: Literal["enable", "disable"]
    retain_stale_time: int
    route_map_in: str
    route_map_in6: str
    route_map_in_vpnv4: str
    route_map_in_vpnv6: str
    route_map_in_evpn: str
    route_map_out: str
    route_map_out_preferable: str
    route_map_out6: str
    route_map_out6_preferable: str
    route_map_out_vpnv4: str
    route_map_out_vpnv6: str
    route_map_out_vpnv4_preferable: str
    route_map_out_vpnv6_preferable: str
    route_map_out_evpn: str
    send_community: Literal["standard", "extended", "both", "disable"]
    send_community6: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv4: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv6: Literal["standard", "extended", "both", "disable"]
    send_community_evpn: Literal["standard", "extended", "both", "disable"]
    keep_alive_timer: int
    holdtime_timer: int
    connect_timer: int
    unsuppress_map: str
    unsuppress_map6: str
    update_source: str
    weight: int
    restart_time: int
    additional_path: Literal["send", "receive", "both", "disable"]
    additional_path6: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv4: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv6: Literal["send", "receive", "both", "disable"]
    adv_additional_path: int
    adv_additional_path6: int
    adv_additional_path_vpnv4: int
    adv_additional_path_vpnv6: int
    password: str
    auth_options: str
    conditional_advertise: str | list[str] | list[BgpNeighborConditionaladvertiseItem]
    conditional_advertise6: str | list[str] | list[BgpNeighborConditionaladvertise6Item]


class BgpNeighborgroupItem(TypedDict, total=False):
    """Nested item for neighbor-group field."""
    name: str
    advertisement_interval: int
    allowas_in_enable: Literal["enable", "disable"]
    allowas_in_enable6: Literal["enable", "disable"]
    allowas_in_enable_vpnv4: Literal["enable", "disable"]
    allowas_in_enable_vpnv6: Literal["enable", "disable"]
    allowas_in_enable_evpn: Literal["enable", "disable"]
    allowas_in: int
    allowas_in6: int
    allowas_in_vpnv4: int
    allowas_in_vpnv6: int
    allowas_in_evpn: int
    attribute_unchanged: Literal["as-path", "med", "next-hop"]
    attribute_unchanged6: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv4: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv6: Literal["as-path", "med", "next-hop"]
    activate: Literal["enable", "disable"]
    activate6: Literal["enable", "disable"]
    activate_vpnv4: Literal["enable", "disable"]
    activate_vpnv6: Literal["enable", "disable"]
    activate_evpn: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]
    capability_dynamic: Literal["enable", "disable"]
    capability_orf: Literal["none", "receive", "send", "both"]
    capability_orf6: Literal["none", "receive", "send", "both"]
    capability_graceful_restart: Literal["enable", "disable"]
    capability_graceful_restart6: Literal["enable", "disable"]
    capability_graceful_restart_vpnv4: Literal["enable", "disable"]
    capability_graceful_restart_vpnv6: Literal["enable", "disable"]
    capability_graceful_restart_evpn: Literal["enable", "disable"]
    capability_route_refresh: Literal["enable", "disable"]
    capability_default_originate: Literal["enable", "disable"]
    capability_default_originate6: Literal["enable", "disable"]
    dont_capability_negotiate: Literal["enable", "disable"]
    ebgp_enforce_multihop: Literal["enable", "disable"]
    link_down_failover: Literal["enable", "disable"]
    stale_route: Literal["enable", "disable"]
    next_hop_self: Literal["enable", "disable"]
    next_hop_self6: Literal["enable", "disable"]
    next_hop_self_rr: Literal["enable", "disable"]
    next_hop_self_rr6: Literal["enable", "disable"]
    next_hop_self_vpnv4: Literal["enable", "disable"]
    next_hop_self_vpnv6: Literal["enable", "disable"]
    override_capability: Literal["enable", "disable"]
    passive: Literal["enable", "disable"]
    remove_private_as: Literal["enable", "disable"]
    remove_private_as6: Literal["enable", "disable"]
    remove_private_as_vpnv4: Literal["enable", "disable"]
    remove_private_as_vpnv6: Literal["enable", "disable"]
    remove_private_as_evpn: Literal["enable", "disable"]
    route_reflector_client: Literal["enable", "disable"]
    route_reflector_client6: Literal["enable", "disable"]
    route_reflector_client_vpnv4: Literal["enable", "disable"]
    route_reflector_client_vpnv6: Literal["enable", "disable"]
    route_reflector_client_evpn: Literal["enable", "disable"]
    route_server_client: Literal["enable", "disable"]
    route_server_client6: Literal["enable", "disable"]
    route_server_client_vpnv4: Literal["enable", "disable"]
    route_server_client_vpnv6: Literal["enable", "disable"]
    route_server_client_evpn: Literal["enable", "disable"]
    rr_attr_allow_change: Literal["enable", "disable"]
    rr_attr_allow_change6: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv4: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv6: Literal["enable", "disable"]
    rr_attr_allow_change_evpn: Literal["enable", "disable"]
    shutdown: Literal["enable", "disable"]
    soft_reconfiguration: Literal["enable", "disable"]
    soft_reconfiguration6: Literal["enable", "disable"]
    soft_reconfiguration_vpnv4: Literal["enable", "disable"]
    soft_reconfiguration_vpnv6: Literal["enable", "disable"]
    soft_reconfiguration_evpn: Literal["enable", "disable"]
    as_override: Literal["enable", "disable"]
    as_override6: Literal["enable", "disable"]
    strict_capability_match: Literal["enable", "disable"]
    default_originate_routemap: str
    default_originate_routemap6: str
    description: str
    distribute_list_in: str
    distribute_list_in6: str
    distribute_list_in_vpnv4: str
    distribute_list_in_vpnv6: str
    distribute_list_out: str
    distribute_list_out6: str
    distribute_list_out_vpnv4: str
    distribute_list_out_vpnv6: str
    ebgp_multihop_ttl: int
    filter_list_in: str
    filter_list_in6: str
    filter_list_in_vpnv4: str
    filter_list_in_vpnv6: str
    filter_list_out: str
    filter_list_out6: str
    filter_list_out_vpnv4: str
    filter_list_out_vpnv6: str
    interface: str
    maximum_prefix: int
    maximum_prefix6: int
    maximum_prefix_vpnv4: int
    maximum_prefix_vpnv6: int
    maximum_prefix_evpn: int
    maximum_prefix_threshold: int
    maximum_prefix_threshold6: int
    maximum_prefix_threshold_vpnv4: int
    maximum_prefix_threshold_vpnv6: int
    maximum_prefix_threshold_evpn: int
    maximum_prefix_warning_only: Literal["enable", "disable"]
    maximum_prefix_warning_only6: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv4: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv6: Literal["enable", "disable"]
    maximum_prefix_warning_only_evpn: Literal["enable", "disable"]
    prefix_list_in: str
    prefix_list_in6: str
    prefix_list_in_vpnv4: str
    prefix_list_in_vpnv6: str
    prefix_list_out: str
    prefix_list_out6: str
    prefix_list_out_vpnv4: str
    prefix_list_out_vpnv6: str
    remote_as: str
    remote_as_filter: str
    local_as: str
    local_as_no_prepend: Literal["enable", "disable"]
    local_as_replace_as: Literal["enable", "disable"]
    retain_stale_time: int
    route_map_in: str
    route_map_in6: str
    route_map_in_vpnv4: str
    route_map_in_vpnv6: str
    route_map_in_evpn: str
    route_map_out: str
    route_map_out_preferable: str
    route_map_out6: str
    route_map_out6_preferable: str
    route_map_out_vpnv4: str
    route_map_out_vpnv6: str
    route_map_out_vpnv4_preferable: str
    route_map_out_vpnv6_preferable: str
    route_map_out_evpn: str
    send_community: Literal["standard", "extended", "both", "disable"]
    send_community6: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv4: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv6: Literal["standard", "extended", "both", "disable"]
    send_community_evpn: Literal["standard", "extended", "both", "disable"]
    keep_alive_timer: int
    holdtime_timer: int
    connect_timer: int
    unsuppress_map: str
    unsuppress_map6: str
    update_source: str
    weight: int
    restart_time: int
    additional_path: Literal["send", "receive", "both", "disable"]
    additional_path6: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv4: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv6: Literal["send", "receive", "both", "disable"]
    adv_additional_path: int
    adv_additional_path6: int
    adv_additional_path_vpnv4: int
    adv_additional_path_vpnv6: int
    password: str
    auth_options: str


class BgpNeighborrangeItem(TypedDict, total=False):
    """Nested item for neighbor-range field."""
    id: int
    prefix: str
    max_neighbor_num: int
    neighbor_group: str


class BgpNeighborrange6Item(TypedDict, total=False):
    """Nested item for neighbor-range6 field."""
    id: int
    prefix6: str
    max_neighbor_num: int
    neighbor_group: str


class BgpNetworkItem(TypedDict, total=False):
    """Nested item for network field."""
    id: int
    prefix: str
    network_import_check: Literal["global", "enable", "disable"]
    backdoor: Literal["enable", "disable"]
    route_map: str
    prefix_name: str


class BgpNetwork6Item(TypedDict, total=False):
    """Nested item for network6 field."""
    id: int
    prefix6: str
    network_import_check: Literal["global", "enable", "disable"]
    backdoor: Literal["enable", "disable"]
    route_map: str


class BgpRedistributeItem(TypedDict, total=False):
    """Nested item for redistribute field."""
    name: str
    status: Literal["enable", "disable"]
    route_map: str


class BgpRedistribute6Item(TypedDict, total=False):
    """Nested item for redistribute6 field."""
    name: str
    status: Literal["enable", "disable"]
    route_map: str


class BgpAdmindistanceItem(TypedDict, total=False):
    """Nested item for admin-distance field."""
    id: int
    neighbour_prefix: str
    route_list: str
    distance: int


class BgpVrfItem(TypedDict, total=False):
    """Nested item for vrf field."""
    vrf: str
    role: Literal["standalone", "ce", "pe"]
    rd: str
    export_rt: str | list[str] | list[BgpVrfExportrtItem]
    import_rt: str | list[str] | list[BgpVrfImportrtItem]
    import_route_map: str
    leak_target: str | list[str] | list[BgpVrfLeaktargetItem]


class BgpVrf6Item(TypedDict, total=False):
    """Nested item for vrf6 field."""
    vrf: str
    role: Literal["standalone", "ce", "pe"]
    rd: str
    export_rt: str | list[str] | list[BgpVrf6ExportrtItem]
    import_rt: str | list[str] | list[BgpVrf6ImportrtItem]
    import_route_map: str
    leak_target: str | list[str] | list[BgpVrf6LeaktargetItem]


class BgpPayload(TypedDict, total=False):
    """Payload type for Bgp operations."""
    asn: str
    router_id: str
    keepalive_timer: int
    holdtime_timer: int
    always_compare_med: Literal["enable", "disable"]
    bestpath_as_path_ignore: Literal["enable", "disable"]
    bestpath_cmp_confed_aspath: Literal["enable", "disable"]
    bestpath_cmp_routerid: Literal["enable", "disable"]
    bestpath_med_confed: Literal["enable", "disable"]
    bestpath_med_missing_as_worst: Literal["enable", "disable"]
    client_to_client_reflection: Literal["enable", "disable"]
    dampening: Literal["enable", "disable"]
    deterministic_med: Literal["enable", "disable"]
    ebgp_multipath: Literal["enable", "disable"]
    ibgp_multipath: Literal["enable", "disable"]
    enforce_first_as: Literal["enable", "disable"]
    fast_external_failover: Literal["enable", "disable"]
    log_neighbour_changes: Literal["enable", "disable"]
    network_import_check: Literal["enable", "disable"]
    ignore_optional_capability: Literal["enable", "disable"]
    additional_path: Literal["enable", "disable"]
    additional_path6: Literal["enable", "disable"]
    additional_path_vpnv4: Literal["enable", "disable"]
    additional_path_vpnv6: Literal["enable", "disable"]
    multipath_recursive_distance: Literal["enable", "disable"]
    recursive_next_hop: Literal["enable", "disable"]
    recursive_inherit_priority: Literal["enable", "disable"]
    tag_resolve_mode: Literal["disable", "preferred", "merge", "merge-all"]
    cluster_id: str
    confederation_identifier: int
    confederation_peers: str | list[str] | list[BgpConfederationpeersItem]
    dampening_route_map: str
    dampening_reachability_half_life: int
    dampening_reuse: int
    dampening_suppress: int
    dampening_max_suppress_time: int
    dampening_unreachability_half_life: int
    default_local_preference: int
    scan_time: int
    distance_external: int
    distance_internal: int
    distance_local: int
    synchronization: Literal["enable", "disable"]
    graceful_restart: Literal["enable", "disable"]
    graceful_restart_time: int
    graceful_stalepath_time: int
    graceful_update_delay: int
    graceful_end_on_timer: Literal["enable", "disable"]
    additional_path_select: int
    additional_path_select6: int
    additional_path_select_vpnv4: int
    additional_path_select_vpnv6: int
    cross_family_conditional_adv: Literal["enable", "disable"]
    aggregate_address: str | list[str] | list[BgpAggregateaddressItem]
    aggregate_address6: str | list[str] | list[BgpAggregateaddress6Item]
    neighbor: str | list[str] | list[BgpNeighborItem]
    neighbor_group: str | list[str] | list[BgpNeighborgroupItem]
    neighbor_range: str | list[str] | list[BgpNeighborrangeItem]
    neighbor_range6: str | list[str] | list[BgpNeighborrange6Item]
    network: str | list[str] | list[BgpNetworkItem]
    network6: str | list[str] | list[BgpNetwork6Item]
    redistribute: str | list[str] | list[BgpRedistributeItem]
    redistribute6: str | list[str] | list[BgpRedistribute6Item]
    admin_distance: str | list[str] | list[BgpAdmindistanceItem]
    vrf: str | list[str] | list[BgpVrfItem]
    vrf6: str | list[str] | list[BgpVrf6Item]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class BgpResponse(TypedDict, total=False):
    """Response type for Bgp - use with .dict property for typed dict access."""
    asn: str
    router_id: str
    keepalive_timer: int
    holdtime_timer: int
    always_compare_med: Literal["enable", "disable"]
    bestpath_as_path_ignore: Literal["enable", "disable"]
    bestpath_cmp_confed_aspath: Literal["enable", "disable"]
    bestpath_cmp_routerid: Literal["enable", "disable"]
    bestpath_med_confed: Literal["enable", "disable"]
    bestpath_med_missing_as_worst: Literal["enable", "disable"]
    client_to_client_reflection: Literal["enable", "disable"]
    dampening: Literal["enable", "disable"]
    deterministic_med: Literal["enable", "disable"]
    ebgp_multipath: Literal["enable", "disable"]
    ibgp_multipath: Literal["enable", "disable"]
    enforce_first_as: Literal["enable", "disable"]
    fast_external_failover: Literal["enable", "disable"]
    log_neighbour_changes: Literal["enable", "disable"]
    network_import_check: Literal["enable", "disable"]
    ignore_optional_capability: Literal["enable", "disable"]
    additional_path: Literal["enable", "disable"]
    additional_path6: Literal["enable", "disable"]
    additional_path_vpnv4: Literal["enable", "disable"]
    additional_path_vpnv6: Literal["enable", "disable"]
    multipath_recursive_distance: Literal["enable", "disable"]
    recursive_next_hop: Literal["enable", "disable"]
    recursive_inherit_priority: Literal["enable", "disable"]
    tag_resolve_mode: Literal["disable", "preferred", "merge", "merge-all"]
    cluster_id: str
    confederation_identifier: int
    confederation_peers: list[BgpConfederationpeersItem]
    dampening_route_map: str
    dampening_reachability_half_life: int
    dampening_reuse: int
    dampening_suppress: int
    dampening_max_suppress_time: int
    dampening_unreachability_half_life: int
    default_local_preference: int
    scan_time: int
    distance_external: int
    distance_internal: int
    distance_local: int
    synchronization: Literal["enable", "disable"]
    graceful_restart: Literal["enable", "disable"]
    graceful_restart_time: int
    graceful_stalepath_time: int
    graceful_update_delay: int
    graceful_end_on_timer: Literal["enable", "disable"]
    additional_path_select: int
    additional_path_select6: int
    additional_path_select_vpnv4: int
    additional_path_select_vpnv6: int
    cross_family_conditional_adv: Literal["enable", "disable"]
    aggregate_address: list[BgpAggregateaddressItem]
    aggregate_address6: list[BgpAggregateaddress6Item]
    neighbor: list[BgpNeighborItem]
    neighbor_group: list[BgpNeighborgroupItem]
    neighbor_range: list[BgpNeighborrangeItem]
    neighbor_range6: list[BgpNeighborrange6Item]
    network: list[BgpNetworkItem]
    network6: list[BgpNetwork6Item]
    redistribute: list[BgpRedistributeItem]
    redistribute6: list[BgpRedistribute6Item]
    admin_distance: list[BgpAdmindistanceItem]
    vrf: list[BgpVrfItem]
    vrf6: list[BgpVrf6Item]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class BgpNeighborConditionaladvertiseItemObject(FortiObject[BgpNeighborConditionaladvertiseItem]):
    """Typed object for neighbor.conditional-advertise table items with attribute access."""
    advertise_routemap: str
    condition_routemap: str | list[str]
    condition_type: Literal["exist", "non-exist"]


class BgpNeighborConditionaladvertise6ItemObject(FortiObject[BgpNeighborConditionaladvertise6Item]):
    """Typed object for neighbor.conditional-advertise6 table items with attribute access."""
    advertise_routemap: str
    condition_routemap: str | list[str]
    condition_type: Literal["exist", "non-exist"]


class BgpVrfExportrtItemObject(FortiObject[BgpVrfExportrtItem]):
    """Typed object for vrf.export-rt table items with attribute access."""
    route_target: str


class BgpVrfImportrtItemObject(FortiObject[BgpVrfImportrtItem]):
    """Typed object for vrf.import-rt table items with attribute access."""
    route_target: str


class BgpVrfLeaktargetItemObject(FortiObject[BgpVrfLeaktargetItem]):
    """Typed object for vrf.leak-target table items with attribute access."""
    vrf: str
    route_map: str
    interface: str


class BgpVrf6ExportrtItemObject(FortiObject[BgpVrf6ExportrtItem]):
    """Typed object for vrf6.export-rt table items with attribute access."""
    route_target: str


class BgpVrf6ImportrtItemObject(FortiObject[BgpVrf6ImportrtItem]):
    """Typed object for vrf6.import-rt table items with attribute access."""
    route_target: str


class BgpVrf6LeaktargetItemObject(FortiObject[BgpVrf6LeaktargetItem]):
    """Typed object for vrf6.leak-target table items with attribute access."""
    vrf: str
    route_map: str
    interface: str


class BgpConfederationpeersItemObject(FortiObject[BgpConfederationpeersItem]):
    """Typed object for confederation-peers table items with attribute access."""
    peer: str


class BgpAggregateaddressItemObject(FortiObject[BgpAggregateaddressItem]):
    """Typed object for aggregate-address table items with attribute access."""
    id: int
    prefix: str
    as_set: Literal["enable", "disable"]
    summary_only: Literal["enable", "disable"]


class BgpAggregateaddress6ItemObject(FortiObject[BgpAggregateaddress6Item]):
    """Typed object for aggregate-address6 table items with attribute access."""
    id: int
    prefix6: str
    as_set: Literal["enable", "disable"]
    summary_only: Literal["enable", "disable"]


class BgpNeighborItemObject(FortiObject[BgpNeighborItem]):
    """Typed object for neighbor table items with attribute access."""
    ip: str
    advertisement_interval: int
    allowas_in_enable: Literal["enable", "disable"]
    allowas_in_enable6: Literal["enable", "disable"]
    allowas_in_enable_vpnv4: Literal["enable", "disable"]
    allowas_in_enable_vpnv6: Literal["enable", "disable"]
    allowas_in_enable_evpn: Literal["enable", "disable"]
    allowas_in: int
    allowas_in6: int
    allowas_in_vpnv4: int
    allowas_in_vpnv6: int
    allowas_in_evpn: int
    attribute_unchanged: Literal["as-path", "med", "next-hop"]
    attribute_unchanged6: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv4: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv6: Literal["as-path", "med", "next-hop"]
    activate: Literal["enable", "disable"]
    activate6: Literal["enable", "disable"]
    activate_vpnv4: Literal["enable", "disable"]
    activate_vpnv6: Literal["enable", "disable"]
    activate_evpn: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]
    capability_dynamic: Literal["enable", "disable"]
    capability_orf: Literal["none", "receive", "send", "both"]
    capability_orf6: Literal["none", "receive", "send", "both"]
    capability_graceful_restart: Literal["enable", "disable"]
    capability_graceful_restart6: Literal["enable", "disable"]
    capability_graceful_restart_vpnv4: Literal["enable", "disable"]
    capability_graceful_restart_vpnv6: Literal["enable", "disable"]
    capability_graceful_restart_evpn: Literal["enable", "disable"]
    capability_route_refresh: Literal["enable", "disable"]
    capability_default_originate: Literal["enable", "disable"]
    capability_default_originate6: Literal["enable", "disable"]
    dont_capability_negotiate: Literal["enable", "disable"]
    ebgp_enforce_multihop: Literal["enable", "disable"]
    link_down_failover: Literal["enable", "disable"]
    stale_route: Literal["enable", "disable"]
    next_hop_self: Literal["enable", "disable"]
    next_hop_self6: Literal["enable", "disable"]
    next_hop_self_rr: Literal["enable", "disable"]
    next_hop_self_rr6: Literal["enable", "disable"]
    next_hop_self_vpnv4: Literal["enable", "disable"]
    next_hop_self_vpnv6: Literal["enable", "disable"]
    override_capability: Literal["enable", "disable"]
    passive: Literal["enable", "disable"]
    remove_private_as: Literal["enable", "disable"]
    remove_private_as6: Literal["enable", "disable"]
    remove_private_as_vpnv4: Literal["enable", "disable"]
    remove_private_as_vpnv6: Literal["enable", "disable"]
    remove_private_as_evpn: Literal["enable", "disable"]
    route_reflector_client: Literal["enable", "disable"]
    route_reflector_client6: Literal["enable", "disable"]
    route_reflector_client_vpnv4: Literal["enable", "disable"]
    route_reflector_client_vpnv6: Literal["enable", "disable"]
    route_reflector_client_evpn: Literal["enable", "disable"]
    route_server_client: Literal["enable", "disable"]
    route_server_client6: Literal["enable", "disable"]
    route_server_client_vpnv4: Literal["enable", "disable"]
    route_server_client_vpnv6: Literal["enable", "disable"]
    route_server_client_evpn: Literal["enable", "disable"]
    rr_attr_allow_change: Literal["enable", "disable"]
    rr_attr_allow_change6: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv4: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv6: Literal["enable", "disable"]
    rr_attr_allow_change_evpn: Literal["enable", "disable"]
    shutdown: Literal["enable", "disable"]
    soft_reconfiguration: Literal["enable", "disable"]
    soft_reconfiguration6: Literal["enable", "disable"]
    soft_reconfiguration_vpnv4: Literal["enable", "disable"]
    soft_reconfiguration_vpnv6: Literal["enable", "disable"]
    soft_reconfiguration_evpn: Literal["enable", "disable"]
    as_override: Literal["enable", "disable"]
    as_override6: Literal["enable", "disable"]
    strict_capability_match: Literal["enable", "disable"]
    default_originate_routemap: str
    default_originate_routemap6: str
    description: str
    distribute_list_in: str
    distribute_list_in6: str
    distribute_list_in_vpnv4: str
    distribute_list_in_vpnv6: str
    distribute_list_out: str
    distribute_list_out6: str
    distribute_list_out_vpnv4: str
    distribute_list_out_vpnv6: str
    ebgp_multihop_ttl: int
    filter_list_in: str
    filter_list_in6: str
    filter_list_in_vpnv4: str
    filter_list_in_vpnv6: str
    filter_list_out: str
    filter_list_out6: str
    filter_list_out_vpnv4: str
    filter_list_out_vpnv6: str
    interface: str
    maximum_prefix: int
    maximum_prefix6: int
    maximum_prefix_vpnv4: int
    maximum_prefix_vpnv6: int
    maximum_prefix_evpn: int
    maximum_prefix_threshold: int
    maximum_prefix_threshold6: int
    maximum_prefix_threshold_vpnv4: int
    maximum_prefix_threshold_vpnv6: int
    maximum_prefix_threshold_evpn: int
    maximum_prefix_warning_only: Literal["enable", "disable"]
    maximum_prefix_warning_only6: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv4: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv6: Literal["enable", "disable"]
    maximum_prefix_warning_only_evpn: Literal["enable", "disable"]
    prefix_list_in: str
    prefix_list_in6: str
    prefix_list_in_vpnv4: str
    prefix_list_in_vpnv6: str
    prefix_list_out: str
    prefix_list_out6: str
    prefix_list_out_vpnv4: str
    prefix_list_out_vpnv6: str
    remote_as: str
    local_as: str
    local_as_no_prepend: Literal["enable", "disable"]
    local_as_replace_as: Literal["enable", "disable"]
    retain_stale_time: int
    route_map_in: str
    route_map_in6: str
    route_map_in_vpnv4: str
    route_map_in_vpnv6: str
    route_map_in_evpn: str
    route_map_out: str
    route_map_out_preferable: str
    route_map_out6: str
    route_map_out6_preferable: str
    route_map_out_vpnv4: str
    route_map_out_vpnv6: str
    route_map_out_vpnv4_preferable: str
    route_map_out_vpnv6_preferable: str
    route_map_out_evpn: str
    send_community: Literal["standard", "extended", "both", "disable"]
    send_community6: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv4: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv6: Literal["standard", "extended", "both", "disable"]
    send_community_evpn: Literal["standard", "extended", "both", "disable"]
    keep_alive_timer: int
    holdtime_timer: int
    connect_timer: int
    unsuppress_map: str
    unsuppress_map6: str
    update_source: str
    weight: int
    restart_time: int
    additional_path: Literal["send", "receive", "both", "disable"]
    additional_path6: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv4: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv6: Literal["send", "receive", "both", "disable"]
    adv_additional_path: int
    adv_additional_path6: int
    adv_additional_path_vpnv4: int
    adv_additional_path_vpnv6: int
    password: str
    auth_options: str
    conditional_advertise: FortiObjectList[BgpNeighborConditionaladvertiseItemObject]
    conditional_advertise6: FortiObjectList[BgpNeighborConditionaladvertise6ItemObject]


class BgpNeighborgroupItemObject(FortiObject[BgpNeighborgroupItem]):
    """Typed object for neighbor-group table items with attribute access."""
    name: str
    advertisement_interval: int
    allowas_in_enable: Literal["enable", "disable"]
    allowas_in_enable6: Literal["enable", "disable"]
    allowas_in_enable_vpnv4: Literal["enable", "disable"]
    allowas_in_enable_vpnv6: Literal["enable", "disable"]
    allowas_in_enable_evpn: Literal["enable", "disable"]
    allowas_in: int
    allowas_in6: int
    allowas_in_vpnv4: int
    allowas_in_vpnv6: int
    allowas_in_evpn: int
    attribute_unchanged: Literal["as-path", "med", "next-hop"]
    attribute_unchanged6: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv4: Literal["as-path", "med", "next-hop"]
    attribute_unchanged_vpnv6: Literal["as-path", "med", "next-hop"]
    activate: Literal["enable", "disable"]
    activate6: Literal["enable", "disable"]
    activate_vpnv4: Literal["enable", "disable"]
    activate_vpnv6: Literal["enable", "disable"]
    activate_evpn: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]
    capability_dynamic: Literal["enable", "disable"]
    capability_orf: Literal["none", "receive", "send", "both"]
    capability_orf6: Literal["none", "receive", "send", "both"]
    capability_graceful_restart: Literal["enable", "disable"]
    capability_graceful_restart6: Literal["enable", "disable"]
    capability_graceful_restart_vpnv4: Literal["enable", "disable"]
    capability_graceful_restart_vpnv6: Literal["enable", "disable"]
    capability_graceful_restart_evpn: Literal["enable", "disable"]
    capability_route_refresh: Literal["enable", "disable"]
    capability_default_originate: Literal["enable", "disable"]
    capability_default_originate6: Literal["enable", "disable"]
    dont_capability_negotiate: Literal["enable", "disable"]
    ebgp_enforce_multihop: Literal["enable", "disable"]
    link_down_failover: Literal["enable", "disable"]
    stale_route: Literal["enable", "disable"]
    next_hop_self: Literal["enable", "disable"]
    next_hop_self6: Literal["enable", "disable"]
    next_hop_self_rr: Literal["enable", "disable"]
    next_hop_self_rr6: Literal["enable", "disable"]
    next_hop_self_vpnv4: Literal["enable", "disable"]
    next_hop_self_vpnv6: Literal["enable", "disable"]
    override_capability: Literal["enable", "disable"]
    passive: Literal["enable", "disable"]
    remove_private_as: Literal["enable", "disable"]
    remove_private_as6: Literal["enable", "disable"]
    remove_private_as_vpnv4: Literal["enable", "disable"]
    remove_private_as_vpnv6: Literal["enable", "disable"]
    remove_private_as_evpn: Literal["enable", "disable"]
    route_reflector_client: Literal["enable", "disable"]
    route_reflector_client6: Literal["enable", "disable"]
    route_reflector_client_vpnv4: Literal["enable", "disable"]
    route_reflector_client_vpnv6: Literal["enable", "disable"]
    route_reflector_client_evpn: Literal["enable", "disable"]
    route_server_client: Literal["enable", "disable"]
    route_server_client6: Literal["enable", "disable"]
    route_server_client_vpnv4: Literal["enable", "disable"]
    route_server_client_vpnv6: Literal["enable", "disable"]
    route_server_client_evpn: Literal["enable", "disable"]
    rr_attr_allow_change: Literal["enable", "disable"]
    rr_attr_allow_change6: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv4: Literal["enable", "disable"]
    rr_attr_allow_change_vpnv6: Literal["enable", "disable"]
    rr_attr_allow_change_evpn: Literal["enable", "disable"]
    shutdown: Literal["enable", "disable"]
    soft_reconfiguration: Literal["enable", "disable"]
    soft_reconfiguration6: Literal["enable", "disable"]
    soft_reconfiguration_vpnv4: Literal["enable", "disable"]
    soft_reconfiguration_vpnv6: Literal["enable", "disable"]
    soft_reconfiguration_evpn: Literal["enable", "disable"]
    as_override: Literal["enable", "disable"]
    as_override6: Literal["enable", "disable"]
    strict_capability_match: Literal["enable", "disable"]
    default_originate_routemap: str
    default_originate_routemap6: str
    description: str
    distribute_list_in: str
    distribute_list_in6: str
    distribute_list_in_vpnv4: str
    distribute_list_in_vpnv6: str
    distribute_list_out: str
    distribute_list_out6: str
    distribute_list_out_vpnv4: str
    distribute_list_out_vpnv6: str
    ebgp_multihop_ttl: int
    filter_list_in: str
    filter_list_in6: str
    filter_list_in_vpnv4: str
    filter_list_in_vpnv6: str
    filter_list_out: str
    filter_list_out6: str
    filter_list_out_vpnv4: str
    filter_list_out_vpnv6: str
    interface: str
    maximum_prefix: int
    maximum_prefix6: int
    maximum_prefix_vpnv4: int
    maximum_prefix_vpnv6: int
    maximum_prefix_evpn: int
    maximum_prefix_threshold: int
    maximum_prefix_threshold6: int
    maximum_prefix_threshold_vpnv4: int
    maximum_prefix_threshold_vpnv6: int
    maximum_prefix_threshold_evpn: int
    maximum_prefix_warning_only: Literal["enable", "disable"]
    maximum_prefix_warning_only6: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv4: Literal["enable", "disable"]
    maximum_prefix_warning_only_vpnv6: Literal["enable", "disable"]
    maximum_prefix_warning_only_evpn: Literal["enable", "disable"]
    prefix_list_in: str
    prefix_list_in6: str
    prefix_list_in_vpnv4: str
    prefix_list_in_vpnv6: str
    prefix_list_out: str
    prefix_list_out6: str
    prefix_list_out_vpnv4: str
    prefix_list_out_vpnv6: str
    remote_as: str
    remote_as_filter: str
    local_as: str
    local_as_no_prepend: Literal["enable", "disable"]
    local_as_replace_as: Literal["enable", "disable"]
    retain_stale_time: int
    route_map_in: str
    route_map_in6: str
    route_map_in_vpnv4: str
    route_map_in_vpnv6: str
    route_map_in_evpn: str
    route_map_out: str
    route_map_out_preferable: str
    route_map_out6: str
    route_map_out6_preferable: str
    route_map_out_vpnv4: str
    route_map_out_vpnv6: str
    route_map_out_vpnv4_preferable: str
    route_map_out_vpnv6_preferable: str
    route_map_out_evpn: str
    send_community: Literal["standard", "extended", "both", "disable"]
    send_community6: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv4: Literal["standard", "extended", "both", "disable"]
    send_community_vpnv6: Literal["standard", "extended", "both", "disable"]
    send_community_evpn: Literal["standard", "extended", "both", "disable"]
    keep_alive_timer: int
    holdtime_timer: int
    connect_timer: int
    unsuppress_map: str
    unsuppress_map6: str
    update_source: str
    weight: int
    restart_time: int
    additional_path: Literal["send", "receive", "both", "disable"]
    additional_path6: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv4: Literal["send", "receive", "both", "disable"]
    additional_path_vpnv6: Literal["send", "receive", "both", "disable"]
    adv_additional_path: int
    adv_additional_path6: int
    adv_additional_path_vpnv4: int
    adv_additional_path_vpnv6: int
    password: str
    auth_options: str


class BgpNeighborrangeItemObject(FortiObject[BgpNeighborrangeItem]):
    """Typed object for neighbor-range table items with attribute access."""
    id: int
    prefix: str
    max_neighbor_num: int
    neighbor_group: str


class BgpNeighborrange6ItemObject(FortiObject[BgpNeighborrange6Item]):
    """Typed object for neighbor-range6 table items with attribute access."""
    id: int
    prefix6: str
    max_neighbor_num: int
    neighbor_group: str


class BgpNetworkItemObject(FortiObject[BgpNetworkItem]):
    """Typed object for network table items with attribute access."""
    id: int
    prefix: str
    network_import_check: Literal["global", "enable", "disable"]
    backdoor: Literal["enable", "disable"]
    route_map: str
    prefix_name: str


class BgpNetwork6ItemObject(FortiObject[BgpNetwork6Item]):
    """Typed object for network6 table items with attribute access."""
    id: int
    prefix6: str
    network_import_check: Literal["global", "enable", "disable"]
    backdoor: Literal["enable", "disable"]
    route_map: str


class BgpRedistributeItemObject(FortiObject[BgpRedistributeItem]):
    """Typed object for redistribute table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    route_map: str


class BgpRedistribute6ItemObject(FortiObject[BgpRedistribute6Item]):
    """Typed object for redistribute6 table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    route_map: str


class BgpAdmindistanceItemObject(FortiObject[BgpAdmindistanceItem]):
    """Typed object for admin-distance table items with attribute access."""
    id: int
    neighbour_prefix: str
    route_list: str
    distance: int


class BgpVrfItemObject(FortiObject[BgpVrfItem]):
    """Typed object for vrf table items with attribute access."""
    vrf: str
    role: Literal["standalone", "ce", "pe"]
    rd: str
    export_rt: FortiObjectList[BgpVrfExportrtItemObject]
    import_rt: FortiObjectList[BgpVrfImportrtItemObject]
    import_route_map: str
    leak_target: FortiObjectList[BgpVrfLeaktargetItemObject]


class BgpVrf6ItemObject(FortiObject[BgpVrf6Item]):
    """Typed object for vrf6 table items with attribute access."""
    vrf: str
    role: Literal["standalone", "ce", "pe"]
    rd: str
    export_rt: FortiObjectList[BgpVrf6ExportrtItemObject]
    import_rt: FortiObjectList[BgpVrf6ImportrtItemObject]
    import_route_map: str
    leak_target: FortiObjectList[BgpVrf6LeaktargetItemObject]


class BgpObject(FortiObject):
    """Typed FortiObject for Bgp with field access."""
    asn: str
    router_id: str
    keepalive_timer: int
    holdtime_timer: int
    always_compare_med: Literal["enable", "disable"]
    bestpath_as_path_ignore: Literal["enable", "disable"]
    bestpath_cmp_confed_aspath: Literal["enable", "disable"]
    bestpath_cmp_routerid: Literal["enable", "disable"]
    bestpath_med_confed: Literal["enable", "disable"]
    bestpath_med_missing_as_worst: Literal["enable", "disable"]
    client_to_client_reflection: Literal["enable", "disable"]
    dampening: Literal["enable", "disable"]
    deterministic_med: Literal["enable", "disable"]
    ebgp_multipath: Literal["enable", "disable"]
    ibgp_multipath: Literal["enable", "disable"]
    enforce_first_as: Literal["enable", "disable"]
    fast_external_failover: Literal["enable", "disable"]
    log_neighbour_changes: Literal["enable", "disable"]
    network_import_check: Literal["enable", "disable"]
    ignore_optional_capability: Literal["enable", "disable"]
    additional_path: Literal["enable", "disable"]
    additional_path6: Literal["enable", "disable"]
    additional_path_vpnv4: Literal["enable", "disable"]
    additional_path_vpnv6: Literal["enable", "disable"]
    multipath_recursive_distance: Literal["enable", "disable"]
    recursive_next_hop: Literal["enable", "disable"]
    recursive_inherit_priority: Literal["enable", "disable"]
    tag_resolve_mode: Literal["disable", "preferred", "merge", "merge-all"]
    cluster_id: str
    confederation_identifier: int
    confederation_peers: FortiObjectList[BgpConfederationpeersItemObject]
    dampening_route_map: str
    dampening_reachability_half_life: int
    dampening_reuse: int
    dampening_suppress: int
    dampening_max_suppress_time: int
    dampening_unreachability_half_life: int
    default_local_preference: int
    scan_time: int
    distance_external: int
    distance_internal: int
    distance_local: int
    synchronization: Literal["enable", "disable"]
    graceful_restart: Literal["enable", "disable"]
    graceful_restart_time: int
    graceful_stalepath_time: int
    graceful_update_delay: int
    graceful_end_on_timer: Literal["enable", "disable"]
    additional_path_select: int
    additional_path_select6: int
    additional_path_select_vpnv4: int
    additional_path_select_vpnv6: int
    cross_family_conditional_adv: Literal["enable", "disable"]
    aggregate_address: FortiObjectList[BgpAggregateaddressItemObject]
    aggregate_address6: FortiObjectList[BgpAggregateaddress6ItemObject]
    neighbor: FortiObjectList[BgpNeighborItemObject]
    neighbor_group: FortiObjectList[BgpNeighborgroupItemObject]
    neighbor_range: FortiObjectList[BgpNeighborrangeItemObject]
    neighbor_range6: FortiObjectList[BgpNeighborrange6ItemObject]
    network: FortiObjectList[BgpNetworkItemObject]
    network6: FortiObjectList[BgpNetwork6ItemObject]
    redistribute: FortiObjectList[BgpRedistributeItemObject]
    redistribute6: FortiObjectList[BgpRedistribute6ItemObject]
    admin_distance: FortiObjectList[BgpAdmindistanceItemObject]
    vrf: FortiObjectList[BgpVrfItemObject]
    vrf6: FortiObjectList[BgpVrf6ItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Bgp:
    """
    
    Endpoint: router/bgp
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BgpObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: BgpPayload | None = ...,
        asn: str | None = ...,
        router_id: str | None = ...,
        keepalive_timer: int | None = ...,
        holdtime_timer: int | None = ...,
        always_compare_med: Literal["enable", "disable"] | None = ...,
        bestpath_as_path_ignore: Literal["enable", "disable"] | None = ...,
        bestpath_cmp_confed_aspath: Literal["enable", "disable"] | None = ...,
        bestpath_cmp_routerid: Literal["enable", "disable"] | None = ...,
        bestpath_med_confed: Literal["enable", "disable"] | None = ...,
        bestpath_med_missing_as_worst: Literal["enable", "disable"] | None = ...,
        client_to_client_reflection: Literal["enable", "disable"] | None = ...,
        dampening: Literal["enable", "disable"] | None = ...,
        deterministic_med: Literal["enable", "disable"] | None = ...,
        ebgp_multipath: Literal["enable", "disable"] | None = ...,
        ibgp_multipath: Literal["enable", "disable"] | None = ...,
        enforce_first_as: Literal["enable", "disable"] | None = ...,
        fast_external_failover: Literal["enable", "disable"] | None = ...,
        log_neighbour_changes: Literal["enable", "disable"] | None = ...,
        network_import_check: Literal["enable", "disable"] | None = ...,
        ignore_optional_capability: Literal["enable", "disable"] | None = ...,
        additional_path: Literal["enable", "disable"] | None = ...,
        additional_path6: Literal["enable", "disable"] | None = ...,
        additional_path_vpnv4: Literal["enable", "disable"] | None = ...,
        additional_path_vpnv6: Literal["enable", "disable"] | None = ...,
        multipath_recursive_distance: Literal["enable", "disable"] | None = ...,
        recursive_next_hop: Literal["enable", "disable"] | None = ...,
        recursive_inherit_priority: Literal["enable", "disable"] | None = ...,
        tag_resolve_mode: Literal["disable", "preferred", "merge", "merge-all"] | None = ...,
        cluster_id: str | None = ...,
        confederation_identifier: int | None = ...,
        confederation_peers: str | list[str] | list[BgpConfederationpeersItem] | None = ...,
        dampening_route_map: str | None = ...,
        dampening_reachability_half_life: int | None = ...,
        dampening_reuse: int | None = ...,
        dampening_suppress: int | None = ...,
        dampening_max_suppress_time: int | None = ...,
        dampening_unreachability_half_life: int | None = ...,
        default_local_preference: int | None = ...,
        scan_time: int | None = ...,
        distance_external: int | None = ...,
        distance_internal: int | None = ...,
        distance_local: int | None = ...,
        synchronization: Literal["enable", "disable"] | None = ...,
        graceful_restart: Literal["enable", "disable"] | None = ...,
        graceful_restart_time: int | None = ...,
        graceful_stalepath_time: int | None = ...,
        graceful_update_delay: int | None = ...,
        graceful_end_on_timer: Literal["enable", "disable"] | None = ...,
        additional_path_select: int | None = ...,
        additional_path_select6: int | None = ...,
        additional_path_select_vpnv4: int | None = ...,
        additional_path_select_vpnv6: int | None = ...,
        cross_family_conditional_adv: Literal["enable", "disable"] | None = ...,
        aggregate_address: str | list[str] | list[BgpAggregateaddressItem] | None = ...,
        aggregate_address6: str | list[str] | list[BgpAggregateaddress6Item] | None = ...,
        neighbor: str | list[str] | list[BgpNeighborItem] | None = ...,
        neighbor_group: str | list[str] | list[BgpNeighborgroupItem] | None = ...,
        neighbor_range: str | list[str] | list[BgpNeighborrangeItem] | None = ...,
        neighbor_range6: str | list[str] | list[BgpNeighborrange6Item] | None = ...,
        network: str | list[str] | list[BgpNetworkItem] | None = ...,
        network6: str | list[str] | list[BgpNetwork6Item] | None = ...,
        redistribute: str | list[str] | list[BgpRedistributeItem] | None = ...,
        redistribute6: str | list[str] | list[BgpRedistribute6Item] | None = ...,
        admin_distance: str | list[str] | list[BgpAdmindistanceItem] | None = ...,
        vrf: str | list[str] | list[BgpVrfItem] | None = ...,
        vrf6: str | list[str] | list[BgpVrf6Item] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BgpObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: BgpPayload | None = ...,
        asn: str | None = ...,
        router_id: str | None = ...,
        keepalive_timer: int | None = ...,
        holdtime_timer: int | None = ...,
        always_compare_med: Literal["enable", "disable"] | None = ...,
        bestpath_as_path_ignore: Literal["enable", "disable"] | None = ...,
        bestpath_cmp_confed_aspath: Literal["enable", "disable"] | None = ...,
        bestpath_cmp_routerid: Literal["enable", "disable"] | None = ...,
        bestpath_med_confed: Literal["enable", "disable"] | None = ...,
        bestpath_med_missing_as_worst: Literal["enable", "disable"] | None = ...,
        client_to_client_reflection: Literal["enable", "disable"] | None = ...,
        dampening: Literal["enable", "disable"] | None = ...,
        deterministic_med: Literal["enable", "disable"] | None = ...,
        ebgp_multipath: Literal["enable", "disable"] | None = ...,
        ibgp_multipath: Literal["enable", "disable"] | None = ...,
        enforce_first_as: Literal["enable", "disable"] | None = ...,
        fast_external_failover: Literal["enable", "disable"] | None = ...,
        log_neighbour_changes: Literal["enable", "disable"] | None = ...,
        network_import_check: Literal["enable", "disable"] | None = ...,
        ignore_optional_capability: Literal["enable", "disable"] | None = ...,
        additional_path: Literal["enable", "disable"] | None = ...,
        additional_path6: Literal["enable", "disable"] | None = ...,
        additional_path_vpnv4: Literal["enable", "disable"] | None = ...,
        additional_path_vpnv6: Literal["enable", "disable"] | None = ...,
        multipath_recursive_distance: Literal["enable", "disable"] | None = ...,
        recursive_next_hop: Literal["enable", "disable"] | None = ...,
        recursive_inherit_priority: Literal["enable", "disable"] | None = ...,
        tag_resolve_mode: Literal["disable", "preferred", "merge", "merge-all"] | None = ...,
        cluster_id: str | None = ...,
        confederation_identifier: int | None = ...,
        confederation_peers: str | list[str] | list[BgpConfederationpeersItem] | None = ...,
        dampening_route_map: str | None = ...,
        dampening_reachability_half_life: int | None = ...,
        dampening_reuse: int | None = ...,
        dampening_suppress: int | None = ...,
        dampening_max_suppress_time: int | None = ...,
        dampening_unreachability_half_life: int | None = ...,
        default_local_preference: int | None = ...,
        scan_time: int | None = ...,
        distance_external: int | None = ...,
        distance_internal: int | None = ...,
        distance_local: int | None = ...,
        synchronization: Literal["enable", "disable"] | None = ...,
        graceful_restart: Literal["enable", "disable"] | None = ...,
        graceful_restart_time: int | None = ...,
        graceful_stalepath_time: int | None = ...,
        graceful_update_delay: int | None = ...,
        graceful_end_on_timer: Literal["enable", "disable"] | None = ...,
        additional_path_select: int | None = ...,
        additional_path_select6: int | None = ...,
        additional_path_select_vpnv4: int | None = ...,
        additional_path_select_vpnv6: int | None = ...,
        cross_family_conditional_adv: Literal["enable", "disable"] | None = ...,
        aggregate_address: str | list[str] | list[BgpAggregateaddressItem] | None = ...,
        aggregate_address6: str | list[str] | list[BgpAggregateaddress6Item] | None = ...,
        neighbor: str | list[str] | list[BgpNeighborItem] | None = ...,
        neighbor_group: str | list[str] | list[BgpNeighborgroupItem] | None = ...,
        neighbor_range: str | list[str] | list[BgpNeighborrangeItem] | None = ...,
        neighbor_range6: str | list[str] | list[BgpNeighborrange6Item] | None = ...,
        network: str | list[str] | list[BgpNetworkItem] | None = ...,
        network6: str | list[str] | list[BgpNetwork6Item] | None = ...,
        redistribute: str | list[str] | list[BgpRedistributeItem] | None = ...,
        redistribute6: str | list[str] | list[BgpRedistribute6Item] | None = ...,
        admin_distance: str | list[str] | list[BgpAdmindistanceItem] | None = ...,
        vrf: str | list[str] | list[BgpVrfItem] | None = ...,
        vrf6: str | list[str] | list[BgpVrf6Item] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> list[str] | list[dict[str, Any]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> FortiObject[Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> FortiObject[Any]: ...
    
    @staticmethod
    def schema() -> FortiObject[Any]: ...


__all__ = [
    "Bgp",
    "BgpPayload",
    "BgpResponse",
    "BgpObject",
]