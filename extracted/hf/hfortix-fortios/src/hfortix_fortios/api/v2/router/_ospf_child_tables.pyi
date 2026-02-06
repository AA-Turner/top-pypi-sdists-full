"""
Child Table Helper Type Stubs for router/ospf

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class AreaDict(TypedDict, total=False):
    """Type definition for area child table entry."""
    id: str | None
    shortcut: str | None
    authentication: str | None
    default_cost: int | None
    nssa_translator_role: str | None
    stub_type: str | None
    type: str | None
    nssa_default_information_originate: str | None
    nssa_default_information_originate_metric: int | None
    nssa_default_information_originate_metric_type: str | None
    nssa_redistribution: str | None
    comments: str | None
    range: list[Any] | None
    virtual_link: list[Any] | None
    filter_list: list[Any] | None

class OspfInterfaceDict(TypedDict, total=False):
    """Type definition for ospf_interface child table entry."""
    name: str | None
    comments: str | None
    interface: str
    ip: str | None
    linkdown_fast_failover: str | None
    authentication: str | None
    authentication_key: str | None
    keychain: str | None
    prefix_length: int | None
    retransmit_interval: int | None
    transmit_delay: int | None
    cost: int | None
    priority: int | None
    dead_interval: int | None
    hello_interval: int | None
    hello_multiplier: int | None
    database_filter_out: str | None
    mtu: int | None
    mtu_ignore: str | None
    network_type: str | None
    bfd: str | None
    status: str | None
    resync_timeout: int | None
    md5_keys: list[Any] | None

class NetworkDict(TypedDict, total=False):
    """Type definition for network child table entry."""
    id: int | None
    prefix: str
    area: str
    comments: str | None

class NeighborDict(TypedDict, total=False):
    """Type definition for neighbor child table entry."""
    id: int | None
    ip: str
    poll_interval: int | None
    cost: int | None
    priority: int | None

class PassiveInterfaceDict(TypedDict, total=False):
    """Type definition for passive_interface child table entry."""
    name: str

class SummaryAddressDict(TypedDict, total=False):
    """Type definition for summary_address child table entry."""
    id: int | None
    prefix: str
    tag: int | None
    advertise: str | None

class DistributeListDict(TypedDict, total=False):
    """Type definition for distribute_list child table entry."""
    id: int | None
    access_list: str
    protocol: str

class RedistributeDict(TypedDict, total=False):
    """Type definition for redistribute child table entry."""
    name: str
    status: str | None
    metric: int | None
    routemap: str | None
    metric_type: str | None
    tag: int | None


class AreaObject(FortiObject):
    """Typed FortiObject for area child table entry with attribute access."""
    id: str | None
    shortcut: str | None
    authentication: str | None
    default_cost: int | None
    nssa_translator_role: str | None
    stub_type: str | None
    type: str | None
    nssa_default_information_originate: str | None
    nssa_default_information_originate_metric: int | None
    nssa_default_information_originate_metric_type: str | None
    nssa_redistribution: str | None
    comments: str | None
    range: list[Any] | None
    virtual_link: list[Any] | None
    filter_list: list[Any] | None


class OspfInterfaceObject(FortiObject):
    """Typed FortiObject for ospf_interface child table entry with attribute access."""
    name: str | None
    comments: str | None
    interface: str
    ip: str | None
    linkdown_fast_failover: str | None
    authentication: str | None
    authentication_key: str | None
    keychain: str | None
    prefix_length: int | None
    retransmit_interval: int | None
    transmit_delay: int | None
    cost: int | None
    priority: int | None
    dead_interval: int | None
    hello_interval: int | None
    hello_multiplier: int | None
    database_filter_out: str | None
    mtu: int | None
    mtu_ignore: str | None
    network_type: str | None
    bfd: str | None
    status: str | None
    resync_timeout: int | None
    md5_keys: list[Any] | None


class NetworkObject(FortiObject):
    """Typed FortiObject for network child table entry with attribute access."""
    id: int | None
    prefix: str
    area: str
    comments: str | None


class NeighborObject(FortiObject):
    """Typed FortiObject for neighbor child table entry with attribute access."""
    id: int | None
    ip: str
    poll_interval: int | None
    cost: int | None
    priority: int | None


class PassiveInterfaceObject(FortiObject):
    """Typed FortiObject for passive_interface child table entry with attribute access."""
    name: str


class SummaryAddressObject(FortiObject):
    """Typed FortiObject for summary_address child table entry with attribute access."""
    id: int | None
    prefix: str
    tag: int | None
    advertise: str | None


class DistributeListObject(FortiObject):
    """Typed FortiObject for distribute_list child table entry with attribute access."""
    id: int | None
    access_list: str
    protocol: str


class RedistributeObject(FortiObject):
    """Typed FortiObject for redistribute child table entry with attribute access."""
    name: str
    status: str | None
    metric: int | None
    routemap: str | None
    metric_type: str | None
    tag: int | None



class AreaHelper:
    """Helper class for managing area child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[AreaObject] | AreaObject | None: ...
    
    def set(
        self,
        id: str | None = ...,
        shortcut: str | None = ...,
        authentication: str | None = ...,
        default_cost: int | None = ...,
        nssa_translator_role: str | None = ...,
        stub_type: str | None = ...,
        type: str | None = ...,
        nssa_default_information_originate: str | None = ...,
        nssa_default_information_originate_metric: int | None = ...,
        nssa_default_information_originate_metric_type: str | None = ...,
        nssa_redistribution: str | None = ...,
        comments: str | None = ...,
        range: list[Any] | None = ...,
        virtual_link: list[Any] | None = ...,
        filter_list: list[Any] | None = ...,
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


class OspfInterfaceHelper:
    """Helper class for managing ospf_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[OspfInterfaceObject] | OspfInterfaceObject | None: ...
    
    def set(
        self,
        interface: str,
        name: str | None = ...,
        comments: str | None = ...,
        ip: str | None = ...,
        linkdown_fast_failover: str | None = ...,
        authentication: str | None = ...,
        authentication_key: str | None = ...,
        keychain: str | None = ...,
        prefix_length: int | None = ...,
        retransmit_interval: int | None = ...,
        transmit_delay: int | None = ...,
        cost: int | None = ...,
        priority: int | None = ...,
        dead_interval: int | None = ...,
        hello_interval: int | None = ...,
        hello_multiplier: int | None = ...,
        database_filter_out: str | None = ...,
        mtu: int | None = ...,
        mtu_ignore: str | None = ...,
        network_type: str | None = ...,
        bfd: str | None = ...,
        status: str | None = ...,
        resync_timeout: int | None = ...,
        md5_keys: list[Any] | None = ...,
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
        prefix: str,
        area: str,
        id: int | None = ...,
        comments: str | None = ...,
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
        ip: str,
        id: int | None = ...,
        poll_interval: int | None = ...,
        cost: int | None = ...,
        priority: int | None = ...,
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


class SummaryAddressHelper:
    """Helper class for managing summary_address child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[SummaryAddressObject] | SummaryAddressObject | None: ...
    
    def set(
        self,
        prefix: str,
        id: int | None = ...,
        tag: int | None = ...,
        advertise: str | None = ...,
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
        access_list: str,
        protocol: str,
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
        metric_type: str | None = ...,
        tag: int | None = ...,
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

