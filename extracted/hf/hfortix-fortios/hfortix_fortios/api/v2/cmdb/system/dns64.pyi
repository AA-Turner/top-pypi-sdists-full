""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/dns64
Category: cmdb
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

class Dns64Payload(TypedDict, total=False):
    """Payload type for Dns64 operations."""
    status: Literal["enable", "disable"]
    dns64_prefix: str
    always_synthesize_aaaa_record: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Dns64Response(TypedDict, total=False):
    """Response type for Dns64 - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    dns64_prefix: str
    always_synthesize_aaaa_record: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Dns64Object(FortiObject):
    """Typed FortiObject for Dns64 with field access."""
    status: Literal["enable", "disable"]
    dns64_prefix: str
    always_synthesize_aaaa_record: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Dns64:
    """
    
    Endpoint: system/dns64
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Dns64Object: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Dns64Payload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dns64_prefix: str | None = ...,
        always_synthesize_aaaa_record: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Dns64Object: ...


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
        payload_dict: Dns64Payload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dns64_prefix: str | None = ...,
        always_synthesize_aaaa_record: Literal["enable", "disable"] | None = ...,
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
    "Dns64",
    "Dns64Payload",
    "Dns64Response",
    "Dns64Object",
]