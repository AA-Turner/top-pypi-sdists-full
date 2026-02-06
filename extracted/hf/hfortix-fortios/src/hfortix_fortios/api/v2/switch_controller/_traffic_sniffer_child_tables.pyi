"""
Child Table Helper Type Stubs for switch-controller/traffic-sniffer

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class TargetMacDict(TypedDict, total=False):
    """Type definition for target_mac child table entry."""
    mac: str
    description: str | None

class TargetIpDict(TypedDict, total=False):
    """Type definition for target_ip child table entry."""
    ip: str
    description: str | None

class TargetPortDict(TypedDict, total=False):
    """Type definition for target_port child table entry."""
    switch_id: str
    description: str | None
    in_ports: list[Any] | None
    out_ports: list[Any] | None


class TargetMacObject(FortiObject):
    """Typed FortiObject for target_mac child table entry with attribute access."""
    mac: str
    description: str | None


class TargetIpObject(FortiObject):
    """Typed FortiObject for target_ip child table entry with attribute access."""
    ip: str
    description: str | None


class TargetPortObject(FortiObject):
    """Typed FortiObject for target_port child table entry with attribute access."""
    switch_id: str
    description: str | None
    in_ports: list[Any] | None
    out_ports: list[Any] | None



class TargetMacHelper:
    """Helper class for managing target_mac child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        mac: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[TargetMacObject] | TargetMacObject | None: ...
    
    def set(
        self,
        mac: str,
        description: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        mac: str,
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
        mac: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class TargetIpHelper:
    """Helper class for managing target_ip child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        ip: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[TargetIpObject] | TargetIpObject | None: ...
    
    def set(
        self,
        ip: str,
        description: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        ip: str,
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
        ip: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class TargetPortHelper:
    """Helper class for managing target_port child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        switch_id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[TargetPortObject] | TargetPortObject | None: ...
    
    def set(
        self,
        switch_id: str,
        description: str | None = ...,
        in_ports: list[Any] | None = ...,
        out_ports: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        switch_id: str,
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
        switch_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

