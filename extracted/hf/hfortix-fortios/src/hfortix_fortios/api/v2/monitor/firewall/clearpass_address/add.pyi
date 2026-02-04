""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/clearpass_address/add
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

class AddPayload(TypedDict, total=False):
    """Payload type for Add operations."""
    endpoint_ip: list[str]
    spt: Literal["healthy", "checkup", "transient", "quarantine", "infected", "unknown"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AddResponse(TypedDict, total=False):
    """Response type for Add - use with .dict property for typed dict access."""
    endpoint_ip: list[str]
    spt: Literal["healthy", "checkup", "transient", "quarantine", "infected", "unknown"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AddObject(FortiObject):
    """Typed FortiObject for Add with field access."""
    endpoint_ip: list[str]
    spt: Literal["healthy", "checkup", "transient", "quarantine", "infected", "unknown"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Add:
    """
    
    Endpoint: firewall/clearpass_address/add
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
    ) -> AddObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: AddPayload | None = ...,
        endpoint_ip: list[str] | None = ...,
        spt: Literal["healthy", "checkup", "transient", "quarantine", "infected", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AddPayload | None = ...,
        endpoint_ip: list[str] | None = ...,
        spt: Literal["healthy", "checkup", "transient", "quarantine", "infected", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddObject: ...




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
        payload_dict: AddPayload | None = ...,
        endpoint_ip: list[str] | None = ...,
        spt: Literal["healthy", "checkup", "transient", "quarantine", "infected", "unknown"] | None = ...,
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
    "Add",
    "AddPayload",
    "AddResponse",
    "AddObject",
]