""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/dynamic_port_policy
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

class DynamicPortPolicyPolicyInterfacetagsItem(TypedDict, total=False):
    """Nested item for policy.interface-tags field."""
    tag_name: str


class DynamicPortPolicyPolicyItem(TypedDict, total=False):
    """Nested item for policy field."""
    name: str
    description: str
    status: Literal["enable", "disable"]
    category: Literal["device", "interface-tag"]
    match_type: Literal["dynamic", "override"]
    match_period: int
    match_remove: Literal["default", "link-down"]
    interface_tags: str | list[str] | list[DynamicPortPolicyPolicyInterfacetagsItem]
    mac: str
    hw_vendor: str
    type: str
    family: str
    host: str
    lldp_profile: str
    qos_policy: str
    x802_1x: str
    vlan_policy: str
    bounce_port_link: Literal["disable", "enable"]
    bounce_port_duration: int
    poe_reset: Literal["disable", "enable"]


class DynamicPortPolicyPayload(TypedDict, total=False):
    """Payload type for DynamicPortPolicy operations."""
    name: str
    description: str
    fortilink: str
    policy: str | list[str] | list[DynamicPortPolicyPolicyItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DynamicPortPolicyResponse(TypedDict, total=False):
    """Response type for DynamicPortPolicy - use with .dict property for typed dict access."""
    name: str
    description: str
    fortilink: str
    policy: list[DynamicPortPolicyPolicyItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DynamicPortPolicyPolicyInterfacetagsItemObject(FortiObject[DynamicPortPolicyPolicyInterfacetagsItem]):
    """Typed object for policy.interface-tags table items with attribute access."""
    tag_name: str


class DynamicPortPolicyPolicyItemObject(FortiObject[DynamicPortPolicyPolicyItem]):
    """Typed object for policy table items with attribute access."""
    name: str
    description: str
    status: Literal["enable", "disable"]
    category: Literal["device", "interface-tag"]
    match_type: Literal["dynamic", "override"]
    match_period: int
    match_remove: Literal["default", "link-down"]
    interface_tags: FortiObjectList[DynamicPortPolicyPolicyInterfacetagsItemObject]
    mac: str
    hw_vendor: str
    type: str
    family: str
    host: str
    lldp_profile: str
    qos_policy: str
    x802_1x: str
    vlan_policy: str
    bounce_port_link: Literal["disable", "enable"]
    bounce_port_duration: int
    poe_reset: Literal["disable", "enable"]


class DynamicPortPolicyObject(FortiObject):
    """Typed FortiObject for DynamicPortPolicy with field access."""
    name: str
    description: str
    fortilink: str
    policy: FortiObjectList[DynamicPortPolicyPolicyItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class DynamicPortPolicy:
    """
    
    Endpoint: switch_controller/dynamic_port_policy
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
    ) -> DynamicPortPolicyObject: ...
    
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
    ) -> FortiObjectList[DynamicPortPolicyObject]: ...
    
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
        payload_dict: DynamicPortPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        policy: str | list[str] | list[DynamicPortPolicyPolicyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DynamicPortPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DynamicPortPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        policy: str | list[str] | list[DynamicPortPolicyPolicyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DynamicPortPolicyObject: ...

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
        payload_dict: DynamicPortPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        policy: str | list[str] | list[DynamicPortPolicyPolicyItem] | None = ...,
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
    "DynamicPortPolicy",
    "DynamicPortPolicyPayload",
    "DynamicPortPolicyResponse",
    "DynamicPortPolicyObject",
]