"""
Child Table Helper Type Stubs for system/standalone-cluster

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class ClusterPeerDict(TypedDict, total=False):
    """Type definition for cluster_peer child table entry."""
    sync_id: int | None
    peervd: str | None
    peerip: str | None
    syncvd: list[Any] | None
    down_intfs_before_sess_sync: list[Any] | None
    hb_interval: int | None
    hb_lost_threshold: int | None
    ipsec_tunnel_sync: str | None
    secondary_add_ipsec_routes: str | None
    session_sync_filter: dict[str, Any] | None

class MonitorInterfaceDict(TypedDict, total=False):
    """Type definition for monitor_interface child table entry."""
    name: str

class PingsvrMonitorInterfaceDict(TypedDict, total=False):
    """Type definition for pingsvr_monitor_interface child table entry."""
    name: str

class MonitorPrefixDict(TypedDict, total=False):
    """Type definition for monitor_prefix child table entry."""
    id: int
    vdom: str
    vrf: int | None
    prefix: str | None


class ClusterPeerObject(FortiObject):
    """Typed FortiObject for cluster_peer child table entry with attribute access."""
    sync_id: int | None
    peervd: str | None
    peerip: str | None
    syncvd: list[Any] | None
    down_intfs_before_sess_sync: list[Any] | None
    hb_interval: int | None
    hb_lost_threshold: int | None
    ipsec_tunnel_sync: str | None
    secondary_add_ipsec_routes: str | None
    session_sync_filter: dict[str, Any] | None


class MonitorInterfaceObject(FortiObject):
    """Typed FortiObject for monitor_interface child table entry with attribute access."""
    name: str


class PingsvrMonitorInterfaceObject(FortiObject):
    """Typed FortiObject for pingsvr_monitor_interface child table entry with attribute access."""
    name: str


class MonitorPrefixObject(FortiObject):
    """Typed FortiObject for monitor_prefix child table entry with attribute access."""
    id: int
    vdom: str
    vrf: int | None
    prefix: str | None



class ClusterPeerHelper:
    """Helper class for managing cluster_peer child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        sync_id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ClusterPeerObject] | ClusterPeerObject | None: ...
    
    def set(
        self,
        sync_id: int | None = ...,
        peervd: str | None = ...,
        peerip: str | None = ...,
        syncvd: list[Any] | None = ...,
        down_intfs_before_sess_sync: list[Any] | None = ...,
        hb_interval: int | None = ...,
        hb_lost_threshold: int | None = ...,
        ipsec_tunnel_sync: str | None = ...,
        secondary_add_ipsec_routes: str | None = ...,
        session_sync_filter: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        sync_id: str,
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
        sync_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class MonitorInterfaceHelper:
    """Helper class for managing monitor_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[MonitorInterfaceObject] | MonitorInterfaceObject | None: ...
    
    def set(
        self,
        name: str,
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


class PingsvrMonitorInterfaceHelper:
    """Helper class for managing pingsvr_monitor_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[PingsvrMonitorInterfaceObject] | PingsvrMonitorInterfaceObject | None: ...
    
    def set(
        self,
        name: str,
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


class MonitorPrefixHelper:
    """Helper class for managing monitor_prefix child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[MonitorPrefixObject] | MonitorPrefixObject | None: ...
    
    def set(
        self,
        id: int,
        vdom: str,
        vrf: int | None = ...,
        prefix: str | None = ...,
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

