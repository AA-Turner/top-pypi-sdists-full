""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/address6
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

class Address6TaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class Address6MacaddrItem(TypedDict, total=False):
    """Nested item for macaddr field."""
    macaddr: str


class Address6TaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[Address6TaggingTagsItem]


class Address6SubnetsegmentItem(TypedDict, total=False):
    """Nested item for subnet-segment field."""
    name: str
    type: Literal["any", "specific"]
    value: str


class Address6ListItem(TypedDict, total=False):
    """Nested item for list field."""
    ip: str


class Address6Payload(TypedDict, total=False):
    """Payload type for Address6 operations."""
    name: str
    uuid: str
    type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"]
    route_tag: int
    macaddr: str | list[str] | list[Address6MacaddrItem]
    sdn: str
    ip6: str
    wildcard: str
    start_ip: str
    end_ip: str
    fqdn: str
    country: str
    cache_ttl: int
    color: int
    obj_id: str
    tagging: str | list[str] | list[Address6TaggingItem]
    comment: str
    template: str
    subnet_segment: str | list[str] | list[Address6SubnetsegmentItem]
    host_type: Literal["any", "specific"]
    host: str
    tenant: str
    epg_name: str
    sdn_tag: str
    filter: str
    list: str | list[str] | list[Address6ListItem]
    sdn_addr_type: Literal["private", "public", "all"]
    passive_fqdn_learning: Literal["disable", "enable"]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Address6Response(TypedDict, total=False):
    """Response type for Address6 - use with .dict property for typed dict access."""
    name: str
    uuid: str
    type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"]
    route_tag: int
    macaddr: list[Address6MacaddrItem]
    sdn: str
    ip6: str
    wildcard: str
    start_ip: str
    end_ip: str
    fqdn: str
    country: str
    cache_ttl: int
    color: int
    obj_id: str
    tagging: list[Address6TaggingItem]
    comment: str
    template: str
    subnet_segment: list[Address6SubnetsegmentItem]
    host_type: Literal["any", "specific"]
    host: str
    tenant: str
    epg_name: str
    sdn_tag: str
    filter: str
    list: list[Address6ListItem]
    sdn_addr_type: Literal["private", "public", "all"]
    passive_fqdn_learning: Literal["disable", "enable"]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Address6TaggingTagsItemObject(FortiObject[Address6TaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class Address6MacaddrItemObject(FortiObject[Address6MacaddrItem]):
    """Typed object for macaddr table items with attribute access."""
    macaddr: str


class Address6TaggingItemObject(FortiObject[Address6TaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[Address6TaggingTagsItemObject]


class Address6SubnetsegmentItemObject(FortiObject[Address6SubnetsegmentItem]):
    """Typed object for subnet-segment table items with attribute access."""
    name: str
    type: Literal["any", "specific"]
    value: str


class Address6ListItemObject(FortiObject[Address6ListItem]):
    """Typed object for list table items with attribute access."""
    ip: str


class Address6Object(FortiObject):
    """Typed FortiObject for Address6 with field access."""
    name: str
    uuid: str
    type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"]
    route_tag: int
    macaddr: FortiObjectList[Address6MacaddrItemObject]
    sdn: str
    ip6: str
    wildcard: str
    start_ip: str
    end_ip: str
    fqdn: str
    country: str
    cache_ttl: int
    color: int
    obj_id: str
    tagging: FortiObjectList[Address6TaggingItemObject]
    comment: str
    template: str
    subnet_segment: FortiObjectList[Address6SubnetsegmentItemObject]
    host_type: Literal["any", "specific"]
    host: str
    tenant: str
    epg_name: str
    sdn_tag: str
    filter: str
    sdn_addr_type: Literal["private", "public", "all"]
    passive_fqdn_learning: Literal["disable", "enable"]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Address6:
    """
    
    Endpoint: firewall/address6
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
    ) -> Address6Object: ...
    
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
    ) -> FortiObjectList[Address6Object]: ...
    
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
        payload_dict: Address6Payload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"] | None = ...,
        route_tag: int | None = ...,
        macaddr: str | list[str] | list[Address6MacaddrItem] | None = ...,
        sdn: str | None = ...,
        ip6: str | None = ...,
        wildcard: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        fqdn: str | None = ...,
        country: str | None = ...,
        cache_ttl: int | None = ...,
        color: int | None = ...,
        obj_id: str | None = ...,
        tagging: str | list[str] | list[Address6TaggingItem] | None = ...,
        comment: str | None = ...,
        template: str | None = ...,
        subnet_segment: str | list[str] | list[Address6SubnetsegmentItem] | None = ...,
        host_type: Literal["any", "specific"] | None = ...,
        host: str | None = ...,
        tenant: str | None = ...,
        epg_name: str | None = ...,
        sdn_tag: str | None = ...,
        filter: str | None = ...,
        list: str | list[str] | list[Address6ListItem] | None = ...,
        sdn_addr_type: Literal["private", "public", "all"] | None = ...,
        passive_fqdn_learning: Literal["disable", "enable"] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Address6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Address6Payload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"] | None = ...,
        route_tag: int | None = ...,
        macaddr: str | list[str] | list[Address6MacaddrItem] | None = ...,
        sdn: str | None = ...,
        ip6: str | None = ...,
        wildcard: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        fqdn: str | None = ...,
        country: str | None = ...,
        cache_ttl: int | None = ...,
        color: int | None = ...,
        obj_id: str | None = ...,
        tagging: str | list[str] | list[Address6TaggingItem] | None = ...,
        comment: str | None = ...,
        template: str | None = ...,
        subnet_segment: str | list[str] | list[Address6SubnetsegmentItem] | None = ...,
        host_type: Literal["any", "specific"] | None = ...,
        host: str | None = ...,
        tenant: str | None = ...,
        epg_name: str | None = ...,
        sdn_tag: str | None = ...,
        filter: str | None = ...,
        list: str | list[str] | list[Address6ListItem] | None = ...,
        sdn_addr_type: Literal["private", "public", "all"] | None = ...,
        passive_fqdn_learning: Literal["disable", "enable"] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Address6Object: ...

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
        payload_dict: Address6Payload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"] | None = ...,
        route_tag: int | None = ...,
        macaddr: str | list[str] | list[Address6MacaddrItem] | None = ...,
        sdn: str | None = ...,
        ip6: str | None = ...,
        wildcard: str | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        fqdn: str | None = ...,
        country: str | None = ...,
        cache_ttl: int | None = ...,
        color: int | None = ...,
        obj_id: str | None = ...,
        tagging: str | list[str] | list[Address6TaggingItem] | None = ...,
        comment: str | None = ...,
        template: str | None = ...,
        subnet_segment: str | list[str] | list[Address6SubnetsegmentItem] | None = ...,
        host_type: Literal["any", "specific"] | None = ...,
        host: str | None = ...,
        tenant: str | None = ...,
        epg_name: str | None = ...,
        sdn_tag: str | None = ...,
        filter: str | None = ...,
        list: str | list[str] | list[Address6ListItem] | None = ...,
        sdn_addr_type: Literal["private", "public", "all"] | None = ...,
        passive_fqdn_learning: Literal["disable", "enable"] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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
    "Address6",
    "Address6Payload",
    "Address6Response",
    "Address6Object",
]