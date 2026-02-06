"""
Child Table Helper Type Stubs for user/quarantine

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class TargetsDict(TypedDict, total=False):
    """Type definition for targets child table entry."""
    entry: str
    description: str | None
    macs: list[Any] | None


class TargetsObject(FortiObject):
    """Typed FortiObject for targets child table entry with attribute access."""
    entry: str
    description: str | None
    macs: list[Any] | None



class TargetsHelper:
    """Helper class for managing targets child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        entry: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[TargetsObject] | TargetsObject | None: ...
    
    def set(
        self,
        entry: str,
        description: str | None = ...,
        macs: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        entry: str,
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
        entry: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

