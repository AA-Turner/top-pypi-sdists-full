""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/netflow
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

class NetflowExclusionfiltersItem(TypedDict, total=False):
    """Nested item for exclusion-filters field."""
    id: int
    source_ip: str
    destination_ip: str
    source_port: str
    destination_port: str
    protocol: int


class NetflowCollectorsItem(TypedDict, total=False):
    """Nested item for collectors field."""
    id: int
    collector_ip: str
    collector_port: int
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class NetflowPayload(TypedDict, total=False):
    """Payload type for Netflow operations."""
    active_flow_timeout: int
    inactive_flow_timeout: int
    template_tx_timeout: int
    template_tx_counter: int
    session_cache_size: Literal["min", "default", "max"]
    exclusion_filters: str | list[str] | list[NetflowExclusionfiltersItem]
    collectors: str | list[str] | list[NetflowCollectorsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class NetflowResponse(TypedDict, total=False):
    """Response type for Netflow - use with .dict property for typed dict access."""
    active_flow_timeout: int
    inactive_flow_timeout: int
    template_tx_timeout: int
    template_tx_counter: int
    session_cache_size: Literal["min", "default", "max"]
    exclusion_filters: list[NetflowExclusionfiltersItem]
    collectors: list[NetflowCollectorsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class NetflowExclusionfiltersItemObject(FortiObject[NetflowExclusionfiltersItem]):
    """Typed object for exclusion-filters table items with attribute access."""
    id: int
    source_ip: str
    destination_ip: str
    source_port: str
    destination_port: str
    protocol: int


class NetflowCollectorsItemObject(FortiObject[NetflowCollectorsItem]):
    """Typed object for collectors table items with attribute access."""
    id: int
    collector_ip: str
    collector_port: int
    source_ip: str
    source_ip_interface: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


class NetflowObject(FortiObject):
    """Typed FortiObject for Netflow with field access."""
    active_flow_timeout: int
    inactive_flow_timeout: int
    template_tx_timeout: int
    template_tx_counter: int
    session_cache_size: Literal["min", "default", "max"]
    exclusion_filters: FortiObjectList[NetflowExclusionfiltersItemObject]
    collectors: FortiObjectList[NetflowCollectorsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Netflow:
    """
    
    Endpoint: system/netflow
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
    ) -> NetflowObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: NetflowPayload | None = ...,
        active_flow_timeout: int | None = ...,
        inactive_flow_timeout: int | None = ...,
        template_tx_timeout: int | None = ...,
        template_tx_counter: int | None = ...,
        session_cache_size: Literal["min", "default", "max"] | None = ...,
        exclusion_filters: str | list[str] | list[NetflowExclusionfiltersItem] | None = ...,
        collectors: str | list[str] | list[NetflowCollectorsItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NetflowObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: NetflowPayload | None = ...,
        active_flow_timeout: int | None = ...,
        inactive_flow_timeout: int | None = ...,
        template_tx_timeout: int | None = ...,
        template_tx_counter: int | None = ...,
        session_cache_size: Literal["min", "default", "max"] | None = ...,
        exclusion_filters: str | list[str] | list[NetflowExclusionfiltersItem] | None = ...,
        collectors: str | list[str] | list[NetflowCollectorsItem] | None = ...,
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
    "Netflow",
    "NetflowPayload",
    "NetflowResponse",
    "NetflowObject",
]