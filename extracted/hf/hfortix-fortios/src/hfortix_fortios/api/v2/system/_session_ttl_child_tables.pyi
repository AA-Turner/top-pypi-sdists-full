"""
Child Table Helper Type Stubs for system/session-ttl

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class PortDict(TypedDict, total=False):
    """Type definition for port child table entry."""
    id: int
    protocol: int
    start_port: int
    end_port: int
    timeout: str | None
    refresh_direction: str | None


class PortObject(FortiObject):
    """Typed FortiObject for port child table entry with attribute access."""
    id: int
    protocol: int
    start_port: int
    end_port: int
    timeout: str | None
    refresh_direction: str | None



class PortHelper:
    """Helper class for managing port child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[PortObject] | PortObject | None: ...
    
    def set(
        self,
        id: int,
        protocol: int,
        start_port: int,
        end_port: int,
        timeout: str | None = ...,
        refresh_direction: str | None = ...,
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

