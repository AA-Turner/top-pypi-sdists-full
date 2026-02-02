""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/dns
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

class DnsServerhostnameItem(TypedDict, total=False):
    """Nested item for server-hostname field."""
    hostname: str


class DnsDomainItem(TypedDict, total=False):
    """Nested item for domain field."""
    domain: str


class DnsPayload(TypedDict, total=False):
    """Payload type for Dns operations."""
    primary: str
    secondary: str
    protocol: str | list[str]
    ssl_certificate: str
    server_hostname: str | list[str] | list[DnsServerhostnameItem]
    domain: str | list[str] | list[DnsDomainItem]
    ip6_primary: str
    ip6_secondary: str
    timeout: int
    retry: int
    dns_cache_limit: int
    dns_cache_ttl: int
    cache_notfound_responses: Literal["disable", "enable"]
    source_ip: str
    source_ip_interface: str
    root_servers: str | list[str]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_select_method: Literal["least-rtt", "failover"]
    alt_primary: str
    alt_secondary: str
    log: Literal["disable", "error", "all"]
    fqdn_cache_ttl: int
    fqdn_max_refresh: int
    fqdn_min_refresh: int
    hostname_ttl: int
    hostname_limit: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DnsResponse(TypedDict, total=False):
    """Response type for Dns - use with .dict property for typed dict access."""
    primary: str
    secondary: str
    protocol: str
    ssl_certificate: str
    server_hostname: list[DnsServerhostnameItem]
    domain: list[DnsDomainItem]
    ip6_primary: str
    ip6_secondary: str
    timeout: int
    retry: int
    dns_cache_limit: int
    dns_cache_ttl: int
    cache_notfound_responses: Literal["disable", "enable"]
    source_ip: str
    source_ip_interface: str
    root_servers: str | list[str]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_select_method: Literal["least-rtt", "failover"]
    alt_primary: str
    alt_secondary: str
    log: Literal["disable", "error", "all"]
    fqdn_cache_ttl: int
    fqdn_max_refresh: int
    fqdn_min_refresh: int
    hostname_ttl: int
    hostname_limit: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DnsServerhostnameItemObject(FortiObject[DnsServerhostnameItem]):
    """Typed object for server-hostname table items with attribute access."""
    hostname: str


class DnsDomainItemObject(FortiObject[DnsDomainItem]):
    """Typed object for domain table items with attribute access."""
    domain: str


class DnsObject(FortiObject):
    """Typed FortiObject for Dns with field access."""
    primary: str
    secondary: str
    protocol: str
    ssl_certificate: str
    server_hostname: FortiObjectList[DnsServerhostnameItemObject]
    domain: FortiObjectList[DnsDomainItemObject]
    ip6_primary: str
    ip6_secondary: str
    timeout: int
    retry: int
    dns_cache_limit: int
    dns_cache_ttl: int
    cache_notfound_responses: Literal["disable", "enable"]
    source_ip: str
    source_ip_interface: str
    root_servers: str | list[str]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    server_select_method: Literal["least-rtt", "failover"]
    alt_primary: str
    alt_secondary: str
    log: Literal["disable", "error", "all"]
    fqdn_cache_ttl: int
    fqdn_max_refresh: int
    fqdn_min_refresh: int
    hostname_ttl: int
    hostname_limit: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Dns:
    """
    
    Endpoint: system/dns
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
    ) -> DnsObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DnsPayload | None = ...,
        primary: str | None = ...,
        secondary: str | None = ...,
        protocol: str | list[str] | None = ...,
        ssl_certificate: str | None = ...,
        server_hostname: str | list[str] | list[DnsServerhostnameItem] | None = ...,
        domain: str | list[str] | list[DnsDomainItem] | None = ...,
        ip6_primary: str | None = ...,
        ip6_secondary: str | None = ...,
        timeout: int | None = ...,
        retry: int | None = ...,
        dns_cache_limit: int | None = ...,
        dns_cache_ttl: int | None = ...,
        cache_notfound_responses: Literal["disable", "enable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        root_servers: str | list[str] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        server_select_method: Literal["least-rtt", "failover"] | None = ...,
        alt_primary: str | None = ...,
        alt_secondary: str | None = ...,
        log: Literal["disable", "error", "all"] | None = ...,
        fqdn_cache_ttl: int | None = ...,
        fqdn_max_refresh: int | None = ...,
        fqdn_min_refresh: int | None = ...,
        hostname_ttl: int | None = ...,
        hostname_limit: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DnsObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DnsPayload | None = ...,
        primary: str | None = ...,
        secondary: str | None = ...,
        protocol: Literal["cleartext", "dot", "doh"] | list[str] | None = ...,
        ssl_certificate: str | None = ...,
        server_hostname: str | list[str] | list[DnsServerhostnameItem] | None = ...,
        domain: str | list[str] | list[DnsDomainItem] | None = ...,
        ip6_primary: str | None = ...,
        ip6_secondary: str | None = ...,
        timeout: int | None = ...,
        retry: int | None = ...,
        dns_cache_limit: int | None = ...,
        dns_cache_ttl: int | None = ...,
        cache_notfound_responses: Literal["disable", "enable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        root_servers: str | list[str] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        server_select_method: Literal["least-rtt", "failover"] | None = ...,
        alt_primary: str | None = ...,
        alt_secondary: str | None = ...,
        log: Literal["disable", "error", "all"] | None = ...,
        fqdn_cache_ttl: int | None = ...,
        fqdn_max_refresh: int | None = ...,
        fqdn_min_refresh: int | None = ...,
        hostname_ttl: int | None = ...,
        hostname_limit: int | None = ...,
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
    "Dns",
    "DnsPayload",
    "DnsResponse",
    "DnsObject",
]