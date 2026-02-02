""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: virtual_wan/interface_log
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

class InterfaceLogPayload(TypedDict, total=False):
    """Payload type for InterfaceLog operations."""
    interface: str
    since: int
    seconds: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InterfaceLogResponse(TypedDict, total=False):
    """Response type for InterfaceLog - use with .dict property for typed dict access."""
    interface: str
    since: int
    seconds: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InterfaceLogObject(FortiObject):
    """Typed FortiObject for InterfaceLog with field access."""
    interface: str
    since: int
    seconds: int


# ================================================================
# Main Endpoint Class
# ================================================================

class InterfaceLog:
    """
    
    Endpoint: virtual_wan/interface_log
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
        interface: str | None = ...,
        since: int | None = ...,
        seconds: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceLogObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InterfaceLogPayload | None = ...,
        interface: str | None = ...,
        since: int | None = ...,
        seconds: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceLogObject: ...


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
        payload_dict: InterfaceLogPayload | None = ...,
        interface: str | None = ...,
        since: int | None = ...,
        seconds: int | None = ...,
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
    "InterfaceLog",
    "InterfaceLogPayload",
    "InterfaceLogResponse",
    "InterfaceLogObject",
]