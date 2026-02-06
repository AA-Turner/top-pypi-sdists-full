"""
Child Table Helper Type Stubs for system/ipam

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class PoolsDict(TypedDict, total=False):
    """Type definition for pools child table entry."""
    name: str
    description: str | None
    subnet: str
    exclude: list[Any] | None

class RulesDict(TypedDict, total=False):
    """Type definition for rules child table entry."""
    name: str
    description: str | None
    device: list[Any]
    interface: list[Any]
    role: str | None
    pool: list[Any]
    dhcp: str | None


class PoolsObject(FortiObject):
    """Typed FortiObject for pools child table entry with attribute access."""
    name: str
    description: str | None
    subnet: str
    exclude: list[Any] | None


class RulesObject(FortiObject):
    """Typed FortiObject for rules child table entry with attribute access."""
    name: str
    description: str | None
    device: list[Any]
    interface: list[Any]
    role: str | None
    pool: list[Any]
    dhcp: str | None



class PoolsHelper:
    """Helper class for managing pools child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[PoolsObject] | PoolsObject | None: ...
    
    def set(
        self,
        name: str,
        subnet: str,
        description: str | None = ...,
        exclude: list[Any] | None = ...,
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


class RulesHelper:
    """Helper class for managing rules child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[RulesObject] | RulesObject | None: ...
    
    def set(
        self,
        name: str,
        device: list[Any],
        interface: list[Any],
        pool: list[Any],
        description: str | None = ...,
        role: str | None = ...,
        dhcp: str | None = ...,
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

