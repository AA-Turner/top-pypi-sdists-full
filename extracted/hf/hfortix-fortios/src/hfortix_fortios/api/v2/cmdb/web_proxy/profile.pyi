""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: web_proxy/profile
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

class ProfileHeadersDstaddrItem(TypedDict, total=False):
    """Nested item for headers.dstaddr field."""
    name: str


class ProfileHeadersDstaddr6Item(TypedDict, total=False):
    """Nested item for headers.dstaddr6 field."""
    name: str


class ProfileHeadersItem(TypedDict, total=False):
    """Nested item for headers field."""
    id: int
    name: str
    dstaddr: str | list[str] | list[ProfileHeadersDstaddrItem]
    dstaddr6: str | list[str] | list[ProfileHeadersDstaddr6Item]
    action: Literal["add-to-request", "add-to-response", "remove-from-request", "remove-from-response", "monitor-request", "monitor-response"]
    content: str
    base64_encoding: Literal["disable", "enable"]
    add_option: Literal["append", "new-on-not-found", "new", "replace", "replace-when-match"]
    protocol: Literal["https", "http"]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    header_client_ip: Literal["pass", "add", "remove"]
    header_via_request: Literal["pass", "add", "remove"]
    header_via_response: Literal["pass", "add", "remove"]
    header_client_cert: Literal["pass", "add", "remove"]
    header_x_forwarded_for: Literal["pass", "add", "remove"]
    header_x_forwarded_client_cert: Literal["pass", "add", "remove"]
    header_front_end_https: Literal["pass", "add", "remove"]
    header_x_authenticated_user: Literal["pass", "add", "remove"]
    header_x_authenticated_groups: Literal["pass", "add", "remove"]
    strip_encoding: Literal["enable", "disable"]
    log_header_change: Literal["enable", "disable"]
    headers: str | list[str] | list[ProfileHeadersItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    header_client_ip: Literal["pass", "add", "remove"]
    header_via_request: Literal["pass", "add", "remove"]
    header_via_response: Literal["pass", "add", "remove"]
    header_client_cert: Literal["pass", "add", "remove"]
    header_x_forwarded_for: Literal["pass", "add", "remove"]
    header_x_forwarded_client_cert: Literal["pass", "add", "remove"]
    header_front_end_https: Literal["pass", "add", "remove"]
    header_x_authenticated_user: Literal["pass", "add", "remove"]
    header_x_authenticated_groups: Literal["pass", "add", "remove"]
    strip_encoding: Literal["enable", "disable"]
    log_header_change: Literal["enable", "disable"]
    headers: list[ProfileHeadersItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileHeadersDstaddrItemObject(FortiObject[ProfileHeadersDstaddrItem]):
    """Typed object for headers.dstaddr table items with attribute access."""
    name: str


class ProfileHeadersDstaddr6ItemObject(FortiObject[ProfileHeadersDstaddr6Item]):
    """Typed object for headers.dstaddr6 table items with attribute access."""
    name: str


class ProfileHeadersItemObject(FortiObject[ProfileHeadersItem]):
    """Typed object for headers table items with attribute access."""
    id: int
    name: str
    dstaddr: FortiObjectList[ProfileHeadersDstaddrItemObject]
    dstaddr6: FortiObjectList[ProfileHeadersDstaddr6ItemObject]
    action: Literal["add-to-request", "add-to-response", "remove-from-request", "remove-from-response", "monitor-request", "monitor-response"]
    content: str
    base64_encoding: Literal["disable", "enable"]
    add_option: Literal["append", "new-on-not-found", "new", "replace", "replace-when-match"]
    protocol: Literal["https", "http"]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    header_client_ip: Literal["pass", "add", "remove"]
    header_via_request: Literal["pass", "add", "remove"]
    header_via_response: Literal["pass", "add", "remove"]
    header_client_cert: Literal["pass", "add", "remove"]
    header_x_forwarded_for: Literal["pass", "add", "remove"]
    header_x_forwarded_client_cert: Literal["pass", "add", "remove"]
    header_front_end_https: Literal["pass", "add", "remove"]
    header_x_authenticated_user: Literal["pass", "add", "remove"]
    header_x_authenticated_groups: Literal["pass", "add", "remove"]
    strip_encoding: Literal["enable", "disable"]
    log_header_change: Literal["enable", "disable"]
    headers: FortiObjectList[ProfileHeadersItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: web_proxy/profile
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
    ) -> ProfileObject: ...
    
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
    ) -> FortiObjectList[ProfileObject]: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[ProfileHeadersItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[ProfileHeadersItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[ProfileHeadersItem] | None = ...,
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
    "Profile",
    "ProfilePayload",
    "ProfileResponse",
    "ProfileObject",
]