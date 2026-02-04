""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: authentication/rule
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

class RuleSrcintfItem(TypedDict, total=False):
    """Nested item for srcintf field."""
    name: str


class RuleSrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class RuleDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class RuleSrcaddr6Item(TypedDict, total=False):
    """Nested item for srcaddr6 field."""
    name: str


class RuleDstaddr6Item(TypedDict, total=False):
    """Nested item for dstaddr6 field."""
    name: str


class RulePayload(TypedDict, total=False):
    """Payload type for Rule operations."""
    name: str
    status: Literal["enable", "disable"]
    protocol: Literal["http", "ftp", "socks", "ssh", "ztna-portal"]
    srcintf: str | list[str] | list[RuleSrcintfItem]
    srcaddr: str | list[str] | list[RuleSrcaddrItem]
    dstaddr: str | list[str] | list[RuleDstaddrItem]
    srcaddr6: str | list[str] | list[RuleSrcaddr6Item]
    dstaddr6: str | list[str] | list[RuleDstaddr6Item]
    ip_based: Literal["enable", "disable"]
    active_auth_method: str
    sso_auth_method: str
    web_auth_cookie: Literal["enable", "disable"]
    cors_stateful: Literal["enable", "disable"]
    cors_depth: int
    cert_auth_cookie: Literal["enable", "disable"]
    transaction_based: Literal["enable", "disable"]
    web_portal: Literal["enable", "disable"]
    comments: str
    session_logout: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class RuleResponse(TypedDict, total=False):
    """Response type for Rule - use with .dict property for typed dict access."""
    name: str
    status: Literal["enable", "disable"]
    protocol: Literal["http", "ftp", "socks", "ssh", "ztna-portal"]
    srcintf: list[RuleSrcintfItem]
    srcaddr: list[RuleSrcaddrItem]
    dstaddr: list[RuleDstaddrItem]
    srcaddr6: list[RuleSrcaddr6Item]
    dstaddr6: list[RuleDstaddr6Item]
    ip_based: Literal["enable", "disable"]
    active_auth_method: str
    sso_auth_method: str
    web_auth_cookie: Literal["enable", "disable"]
    cors_stateful: Literal["enable", "disable"]
    cors_depth: int
    cert_auth_cookie: Literal["enable", "disable"]
    transaction_based: Literal["enable", "disable"]
    web_portal: Literal["enable", "disable"]
    comments: str
    session_logout: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class RuleSrcintfItemObject(FortiObject[RuleSrcintfItem]):
    """Typed object for srcintf table items with attribute access."""
    name: str


class RuleSrcaddrItemObject(FortiObject[RuleSrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class RuleDstaddrItemObject(FortiObject[RuleDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class RuleSrcaddr6ItemObject(FortiObject[RuleSrcaddr6Item]):
    """Typed object for srcaddr6 table items with attribute access."""
    name: str


class RuleDstaddr6ItemObject(FortiObject[RuleDstaddr6Item]):
    """Typed object for dstaddr6 table items with attribute access."""
    name: str


class RuleObject(FortiObject):
    """Typed FortiObject for Rule with field access."""
    name: str
    status: Literal["enable", "disable"]
    protocol: Literal["http", "ftp", "socks", "ssh", "ztna-portal"]
    srcintf: FortiObjectList[RuleSrcintfItemObject]
    srcaddr: FortiObjectList[RuleSrcaddrItemObject]
    dstaddr: FortiObjectList[RuleDstaddrItemObject]
    srcaddr6: FortiObjectList[RuleSrcaddr6ItemObject]
    dstaddr6: FortiObjectList[RuleDstaddr6ItemObject]
    ip_based: Literal["enable", "disable"]
    active_auth_method: str
    sso_auth_method: str
    web_auth_cookie: Literal["enable", "disable"]
    cors_stateful: Literal["enable", "disable"]
    cors_depth: int
    cert_auth_cookie: Literal["enable", "disable"]
    transaction_based: Literal["enable", "disable"]
    web_portal: Literal["enable", "disable"]
    comments: str
    session_logout: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Rule:
    """
    
    Endpoint: authentication/rule
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
    ) -> RuleObject: ...
    
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
    ) -> FortiObjectList[RuleObject]: ...
    
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
        payload_dict: RulePayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        protocol: Literal["http", "ftp", "socks", "ssh", "ztna-portal"] | None = ...,
        srcintf: str | list[str] | list[RuleSrcintfItem] | None = ...,
        srcaddr: str | list[str] | list[RuleSrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[RuleDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[RuleSrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[RuleDstaddr6Item] | None = ...,
        ip_based: Literal["enable", "disable"] | None = ...,
        active_auth_method: str | None = ...,
        sso_auth_method: str | None = ...,
        web_auth_cookie: Literal["enable", "disable"] | None = ...,
        cors_stateful: Literal["enable", "disable"] | None = ...,
        cors_depth: int | None = ...,
        cert_auth_cookie: Literal["enable", "disable"] | None = ...,
        transaction_based: Literal["enable", "disable"] | None = ...,
        web_portal: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        session_logout: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RuleObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: RulePayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        protocol: Literal["http", "ftp", "socks", "ssh", "ztna-portal"] | None = ...,
        srcintf: str | list[str] | list[RuleSrcintfItem] | None = ...,
        srcaddr: str | list[str] | list[RuleSrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[RuleDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[RuleSrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[RuleDstaddr6Item] | None = ...,
        ip_based: Literal["enable", "disable"] | None = ...,
        active_auth_method: str | None = ...,
        sso_auth_method: str | None = ...,
        web_auth_cookie: Literal["enable", "disable"] | None = ...,
        cors_stateful: Literal["enable", "disable"] | None = ...,
        cors_depth: int | None = ...,
        cert_auth_cookie: Literal["enable", "disable"] | None = ...,
        transaction_based: Literal["enable", "disable"] | None = ...,
        web_portal: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        session_logout: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> RuleObject: ...

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
        payload_dict: RulePayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        protocol: Literal["http", "ftp", "socks", "ssh", "ztna-portal"] | None = ...,
        srcintf: str | list[str] | list[RuleSrcintfItem] | None = ...,
        srcaddr: str | list[str] | list[RuleSrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[RuleDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[RuleSrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[RuleDstaddr6Item] | None = ...,
        ip_based: Literal["enable", "disable"] | None = ...,
        active_auth_method: str | None = ...,
        sso_auth_method: str | None = ...,
        web_auth_cookie: Literal["enable", "disable"] | None = ...,
        cors_stateful: Literal["enable", "disable"] | None = ...,
        cors_depth: int | None = ...,
        cert_auth_cookie: Literal["enable", "disable"] | None = ...,
        transaction_based: Literal["enable", "disable"] | None = ...,
        web_portal: Literal["enable", "disable"] | None = ...,
        comments: str | None = ...,
        session_logout: Literal["enable", "disable"] | None = ...,
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
    "Rule",
    "RulePayload",
    "RuleResponse",
    "RuleObject",
]