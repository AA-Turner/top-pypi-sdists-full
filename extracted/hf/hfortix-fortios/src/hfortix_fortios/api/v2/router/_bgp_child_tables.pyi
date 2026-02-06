"""
Child Table Helper Type Stubs for router/bgp

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class ConfederationPeersDict(TypedDict, total=False):
    """Type definition for confederation_peers child table entry."""
    peer: str | None

class AggregateAddressDict(TypedDict, total=False):
    """Type definition for aggregate_address child table entry."""
    id: int
    prefix: str
    as_set: str | None
    summary_only: str | None

class AggregateAddress6Dict(TypedDict, total=False):
    """Type definition for aggregate_address6 child table entry."""
    id: int
    prefix6: str
    as_set: str | None
    summary_only: str | None

class NeighborDict(TypedDict, total=False):
    """Type definition for neighbor child table entry."""
    ip: str
    advertisement_interval: int | None
    allowas_in_enable: str | None
    allowas_in_enable6: str | None
    allowas_in_enable_vpnv4: str | None
    allowas_in_enable_vpnv6: str | None
    allowas_in_enable_evpn: str | None
    allowas_in: int | None
    allowas_in6: int | None
    allowas_in_vpnv4: int | None
    allowas_in_vpnv6: int | None
    allowas_in_evpn: int | None
    attribute_unchanged: str | None
    attribute_unchanged6: str | None
    attribute_unchanged_vpnv4: str | None
    attribute_unchanged_vpnv6: str | None
    activate: str | None
    activate6: str | None
    activate_vpnv4: str | None
    activate_vpnv6: str | None
    activate_evpn: str | None
    bfd: str | None
    capability_dynamic: str | None
    capability_orf: str | None
    capability_orf6: str | None
    capability_graceful_restart: str | None
    capability_graceful_restart6: str | None
    capability_graceful_restart_vpnv4: str | None
    capability_graceful_restart_vpnv6: str | None
    capability_graceful_restart_evpn: str | None
    capability_route_refresh: str | None
    capability_default_originate: str | None
    capability_default_originate6: str | None
    dont_capability_negotiate: str | None
    ebgp_enforce_multihop: str | None
    link_down_failover: str | None
    stale_route: str | None
    next_hop_self: str | None
    next_hop_self6: str | None
    next_hop_self_rr: str | None
    next_hop_self_rr6: str | None
    next_hop_self_vpnv4: str | None
    next_hop_self_vpnv6: str | None
    override_capability: str | None
    passive: str | None
    remove_private_as: str | None
    remove_private_as6: str | None
    remove_private_as_vpnv4: str | None
    remove_private_as_vpnv6: str | None
    remove_private_as_evpn: str | None
    route_reflector_client: str | None
    route_reflector_client6: str | None
    route_reflector_client_vpnv4: str | None
    route_reflector_client_vpnv6: str | None
    route_reflector_client_evpn: str | None
    route_server_client: str | None
    route_server_client6: str | None
    route_server_client_vpnv4: str | None
    route_server_client_vpnv6: str | None
    route_server_client_evpn: str | None
    rr_attr_allow_change: str | None
    rr_attr_allow_change6: str | None
    rr_attr_allow_change_vpnv4: str | None
    rr_attr_allow_change_vpnv6: str | None
    rr_attr_allow_change_evpn: str | None
    shutdown: str | None
    soft_reconfiguration: str | None
    soft_reconfiguration6: str | None
    soft_reconfiguration_vpnv4: str | None
    soft_reconfiguration_vpnv6: str | None
    soft_reconfiguration_evpn: str | None
    as_override: str | None
    as_override6: str | None
    strict_capability_match: str | None
    default_originate_routemap: str | None
    default_originate_routemap6: str | None
    description: str | None
    distribute_list_in: str | None
    distribute_list_in6: str | None
    distribute_list_in_vpnv4: str | None
    distribute_list_in_vpnv6: str | None
    distribute_list_out: str | None
    distribute_list_out6: str | None
    distribute_list_out_vpnv4: str | None
    distribute_list_out_vpnv6: str | None
    ebgp_multihop_ttl: int | None
    filter_list_in: str | None
    filter_list_in6: str | None
    filter_list_in_vpnv4: str | None
    filter_list_in_vpnv6: str | None
    filter_list_out: str | None
    filter_list_out6: str | None
    filter_list_out_vpnv4: str | None
    filter_list_out_vpnv6: str | None
    interface: str | None
    maximum_prefix: int | None
    maximum_prefix6: int | None
    maximum_prefix_vpnv4: int | None
    maximum_prefix_vpnv6: int | None
    maximum_prefix_evpn: int | None
    maximum_prefix_threshold: int | None
    maximum_prefix_threshold6: int | None
    maximum_prefix_threshold_vpnv4: int | None
    maximum_prefix_threshold_vpnv6: int | None
    maximum_prefix_threshold_evpn: int | None
    maximum_prefix_warning_only: str | None
    maximum_prefix_warning_only6: str | None
    maximum_prefix_warning_only_vpnv4: str | None
    maximum_prefix_warning_only_vpnv6: str | None
    maximum_prefix_warning_only_evpn: str | None
    prefix_list_in: str | None
    prefix_list_in6: str | None
    prefix_list_in_vpnv4: str | None
    prefix_list_in_vpnv6: str | None
    prefix_list_out: str | None
    prefix_list_out6: str | None
    prefix_list_out_vpnv4: str | None
    prefix_list_out_vpnv6: str | None
    remote_as: str
    local_as: str | None
    local_as_no_prepend: str | None
    local_as_replace_as: str | None
    retain_stale_time: int | None
    route_map_in: str | None
    route_map_in6: str | None
    route_map_in_vpnv4: str | None
    route_map_in_vpnv6: str | None
    route_map_in_evpn: str | None
    route_map_out: str | None
    route_map_out_preferable: str | None
    route_map_out6: str | None
    route_map_out6_preferable: str | None
    route_map_out_vpnv4: str | None
    route_map_out_vpnv6: str | None
    route_map_out_vpnv4_preferable: str | None
    route_map_out_vpnv6_preferable: str | None
    route_map_out_evpn: str | None
    send_community: str | None
    send_community6: str | None
    send_community_vpnv4: str | None
    send_community_vpnv6: str | None
    send_community_evpn: str | None
    keep_alive_timer: int | None
    holdtime_timer: int | None
    connect_timer: int | None
    unsuppress_map: str | None
    unsuppress_map6: str | None
    update_source: str | None
    weight: int | None
    restart_time: int | None
    additional_path: str | None
    additional_path6: str | None
    additional_path_vpnv4: str | None
    additional_path_vpnv6: str | None
    adv_additional_path: int | None
    adv_additional_path6: int | None
    adv_additional_path_vpnv4: int | None
    adv_additional_path_vpnv6: int | None
    password: str | None
    auth_options: str | None
    conditional_advertise: list[Any] | None
    conditional_advertise6: list[Any] | None

class NeighborGroupDict(TypedDict, total=False):
    """Type definition for neighbor_group child table entry."""
    name: str
    advertisement_interval: int | None
    allowas_in_enable: str | None
    allowas_in_enable6: str | None
    allowas_in_enable_vpnv4: str | None
    allowas_in_enable_vpnv6: str | None
    allowas_in_enable_evpn: str | None
    allowas_in: int | None
    allowas_in6: int | None
    allowas_in_vpnv4: int | None
    allowas_in_vpnv6: int | None
    allowas_in_evpn: int | None
    attribute_unchanged: str | None
    attribute_unchanged6: str | None
    attribute_unchanged_vpnv4: str | None
    attribute_unchanged_vpnv6: str | None
    activate: str | None
    activate6: str | None
    activate_vpnv4: str | None
    activate_vpnv6: str | None
    activate_evpn: str | None
    bfd: str | None
    capability_dynamic: str | None
    capability_orf: str | None
    capability_orf6: str | None
    capability_graceful_restart: str | None
    capability_graceful_restart6: str | None
    capability_graceful_restart_vpnv4: str | None
    capability_graceful_restart_vpnv6: str | None
    capability_graceful_restart_evpn: str | None
    capability_route_refresh: str | None
    capability_default_originate: str | None
    capability_default_originate6: str | None
    dont_capability_negotiate: str | None
    ebgp_enforce_multihop: str | None
    link_down_failover: str | None
    stale_route: str | None
    next_hop_self: str | None
    next_hop_self6: str | None
    next_hop_self_rr: str | None
    next_hop_self_rr6: str | None
    next_hop_self_vpnv4: str | None
    next_hop_self_vpnv6: str | None
    override_capability: str | None
    passive: str | None
    remove_private_as: str | None
    remove_private_as6: str | None
    remove_private_as_vpnv4: str | None
    remove_private_as_vpnv6: str | None
    remove_private_as_evpn: str | None
    route_reflector_client: str | None
    route_reflector_client6: str | None
    route_reflector_client_vpnv4: str | None
    route_reflector_client_vpnv6: str | None
    route_reflector_client_evpn: str | None
    route_server_client: str | None
    route_server_client6: str | None
    route_server_client_vpnv4: str | None
    route_server_client_vpnv6: str | None
    route_server_client_evpn: str | None
    rr_attr_allow_change: str | None
    rr_attr_allow_change6: str | None
    rr_attr_allow_change_vpnv4: str | None
    rr_attr_allow_change_vpnv6: str | None
    rr_attr_allow_change_evpn: str | None
    shutdown: str | None
    soft_reconfiguration: str | None
    soft_reconfiguration6: str | None
    soft_reconfiguration_vpnv4: str | None
    soft_reconfiguration_vpnv6: str | None
    soft_reconfiguration_evpn: str | None
    as_override: str | None
    as_override6: str | None
    strict_capability_match: str | None
    default_originate_routemap: str | None
    default_originate_routemap6: str | None
    description: str | None
    distribute_list_in: str | None
    distribute_list_in6: str | None
    distribute_list_in_vpnv4: str | None
    distribute_list_in_vpnv6: str | None
    distribute_list_out: str | None
    distribute_list_out6: str | None
    distribute_list_out_vpnv4: str | None
    distribute_list_out_vpnv6: str | None
    ebgp_multihop_ttl: int | None
    filter_list_in: str | None
    filter_list_in6: str | None
    filter_list_in_vpnv4: str | None
    filter_list_in_vpnv6: str | None
    filter_list_out: str | None
    filter_list_out6: str | None
    filter_list_out_vpnv4: str | None
    filter_list_out_vpnv6: str | None
    interface: str | None
    maximum_prefix: int | None
    maximum_prefix6: int | None
    maximum_prefix_vpnv4: int | None
    maximum_prefix_vpnv6: int | None
    maximum_prefix_evpn: int | None
    maximum_prefix_threshold: int | None
    maximum_prefix_threshold6: int | None
    maximum_prefix_threshold_vpnv4: int | None
    maximum_prefix_threshold_vpnv6: int | None
    maximum_prefix_threshold_evpn: int | None
    maximum_prefix_warning_only: str | None
    maximum_prefix_warning_only6: str | None
    maximum_prefix_warning_only_vpnv4: str | None
    maximum_prefix_warning_only_vpnv6: str | None
    maximum_prefix_warning_only_evpn: str | None
    prefix_list_in: str | None
    prefix_list_in6: str | None
    prefix_list_in_vpnv4: str | None
    prefix_list_in_vpnv6: str | None
    prefix_list_out: str | None
    prefix_list_out6: str | None
    prefix_list_out_vpnv4: str | None
    prefix_list_out_vpnv6: str | None
    remote_as: str
    remote_as_filter: str
    local_as: str | None
    local_as_no_prepend: str | None
    local_as_replace_as: str | None
    retain_stale_time: int | None
    route_map_in: str | None
    route_map_in6: str | None
    route_map_in_vpnv4: str | None
    route_map_in_vpnv6: str | None
    route_map_in_evpn: str | None
    route_map_out: str | None
    route_map_out_preferable: str | None
    route_map_out6: str | None
    route_map_out6_preferable: str | None
    route_map_out_vpnv4: str | None
    route_map_out_vpnv6: str | None
    route_map_out_vpnv4_preferable: str | None
    route_map_out_vpnv6_preferable: str | None
    route_map_out_evpn: str | None
    send_community: str | None
    send_community6: str | None
    send_community_vpnv4: str | None
    send_community_vpnv6: str | None
    send_community_evpn: str | None
    keep_alive_timer: int | None
    holdtime_timer: int | None
    connect_timer: int | None
    unsuppress_map: str | None
    unsuppress_map6: str | None
    update_source: str | None
    weight: int | None
    restart_time: int | None
    additional_path: str | None
    additional_path6: str | None
    additional_path_vpnv4: str | None
    additional_path_vpnv6: str | None
    adv_additional_path: int | None
    adv_additional_path6: int | None
    adv_additional_path_vpnv4: int | None
    adv_additional_path_vpnv6: int | None
    password: str | None
    auth_options: str | None

class NeighborRangeDict(TypedDict, total=False):
    """Type definition for neighbor_range child table entry."""
    id: int | None
    prefix: str
    max_neighbor_num: int | None
    neighbor_group: str

class NeighborRange6Dict(TypedDict, total=False):
    """Type definition for neighbor_range6 child table entry."""
    id: int | None
    prefix6: str
    max_neighbor_num: int | None
    neighbor_group: str

class NetworkDict(TypedDict, total=False):
    """Type definition for network child table entry."""
    id: int
    prefix: str
    network_import_check: str | None
    backdoor: str | None
    route_map: str | None
    prefix_name: str | None

class Network6Dict(TypedDict, total=False):
    """Type definition for network6 child table entry."""
    id: int
    prefix6: str
    network_import_check: str | None
    backdoor: str | None
    route_map: str | None

class RedistributeDict(TypedDict, total=False):
    """Type definition for redistribute child table entry."""
    name: str
    status: str | None
    route_map: str | None

class Redistribute6Dict(TypedDict, total=False):
    """Type definition for redistribute6 child table entry."""
    name: str
    status: str | None
    route_map: str | None

class AdminDistanceDict(TypedDict, total=False):
    """Type definition for admin_distance child table entry."""
    id: int
    neighbour_prefix: str
    route_list: str | None
    distance: int

class VrfDict(TypedDict, total=False):
    """Type definition for vrf child table entry."""
    vrf: str | None
    role: str | None
    rd: str | None
    export_rt: list[Any] | None
    import_rt: list[Any] | None
    import_route_map: str | None
    leak_target: list[Any] | None

class Vrf6Dict(TypedDict, total=False):
    """Type definition for vrf6 child table entry."""
    vrf: str | None
    role: str | None
    rd: str | None
    export_rt: list[Any] | None
    import_rt: list[Any] | None
    import_route_map: str | None
    leak_target: list[Any] | None


class ConfederationPeersObject(FortiObject):
    """Typed FortiObject for confederation_peers child table entry with attribute access."""
    peer: str | None


class AggregateAddressObject(FortiObject):
    """Typed FortiObject for aggregate_address child table entry with attribute access."""
    id: int
    prefix: str
    as_set: str | None
    summary_only: str | None


class AggregateAddress6Object(FortiObject):
    """Typed FortiObject for aggregate_address6 child table entry with attribute access."""
    id: int
    prefix6: str
    as_set: str | None
    summary_only: str | None


class NeighborObject(FortiObject):
    """Typed FortiObject for neighbor child table entry with attribute access."""
    ip: str
    advertisement_interval: int | None
    allowas_in_enable: str | None
    allowas_in_enable6: str | None
    allowas_in_enable_vpnv4: str | None
    allowas_in_enable_vpnv6: str | None
    allowas_in_enable_evpn: str | None
    allowas_in: int | None
    allowas_in6: int | None
    allowas_in_vpnv4: int | None
    allowas_in_vpnv6: int | None
    allowas_in_evpn: int | None
    attribute_unchanged: str | None
    attribute_unchanged6: str | None
    attribute_unchanged_vpnv4: str | None
    attribute_unchanged_vpnv6: str | None
    activate: str | None
    activate6: str | None
    activate_vpnv4: str | None
    activate_vpnv6: str | None
    activate_evpn: str | None
    bfd: str | None
    capability_dynamic: str | None
    capability_orf: str | None
    capability_orf6: str | None
    capability_graceful_restart: str | None
    capability_graceful_restart6: str | None
    capability_graceful_restart_vpnv4: str | None
    capability_graceful_restart_vpnv6: str | None
    capability_graceful_restart_evpn: str | None
    capability_route_refresh: str | None
    capability_default_originate: str | None
    capability_default_originate6: str | None
    dont_capability_negotiate: str | None
    ebgp_enforce_multihop: str | None
    link_down_failover: str | None
    stale_route: str | None
    next_hop_self: str | None
    next_hop_self6: str | None
    next_hop_self_rr: str | None
    next_hop_self_rr6: str | None
    next_hop_self_vpnv4: str | None
    next_hop_self_vpnv6: str | None
    override_capability: str | None
    passive: str | None
    remove_private_as: str | None
    remove_private_as6: str | None
    remove_private_as_vpnv4: str | None
    remove_private_as_vpnv6: str | None
    remove_private_as_evpn: str | None
    route_reflector_client: str | None
    route_reflector_client6: str | None
    route_reflector_client_vpnv4: str | None
    route_reflector_client_vpnv6: str | None
    route_reflector_client_evpn: str | None
    route_server_client: str | None
    route_server_client6: str | None
    route_server_client_vpnv4: str | None
    route_server_client_vpnv6: str | None
    route_server_client_evpn: str | None
    rr_attr_allow_change: str | None
    rr_attr_allow_change6: str | None
    rr_attr_allow_change_vpnv4: str | None
    rr_attr_allow_change_vpnv6: str | None
    rr_attr_allow_change_evpn: str | None
    shutdown: str | None
    soft_reconfiguration: str | None
    soft_reconfiguration6: str | None
    soft_reconfiguration_vpnv4: str | None
    soft_reconfiguration_vpnv6: str | None
    soft_reconfiguration_evpn: str | None
    as_override: str | None
    as_override6: str | None
    strict_capability_match: str | None
    default_originate_routemap: str | None
    default_originate_routemap6: str | None
    description: str | None
    distribute_list_in: str | None
    distribute_list_in6: str | None
    distribute_list_in_vpnv4: str | None
    distribute_list_in_vpnv6: str | None
    distribute_list_out: str | None
    distribute_list_out6: str | None
    distribute_list_out_vpnv4: str | None
    distribute_list_out_vpnv6: str | None
    ebgp_multihop_ttl: int | None
    filter_list_in: str | None
    filter_list_in6: str | None
    filter_list_in_vpnv4: str | None
    filter_list_in_vpnv6: str | None
    filter_list_out: str | None
    filter_list_out6: str | None
    filter_list_out_vpnv4: str | None
    filter_list_out_vpnv6: str | None
    interface: str | None
    maximum_prefix: int | None
    maximum_prefix6: int | None
    maximum_prefix_vpnv4: int | None
    maximum_prefix_vpnv6: int | None
    maximum_prefix_evpn: int | None
    maximum_prefix_threshold: int | None
    maximum_prefix_threshold6: int | None
    maximum_prefix_threshold_vpnv4: int | None
    maximum_prefix_threshold_vpnv6: int | None
    maximum_prefix_threshold_evpn: int | None
    maximum_prefix_warning_only: str | None
    maximum_prefix_warning_only6: str | None
    maximum_prefix_warning_only_vpnv4: str | None
    maximum_prefix_warning_only_vpnv6: str | None
    maximum_prefix_warning_only_evpn: str | None
    prefix_list_in: str | None
    prefix_list_in6: str | None
    prefix_list_in_vpnv4: str | None
    prefix_list_in_vpnv6: str | None
    prefix_list_out: str | None
    prefix_list_out6: str | None
    prefix_list_out_vpnv4: str | None
    prefix_list_out_vpnv6: str | None
    remote_as: str
    local_as: str | None
    local_as_no_prepend: str | None
    local_as_replace_as: str | None
    retain_stale_time: int | None
    route_map_in: str | None
    route_map_in6: str | None
    route_map_in_vpnv4: str | None
    route_map_in_vpnv6: str | None
    route_map_in_evpn: str | None
    route_map_out: str | None
    route_map_out_preferable: str | None
    route_map_out6: str | None
    route_map_out6_preferable: str | None
    route_map_out_vpnv4: str | None
    route_map_out_vpnv6: str | None
    route_map_out_vpnv4_preferable: str | None
    route_map_out_vpnv6_preferable: str | None
    route_map_out_evpn: str | None
    send_community: str | None
    send_community6: str | None
    send_community_vpnv4: str | None
    send_community_vpnv6: str | None
    send_community_evpn: str | None
    keep_alive_timer: int | None
    holdtime_timer: int | None
    connect_timer: int | None
    unsuppress_map: str | None
    unsuppress_map6: str | None
    update_source: str | None
    weight: int | None
    restart_time: int | None
    additional_path: str | None
    additional_path6: str | None
    additional_path_vpnv4: str | None
    additional_path_vpnv6: str | None
    adv_additional_path: int | None
    adv_additional_path6: int | None
    adv_additional_path_vpnv4: int | None
    adv_additional_path_vpnv6: int | None
    password: str | None
    auth_options: str | None
    conditional_advertise: list[Any] | None
    conditional_advertise6: list[Any] | None


class NeighborGroupObject(FortiObject):
    """Typed FortiObject for neighbor_group child table entry with attribute access."""
    name: str
    advertisement_interval: int | None
    allowas_in_enable: str | None
    allowas_in_enable6: str | None
    allowas_in_enable_vpnv4: str | None
    allowas_in_enable_vpnv6: str | None
    allowas_in_enable_evpn: str | None
    allowas_in: int | None
    allowas_in6: int | None
    allowas_in_vpnv4: int | None
    allowas_in_vpnv6: int | None
    allowas_in_evpn: int | None
    attribute_unchanged: str | None
    attribute_unchanged6: str | None
    attribute_unchanged_vpnv4: str | None
    attribute_unchanged_vpnv6: str | None
    activate: str | None
    activate6: str | None
    activate_vpnv4: str | None
    activate_vpnv6: str | None
    activate_evpn: str | None
    bfd: str | None
    capability_dynamic: str | None
    capability_orf: str | None
    capability_orf6: str | None
    capability_graceful_restart: str | None
    capability_graceful_restart6: str | None
    capability_graceful_restart_vpnv4: str | None
    capability_graceful_restart_vpnv6: str | None
    capability_graceful_restart_evpn: str | None
    capability_route_refresh: str | None
    capability_default_originate: str | None
    capability_default_originate6: str | None
    dont_capability_negotiate: str | None
    ebgp_enforce_multihop: str | None
    link_down_failover: str | None
    stale_route: str | None
    next_hop_self: str | None
    next_hop_self6: str | None
    next_hop_self_rr: str | None
    next_hop_self_rr6: str | None
    next_hop_self_vpnv4: str | None
    next_hop_self_vpnv6: str | None
    override_capability: str | None
    passive: str | None
    remove_private_as: str | None
    remove_private_as6: str | None
    remove_private_as_vpnv4: str | None
    remove_private_as_vpnv6: str | None
    remove_private_as_evpn: str | None
    route_reflector_client: str | None
    route_reflector_client6: str | None
    route_reflector_client_vpnv4: str | None
    route_reflector_client_vpnv6: str | None
    route_reflector_client_evpn: str | None
    route_server_client: str | None
    route_server_client6: str | None
    route_server_client_vpnv4: str | None
    route_server_client_vpnv6: str | None
    route_server_client_evpn: str | None
    rr_attr_allow_change: str | None
    rr_attr_allow_change6: str | None
    rr_attr_allow_change_vpnv4: str | None
    rr_attr_allow_change_vpnv6: str | None
    rr_attr_allow_change_evpn: str | None
    shutdown: str | None
    soft_reconfiguration: str | None
    soft_reconfiguration6: str | None
    soft_reconfiguration_vpnv4: str | None
    soft_reconfiguration_vpnv6: str | None
    soft_reconfiguration_evpn: str | None
    as_override: str | None
    as_override6: str | None
    strict_capability_match: str | None
    default_originate_routemap: str | None
    default_originate_routemap6: str | None
    description: str | None
    distribute_list_in: str | None
    distribute_list_in6: str | None
    distribute_list_in_vpnv4: str | None
    distribute_list_in_vpnv6: str | None
    distribute_list_out: str | None
    distribute_list_out6: str | None
    distribute_list_out_vpnv4: str | None
    distribute_list_out_vpnv6: str | None
    ebgp_multihop_ttl: int | None
    filter_list_in: str | None
    filter_list_in6: str | None
    filter_list_in_vpnv4: str | None
    filter_list_in_vpnv6: str | None
    filter_list_out: str | None
    filter_list_out6: str | None
    filter_list_out_vpnv4: str | None
    filter_list_out_vpnv6: str | None
    interface: str | None
    maximum_prefix: int | None
    maximum_prefix6: int | None
    maximum_prefix_vpnv4: int | None
    maximum_prefix_vpnv6: int | None
    maximum_prefix_evpn: int | None
    maximum_prefix_threshold: int | None
    maximum_prefix_threshold6: int | None
    maximum_prefix_threshold_vpnv4: int | None
    maximum_prefix_threshold_vpnv6: int | None
    maximum_prefix_threshold_evpn: int | None
    maximum_prefix_warning_only: str | None
    maximum_prefix_warning_only6: str | None
    maximum_prefix_warning_only_vpnv4: str | None
    maximum_prefix_warning_only_vpnv6: str | None
    maximum_prefix_warning_only_evpn: str | None
    prefix_list_in: str | None
    prefix_list_in6: str | None
    prefix_list_in_vpnv4: str | None
    prefix_list_in_vpnv6: str | None
    prefix_list_out: str | None
    prefix_list_out6: str | None
    prefix_list_out_vpnv4: str | None
    prefix_list_out_vpnv6: str | None
    remote_as: str
    remote_as_filter: str
    local_as: str | None
    local_as_no_prepend: str | None
    local_as_replace_as: str | None
    retain_stale_time: int | None
    route_map_in: str | None
    route_map_in6: str | None
    route_map_in_vpnv4: str | None
    route_map_in_vpnv6: str | None
    route_map_in_evpn: str | None
    route_map_out: str | None
    route_map_out_preferable: str | None
    route_map_out6: str | None
    route_map_out6_preferable: str | None
    route_map_out_vpnv4: str | None
    route_map_out_vpnv6: str | None
    route_map_out_vpnv4_preferable: str | None
    route_map_out_vpnv6_preferable: str | None
    route_map_out_evpn: str | None
    send_community: str | None
    send_community6: str | None
    send_community_vpnv4: str | None
    send_community_vpnv6: str | None
    send_community_evpn: str | None
    keep_alive_timer: int | None
    holdtime_timer: int | None
    connect_timer: int | None
    unsuppress_map: str | None
    unsuppress_map6: str | None
    update_source: str | None
    weight: int | None
    restart_time: int | None
    additional_path: str | None
    additional_path6: str | None
    additional_path_vpnv4: str | None
    additional_path_vpnv6: str | None
    adv_additional_path: int | None
    adv_additional_path6: int | None
    adv_additional_path_vpnv4: int | None
    adv_additional_path_vpnv6: int | None
    password: str | None
    auth_options: str | None


class NeighborRangeObject(FortiObject):
    """Typed FortiObject for neighbor_range child table entry with attribute access."""
    id: int | None
    prefix: str
    max_neighbor_num: int | None
    neighbor_group: str


class NeighborRange6Object(FortiObject):
    """Typed FortiObject for neighbor_range6 child table entry with attribute access."""
    id: int | None
    prefix6: str
    max_neighbor_num: int | None
    neighbor_group: str


class NetworkObject(FortiObject):
    """Typed FortiObject for network child table entry with attribute access."""
    id: int
    prefix: str
    network_import_check: str | None
    backdoor: str | None
    route_map: str | None
    prefix_name: str | None


class Network6Object(FortiObject):
    """Typed FortiObject for network6 child table entry with attribute access."""
    id: int
    prefix6: str
    network_import_check: str | None
    backdoor: str | None
    route_map: str | None


class RedistributeObject(FortiObject):
    """Typed FortiObject for redistribute child table entry with attribute access."""
    name: str
    status: str | None
    route_map: str | None


class Redistribute6Object(FortiObject):
    """Typed FortiObject for redistribute6 child table entry with attribute access."""
    name: str
    status: str | None
    route_map: str | None


class AdminDistanceObject(FortiObject):
    """Typed FortiObject for admin_distance child table entry with attribute access."""
    id: int
    neighbour_prefix: str
    route_list: str | None
    distance: int


class VrfObject(FortiObject):
    """Typed FortiObject for vrf child table entry with attribute access."""
    vrf: str | None
    role: str | None
    rd: str | None
    export_rt: list[Any] | None
    import_rt: list[Any] | None
    import_route_map: str | None
    leak_target: list[Any] | None


class Vrf6Object(FortiObject):
    """Typed FortiObject for vrf6 child table entry with attribute access."""
    vrf: str | None
    role: str | None
    rd: str | None
    export_rt: list[Any] | None
    import_rt: list[Any] | None
    import_route_map: str | None
    leak_target: list[Any] | None



class ConfederationPeersHelper:
    """Helper class for managing confederation_peers child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        peer: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ConfederationPeersObject] | ConfederationPeersObject | None: ...
    
    def set(
        self,
        peer: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        peer: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        peer: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class AggregateAddressHelper:
    """Helper class for managing aggregate_address child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AggregateAddressObject] | AggregateAddressObject | None: ...
    
    def set(
        self,
        id: int,
        prefix: str,
        as_set: str | None = ...,
        summary_only: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class AggregateAddress6Helper:
    """Helper class for managing aggregate_address6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AggregateAddress6Object] | AggregateAddress6Object | None: ...
    
    def set(
        self,
        id: int,
        prefix6: str,
        as_set: str | None = ...,
        summary_only: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class NeighborHelper:
    """Helper class for managing neighbor child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        ip: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NeighborObject] | NeighborObject | None: ...
    
    def set(
        self,
        ip: str,
        remote_as: str,
        advertisement_interval: int | None = ...,
        allowas_in_enable: str | None = ...,
        allowas_in_enable6: str | None = ...,
        allowas_in_enable_vpnv4: str | None = ...,
        allowas_in_enable_vpnv6: str | None = ...,
        allowas_in_enable_evpn: str | None = ...,
        allowas_in: int | None = ...,
        allowas_in6: int | None = ...,
        allowas_in_vpnv4: int | None = ...,
        allowas_in_vpnv6: int | None = ...,
        allowas_in_evpn: int | None = ...,
        attribute_unchanged: str | None = ...,
        attribute_unchanged6: str | None = ...,
        attribute_unchanged_vpnv4: str | None = ...,
        attribute_unchanged_vpnv6: str | None = ...,
        activate: str | None = ...,
        activate6: str | None = ...,
        activate_vpnv4: str | None = ...,
        activate_vpnv6: str | None = ...,
        activate_evpn: str | None = ...,
        bfd: str | None = ...,
        capability_dynamic: str | None = ...,
        capability_orf: str | None = ...,
        capability_orf6: str | None = ...,
        capability_graceful_restart: str | None = ...,
        capability_graceful_restart6: str | None = ...,
        capability_graceful_restart_vpnv4: str | None = ...,
        capability_graceful_restart_vpnv6: str | None = ...,
        capability_graceful_restart_evpn: str | None = ...,
        capability_route_refresh: str | None = ...,
        capability_default_originate: str | None = ...,
        capability_default_originate6: str | None = ...,
        dont_capability_negotiate: str | None = ...,
        ebgp_enforce_multihop: str | None = ...,
        link_down_failover: str | None = ...,
        stale_route: str | None = ...,
        next_hop_self: str | None = ...,
        next_hop_self6: str | None = ...,
        next_hop_self_rr: str | None = ...,
        next_hop_self_rr6: str | None = ...,
        next_hop_self_vpnv4: str | None = ...,
        next_hop_self_vpnv6: str | None = ...,
        override_capability: str | None = ...,
        passive: str | None = ...,
        remove_private_as: str | None = ...,
        remove_private_as6: str | None = ...,
        remove_private_as_vpnv4: str | None = ...,
        remove_private_as_vpnv6: str | None = ...,
        remove_private_as_evpn: str | None = ...,
        route_reflector_client: str | None = ...,
        route_reflector_client6: str | None = ...,
        route_reflector_client_vpnv4: str | None = ...,
        route_reflector_client_vpnv6: str | None = ...,
        route_reflector_client_evpn: str | None = ...,
        route_server_client: str | None = ...,
        route_server_client6: str | None = ...,
        route_server_client_vpnv4: str | None = ...,
        route_server_client_vpnv6: str | None = ...,
        route_server_client_evpn: str | None = ...,
        rr_attr_allow_change: str | None = ...,
        rr_attr_allow_change6: str | None = ...,
        rr_attr_allow_change_vpnv4: str | None = ...,
        rr_attr_allow_change_vpnv6: str | None = ...,
        rr_attr_allow_change_evpn: str | None = ...,
        shutdown: str | None = ...,
        soft_reconfiguration: str | None = ...,
        soft_reconfiguration6: str | None = ...,
        soft_reconfiguration_vpnv4: str | None = ...,
        soft_reconfiguration_vpnv6: str | None = ...,
        soft_reconfiguration_evpn: str | None = ...,
        as_override: str | None = ...,
        as_override6: str | None = ...,
        strict_capability_match: str | None = ...,
        default_originate_routemap: str | None = ...,
        default_originate_routemap6: str | None = ...,
        description: str | None = ...,
        distribute_list_in: str | None = ...,
        distribute_list_in6: str | None = ...,
        distribute_list_in_vpnv4: str | None = ...,
        distribute_list_in_vpnv6: str | None = ...,
        distribute_list_out: str | None = ...,
        distribute_list_out6: str | None = ...,
        distribute_list_out_vpnv4: str | None = ...,
        distribute_list_out_vpnv6: str | None = ...,
        ebgp_multihop_ttl: int | None = ...,
        filter_list_in: str | None = ...,
        filter_list_in6: str | None = ...,
        filter_list_in_vpnv4: str | None = ...,
        filter_list_in_vpnv6: str | None = ...,
        filter_list_out: str | None = ...,
        filter_list_out6: str | None = ...,
        filter_list_out_vpnv4: str | None = ...,
        filter_list_out_vpnv6: str | None = ...,
        interface: str | None = ...,
        maximum_prefix: int | None = ...,
        maximum_prefix6: int | None = ...,
        maximum_prefix_vpnv4: int | None = ...,
        maximum_prefix_vpnv6: int | None = ...,
        maximum_prefix_evpn: int | None = ...,
        maximum_prefix_threshold: int | None = ...,
        maximum_prefix_threshold6: int | None = ...,
        maximum_prefix_threshold_vpnv4: int | None = ...,
        maximum_prefix_threshold_vpnv6: int | None = ...,
        maximum_prefix_threshold_evpn: int | None = ...,
        maximum_prefix_warning_only: str | None = ...,
        maximum_prefix_warning_only6: str | None = ...,
        maximum_prefix_warning_only_vpnv4: str | None = ...,
        maximum_prefix_warning_only_vpnv6: str | None = ...,
        maximum_prefix_warning_only_evpn: str | None = ...,
        prefix_list_in: str | None = ...,
        prefix_list_in6: str | None = ...,
        prefix_list_in_vpnv4: str | None = ...,
        prefix_list_in_vpnv6: str | None = ...,
        prefix_list_out: str | None = ...,
        prefix_list_out6: str | None = ...,
        prefix_list_out_vpnv4: str | None = ...,
        prefix_list_out_vpnv6: str | None = ...,
        local_as: str | None = ...,
        local_as_no_prepend: str | None = ...,
        local_as_replace_as: str | None = ...,
        retain_stale_time: int | None = ...,
        route_map_in: str | None = ...,
        route_map_in6: str | None = ...,
        route_map_in_vpnv4: str | None = ...,
        route_map_in_vpnv6: str | None = ...,
        route_map_in_evpn: str | None = ...,
        route_map_out: str | None = ...,
        route_map_out_preferable: str | None = ...,
        route_map_out6: str | None = ...,
        route_map_out6_preferable: str | None = ...,
        route_map_out_vpnv4: str | None = ...,
        route_map_out_vpnv6: str | None = ...,
        route_map_out_vpnv4_preferable: str | None = ...,
        route_map_out_vpnv6_preferable: str | None = ...,
        route_map_out_evpn: str | None = ...,
        send_community: str | None = ...,
        send_community6: str | None = ...,
        send_community_vpnv4: str | None = ...,
        send_community_vpnv6: str | None = ...,
        send_community_evpn: str | None = ...,
        keep_alive_timer: int | None = ...,
        holdtime_timer: int | None = ...,
        connect_timer: int | None = ...,
        unsuppress_map: str | None = ...,
        unsuppress_map6: str | None = ...,
        update_source: str | None = ...,
        weight: int | None = ...,
        restart_time: int | None = ...,
        additional_path: str | None = ...,
        additional_path6: str | None = ...,
        additional_path_vpnv4: str | None = ...,
        additional_path_vpnv6: str | None = ...,
        adv_additional_path: int | None = ...,
        adv_additional_path6: int | None = ...,
        adv_additional_path_vpnv4: int | None = ...,
        adv_additional_path_vpnv6: int | None = ...,
        password: str | None = ...,
        auth_options: str | None = ...,
        conditional_advertise: list[Any] | None = ...,
        conditional_advertise6: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        ip: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        ip: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class NeighborGroupHelper:
    """Helper class for managing neighbor_group child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NeighborGroupObject] | NeighborGroupObject | None: ...
    
    def set(
        self,
        name: str,
        remote_as: str,
        remote_as_filter: str,
        advertisement_interval: int | None = ...,
        allowas_in_enable: str | None = ...,
        allowas_in_enable6: str | None = ...,
        allowas_in_enable_vpnv4: str | None = ...,
        allowas_in_enable_vpnv6: str | None = ...,
        allowas_in_enable_evpn: str | None = ...,
        allowas_in: int | None = ...,
        allowas_in6: int | None = ...,
        allowas_in_vpnv4: int | None = ...,
        allowas_in_vpnv6: int | None = ...,
        allowas_in_evpn: int | None = ...,
        attribute_unchanged: str | None = ...,
        attribute_unchanged6: str | None = ...,
        attribute_unchanged_vpnv4: str | None = ...,
        attribute_unchanged_vpnv6: str | None = ...,
        activate: str | None = ...,
        activate6: str | None = ...,
        activate_vpnv4: str | None = ...,
        activate_vpnv6: str | None = ...,
        activate_evpn: str | None = ...,
        bfd: str | None = ...,
        capability_dynamic: str | None = ...,
        capability_orf: str | None = ...,
        capability_orf6: str | None = ...,
        capability_graceful_restart: str | None = ...,
        capability_graceful_restart6: str | None = ...,
        capability_graceful_restart_vpnv4: str | None = ...,
        capability_graceful_restart_vpnv6: str | None = ...,
        capability_graceful_restart_evpn: str | None = ...,
        capability_route_refresh: str | None = ...,
        capability_default_originate: str | None = ...,
        capability_default_originate6: str | None = ...,
        dont_capability_negotiate: str | None = ...,
        ebgp_enforce_multihop: str | None = ...,
        link_down_failover: str | None = ...,
        stale_route: str | None = ...,
        next_hop_self: str | None = ...,
        next_hop_self6: str | None = ...,
        next_hop_self_rr: str | None = ...,
        next_hop_self_rr6: str | None = ...,
        next_hop_self_vpnv4: str | None = ...,
        next_hop_self_vpnv6: str | None = ...,
        override_capability: str | None = ...,
        passive: str | None = ...,
        remove_private_as: str | None = ...,
        remove_private_as6: str | None = ...,
        remove_private_as_vpnv4: str | None = ...,
        remove_private_as_vpnv6: str | None = ...,
        remove_private_as_evpn: str | None = ...,
        route_reflector_client: str | None = ...,
        route_reflector_client6: str | None = ...,
        route_reflector_client_vpnv4: str | None = ...,
        route_reflector_client_vpnv6: str | None = ...,
        route_reflector_client_evpn: str | None = ...,
        route_server_client: str | None = ...,
        route_server_client6: str | None = ...,
        route_server_client_vpnv4: str | None = ...,
        route_server_client_vpnv6: str | None = ...,
        route_server_client_evpn: str | None = ...,
        rr_attr_allow_change: str | None = ...,
        rr_attr_allow_change6: str | None = ...,
        rr_attr_allow_change_vpnv4: str | None = ...,
        rr_attr_allow_change_vpnv6: str | None = ...,
        rr_attr_allow_change_evpn: str | None = ...,
        shutdown: str | None = ...,
        soft_reconfiguration: str | None = ...,
        soft_reconfiguration6: str | None = ...,
        soft_reconfiguration_vpnv4: str | None = ...,
        soft_reconfiguration_vpnv6: str | None = ...,
        soft_reconfiguration_evpn: str | None = ...,
        as_override: str | None = ...,
        as_override6: str | None = ...,
        strict_capability_match: str | None = ...,
        default_originate_routemap: str | None = ...,
        default_originate_routemap6: str | None = ...,
        description: str | None = ...,
        distribute_list_in: str | None = ...,
        distribute_list_in6: str | None = ...,
        distribute_list_in_vpnv4: str | None = ...,
        distribute_list_in_vpnv6: str | None = ...,
        distribute_list_out: str | None = ...,
        distribute_list_out6: str | None = ...,
        distribute_list_out_vpnv4: str | None = ...,
        distribute_list_out_vpnv6: str | None = ...,
        ebgp_multihop_ttl: int | None = ...,
        filter_list_in: str | None = ...,
        filter_list_in6: str | None = ...,
        filter_list_in_vpnv4: str | None = ...,
        filter_list_in_vpnv6: str | None = ...,
        filter_list_out: str | None = ...,
        filter_list_out6: str | None = ...,
        filter_list_out_vpnv4: str | None = ...,
        filter_list_out_vpnv6: str | None = ...,
        interface: str | None = ...,
        maximum_prefix: int | None = ...,
        maximum_prefix6: int | None = ...,
        maximum_prefix_vpnv4: int | None = ...,
        maximum_prefix_vpnv6: int | None = ...,
        maximum_prefix_evpn: int | None = ...,
        maximum_prefix_threshold: int | None = ...,
        maximum_prefix_threshold6: int | None = ...,
        maximum_prefix_threshold_vpnv4: int | None = ...,
        maximum_prefix_threshold_vpnv6: int | None = ...,
        maximum_prefix_threshold_evpn: int | None = ...,
        maximum_prefix_warning_only: str | None = ...,
        maximum_prefix_warning_only6: str | None = ...,
        maximum_prefix_warning_only_vpnv4: str | None = ...,
        maximum_prefix_warning_only_vpnv6: str | None = ...,
        maximum_prefix_warning_only_evpn: str | None = ...,
        prefix_list_in: str | None = ...,
        prefix_list_in6: str | None = ...,
        prefix_list_in_vpnv4: str | None = ...,
        prefix_list_in_vpnv6: str | None = ...,
        prefix_list_out: str | None = ...,
        prefix_list_out6: str | None = ...,
        prefix_list_out_vpnv4: str | None = ...,
        prefix_list_out_vpnv6: str | None = ...,
        local_as: str | None = ...,
        local_as_no_prepend: str | None = ...,
        local_as_replace_as: str | None = ...,
        retain_stale_time: int | None = ...,
        route_map_in: str | None = ...,
        route_map_in6: str | None = ...,
        route_map_in_vpnv4: str | None = ...,
        route_map_in_vpnv6: str | None = ...,
        route_map_in_evpn: str | None = ...,
        route_map_out: str | None = ...,
        route_map_out_preferable: str | None = ...,
        route_map_out6: str | None = ...,
        route_map_out6_preferable: str | None = ...,
        route_map_out_vpnv4: str | None = ...,
        route_map_out_vpnv6: str | None = ...,
        route_map_out_vpnv4_preferable: str | None = ...,
        route_map_out_vpnv6_preferable: str | None = ...,
        route_map_out_evpn: str | None = ...,
        send_community: str | None = ...,
        send_community6: str | None = ...,
        send_community_vpnv4: str | None = ...,
        send_community_vpnv6: str | None = ...,
        send_community_evpn: str | None = ...,
        keep_alive_timer: int | None = ...,
        holdtime_timer: int | None = ...,
        connect_timer: int | None = ...,
        unsuppress_map: str | None = ...,
        unsuppress_map6: str | None = ...,
        update_source: str | None = ...,
        weight: int | None = ...,
        restart_time: int | None = ...,
        additional_path: str | None = ...,
        additional_path6: str | None = ...,
        additional_path_vpnv4: str | None = ...,
        additional_path_vpnv6: str | None = ...,
        adv_additional_path: int | None = ...,
        adv_additional_path6: int | None = ...,
        adv_additional_path_vpnv4: int | None = ...,
        adv_additional_path_vpnv6: int | None = ...,
        password: str | None = ...,
        auth_options: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class NeighborRangeHelper:
    """Helper class for managing neighbor_range child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NeighborRangeObject] | NeighborRangeObject | None: ...
    
    def set(
        self,
        prefix: str,
        neighbor_group: str,
        id: int | None = ...,
        max_neighbor_num: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class NeighborRange6Helper:
    """Helper class for managing neighbor_range6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NeighborRange6Object] | NeighborRange6Object | None: ...
    
    def set(
        self,
        prefix6: str,
        neighbor_group: str,
        id: int | None = ...,
        max_neighbor_num: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class NetworkHelper:
    """Helper class for managing network child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NetworkObject] | NetworkObject | None: ...
    
    def set(
        self,
        id: int,
        prefix: str,
        network_import_check: str | None = ...,
        backdoor: str | None = ...,
        route_map: str | None = ...,
        prefix_name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class Network6Helper:
    """Helper class for managing network6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[Network6Object] | Network6Object | None: ...
    
    def set(
        self,
        id: int,
        prefix6: str,
        network_import_check: str | None = ...,
        backdoor: str | None = ...,
        route_map: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class RedistributeHelper:
    """Helper class for managing redistribute child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[RedistributeObject] | RedistributeObject | None: ...
    
    def set(
        self,
        name: str,
        status: str | None = ...,
        route_map: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class Redistribute6Helper:
    """Helper class for managing redistribute6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[Redistribute6Object] | Redistribute6Object | None: ...
    
    def set(
        self,
        name: str,
        status: str | None = ...,
        route_map: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class AdminDistanceHelper:
    """Helper class for managing admin_distance child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AdminDistanceObject] | AdminDistanceObject | None: ...
    
    def set(
        self,
        id: int,
        neighbour_prefix: str,
        distance: int,
        route_list: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class VrfHelper:
    """Helper class for managing vrf child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        vrf: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[VrfObject] | VrfObject | None: ...
    
    def set(
        self,
        vrf: str | None = ...,
        role: str | None = ...,
        rd: str | None = ...,
        export_rt: list[Any] | None = ...,
        import_rt: list[Any] | None = ...,
        import_route_map: str | None = ...,
        leak_target: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        vrf: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        vrf: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class Vrf6Helper:
    """Helper class for managing vrf6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        vrf: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[Vrf6Object] | Vrf6Object | None: ...
    
    def set(
        self,
        vrf: str | None = ...,
        role: str | None = ...,
        rd: str | None = ...,
        export_rt: list[Any] | None = ...,
        import_rt: list[Any] | None = ...,
        import_route_map: str | None = ...,
        leak_target: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        vrf: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        vrf: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

