""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/ipv6
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

class Ipv6Payload(TypedDict, total=False):
    """Payload type for Ipv6 operations."""
    operator: Literal["and", "or"]
    ip_mask: str
    gateway: str
    type: str
    origin: str
    interface: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class Ipv6Response(TypedDict, total=False):
    """Response type for Ipv6 - use with .dict property for typed dict access."""
    ip_version: int
    type: str
    origin: str
    subtype: str
    ip_mask: str
    distance: int
    metric: int
    priority: int
    gateway: str
    non_rc_gateway: str
    interface: str
    is_tunnel_route: bool
    tunnel_parent: str
    install_date: int
    vrf: int


class Ipv6Object(FortiObject[Ipv6Response]):
    """Typed FortiObject for Ipv6 with field access."""
    ip_version: int
    type: str
    origin: str
    subtype: str
    ip_mask: str
    distance: int
    metric: int
    priority: int
    gateway: str
    non_rc_gateway: str
    interface: str
    is_tunnel_route: bool
    tunnel_parent: str
    install_date: int
    vrf: int



# ================================================================
# Main Endpoint Class
# ================================================================

class Ipv6:
    """
    
    Endpoint: router/ipv6
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
        operator: Literal["and", "or"] | None = ...,
        ip_mask: str | None = ...,
        gateway: str | None = ...,
        type: str | None = ...,
        origin: str | None = ...,
        interface: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[Ipv6Object]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Ipv6Payload | None = ...,
        operator: Literal["and", "or"] | None = ...,
        ip_mask: str | None = ...,
        gateway: str | None = ...,
        type: str | None = ...,
        origin: str | None = ...,
        interface: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Ipv6Object: ...




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
        payload_dict: Ipv6Payload | None = ...,
        operator: Literal["and", "or"] | None = ...,
        ip_mask: str | None = ...,
        gateway: str | None = ...,
        type: str | None = ...,
        origin: str | None = ...,
        interface: str | None = ...,
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
    "Ipv6",
    "Ipv6Response",
    "Ipv6Object",
]