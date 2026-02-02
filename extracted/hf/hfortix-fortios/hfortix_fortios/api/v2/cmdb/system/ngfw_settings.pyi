""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ngfw_settings
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

class NgfwSettingsPayload(TypedDict, total=False):
    """Payload type for NgfwSettings operations."""
    match_timeout: int
    tcp_match_timeout: int
    tcp_halfopen_match_timeout: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class NgfwSettingsResponse(TypedDict, total=False):
    """Response type for NgfwSettings - use with .dict property for typed dict access."""
    match_timeout: int
    tcp_match_timeout: int
    tcp_halfopen_match_timeout: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class NgfwSettingsObject(FortiObject):
    """Typed FortiObject for NgfwSettings with field access."""
    match_timeout: int
    tcp_match_timeout: int
    tcp_halfopen_match_timeout: int


# ================================================================
# Main Endpoint Class
# ================================================================

class NgfwSettings:
    """
    
    Endpoint: system/ngfw_settings
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NgfwSettingsObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: NgfwSettingsPayload | None = ...,
        match_timeout: int | None = ...,
        tcp_match_timeout: int | None = ...,
        tcp_halfopen_match_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NgfwSettingsObject: ...


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
        payload_dict: NgfwSettingsPayload | None = ...,
        match_timeout: int | None = ...,
        tcp_match_timeout: int | None = ...,
        tcp_halfopen_match_timeout: int | None = ...,
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
    "NgfwSettings",
    "NgfwSettingsPayload",
    "NgfwSettingsResponse",
    "NgfwSettingsObject",
]