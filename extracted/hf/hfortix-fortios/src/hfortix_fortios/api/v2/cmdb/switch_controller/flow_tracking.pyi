""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/flow_tracking
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

class FlowTrackingCollectorsItem(TypedDict, total=False):
    """Nested item for collectors field."""
    name: str
    ip: str
    port: int
    transport: Literal["udp", "tcp", "sctp"]


class FlowTrackingAggregatesItem(TypedDict, total=False):
    """Nested item for aggregates field."""
    id: int
    ip: str


class FlowTrackingPayload(TypedDict, total=False):
    """Payload type for FlowTracking operations."""
    sample_mode: Literal["local", "perimeter", "device-ingress"]
    sample_rate: int
    format: Literal["netflow1", "netflow5", "netflow9", "ipfix"]
    collectors: str | list[str] | list[FlowTrackingCollectorsItem]
    level: Literal["vlan", "ip", "port", "proto", "mac"]
    max_export_pkt_size: int
    template_export_period: int
    timeout_general: int
    timeout_icmp: int
    timeout_max: int
    timeout_tcp: int
    timeout_tcp_fin: int
    timeout_tcp_rst: int
    timeout_udp: int
    aggregates: str | list[str] | list[FlowTrackingAggregatesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FlowTrackingResponse(TypedDict, total=False):
    """Response type for FlowTracking - use with .dict property for typed dict access."""
    sample_mode: Literal["local", "perimeter", "device-ingress"]
    sample_rate: int
    format: Literal["netflow1", "netflow5", "netflow9", "ipfix"]
    collectors: list[FlowTrackingCollectorsItem]
    level: Literal["vlan", "ip", "port", "proto", "mac"]
    max_export_pkt_size: int
    template_export_period: int
    timeout_general: int
    timeout_icmp: int
    timeout_max: int
    timeout_tcp: int
    timeout_tcp_fin: int
    timeout_tcp_rst: int
    timeout_udp: int
    aggregates: list[FlowTrackingAggregatesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FlowTrackingCollectorsItemObject(FortiObject[FlowTrackingCollectorsItem]):
    """Typed object for collectors table items with attribute access."""
    name: str
    ip: str
    port: int
    transport: Literal["udp", "tcp", "sctp"]


class FlowTrackingAggregatesItemObject(FortiObject[FlowTrackingAggregatesItem]):
    """Typed object for aggregates table items with attribute access."""
    id: int
    ip: str


class FlowTrackingObject(FortiObject):
    """Typed FortiObject for FlowTracking with field access."""
    sample_mode: Literal["local", "perimeter", "device-ingress"]
    sample_rate: int
    format: Literal["netflow1", "netflow5", "netflow9", "ipfix"]
    collectors: FortiObjectList[FlowTrackingCollectorsItemObject]
    level: Literal["vlan", "ip", "port", "proto", "mac"]
    max_export_pkt_size: int
    template_export_period: int
    timeout_general: int
    timeout_icmp: int
    timeout_max: int
    timeout_tcp: int
    timeout_tcp_fin: int
    timeout_tcp_rst: int
    timeout_udp: int
    aggregates: FortiObjectList[FlowTrackingAggregatesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class FlowTracking:
    """
    
    Endpoint: switch_controller/flow_tracking
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FlowTrackingObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[FlowTrackingCollectorsItem] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[FlowTrackingAggregatesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FlowTrackingObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[FlowTrackingCollectorsItem] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[FlowTrackingAggregatesItem] | None = ...,
        vdom: str | bool | None = ...,
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
    "FlowTracking",
    "FlowTrackingPayload",
    "FlowTrackingResponse",
    "FlowTrackingObject",
]