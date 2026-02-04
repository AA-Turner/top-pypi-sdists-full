""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/fabric_vpn
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

class FabricVpnOverlaysItem(TypedDict, total=False):
    """Nested item for overlays field."""
    name: str
    ipsec_network_id: int
    overlay_tunnel_block: str
    remote_gw: str
    interface: str
    bgp_neighbor: str
    overlay_policy: int
    bgp_network: int
    route_policy: int
    bgp_neighbor_group: str
    bgp_neighbor_range: int
    ipsec_phase1: str
    sdwan_member: int


class FabricVpnAdvertisedsubnetsItem(TypedDict, total=False):
    """Nested item for advertised-subnets field."""
    id: int
    prefix: str
    access: Literal["inbound", "bidirectional"]
    bgp_network: int
    firewall_address: str
    policies: int | list[int]


class FabricVpnPayload(TypedDict, total=False):
    """Payload type for FabricVpn operations."""
    status: Literal["enable", "disable"]
    sync_mode: Literal["enable", "disable"]
    branch_name: str
    policy_rule: Literal["health-check", "manual", "auto"]
    vpn_role: Literal["hub", "spoke"]
    overlays: str | list[str] | list[FabricVpnOverlaysItem]
    advertised_subnets: str | list[str] | list[FabricVpnAdvertisedsubnetsItem]
    loopback_address_block: str
    loopback_interface: str
    loopback_advertised_subnet: int
    psksecret: str
    bgp_as: str
    sdwan_zone: str
    health_checks: str | list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FabricVpnResponse(TypedDict, total=False):
    """Response type for FabricVpn - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    sync_mode: Literal["enable", "disable"]
    branch_name: str
    policy_rule: Literal["health-check", "manual", "auto"]
    vpn_role: Literal["hub", "spoke"]
    overlays: list[FabricVpnOverlaysItem]
    advertised_subnets: list[FabricVpnAdvertisedsubnetsItem]
    loopback_address_block: str
    loopback_interface: str
    loopback_advertised_subnet: int
    psksecret: str
    bgp_as: str
    sdwan_zone: str
    health_checks: str | list[str]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FabricVpnOverlaysItemObject(FortiObject[FabricVpnOverlaysItem]):
    """Typed object for overlays table items with attribute access."""
    name: str
    ipsec_network_id: int
    overlay_tunnel_block: str
    remote_gw: str
    interface: str
    bgp_neighbor: str
    overlay_policy: int
    bgp_network: int
    route_policy: int
    bgp_neighbor_group: str
    bgp_neighbor_range: int
    ipsec_phase1: str
    sdwan_member: int


class FabricVpnAdvertisedsubnetsItemObject(FortiObject[FabricVpnAdvertisedsubnetsItem]):
    """Typed object for advertised-subnets table items with attribute access."""
    id: int
    prefix: str
    access: Literal["inbound", "bidirectional"]
    bgp_network: int
    firewall_address: str
    policies: int | list[int]


class FabricVpnObject(FortiObject):
    """Typed FortiObject for FabricVpn with field access."""
    status: Literal["enable", "disable"]
    sync_mode: Literal["enable", "disable"]
    branch_name: str
    policy_rule: Literal["health-check", "manual", "auto"]
    vpn_role: Literal["hub", "spoke"]
    overlays: FortiObjectList[FabricVpnOverlaysItemObject]
    advertised_subnets: FortiObjectList[FabricVpnAdvertisedsubnetsItemObject]
    loopback_address_block: str
    loopback_interface: str
    loopback_advertised_subnet: int
    psksecret: str
    bgp_as: str
    sdwan_zone: str
    health_checks: str | list[str]


# ================================================================
# Main Endpoint Class
# ================================================================

class FabricVpn:
    """
    
    Endpoint: system/fabric_vpn
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FabricVpnObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FabricVpnPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        sync_mode: Literal["enable", "disable"] | None = ...,
        branch_name: str | None = ...,
        policy_rule: Literal["health-check", "manual", "auto"] | None = ...,
        vpn_role: Literal["hub", "spoke"] | None = ...,
        overlays: str | list[str] | list[FabricVpnOverlaysItem] | None = ...,
        advertised_subnets: str | list[str] | list[FabricVpnAdvertisedsubnetsItem] | None = ...,
        loopback_address_block: str | None = ...,
        loopback_interface: str | None = ...,
        loopback_advertised_subnet: int | None = ...,
        psksecret: str | None = ...,
        bgp_as: str | None = ...,
        sdwan_zone: str | None = ...,
        health_checks: str | list[str] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FabricVpnObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FabricVpnPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        sync_mode: Literal["enable", "disable"] | None = ...,
        branch_name: str | None = ...,
        policy_rule: Literal["health-check", "manual", "auto"] | None = ...,
        vpn_role: Literal["hub", "spoke"] | None = ...,
        overlays: str | list[str] | list[FabricVpnOverlaysItem] | None = ...,
        advertised_subnets: str | list[str] | list[FabricVpnAdvertisedsubnetsItem] | None = ...,
        loopback_address_block: str | None = ...,
        loopback_interface: str | None = ...,
        loopback_advertised_subnet: int | None = ...,
        psksecret: str | None = ...,
        bgp_as: str | None = ...,
        sdwan_zone: str | None = ...,
        health_checks: str | list[str] | None = ...,
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
    "FabricVpn",
    "FabricVpnPayload",
    "FabricVpnResponse",
    "FabricVpnObject",
]