"""
Child Table Helper Type Stubs for router/ripng

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class DistanceDict(TypedDict, total=False):
    """Type definition for distance child table entry."""
    id: int
    distance: int
    prefix6: str | None
    access_list6: str | None

class DistributeListDict(TypedDict, total=False):
    """Type definition for distribute_list child table entry."""
    id: int
    status: str | None
    direction: str
    listname: str
    interface: str | None

class NeighborDict(TypedDict, total=False):
    """Type definition for neighbor child table entry."""
    id: int | None
    ip6: str
    interface: str

class NetworkDict(TypedDict, total=False):
    """Type definition for network child table entry."""
    id: int | None
    prefix: str | None

class AggregateAddressDict(TypedDict, total=False):
    """Type definition for aggregate_address child table entry."""
    id: int | None
    prefix6: str | None

class OffsetListDict(TypedDict, total=False):
    """Type definition for offset_list child table entry."""
    id: int
    status: str | None
    direction: str
    access_list6: str
    offset: int
    interface: str | None

class PassiveInterfaceDict(TypedDict, total=False):
    """Type definition for passive_interface child table entry."""
    name: str

class RedistributeDict(TypedDict, total=False):
    """Type definition for redistribute child table entry."""
    name: str
    status: str | None
    metric: int | None
    routemap: str | None

class InterfaceDict(TypedDict, total=False):
    """Type definition for interface child table entry."""
    name: str | None
    split_horizon_status: str | None
    split_horizon: str | None
    flags: int | None


class DistanceObject(FortiObject):
    """Typed FortiObject for distance child table entry with attribute access."""
    id: int
    distance: int
    prefix6: str | None
    access_list6: str | None


class DistributeListObject(FortiObject):
    """Typed FortiObject for distribute_list child table entry with attribute access."""
    id: int
    status: str | None
    direction: str
    listname: str
    interface: str | None


class NeighborObject(FortiObject):
    """Typed FortiObject for neighbor child table entry with attribute access."""
    id: int | None
    ip6: str
    interface: str


class NetworkObject(FortiObject):
    """Typed FortiObject for network child table entry with attribute access."""
    id: int | None
    prefix: str | None


class AggregateAddressObject(FortiObject):
    """Typed FortiObject for aggregate_address child table entry with attribute access."""
    id: int | None
    prefix6: str | None


class OffsetListObject(FortiObject):
    """Typed FortiObject for offset_list child table entry with attribute access."""
    id: int
    status: str | None
    direction: str
    access_list6: str
    offset: int
    interface: str | None


class PassiveInterfaceObject(FortiObject):
    """Typed FortiObject for passive_interface child table entry with attribute access."""
    name: str


class RedistributeObject(FortiObject):
    """Typed FortiObject for redistribute child table entry with attribute access."""
    name: str
    status: str | None
    metric: int | None
    routemap: str | None


class InterfaceObject(FortiObject):
    """Typed FortiObject for interface child table entry with attribute access."""
    name: str | None
    split_horizon_status: str | None
    split_horizon: str | None
    flags: int | None



class DistanceHelper:
    """Helper class for managing distance child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[DistanceObject] | DistanceObject | None: ...
    
    def set(
        self,
        id: int,
        distance: int,
        prefix6: str | None = ...,
        access_list6: str | None = ...,
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


class DistributeListHelper:
    """Helper class for managing distribute_list child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[DistributeListObject] | DistributeListObject | None: ...
    
    def set(
        self,
        id: int,
        direction: str,
        listname: str,
        status: str | None = ...,
        interface: str | None = ...,
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


class NeighborHelper:
    """Helper class for managing neighbor child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NeighborObject] | NeighborObject | None: ...
    
    def set(
        self,
        ip6: str,
        interface: str,
        id: int | None = ...,
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


class NetworkHelper:
    """Helper class for managing network child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[NetworkObject] | NetworkObject | None: ...
    
    def set(
        self,
        id: int | None = ...,
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


class AggregateAddressHelper:
    """Helper class for managing aggregate_address child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AggregateAddressObject] | AggregateAddressObject | None: ...
    
    def set(
        self,
        id: int | None = ...,
        prefix6: str | None = ...,
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


class OffsetListHelper:
    """Helper class for managing offset_list child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[OffsetListObject] | OffsetListObject | None: ...
    
    def set(
        self,
        id: int,
        direction: str,
        access_list6: str,
        offset: int,
        status: str | None = ...,
        interface: str | None = ...,
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


class PassiveInterfaceHelper:
    """Helper class for managing passive_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[PassiveInterfaceObject] | PassiveInterfaceObject | None: ...
    
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


class RedistributeHelper:
    """Helper class for managing redistribute child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[RedistributeObject] | RedistributeObject | None: ...
    
    def set(
        self,
        name: str,
        status: str | None = ...,
        metric: int | None = ...,
        routemap: str | None = ...,
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


class InterfaceHelper:
    """Helper class for managing interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[InterfaceObject] | InterfaceObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        split_horizon_status: str | None = ...,
        split_horizon: str | None = ...,
        flags: int | None = ...,
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

