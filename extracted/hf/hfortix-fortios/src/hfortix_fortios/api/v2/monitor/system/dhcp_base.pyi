""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/dhcp
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

class DhcpPayload(TypedDict, total=False):
    """Payload type for Dhcp operations."""
    scope: Literal["vdom", "global"]
    ipv6: bool
    interface: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class DhcpResponse(TypedDict, total=False):
    """Response type for Dhcp - use with .dict property for typed dict access."""
    type: str
    status: str
    ip: str
    expire_time: int
    interface: str
    server_mkey: int
    server_ipam_enabled: bool
    reserved: bool
    mac: str
    vci: str
    hostname: str
    duid: str
    iaid: int
    ssid: str
    access_point: str


class DhcpObject(FortiObject[DhcpResponse]):
    """Typed FortiObject for Dhcp with field access."""
    type: str
    status: str
    ip: str
    expire_time: int
    interface: str
    server_mkey: int
    server_ipam_enabled: bool
    reserved: bool
    mac: str
    vci: str
    hostname: str
    duid: str
    iaid: int
    ssid: str
    access_point: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Dhcp:
    """
    
    Endpoint: system/dhcp
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
        scope: Literal["vdom", "global"] | None = ...,
        ipv6: bool | None = ...,
        interface: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[DhcpObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DhcpPayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        ipv6: bool | None = ...,
        interface: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DhcpObject: ...




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
        payload_dict: DhcpPayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        ipv6: bool | None = ...,
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
    "Dhcp",
    "DhcpResponse",
    "DhcpObject",
]