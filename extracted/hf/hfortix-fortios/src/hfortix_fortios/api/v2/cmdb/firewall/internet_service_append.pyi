""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_append
Category: cmdb
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

class InternetServiceAppendPayload(TypedDict, total=False):
    """Payload type for InternetServiceAppend operations."""
    addr_mode: Literal["ipv4", "ipv6", "both"]
    match_port: int
    append_port: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InternetServiceAppendResponse(TypedDict, total=False):
    """Response type for InternetServiceAppend - use with .dict property for typed dict access."""
    addr_mode: Literal["ipv4", "ipv6", "both"]
    match_port: int
    append_port: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InternetServiceAppendObject(FortiObject):
    """Typed FortiObject for InternetServiceAppend with field access."""
    addr_mode: Literal["ipv4", "ipv6", "both"]
    match_port: int
    append_port: int


# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceAppend:
    """
    
    Endpoint: firewall/internet_service_append
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceAppendObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceAppendPayload | None = ...,
        addr_mode: Literal["ipv4", "ipv6", "both"] | None = ...,
        match_port: int | None = ...,
        append_port: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceAppendObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServiceAppendPayload | None = ...,
        addr_mode: Literal["ipv4", "ipv6", "both"] | None = ...,
        match_port: int | None = ...,
        append_port: int | None = ...,
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
    "InternetServiceAppend",
    "InternetServiceAppendPayload",
    "InternetServiceAppendResponse",
    "InternetServiceAppendObject",
]