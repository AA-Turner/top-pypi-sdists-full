""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/interface/dhcp_renew
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

class DhcpRenewPayload(TypedDict, total=False):
    """Payload type for DhcpRenew operations."""
    mkey: str
    ipv6: bool


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DhcpRenewResponse(TypedDict, total=False):
    """Response type for DhcpRenew - use with .dict property for typed dict access."""
    mkey: str
    ipv6: bool


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DhcpRenewObject(FortiObject):
    """Typed FortiObject for DhcpRenew with field access."""
    ipv6: bool


# ================================================================
# Main Endpoint Class
# ================================================================

class DhcpRenew:
    """
    
    Endpoint: system/interface/dhcp_renew
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
    ) -> DhcpRenewObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: DhcpRenewPayload | None = ...,
        mkey: str | None = ...,
        ipv6: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DhcpRenewObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DhcpRenewPayload | None = ...,
        mkey: str | None = ...,
        ipv6: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DhcpRenewObject: ...


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
        payload_dict: DhcpRenewPayload | None = ...,
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
    "DhcpRenew",
    "DhcpRenewPayload",
    "DhcpRenewResponse",
    "DhcpRenewObject",
]