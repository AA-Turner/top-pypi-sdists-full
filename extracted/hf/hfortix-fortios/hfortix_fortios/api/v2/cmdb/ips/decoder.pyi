""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ips/decoder
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class DecoderParameterItem(TypedDict, total=False):
    """Nested item for parameter field."""
    name: str
    value: str


class DecoderPayload(TypedDict, total=False):
    """Payload type for Decoder operations."""
    name: str
    parameter: str | list[str] | list[DecoderParameterItem]
    status: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DecoderResponse(TypedDict, total=False):
    """Response type for Decoder - use with .dict property for typed dict access."""
    name: str
    parameter: list[DecoderParameterItem]
    status: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DecoderParameterItemObject(FortiObject[DecoderParameterItem]):
    """Typed object for parameter table items with attribute access."""
    name: str
    value: str


class DecoderObject(FortiObject):
    """Typed FortiObject for Decoder with field access."""
    name: str
    parameter: FortiObjectList[DecoderParameterItemObject]
    status: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Decoder:
    """
    
    Endpoint: ips/decoder
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DecoderObject: ...
    
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[DecoderObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...




    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DecoderPayload | None = ...,
        name: str | None = ...,
        parameter: str | list[str] | list[DecoderParameterItem] | None = ...,
        status: str | None = ...,
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
    "Decoder",
    "DecoderPayload",
    "DecoderResponse",
    "DecoderObject",
]