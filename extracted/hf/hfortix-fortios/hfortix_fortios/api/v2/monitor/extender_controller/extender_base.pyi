""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: extender_controller/extender
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

class ExtenderPayload(TypedDict, total=False):
    """Payload type for Extender operations."""
    fortiextender_name: list[str]
    type: Literal["system", "modem", "usage", "last"]


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class ExtenderResponse(TypedDict, total=False):
    """Response type for Extender - use with .dict property for typed dict access."""
    name: str
    id: str
    authorization_status_locked: bool
    system: str


class ExtenderObject(FortiObject[ExtenderResponse]):
    """Typed FortiObject for Extender with field access."""
    name: str
    id: str
    authorization_status_locked: bool
    system: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Extender:
    """
    
    Endpoint: extender_controller/extender
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
        fortiextender_name: list[str] | None = ...,
        type: Literal["system", "modem", "usage", "last"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[ExtenderObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ExtenderPayload | None = ...,
        fortiextender_name: list[str] | None = ...,
        type: Literal["system", "modem", "usage", "last"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExtenderObject: ...


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
        payload_dict: ExtenderPayload | None = ...,
        fortiextender_name: list[str] | None = ...,
        type: Literal["system", "modem", "usage", "last"] | None = ...,
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
    "Extender",
    "ExtenderResponse",
    "ExtenderObject",
]