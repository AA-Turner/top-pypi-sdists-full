""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/interface
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

class InterfacePayload(TypedDict, total=False):
    """Payload type for Interface operations."""
    interface_name: str
    include_vlan: bool
    include_aggregate: bool
    scope: Literal["vdom", "global"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InterfaceResponse(TypedDict, total=False):
    """Response type for Interface - use with .dict property for typed dict access."""
    interface_name: str
    include_vlan: bool
    include_aggregate: bool
    scope: Literal["vdom", "global"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InterfaceObject(FortiObject):
    """Typed FortiObject for Interface with field access."""
    interface_name: str
    include_vlan: bool
    include_aggregate: bool
    scope: Literal["vdom", "global"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Interface:
    """
    
    Endpoint: system/interface
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
        interface_name: str | None = ...,
        include_vlan: bool | None = ...,
        include_aggregate: bool | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InterfacePayload | None = ...,
        interface_name: str | None = ...,
        include_vlan: bool | None = ...,
        include_aggregate: bool | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceObject: ...


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
        payload_dict: InterfacePayload | None = ...,
        interface_name: str | None = ...,
        include_vlan: bool | None = ...,
        include_aggregate: bool | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
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
    "Interface",
    "InterfacePayload",
    "InterfaceResponse",
    "InterfaceObject",
]