""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/auto_install
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

class AutoInstallPayload(TypedDict, total=False):
    """Payload type for AutoInstall operations."""
    auto_install_config: Literal["enable", "disable"]
    auto_install_image: Literal["enable", "disable"]
    default_config_file: str
    default_image_file: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AutoInstallResponse(TypedDict, total=False):
    """Response type for AutoInstall - use with .dict property for typed dict access."""
    auto_install_config: Literal["enable", "disable"]
    auto_install_image: Literal["enable", "disable"]
    default_config_file: str
    default_image_file: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AutoInstallObject(FortiObject):
    """Typed FortiObject for AutoInstall with field access."""
    auto_install_config: Literal["enable", "disable"]
    auto_install_image: Literal["enable", "disable"]
    default_config_file: str
    default_image_file: str


# ================================================================
# Main Endpoint Class
# ================================================================

class AutoInstall:
    """
    
    Endpoint: system/auto_install
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutoInstallObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AutoInstallPayload | None = ...,
        auto_install_config: Literal["enable", "disable"] | None = ...,
        auto_install_image: Literal["enable", "disable"] | None = ...,
        default_config_file: str | None = ...,
        default_image_file: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutoInstallObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AutoInstallPayload | None = ...,
        auto_install_config: Literal["enable", "disable"] | None = ...,
        auto_install_image: Literal["enable", "disable"] | None = ...,
        default_config_file: str | None = ...,
        default_image_file: str | None = ...,
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
    "AutoInstall",
    "AutoInstallPayload",
    "AutoInstallResponse",
    "AutoInstallObject",
]