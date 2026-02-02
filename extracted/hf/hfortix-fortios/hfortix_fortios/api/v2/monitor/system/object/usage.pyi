""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/object/usage
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

class UsagePayload(TypedDict, total=False):
    """Payload type for Usage operations."""
    q_path: str
    q_name: str
    qtypes: list[str]
    scope: Literal["vdom", "global"]
    mkey: str
    child_path: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UsageResponse(TypedDict, total=False):
    """Response type for Usage - use with .dict property for typed dict access."""
    q_path: str
    q_name: str
    qtypes: list[str]
    scope: Literal["vdom", "global"]
    mkey: str
    child_path: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UsageObject(FortiObject):
    """Typed FortiObject for Usage with field access."""
    q_path: str
    q_name: str
    qtypes: list[str]
    scope: Literal["vdom", "global"]
    child_path: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Usage:
    """
    
    Endpoint: system/object/usage
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
        q_path: str | None = ...,
        q_name: str | None = ...,
        qtypes: list[str] | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        mkey: str | None = ...,
        child_path: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UsageObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UsagePayload | None = ...,
        q_path: str | None = ...,
        q_name: str | None = ...,
        qtypes: list[str] | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        mkey: str | None = ...,
        child_path: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UsageObject: ...


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
        payload_dict: UsagePayload | None = ...,
        q_path: str | None = ...,
        q_name: str | None = ...,
        qtypes: list[str] | None = ...,
        scope: Literal["vdom", "global"] | None = ...,
        mkey: str | None = ...,
        child_path: str | None = ...,
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
    "Usage",
    "UsagePayload",
    "UsageResponse",
    "UsageObject",
]