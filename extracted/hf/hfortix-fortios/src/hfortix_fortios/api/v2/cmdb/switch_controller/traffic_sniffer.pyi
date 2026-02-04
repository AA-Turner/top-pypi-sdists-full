""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/traffic_sniffer
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

class TrafficSnifferTargetportInportsItem(TypedDict, total=False):
    """Nested item for target-port.in-ports field."""
    name: str


class TrafficSnifferTargetportOutportsItem(TypedDict, total=False):
    """Nested item for target-port.out-ports field."""
    name: str


class TrafficSnifferTargetmacItem(TypedDict, total=False):
    """Nested item for target-mac field."""
    mac: str
    description: str


class TrafficSnifferTargetipItem(TypedDict, total=False):
    """Nested item for target-ip field."""
    ip: str
    description: str


class TrafficSnifferTargetportItem(TypedDict, total=False):
    """Nested item for target-port field."""
    switch_id: str
    description: str
    in_ports: str | list[str] | list[TrafficSnifferTargetportInportsItem]
    out_ports: str | list[str] | list[TrafficSnifferTargetportOutportsItem]


class TrafficSnifferPayload(TypedDict, total=False):
    """Payload type for TrafficSniffer operations."""
    mode: Literal["erspan-auto", "rspan", "none"]
    erspan_ip: str
    target_mac: str | list[str] | list[TrafficSnifferTargetmacItem]
    target_ip: str | list[str] | list[TrafficSnifferTargetipItem]
    target_port: str | list[str] | list[TrafficSnifferTargetportItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class TrafficSnifferResponse(TypedDict, total=False):
    """Response type for TrafficSniffer - use with .dict property for typed dict access."""
    mode: Literal["erspan-auto", "rspan", "none"]
    erspan_ip: str
    target_mac: list[TrafficSnifferTargetmacItem]
    target_ip: list[TrafficSnifferTargetipItem]
    target_port: list[TrafficSnifferTargetportItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class TrafficSnifferTargetportInportsItemObject(FortiObject[TrafficSnifferTargetportInportsItem]):
    """Typed object for target-port.in-ports table items with attribute access."""
    name: str


class TrafficSnifferTargetportOutportsItemObject(FortiObject[TrafficSnifferTargetportOutportsItem]):
    """Typed object for target-port.out-ports table items with attribute access."""
    name: str


class TrafficSnifferTargetmacItemObject(FortiObject[TrafficSnifferTargetmacItem]):
    """Typed object for target-mac table items with attribute access."""
    mac: str
    description: str


class TrafficSnifferTargetipItemObject(FortiObject[TrafficSnifferTargetipItem]):
    """Typed object for target-ip table items with attribute access."""
    ip: str
    description: str


class TrafficSnifferTargetportItemObject(FortiObject[TrafficSnifferTargetportItem]):
    """Typed object for target-port table items with attribute access."""
    switch_id: str
    description: str
    in_ports: FortiObjectList[TrafficSnifferTargetportInportsItemObject]
    out_ports: FortiObjectList[TrafficSnifferTargetportOutportsItemObject]


class TrafficSnifferObject(FortiObject):
    """Typed FortiObject for TrafficSniffer with field access."""
    mode: Literal["erspan-auto", "rspan", "none"]
    erspan_ip: str
    target_mac: FortiObjectList[TrafficSnifferTargetmacItemObject]
    target_ip: FortiObjectList[TrafficSnifferTargetipItemObject]
    target_port: FortiObjectList[TrafficSnifferTargetportItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class TrafficSniffer:
    """
    
    Endpoint: switch_controller/traffic_sniffer
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
    ) -> TrafficSnifferObject: ...
    
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
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[TrafficSnifferTargetmacItem] | None = ...,
        target_ip: str | list[str] | list[TrafficSnifferTargetipItem] | None = ...,
        target_port: str | list[str] | list[TrafficSnifferTargetportItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TrafficSnifferObject: ...


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
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[TrafficSnifferTargetmacItem] | None = ...,
        target_ip: str | list[str] | list[TrafficSnifferTargetipItem] | None = ...,
        target_port: str | list[str] | list[TrafficSnifferTargetportItem] | None = ...,
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
    "TrafficSniffer",
    "TrafficSnifferPayload",
    "TrafficSnifferResponse",
    "TrafficSnifferObject",
]