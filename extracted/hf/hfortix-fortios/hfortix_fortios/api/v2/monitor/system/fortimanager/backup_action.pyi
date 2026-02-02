""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/fortimanager/backup_action
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

class BackupActionPayload(TypedDict, total=False):
    """Payload type for BackupAction operations."""
    operation: Literal["import", "update"]
    objects: list[str]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class BackupActionResponse(TypedDict, total=False):
    """Response type for BackupAction - use with .dict property for typed dict access."""
    operation: Literal["import", "update"]
    objects: list[str]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class BackupActionObject(FortiObject):
    """Typed FortiObject for BackupAction with field access."""
    operation: Literal["import", "update"]
    objects: list[str]


# ================================================================
# Main Endpoint Class
# ================================================================

class BackupAction:
    """
    
    Endpoint: system/fortimanager/backup_action
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
    ) -> BackupActionObject: ...
    

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: BackupActionPayload | None = ...,
        operation: Literal["import", "update"] | None = ...,
        objects: list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BackupActionObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: BackupActionPayload | None = ...,
        operation: Literal["import", "update"] | None = ...,
        objects: list[str] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> BackupActionObject: ...


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
        payload_dict: BackupActionPayload | None = ...,
        operation: Literal["import", "update"] | None = ...,
        objects: list[str] | None = ...,
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
    "BackupAction",
    "BackupActionPayload",
    "BackupActionResponse",
    "BackupActionObject",
]