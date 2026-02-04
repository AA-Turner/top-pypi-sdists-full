""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/sdn_connector/nsx_security_tags
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

class NsxSecurityTagsPayload(TypedDict, total=False):
    """Payload type for NsxSecurityTags operations."""
    mkey: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class NsxSecurityTagsResponse(TypedDict, total=False):
    """Response type for NsxSecurityTags - use with .dict property for typed dict access."""
    mkey: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class NsxSecurityTagsObject(FortiObject):
    """Typed FortiObject for NsxSecurityTags with field access."""


# ================================================================
# Main Endpoint Class
# ================================================================

class NsxSecurityTags:
    """
    
    Endpoint: system/sdn_connector/nsx_security_tags
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
        mkey: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NsxSecurityTagsObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: NsxSecurityTagsPayload | None = ...,
        mkey: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NsxSecurityTagsObject: ...




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
        payload_dict: NsxSecurityTagsPayload | None = ...,
        mkey: str | None = ...,
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
    "NsxSecurityTags",
    "NsxSecurityTagsPayload",
    "NsxSecurityTagsResponse",
    "NsxSecurityTagsObject",
]