""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/api_user
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

class ApiUserVdomItem(TypedDict, total=False):
    """Nested item for vdom field."""
    name: str


class ApiUserTrusthostItem(TypedDict, total=False):
    """Nested item for trusthost field."""
    id: int
    type: Literal["ipv4-trusthost", "ipv6-trusthost"]
    ipv4_trusthost: str
    ipv6_trusthost: str


class ApiUserPayload(TypedDict, total=False):
    """Payload type for ApiUser operations."""
    name: str
    comments: str
    api_key: str
    accprofile: str
    vdom: str | list[str] | list[ApiUserVdomItem]
    schedule: str
    cors_allow_origin: str
    peer_auth: Literal["enable", "disable"]
    peer_group: str
    trusthost: str | list[str] | list[ApiUserTrusthostItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ApiUserResponse(TypedDict, total=False):
    """Response type for ApiUser - use with .dict property for typed dict access."""
    name: str
    comments: str
    api_key: str
    accprofile: str
    vdom: list[ApiUserVdomItem]
    schedule: str
    cors_allow_origin: str
    peer_auth: Literal["enable", "disable"]
    peer_group: str
    trusthost: list[ApiUserTrusthostItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ApiUserVdomItemObject(FortiObject[ApiUserVdomItem]):
    """Typed object for vdom table items with attribute access."""
    name: str


class ApiUserTrusthostItemObject(FortiObject[ApiUserTrusthostItem]):
    """Typed object for trusthost table items with attribute access."""
    id: int
    type: Literal["ipv4-trusthost", "ipv6-trusthost"]
    ipv4_trusthost: str
    ipv6_trusthost: str


class ApiUserObject(FortiObject):
    """Typed FortiObject for ApiUser with field access."""
    name: str
    comments: str
    api_key: str
    accprofile: str
    schedule: str
    cors_allow_origin: str
    peer_auth: Literal["enable", "disable"]
    peer_group: str
    trusthost: FortiObjectList[ApiUserTrusthostItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ApiUser:
    """
    
    Endpoint: system/api_user
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
    ) -> ApiUserObject: ...
    
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
    ) -> FortiObjectList[ApiUserObject]: ...
    
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
        payload_dict: ApiUserPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        api_key: str | None = ...,
        accprofile: str | None = ...,
        schedule: str | None = ...,
        cors_allow_origin: str | None = ...,
        peer_auth: Literal["enable", "disable"] | None = ...,
        peer_group: str | None = ...,
        trusthost: str | list[str] | list[ApiUserTrusthostItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ApiUserObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ApiUserPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        api_key: str | None = ...,
        accprofile: str | None = ...,
        schedule: str | None = ...,
        cors_allow_origin: str | None = ...,
        peer_auth: Literal["enable", "disable"] | None = ...,
        peer_group: str | None = ...,
        trusthost: str | list[str] | list[ApiUserTrusthostItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ApiUserObject: ...

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
        payload_dict: ApiUserPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        api_key: str | None = ...,
        accprofile: str | None = ...,
        schedule: str | None = ...,
        cors_allow_origin: str | None = ...,
        peer_auth: Literal["enable", "disable"] | None = ...,
        peer_group: str | None = ...,
        trusthost: str | list[str] | list[ApiUserTrusthostItem] | None = ...,
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
    "ApiUser",
    "ApiUserPayload",
    "ApiUserResponse",
    "ApiUserObject",
]