"""
Child Table Helper Type Stubs for router/multicast

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class PimSmGlobalVrfDict(TypedDict, total=False):
    """Type definition for pim_sm_global_vrf child table entry."""
    vrf: int | None
    bsr_candidate: str | None
    bsr_interface: str | None
    bsr_priority: int | None
    bsr_hash: int | None
    bsr_allow_quick_refresh: str | None
    cisco_crp_prefix: str | None
    rp_address: list[Any] | None

class InterfaceDict(TypedDict, total=False):
    """Type definition for interface child table entry."""
    name: str | None
    ttl_threshold: int | None
    pim_mode: str | None
    passive: str | None
    bfd: str | None
    neighbour_filter: str | None
    hello_interval: int | None
    hello_holdtime: int | None
    cisco_exclude_genid: str | None
    dr_priority: int | None
    propagation_delay: int | None
    state_refresh_interval: int | None
    rp_candidate: str | None
    rp_candidate_group: str | None
    rp_candidate_priority: int | None
    rp_candidate_interval: int | None
    multicast_flow: str | None
    static_group: str | None
    rpf_nbr_fail_back: str | None
    rpf_nbr_fail_back_filter: str | None
    join_group: list[Any] | None
    igmp: dict[str, Any] | None


class PimSmGlobalVrfObject(FortiObject):
    """Typed FortiObject for pim_sm_global_vrf child table entry with attribute access."""
    vrf: int | None
    bsr_candidate: str | None
    bsr_interface: str | None
    bsr_priority: int | None
    bsr_hash: int | None
    bsr_allow_quick_refresh: str | None
    cisco_crp_prefix: str | None
    rp_address: list[Any] | None


class InterfaceObject(FortiObject):
    """Typed FortiObject for interface child table entry with attribute access."""
    name: str | None
    ttl_threshold: int | None
    pim_mode: str | None
    passive: str | None
    bfd: str | None
    neighbour_filter: str | None
    hello_interval: int | None
    hello_holdtime: int | None
    cisco_exclude_genid: str | None
    dr_priority: int | None
    propagation_delay: int | None
    state_refresh_interval: int | None
    rp_candidate: str | None
    rp_candidate_group: str | None
    rp_candidate_priority: int | None
    rp_candidate_interval: int | None
    multicast_flow: str | None
    static_group: str | None
    rpf_nbr_fail_back: str | None
    rpf_nbr_fail_back_filter: str | None
    join_group: list[Any] | None
    igmp: dict[str, Any] | None



class PimSmGlobalVrfHelper:
    """Helper class for managing pim_sm_global_vrf child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        vrf: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[PimSmGlobalVrfObject] | PimSmGlobalVrfObject | None: ...
    
    def set(
        self,
        vrf: int | None = ...,
        bsr_candidate: str | None = ...,
        bsr_interface: str | None = ...,
        bsr_priority: int | None = ...,
        bsr_hash: int | None = ...,
        bsr_allow_quick_refresh: str | None = ...,
        cisco_crp_prefix: str | None = ...,
        rp_address: list[Any] | None = ...,
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


class InterfaceHelper:
    """Helper class for managing interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[InterfaceObject] | InterfaceObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        ttl_threshold: int | None = ...,
        pim_mode: str | None = ...,
        passive: str | None = ...,
        bfd: str | None = ...,
        neighbour_filter: str | None = ...,
        hello_interval: int | None = ...,
        hello_holdtime: int | None = ...,
        cisco_exclude_genid: str | None = ...,
        dr_priority: int | None = ...,
        propagation_delay: int | None = ...,
        state_refresh_interval: int | None = ...,
        rp_candidate: str | None = ...,
        rp_candidate_group: str | None = ...,
        rp_candidate_priority: int | None = ...,
        rp_candidate_interval: int | None = ...,
        multicast_flow: str | None = ...,
        static_group: str | None = ...,
        rpf_nbr_fail_back: str | None = ...,
        rpf_nbr_fail_back_filter: str | None = ...,
        join_group: list[Any] | None = ...,
        igmp: dict[str, Any] | None = ...,
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

