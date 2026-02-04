""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: web_proxy/fast_fallback
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

class FastFallbackPayload(TypedDict, total=False):
    """Payload type for FastFallback operations."""
    name: str
    status: Literal["enable", "disable"]
    connection_mode: Literal["sequentially", "simultaneously"]
    protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"]
    connection_timeout: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FastFallbackResponse(TypedDict, total=False):
    """Response type for FastFallback - use with .dict property for typed dict access."""
    name: str
    status: Literal["enable", "disable"]
    connection_mode: Literal["sequentially", "simultaneously"]
    protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"]
    connection_timeout: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FastFallbackObject(FortiObject):
    """Typed FortiObject for FastFallback with field access."""
    name: str
    status: Literal["enable", "disable"]
    connection_mode: Literal["sequentially", "simultaneously"]
    protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"]
    connection_timeout: int


# ================================================================
# Main Endpoint Class
# ================================================================

class FastFallback:
    """
    
    Endpoint: web_proxy/fast_fallback
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
    ) -> FastFallbackObject: ...
    
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
    ) -> FortiObjectList[FastFallbackObject]: ...
    
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
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FastFallbackObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FastFallbackObject: ...

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
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
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
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
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
    "FastFallback",
    "FastFallbackPayload",
    "FastFallbackResponse",
    "FastFallbackObject",
]