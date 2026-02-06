"""
Child Table Helper Type Stubs for system/fabric-vpn

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class OverlaysDict(TypedDict, total=False):
    """Type definition for overlays child table entry."""
    name: str
    ipsec_network_id: int | None
    overlay_tunnel_block: str | None
    remote_gw: str | None
    interface: str | None
    bgp_neighbor: str | None
    overlay_policy: int | None
    bgp_network: int | None
    route_policy: int | None
    bgp_neighbor_group: str | None
    bgp_neighbor_range: int | None
    ipsec_phase1: str | None
    sdwan_member: int | None

class AdvertisedSubnetsDict(TypedDict, total=False):
    """Type definition for advertised_subnets child table entry."""
    id: int | None
    prefix: str
    access: str
    bgp_network: int | None
    firewall_address: str | None
    policies: int | None


class OverlaysObject(FortiObject):
    """Typed FortiObject for overlays child table entry with attribute access."""
    name: str
    ipsec_network_id: int | None
    overlay_tunnel_block: str | None
    remote_gw: str | None
    interface: str | None
    bgp_neighbor: str | None
    overlay_policy: int | None
    bgp_network: int | None
    route_policy: int | None
    bgp_neighbor_group: str | None
    bgp_neighbor_range: int | None
    ipsec_phase1: str | None
    sdwan_member: int | None


class AdvertisedSubnetsObject(FortiObject):
    """Typed FortiObject for advertised_subnets child table entry with attribute access."""
    id: int | None
    prefix: str
    access: str
    bgp_network: int | None
    firewall_address: str | None
    policies: int | None



class OverlaysHelper:
    """Helper class for managing overlays child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[OverlaysObject] | OverlaysObject | None: ...
    
    def set(
        self,
        name: str,
        ipsec_network_id: int | None = ...,
        overlay_tunnel_block: str | None = ...,
        remote_gw: str | None = ...,
        interface: str | None = ...,
        bgp_neighbor: str | None = ...,
        overlay_policy: int | None = ...,
        bgp_network: int | None = ...,
        route_policy: int | None = ...,
        bgp_neighbor_group: str | None = ...,
        bgp_neighbor_range: int | None = ...,
        ipsec_phase1: str | None = ...,
        sdwan_member: int | None = ...,
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


class AdvertisedSubnetsHelper:
    """Helper class for managing advertised_subnets child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AdvertisedSubnetsObject] | AdvertisedSubnetsObject | None: ...
    
    def set(
        self,
        prefix: str,
        access: str,
        id: int | None = ...,
        bgp_network: int | None = ...,
        firewall_address: str | None = ...,
        policies: int | None = ...,
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

