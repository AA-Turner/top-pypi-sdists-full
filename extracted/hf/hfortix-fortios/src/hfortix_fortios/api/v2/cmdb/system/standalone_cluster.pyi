""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/standalone_cluster
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class StandaloneClusterClusterpeerSyncvdItem(TypedDict, total=False):
    """Nested item for cluster-peer.syncvd field."""
    name: str


class StandaloneClusterClusterpeerDownintfsbeforesesssyncItem(TypedDict, total=False):
    """Nested item for cluster-peer.down-intfs-before-sess-sync field."""
    name: str


class StandaloneClusterClusterpeerSessionsyncfilterDict(TypedDict, total=False):
    """Nested object type for cluster-peer.session-sync-filter field."""
    srcintf: str
    dstintf: str
    srcaddr: str
    dstaddr: str
    srcaddr6: str
    dstaddr6: str
    custom_service: str | list[str]


class StandaloneClusterClusterpeerItem(TypedDict, total=False):
    """Nested item for cluster-peer field."""
    sync_id: int
    peervd: str
    peerip: str
    syncvd: str | list[str] | list[StandaloneClusterClusterpeerSyncvdItem]
    down_intfs_before_sess_sync: str | list[str] | list[StandaloneClusterClusterpeerDownintfsbeforesesssyncItem]
    hb_interval: int
    hb_lost_threshold: int
    ipsec_tunnel_sync: Literal["enable", "disable"]
    secondary_add_ipsec_routes: Literal["enable", "disable"]
    session_sync_filter: StandaloneClusterClusterpeerSessionsyncfilterDict


class StandaloneClusterMonitorinterfaceItem(TypedDict, total=False):
    """Nested item for monitor-interface field."""
    name: str


class StandaloneClusterPingsvrmonitorinterfaceItem(TypedDict, total=False):
    """Nested item for pingsvr-monitor-interface field."""
    name: str


class StandaloneClusterMonitorprefixItem(TypedDict, total=False):
    """Nested item for monitor-prefix field."""
    id: int
    vdom: str
    vrf: int
    prefix: str


class StandaloneClusterPayload(TypedDict, total=False):
    """Payload type for StandaloneCluster operations."""
    standalone_group_id: int
    group_member_id: int
    layer2_connection: Literal["available", "unavailable"]
    session_sync_dev: str | list[str]
    encryption: Literal["enable", "disable"]
    psksecret: str
    asymmetric_traffic_control: Literal["cps-preferred", "strict-anti-replay"]
    cluster_peer: str | list[str] | list[StandaloneClusterClusterpeerItem]
    monitor_interface: str | list[str] | list[StandaloneClusterMonitorinterfaceItem]
    pingsvr_monitor_interface: str | list[str] | list[StandaloneClusterPingsvrmonitorinterfaceItem]
    monitor_prefix: str | list[str] | list[StandaloneClusterMonitorprefixItem]
    helper_traffic_bounce: Literal["enable", "disable"]
    utm_traffic_bounce: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StandaloneClusterResponse(TypedDict, total=False):
    """Response type for StandaloneCluster - use with .dict property for typed dict access."""
    standalone_group_id: int
    group_member_id: int
    layer2_connection: Literal["available", "unavailable"]
    session_sync_dev: str | list[str]
    encryption: Literal["enable", "disable"]
    psksecret: str
    asymmetric_traffic_control: Literal["cps-preferred", "strict-anti-replay"]
    cluster_peer: list[StandaloneClusterClusterpeerItem]
    monitor_interface: list[StandaloneClusterMonitorinterfaceItem]
    pingsvr_monitor_interface: list[StandaloneClusterPingsvrmonitorinterfaceItem]
    monitor_prefix: list[StandaloneClusterMonitorprefixItem]
    helper_traffic_bounce: Literal["enable", "disable"]
    utm_traffic_bounce: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StandaloneClusterClusterpeerSyncvdItemObject(FortiObject[StandaloneClusterClusterpeerSyncvdItem]):
    """Typed object for cluster-peer.syncvd table items with attribute access."""
    name: str


class StandaloneClusterClusterpeerDownintfsbeforesesssyncItemObject(FortiObject[StandaloneClusterClusterpeerDownintfsbeforesesssyncItem]):
    """Typed object for cluster-peer.down-intfs-before-sess-sync table items with attribute access."""
    name: str


class StandaloneClusterClusterpeerItemObject(FortiObject[StandaloneClusterClusterpeerItem]):
    """Typed object for cluster-peer table items with attribute access."""
    sync_id: int
    peervd: str
    peerip: str
    syncvd: FortiObjectList[StandaloneClusterClusterpeerSyncvdItemObject]
    down_intfs_before_sess_sync: FortiObjectList[StandaloneClusterClusterpeerDownintfsbeforesesssyncItemObject]
    hb_interval: int
    hb_lost_threshold: int
    ipsec_tunnel_sync: Literal["enable", "disable"]
    secondary_add_ipsec_routes: Literal["enable", "disable"]
    session_sync_filter: StandaloneClusterClusterpeerSessionsyncfilterObject


class StandaloneClusterMonitorinterfaceItemObject(FortiObject[StandaloneClusterMonitorinterfaceItem]):
    """Typed object for monitor-interface table items with attribute access."""
    name: str


class StandaloneClusterPingsvrmonitorinterfaceItemObject(FortiObject[StandaloneClusterPingsvrmonitorinterfaceItem]):
    """Typed object for pingsvr-monitor-interface table items with attribute access."""
    name: str


class StandaloneClusterMonitorprefixItemObject(FortiObject[StandaloneClusterMonitorprefixItem]):
    """Typed object for monitor-prefix table items with attribute access."""
    id: int
    vdom: str
    vrf: int
    prefix: str


class StandaloneClusterClusterpeerSessionsyncfilterObject(FortiObject):
    """Nested object for cluster-peer.session-sync-filter field with attribute access."""
    srcintf: str
    dstintf: str
    srcaddr: str
    dstaddr: str
    srcaddr6: str
    dstaddr6: str
    custom_service: str | list[str]


class StandaloneClusterObject(FortiObject):
    """Typed FortiObject for StandaloneCluster with field access."""
    standalone_group_id: int
    group_member_id: int
    layer2_connection: Literal["available", "unavailable"]
    session_sync_dev: str | list[str]
    encryption: Literal["enable", "disable"]
    psksecret: str
    asymmetric_traffic_control: Literal["cps-preferred", "strict-anti-replay"]
    cluster_peer: FortiObjectList[StandaloneClusterClusterpeerItemObject]
    monitor_interface: FortiObjectList[StandaloneClusterMonitorinterfaceItemObject]
    pingsvr_monitor_interface: FortiObjectList[StandaloneClusterPingsvrmonitorinterfaceItemObject]
    monitor_prefix: FortiObjectList[StandaloneClusterMonitorprefixItemObject]
    helper_traffic_bounce: Literal["enable", "disable"]
    utm_traffic_bounce: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class StandaloneCluster:
    """
    
    Endpoint: system/standalone_cluster
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StandaloneClusterObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StandaloneClusterPayload | None = ...,
        standalone_group_id: int | None = ...,
        group_member_id: int | None = ...,
        layer2_connection: Literal["available", "unavailable"] | None = ...,
        session_sync_dev: str | list[str] | None = ...,
        encryption: Literal["enable", "disable"] | None = ...,
        psksecret: str | None = ...,
        asymmetric_traffic_control: Literal["cps-preferred", "strict-anti-replay"] | None = ...,
        cluster_peer: str | list[str] | list[StandaloneClusterClusterpeerItem] | None = ...,
        monitor_interface: str | list[str] | list[StandaloneClusterMonitorinterfaceItem] | None = ...,
        pingsvr_monitor_interface: str | list[str] | list[StandaloneClusterPingsvrmonitorinterfaceItem] | None = ...,
        monitor_prefix: str | list[str] | list[StandaloneClusterMonitorprefixItem] | None = ...,
        helper_traffic_bounce: Literal["enable", "disable"] | None = ...,
        utm_traffic_bounce: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StandaloneClusterObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: StandaloneClusterPayload | None = ...,
        standalone_group_id: int | None = ...,
        group_member_id: int | None = ...,
        layer2_connection: Literal["available", "unavailable"] | None = ...,
        session_sync_dev: str | list[str] | None = ...,
        encryption: Literal["enable", "disable"] | None = ...,
        psksecret: str | None = ...,
        asymmetric_traffic_control: Literal["cps-preferred", "strict-anti-replay"] | None = ...,
        cluster_peer: str | list[str] | list[StandaloneClusterClusterpeerItem] | None = ...,
        monitor_interface: str | list[str] | list[StandaloneClusterMonitorinterfaceItem] | None = ...,
        pingsvr_monitor_interface: str | list[str] | list[StandaloneClusterPingsvrmonitorinterfaceItem] | None = ...,
        monitor_prefix: str | list[str] | list[StandaloneClusterMonitorprefixItem] | None = ...,
        helper_traffic_bounce: Literal["enable", "disable"] | None = ...,
        utm_traffic_bounce: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> list[str] | list[dict[str, Any]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> FortiObject[Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> FortiObject[Any]: ...
    
    @staticmethod
    def schema() -> FortiObject[Any]: ...


__all__ = [
    "StandaloneCluster",
    "StandaloneClusterPayload",
    "StandaloneClusterResponse",
    "StandaloneClusterObject",
]