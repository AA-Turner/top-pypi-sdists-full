""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/vxlan
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

class VxlanRemoteipItem(TypedDict, total=False):
    """Nested item for remote-ip field."""
    ip: str


class VxlanRemoteip6Item(TypedDict, total=False):
    """Nested item for remote-ip6 field."""
    ip6: str


class VxlanPayload(TypedDict, total=False):
    """Payload type for Vxlan operations."""
    name: str
    interface: str
    vni: int
    ip_version: Literal["ipv4-unicast", "ipv6-unicast", "ipv4-multicast", "ipv6-multicast"]
    remote_ip: str | list[str] | list[VxlanRemoteipItem]
    local_ip: str
    remote_ip6: str | list[str] | list[VxlanRemoteip6Item]
    local_ip6: str
    dstport: int
    multicast_ttl: int
    evpn_id: int
    learn_from_traffic: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VxlanResponse(TypedDict, total=False):
    """Response type for Vxlan - use with .dict property for typed dict access."""
    name: str
    interface: str
    vni: int
    ip_version: Literal["ipv4-unicast", "ipv6-unicast", "ipv4-multicast", "ipv6-multicast"]
    remote_ip: list[VxlanRemoteipItem]
    local_ip: str
    remote_ip6: list[VxlanRemoteip6Item]
    local_ip6: str
    dstport: int
    multicast_ttl: int
    evpn_id: int
    learn_from_traffic: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VxlanRemoteipItemObject(FortiObject[VxlanRemoteipItem]):
    """Typed object for remote-ip table items with attribute access."""
    ip: str


class VxlanRemoteip6ItemObject(FortiObject[VxlanRemoteip6Item]):
    """Typed object for remote-ip6 table items with attribute access."""
    ip6: str


class VxlanObject(FortiObject):
    """Typed FortiObject for Vxlan with field access."""
    name: str
    interface: str
    vni: int
    ip_version: Literal["ipv4-unicast", "ipv6-unicast", "ipv4-multicast", "ipv6-multicast"]
    remote_ip: FortiObjectList[VxlanRemoteipItemObject]
    local_ip: str
    remote_ip6: FortiObjectList[VxlanRemoteip6ItemObject]
    local_ip6: str
    dstport: int
    multicast_ttl: int
    evpn_id: int
    learn_from_traffic: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Vxlan:
    """
    
    Endpoint: system/vxlan
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
    ) -> VxlanObject: ...
    
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
    ) -> FortiObjectList[VxlanObject]: ...
    
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
        payload_dict: VxlanPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        vni: int | None = ...,
        ip_version: Literal["ipv4-unicast", "ipv6-unicast", "ipv4-multicast", "ipv6-multicast"] | None = ...,
        remote_ip: str | list[str] | list[VxlanRemoteipItem] | None = ...,
        local_ip: str | None = ...,
        remote_ip6: str | list[str] | list[VxlanRemoteip6Item] | None = ...,
        local_ip6: str | None = ...,
        dstport: int | None = ...,
        multicast_ttl: int | None = ...,
        evpn_id: int | None = ...,
        learn_from_traffic: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VxlanObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VxlanPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        vni: int | None = ...,
        ip_version: Literal["ipv4-unicast", "ipv6-unicast", "ipv4-multicast", "ipv6-multicast"] | None = ...,
        remote_ip: str | list[str] | list[VxlanRemoteipItem] | None = ...,
        local_ip: str | None = ...,
        remote_ip6: str | list[str] | list[VxlanRemoteip6Item] | None = ...,
        local_ip6: str | None = ...,
        dstport: int | None = ...,
        multicast_ttl: int | None = ...,
        evpn_id: int | None = ...,
        learn_from_traffic: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VxlanObject: ...

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
        payload_dict: VxlanPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        vni: int | None = ...,
        ip_version: Literal["ipv4-unicast", "ipv6-unicast", "ipv4-multicast", "ipv6-multicast"] | None = ...,
        remote_ip: str | list[str] | list[VxlanRemoteipItem] | None = ...,
        local_ip: str | None = ...,
        remote_ip6: str | list[str] | list[VxlanRemoteip6Item] | None = ...,
        local_ip6: str | None = ...,
        dstport: int | None = ...,
        multicast_ttl: int | None = ...,
        evpn_id: int | None = ...,
        learn_from_traffic: Literal["enable", "disable"] | None = ...,
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
    "Vxlan",
    "VxlanPayload",
    "VxlanResponse",
    "VxlanObject",
]