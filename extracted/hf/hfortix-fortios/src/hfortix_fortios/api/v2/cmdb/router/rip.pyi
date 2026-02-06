""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/rip
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

# Import child table helper types
from ._rip_child_tables import (
    DistanceHelper,
    DistributeListHelper,
    NeighborHelper,
    NetworkHelper,
    OffsetListHelper,
    PassiveInterfaceHelper,
    RedistributeHelper,
    InterfaceHelper,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class RipDistanceItem(TypedDict, total=False):
    """Nested item for distance field."""
    id: int
    prefix: str
    distance: int
    access_list: str


class RipDistributelistItem(TypedDict, total=False):
    """Nested item for distribute-list field."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    listname: str
    interface: str


class RipNeighborItem(TypedDict, total=False):
    """Nested item for neighbor field."""
    id: int
    ip: str


class RipNetworkItem(TypedDict, total=False):
    """Nested item for network field."""
    id: int
    prefix: str


class RipOffsetlistItem(TypedDict, total=False):
    """Nested item for offset-list field."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    access_list: str
    offset: int
    interface: str


class RipPassiveinterfaceItem(TypedDict, total=False):
    """Nested item for passive-interface field."""
    name: str


class RipRedistributeItem(TypedDict, total=False):
    """Nested item for redistribute field."""
    name: str
    status: Literal["enable", "disable"]
    metric: int
    routemap: str


class RipInterfaceItem(TypedDict, total=False):
    """Nested item for interface field."""
    name: str
    auth_keychain: str
    auth_mode: Literal["none", "text", "md5"]
    auth_string: str
    receive_version: Literal["1", "2"]
    send_version: Literal["1", "2"]
    send_version2_broadcast: Literal["disable", "enable"]
    split_horizon_status: Literal["enable", "disable"]
    split_horizon: Literal["poisoned", "regular"]
    flags: int


class RipPayload(TypedDict, total=False):
    """Payload type for Rip operations."""
    default_information_originate: Literal["enable", "disable"]
    default_metric: int
    max_out_metric: int
    distance: str | list[str] | list[RipDistanceItem]
    distribute_list: str | list[str] | list[RipDistributelistItem]
    neighbor: str | list[str] | list[RipNeighborItem]
    network: str | list[str] | list[RipNetworkItem]
    offset_list: str | list[str] | list[RipOffsetlistItem]
    passive_interface: str | list[str] | list[RipPassiveinterfaceItem]
    redistribute: str | list[str] | list[RipRedistributeItem]
    update_timer: int
    timeout_timer: int
    garbage_timer: int
    version: Literal["1", "2"]
    interface: str | list[str] | list[RipInterfaceItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RipResponse(TypedDict, total=False):
    """Response type for Rip - use with .dict property for typed dict access."""
    default_information_originate: Literal["enable", "disable"]
    default_metric: int
    max_out_metric: int
    distance: list[RipDistanceItem]
    distribute_list: list[RipDistributelistItem]
    neighbor: list[RipNeighborItem]
    network: list[RipNetworkItem]
    offset_list: list[RipOffsetlistItem]
    passive_interface: list[RipPassiveinterfaceItem]
    redistribute: list[RipRedistributeItem]
    update_timer: int
    timeout_timer: int
    garbage_timer: int
    version: Literal["1", "2"]
    interface: list[RipInterfaceItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RipDistanceItemObject(FortiObject[RipDistanceItem]):
    """Typed object for distance table items with attribute access."""
    id: int
    prefix: str
    distance: int
    access_list: str


class RipDistributelistItemObject(FortiObject[RipDistributelistItem]):
    """Typed object for distribute-list table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    listname: str
    interface: str


class RipNeighborItemObject(FortiObject[RipNeighborItem]):
    """Typed object for neighbor table items with attribute access."""
    id: int
    ip: str


class RipNetworkItemObject(FortiObject[RipNetworkItem]):
    """Typed object for network table items with attribute access."""
    id: int
    prefix: str


class RipOffsetlistItemObject(FortiObject[RipOffsetlistItem]):
    """Typed object for offset-list table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    direction: Literal["in", "out"]
    access_list: str
    offset: int
    interface: str


class RipPassiveinterfaceItemObject(FortiObject[RipPassiveinterfaceItem]):
    """Typed object for passive-interface table items with attribute access."""
    name: str


class RipRedistributeItemObject(FortiObject[RipRedistributeItem]):
    """Typed object for redistribute table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    metric: int
    routemap: str


class RipInterfaceItemObject(FortiObject[RipInterfaceItem]):
    """Typed object for interface table items with attribute access."""
    name: str
    auth_keychain: str
    auth_mode: Literal["none", "text", "md5"]
    auth_string: str
    receive_version: Literal["1", "2"]
    send_version: Literal["1", "2"]
    send_version2_broadcast: Literal["disable", "enable"]
    split_horizon_status: Literal["enable", "disable"]
    split_horizon: Literal["poisoned", "regular"]
    flags: int


class RipObject(FortiObject):
    """Typed FortiObject for Rip with field access."""
    default_information_originate: Literal["enable", "disable"]
    default_metric: int
    max_out_metric: int
    distance: FortiObjectList[RipDistanceItemObject]
    distribute_list: FortiObjectList[RipDistributelistItemObject]
    neighbor: FortiObjectList[RipNeighborItemObject]
    network: FortiObjectList[RipNetworkItemObject]
    offset_list: FortiObjectList[RipOffsetlistItemObject]
    passive_interface: FortiObjectList[RipPassiveinterfaceItemObject]
    redistribute: FortiObjectList[RipRedistributeItemObject]
    update_timer: int
    timeout_timer: int
    garbage_timer: int
    interface: FortiObjectList[RipInterfaceItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Rip:
    """
    
    Endpoint: router/rip
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    # Child table helpers
    distance: DistanceHelper
    distribute_list: DistributeListHelper
    neighbor: NeighborHelper
    network: NetworkHelper
    offset_list: OffsetListHelper
    passive_interface: PassiveInterfaceHelper
    redistribute: RedistributeHelper
    interface: InterfaceHelper
    
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
    ) -> RipObject: ...
    
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
        payload_dict: RipPayload | None = ...,
        default_information_originate: Literal["enable", "disable"] | None = ...,
        default_metric: int | None = ...,
        max_out_metric: int | None = ...,
        distance: str | list[str] | list[RipDistanceItem] | None = ...,
        distribute_list: str | list[str] | list[RipDistributelistItem] | None = ...,
        neighbor: str | list[str] | list[RipNeighborItem] | None = ...,
        network: str | list[str] | list[RipNetworkItem] | None = ...,
        offset_list: str | list[str] | list[RipOffsetlistItem] | None = ...,
        passive_interface: str | list[str] | list[RipPassiveinterfaceItem] | None = ...,
        redistribute: str | list[str] | list[RipRedistributeItem] | None = ...,
        update_timer: int | None = ...,
        timeout_timer: int | None = ...,
        garbage_timer: int | None = ...,
        version: Literal["1", "2"] | None = ...,
        interface: str | list[str] | list[RipInterfaceItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RipObject: ...


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
        payload_dict: RipPayload | None = ...,
        default_information_originate: Literal["enable", "disable"] | None = ...,
        default_metric: int | None = ...,
        max_out_metric: int | None = ...,
        distance: str | list[str] | list[RipDistanceItem] | None = ...,
        distribute_list: str | list[str] | list[RipDistributelistItem] | None = ...,
        neighbor: str | list[str] | list[RipNeighborItem] | None = ...,
        network: str | list[str] | list[RipNetworkItem] | None = ...,
        offset_list: str | list[str] | list[RipOffsetlistItem] | None = ...,
        passive_interface: str | list[str] | list[RipPassiveinterfaceItem] | None = ...,
        redistribute: str | list[str] | list[RipRedistributeItem] | None = ...,
        update_timer: int | None = ...,
        timeout_timer: int | None = ...,
        garbage_timer: int | None = ...,
        version: Literal["1", "2"] | None = ...,
        interface: str | list[str] | list[RipInterfaceItem] | None = ...,
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
    "Rip",
    "RipPayload",
    "RipResponse",
    "RipObject",
]