""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/ospf
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

class OspfAreaRangeItem(TypedDict, total=False):
    """Nested item for area.range field."""
    id: int
    prefix: str
    advertise: Literal["disable", "enable"]
    substitute: str
    substitute_status: Literal["enable", "disable"]


class OspfAreaVirtuallinkItem(TypedDict, total=False):
    """Nested item for area.virtual-link field."""
    name: str
    authentication: Literal["none", "text", "message-digest"]
    authentication_key: str
    keychain: str
    dead_interval: int
    hello_interval: int
    retransmit_interval: int
    transmit_delay: int
    peer: str
    md5_keys: str | list[str]


class OspfAreaFilterlistItem(TypedDict, total=False):
    """Nested item for area.filter-list field."""
    id: int
    list: str
    direction: Literal["in", "out"]


class OspfOspfinterfaceMd5keysItem(TypedDict, total=False):
    """Nested item for ospf-interface.md5-keys field."""
    id: int
    key_string: str


class OspfAreaItem(TypedDict, total=False):
    """Nested item for area field."""
    id: str
    shortcut: Literal["disable", "enable", "default"]
    authentication: Literal["none", "text", "message-digest"]
    default_cost: int
    nssa_translator_role: Literal["candidate", "never", "always"]
    stub_type: Literal["no-summary", "summary"]
    type: Literal["regular", "nssa", "stub"]
    nssa_default_information_originate: Literal["enable", "always", "disable"]
    nssa_default_information_originate_metric: int
    nssa_default_information_originate_metric_type: Literal["1", "2"]
    nssa_redistribution: Literal["enable", "disable"]
    comments: str
    range: str | list[str] | list[OspfAreaRangeItem]
    virtual_link: str | list[str] | list[OspfAreaVirtuallinkItem]
    filter_list: str | list[str] | list[OspfAreaFilterlistItem]


class OspfOspfinterfaceItem(TypedDict, total=False):
    """Nested item for ospf-interface field."""
    name: str
    comments: str
    interface: str
    ip: str
    linkdown_fast_failover: Literal["enable", "disable"]
    authentication: Literal["none", "text", "message-digest"]
    authentication_key: str
    keychain: str
    prefix_length: int
    retransmit_interval: int
    transmit_delay: int
    cost: int
    priority: int
    dead_interval: int
    hello_interval: int
    hello_multiplier: int
    database_filter_out: Literal["enable", "disable"]
    mtu: int
    mtu_ignore: Literal["enable", "disable"]
    network_type: Literal["broadcast", "non-broadcast", "point-to-point", "point-to-multipoint", "point-to-multipoint-non-broadcast"]
    bfd: Literal["global", "enable", "disable"]
    status: Literal["disable", "enable"]
    resync_timeout: int
    md5_keys: str | list[str] | list[OspfOspfinterfaceMd5keysItem]


class OspfNetworkItem(TypedDict, total=False):
    """Nested item for network field."""
    id: int
    prefix: str
    area: str
    comments: str


class OspfNeighborItem(TypedDict, total=False):
    """Nested item for neighbor field."""
    id: int
    ip: str
    poll_interval: int
    cost: int
    priority: int


class OspfPassiveinterfaceItem(TypedDict, total=False):
    """Nested item for passive-interface field."""
    name: str


class OspfSummaryaddressItem(TypedDict, total=False):
    """Nested item for summary-address field."""
    id: int
    prefix: str
    tag: int
    advertise: Literal["disable", "enable"]


class OspfDistributelistItem(TypedDict, total=False):
    """Nested item for distribute-list field."""
    id: int
    access_list: str
    protocol: Literal["connected", "static", "rip"]


class OspfRedistributeItem(TypedDict, total=False):
    """Nested item for redistribute field."""
    name: str
    status: Literal["enable", "disable"]
    metric: int
    routemap: str
    metric_type: Literal["1", "2"]
    tag: int


class OspfPayload(TypedDict, total=False):
    """Payload type for Ospf operations."""
    abr_type: Literal["cisco", "ibm", "shortcut", "standard"]
    auto_cost_ref_bandwidth: int
    distance_external: int
    distance_inter_area: int
    distance_intra_area: int
    database_overflow: Literal["enable", "disable"]
    database_overflow_max_lsas: int
    database_overflow_time_to_recover: int
    default_information_originate: Literal["enable", "always", "disable"]
    default_information_metric: int
    default_information_metric_type: Literal["1", "2"]
    default_information_route_map: str
    default_metric: int
    distance: int
    lsa_refresh_interval: int
    rfc1583_compatible: Literal["enable", "disable"]
    router_id: str
    spf_timers: str
    bfd: Literal["enable", "disable"]
    log_neighbour_changes: Literal["enable", "disable"]
    distribute_list_in: str
    distribute_route_map_in: str
    restart_mode: Literal["none", "lls", "graceful-restart"]
    restart_period: int
    restart_on_topology_change: Literal["enable", "disable"]
    area: str | list[str] | list[OspfAreaItem]
    ospf_interface: str | list[str] | list[OspfOspfinterfaceItem]
    network: str | list[str] | list[OspfNetworkItem]
    neighbor: str | list[str] | list[OspfNeighborItem]
    passive_interface: str | list[str] | list[OspfPassiveinterfaceItem]
    summary_address: str | list[str] | list[OspfSummaryaddressItem]
    distribute_list: str | list[str] | list[OspfDistributelistItem]
    redistribute: str | list[str] | list[OspfRedistributeItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class OspfResponse(TypedDict, total=False):
    """Response type for Ospf - use with .dict property for typed dict access."""
    abr_type: Literal["cisco", "ibm", "shortcut", "standard"]
    auto_cost_ref_bandwidth: int
    distance_external: int
    distance_inter_area: int
    distance_intra_area: int
    database_overflow: Literal["enable", "disable"]
    database_overflow_max_lsas: int
    database_overflow_time_to_recover: int
    default_information_originate: Literal["enable", "always", "disable"]
    default_information_metric: int
    default_information_metric_type: Literal["1", "2"]
    default_information_route_map: str
    default_metric: int
    distance: int
    lsa_refresh_interval: int
    rfc1583_compatible: Literal["enable", "disable"]
    router_id: str
    spf_timers: str
    bfd: Literal["enable", "disable"]
    log_neighbour_changes: Literal["enable", "disable"]
    distribute_list_in: str
    distribute_route_map_in: str
    restart_mode: Literal["none", "lls", "graceful-restart"]
    restart_period: int
    restart_on_topology_change: Literal["enable", "disable"]
    area: list[OspfAreaItem]
    ospf_interface: list[OspfOspfinterfaceItem]
    network: list[OspfNetworkItem]
    neighbor: list[OspfNeighborItem]
    passive_interface: list[OspfPassiveinterfaceItem]
    summary_address: list[OspfSummaryaddressItem]
    distribute_list: list[OspfDistributelistItem]
    redistribute: list[OspfRedistributeItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class OspfAreaRangeItemObject(FortiObject[OspfAreaRangeItem]):
    """Typed object for area.range table items with attribute access."""
    id: int
    prefix: str
    advertise: Literal["disable", "enable"]
    substitute: str
    substitute_status: Literal["enable", "disable"]


class OspfAreaVirtuallinkItemObject(FortiObject[OspfAreaVirtuallinkItem]):
    """Typed object for area.virtual-link table items with attribute access."""
    name: str
    authentication: Literal["none", "text", "message-digest"]
    authentication_key: str
    keychain: str
    dead_interval: int
    hello_interval: int
    retransmit_interval: int
    transmit_delay: int
    peer: str
    md5_keys: str | list[str]


class OspfAreaFilterlistItemObject(FortiObject[OspfAreaFilterlistItem]):
    """Typed object for area.filter-list table items with attribute access."""
    id: int
    list: str
    direction: Literal["in", "out"]


class OspfOspfinterfaceMd5keysItemObject(FortiObject[OspfOspfinterfaceMd5keysItem]):
    """Typed object for ospf-interface.md5-keys table items with attribute access."""
    id: int
    key_string: str


class OspfAreaItemObject(FortiObject[OspfAreaItem]):
    """Typed object for area table items with attribute access."""
    id: str
    shortcut: Literal["disable", "enable", "default"]
    authentication: Literal["none", "text", "message-digest"]
    default_cost: int
    nssa_translator_role: Literal["candidate", "never", "always"]
    stub_type: Literal["no-summary", "summary"]
    type: Literal["regular", "nssa", "stub"]
    nssa_default_information_originate: Literal["enable", "always", "disable"]
    nssa_default_information_originate_metric: int
    nssa_default_information_originate_metric_type: Literal["1", "2"]
    nssa_redistribution: Literal["enable", "disable"]
    comments: str
    range: FortiObjectList[OspfAreaRangeItemObject]
    virtual_link: FortiObjectList[OspfAreaVirtuallinkItemObject]
    filter_list: FortiObjectList[OspfAreaFilterlistItemObject]


class OspfOspfinterfaceItemObject(FortiObject[OspfOspfinterfaceItem]):
    """Typed object for ospf-interface table items with attribute access."""
    name: str
    comments: str
    interface: str
    ip: str
    linkdown_fast_failover: Literal["enable", "disable"]
    authentication: Literal["none", "text", "message-digest"]
    authentication_key: str
    keychain: str
    prefix_length: int
    retransmit_interval: int
    transmit_delay: int
    cost: int
    priority: int
    dead_interval: int
    hello_interval: int
    hello_multiplier: int
    database_filter_out: Literal["enable", "disable"]
    mtu: int
    mtu_ignore: Literal["enable", "disable"]
    network_type: Literal["broadcast", "non-broadcast", "point-to-point", "point-to-multipoint", "point-to-multipoint-non-broadcast"]
    bfd: Literal["global", "enable", "disable"]
    status: Literal["disable", "enable"]
    resync_timeout: int
    md5_keys: FortiObjectList[OspfOspfinterfaceMd5keysItemObject]


class OspfNetworkItemObject(FortiObject[OspfNetworkItem]):
    """Typed object for network table items with attribute access."""
    id: int
    prefix: str
    area: str
    comments: str


class OspfNeighborItemObject(FortiObject[OspfNeighborItem]):
    """Typed object for neighbor table items with attribute access."""
    id: int
    ip: str
    poll_interval: int
    cost: int
    priority: int


class OspfPassiveinterfaceItemObject(FortiObject[OspfPassiveinterfaceItem]):
    """Typed object for passive-interface table items with attribute access."""
    name: str


class OspfSummaryaddressItemObject(FortiObject[OspfSummaryaddressItem]):
    """Typed object for summary-address table items with attribute access."""
    id: int
    prefix: str
    tag: int
    advertise: Literal["disable", "enable"]


class OspfDistributelistItemObject(FortiObject[OspfDistributelistItem]):
    """Typed object for distribute-list table items with attribute access."""
    id: int
    access_list: str
    protocol: Literal["connected", "static", "rip"]


class OspfRedistributeItemObject(FortiObject[OspfRedistributeItem]):
    """Typed object for redistribute table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    metric: int
    routemap: str
    metric_type: Literal["1", "2"]
    tag: int


class OspfObject(FortiObject):
    """Typed FortiObject for Ospf with field access."""
    abr_type: Literal["cisco", "ibm", "shortcut", "standard"]
    auto_cost_ref_bandwidth: int
    distance_external: int
    distance_inter_area: int
    distance_intra_area: int
    database_overflow: Literal["enable", "disable"]
    database_overflow_max_lsas: int
    database_overflow_time_to_recover: int
    default_information_originate: Literal["enable", "always", "disable"]
    default_information_metric: int
    default_information_metric_type: Literal["1", "2"]
    default_information_route_map: str
    default_metric: int
    distance: int
    lsa_refresh_interval: int
    rfc1583_compatible: Literal["enable", "disable"]
    router_id: str
    spf_timers: str
    bfd: Literal["enable", "disable"]
    log_neighbour_changes: Literal["enable", "disable"]
    distribute_list_in: str
    distribute_route_map_in: str
    restart_mode: Literal["none", "lls", "graceful-restart"]
    restart_period: int
    restart_on_topology_change: Literal["enable", "disable"]
    area: FortiObjectList[OspfAreaItemObject]
    ospf_interface: FortiObjectList[OspfOspfinterfaceItemObject]
    network: FortiObjectList[OspfNetworkItemObject]
    neighbor: FortiObjectList[OspfNeighborItemObject]
    passive_interface: FortiObjectList[OspfPassiveinterfaceItemObject]
    summary_address: FortiObjectList[OspfSummaryaddressItemObject]
    distribute_list: FortiObjectList[OspfDistributelistItemObject]
    redistribute: FortiObjectList[OspfRedistributeItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ospf:
    """
    
    Endpoint: router/ospf
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
    ) -> OspfObject: ...
    
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
        payload_dict: OspfPayload | None = ...,
        abr_type: Literal["cisco", "ibm", "shortcut", "standard"] | None = ...,
        auto_cost_ref_bandwidth: int | None = ...,
        distance_external: int | None = ...,
        distance_inter_area: int | None = ...,
        distance_intra_area: int | None = ...,
        database_overflow: Literal["enable", "disable"] | None = ...,
        database_overflow_max_lsas: int | None = ...,
        database_overflow_time_to_recover: int | None = ...,
        default_information_originate: Literal["enable", "always", "disable"] | None = ...,
        default_information_metric: int | None = ...,
        default_information_metric_type: Literal["1", "2"] | None = ...,
        default_information_route_map: str | None = ...,
        default_metric: int | None = ...,
        distance: int | None = ...,
        lsa_refresh_interval: int | None = ...,
        rfc1583_compatible: Literal["enable", "disable"] | None = ...,
        router_id: str | None = ...,
        spf_timers: str | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        log_neighbour_changes: Literal["enable", "disable"] | None = ...,
        distribute_list_in: str | None = ...,
        distribute_route_map_in: str | None = ...,
        restart_mode: Literal["none", "lls", "graceful-restart"] | None = ...,
        restart_period: int | None = ...,
        restart_on_topology_change: Literal["enable", "disable"] | None = ...,
        area: str | list[str] | list[OspfAreaItem] | None = ...,
        ospf_interface: str | list[str] | list[OspfOspfinterfaceItem] | None = ...,
        network: str | list[str] | list[OspfNetworkItem] | None = ...,
        neighbor: str | list[str] | list[OspfNeighborItem] | None = ...,
        passive_interface: str | list[str] | list[OspfPassiveinterfaceItem] | None = ...,
        summary_address: str | list[str] | list[OspfSummaryaddressItem] | None = ...,
        distribute_list: str | list[str] | list[OspfDistributelistItem] | None = ...,
        redistribute: str | list[str] | list[OspfRedistributeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> OspfObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


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
        payload_dict: OspfPayload | None = ...,
        abr_type: Literal["cisco", "ibm", "shortcut", "standard"] | None = ...,
        auto_cost_ref_bandwidth: int | None = ...,
        distance_external: int | None = ...,
        distance_inter_area: int | None = ...,
        distance_intra_area: int | None = ...,
        database_overflow: Literal["enable", "disable"] | None = ...,
        database_overflow_max_lsas: int | None = ...,
        database_overflow_time_to_recover: int | None = ...,
        default_information_originate: Literal["enable", "always", "disable"] | None = ...,
        default_information_metric: int | None = ...,
        default_information_metric_type: Literal["1", "2"] | None = ...,
        default_information_route_map: str | None = ...,
        default_metric: int | None = ...,
        distance: int | None = ...,
        lsa_refresh_interval: int | None = ...,
        rfc1583_compatible: Literal["enable", "disable"] | None = ...,
        router_id: str | None = ...,
        spf_timers: str | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        log_neighbour_changes: Literal["enable", "disable"] | None = ...,
        distribute_list_in: str | None = ...,
        distribute_route_map_in: str | None = ...,
        restart_mode: Literal["none", "lls", "graceful-restart"] | None = ...,
        restart_period: int | None = ...,
        restart_on_topology_change: Literal["enable", "disable"] | None = ...,
        area: str | list[str] | list[OspfAreaItem] | None = ...,
        ospf_interface: str | list[str] | list[OspfOspfinterfaceItem] | None = ...,
        network: str | list[str] | list[OspfNetworkItem] | None = ...,
        neighbor: str | list[str] | list[OspfNeighborItem] | None = ...,
        passive_interface: str | list[str] | list[OspfPassiveinterfaceItem] | None = ...,
        summary_address: str | list[str] | list[OspfSummaryaddressItem] | None = ...,
        distribute_list: str | list[str] | list[OspfDistributelistItem] | None = ...,
        redistribute: str | list[str] | list[OspfRedistributeItem] | None = ...,
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
    "Ospf",
    "OspfPayload",
    "OspfResponse",
    "OspfObject",
]