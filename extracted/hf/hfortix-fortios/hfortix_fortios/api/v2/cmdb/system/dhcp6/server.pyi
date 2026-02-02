""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/dhcp6/server
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

class ServerOptionsVcistringItem(TypedDict, total=False):
    """Nested item for options.vci-string field."""
    vci_string: str


class ServerIprangeVcistringItem(TypedDict, total=False):
    """Nested item for ip-range.vci-string field."""
    vci_string: str


class ServerOptionsItem(TypedDict, total=False):
    """Nested item for options field."""
    id: int
    code: int
    type: Literal["hex", "string", "ip6", "fqdn"]
    value: str
    ip6: str | list[str]
    vci_match: Literal["disable", "enable"]
    vci_string: str | list[str] | list[ServerOptionsVcistringItem]


class ServerPrefixrangeItem(TypedDict, total=False):
    """Nested item for prefix-range field."""
    id: int
    start_prefix: str
    end_prefix: str
    prefix_length: int


class ServerIprangeItem(TypedDict, total=False):
    """Nested item for ip-range field."""
    id: int
    start_ip: str
    end_ip: str
    vci_match: Literal["disable", "enable"]
    vci_string: str | list[str] | list[ServerIprangeVcistringItem]


class ServerPayload(TypedDict, total=False):
    """Payload type for Server operations."""
    id: int
    status: Literal["disable", "enable"]
    rapid_commit: Literal["disable", "enable"]
    lease_time: int
    dns_service: Literal["delegated", "default", "specify"]
    dns_search_list: Literal["delegated", "specify"]
    dns_server1: str
    dns_server2: str
    dns_server3: str
    dns_server4: str
    domain: str
    subnet: str
    interface: str
    delegated_prefix_route: Literal["disable", "enable"]
    options: str | list[str] | list[ServerOptionsItem]
    upstream_interface: str
    delegated_prefix_iaid: int
    ip_mode: Literal["range", "delegated"]
    prefix_mode: Literal["dhcp6", "ra"]
    prefix_range: str | list[str] | list[ServerPrefixrangeItem]
    ip_range: str | list[str] | list[ServerIprangeItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ServerResponse(TypedDict, total=False):
    """Response type for Server - use with .dict property for typed dict access."""
    id: int
    status: Literal["disable", "enable"]
    rapid_commit: Literal["disable", "enable"]
    lease_time: int
    dns_service: Literal["delegated", "default", "specify"]
    dns_search_list: Literal["delegated", "specify"]
    dns_server1: str
    dns_server2: str
    dns_server3: str
    dns_server4: str
    domain: str
    subnet: str
    interface: str
    delegated_prefix_route: Literal["disable", "enable"]
    options: list[ServerOptionsItem]
    upstream_interface: str
    delegated_prefix_iaid: int
    ip_mode: Literal["range", "delegated"]
    prefix_mode: Literal["dhcp6", "ra"]
    prefix_range: list[ServerPrefixrangeItem]
    ip_range: list[ServerIprangeItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ServerOptionsVcistringItemObject(FortiObject[ServerOptionsVcistringItem]):
    """Typed object for options.vci-string table items with attribute access."""
    vci_string: str


class ServerIprangeVcistringItemObject(FortiObject[ServerIprangeVcistringItem]):
    """Typed object for ip-range.vci-string table items with attribute access."""
    vci_string: str


class ServerOptionsItemObject(FortiObject[ServerOptionsItem]):
    """Typed object for options table items with attribute access."""
    id: int
    code: int
    type: Literal["hex", "string", "ip6", "fqdn"]
    value: str
    ip6: str | list[str]
    vci_match: Literal["disable", "enable"]
    vci_string: FortiObjectList[ServerOptionsVcistringItemObject]


class ServerPrefixrangeItemObject(FortiObject[ServerPrefixrangeItem]):
    """Typed object for prefix-range table items with attribute access."""
    id: int
    start_prefix: str
    end_prefix: str
    prefix_length: int


class ServerIprangeItemObject(FortiObject[ServerIprangeItem]):
    """Typed object for ip-range table items with attribute access."""
    id: int
    start_ip: str
    end_ip: str
    vci_match: Literal["disable", "enable"]
    vci_string: FortiObjectList[ServerIprangeVcistringItemObject]


class ServerObject(FortiObject):
    """Typed FortiObject for Server with field access."""
    id: int
    status: Literal["disable", "enable"]
    rapid_commit: Literal["disable", "enable"]
    lease_time: int
    dns_service: Literal["delegated", "default", "specify"]
    dns_search_list: Literal["delegated", "specify"]
    dns_server1: str
    dns_server2: str
    dns_server3: str
    dns_server4: str
    domain: str
    subnet: str
    interface: str
    delegated_prefix_route: Literal["disable", "enable"]
    options: FortiObjectList[ServerOptionsItemObject]
    upstream_interface: str
    delegated_prefix_iaid: int
    ip_mode: Literal["range", "delegated"]
    prefix_mode: Literal["dhcp6", "ra"]
    prefix_range: FortiObjectList[ServerPrefixrangeItemObject]
    ip_range: FortiObjectList[ServerIprangeItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Server:
    """
    
    Endpoint: system/dhcp6/server
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> ServerObject: ...
    
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
    ) -> FortiObjectList[ServerObject]: ...
    
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
        payload_dict: ServerPayload | None = ...,
        id: int | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        rapid_commit: Literal["disable", "enable"] | None = ...,
        lease_time: int | None = ...,
        dns_service: Literal["delegated", "default", "specify"] | None = ...,
        dns_search_list: Literal["delegated", "specify"] | None = ...,
        dns_server1: str | None = ...,
        dns_server2: str | None = ...,
        dns_server3: str | None = ...,
        dns_server4: str | None = ...,
        domain: str | None = ...,
        subnet: str | None = ...,
        interface: str | None = ...,
        delegated_prefix_route: Literal["disable", "enable"] | None = ...,
        options: str | list[str] | list[ServerOptionsItem] | None = ...,
        upstream_interface: str | None = ...,
        delegated_prefix_iaid: int | None = ...,
        ip_mode: Literal["range", "delegated"] | None = ...,
        prefix_mode: Literal["dhcp6", "ra"] | None = ...,
        prefix_range: str | list[str] | list[ServerPrefixrangeItem] | None = ...,
        ip_range: str | list[str] | list[ServerIprangeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ServerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        id: int | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        rapid_commit: Literal["disable", "enable"] | None = ...,
        lease_time: int | None = ...,
        dns_service: Literal["delegated", "default", "specify"] | None = ...,
        dns_search_list: Literal["delegated", "specify"] | None = ...,
        dns_server1: str | None = ...,
        dns_server2: str | None = ...,
        dns_server3: str | None = ...,
        dns_server4: str | None = ...,
        domain: str | None = ...,
        subnet: str | None = ...,
        interface: str | None = ...,
        delegated_prefix_route: Literal["disable", "enable"] | None = ...,
        options: str | list[str] | list[ServerOptionsItem] | None = ...,
        upstream_interface: str | None = ...,
        delegated_prefix_iaid: int | None = ...,
        ip_mode: Literal["range", "delegated"] | None = ...,
        prefix_mode: Literal["dhcp6", "ra"] | None = ...,
        prefix_range: str | list[str] | list[ServerPrefixrangeItem] | None = ...,
        ip_range: str | list[str] | list[ServerIprangeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ServerObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ServerPayload | None = ...,
        id: int | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        rapid_commit: Literal["disable", "enable"] | None = ...,
        lease_time: int | None = ...,
        dns_service: Literal["delegated", "default", "specify"] | None = ...,
        dns_search_list: Literal["delegated", "specify"] | None = ...,
        dns_server1: str | None = ...,
        dns_server2: str | None = ...,
        dns_server3: str | None = ...,
        dns_server4: str | None = ...,
        domain: str | None = ...,
        subnet: str | None = ...,
        interface: str | None = ...,
        delegated_prefix_route: Literal["disable", "enable"] | None = ...,
        options: str | list[str] | list[ServerOptionsItem] | None = ...,
        upstream_interface: str | None = ...,
        delegated_prefix_iaid: int | None = ...,
        ip_mode: Literal["range", "delegated"] | None = ...,
        prefix_mode: Literal["dhcp6", "ra"] | None = ...,
        prefix_range: str | list[str] | list[ServerPrefixrangeItem] | None = ...,
        ip_range: str | list[str] | list[ServerIprangeItem] | None = ...,
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
    "Server",
    "ServerPayload",
    "ServerResponse",
    "ServerObject",
]