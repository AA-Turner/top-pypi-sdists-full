""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wifi/interfering_ap
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

class InterferingApPayload(TypedDict, total=False):
    """Payload type for InterferingAp operations."""
    wtp: str
    radio: int


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class InterferingApResponse(TypedDict, total=False):
    """Response type for InterferingAp - use with .dict property for typed dict access."""
    mac: str
    channel: int
    ssid: str
    signal: int
    is_infra_ssid: bool


class InterferingApObject(FortiObject[InterferingApResponse]):
    """Typed FortiObject for InterferingAp with field access."""
    mac: str
    channel: int
    ssid: str
    signal: int
    is_infra_ssid: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class InterferingAp:
    """
    
    Endpoint: wifi/interfering_ap
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
        wtp: str | None = ...,
        radio: int | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[InterferingApObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InterferingApPayload | None = ...,
        wtp: str | None = ...,
        radio: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterferingApObject: ...




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
        payload_dict: InterferingApPayload | None = ...,
        wtp: str | None = ...,
        radio: int | None = ...,
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
    "InterferingAp",
    "InterferingApResponse",
    "InterferingApObject",
]