"""
Child Table Helper Type Stubs for router/bfd6

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class NeighborDict(TypedDict, total=False):
    """Type definition for neighbor child table entry."""
    ip6_address: str
    interface: str

class MultihopTemplateDict(TypedDict, total=False):
    """Type definition for multihop_template child table entry."""
    id: int
    src: str
    dst: str
    bfd_desired_min_tx: int | None
    bfd_required_min_rx: int | None
    bfd_detect_mult: int | None
    auth_mode: str | None
    md5_key: str | None


class NeighborObject(FortiObject):
    """Typed FortiObject for neighbor child table entry with attribute access."""
    ip6_address: str
    interface: str


class MultihopTemplateObject(FortiObject):
    """Typed FortiObject for multihop_template child table entry with attribute access."""
    id: int
    src: str
    dst: str
    bfd_desired_min_tx: int | None
    bfd_required_min_rx: int | None
    bfd_detect_mult: int | None
    auth_mode: str | None
    md5_key: str | None



class NeighborHelper:
    """Helper class for managing neighbor child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        ip6_address: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NeighborObject] | NeighborObject | None: ...
    
    def set(
        self,
        ip6_address: str,
        interface: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        ip6_address: str,
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
        ip6_address: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class MultihopTemplateHelper:
    """Helper class for managing multihop_template child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[MultihopTemplateObject] | MultihopTemplateObject | None: ...
    
    def set(
        self,
        id: int,
        src: str,
        dst: str,
        bfd_desired_min_tx: int | None = ...,
        bfd_required_min_rx: int | None = ...,
        bfd_detect_mult: int | None = ...,
        auth_mode: str | None = ...,
        md5_key: str | None = ...,
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

