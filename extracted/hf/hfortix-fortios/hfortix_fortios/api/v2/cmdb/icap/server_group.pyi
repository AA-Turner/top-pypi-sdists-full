""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: icap/server_group
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

class ServerGroupServerlistItem(TypedDict, total=False):
    """Nested item for server-list field."""
    name: str
    weight: int


class ServerGroupPayload(TypedDict, total=False):
    """Payload type for ServerGroup operations."""
    name: str
    ldb_method: Literal["weighted", "least-session", "active-passive"]
    server_list: str | list[str] | list[ServerGroupServerlistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ServerGroupResponse(TypedDict, total=False):
    """Response type for ServerGroup - use with .dict property for typed dict access."""
    name: str
    ldb_method: Literal["weighted", "least-session", "active-passive"]
    server_list: list[ServerGroupServerlistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ServerGroupServerlistItemObject(FortiObject[ServerGroupServerlistItem]):
    """Typed object for server-list table items with attribute access."""
    name: str
    weight: int


class ServerGroupObject(FortiObject):
    """Typed FortiObject for ServerGroup with field access."""
    name: str
    ldb_method: Literal["weighted", "least-session", "active-passive"]
    server_list: FortiObjectList[ServerGroupServerlistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ServerGroup:
    """
    
    Endpoint: icap/server_group
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
    ) -> ServerGroupObject: ...
    
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
    ) -> FortiObjectList[ServerGroupObject]: ...
    
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
        payload_dict: ServerGroupPayload | None = ...,
        name: str | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        server_list: str | list[str] | list[ServerGroupServerlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ServerGroupObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ServerGroupPayload | None = ...,
        name: str | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        server_list: str | list[str] | list[ServerGroupServerlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ServerGroupObject: ...

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
        payload_dict: ServerGroupPayload | None = ...,
        name: str | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        server_list: str | list[str] | list[ServerGroupServerlistItem] | None = ...,
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
    "ServerGroup",
    "ServerGroupPayload",
    "ServerGroupResponse",
    "ServerGroupObject",
]