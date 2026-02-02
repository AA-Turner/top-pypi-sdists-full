""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/link_monitor
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

class LinkMonitorServerItem(TypedDict, total=False):
    """Nested item for server field."""
    address: str


class LinkMonitorRouteItem(TypedDict, total=False):
    """Nested item for route field."""
    subnet: str


class LinkMonitorServerlistItem(TypedDict, total=False):
    """Nested item for server-list field."""
    id: int
    dst: str
    protocol: Literal["ping", "tcp-echo", "udp-echo", "http", "https", "twamp"]
    port: int
    weight: int


class LinkMonitorPayload(TypedDict, total=False):
    """Payload type for LinkMonitor operations."""
    name: str
    addr_mode: Literal["ipv4", "ipv6"]
    srcintf: str
    server_config: Literal["default", "individual"]
    server_type: Literal["static", "dynamic"]
    server: str | list[str] | list[LinkMonitorServerItem]
    protocol: str | list[str]
    port: int
    gateway_ip: str
    gateway_ip6: str
    route: str | list[str] | list[LinkMonitorRouteItem]
    source_ip: str
    source_ip6: str
    http_get: str
    http_agent: str
    http_match: str
    interval: int
    probe_timeout: int
    failtime: int
    recoverytime: int
    probe_count: int
    security_mode: Literal["none", "authentication"]
    password: str
    packet_size: int
    ha_priority: int
    fail_weight: int
    update_cascade_interface: Literal["enable", "disable"]
    update_static_route: Literal["enable", "disable"]
    update_policy_route: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    diffservcode: str
    class_id: int
    service_detection: Literal["enable", "disable"]
    server_list: str | list[str] | list[LinkMonitorServerlistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LinkMonitorResponse(TypedDict, total=False):
    """Response type for LinkMonitor - use with .dict property for typed dict access."""
    name: str
    addr_mode: Literal["ipv4", "ipv6"]
    srcintf: str
    server_config: Literal["default", "individual"]
    server_type: Literal["static", "dynamic"]
    server: list[LinkMonitorServerItem]
    protocol: str
    port: int
    gateway_ip: str
    gateway_ip6: str
    route: list[LinkMonitorRouteItem]
    source_ip: str
    source_ip6: str
    http_get: str
    http_agent: str
    http_match: str
    interval: int
    probe_timeout: int
    failtime: int
    recoverytime: int
    probe_count: int
    security_mode: Literal["none", "authentication"]
    password: str
    packet_size: int
    ha_priority: int
    fail_weight: int
    update_cascade_interface: Literal["enable", "disable"]
    update_static_route: Literal["enable", "disable"]
    update_policy_route: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    diffservcode: str
    class_id: int
    service_detection: Literal["enable", "disable"]
    server_list: list[LinkMonitorServerlistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LinkMonitorServerItemObject(FortiObject[LinkMonitorServerItem]):
    """Typed object for server table items with attribute access."""
    address: str


class LinkMonitorRouteItemObject(FortiObject[LinkMonitorRouteItem]):
    """Typed object for route table items with attribute access."""
    subnet: str


class LinkMonitorServerlistItemObject(FortiObject[LinkMonitorServerlistItem]):
    """Typed object for server-list table items with attribute access."""
    id: int
    dst: str
    protocol: Literal["ping", "tcp-echo", "udp-echo", "http", "https", "twamp"]
    port: int
    weight: int


class LinkMonitorObject(FortiObject):
    """Typed FortiObject for LinkMonitor with field access."""
    name: str
    addr_mode: Literal["ipv4", "ipv6"]
    srcintf: str
    server_config: Literal["default", "individual"]
    server_type: Literal["static", "dynamic"]
    server: FortiObjectList[LinkMonitorServerItemObject]
    protocol: str
    port: int
    gateway_ip: str
    gateway_ip6: str
    route: FortiObjectList[LinkMonitorRouteItemObject]
    source_ip: str
    source_ip6: str
    http_get: str
    http_agent: str
    http_match: str
    interval: int
    probe_timeout: int
    failtime: int
    recoverytime: int
    probe_count: int
    security_mode: Literal["none", "authentication"]
    password: str
    packet_size: int
    ha_priority: int
    fail_weight: int
    update_cascade_interface: Literal["enable", "disable"]
    update_static_route: Literal["enable", "disable"]
    update_policy_route: Literal["enable", "disable"]
    status: Literal["enable", "disable"]
    diffservcode: str
    class_id: int
    service_detection: Literal["enable", "disable"]
    server_list: FortiObjectList[LinkMonitorServerlistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class LinkMonitor:
    """
    
    Endpoint: system/link_monitor
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
    ) -> LinkMonitorObject: ...
    
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
    ) -> FortiObjectList[LinkMonitorObject]: ...
    
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
        payload_dict: LinkMonitorPayload | None = ...,
        name: str | None = ...,
        addr_mode: Literal["ipv4", "ipv6"] | None = ...,
        srcintf: str | None = ...,
        server_config: Literal["default", "individual"] | None = ...,
        server_type: Literal["static", "dynamic"] | None = ...,
        server: str | list[str] | list[LinkMonitorServerItem] | None = ...,
        protocol: str | list[str] | None = ...,
        port: int | None = ...,
        gateway_ip: str | None = ...,
        gateway_ip6: str | None = ...,
        route: str | list[str] | list[LinkMonitorRouteItem] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        http_get: str | None = ...,
        http_agent: str | None = ...,
        http_match: str | None = ...,
        interval: int | None = ...,
        probe_timeout: int | None = ...,
        failtime: int | None = ...,
        recoverytime: int | None = ...,
        probe_count: int | None = ...,
        security_mode: Literal["none", "authentication"] | None = ...,
        password: str | None = ...,
        packet_size: int | None = ...,
        ha_priority: int | None = ...,
        fail_weight: int | None = ...,
        update_cascade_interface: Literal["enable", "disable"] | None = ...,
        update_static_route: Literal["enable", "disable"] | None = ...,
        update_policy_route: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        class_id: int | None = ...,
        service_detection: Literal["enable", "disable"] | None = ...,
        server_list: str | list[str] | list[LinkMonitorServerlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LinkMonitorObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LinkMonitorPayload | None = ...,
        name: str | None = ...,
        addr_mode: Literal["ipv4", "ipv6"] | None = ...,
        srcintf: str | None = ...,
        server_config: Literal["default", "individual"] | None = ...,
        server_type: Literal["static", "dynamic"] | None = ...,
        server: str | list[str] | list[LinkMonitorServerItem] | None = ...,
        protocol: str | list[str] | None = ...,
        port: int | None = ...,
        gateway_ip: str | None = ...,
        gateway_ip6: str | None = ...,
        route: str | list[str] | list[LinkMonitorRouteItem] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        http_get: str | None = ...,
        http_agent: str | None = ...,
        http_match: str | None = ...,
        interval: int | None = ...,
        probe_timeout: int | None = ...,
        failtime: int | None = ...,
        recoverytime: int | None = ...,
        probe_count: int | None = ...,
        security_mode: Literal["none", "authentication"] | None = ...,
        password: str | None = ...,
        packet_size: int | None = ...,
        ha_priority: int | None = ...,
        fail_weight: int | None = ...,
        update_cascade_interface: Literal["enable", "disable"] | None = ...,
        update_static_route: Literal["enable", "disable"] | None = ...,
        update_policy_route: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        class_id: int | None = ...,
        service_detection: Literal["enable", "disable"] | None = ...,
        server_list: str | list[str] | list[LinkMonitorServerlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LinkMonitorObject: ...

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
        payload_dict: LinkMonitorPayload | None = ...,
        name: str | None = ...,
        addr_mode: Literal["ipv4", "ipv6"] | None = ...,
        srcintf: str | None = ...,
        server_config: Literal["default", "individual"] | None = ...,
        server_type: Literal["static", "dynamic"] | None = ...,
        server: str | list[str] | list[LinkMonitorServerItem] | None = ...,
        protocol: Literal["ping", "tcp-echo", "udp-echo", "http", "https", "twamp"] | list[str] | None = ...,
        port: int | None = ...,
        gateway_ip: str | None = ...,
        gateway_ip6: str | None = ...,
        route: str | list[str] | list[LinkMonitorRouteItem] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        http_get: str | None = ...,
        http_agent: str | None = ...,
        http_match: str | None = ...,
        interval: int | None = ...,
        probe_timeout: int | None = ...,
        failtime: int | None = ...,
        recoverytime: int | None = ...,
        probe_count: int | None = ...,
        security_mode: Literal["none", "authentication"] | None = ...,
        password: str | None = ...,
        packet_size: int | None = ...,
        ha_priority: int | None = ...,
        fail_weight: int | None = ...,
        update_cascade_interface: Literal["enable", "disable"] | None = ...,
        update_static_route: Literal["enable", "disable"] | None = ...,
        update_policy_route: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        class_id: int | None = ...,
        service_detection: Literal["enable", "disable"] | None = ...,
        server_list: str | list[str] | list[LinkMonitorServerlistItem] | None = ...,
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
    "LinkMonitor",
    "LinkMonitorPayload",
    "LinkMonitorResponse",
    "LinkMonitorObject",
]