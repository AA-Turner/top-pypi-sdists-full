""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/identity_based_route
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

class IdentityBasedRouteRuleGroupsItem(TypedDict, total=False):
    """Nested item for rule.groups field."""
    name: str


class IdentityBasedRouteRuleItem(TypedDict, total=False):
    """Nested item for rule field."""
    id: int
    gateway: str
    device: str
    groups: str | list[str] | list[IdentityBasedRouteRuleGroupsItem]


class IdentityBasedRoutePayload(TypedDict, total=False):
    """Payload type for IdentityBasedRoute operations."""
    name: str
    comments: str
    rule: str | list[str] | list[IdentityBasedRouteRuleItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IdentityBasedRouteResponse(TypedDict, total=False):
    """Response type for IdentityBasedRoute - use with .dict property for typed dict access."""
    name: str
    comments: str
    rule: list[IdentityBasedRouteRuleItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IdentityBasedRouteRuleGroupsItemObject(FortiObject[IdentityBasedRouteRuleGroupsItem]):
    """Typed object for rule.groups table items with attribute access."""
    name: str


class IdentityBasedRouteRuleItemObject(FortiObject[IdentityBasedRouteRuleItem]):
    """Typed object for rule table items with attribute access."""
    id: int
    gateway: str
    device: str
    groups: FortiObjectList[IdentityBasedRouteRuleGroupsItemObject]


class IdentityBasedRouteObject(FortiObject):
    """Typed FortiObject for IdentityBasedRoute with field access."""
    name: str
    comments: str
    rule: FortiObjectList[IdentityBasedRouteRuleItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class IdentityBasedRoute:
    """
    
    Endpoint: firewall/identity_based_route
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
    ) -> IdentityBasedRouteObject: ...
    
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
    ) -> FortiObjectList[IdentityBasedRouteObject]: ...
    
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
        payload_dict: IdentityBasedRoutePayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[IdentityBasedRouteRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IdentityBasedRouteObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IdentityBasedRoutePayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[IdentityBasedRouteRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IdentityBasedRouteObject: ...

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
        payload_dict: IdentityBasedRoutePayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        rule: str | list[str] | list[IdentityBasedRouteRuleItem] | None = ...,
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
    "IdentityBasedRoute",
    "IdentityBasedRoutePayload",
    "IdentityBasedRouteResponse",
    "IdentityBasedRouteObject",
]