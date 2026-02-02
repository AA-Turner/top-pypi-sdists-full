""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: web_ui/custom_language/update
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

class UpdatePayload(TypedDict, total=False):
    """Payload type for Update operations."""
    mkey: str
    lang_name: str
    lang_comments: str
    file_content: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UpdateResponse(TypedDict, total=False):
    """Response type for Update - use with .dict property for typed dict access."""
    mkey: str
    lang_name: str
    lang_comments: str
    file_content: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UpdateObject(FortiObject):
    """Typed FortiObject for Update with field access."""
    lang_name: str
    lang_comments: str
    file_content: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Update:
    """
    
    Endpoint: web_ui/custom_language/update
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
    ) -> UpdateObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: UpdatePayload | None = ...,
        mkey: str | None = ...,
        lang_name: str | None = ...,
        lang_comments: str | None = ...,
        file_content: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UpdateObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UpdatePayload | None = ...,
        mkey: str | None = ...,
        lang_name: str | None = ...,
        lang_comments: str | None = ...,
        file_content: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UpdateObject: ...


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
        payload_dict: UpdatePayload | None = ...,
        mkey: str | None = ...,
        lang_name: str | None = ...,
        lang_comments: str | None = ...,
        file_content: str | None = ...,
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
    "Update",
    "UpdatePayload",
    "UpdateResponse",
    "UpdateObject",
]