""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/vlan_policy
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

class VlanPolicyAllowedvlansItem(TypedDict, total=False):
    """Nested item for allowed-vlans field."""
    vlan_name: str


class VlanPolicyUntaggedvlansItem(TypedDict, total=False):
    """Nested item for untagged-vlans field."""
    vlan_name: str


class VlanPolicyPayload(TypedDict, total=False):
    """Payload type for VlanPolicy operations."""
    name: str
    description: str
    fortilink: str
    vlan: str
    allowed_vlans: str | list[str] | list[VlanPolicyAllowedvlansItem]
    untagged_vlans: str | list[str] | list[VlanPolicyUntaggedvlansItem]
    allowed_vlans_all: Literal["enable", "disable"]
    discard_mode: Literal["none", "all-untagged", "all-tagged"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VlanPolicyResponse(TypedDict, total=False):
    """Response type for VlanPolicy - use with .dict property for typed dict access."""
    name: str
    description: str
    fortilink: str
    vlan: str
    allowed_vlans: list[VlanPolicyAllowedvlansItem]
    untagged_vlans: list[VlanPolicyUntaggedvlansItem]
    allowed_vlans_all: Literal["enable", "disable"]
    discard_mode: Literal["none", "all-untagged", "all-tagged"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VlanPolicyAllowedvlansItemObject(FortiObject[VlanPolicyAllowedvlansItem]):
    """Typed object for allowed-vlans table items with attribute access."""
    vlan_name: str


class VlanPolicyUntaggedvlansItemObject(FortiObject[VlanPolicyUntaggedvlansItem]):
    """Typed object for untagged-vlans table items with attribute access."""
    vlan_name: str


class VlanPolicyObject(FortiObject):
    """Typed FortiObject for VlanPolicy with field access."""
    name: str
    description: str
    fortilink: str
    vlan: str
    allowed_vlans: FortiObjectList[VlanPolicyAllowedvlansItemObject]
    untagged_vlans: FortiObjectList[VlanPolicyUntaggedvlansItemObject]
    allowed_vlans_all: Literal["enable", "disable"]
    discard_mode: Literal["none", "all-untagged", "all-tagged"]


# ================================================================
# Main Endpoint Class
# ================================================================

class VlanPolicy:
    """
    
    Endpoint: switch_controller/vlan_policy
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
    ) -> VlanPolicyObject: ...
    
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
    ) -> FortiObjectList[VlanPolicyObject]: ...
    
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
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[VlanPolicyAllowedvlansItem] | None = ...,
        untagged_vlans: str | list[str] | list[VlanPolicyUntaggedvlansItem] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VlanPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[VlanPolicyAllowedvlansItem] | None = ...,
        untagged_vlans: str | list[str] | list[VlanPolicyUntaggedvlansItem] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VlanPolicyObject: ...

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
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[VlanPolicyAllowedvlansItem] | None = ...,
        untagged_vlans: str | list[str] | list[VlanPolicyUntaggedvlansItem] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
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
    "VlanPolicy",
    "VlanPolicyPayload",
    "VlanPolicyResponse",
    "VlanPolicyObject",
]