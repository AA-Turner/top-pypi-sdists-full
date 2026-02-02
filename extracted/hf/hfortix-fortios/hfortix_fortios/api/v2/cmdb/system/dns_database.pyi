""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/dns_database
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class DnsDatabaseDnsentryItem(TypedDict, total=False):
    """Nested item for dns-entry field."""
    id: int
    status: Literal["enable", "disable"]
    type: Literal["A", "NS", "CNAME", "MX", "AAAA", "PTR", "PTR_V6"]
    ttl: int
    preference: int
    ip: str
    ipv6: str
    hostname: str
    canonical_name: str


class DnsDatabasePayload(TypedDict, total=False):
    """Payload type for DnsDatabase operations."""
    name: str
    status: Literal["enable", "disable"]
    domain: str
    allow_transfer: str | list[str]
    type: Literal["primary", "secondary"]
    view: Literal["shadow", "public", "shadow-ztna", "proxy"]
    ip_primary: str
    primary_name: str
    contact: str
    ttl: int
    authoritative: Literal["enable", "disable"]
    forwarder: str | list[str]
    forwarder6: str
    source_ip: str
    source_ip6: str
    source_ip_interface: str
    rr_max: int
    dns_entry: str | list[str] | list[DnsDatabaseDnsentryItem]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DnsDatabaseResponse(TypedDict, total=False):
    """Response type for DnsDatabase - use with .dict property for typed dict access."""
    name: str
    status: Literal["enable", "disable"]
    domain: str
    allow_transfer: str | list[str]
    type: Literal["primary", "secondary"]
    view: Literal["shadow", "public", "shadow-ztna", "proxy"]
    ip_primary: str
    primary_name: str
    contact: str
    ttl: int
    authoritative: Literal["enable", "disable"]
    forwarder: str | list[str]
    forwarder6: str
    source_ip: str
    source_ip6: str
    source_ip_interface: str
    rr_max: int
    dns_entry: list[DnsDatabaseDnsentryItem]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DnsDatabaseDnsentryItemObject(FortiObject[DnsDatabaseDnsentryItem]):
    """Typed object for dns-entry table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    type: Literal["A", "NS", "CNAME", "MX", "AAAA", "PTR", "PTR_V6"]
    ttl: int
    preference: int
    ip: str
    ipv6: str
    hostname: str
    canonical_name: str


class DnsDatabaseObject(FortiObject):
    """Typed FortiObject for DnsDatabase with field access."""
    name: str
    status: Literal["enable", "disable"]
    domain: str
    allow_transfer: str | list[str]
    type: Literal["primary", "secondary"]
    view: Literal["shadow", "public", "shadow-ztna", "proxy"]
    ip_primary: str
    primary_name: str
    contact: str
    ttl: int
    authoritative: Literal["enable", "disable"]
    forwarder: str | list[str]
    forwarder6: str
    source_ip: str
    source_ip6: str
    source_ip_interface: str
    rr_max: int
    dns_entry: FortiObjectList[DnsDatabaseDnsentryItemObject]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class DnsDatabase:
    """
    
    Endpoint: system/dns_database
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
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
    ) -> DnsDatabaseObject: ...
    
    @overload
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
    ) -> FortiObjectList[DnsDatabaseObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: DnsDatabasePayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        domain: str | None = ...,
        allow_transfer: str | list[str] | None = ...,
        type: Literal["primary", "secondary"] | None = ...,
        view: Literal["shadow", "public", "shadow-ztna", "proxy"] | None = ...,
        ip_primary: str | None = ...,
        primary_name: str | None = ...,
        contact: str | None = ...,
        ttl: int | None = ...,
        authoritative: Literal["enable", "disable"] | None = ...,
        forwarder: str | list[str] | None = ...,
        forwarder6: str | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        source_ip_interface: str | None = ...,
        rr_max: int | None = ...,
        dns_entry: str | list[str] | list[DnsDatabaseDnsentryItem] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DnsDatabaseObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DnsDatabasePayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        domain: str | None = ...,
        allow_transfer: str | list[str] | None = ...,
        type: Literal["primary", "secondary"] | None = ...,
        view: Literal["shadow", "public", "shadow-ztna", "proxy"] | None = ...,
        ip_primary: str | None = ...,
        primary_name: str | None = ...,
        contact: str | None = ...,
        ttl: int | None = ...,
        authoritative: Literal["enable", "disable"] | None = ...,
        forwarder: str | list[str] | None = ...,
        forwarder6: str | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        source_ip_interface: str | None = ...,
        rr_max: int | None = ...,
        dns_entry: str | list[str] | list[DnsDatabaseDnsentryItem] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DnsDatabaseObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
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
        payload_dict: DnsDatabasePayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        domain: str | None = ...,
        allow_transfer: str | list[str] | None = ...,
        type: Literal["primary", "secondary"] | None = ...,
        view: Literal["shadow", "public", "shadow-ztna", "proxy"] | None = ...,
        ip_primary: str | None = ...,
        primary_name: str | None = ...,
        contact: str | None = ...,
        ttl: int | None = ...,
        authoritative: Literal["enable", "disable"] | None = ...,
        forwarder: str | list[str] | None = ...,
        forwarder6: str | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        source_ip_interface: str | None = ...,
        rr_max: int | None = ...,
        dns_entry: str | list[str] | list[DnsDatabaseDnsentryItem] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
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
    "DnsDatabase",
    "DnsDatabasePayload",
    "DnsDatabaseResponse",
    "DnsDatabaseObject",
]