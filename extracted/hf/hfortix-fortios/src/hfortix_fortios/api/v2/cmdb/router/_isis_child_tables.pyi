"""
Child Table Helper Type Stubs for cmdb.router.isis

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject




class IsisNetHelper:
    """Helper class for managing isis_net child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
    ) -> list[IsisNetObject] | IsisNetObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IsisNetObject: ...
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IsisNetObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[IsisNetObject]: ...
    
    def exists(
        self,
        id: str,
    ) -> bool: ...


class IsisInterfaceHelper:
    """Helper class for managing isis_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
    ) -> list[IsisInterfaceObject] | IsisInterfaceObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IsisInterfaceObject: ...
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IsisInterfaceObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[IsisInterfaceObject]: ...
    
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


class SummaryAddress6Helper:
    """Helper class for managing summary_address6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
    ) -> list[SummaryAddress6Object] | SummaryAddress6Object | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SummaryAddress6Object: ...
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SummaryAddress6Object: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[SummaryAddress6Object]: ...
    
    def exists(
        self,
        id: str,
    ) -> bool: ...


class RedistributeHelper:
    """Helper class for managing redistribute child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        protocol: str | None = ...,
    ) -> list[RedistributeObject] | RedistributeObject | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RedistributeObject: ...
    
    def delete(
        self,
        protocol: str,
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
        protocol: str,
    ) -> bool: ...


class Redistribute6Helper:
    """Helper class for managing redistribute6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        protocol: str | None = ...,
    ) -> list[Redistribute6Object] | Redistribute6Object | None: ...
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Redistribute6Object: ...
    
    def delete(
        self,
        protocol: str,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Redistribute6Object: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> list[Redistribute6Object]: ...
    
    def exists(
        self,
        protocol: str,
    ) -> bool: ...

