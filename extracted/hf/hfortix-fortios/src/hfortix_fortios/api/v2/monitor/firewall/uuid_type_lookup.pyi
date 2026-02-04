""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/uuid_type_lookup
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

class UuidTypeLookupPayload(TypedDict, total=False):
    """Payload type for UuidTypeLookup operations."""
    uuids: list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UuidTypeLookupResponse(TypedDict, total=False):
    """Response type for UuidTypeLookup - use with .dict property for typed dict access."""
    uuids: list[str]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UuidTypeLookupObject(FortiObject):
    """Typed FortiObject for UuidTypeLookup with field access."""
    uuids: list[str]


# ================================================================
# Main Endpoint Class
# ================================================================

class UuidTypeLookup:
    """
    
    Endpoint: firewall/uuid_type_lookup
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
        uuids: list[str] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UuidTypeLookupObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UuidTypeLookupPayload | None = ...,
        uuids: list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UuidTypeLookupObject: ...




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
        payload_dict: UuidTypeLookupPayload | None = ...,
        uuids: list[str] | None = ...,
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
    "UuidTypeLookup",
    "UuidTypeLookupPayload",
    "UuidTypeLookupResponse",
    "UuidTypeLookupObject",
]