"""
Child Table Helper Type Stubs for wireless-controller/inter-controller

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class InterControllerPeerDict(TypedDict, total=False):
    """Type definition for inter_controller_peer child table entry."""
    id: int | None
    peer_ip: str | None
    peer_port: int | None
    peer_priority: str | None


class InterControllerPeerObject(FortiObject):
    """Typed FortiObject for inter_controller_peer child table entry with attribute access."""
    id: int | None
    peer_ip: str | None
    peer_port: int | None
    peer_priority: str | None



class InterControllerPeerHelper:
    """Helper class for managing inter_controller_peer child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[InterControllerPeerObject] | InterControllerPeerObject | None: ...
    
    def set(
        self,
        id: int | None = ...,
        peer_ip: str | None = ...,
        peer_port: int | None = ...,
        peer_priority: str | None = ...,
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

