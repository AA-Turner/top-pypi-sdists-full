"""
Child Table Helper Type Stubs for system/central-management

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class ServerListDict(TypedDict, total=False):
    """Type definition for server_list child table entry."""
    id: int | None
    server_type: str
    addr_type: str | None
    server_address: str
    server_address6: str
    fqdn: str


class ServerListObject(FortiObject):
    """Typed FortiObject for server_list child table entry with attribute access."""
    id: int | None
    server_type: str
    addr_type: str | None
    server_address: str
    server_address6: str
    fqdn: str



class ServerListHelper:
    """Helper class for managing server_list child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ServerListObject] | ServerListObject | None: ...
    
    def set(
        self,
        server_type: str,
        server_address: str,
        server_address6: str,
        fqdn: str,
        id: int | None = ...,
        addr_type: str | None = ...,
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

