""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/csf
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

class CsfPayload(TypedDict, total=False):
    """Payload type for Csf operations."""
    scope: Literal["vdom", "global"]
    all_vdoms: bool


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class CsfResponse(TypedDict, total=False):
    """Response type for Csf - use with .dict property for typed dict access."""
    protocol_enabled: bool
    csf_group_name: str
    pending: list[str]
    trusted: list[str]
    devices: str
    faceplate_map: str


class CsfObject(FortiObject[CsfResponse]):
    """Typed FortiObject for Csf with field access."""
    protocol_enabled: bool
    csf_group_name: str
    pending: list[str]
    trusted: list[str]
    devices: str
    faceplate_map: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Csf:
    """
    
    Endpoint: system/csf
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
        scope: Literal["vdom", "global"] | None = ...,
        all_vdoms: bool | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[CsfObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CsfPayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        all_vdoms: bool | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CsfObject: ...


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
        payload_dict: CsfPayload | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        all_vdoms: bool | None = ...,
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
    "Csf",
    "CsfResponse",
    "CsfObject",
]