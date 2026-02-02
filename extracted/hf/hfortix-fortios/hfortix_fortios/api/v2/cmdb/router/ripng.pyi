""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/ripng
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

class RipngDistanceItem(TypedDict, total=False):
    """Nested item for distance field."""
    id: int
    distance: int
    prefix6: str
    access_list6: str


class RipngDistributelistItem(TypedDict, total=False):
    """Nested item for distribute-list field."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    listname: str
    interface: str


class RipngNeighborItem(TypedDict, total=False):
    """Nested item for neighbor field."""
    id: int
    ip6: str
    interface: str


class RipngNetworkItem(TypedDict, total=False):
    """Nested item for network field."""
    id: int
    prefix: str


class RipngAggregateaddressItem(TypedDict, total=False):
    """Nested item for aggregate-address field."""
    id: int
    prefix6: str


class RipngOffsetlistItem(TypedDict, total=False):
    """Nested item for offset-list field."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    access_list6: str
    offset: int
    interface: str


class RipngPassiveinterfaceItem(TypedDict, total=False):
    """Nested item for passive-interface field."""
    name: str


class RipngRedistributeItem(TypedDict, total=False):
    """Nested item for redistribute field."""
    name: str
    status: Literal["enable", "disable"]
    metric: int
    routemap: str


class RipngInterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    name: str
    split_horizon_status: Literal["enable", "disable"]
    split_horizon: Literal["poisoned", "regular"]
    flags: int


class RipngPayload(TypedDict, total=False):
    """Payload type for Ripng operations."""
    default_information_originate: Literal["enable", "disable"]
    default_metric: int
    max_out_metric: int
    distance: str | list[str] | list[RipngDistanceItem]
    distribute_list: str | list[str] | list[RipngDistributelistItem]
    neighbor: str | list[str] | list[RipngNeighborItem]
    network: str | list[str] | list[RipngNetworkItem]
    aggregate_address: str | list[str] | list[RipngAggregateaddressItem]
    offset_list: str | list[str] | list[RipngOffsetlistItem]
    passive_interface: str | list[str] | list[RipngPassiveinterfaceItem]
    redistribute: str | list[str] | list[RipngRedistributeItem]
    update_timer: int
    timeout_timer: int
    garbage_timer: int
    interface: str | list[str] | list[RipngInterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RipngResponse(TypedDict, total=False):
    """Response type for Ripng - use with .dict property for typed dict access."""
    default_information_originate: Literal["enable", "disable"]
    default_metric: int
    max_out_metric: int
    distance: list[RipngDistanceItem]
    distribute_list: list[RipngDistributelistItem]
    neighbor: list[RipngNeighborItem]
    network: list[RipngNetworkItem]
    aggregate_address: list[RipngAggregateaddressItem]
    offset_list: list[RipngOffsetlistItem]
    passive_interface: list[RipngPassiveinterfaceItem]
    redistribute: list[RipngRedistributeItem]
    update_timer: int
    timeout_timer: int
    garbage_timer: int
    interface: list[RipngInterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RipngDistanceItemObject(FortiObject[RipngDistanceItem]):
    """Typed object for distance table items with attribute access."""
    id: int
    distance: int
    prefix6: str
    access_list6: str


class RipngDistributelistItemObject(FortiObject[RipngDistributelistItem]):
    """Typed object for distribute-list table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    listname: str
    interface: str


class RipngNeighborItemObject(FortiObject[RipngNeighborItem]):
    """Typed object for neighbor table items with attribute access."""
    id: int
    ip6: str
    interface: str


class RipngNetworkItemObject(FortiObject[RipngNetworkItem]):
    """Typed object for network table items with attribute access."""
    id: int
    prefix: str


class RipngAggregateaddressItemObject(FortiObject[RipngAggregateaddressItem]):
    """Typed object for aggregate-address table items with attribute access."""
    id: int
    prefix6: str


class RipngOffsetlistItemObject(FortiObject[RipngOffsetlistItem]):
    """Typed object for offset-list table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    access_list6: str
    offset: int
    interface: str


class RipngPassiveinterfaceItemObject(FortiObject[RipngPassiveinterfaceItem]):
    """Typed object for passive-interface table items with attribute access."""
    name: str


class RipngRedistributeItemObject(FortiObject[RipngRedistributeItem]):
    """Typed object for redistribute table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    metric: int
    routemap: str


class RipngInterfaceItemObject(FortiObject[RipngInterfaceItem]):
    """Typed object for interface table items with attribute access."""
    name: str
    split_horizon_status: Literal["enable", "disable"]
    split_horizon: Literal["poisoned", "regular"]
    flags: int


class RipngObject(FortiObject):
    """Typed FortiObject for Ripng with field access."""
    default_information_originate: Literal["enable", "disable"]
    default_metric: int
    max_out_metric: int
    distance: FortiObjectList[RipngDistanceItemObject]
    distribute_list: FortiObjectList[RipngDistributelistItemObject]
    neighbor: FortiObjectList[RipngNeighborItemObject]
    network: FortiObjectList[RipngNetworkItemObject]
    aggregate_address: FortiObjectList[RipngAggregateaddressItemObject]
    offset_list: FortiObjectList[RipngOffsetlistItemObject]
    passive_interface: FortiObjectList[RipngPassiveinterfaceItemObject]
    redistribute: FortiObjectList[RipngRedistributeItemObject]
    update_timer: int
    timeout_timer: int
    garbage_timer: int
    interface: FortiObjectList[RipngInterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Ripng:
    """
    
    Endpoint: router/ripng
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
    ) -> RipngObject: ...
    
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
        payload_dict: RipngPayload | None = ...,
        default_information_originate: Literal["enable", "disable"] | None = ...,
        default_metric: int | None = ...,
        max_out_metric: int | None = ...,
        distance: str | list[str] | list[RipngDistanceItem] | None = ...,
        distribute_list: str | list[str] | list[RipngDistributelistItem] | None = ...,
        neighbor: str | list[str] | list[RipngNeighborItem] | None = ...,
        network: str | list[str] | list[RipngNetworkItem] | None = ...,
        aggregate_address: str | list[str] | list[RipngAggregateaddressItem] | None = ...,
        offset_list: str | list[str] | list[RipngOffsetlistItem] | None = ...,
        passive_interface: str | list[str] | list[RipngPassiveinterfaceItem] | None = ...,
        redistribute: str | list[str] | list[RipngRedistributeItem] | None = ...,
        update_timer: int | None = ...,
        timeout_timer: int | None = ...,
        garbage_timer: int | None = ...,
        interface: str | list[str] | list[RipngInterfaceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RipngObject: ...


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
        payload_dict: RipngPayload | None = ...,
        default_information_originate: Literal["enable", "disable"] | None = ...,
        default_metric: int | None = ...,
        max_out_metric: int | None = ...,
        distance: str | list[str] | list[RipngDistanceItem] | None = ...,
        distribute_list: str | list[str] | list[RipngDistributelistItem] | None = ...,
        neighbor: str | list[str] | list[RipngNeighborItem] | None = ...,
        network: str | list[str] | list[RipngNetworkItem] | None = ...,
        aggregate_address: str | list[str] | list[RipngAggregateaddressItem] | None = ...,
        offset_list: str | list[str] | list[RipngOffsetlistItem] | None = ...,
        passive_interface: str | list[str] | list[RipngPassiveinterfaceItem] | None = ...,
        redistribute: str | list[str] | list[RipngRedistributeItem] | None = ...,
        update_timer: int | None = ...,
        timeout_timer: int | None = ...,
        garbage_timer: int | None = ...,
        interface: str | list[str] | list[RipngInterfaceItem] | None = ...,
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
    "Ripng",
    "RipngPayload",
    "RipngResponse",
    "RipngObject",
]