"""
Child Table Helper Type Stubs for cmdb.router.ospf6

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject




class AreaHelper:
    """Helper class for managing area child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
    ) -> list[AreaObject] | AreaObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AreaObject: ...
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AreaObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[AreaObject]: ...
    
    def exists(
        self,
        id: str,
    ) -> bool: ...


class Ospf6InterfaceHelper:
    """Helper class for managing ospf6_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
    ) -> list[Ospf6InterfaceObject] | Ospf6InterfaceObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Ospf6InterfaceObject: ...
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Ospf6InterfaceObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[Ospf6InterfaceObject]: ...
    
    def exists(
        self,
        name: str,
    ) -> bool: ...


class RedistributeHelper:
    """Helper class for managing redistribute child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
    ) -> list[RedistributeObject] | RedistributeObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RedistributeObject: ...
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RedistributeObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[RedistributeObject]: ...
    
    def exists(
        self,
        name: str,
    ) -> bool: ...


class PassiveInterfaceHelper:
    """Helper class for managing passive_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
    ) -> list[PassiveInterfaceObject] | PassiveInterfaceObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PassiveInterfaceObject: ...
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PassiveInterfaceObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[PassiveInterfaceObject]: ...
    
    def exists(
        self,
        name: str,
    ) -> bool: ...


class SummaryAddressHelper:
    """Helper class for managing summary_address child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
    ) -> list[SummaryAddressObject] | SummaryAddressObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SummaryAddressObject: ...
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SummaryAddressObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[SummaryAddressObject]: ...
    
    def exists(
        self,
        id: str,
    ) -> bool: ...

