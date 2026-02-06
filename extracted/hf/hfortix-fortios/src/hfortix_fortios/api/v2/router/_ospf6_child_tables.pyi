"""
Child Table Helper Type Stubs for router/ospf6

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class AreaDict(TypedDict, total=False):
    """Type definition for area child table entry."""
    id: str | None
    default_cost: int | None
    nssa_translator_role: str | None
    stub_type: str | None
    type: str | None
    nssa_default_information_originate: str | None
    nssa_default_information_originate_metric: int | None
    nssa_default_information_originate_metric_type: str | None
    nssa_redistribution: str | None
    authentication: str | None
    key_rollover_interval: int | None
    ipsec_auth_alg: str | None
    ipsec_enc_alg: str | None
    ipsec_keys: list[Any] | None
    range: list[Any] | None
    virtual_link: list[Any] | None

class Ospf6InterfaceDict(TypedDict, total=False):
    """Type definition for ospf6_interface child table entry."""
    name: str | None
    area_id: str
    interface: str
    retransmit_interval: int | None
    transmit_delay: int | None
    cost: int | None
    priority: int | None
    dead_interval: int | None
    hello_interval: int | None
    status: str | None
    network_type: str | None
    bfd: str | None
    mtu: int | None
    mtu_ignore: str | None
    authentication: str | None
    key_rollover_interval: int | None
    ipsec_auth_alg: str | None
    ipsec_enc_alg: str | None
    ipsec_keys: list[Any] | None
    neighbor: list[Any] | None

class RedistributeDict(TypedDict, total=False):
    """Type definition for redistribute child table entry."""
    name: str
    status: str | None
    metric: int | None
    routemap: str | None
    metric_type: str | None

class PassiveInterfaceDict(TypedDict, total=False):
    """Type definition for passive_interface child table entry."""
    name: str

class SummaryAddressDict(TypedDict, total=False):
    """Type definition for summary_address child table entry."""
    id: int | None
    prefix6: str
    advertise: str | None
    tag: int | None


class AreaObject(FortiObject):
    """Typed FortiObject for area child table entry with attribute access."""
    id: str | None
    default_cost: int | None
    nssa_translator_role: str | None
    stub_type: str | None
    type: str | None
    nssa_default_information_originate: str | None
    nssa_default_information_originate_metric: int | None
    nssa_default_information_originate_metric_type: str | None
    nssa_redistribution: str | None
    authentication: str | None
    key_rollover_interval: int | None
    ipsec_auth_alg: str | None
    ipsec_enc_alg: str | None
    ipsec_keys: list[Any] | None
    range: list[Any] | None
    virtual_link: list[Any] | None


class Ospf6InterfaceObject(FortiObject):
    """Typed FortiObject for ospf6_interface child table entry with attribute access."""
    name: str | None
    area_id: str
    interface: str
    retransmit_interval: int | None
    transmit_delay: int | None
    cost: int | None
    priority: int | None
    dead_interval: int | None
    hello_interval: int | None
    status: str | None
    network_type: str | None
    bfd: str | None
    mtu: int | None
    mtu_ignore: str | None
    authentication: str | None
    key_rollover_interval: int | None
    ipsec_auth_alg: str | None
    ipsec_enc_alg: str | None
    ipsec_keys: list[Any] | None
    neighbor: list[Any] | None


class RedistributeObject(FortiObject):
    """Typed FortiObject for redistribute child table entry with attribute access."""
    name: str
    status: str | None
    metric: int | None
    routemap: str | None
    metric_type: str | None


class PassiveInterfaceObject(FortiObject):
    """Typed FortiObject for passive_interface child table entry with attribute access."""
    name: str


class SummaryAddressObject(FortiObject):
    """Typed FortiObject for summary_address child table entry with attribute access."""
    id: int | None
    prefix6: str
    advertise: str | None
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
        default_cost: int | None = ...,
        nssa_translator_role: str | None = ...,
        stub_type: str | None = ...,
        type: str | None = ...,
        nssa_default_information_originate: str | None = ...,
        nssa_default_information_originate_metric: int | None = ...,
        nssa_default_information_originate_metric_type: str | None = ...,
        nssa_redistribution: str | None = ...,
        authentication: str | None = ...,
        key_rollover_interval: int | None = ...,
        ipsec_auth_alg: str | None = ...,
        ipsec_enc_alg: str | None = ...,
        ipsec_keys: list[Any] | None = ...,
        range: list[Any] | None = ...,
        virtual_link: list[Any] | None = ...,
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


class Ospf6InterfaceHelper:
    """Helper class for managing ospf6_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[Ospf6InterfaceObject] | Ospf6InterfaceObject | None: ...
    
    def set(
        self,
        area_id: str,
        interface: str,
        name: str | None = ...,
        retransmit_interval: int | None = ...,
        transmit_delay: int | None = ...,
        cost: int | None = ...,
        priority: int | None = ...,
        dead_interval: int | None = ...,
        hello_interval: int | None = ...,
        status: str | None = ...,
        network_type: str | None = ...,
        bfd: str | None = ...,
        mtu: int | None = ...,
        mtu_ignore: str | None = ...,
        authentication: str | None = ...,
        key_rollover_interval: int | None = ...,
        ipsec_auth_alg: str | None = ...,
        ipsec_enc_alg: str | None = ...,
        ipsec_keys: list[Any] | None = ...,
        neighbor: list[Any] | None = ...,
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
        metric_type: str | None = ...,
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
        prefix6: str,
        id: int | None = ...,
        advertise: str | None = ...,
        tag: int | None = ...,
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

