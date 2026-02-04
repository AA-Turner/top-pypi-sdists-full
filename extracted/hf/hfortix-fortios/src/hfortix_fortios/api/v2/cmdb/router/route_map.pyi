""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/route_map
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class RouteMapRuleSetaspathItem(TypedDict, total=False):
    """Nested item for rule.set-aspath field."""
    asn: str


class RouteMapRuleSetcommunityItem(TypedDict, total=False):
    """Nested item for rule.set-community field."""
    community: str


class RouteMapRuleSetextcommunityrtItem(TypedDict, total=False):
    """Nested item for rule.set-extcommunity-rt field."""
    community: str


class RouteMapRuleSetextcommunitysooItem(TypedDict, total=False):
    """Nested item for rule.set-extcommunity-soo field."""
    community: str


class RouteMapRuleItem(TypedDict, total=False):
    """Nested item for rule field."""
    id: int
    action: Literal["permit", "deny"]
    match_as_path: str
    match_community: str
    match_extcommunity: str
    match_community_exact: Literal["enable", "disable"]
    match_extcommunity_exact: Literal["enable", "disable"]
    match_origin: Literal["none", "egp", "igp", "incomplete"]
    match_interface: str
    match_ip_address: str
    match_ip6_address: str
    match_ip_nexthop: str
    match_ip6_nexthop: str
    match_metric: int
    match_route_type: Literal["external-type1", "external-type2", "none"]
    match_tag: int
    match_vrf: int
    match_suppress: Literal["enable", "disable"]
    set_aggregator_as: int
    set_aggregator_ip: str
    set_aspath_action: Literal["prepend", "replace"]
    set_aspath: str | list[str] | list[RouteMapRuleSetaspathItem]
    set_atomic_aggregate: Literal["enable", "disable"]
    set_community_delete: str
    set_community: str | list[str] | list[RouteMapRuleSetcommunityItem]
    set_community_additive: Literal["enable", "disable"]
    set_dampening_reachability_half_life: int
    set_dampening_reuse: int
    set_dampening_suppress: int
    set_dampening_max_suppress: int
    set_dampening_unreachability_half_life: int
    set_extcommunity_rt: str | list[str] | list[RouteMapRuleSetextcommunityrtItem]
    set_extcommunity_soo: str | list[str] | list[RouteMapRuleSetextcommunitysooItem]
    set_ip_nexthop: str
    set_ip_prefsrc: str
    set_vpnv4_nexthop: str
    set_ip6_nexthop: str
    set_ip6_nexthop_local: str
    set_vpnv6_nexthop: str
    set_vpnv6_nexthop_local: str
    set_local_preference: int
    set_metric: int
    set_metric_type: Literal["external-type1", "external-type2", "none"]
    set_originator_id: str
    set_origin: Literal["none", "egp", "igp", "incomplete"]
    set_tag: int
    set_weight: int
    set_route_tag: int
    set_priority: int


class RouteMapPayload(TypedDict, total=False):
    """Payload type for RouteMap operations."""
    name: str
    comments: str
    rule: str | list[str] | list[RouteMapRuleItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RouteMapResponse(TypedDict, total=False):
    """Response type for RouteMap - use with .dict property for typed dict access."""
    name: str
    comments: str
    rule: list[RouteMapRuleItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RouteMapRuleSetaspathItemObject(FortiObject[RouteMapRuleSetaspathItem]):
    """Typed object for rule.set-aspath table items with attribute access."""
    asn: str


class RouteMapRuleSetcommunityItemObject(FortiObject[RouteMapRuleSetcommunityItem]):
    """Typed object for rule.set-community table items with attribute access."""
    community: str


class RouteMapRuleSetextcommunityrtItemObject(FortiObject[RouteMapRuleSetextcommunityrtItem]):
    """Typed object for rule.set-extcommunity-rt table items with attribute access."""
    community: str


class RouteMapRuleSetextcommunitysooItemObject(FortiObject[RouteMapRuleSetextcommunitysooItem]):
    """Typed object for rule.set-extcommunity-soo table items with attribute access."""
    community: str


class RouteMapRuleItemObject(FortiObject[RouteMapRuleItem]):
    """Typed object for rule table items with attribute access."""
    id: int
    action: Literal["permit", "deny"]
    match_as_path: str
    match_community: str
    match_extcommunity: str
    match_community_exact: Literal["enable", "disable"]
    match_extcommunity_exact: Literal["enable", "disable"]
    match_origin: Literal["none", "egp", "igp", "incomplete"]
    match_interface: str
    match_ip_address: str
    match_ip6_address: str
    match_ip_nexthop: str
    match_ip6_nexthop: str
    match_metric: int
    match_route_type: Literal["external-type1", "external-type2", "none"]
    match_tag: int
    match_vrf: int
    match_suppress: Literal["enable", "disable"]
    set_aggregator_as: int
    set_aggregator_ip: str
    set_aspath_action: Literal["prepend", "replace"]
    set_aspath: FortiObjectList[RouteMapRuleSetaspathItemObject]
    set_atomic_aggregate: Literal["enable", "disable"]
    set_community_delete: str
    set_community: FortiObjectList[RouteMapRuleSetcommunityItemObject]
    set_community_additive: Literal["enable", "disable"]
    set_dampening_reachability_half_life: int
    set_dampening_reuse: int
    set_dampening_suppress: int
    set_dampening_max_suppress: int
    set_dampening_unreachability_half_life: int
    set_extcommunity_rt: FortiObjectList[RouteMapRuleSetextcommunityrtItemObject]
    set_extcommunity_soo: FortiObjectList[RouteMapRuleSetextcommunitysooItemObject]
    set_ip_nexthop: str
    set_ip_prefsrc: str
    set_vpnv4_nexthop: str
    set_ip6_nexthop: str
    set_ip6_nexthop_local: str
    set_vpnv6_nexthop: str
    set_vpnv6_nexthop_local: str
    set_local_preference: int
    set_metric: int
    set_metric_type: Literal["external-type1", "external-type2", "none"]
    set_originator_id: str
    set_origin: Literal["none", "egp", "igp", "incomplete"]
    set_tag: int
    set_weight: int
    set_route_tag: int
    set_priority: int


class RouteMapObject(FortiObject):
    """Typed FortiObject for RouteMap with field access."""
    name: str
    comments: str
    rule: FortiObjectList[RouteMapRuleItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class RouteMap:
    """
    
    Endpoint: router/route_map
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
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
    ) -> RouteMapObject: ...
    
    @overload
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
    ) -> FortiObjectList[RouteMapObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: RouteMapPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[RouteMapRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RouteMapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RouteMapPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[RouteMapRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RouteMapObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

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
        payload_dict: RouteMapPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[RouteMapRuleItem] | None = ...,
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
    "RouteMap",
    "RouteMapPayload",
    "RouteMapResponse",
    "RouteMapObject",
]