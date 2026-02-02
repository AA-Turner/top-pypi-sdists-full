""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ddns
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

class DdnsDdnsserveraddrItem(TypedDict, total=False):
    """Nested item for ddns-server-addr field."""
    addr: str


class DdnsMonitorinterfaceItem(TypedDict, total=False):
    """Nested item for monitor-interface field."""
    interface_name: str


class DdnsPayload(TypedDict, total=False):
    """Payload type for Ddns operations."""
    ddnsid: int
    ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"]
    addr_type: Literal["ipv4", "ipv6"]
    server_type: Literal["ipv4", "ipv6"]
    ddns_server_addr: str | list[str] | list[DdnsDdnsserveraddrItem]
    ddns_zone: str
    ddns_ttl: int
    ddns_auth: Literal["disable", "tsig"]
    ddns_keyname: str
    ddns_key: str
    ddns_domain: str
    ddns_username: str
    ddns_sn: str
    ddns_password: str
    use_public_ip: Literal["disable", "enable"]
    update_interval: int
    clear_text: Literal["disable", "enable"]
    ssl_certificate: str
    bound_ip: str
    monitor_interface: str | list[str] | list[DdnsMonitorinterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DdnsResponse(TypedDict, total=False):
    """Response type for Ddns - use with .dict property for typed dict access."""
    ddnsid: int
    ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"]
    addr_type: Literal["ipv4", "ipv6"]
    server_type: Literal["ipv4", "ipv6"]
    ddns_server_addr: list[DdnsDdnsserveraddrItem]
    ddns_zone: str
    ddns_ttl: int
    ddns_auth: Literal["disable", "tsig"]
    ddns_keyname: str
    ddns_key: str
    ddns_domain: str
    ddns_username: str
    ddns_sn: str
    ddns_password: str
    use_public_ip: Literal["disable", "enable"]
    update_interval: int
    clear_text: Literal["disable", "enable"]
    ssl_certificate: str
    bound_ip: str
    monitor_interface: list[DdnsMonitorinterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DdnsDdnsserveraddrItemObject(FortiObject[DdnsDdnsserveraddrItem]):
    """Typed object for ddns-server-addr table items with attribute access."""
    addr: str


class DdnsMonitorinterfaceItemObject(FortiObject[DdnsMonitorinterfaceItem]):
    """Typed object for monitor-interface table items with attribute access."""
    interface_name: str


class DdnsObject(FortiObject):
    """Typed FortiObject for Ddns with field access."""
    ddnsid: int
    ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"]
    addr_type: Literal["ipv4", "ipv6"]
    server_type: Literal["ipv4", "ipv6"]
    ddns_server_addr: FortiObjectList[DdnsDdnsserveraddrItemObject]
    ddns_zone: str
    ddns_ttl: int
    ddns_auth: Literal["disable", "tsig"]
    ddns_keyname: str
    ddns_key: str
    ddns_domain: str
    ddns_username: str
    ddns_sn: str
    ddns_password: str
    use_public_ip: Literal["disable", "enable"]
    update_interval: int
    clear_text: Literal["disable", "enable"]
    ssl_certificate: str
    bound_ip: str
    monitor_interface: FortiObjectList[DdnsMonitorinterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ddns:
    """
    
    Endpoint: system/ddns
    Category: cmdb
    MKey: ddnsid
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
        ddnsid: int,
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
    ) -> DdnsObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[DdnsObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[DdnsDdnsserveraddrItem] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[DdnsMonitorinterfaceItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DdnsObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[DdnsDdnsserveraddrItem] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[DdnsMonitorinterfaceItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DdnsObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        ddnsid: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        ddnsid: int,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[DdnsDdnsserveraddrItem] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[DdnsMonitorinterfaceItem] | None = ...,
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
    "Ddns",
    "DdnsPayload",
    "DdnsResponse",
    "DdnsObject",
]