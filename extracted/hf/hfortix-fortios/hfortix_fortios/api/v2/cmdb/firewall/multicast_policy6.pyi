""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/multicast_policy6
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

class MulticastPolicy6SrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class MulticastPolicy6DstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class MulticastPolicy6Payload(TypedDict, total=False):
    """Payload type for MulticastPolicy6 operations."""
    id: int
    uuid: str
    status: Literal["enable", "disable"]
    name: str
    srcintf: str
    dstintf: str
    srcaddr: str | list[str] | list[MulticastPolicy6SrcaddrItem]
    dstaddr: str | list[str] | list[MulticastPolicy6DstaddrItem]
    action: Literal["accept", "deny"]
    protocol: int
    start_port: int
    end_port: int
    utm_status: Literal["enable", "disable"]
    ips_sensor: str
    logtraffic: Literal["all", "utm", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    comments: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class MulticastPolicy6Response(TypedDict, total=False):
    """Response type for MulticastPolicy6 - use with .dict property for typed dict access."""
    id: int
    uuid: str
    status: Literal["enable", "disable"]
    name: str
    srcintf: str
    dstintf: str
    srcaddr: list[MulticastPolicy6SrcaddrItem]
    dstaddr: list[MulticastPolicy6DstaddrItem]
    action: Literal["accept", "deny"]
    protocol: int
    start_port: int
    end_port: int
    utm_status: Literal["enable", "disable"]
    ips_sensor: str
    logtraffic: Literal["all", "utm", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    comments: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class MulticastPolicy6SrcaddrItemObject(FortiObject[MulticastPolicy6SrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class MulticastPolicy6DstaddrItemObject(FortiObject[MulticastPolicy6DstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class MulticastPolicy6Object(FortiObject):
    """Typed FortiObject for MulticastPolicy6 with field access."""
    id: int
    uuid: str
    status: Literal["enable", "disable"]
    name: str
    srcintf: str
    dstintf: str
    srcaddr: FortiObjectList[MulticastPolicy6SrcaddrItemObject]
    dstaddr: FortiObjectList[MulticastPolicy6DstaddrItemObject]
    action: Literal["accept", "deny"]
    protocol: int
    start_port: int
    end_port: int
    utm_status: Literal["enable", "disable"]
    ips_sensor: str
    logtraffic: Literal["all", "utm", "disable"]
    auto_asic_offload: Literal["enable", "disable"]
    comments: str


# ================================================================
# Main Endpoint Class
# ================================================================

class MulticastPolicy6:
    """
    
    Endpoint: firewall/multicast_policy6
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
    ) -> MulticastPolicy6Object: ...
    
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
    ) -> FortiObjectList[MulticastPolicy6Object]: ...
    
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
        payload_dict: MulticastPolicy6Payload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        srcaddr: str | list[str] | list[MulticastPolicy6SrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[MulticastPolicy6DstaddrItem] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastPolicy6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MulticastPolicy6Payload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        srcaddr: str | list[str] | list[MulticastPolicy6SrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[MulticastPolicy6DstaddrItem] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MulticastPolicy6Object: ...

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
        payload_dict: MulticastPolicy6Payload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        srcintf: str | None = ...,
        dstintf: str | None = ...,
        srcaddr: str | list[str] | list[MulticastPolicy6SrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[MulticastPolicy6DstaddrItem] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        protocol: int | None = ...,
        start_port: int | None = ...,
        end_port: int | None = ...,
        utm_status: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        logtraffic: Literal["all", "utm", "disable"] | None = ...,
        auto_asic_offload: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
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
    "MulticastPolicy6",
    "MulticastPolicy6Payload",
    "MulticastPolicy6Response",
    "MulticastPolicy6Object",
]