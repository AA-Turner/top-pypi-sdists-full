"""
Child Table Helper Type Stubs for system/sflow

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class CollectorsDict(TypedDict, total=False):
    """Type definition for collectors child table entry."""
    id: int
    collector_ip: str
    collector_port: int | None
    source_ip: str | None
    interface_select_method: str | None
    interface: str


class CollectorsObject(FortiObject):
    """Typed FortiObject for collectors child table entry with attribute access."""
    id: int
    collector_ip: str
    collector_port: int | None
    source_ip: str | None
    interface_select_method: str | None
    interface: str



class CollectorsHelper:
    """Helper class for managing collectors child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[CollectorsObject] | CollectorsObject | None: ...
    
    def set(
        self,
        id: int,
        collector_ip: str,
        interface: str,
        collector_port: int | None = ...,
        source_ip: str | None = ...,
        interface_select_method: str | None = ...,
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

