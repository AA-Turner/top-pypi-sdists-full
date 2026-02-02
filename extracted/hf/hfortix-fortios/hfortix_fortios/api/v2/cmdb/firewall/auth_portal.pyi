""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/auth_portal
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


# ================================================================
# TypedDict Payloads
# ================================================================

class AuthPortalGroupsItem(TypedDict, total=False):
    """Nested item for groups field."""
    name: str


class AuthPortalPayload(TypedDict, total=False):
    """Payload type for AuthPortal operations."""
    groups: str | list[str] | list[AuthPortalGroupsItem]
    portal_addr: str
    portal_addr6: str
    identity_based_route: str
    proxy_auth: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AuthPortalResponse(TypedDict, total=False):
    """Response type for AuthPortal - use with .dict property for typed dict access."""
    groups: list[AuthPortalGroupsItem]
    portal_addr: str
    portal_addr6: str
    identity_based_route: str
    proxy_auth: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AuthPortalGroupsItemObject(FortiObject[AuthPortalGroupsItem]):
    """Typed object for groups table items with attribute access."""
    name: str


class AuthPortalObject(FortiObject):
    """Typed FortiObject for AuthPortal with field access."""
    groups: FortiObjectList[AuthPortalGroupsItemObject]
    portal_addr: str
    portal_addr6: str
    identity_based_route: str
    proxy_auth: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class AuthPortal:
    """
    
    Endpoint: firewall/auth_portal
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
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
    ) -> AuthPortalObject: ...
    
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
        payload_dict: AuthPortalPayload | None = ...,
        groups: str | list[str] | list[AuthPortalGroupsItem] | None = ...,
        portal_addr: str | None = ...,
        portal_addr6: str | None = ...,
        identity_based_route: str | None = ...,
        proxy_auth: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AuthPortalObject: ...


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
        payload_dict: AuthPortalPayload | None = ...,
        groups: str | list[str] | list[AuthPortalGroupsItem] | None = ...,
        portal_addr: str | None = ...,
        portal_addr6: str | None = ...,
        identity_based_route: str | None = ...,
        proxy_auth: Literal["enable", "disable"] | None = ...,
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
    "AuthPortal",
    "AuthPortalPayload",
    "AuthPortalResponse",
    "AuthPortalObject",
]