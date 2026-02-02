""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/address
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

class AddressTaggingTagsItem(TypedDict, total=False):
    """Nested item for tagging.tags field."""
    name: str


class AddressMacaddrItem(TypedDict, total=False):
    """Nested item for macaddr field."""
    macaddr: str


class AddressFssogroupItem(TypedDict, total=False):
    """Nested item for fsso-group field."""
    name: str


class AddressSsoattributevalueItem(TypedDict, total=False):
    """Nested item for sso-attribute-value field."""
    name: str


class AddressListItem(TypedDict, total=False):
    """Nested item for list field."""
    ip: str


class AddressTaggingItem(TypedDict, total=False):
    """Nested item for tagging field."""
    name: str
    category: str
    tags: str | list[str] | list[AddressTaggingTagsItem]


class AddressPayload(TypedDict, total=False):
    """Payload type for Address operations."""
    name: str
    uuid: str
    subnet: str
    type: Literal["ipmask", "iprange", "fqdn", "geography", "wildcard", "dynamic", "interface-subnet", "mac", "route-tag"]
    route_tag: int
    sub_type: Literal["sdn", "clearpass-spt", "fsso", "rsso", "ems-tag", "fortivoice-tag", "fortinac-tag", "swc-tag", "device-identification", "external-resource", "obsolete"]
    clearpass_spt: Literal["unknown", "healthy", "quarantine", "checkup", "transient", "infected"]
    macaddr: str | list[str] | list[AddressMacaddrItem]
    start_ip: str
    end_ip: str
    fqdn: str
    country: str
    wildcard_fqdn: str
    cache_ttl: int
    wildcard: str
    sdn: str
    fsso_group: str | list[str] | list[AddressFssogroupItem]
    sso_attribute_value: str | list[str] | list[AddressSsoattributevalueItem]
    interface: str
    tenant: str
    organization: str
    epg_name: str
    subnet_name: str
    sdn_tag: str
    policy_group: str
    obj_tag: str
    obj_type: Literal["ip", "mac"]
    tag_detection_level: str
    tag_type: str
    hw_vendor: str
    hw_model: str
    os: str
    sw_version: str
    comment: str
    associated_interface: str
    color: int
    filter: str
    sdn_addr_type: Literal["private", "public", "all"]
    node_ip_only: Literal["enable", "disable"]
    obj_id: str
    list: str | list[str] | list[AddressListItem]
    tagging: str | list[str] | list[AddressTaggingItem]
    allow_routing: Literal["enable", "disable"]
    passive_fqdn_learning: Literal["disable", "enable"]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AddressResponse(TypedDict, total=False):
    """Response type for Address - use with .dict property for typed dict access."""
    name: str
    uuid: str
    subnet: str
    type: Literal["ipmask", "iprange", "fqdn", "geography", "wildcard", "dynamic", "interface-subnet", "mac", "route-tag"]
    route_tag: int
    sub_type: Literal["sdn", "clearpass-spt", "fsso", "rsso", "ems-tag", "fortivoice-tag", "fortinac-tag", "swc-tag", "device-identification", "external-resource", "obsolete"]
    clearpass_spt: Literal["unknown", "healthy", "quarantine", "checkup", "transient", "infected"]
    macaddr: list[AddressMacaddrItem]
    start_ip: str
    end_ip: str
    fqdn: str
    country: str
    wildcard_fqdn: str
    cache_ttl: int
    wildcard: str
    sdn: str
    fsso_group: list[AddressFssogroupItem]
    sso_attribute_value: list[AddressSsoattributevalueItem]
    interface: str
    tenant: str
    organization: str
    epg_name: str
    subnet_name: str
    sdn_tag: str
    policy_group: str
    obj_tag: str
    obj_type: Literal["ip", "mac"]
    tag_detection_level: str
    tag_type: str
    hw_vendor: str
    hw_model: str
    os: str
    sw_version: str
    comment: str
    associated_interface: str
    color: int
    filter: str
    sdn_addr_type: Literal["private", "public", "all"]
    node_ip_only: Literal["enable", "disable"]
    obj_id: str
    list: list[AddressListItem]
    tagging: list[AddressTaggingItem]
    allow_routing: Literal["enable", "disable"]
    passive_fqdn_learning: Literal["disable", "enable"]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AddressTaggingTagsItemObject(FortiObject[AddressTaggingTagsItem]):
    """Typed object for tagging.tags table items with attribute access."""
    name: str


class AddressMacaddrItemObject(FortiObject[AddressMacaddrItem]):
    """Typed object for macaddr table items with attribute access."""
    macaddr: str


class AddressFssogroupItemObject(FortiObject[AddressFssogroupItem]):
    """Typed object for fsso-group table items with attribute access."""
    name: str


class AddressSsoattributevalueItemObject(FortiObject[AddressSsoattributevalueItem]):
    """Typed object for sso-attribute-value table items with attribute access."""
    name: str


class AddressListItemObject(FortiObject[AddressListItem]):
    """Typed object for list table items with attribute access."""
    ip: str


class AddressTaggingItemObject(FortiObject[AddressTaggingItem]):
    """Typed object for tagging table items with attribute access."""
    name: str
    category: str
    tags: FortiObjectList[AddressTaggingTagsItemObject]


class AddressObject(FortiObject):
    """Typed FortiObject for Address with field access."""
    name: str
    uuid: str
    subnet: str
    type: Literal["ipmask", "iprange", "fqdn", "geography", "wildcard", "dynamic", "interface-subnet", "mac", "route-tag"]
    route_tag: int
    sub_type: Literal["sdn", "clearpass-spt", "fsso", "rsso", "ems-tag", "fortivoice-tag", "fortinac-tag", "swc-tag", "device-identification", "external-resource", "obsolete"]
    clearpass_spt: Literal["unknown", "healthy", "quarantine", "checkup", "transient", "infected"]
    macaddr: FortiObjectList[AddressMacaddrItemObject]
    start_ip: str
    end_ip: str
    fqdn: str
    country: str
    wildcard_fqdn: str
    cache_ttl: int
    wildcard: str
    sdn: str
    fsso_group: FortiObjectList[AddressFssogroupItemObject]
    sso_attribute_value: FortiObjectList[AddressSsoattributevalueItemObject]
    interface: str
    tenant: str
    organization: str
    epg_name: str
    subnet_name: str
    sdn_tag: str
    policy_group: str
    obj_tag: str
    obj_type: Literal["ip", "mac"]
    tag_detection_level: str
    tag_type: str
    hw_vendor: str
    hw_model: str
    os: str
    sw_version: str
    comment: str
    associated_interface: str
    color: int
    filter: str
    sdn_addr_type: Literal["private", "public", "all"]
    node_ip_only: Literal["enable", "disable"]
    obj_id: str
    tagging: FortiObjectList[AddressTaggingItemObject]
    allow_routing: Literal["enable", "disable"]
    passive_fqdn_learning: Literal["disable", "enable"]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Address:
    """
    
    Endpoint: firewall/address
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
    ) -> AddressObject: ...
    
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
    ) -> FortiObjectList[AddressObject]: ...
    
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
        payload_dict: AddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        subnet: str | None = ...,
        type: Literal["ipmask", "iprange", "fqdn", "geography", "wildcard", "dynamic", "interface-subnet", "mac", "route-tag"] | None = ...,
        route_tag: int | None = ...,
        sub_type: Literal["sdn", "clearpass-spt", "fsso", "rsso", "ems-tag", "fortivoice-tag", "fortinac-tag", "swc-tag", "device-identification", "external-resource", "obsolete"] | None = ...,
        clearpass_spt: Literal["unknown", "healthy", "quarantine", "checkup", "transient", "infected"] | None = ...,
        macaddr: str | list[str] | list[AddressMacaddrItem] | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        fqdn: str | None = ...,
        country: str | None = ...,
        wildcard_fqdn: str | None = ...,
        cache_ttl: int | None = ...,
        wildcard: str | None = ...,
        sdn: str | None = ...,
        fsso_group: str | list[str] | list[AddressFssogroupItem] | None = ...,
        sso_attribute_value: str | list[str] | list[AddressSsoattributevalueItem] | None = ...,
        interface: str | None = ...,
        tenant: str | None = ...,
        organization: str | None = ...,
        epg_name: str | None = ...,
        subnet_name: str | None = ...,
        sdn_tag: str | None = ...,
        policy_group: str | None = ...,
        obj_tag: str | None = ...,
        obj_type: Literal["ip", "mac"] | None = ...,
        tag_detection_level: str | None = ...,
        tag_type: str | None = ...,
        hw_vendor: str | None = ...,
        hw_model: str | None = ...,
        os: str | None = ...,
        sw_version: str | None = ...,
        comment: str | None = ...,
        associated_interface: str | None = ...,
        color: int | None = ...,
        filter: str | None = ...,
        sdn_addr_type: Literal["private", "public", "all"] | None = ...,
        node_ip_only: Literal["enable", "disable"] | None = ...,
        obj_id: str | None = ...,
        list: str | list[str] | list[AddressListItem] | None = ...,
        tagging: str | list[str] | list[AddressTaggingItem] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        passive_fqdn_learning: Literal["disable", "enable"] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddressObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        subnet: str | None = ...,
        type: Literal["ipmask", "iprange", "fqdn", "geography", "wildcard", "dynamic", "interface-subnet", "mac", "route-tag"] | None = ...,
        route_tag: int | None = ...,
        sub_type: Literal["sdn", "clearpass-spt", "fsso", "rsso", "ems-tag", "fortivoice-tag", "fortinac-tag", "swc-tag", "device-identification", "external-resource", "obsolete"] | None = ...,
        clearpass_spt: Literal["unknown", "healthy", "quarantine", "checkup", "transient", "infected"] | None = ...,
        macaddr: str | list[str] | list[AddressMacaddrItem] | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        fqdn: str | None = ...,
        country: str | None = ...,
        wildcard_fqdn: str | None = ...,
        cache_ttl: int | None = ...,
        wildcard: str | None = ...,
        sdn: str | None = ...,
        fsso_group: str | list[str] | list[AddressFssogroupItem] | None = ...,
        sso_attribute_value: str | list[str] | list[AddressSsoattributevalueItem] | None = ...,
        interface: str | None = ...,
        tenant: str | None = ...,
        organization: str | None = ...,
        epg_name: str | None = ...,
        subnet_name: str | None = ...,
        sdn_tag: str | None = ...,
        policy_group: str | None = ...,
        obj_tag: str | None = ...,
        obj_type: Literal["ip", "mac"] | None = ...,
        tag_detection_level: str | None = ...,
        tag_type: str | None = ...,
        hw_vendor: str | None = ...,
        hw_model: str | None = ...,
        os: str | None = ...,
        sw_version: str | None = ...,
        comment: str | None = ...,
        associated_interface: str | None = ...,
        color: int | None = ...,
        filter: str | None = ...,
        sdn_addr_type: Literal["private", "public", "all"] | None = ...,
        node_ip_only: Literal["enable", "disable"] | None = ...,
        obj_id: str | None = ...,
        list: str | list[str] | list[AddressListItem] | None = ...,
        tagging: str | list[str] | list[AddressTaggingItem] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        passive_fqdn_learning: Literal["disable", "enable"] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AddressObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        subnet: str | None = ...,
        type: Literal["ipmask", "iprange", "fqdn", "geography", "wildcard", "dynamic", "interface-subnet", "mac", "route-tag"] | None = ...,
        route_tag: int | None = ...,
        sub_type: Literal["sdn", "clearpass-spt", "fsso", "rsso", "ems-tag", "fortivoice-tag", "fortinac-tag", "swc-tag", "device-identification", "external-resource", "obsolete"] | None = ...,
        clearpass_spt: Literal["unknown", "healthy", "quarantine", "checkup", "transient", "infected"] | None = ...,
        macaddr: str | list[str] | list[AddressMacaddrItem] | None = ...,
        start_ip: str | None = ...,
        end_ip: str | None = ...,
        fqdn: str | None = ...,
        country: str | None = ...,
        wildcard_fqdn: str | None = ...,
        cache_ttl: int | None = ...,
        wildcard: str | None = ...,
        sdn: str | None = ...,
        fsso_group: str | list[str] | list[AddressFssogroupItem] | None = ...,
        sso_attribute_value: str | list[str] | list[AddressSsoattributevalueItem] | None = ...,
        interface: str | None = ...,
        tenant: str | None = ...,
        organization: str | None = ...,
        epg_name: str | None = ...,
        subnet_name: str | None = ...,
        sdn_tag: str | None = ...,
        policy_group: str | None = ...,
        obj_tag: str | None = ...,
        obj_type: Literal["ip", "mac"] | None = ...,
        tag_detection_level: str | None = ...,
        tag_type: str | None = ...,
        hw_vendor: str | None = ...,
        hw_model: str | None = ...,
        os: str | None = ...,
        sw_version: str | None = ...,
        comment: str | None = ...,
        associated_interface: str | None = ...,
        color: int | None = ...,
        filter: str | None = ...,
        sdn_addr_type: Literal["private", "public", "all"] | None = ...,
        node_ip_only: Literal["enable", "disable"] | None = ...,
        obj_id: str | None = ...,
        list: str | list[str] | list[AddressListItem] | None = ...,
        tagging: str | list[str] | list[AddressTaggingItem] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
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
    "Address",
    "AddressPayload",
    "AddressResponse",
    "AddressObject",
]