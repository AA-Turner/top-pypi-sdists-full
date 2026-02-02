""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/interface/dhcp_status
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

class DhcpStatusPayload(TypedDict, total=False):
    """Payload type for DhcpStatus operations."""
    mkey: str
    ipv6: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class DhcpStatusResponse(TypedDict, total=False):
    """Response type for DhcpStatus - use with .dict property for typed dict access."""
    status: str
    ip: str
    netmask: str
    expiry_date: str
    dynamic_dns1: str
    dynamic_dns2: str
    dynamic_gateway: str
    show_gateway: bool
    override_dns: bool


class DhcpStatusObject(FortiObject[DhcpStatusResponse]):
    """Typed FortiObject for DhcpStatus with field access."""
    status: str
    ip: str
    netmask: str
    expiry_date: str
    dynamic_dns1: str
    dynamic_dns2: str
    dynamic_gateway: str
    show_gateway: bool
    override_dns: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class DhcpStatus:
    """
    
    Endpoint: system/interface/dhcp_status
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
        mkey: str,
        ipv6: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[DhcpStatusObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DhcpStatusPayload | None = ...,
        mkey: str | None = ...,
        ipv6: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DhcpStatusObject: ...


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
        payload_dict: DhcpStatusPayload | None = ...,
        mkey: str | None = ...,
        ipv6: bool | None = ...,
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
    "DhcpStatus",
    "DhcpStatusResponse",
    "DhcpStatusObject",
]