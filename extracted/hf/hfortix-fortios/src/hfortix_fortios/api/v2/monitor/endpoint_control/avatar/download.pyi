""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: endpoint_control/avatar/download
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

class DownloadPayload(TypedDict, total=False):
    """Payload type for Download operations."""
    uid: str
    user: str
    fingerprint: str
    default: Literal["\u0027authuser\u0027", "\u0027unauthuser\u0027", "\u0027authuser_72\u0027", "\u0027unauthuser_72\u0027"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DownloadResponse(TypedDict, total=False):
    """Response type for Download - use with .dict property for typed dict access."""
    uid: str
    user: str
    fingerprint: str
    default: Literal["\u0027authuser\u0027", "\u0027unauthuser\u0027", "\u0027authuser_72\u0027", "\u0027unauthuser_72\u0027"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DownloadObject(FortiObject):
    """Typed FortiObject for Download with field access."""
    uid: str
    user: str
    fingerprint: str
    default: Literal["\u0027authuser\u0027", "\u0027unauthuser\u0027", "\u0027authuser_72\u0027", "\u0027unauthuser_72\u0027"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Download:
    """
    
    Endpoint: endpoint_control/avatar/download
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
        uid: str | None = ...,
        user: str | None = ...,
        fingerprint: str | None = ...,
        default: Literal["\u0027authuser\u0027", "\u0027unauthuser\u0027", "\u0027authuser_72\u0027", "\u0027unauthuser_72\u0027"] | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DownloadObject: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DownloadPayload | None = ...,
        uid: str | None = ...,
        user: str | None = ...,
        fingerprint: str | None = ...,
        default: Literal["\u0027authuser\u0027", "\u0027unauthuser\u0027", "\u0027authuser_72\u0027", "\u0027unauthuser_72\u0027"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DownloadObject: ...




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
        payload_dict: DownloadPayload | None = ...,
        uid: str | None = ...,
        user: str | None = ...,
        fingerprint: str | None = ...,
        default: Literal["\u0027authuser\u0027", "\u0027unauthuser\u0027", "\u0027authuser_72\u0027", "\u0027unauthuser_72\u0027"] | None = ...,
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
    "Download",
    "DownloadPayload",
    "DownloadResponse",
    "DownloadObject",
]