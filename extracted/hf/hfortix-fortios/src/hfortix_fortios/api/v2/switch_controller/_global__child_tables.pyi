"""
Child Table Helper Type Stubs for switch-controller/global

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class DisableDiscoveryDict(TypedDict, total=False):
    """Type definition for disable_discovery child table entry."""
    name: str | None

class CustomCommandDict(TypedDict, total=False):
    """Type definition for custom_command child table entry."""
    command_entry: str | None
    command_name: str


class DisableDiscoveryObject(FortiObject):
    """Typed FortiObject for disable_discovery child table entry with attribute access."""
    name: str | None


class CustomCommandObject(FortiObject):
    """Typed FortiObject for custom_command child table entry with attribute access."""
    command_entry: str | None
    command_name: str



class DisableDiscoveryHelper:
    """Helper class for managing disable_discovery child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[DisableDiscoveryObject] | DisableDiscoveryObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class CustomCommandHelper:
    """Helper class for managing custom_command child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        command_entry: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[CustomCommandObject] | CustomCommandObject | None: ...
    
    def set(
        self,
        command_name: str,
        command_entry: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        command_entry: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        command_entry: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

