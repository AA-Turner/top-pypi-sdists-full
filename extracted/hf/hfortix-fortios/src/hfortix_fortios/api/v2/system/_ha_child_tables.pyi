"""
Child Table Helper Type Stubs for system/ha

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class AutoVirtualMacInterfaceDict(TypedDict, total=False):
    """Type definition for auto_virtual_mac_interface child table entry."""
    interface_name: str

class BackupHbdevDict(TypedDict, total=False):
    """Type definition for backup_hbdev child table entry."""
    name: str | None

class HaMgmtInterfacesDict(TypedDict, total=False):
    """Type definition for ha_mgmt_interfaces child table entry."""
    id: int | None
    interface: str
    dst: str | None
    gateway: str | None
    dst6: str | None
    gateway6: str | None

class UnicastPeersDict(TypedDict, total=False):
    """Type definition for unicast_peers child table entry."""
    id: int | None
    peer_ip: str | None

class VclusterDict(TypedDict, total=False):
    """Type definition for vcluster child table entry."""
    vcluster_id: int | None
    override: str | None
    priority: int | None
    override_wait_time: int | None
    monitor: str | None
    pingserver_monitor_interface: str | None
    pingserver_failover_threshold: int | None
    pingserver_secondary_force_reset: str | None
    pingserver_flip_timeout: int | None
    vdom: list[Any] | None


class AutoVirtualMacInterfaceObject(FortiObject):
    """Typed FortiObject for auto_virtual_mac_interface child table entry with attribute access."""
    interface_name: str


class BackupHbdevObject(FortiObject):
    """Typed FortiObject for backup_hbdev child table entry with attribute access."""
    name: str | None


class HaMgmtInterfacesObject(FortiObject):
    """Typed FortiObject for ha_mgmt_interfaces child table entry with attribute access."""
    id: int | None
    interface: str
    dst: str | None
    gateway: str | None
    dst6: str | None
    gateway6: str | None


class UnicastPeersObject(FortiObject):
    """Typed FortiObject for unicast_peers child table entry with attribute access."""
    id: int | None
    peer_ip: str | None


class VclusterObject(FortiObject):
    """Typed FortiObject for vcluster child table entry with attribute access."""
    vcluster_id: int | None
    override: str | None
    priority: int | None
    override_wait_time: int | None
    monitor: str | None
    pingserver_monitor_interface: str | None
    pingserver_failover_threshold: int | None
    pingserver_secondary_force_reset: str | None
    pingserver_flip_timeout: int | None
    vdom: list[Any] | None



class AutoVirtualMacInterfaceHelper:
    """Helper class for managing auto_virtual_mac_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        interface_name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AutoVirtualMacInterfaceObject] | AutoVirtualMacInterfaceObject | None: ...
    
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


class BackupHbdevHelper:
    """Helper class for managing backup_hbdev child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[BackupHbdevObject] | BackupHbdevObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
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
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class HaMgmtInterfacesHelper:
    """Helper class for managing ha_mgmt_interfaces child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[HaMgmtInterfacesObject] | HaMgmtInterfacesObject | None: ...
    
    def set(
        self,
        interface: str,
        id: int | None = ...,
        dst: str | None = ...,
        gateway: str | None = ...,
        dst6: str | None = ...,
        gateway6: str | None = ...,
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


class UnicastPeersHelper:
    """Helper class for managing unicast_peers child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[UnicastPeersObject] | UnicastPeersObject | None: ...
    
    def set(
        self,
        id: int | None = ...,
        peer_ip: str | None = ...,
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


class VclusterHelper:
    """Helper class for managing vcluster child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        vcluster_id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[VclusterObject] | VclusterObject | None: ...
    
    def set(
        self,
        vcluster_id: int | None = ...,
        override: str | None = ...,
        priority: int | None = ...,
        override_wait_time: int | None = ...,
        monitor: str | None = ...,
        pingserver_monitor_interface: str | None = ...,
        pingserver_failover_threshold: int | None = ...,
        pingserver_secondary_force_reset: str | None = ...,
        pingserver_flip_timeout: int | None = ...,
        vdom: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        vcluster_id: str,
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
        vcluster_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

