""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: log/gui_display
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

class GuiDisplayPayload(TypedDict, total=False):
    """Payload type for GuiDisplay operations."""
    resolve_hosts: Literal["enable", "disable"]
    resolve_apps: Literal["enable", "disable"]
    fortiview_unscanned_apps: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class GuiDisplayResponse(TypedDict, total=False):
    """Response type for GuiDisplay - use with .dict property for typed dict access."""
    resolve_hosts: Literal["enable", "disable"]
    resolve_apps: Literal["enable", "disable"]
    fortiview_unscanned_apps: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class GuiDisplayObject(FortiObject):
    """Typed FortiObject for GuiDisplay with field access."""
    resolve_hosts: Literal["enable", "disable"]
    resolve_apps: Literal["enable", "disable"]
    fortiview_unscanned_apps: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class GuiDisplay:
    """
    
    Endpoint: log/gui_display
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
    ) -> GuiDisplayObject: ...
    
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
        payload_dict: GuiDisplayPayload | None = ...,
        resolve_hosts: Literal["enable", "disable"] | None = ...,
        resolve_apps: Literal["enable", "disable"] | None = ...,
        fortiview_unscanned_apps: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> GuiDisplayObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


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
        payload_dict: GuiDisplayPayload | None = ...,
        resolve_hosts: Literal["enable", "disable"] | None = ...,
        resolve_apps: Literal["enable", "disable"] | None = ...,
        fortiview_unscanned_apps: Literal["enable", "disable"] | None = ...,
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
    "GuiDisplay",
    "GuiDisplayPayload",
    "GuiDisplayResponse",
    "GuiDisplayObject",
]