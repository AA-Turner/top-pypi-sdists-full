"""
Child Table Helper Type Stubs for system/federated-upgrade

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class KnownHaMembersDict(TypedDict, total=False):
    """Type definition for known_ha_members child table entry."""
    serial: str

class NodeListDict(TypedDict, total=False):
    """Type definition for node_list child table entry."""
    serial: str
    timing: str
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: str
    allow_download: str | None
    coordinating_fortigate: str | None
    failure_reason: str | None


class KnownHaMembersObject(FortiObject):
    """Typed FortiObject for known_ha_members child table entry with attribute access."""
    serial: str


class NodeListObject(FortiObject):
    """Typed FortiObject for node_list child table entry with attribute access."""
    serial: str
    timing: str
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: str
    allow_download: str | None
    coordinating_fortigate: str | None
    failure_reason: str | None



class KnownHaMembersHelper:
    """Helper class for managing known_ha_members child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        serial: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[KnownHaMembersObject] | KnownHaMembersObject | None: ...
    
    def set(
        self,
        serial: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        serial: str,
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
        serial: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class NodeListHelper:
    """Helper class for managing node_list child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        serial: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NodeListObject] | NodeListObject | None: ...
    
    def set(
        self,
        serial: str,
        timing: str,
        maximum_minutes: int,
        time: str,
        setup_time: str,
        upgrade_path: str,
        device_type: str,
        allow_download: str | None = ...,
        coordinating_fortigate: str | None = ...,
        failure_reason: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        serial: str,
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
        serial: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

