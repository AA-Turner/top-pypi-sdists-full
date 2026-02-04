""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: virtual_wan/members
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

class MembersPayload(TypedDict, total=False):
    """Payload type for Members operations."""
    interface: list[str]
    zone: str
    sla: str
    skip_vpn_child: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class MembersResponse(TypedDict, total=False):
    """Response type for Members - use with .dict property for typed dict access."""
    interface: str
    seq_num: str
    status: str
    ipv4_gateway: str
    ipv6_gateway: str
    link: str
    session: int
    tx_bytes: int
    rx_bytes: int
    tx_bandwidth: int
    rx_bandwidth: int
    state_changed: int
    child_intfs: str


class MembersObject(FortiObject[MembersResponse]):
    """Typed FortiObject for Members with field access."""
    interface: str
    seq_num: str
    status: str
    ipv4_gateway: str
    ipv6_gateway: str
    link: str
    session: int
    tx_bytes: int
    rx_bytes: int
    tx_bandwidth: int
    rx_bandwidth: int
    state_changed: int
    child_intfs: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Members:
    """
    
    Endpoint: virtual_wan/members
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
        interface: list[str] | None = ...,
        zone: str | None = ...,
        sla: str | None = ...,
        skip_vpn_child: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[MembersObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MembersPayload | None = ...,
        interface: list[str] | None = ...,
        zone: str | None = ...,
        sla: str | None = ...,
        skip_vpn_child: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MembersObject: ...




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
        payload_dict: MembersPayload | None = ...,
        interface: list[str] | None = ...,
        zone: str | None = ...,
        sla: str | None = ...,
        skip_vpn_child: bool | None = ...,
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
    "Members",
    "MembersResponse",
    "MembersObject",
]