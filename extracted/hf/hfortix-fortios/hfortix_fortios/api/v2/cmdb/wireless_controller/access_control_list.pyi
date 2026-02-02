""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/access_control_list
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

class AccessControlListLayer3ipv4rulesItem(TypedDict, total=False):
    """Nested item for layer3-ipv4-rules field."""
    rule_id: int
    comment: str
    srcaddr: str
    srcport: int
    dstaddr: str
    dstport: int
    protocol: int
    action: Literal["allow", "deny"]


class AccessControlListLayer3ipv6rulesItem(TypedDict, total=False):
    """Nested item for layer3-ipv6-rules field."""
    rule_id: int
    comment: str
    srcaddr: str
    srcport: int
    dstaddr: str
    dstport: int
    protocol: int
    action: Literal["allow", "deny"]


class AccessControlListPayload(TypedDict, total=False):
    """Payload type for AccessControlList operations."""
    name: str
    comment: str
    layer3_ipv4_rules: str | list[str] | list[AccessControlListLayer3ipv4rulesItem]
    layer3_ipv6_rules: str | list[str] | list[AccessControlListLayer3ipv6rulesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AccessControlListResponse(TypedDict, total=False):
    """Response type for AccessControlList - use with .dict property for typed dict access."""
    name: str
    comment: str
    layer3_ipv4_rules: list[AccessControlListLayer3ipv4rulesItem]
    layer3_ipv6_rules: list[AccessControlListLayer3ipv6rulesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AccessControlListLayer3ipv4rulesItemObject(FortiObject[AccessControlListLayer3ipv4rulesItem]):
    """Typed object for layer3-ipv4-rules table items with attribute access."""
    rule_id: int
    comment: str
    srcaddr: str
    srcport: int
    dstaddr: str
    dstport: int
    protocol: int
    action: Literal["allow", "deny"]


class AccessControlListLayer3ipv6rulesItemObject(FortiObject[AccessControlListLayer3ipv6rulesItem]):
    """Typed object for layer3-ipv6-rules table items with attribute access."""
    rule_id: int
    comment: str
    srcaddr: str
    srcport: int
    dstaddr: str
    dstport: int
    protocol: int
    action: Literal["allow", "deny"]


class AccessControlListObject(FortiObject):
    """Typed FortiObject for AccessControlList with field access."""
    name: str
    comment: str
    layer3_ipv4_rules: FortiObjectList[AccessControlListLayer3ipv4rulesItemObject]
    layer3_ipv6_rules: FortiObjectList[AccessControlListLayer3ipv6rulesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class AccessControlList:
    """
    
    Endpoint: wireless_controller/access_control_list
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
    ) -> AccessControlListObject: ...
    
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
    ) -> FortiObjectList[AccessControlListObject]: ...
    
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
        payload_dict: AccessControlListPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        layer3_ipv4_rules: str | list[str] | list[AccessControlListLayer3ipv4rulesItem] | None = ...,
        layer3_ipv6_rules: str | list[str] | list[AccessControlListLayer3ipv6rulesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessControlListObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AccessControlListPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        layer3_ipv4_rules: str | list[str] | list[AccessControlListLayer3ipv4rulesItem] | None = ...,
        layer3_ipv6_rules: str | list[str] | list[AccessControlListLayer3ipv6rulesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AccessControlListObject: ...

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
        payload_dict: AccessControlListPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        layer3_ipv4_rules: str | list[str] | list[AccessControlListLayer3ipv4rulesItem] | None = ...,
        layer3_ipv6_rules: str | list[str] | list[AccessControlListLayer3ipv6rulesItem] | None = ...,
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
    "AccessControlList",
    "AccessControlListPayload",
    "AccessControlListResponse",
    "AccessControlListObject",
]