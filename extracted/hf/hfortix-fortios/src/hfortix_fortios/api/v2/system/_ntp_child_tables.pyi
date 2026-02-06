"""
Child Table Helper Type Stubs for system/ntp

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class NtpserverDict(TypedDict, total=False):
    """Type definition for ntpserver child table entry."""
    id: int
    server: str
    ntpv3: str | None
    authentication: str | None
    key_type: str | None
    key: str
    key_id: int
    ip_type: str | None
    interface_select_method: str | None
    interface: str
    vrf_select: int | None

class InterfaceDict(TypedDict, total=False):
    """Type definition for interface child table entry."""
    interface_name: str


class NtpserverObject(FortiObject):
    """Typed FortiObject for ntpserver child table entry with attribute access."""
    id: int
    server: str
    ntpv3: str | None
    authentication: str | None
    key_type: str | None
    key: str
    key_id: int
    ip_type: str | None
    interface_select_method: str | None
    interface: str
    vrf_select: int | None


class InterfaceObject(FortiObject):
    """Typed FortiObject for interface child table entry with attribute access."""
    interface_name: str



class NtpserverHelper:
    """Helper class for managing ntpserver child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NtpserverObject] | NtpserverObject | None: ...
    
    def set(
        self,
        id: int,
        server: str,
        key: str,
        key_id: int,
        interface: str,
        ntpv3: str | None = ...,
        authentication: str | None = ...,
        key_type: str | None = ...,
        ip_type: str | None = ...,
        interface_select_method: str | None = ...,
        vrf_select: int | None = ...,
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


class InterfaceHelper:
    """Helper class for managing interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        interface_name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[InterfaceObject] | InterfaceObject | None: ...
    
    def set(
        self,
        interface_name: str,
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

