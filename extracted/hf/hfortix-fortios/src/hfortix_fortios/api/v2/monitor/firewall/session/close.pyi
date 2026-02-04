""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/session/close
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

class ClosePayload(TypedDict, total=False):
    """Payload type for Close operations."""
    pro: Literal["tcp", "udp", "icmp", "..."]
    saddr: str
    daddr: str
    sport: int
    dport: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CloseResponse(TypedDict, total=False):
    """Response type for Close - use with .dict property for typed dict access."""
    pro: Literal["tcp", "udp", "icmp", "..."]
    saddr: str
    daddr: str
    sport: int
    dport: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CloseObject(FortiObject):
    """Typed FortiObject for Close with field access."""
    pro: Literal["tcp", "udp", "icmp", "..."]
    saddr: str
    daddr: str
    sport: int
    dport: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Close:
    """
    
    Endpoint: firewall/session/close
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
    ) -> CloseObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: ClosePayload | None = ...,
        pro: Literal["tcp", "udp", "icmp", "..."] | None = ...,
        saddr: str | None = ...,
        daddr: str | None = ...,
        sport: int | None = ...,
        dport: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CloseObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ClosePayload | None = ...,
        pro: Literal["tcp", "udp", "icmp", "..."] | None = ...,
        saddr: str | None = ...,
        daddr: str | None = ...,
        sport: int | None = ...,
        dport: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CloseObject: ...




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
        payload_dict: ClosePayload | None = ...,
        pro: Literal["tcp", "udp", "icmp", "..."] | None = ...,
        saddr: str | None = ...,
        daddr: str | None = ...,
        sport: int | None = ...,
        dport: int | None = ...,
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
    "Close",
    "ClosePayload",
    "CloseResponse",
    "CloseObject",
]