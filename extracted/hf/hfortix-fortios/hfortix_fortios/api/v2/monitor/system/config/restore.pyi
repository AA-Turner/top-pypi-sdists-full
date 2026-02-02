""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/config/restore
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

class RestorePayload(TypedDict, total=False):
    """Payload type for Restore operations."""
    source: Literal["upload", "usb", "revision"]
    usb_filename: str
    config_id: int
    password: str
    scope: Literal["global", "vdom"]
    vdom: str
    confirm_password_mask: bool
    file_content: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class RestoreResponse(TypedDict, total=False):
    """Response type for Restore - use with .dict property for typed dict access."""
    restore_started: bool
    error: str
    session_id: str
    config_restored: bool


class RestoreObject(FortiObject[RestoreResponse]):
    """Typed FortiObject for Restore with field access."""
    restore_started: bool
    error: str
    session_id: str
    config_restored: bool



# ================================================================
# Main Endpoint Class
# ================================================================

class Restore:
    """
    
    Endpoint: system/config/restore
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
    ) -> FortiObjectList[RestoreObject]: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: RestorePayload | None = ...,
        source: Literal["upload", "usb", "revision"] | None = ...,
        usb_filename: str | None = ...,
        config_id: int | None = ...,
        password: str | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        confirm_password_mask: bool | None = ...,
        file_content: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RestoreObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RestorePayload | None = ...,
        source: Literal["upload", "usb", "revision"] | None = ...,
        usb_filename: str | None = ...,
        config_id: int | None = ...,
        password: str | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        confirm_password_mask: bool | None = ...,
        file_content: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RestoreObject: ...


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
        payload_dict: RestorePayload | None = ...,
        source: Literal["upload", "usb", "revision"] | None = ...,
        usb_filename: str | None = ...,
        config_id: int | None = ...,
        password: str | None = ...,
        scope: Literal["global", "vdom"] | None = ...,
        confirm_password_mask: bool | None = ...,
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
    "Restore",
    "RestoreResponse",
    "RestoreObject",
]