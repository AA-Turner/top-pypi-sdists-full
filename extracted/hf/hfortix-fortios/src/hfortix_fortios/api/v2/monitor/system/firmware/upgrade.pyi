""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/firmware/upgrade
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

class UpgradePayload(TypedDict, total=False):
    """Payload type for Upgrade operations."""
    source: Literal["upload", "usb", "fortiguard", "url"]
    url: str
    passphrase: str
    force: bool
    filename: str
    format_partition: bool
    ignore_invalid_signature: bool
    file_id: str
    ignore_admin_lockout_upon_downgrade: bool
    file_content: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UpgradeResponse(TypedDict, total=False):
    """Response type for Upgrade - use with .dict property for typed dict access."""
    source: Literal["upload", "usb", "fortiguard", "url"]
    url: str
    passphrase: str
    force: bool
    filename: str
    format_partition: bool
    ignore_invalid_signature: bool
    file_id: str
    ignore_admin_lockout_upon_downgrade: bool
    file_content: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UpgradeObject(FortiObject):
    """Typed FortiObject for Upgrade with field access."""
    source: Literal["upload", "usb", "fortiguard", "url"]
    url: str
    passphrase: str
    force: bool
    filename: str
    format_partition: bool
    ignore_invalid_signature: bool
    file_id: str
    ignore_admin_lockout_upon_downgrade: bool
    file_content: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Upgrade:
    """
    
    Endpoint: system/firmware/upgrade
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
    ) -> UpgradeObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: UpgradePayload | None = ...,
        source: Literal["upload", "usb", "fortiguard", "url"] | None = ...,
        url: str | None = ...,
        passphrase: str | None = ...,
        force: bool | None = ...,
        filename: str | None = ...,
        format_partition: bool | None = ...,
        ignore_invalid_signature: bool | None = ...,
        file_id: str | None = ...,
        ignore_admin_lockout_upon_downgrade: bool | None = ...,
        file_content: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UpgradeObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UpgradePayload | None = ...,
        source: Literal["upload", "usb", "fortiguard", "url"] | None = ...,
        url: str | None = ...,
        passphrase: str | None = ...,
        force: bool | None = ...,
        filename: str | None = ...,
        format_partition: bool | None = ...,
        ignore_invalid_signature: bool | None = ...,
        file_id: str | None = ...,
        ignore_admin_lockout_upon_downgrade: bool | None = ...,
        file_content: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UpgradeObject: ...




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
        payload_dict: UpgradePayload | None = ...,
        source: Literal["upload", "usb", "fortiguard", "url"] | None = ...,
        url: str | None = ...,
        passphrase: str | None = ...,
        force: bool | None = ...,
        filename: str | None = ...,
        format_partition: bool | None = ...,
        ignore_invalid_signature: bool | None = ...,
        file_id: str | None = ...,
        ignore_admin_lockout_upon_downgrade: bool | None = ...,
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
    "Upgrade",
    "UpgradePayload",
    "UpgradeResponse",
    "UpgradeObject",
]