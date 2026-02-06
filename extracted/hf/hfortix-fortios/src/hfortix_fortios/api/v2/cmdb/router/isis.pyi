""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/isis
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
from ._isis_child_tables import (
    IsisNetHelper,
    IsisInterfaceHelper,
    SummaryAddressHelper,
    SummaryAddress6Helper,
    RedistributeHelper,
    Redistribute6Helper,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class IsisIsisnetItem(TypedDict, total=False):
    """Nested item for isis-net field."""
    id: int
    net: str


class IsisIsisinterfaceItem(TypedDict, total=False):
    """Nested item for isis-interface field."""
    name: str
    status: Literal["enable", "disable"]
    status6: Literal["enable", "disable"]
    network_type: Literal["broadcast", "point-to-point", "loopback"]
    circuit_type: Literal["level-1-2", "level-1", "level-2"]
    csnp_interval_l1: int
    csnp_interval_l2: int
    hello_interval_l1: int
    hello_interval_l2: int
    hello_multiplier_l1: int
    hello_multiplier_l2: int
    hello_padding: Literal["enable", "disable"]
    lsp_interval: int
    lsp_retransmit_interval: int
    metric_l1: int
    metric_l2: int
    wide_metric_l1: int
    wide_metric_l2: int
    auth_password_l1: str
    auth_password_l2: str
    auth_keychain_l1: str
    auth_keychain_l2: str
    auth_send_only_l1: Literal["enable", "disable"]
    auth_send_only_l2: Literal["enable", "disable"]
    auth_mode_l1: Literal["md5", "password"]
    auth_mode_l2: Literal["md5", "password"]
    priority_l1: int
    priority_l2: int
    mesh_group: Literal["enable", "disable"]
    mesh_group_id: int


class IsisSummaryaddressItem(TypedDict, total=False):
    """Nested item for summary-address field."""
    id: int
    prefix: str
    level: Literal["level-1-2", "level-1", "level-2"]


class IsisSummaryaddress6Item(TypedDict, total=False):
    """Nested item for summary-address6 field."""
    id: int
    prefix6: str
    level: Literal["level-1-2", "level-1", "level-2"]


class IsisRedistributeItem(TypedDict, total=False):
    """Nested item for redistribute field."""
    protocol: str
    status: Literal["enable", "disable"]
    metric: int
    metric_type: Literal["external", "internal"]
    level: Literal["level-1-2", "level-1", "level-2"]
    routemap: str


class IsisRedistribute6Item(TypedDict, total=False):
    """Nested item for redistribute6 field."""
    protocol: str
    status: Literal["enable", "disable"]
    metric: int
    metric_type: Literal["external", "internal"]
    level: Literal["level-1-2", "level-1", "level-2"]
    routemap: str


class IsisPayload(TypedDict, total=False):
    """Payload type for Isis operations."""
    is_type: Literal["level-1-2", "level-1", "level-2-only"]
    adv_passive_only: Literal["enable", "disable"]
    adv_passive_only6: Literal["enable", "disable"]
    auth_mode_l1: Literal["password", "md5"]
    auth_mode_l2: Literal["password", "md5"]
    auth_password_l1: str
    auth_password_l2: str
    auth_keychain_l1: str
    auth_keychain_l2: str
    auth_sendonly_l1: Literal["enable", "disable"]
    auth_sendonly_l2: Literal["enable", "disable"]
    ignore_lsp_errors: Literal["enable", "disable"]
    lsp_gen_interval_l1: int
    lsp_gen_interval_l2: int
    lsp_refresh_interval: int
    max_lsp_lifetime: int
    spf_interval_exp_l1: str
    spf_interval_exp_l2: str
    dynamic_hostname: Literal["enable", "disable"]
    adjacency_check: Literal["enable", "disable"]
    adjacency_check6: Literal["enable", "disable"]
    overload_bit: Literal["enable", "disable"]
    overload_bit_suppress: str | list[str]
    overload_bit_on_startup: int
    default_originate: Literal["enable", "disable"]
    default_originate6: Literal["enable", "disable"]
    metric_style: Literal["narrow", "wide", "transition", "narrow-transition", "narrow-transition-l1", "narrow-transition-l2", "wide-l1", "wide-l2", "wide-transition", "wide-transition-l1", "wide-transition-l2", "transition-l1", "transition-l2"]
    redistribute_l1: Literal["enable", "disable"]
    redistribute_l1_list: str
    redistribute_l2: Literal["enable", "disable"]
    redistribute_l2_list: str
    redistribute6_l1: Literal["enable", "disable"]
    redistribute6_l1_list: str
    redistribute6_l2: Literal["enable", "disable"]
    redistribute6_l2_list: str
    isis_net: str | list[str] | list[IsisIsisnetItem]
    isis_interface: str | list[str] | list[IsisIsisinterfaceItem]
    summary_address: str | list[str] | list[IsisSummaryaddressItem]
    summary_address6: str | list[str] | list[IsisSummaryaddress6Item]
    redistribute: str | list[str] | list[IsisRedistributeItem]
    redistribute6: str | list[str] | list[IsisRedistribute6Item]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IsisResponse(TypedDict, total=False):
    """Response type for Isis - use with .dict property for typed dict access."""
    is_type: Literal["level-1-2", "level-1", "level-2-only"]
    adv_passive_only: Literal["enable", "disable"]
    adv_passive_only6: Literal["enable", "disable"]
    auth_mode_l1: Literal["password", "md5"]
    auth_mode_l2: Literal["password", "md5"]
    auth_password_l1: str
    auth_password_l2: str
    auth_keychain_l1: str
    auth_keychain_l2: str
    auth_sendonly_l1: Literal["enable", "disable"]
    auth_sendonly_l2: Literal["enable", "disable"]
    ignore_lsp_errors: Literal["enable", "disable"]
    lsp_gen_interval_l1: int
    lsp_gen_interval_l2: int
    lsp_refresh_interval: int
    max_lsp_lifetime: int
    spf_interval_exp_l1: str
    spf_interval_exp_l2: str
    dynamic_hostname: Literal["enable", "disable"]
    adjacency_check: Literal["enable", "disable"]
    adjacency_check6: Literal["enable", "disable"]
    overload_bit: Literal["enable", "disable"]
    overload_bit_suppress: str
    overload_bit_on_startup: int
    default_originate: Literal["enable", "disable"]
    default_originate6: Literal["enable", "disable"]
    metric_style: Literal["narrow", "wide", "transition", "narrow-transition", "narrow-transition-l1", "narrow-transition-l2", "wide-l1", "wide-l2", "wide-transition", "wide-transition-l1", "wide-transition-l2", "transition-l1", "transition-l2"]
    redistribute_l1: Literal["enable", "disable"]
    redistribute_l1_list: str
    redistribute_l2: Literal["enable", "disable"]
    redistribute_l2_list: str
    redistribute6_l1: Literal["enable", "disable"]
    redistribute6_l1_list: str
    redistribute6_l2: Literal["enable", "disable"]
    redistribute6_l2_list: str
    isis_net: list[IsisIsisnetItem]
    isis_interface: list[IsisIsisinterfaceItem]
    summary_address: list[IsisSummaryaddressItem]
    summary_address6: list[IsisSummaryaddress6Item]
    redistribute: list[IsisRedistributeItem]
    redistribute6: list[IsisRedistribute6Item]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IsisIsisnetItemObject(FortiObject[IsisIsisnetItem]):
    """Typed object for isis-net table items with attribute access."""
    id: int
    net: str


class IsisIsisinterfaceItemObject(FortiObject[IsisIsisinterfaceItem]):
    """Typed object for isis-interface table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    status6: Literal["enable", "disable"]
    network_type: Literal["broadcast", "point-to-point", "loopback"]
    circuit_type: Literal["level-1-2", "level-1", "level-2"]
    csnp_interval_l1: int
    csnp_interval_l2: int
    hello_interval_l1: int
    hello_interval_l2: int
    hello_multiplier_l1: int
    hello_multiplier_l2: int
    hello_padding: Literal["enable", "disable"]
    lsp_interval: int
    lsp_retransmit_interval: int
    metric_l1: int
    metric_l2: int
    wide_metric_l1: int
    wide_metric_l2: int
    auth_password_l1: str
    auth_password_l2: str
    auth_keychain_l1: str
    auth_keychain_l2: str
    auth_send_only_l1: Literal["enable", "disable"]
    auth_send_only_l2: Literal["enable", "disable"]
    auth_mode_l1: Literal["md5", "password"]
    auth_mode_l2: Literal["md5", "password"]
    priority_l1: int
    priority_l2: int
    mesh_group: Literal["enable", "disable"]
    mesh_group_id: int


class IsisSummaryaddressItemObject(FortiObject[IsisSummaryaddressItem]):
    """Typed object for summary-address table items with attribute access."""
    id: int
    prefix: str
    level: Literal["level-1-2", "level-1", "level-2"]


class IsisSummaryaddress6ItemObject(FortiObject[IsisSummaryaddress6Item]):
    """Typed object for summary-address6 table items with attribute access."""
    id: int
    prefix6: str
    level: Literal["level-1-2", "level-1", "level-2"]


class IsisRedistributeItemObject(FortiObject[IsisRedistributeItem]):
    """Typed object for redistribute table items with attribute access."""
    protocol: str
    status: Literal["enable", "disable"]
    metric: int
    metric_type: Literal["external", "internal"]
    level: Literal["level-1-2", "level-1", "level-2"]
    routemap: str


class IsisRedistribute6ItemObject(FortiObject[IsisRedistribute6Item]):
    """Typed object for redistribute6 table items with attribute access."""
    protocol: str
    status: Literal["enable", "disable"]
    metric: int
    metric_type: Literal["external", "internal"]
    level: Literal["level-1-2", "level-1", "level-2"]
    routemap: str


class IsisObject(FortiObject):
    """Typed FortiObject for Isis with field access."""
    is_type: Literal["level-1-2", "level-1", "level-2-only"]
    adv_passive_only: Literal["enable", "disable"]
    adv_passive_only6: Literal["enable", "disable"]
    auth_mode_l1: Literal["password", "md5"]
    auth_mode_l2: Literal["password", "md5"]
    auth_password_l1: str
    auth_password_l2: str
    auth_keychain_l1: str
    auth_keychain_l2: str
    auth_sendonly_l1: Literal["enable", "disable"]
    auth_sendonly_l2: Literal["enable", "disable"]
    ignore_lsp_errors: Literal["enable", "disable"]
    lsp_gen_interval_l1: int
    lsp_gen_interval_l2: int
    lsp_refresh_interval: int
    max_lsp_lifetime: int
    spf_interval_exp_l1: str
    spf_interval_exp_l2: str
    dynamic_hostname: Literal["enable", "disable"]
    adjacency_check: Literal["enable", "disable"]
    adjacency_check6: Literal["enable", "disable"]
    overload_bit: Literal["enable", "disable"]
    overload_bit_suppress: str
    overload_bit_on_startup: int
    default_originate: Literal["enable", "disable"]
    default_originate6: Literal["enable", "disable"]
    metric_style: Literal["narrow", "wide", "transition", "narrow-transition", "narrow-transition-l1", "narrow-transition-l2", "wide-l1", "wide-l2", "wide-transition", "wide-transition-l1", "wide-transition-l2", "transition-l1", "transition-l2"]
    redistribute_l1: Literal["enable", "disable"]
    redistribute_l1_list: str
    redistribute_l2: Literal["enable", "disable"]
    redistribute_l2_list: str
    redistribute6_l1: Literal["enable", "disable"]
    redistribute6_l1_list: str
    redistribute6_l2: Literal["enable", "disable"]
    redistribute6_l2_list: str
    isis_net: FortiObjectList[IsisIsisnetItemObject]
    isis_interface: FortiObjectList[IsisIsisinterfaceItemObject]
    summary_address: FortiObjectList[IsisSummaryaddressItemObject]
    summary_address6: FortiObjectList[IsisSummaryaddress6ItemObject]
    redistribute: FortiObjectList[IsisRedistributeItemObject]
    redistribute6: FortiObjectList[IsisRedistribute6ItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Isis:
    """
    
    Endpoint: router/isis
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    # Child table helpers
    isis_net: IsisNetHelper
    isis_interface: IsisInterfaceHelper
    summary_address: SummaryAddressHelper
    summary_address6: SummaryAddress6Helper
    redistribute: RedistributeHelper
    redistribute6: Redistribute6Helper
    
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
    ) -> IsisObject: ...
    
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
        payload_dict: IsisPayload | None = ...,
        is_type: Literal["level-1-2", "level-1", "level-2-only"] | None = ...,
        adv_passive_only: Literal["enable", "disable"] | None = ...,
        adv_passive_only6: Literal["enable", "disable"] | None = ...,
        auth_mode_l1: Literal["password", "md5"] | None = ...,
        auth_mode_l2: Literal["password", "md5"] | None = ...,
        auth_password_l1: str | None = ...,
        auth_password_l2: str | None = ...,
        auth_keychain_l1: str | None = ...,
        auth_keychain_l2: str | None = ...,
        auth_sendonly_l1: Literal["enable", "disable"] | None = ...,
        auth_sendonly_l2: Literal["enable", "disable"] | None = ...,
        ignore_lsp_errors: Literal["enable", "disable"] | None = ...,
        lsp_gen_interval_l1: int | None = ...,
        lsp_gen_interval_l2: int | None = ...,
        lsp_refresh_interval: int | None = ...,
        max_lsp_lifetime: int | None = ...,
        spf_interval_exp_l1: str | None = ...,
        spf_interval_exp_l2: str | None = ...,
        dynamic_hostname: Literal["enable", "disable"] | None = ...,
        adjacency_check: Literal["enable", "disable"] | None = ...,
        adjacency_check6: Literal["enable", "disable"] | None = ...,
        overload_bit: Literal["enable", "disable"] | None = ...,
        overload_bit_suppress: str | list[str] | None = ...,
        overload_bit_on_startup: int | None = ...,
        default_originate: Literal["enable", "disable"] | None = ...,
        default_originate6: Literal["enable", "disable"] | None = ...,
        metric_style: Literal["narrow", "wide", "transition", "narrow-transition", "narrow-transition-l1", "narrow-transition-l2", "wide-l1", "wide-l2", "wide-transition", "wide-transition-l1", "wide-transition-l2", "transition-l1", "transition-l2"] | None = ...,
        redistribute_l1: Literal["enable", "disable"] | None = ...,
        redistribute_l1_list: str | None = ...,
        redistribute_l2: Literal["enable", "disable"] | None = ...,
        redistribute_l2_list: str | None = ...,
        redistribute6_l1: Literal["enable", "disable"] | None = ...,
        redistribute6_l1_list: str | None = ...,
        redistribute6_l2: Literal["enable", "disable"] | None = ...,
        redistribute6_l2_list: str | None = ...,
        isis_net: str | list[str] | list[IsisIsisnetItem] | None = ...,
        isis_interface: str | list[str] | list[IsisIsisinterfaceItem] | None = ...,
        summary_address: str | list[str] | list[IsisSummaryaddressItem] | None = ...,
        summary_address6: str | list[str] | list[IsisSummaryaddress6Item] | None = ...,
        redistribute: str | list[str] | list[IsisRedistributeItem] | None = ...,
        redistribute6: str | list[str] | list[IsisRedistribute6Item] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IsisObject: ...


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
        payload_dict: IsisPayload | None = ...,
        is_type: Literal["level-1-2", "level-1", "level-2-only"] | None = ...,
        adv_passive_only: Literal["enable", "disable"] | None = ...,
        adv_passive_only6: Literal["enable", "disable"] | None = ...,
        auth_mode_l1: Literal["password", "md5"] | None = ...,
        auth_mode_l2: Literal["password", "md5"] | None = ...,
        auth_password_l1: str | None = ...,
        auth_password_l2: str | None = ...,
        auth_keychain_l1: str | None = ...,
        auth_keychain_l2: str | None = ...,
        auth_sendonly_l1: Literal["enable", "disable"] | None = ...,
        auth_sendonly_l2: Literal["enable", "disable"] | None = ...,
        ignore_lsp_errors: Literal["enable", "disable"] | None = ...,
        lsp_gen_interval_l1: int | None = ...,
        lsp_gen_interval_l2: int | None = ...,
        lsp_refresh_interval: int | None = ...,
        max_lsp_lifetime: int | None = ...,
        spf_interval_exp_l1: str | None = ...,
        spf_interval_exp_l2: str | None = ...,
        dynamic_hostname: Literal["enable", "disable"] | None = ...,
        adjacency_check: Literal["enable", "disable"] | None = ...,
        adjacency_check6: Literal["enable", "disable"] | None = ...,
        overload_bit: Literal["enable", "disable"] | None = ...,
        overload_bit_suppress: Literal["external", "interlevel"] | list[str] | None = ...,
        overload_bit_on_startup: int | None = ...,
        default_originate: Literal["enable", "disable"] | None = ...,
        default_originate6: Literal["enable", "disable"] | None = ...,
        metric_style: Literal["narrow", "wide", "transition", "narrow-transition", "narrow-transition-l1", "narrow-transition-l2", "wide-l1", "wide-l2", "wide-transition", "wide-transition-l1", "wide-transition-l2", "transition-l1", "transition-l2"] | None = ...,
        redistribute_l1: Literal["enable", "disable"] | None = ...,
        redistribute_l1_list: str | None = ...,
        redistribute_l2: Literal["enable", "disable"] | None = ...,
        redistribute_l2_list: str | None = ...,
        redistribute6_l1: Literal["enable", "disable"] | None = ...,
        redistribute6_l1_list: str | None = ...,
        redistribute6_l2: Literal["enable", "disable"] | None = ...,
        redistribute6_l2_list: str | None = ...,
        isis_net: str | list[str] | list[IsisIsisnetItem] | None = ...,
        isis_interface: str | list[str] | list[IsisIsisinterfaceItem] | None = ...,
        summary_address: str | list[str] | list[IsisSummaryaddressItem] | None = ...,
        summary_address6: str | list[str] | list[IsisSummaryaddress6Item] | None = ...,
        redistribute: str | list[str] | list[IsisRedistributeItem] | None = ...,
        redistribute6: str | list[str] | list[IsisRedistribute6Item] | None = ...,
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
    "Isis",
    "IsisPayload",
    "IsisResponse",
    "IsisObject",
]