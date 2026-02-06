"""
Child Table Helper Type Stubs for switch-controller/flow-tracking

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class CollectorsDict(TypedDict, total=False):
    """Type definition for collectors child table entry."""
    name: str | None
    ip: str | None
    port: int | None
    transport: str | None

class AggregatesDict(TypedDict, total=False):
    """Type definition for aggregates child table entry."""
    id: int | None
    ip: str


class CollectorsObject(FortiObject):
    """Typed FortiObject for collectors child table entry with attribute access."""
    name: str | None
    ip: str | None
    port: int | None
    transport: str | None


class AggregatesObject(FortiObject):
    """Typed FortiObject for aggregates child table entry with attribute access."""
    id: int | None
    ip: str



class CollectorsHelper:
    """Helper class for managing collectors child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[CollectorsObject] | CollectorsObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        transport: str | None = ...,
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


class AggregatesHelper:
    """Helper class for managing aggregates child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AggregatesObject] | AggregatesObject | None: ...
    
    def set(
        self,
        ip: str,
        id: int | None = ...,
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

