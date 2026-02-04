""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: web_proxy/forward_server_group
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

class ForwardServerGroupServerlistItem(TypedDict, total=False):
    """Nested item for server-list field."""
    name: str
    weight: int


class ForwardServerGroupPayload(TypedDict, total=False):
    """Payload type for ForwardServerGroup operations."""
    name: str
    affinity: Literal["enable", "disable"]
    ldb_method: Literal["weighted", "least-session", "active-passive"]
    group_down_option: Literal["block", "pass"]
    server_list: str | list[str] | list[ForwardServerGroupServerlistItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ForwardServerGroupResponse(TypedDict, total=False):
    """Response type for ForwardServerGroup - use with .dict property for typed dict access."""
    name: str
    affinity: Literal["enable", "disable"]
    ldb_method: Literal["weighted", "least-session", "active-passive"]
    group_down_option: Literal["block", "pass"]
    server_list: list[ForwardServerGroupServerlistItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ForwardServerGroupServerlistItemObject(FortiObject[ForwardServerGroupServerlistItem]):
    """Typed object for server-list table items with attribute access."""
    name: str
    weight: int


class ForwardServerGroupObject(FortiObject):
    """Typed FortiObject for ForwardServerGroup with field access."""
    name: str
    affinity: Literal["enable", "disable"]
    ldb_method: Literal["weighted", "least-session", "active-passive"]
    group_down_option: Literal["block", "pass"]
    server_list: FortiObjectList[ForwardServerGroupServerlistItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ForwardServerGroup:
    """
    
    Endpoint: web_proxy/forward_server_group
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
    ) -> ForwardServerGroupObject: ...
    
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
    ) -> FortiObjectList[ForwardServerGroupObject]: ...
    
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
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[ForwardServerGroupServerlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ForwardServerGroupObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[ForwardServerGroupServerlistItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ForwardServerGroupObject: ...

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
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[ForwardServerGroupServerlistItem] | None = ...,
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
    "ForwardServerGroup",
    "ForwardServerGroupPayload",
    "ForwardServerGroupResponse",
    "ForwardServerGroupObject",
]