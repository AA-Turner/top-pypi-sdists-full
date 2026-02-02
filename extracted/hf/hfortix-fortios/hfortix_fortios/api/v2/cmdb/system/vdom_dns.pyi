""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vdom_dns
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

class VdomDnsServerhostnameItem(TypedDict, total=False):
    """Nested item for server-hostname field."""
    hostname: str


class VdomDnsPayload(TypedDict, total=False):
    """Payload type for VdomDns operations."""
    vdom_dns: Literal["enable", "disable"]
    primary: str
    secondary: str
    protocol: str | list[str]
    ssl_certificate: str
    server_hostname: str | list[str] | list[VdomDnsServerhostnameItem]
    ip6_primary: str
    ip6_secondary: str
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_select_method: Literal["least-rtt", "failover"]
    alt_primary: str
    alt_secondary: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VdomDnsResponse(TypedDict, total=False):
    """Response type for VdomDns - use with .dict property for typed dict access."""
    vdom_dns: Literal["enable", "disable"]
    primary: str
    secondary: str
    protocol: str
    ssl_certificate: str
    server_hostname: list[VdomDnsServerhostnameItem]
    ip6_primary: str
    ip6_secondary: str
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_select_method: Literal["least-rtt", "failover"]
    alt_primary: str
    alt_secondary: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VdomDnsServerhostnameItemObject(FortiObject[VdomDnsServerhostnameItem]):
    """Typed object for server-hostname table items with attribute access."""
    hostname: str


class VdomDnsObject(FortiObject):
    """Typed FortiObject for VdomDns with field access."""
    vdom_dns: Literal["enable", "disable"]
    primary: str
    secondary: str
    protocol: str
    ssl_certificate: str
    server_hostname: FortiObjectList[VdomDnsServerhostnameItemObject]
    ip6_primary: str
    ip6_secondary: str
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_select_method: Literal["least-rtt", "failover"]
    alt_primary: str
    alt_secondary: str


# ================================================================
# Main Endpoint Class
# ================================================================

class VdomDns:
    """
    
    Endpoint: system/vdom_dns
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
    ) -> VdomDnsObject: ...
    
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
        payload_dict: VdomDnsPayload | None = ...,
        vdom_dns: Literal["enable", "disable"] | None = ...,
        primary: str | None = ...,
        secondary: str | None = ...,
        protocol: str | list[str] | None = ...,
        ssl_certificate: str | None = ...,
        server_hostname: str | list[str] | list[VdomDnsServerhostnameItem] | None = ...,
        ip6_primary: str | None = ...,
        ip6_secondary: str | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        server_select_method: Literal["least-rtt", "failover"] | None = ...,
        alt_primary: str | None = ...,
        alt_secondary: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VdomDnsObject: ...


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
        payload_dict: VdomDnsPayload | None = ...,
        vdom_dns: Literal["enable", "disable"] | None = ...,
        primary: str | None = ...,
        secondary: str | None = ...,
        protocol: Literal["cleartext", "dot", "doh"] | list[str] | None = ...,
        ssl_certificate: str | None = ...,
        server_hostname: str | list[str] | list[VdomDnsServerhostnameItem] | None = ...,
        ip6_primary: str | None = ...,
        ip6_secondary: str | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        server_select_method: Literal["least-rtt", "failover"] | None = ...,
        alt_primary: str | None = ...,
        alt_secondary: str | None = ...,
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
    "VdomDns",
    "VdomDnsPayload",
    "VdomDnsResponse",
    "VdomDnsObject",
]