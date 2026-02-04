""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wifi/spectrum/start
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

class StartPayload(TypedDict, total=False):
    """Payload type for Start operations."""
    wtp_id: str
    radio_id: int
    channels: list[str]
    duration: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StartResponse(TypedDict, total=False):
    """Response type for Start - use with .dict property for typed dict access."""
    wtp_id: str
    radio_id: int
    channels: list[str]
    duration: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StartObject(FortiObject):
    """Typed FortiObject for Start with field access."""
    wtp_id: str
    radio_id: int
    channels: list[str]
    duration: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Start:
    """
    
    Endpoint: wifi/spectrum/start
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
    ) -> StartObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: StartPayload | None = ...,
        wtp_id: str | None = ...,
        radio_id: int | None = ...,
        channels: list[str] | None = ...,
        duration: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StartObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StartPayload | None = ...,
        wtp_id: str | None = ...,
        radio_id: int | None = ...,
        channels: list[str] | None = ...,
        duration: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StartObject: ...




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
        payload_dict: StartPayload | None = ...,
        wtp_id: str | None = ...,
        radio_id: int | None = ...,
        channels: list[str] | None = ...,
        duration: int | None = ...,
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
    "Start",
    "StartPayload",
    "StartResponse",
    "StartObject",
]