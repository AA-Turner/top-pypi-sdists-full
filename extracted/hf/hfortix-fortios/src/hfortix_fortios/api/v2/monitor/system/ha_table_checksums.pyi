""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ha_table_checksums
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

class HaTableChecksumsPayload(TypedDict, total=False):
    """Payload type for HaTableChecksums operations."""
    serial_no: str
    vdom_name: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class HaTableChecksumsResponse(TypedDict, total=False):
    """Response type for HaTableChecksums - use with .dict property for typed dict access."""
    serial_no: str
    tables: str


class HaTableChecksumsObject(FortiObject[HaTableChecksumsResponse]):
    """Typed FortiObject for HaTableChecksums with field access."""
    serial_no: str
    tables: str



# ================================================================
# Main Endpoint Class
# ================================================================

class HaTableChecksums:
    """
    
    Endpoint: system/ha_table_checksums
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
        serial_no: str,
        vdom_name: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[HaTableChecksumsObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: HaTableChecksumsPayload | None = ...,
        serial_no: str | None = ...,
        vdom_name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HaTableChecksumsObject: ...




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
        payload_dict: HaTableChecksumsPayload | None = ...,
        serial_no: str | None = ...,
        vdom_name: str | None = ...,
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
    "HaTableChecksums",
    "HaTableChecksumsResponse",
    "HaTableChecksumsObject",
]