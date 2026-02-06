"""
Child Table Helper Type Stubs for system/ptp

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class ServerInterfaceDict(TypedDict, total=False):
    """Type definition for server_interface child table entry."""
    id: int
    server_interface_name: str
    delay_mechanism: str | None


class ServerInterfaceObject(FortiObject):
    """Typed FortiObject for server_interface child table entry with attribute access."""
    id: int
    server_interface_name: str
    delay_mechanism: str | None



class ServerInterfaceHelper:
    """Helper class for managing server_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ServerInterfaceObject] | ServerInterfaceObject | None: ...
    
    def set(
        self,
        id: int,
        server_interface_name: str,
        delay_mechanism: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
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
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

