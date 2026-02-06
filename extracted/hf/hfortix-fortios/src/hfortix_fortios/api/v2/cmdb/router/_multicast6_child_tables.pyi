"""
Child Table Helper Type Stubs for cmdb.router.multicast6

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject




class InterfaceHelper:
    """Helper class for managing interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
    ) -> list[InterfaceObject] | InterfaceObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceObject: ...
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterfaceObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[InterfaceObject]: ...
    
    def exists(
        self,
        name: str,
    ) -> bool: ...

