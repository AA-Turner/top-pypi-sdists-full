""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/banned/add_users
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

class AddUsersPayload(TypedDict, total=False):
    """Payload type for AddUsers operations."""
    ip_addresses: list[str]
    expiry: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AddUsersResponse(TypedDict, total=False):
    """Response type for AddUsers - use with .dict property for typed dict access."""
    ip_addresses: list[str]
    expiry: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AddUsersObject(FortiObject):
    """Typed FortiObject for AddUsers with field access."""
    ip_addresses: list[str]
    expiry: int


# ================================================================
# Main Endpoint Class
# ================================================================

class AddUsers:
    """
    
    Endpoint: user/banned/add_users
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
    ) -> AddUsersObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: AddUsersPayload | None = ...,
        ip_addresses: list[str] | None = ...,
        expiry: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddUsersObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AddUsersPayload | None = ...,
        ip_addresses: list[str] | None = ...,
        expiry: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddUsersObject: ...




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
        payload_dict: AddUsersPayload | None = ...,
        ip_addresses: list[str] | None = ...,
        expiry: int | None = ...,
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
    "AddUsers",
    "AddUsersPayload",
    "AddUsersResponse",
    "AddUsersObject",
]