"""
Child Table Helper Type Stubs for router/isis

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class IsisNetDict(TypedDict, total=False):
    """Type definition for isis_net child table entry."""
    id: int | None
    net: str | None

class IsisInterfaceDict(TypedDict, total=False):
    """Type definition for isis_interface child table entry."""
    name: str | None
    status: str | None
    status6: str | None
    network_type: str | None
    circuit_type: str | None
    csnp_interval_l1: int | None
    csnp_interval_l2: int | None
    hello_interval_l1: int | None
    hello_interval_l2: int | None
    hello_multiplier_l1: int | None
    hello_multiplier_l2: int | None
    hello_padding: str | None
    lsp_interval: int | None
    lsp_retransmit_interval: int | None
    metric_l1: int | None
    metric_l2: int | None
    wide_metric_l1: int | None
    wide_metric_l2: int | None
    auth_password_l1: str | None
    auth_password_l2: str | None
    auth_keychain_l1: str | None
    auth_keychain_l2: str | None
    auth_send_only_l1: str | None
    auth_send_only_l2: str | None
    auth_mode_l1: str | None
    auth_mode_l2: str | None
    priority_l1: int | None
    priority_l2: int | None
    mesh_group: str | None
    mesh_group_id: int | None

class SummaryAddressDict(TypedDict, total=False):
    """Type definition for summary_address child table entry."""
    id: int | None
    prefix: str
    level: str | None

class SummaryAddress6Dict(TypedDict, total=False):
    """Type definition for summary_address6 child table entry."""
    id: int | None
    prefix6: str
    level: str | None

class RedistributeDict(TypedDict, total=False):
    """Type definition for redistribute child table entry."""
    protocol: str
    status: str | None
    metric: int | None
    metric_type: str | None
    level: str | None
    routemap: str | None

class Redistribute6Dict(TypedDict, total=False):
    """Type definition for redistribute6 child table entry."""
    protocol: str
    status: str | None
    metric: int | None
    metric_type: str | None
    level: str | None
    routemap: str | None


class IsisNetObject(FortiObject):
    """Typed FortiObject for isis_net child table entry with attribute access."""
    id: int | None
    net: str | None


class IsisInterfaceObject(FortiObject):
    """Typed FortiObject for isis_interface child table entry with attribute access."""
    name: str | None
    status: str | None
    status6: str | None
    network_type: str | None
    circuit_type: str | None
    csnp_interval_l1: int | None
    csnp_interval_l2: int | None
    hello_interval_l1: int | None
    hello_interval_l2: int | None
    hello_multiplier_l1: int | None
    hello_multiplier_l2: int | None
    hello_padding: str | None
    lsp_interval: int | None
    lsp_retransmit_interval: int | None
    metric_l1: int | None
    metric_l2: int | None
    wide_metric_l1: int | None
    wide_metric_l2: int | None
    auth_password_l1: str | None
    auth_password_l2: str | None
    auth_keychain_l1: str | None
    auth_keychain_l2: str | None
    auth_send_only_l1: str | None
    auth_send_only_l2: str | None
    auth_mode_l1: str | None
    auth_mode_l2: str | None
    priority_l1: int | None
    priority_l2: int | None
    mesh_group: str | None
    mesh_group_id: int | None


class SummaryAddressObject(FortiObject):
    """Typed FortiObject for summary_address child table entry with attribute access."""
    id: int | None
    prefix: str
    level: str | None


class SummaryAddress6Object(FortiObject):
    """Typed FortiObject for summary_address6 child table entry with attribute access."""
    id: int | None
    prefix6: str
    level: str | None


class RedistributeObject(FortiObject):
    """Typed FortiObject for redistribute child table entry with attribute access."""
    protocol: str
    status: str | None
    metric: int | None
    metric_type: str | None
    level: str | None
    routemap: str | None


class Redistribute6Object(FortiObject):
    """Typed FortiObject for redistribute6 child table entry with attribute access."""
    protocol: str
    status: str | None
    metric: int | None
    metric_type: str | None
    level: str | None
    routemap: str | None



class IsisNetHelper:
    """Helper class for managing isis_net child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[IsisNetObject] | IsisNetObject | None: ...
    
    def set(
        self,
        id: int | None = ...,
        net: str | None = ...,
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


class IsisInterfaceHelper:
    """Helper class for managing isis_interface child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[IsisInterfaceObject] | IsisInterfaceObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        status: str | None = ...,
        status6: str | None = ...,
        network_type: str | None = ...,
        circuit_type: str | None = ...,
        csnp_interval_l1: int | None = ...,
        csnp_interval_l2: int | None = ...,
        hello_interval_l1: int | None = ...,
        hello_interval_l2: int | None = ...,
        hello_multiplier_l1: int | None = ...,
        hello_multiplier_l2: int | None = ...,
        hello_padding: str | None = ...,
        lsp_interval: int | None = ...,
        lsp_retransmit_interval: int | None = ...,
        metric_l1: int | None = ...,
        metric_l2: int | None = ...,
        wide_metric_l1: int | None = ...,
        wide_metric_l2: int | None = ...,
        auth_password_l1: str | None = ...,
        auth_password_l2: str | None = ...,
        auth_keychain_l1: str | None = ...,
        auth_keychain_l2: str | None = ...,
        auth_send_only_l1: str | None = ...,
        auth_send_only_l2: str | None = ...,
        auth_mode_l1: str | None = ...,
        auth_mode_l2: str | None = ...,
        priority_l1: int | None = ...,
        priority_l2: int | None = ...,
        mesh_group: str | None = ...,
        mesh_group_id: int | None = ...,
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
        level: str | None = ...,
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


class SummaryAddress6Helper:
    """Helper class for managing summary_address6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[SummaryAddress6Object] | SummaryAddress6Object | None: ...
    
    def set(
        self,
        prefix6: str,
        id: int | None = ...,
        level: str | None = ...,
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
        protocol: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[RedistributeObject] | RedistributeObject | None: ...
    
    def set(
        self,
        protocol: str,
        status: str | None = ...,
        metric: int | None = ...,
        metric_type: str | None = ...,
        level: str | None = ...,
        routemap: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        protocol: str,
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
        protocol: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class Redistribute6Helper:
    """Helper class for managing redistribute6 child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        protocol: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[Redistribute6Object] | Redistribute6Object | None: ...
    
    def set(
        self,
        protocol: str,
        status: str | None = ...,
        metric: int | None = ...,
        metric_type: str | None = ...,
        level: str | None = ...,
        routemap: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        protocol: str,
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
        protocol: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

