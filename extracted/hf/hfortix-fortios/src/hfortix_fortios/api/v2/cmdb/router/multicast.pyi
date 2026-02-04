""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/multicast
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

class MulticastPimsmglobalvrfRpaddressItem(TypedDict, total=False):
    """Nested item for pim-sm-global-vrf.rp-address field."""
    id: int
    ip_address: str
    group: str


class MulticastInterfaceJoingroupItem(TypedDict, total=False):
    """Nested item for interface.join-group field."""
    address: str


class MulticastInterfaceIgmpDict(TypedDict, total=False):
    """Nested object type for interface.igmp field."""
    access_group: str
    version: Literal["3", "2", "1"]
    immediate_leave_group: str
    last_member_query_interval: int
    last_member_query_count: int
    query_max_response_time: int
    query_interval: int
    query_timeout: int
    router_alert_check: Literal["enable", "disable"]


class MulticastPimsmglobalRpaddressItem(TypedDict, total=False):
    """Nested item for pim-sm-global.rp-address field."""
    id: int
    ip_address: str
    group: str


class MulticastPimsmglobalDict(TypedDict, total=False):
    """Nested object type for pim-sm-global field."""
    message_interval: int
    join_prune_holdtime: int
    accept_register_list: str
    accept_source_list: str
    bsr_candidate: Literal["enable", "disable"]
    bsr_interface: str
    bsr_priority: int
    bsr_hash: int
    bsr_allow_quick_refresh: Literal["enable", "disable"]
    cisco_crp_prefix: Literal["enable", "disable"]
    cisco_register_checksum: Literal["enable", "disable"]
    cisco_register_checksum_group: str
    cisco_ignore_rp_set_priority: Literal["enable", "disable"]
    register_rp_reachability: Literal["enable", "disable"]
    register_source: Literal["disable", "interface", "ip-address"]
    register_source_interface: str
    register_source_ip: str
    register_supression: int
    null_register_retries: int
    rp_register_keepalive: int
    spt_threshold: Literal["enable", "disable"]
    spt_threshold_group: str
    ssm: Literal["enable", "disable"]
    ssm_range: str
    register_rate_limit: int
    pim_use_sdwan: Literal["enable", "disable"]
    rp_address: str | list[str] | list[MulticastPimsmglobalRpaddressItem]


class MulticastPimsmglobalvrfItem(TypedDict, total=False):
    """Nested item for pim-sm-global-vrf field."""
    vrf: int
    bsr_candidate: Literal["enable", "disable"]
    bsr_interface: str
    bsr_priority: int
    bsr_hash: int
    bsr_allow_quick_refresh: Literal["enable", "disable"]
    cisco_crp_prefix: Literal["enable", "disable"]
    rp_address: str | list[str] | list[MulticastPimsmglobalvrfRpaddressItem]


class MulticastInterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    name: str
    ttl_threshold: int
    pim_mode: Literal["sparse-mode", "dense-mode"]
    passive: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]
    neighbour_filter: str
    hello_interval: int
    hello_holdtime: int
    cisco_exclude_genid: Literal["enable", "disable"]
    dr_priority: int
    propagation_delay: int
    state_refresh_interval: int
    rp_candidate: Literal["enable", "disable"]
    rp_candidate_group: str
    rp_candidate_priority: int
    rp_candidate_interval: int
    multicast_flow: str
    static_group: str
    rpf_nbr_fail_back: Literal["enable", "disable"]
    rpf_nbr_fail_back_filter: str
    join_group: str | list[str] | list[MulticastInterfaceJoingroupItem]
    igmp: MulticastInterfaceIgmpDict


class MulticastPayload(TypedDict, total=False):
    """Payload type for Multicast operations."""
    route_threshold: int
    route_limit: int
    multicast_routing: Literal["enable", "disable"]
    pim_sm_global: MulticastPimsmglobalDict
    pim_sm_global_vrf: str | list[str] | list[MulticastPimsmglobalvrfItem]
    interface: str | list[str] | list[MulticastInterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class MulticastResponse(TypedDict, total=False):
    """Response type for Multicast - use with .dict property for typed dict access."""
    route_threshold: int
    route_limit: int
    multicast_routing: Literal["enable", "disable"]
    pim_sm_global: MulticastPimsmglobalDict
    pim_sm_global_vrf: list[MulticastPimsmglobalvrfItem]
    interface: list[MulticastInterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class MulticastPimsmglobalvrfRpaddressItemObject(FortiObject[MulticastPimsmglobalvrfRpaddressItem]):
    """Typed object for pim-sm-global-vrf.rp-address table items with attribute access."""
    id: int
    ip_address: str
    group: str


class MulticastInterfaceJoingroupItemObject(FortiObject[MulticastInterfaceJoingroupItem]):
    """Typed object for interface.join-group table items with attribute access."""
    address: str


class MulticastPimsmglobalvrfItemObject(FortiObject[MulticastPimsmglobalvrfItem]):
    """Typed object for pim-sm-global-vrf table items with attribute access."""
    vrf: int
    bsr_candidate: Literal["enable", "disable"]
    bsr_interface: str
    bsr_priority: int
    bsr_hash: int
    bsr_allow_quick_refresh: Literal["enable", "disable"]
    cisco_crp_prefix: Literal["enable", "disable"]
    rp_address: FortiObjectList[MulticastPimsmglobalvrfRpaddressItemObject]


class MulticastInterfaceItemObject(FortiObject[MulticastInterfaceItem]):
    """Typed object for interface table items with attribute access."""
    name: str
    ttl_threshold: int
    pim_mode: Literal["sparse-mode", "dense-mode"]
    passive: Literal["enable", "disable"]
    bfd: Literal["enable", "disable"]
    neighbour_filter: str
    hello_interval: int
    hello_holdtime: int
    cisco_exclude_genid: Literal["enable", "disable"]
    dr_priority: int
    propagation_delay: int
    state_refresh_interval: int
    rp_candidate: Literal["enable", "disable"]
    rp_candidate_group: str
    rp_candidate_priority: int
    rp_candidate_interval: int
    multicast_flow: str
    static_group: str
    rpf_nbr_fail_back: Literal["enable", "disable"]
    rpf_nbr_fail_back_filter: str
    join_group: FortiObjectList[MulticastInterfaceJoingroupItemObject]
    igmp: MulticastInterfaceIgmpObject


class MulticastInterfaceIgmpObject(FortiObject):
    """Nested object for interface.igmp field with attribute access."""
    access_group: str
    version: Literal["3", "2", "1"]
    immediate_leave_group: str
    last_member_query_interval: int
    last_member_query_count: int
    query_max_response_time: int
    query_interval: int
    query_timeout: int
    router_alert_check: Literal["enable", "disable"]


class MulticastPimsmglobalRpaddressItemObject(FortiObject[MulticastPimsmglobalRpaddressItem]):
    """Typed object for pim-sm-global.rp-address table items with attribute access."""
    id: int
    ip_address: str
    group: str


class MulticastPimsmglobalObject(FortiObject):
    """Nested object for pim-sm-global field with attribute access."""
    message_interval: int
    join_prune_holdtime: int
    accept_register_list: str
    accept_source_list: str
    bsr_candidate: Literal["enable", "disable"]
    bsr_interface: str
    bsr_priority: int
    bsr_hash: int
    bsr_allow_quick_refresh: Literal["enable", "disable"]
    cisco_crp_prefix: Literal["enable", "disable"]
    cisco_register_checksum: Literal["enable", "disable"]
    cisco_register_checksum_group: str
    cisco_ignore_rp_set_priority: Literal["enable", "disable"]
    register_rp_reachability: Literal["enable", "disable"]
    register_source: Literal["disable", "interface", "ip-address"]
    register_source_interface: str
    register_source_ip: str
    register_supression: int
    null_register_retries: int
    rp_register_keepalive: int
    spt_threshold: Literal["enable", "disable"]
    spt_threshold_group: str
    ssm: Literal["enable", "disable"]
    ssm_range: str
    register_rate_limit: int
    pim_use_sdwan: Literal["enable", "disable"]
    rp_address: str | list[str]


class MulticastObject(FortiObject):
    """Typed FortiObject for Multicast with field access."""
    route_threshold: int
    route_limit: int
    multicast_routing: Literal["enable", "disable"]
    pim_sm_global: MulticastPimsmglobalObject
    pim_sm_global_vrf: FortiObjectList[MulticastPimsmglobalvrfItemObject]
    interface: FortiObjectList[MulticastInterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Multicast:
    """
    
    Endpoint: router/multicast
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
    ) -> MulticastObject: ...
    
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
        payload_dict: MulticastPayload | None = ...,
        route_threshold: int | None = ...,
        route_limit: int | None = ...,
        multicast_routing: Literal["enable", "disable"] | None = ...,
        pim_sm_global: MulticastPimsmglobalDict | None = ...,
        pim_sm_global_vrf: str | list[str] | list[MulticastPimsmglobalvrfItem] | None = ...,
        interface: str | list[str] | list[MulticastInterfaceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastObject: ...


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
        payload_dict: MulticastPayload | None = ...,
        route_threshold: int | None = ...,
        route_limit: int | None = ...,
        multicast_routing: Literal["enable", "disable"] | None = ...,
        pim_sm_global: MulticastPimsmglobalDict | None = ...,
        pim_sm_global_vrf: str | list[str] | list[MulticastPimsmglobalvrfItem] | None = ...,
        interface: str | list[str] | list[MulticastInterfaceItem] | None = ...,
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
    "Multicast",
    "MulticastPayload",
    "MulticastResponse",
    "MulticastObject",
]