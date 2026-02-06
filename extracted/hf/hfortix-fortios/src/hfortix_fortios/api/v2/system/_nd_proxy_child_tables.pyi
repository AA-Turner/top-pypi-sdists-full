"""
Child Table Helper Type Stubs for system/nd-proxy

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class MemberDict(TypedDict, total=False):
    """Type definition for member child table entry."""
    interface_name: str | None


class MemberObject(FortiObject):
    """Typed FortiObject for member child table entry with attribute access."""
    interface_name: str | None



class MemberHelper:
    """Helper class for managing member child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        interface_name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[MemberObject] | MemberObject | None: ...
    
    def set(
        self,
        interface_name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        interface_name: str,
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
        interface_name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

