""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/device/purdue_level
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

class PurdueLevelPayload(TypedDict, total=False):
    """Payload type for PurdueLevel operations."""
    mac: str
    ip: str
    level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PurdueLevelResponse(TypedDict, total=False):
    """Response type for PurdueLevel - use with .dict property for typed dict access."""
    mac: str
    ip: str
    level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PurdueLevelObject(FortiObject):
    """Typed FortiObject for PurdueLevel with field access."""
    mac: str
    ip: str
    level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"]


# ================================================================
# Main Endpoint Class
# ================================================================

class PurdueLevel:
    """
    
    Endpoint: user/device/purdue_level
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
    ) -> PurdueLevelObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: PurdueLevelPayload | None = ...,
        mac: str | None = ...,
        ip: str | None = ...,
        level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PurdueLevelObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PurdueLevelPayload | None = ...,
        mac: str | None = ...,
        ip: str | None = ...,
        level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PurdueLevelObject: ...


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
        payload_dict: PurdueLevelPayload | None = ...,
        mac: str | None = ...,
        ip: str | None = ...,
        level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = ...,
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
    "PurdueLevel",
    "PurdueLevelPayload",
    "PurdueLevelResponse",
    "PurdueLevelObject",
]