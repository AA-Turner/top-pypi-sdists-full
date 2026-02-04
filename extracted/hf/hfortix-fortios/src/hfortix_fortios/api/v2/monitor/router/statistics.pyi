""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/statistics
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

class StatisticsPayload(TypedDict, total=False):
    """Payload type for Statistics operations."""
    operator: Literal["and", "or"]
    ip_version: int
    ip_mask: str
    gateway: str
    type: str
    origin: str
    interface: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StatisticsResponse(TypedDict, total=False):
    """Response type for Statistics - use with .dict property for typed dict access."""
    operator: Literal["and", "or"]
    ip_version: int
    ip_mask: str
    gateway: str
    type: str
    origin: str
    interface: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StatisticsObject(FortiObject):
    """Typed FortiObject for Statistics with field access."""
    operator: Literal["and", "or"]
    ip_version: int
    ip_mask: str
    gateway: str
    type: str
    origin: str
    interface: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Statistics:
    """
    
    Endpoint: router/statistics
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
        ip_version: int | None = ...,
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
    ) -> StatisticsObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StatisticsPayload | None = ...,
        operator: Literal["and", "or"] | None = ...,
        ip_version: int | None = ...,
        ip_mask: str | None = ...,
        gateway: str | None = ...,
        type: str | None = ...,
        origin: str | None = ...,
        interface: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StatisticsObject: ...




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
        payload_dict: StatisticsPayload | None = ...,
        operator: Literal["and", "or"] | None = ...,
        ip_version: int | None = ...,
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
    "Statistics",
    "StatisticsPayload",
    "StatisticsResponse",
    "StatisticsObject",
]