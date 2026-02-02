""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: network/debug_flow/start
Category: monitor
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

class StartPayload(TypedDict, total=False):
    """Payload type for Start operations."""
    num_packets: int
    ipv6: bool
    negate: bool
    addr_from: str
    addr_to: str
    daddr_from: str
    daddr_to: str
    saddr_from: str
    saddr_to: str
    port_from: int
    port_to: int
    dport_from: int
    dport_to: int
    sport_from: int
    sport_to: int
    proto: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StartResponse(TypedDict, total=False):
    """Response type for Start - use with .dict property for typed dict access."""
    num_packets: int
    ipv6: bool
    negate: bool
    addr_from: str
    addr_to: str
    daddr_from: str
    daddr_to: str
    saddr_from: str
    saddr_to: str
    port_from: int
    port_to: int
    dport_from: int
    dport_to: int
    sport_from: int
    sport_to: int
    proto: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StartObject(FortiObject):
    """Typed FortiObject for Start with field access."""
    num_packets: int
    ipv6: bool
    negate: bool
    addr_from: str
    addr_to: str
    daddr_from: str
    daddr_to: str
    saddr_from: str
    saddr_to: str
    port_from: int
    port_to: int
    dport_from: int
    dport_to: int
    sport_from: int
    sport_to: int
    proto: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Start:
    """
    
    Endpoint: network/debug_flow/start
    Category: monitor
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StartObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: StartPayload | None = ...,
        num_packets: int | None = ...,
        ipv6: bool | None = ...,
        negate: bool | None = ...,
        addr_from: str | None = ...,
        addr_to: str | None = ...,
        daddr_from: str | None = ...,
        daddr_to: str | None = ...,
        saddr_from: str | None = ...,
        saddr_to: str | None = ...,
        port_from: int | None = ...,
        port_to: int | None = ...,
        dport_from: int | None = ...,
        dport_to: int | None = ...,
        sport_from: int | None = ...,
        sport_to: int | None = ...,
        proto: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StartObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StartPayload | None = ...,
        num_packets: int | None = ...,
        ipv6: bool | None = ...,
        negate: bool | None = ...,
        addr_from: str | None = ...,
        addr_to: str | None = ...,
        daddr_from: str | None = ...,
        daddr_to: str | None = ...,
        saddr_from: str | None = ...,
        saddr_to: str | None = ...,
        port_from: int | None = ...,
        port_to: int | None = ...,
        dport_from: int | None = ...,
        dport_to: int | None = ...,
        sport_from: int | None = ...,
        sport_to: int | None = ...,
        proto: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StartObject: ...


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
        payload_dict: StartPayload | None = ...,
        num_packets: int | None = ...,
        ipv6: bool | None = ...,
        negate: bool | None = ...,
        addr_from: str | None = ...,
        addr_to: str | None = ...,
        daddr_from: str | None = ...,
        daddr_to: str | None = ...,
        saddr_from: str | None = ...,
        saddr_to: str | None = ...,
        port_from: int | None = ...,
        port_to: int | None = ...,
        dport_from: int | None = ...,
        dport_to: int | None = ...,
        sport_from: int | None = ...,
        sport_to: int | None = ...,
        proto: int | None = ...,
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
    "Start",
    "StartPayload",
    "StartResponse",
    "StartObject",
]