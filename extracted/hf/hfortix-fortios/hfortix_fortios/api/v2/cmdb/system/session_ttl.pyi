""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/session_ttl
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

class SessionTtlPortItem(TypedDict, total=False):
    """Nested item for port field."""
    id: int
    protocol: int
    start_port: int
    end_port: int
    timeout: str
    refresh_direction: Literal["both", "outgoing", "incoming"]


class SessionTtlPayload(TypedDict, total=False):
    """Payload type for SessionTtl operations."""
    default: str
    port: str | list[str] | list[SessionTtlPortItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SessionTtlResponse(TypedDict, total=False):
    """Response type for SessionTtl - use with .dict property for typed dict access."""
    default: str
    port: list[SessionTtlPortItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SessionTtlPortItemObject(FortiObject[SessionTtlPortItem]):
    """Typed object for port table items with attribute access."""
    id: int
    protocol: int
    start_port: int
    end_port: int
    timeout: str
    refresh_direction: Literal["both", "outgoing", "incoming"]


class SessionTtlObject(FortiObject):
    """Typed FortiObject for SessionTtl with field access."""
    default: str
    port: FortiObjectList[SessionTtlPortItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class SessionTtl:
    """
    
    Endpoint: system/session_ttl
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
    ) -> SessionTtlObject: ...
    
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
        payload_dict: SessionTtlPayload | None = ...,
        default: str | None = ...,
        port: str | list[str] | list[SessionTtlPortItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SessionTtlObject: ...


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
        payload_dict: SessionTtlPayload | None = ...,
        default: str | None = ...,
        port: str | list[str] | list[SessionTtlPortItem] | None = ...,
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
    "SessionTtl",
    "SessionTtlPayload",
    "SessionTtlResponse",
    "SessionTtlObject",
]