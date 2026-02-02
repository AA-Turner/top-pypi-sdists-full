""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/security_exempt_list
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

class SecurityExemptListRuleSrcaddrItem(TypedDict, total=False):
    """Nested item for rule.srcaddr field."""
    name: str


class SecurityExemptListRuleDstaddrItem(TypedDict, total=False):
    """Nested item for rule.dstaddr field."""
    name: str


class SecurityExemptListRuleServiceItem(TypedDict, total=False):
    """Nested item for rule.service field."""
    name: str


class SecurityExemptListRuleItem(TypedDict, total=False):
    """Nested item for rule field."""
    id: int
    srcaddr: str | list[str] | list[SecurityExemptListRuleSrcaddrItem]
    dstaddr: str | list[str] | list[SecurityExemptListRuleDstaddrItem]
    service: str | list[str] | list[SecurityExemptListRuleServiceItem]


class SecurityExemptListPayload(TypedDict, total=False):
    """Payload type for SecurityExemptList operations."""
    name: str
    description: str
    rule: str | list[str] | list[SecurityExemptListRuleItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SecurityExemptListResponse(TypedDict, total=False):
    """Response type for SecurityExemptList - use with .dict property for typed dict access."""
    name: str
    description: str
    rule: list[SecurityExemptListRuleItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SecurityExemptListRuleSrcaddrItemObject(FortiObject[SecurityExemptListRuleSrcaddrItem]):
    """Typed object for rule.srcaddr table items with attribute access."""
    name: str


class SecurityExemptListRuleDstaddrItemObject(FortiObject[SecurityExemptListRuleDstaddrItem]):
    """Typed object for rule.dstaddr table items with attribute access."""
    name: str


class SecurityExemptListRuleServiceItemObject(FortiObject[SecurityExemptListRuleServiceItem]):
    """Typed object for rule.service table items with attribute access."""
    name: str


class SecurityExemptListRuleItemObject(FortiObject[SecurityExemptListRuleItem]):
    """Typed object for rule table items with attribute access."""
    id: int
    srcaddr: FortiObjectList[SecurityExemptListRuleSrcaddrItemObject]
    dstaddr: FortiObjectList[SecurityExemptListRuleDstaddrItemObject]
    service: FortiObjectList[SecurityExemptListRuleServiceItemObject]


class SecurityExemptListObject(FortiObject):
    """Typed FortiObject for SecurityExemptList with field access."""
    name: str
    description: str
    rule: FortiObjectList[SecurityExemptListRuleItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class SecurityExemptList:
    """
    
    Endpoint: user/security_exempt_list
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
    ) -> SecurityExemptListObject: ...
    
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
    ) -> FortiObjectList[SecurityExemptListObject]: ...
    
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
        payload_dict: SecurityExemptListPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        rule: str | list[str] | list[SecurityExemptListRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SecurityExemptListObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SecurityExemptListPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        rule: str | list[str] | list[SecurityExemptListRuleItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SecurityExemptListObject: ...

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
        payload_dict: SecurityExemptListPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        rule: str | list[str] | list[SecurityExemptListRuleItem] | None = ...,
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
    "SecurityExemptList",
    "SecurityExemptListPayload",
    "SecurityExemptListResponse",
    "SecurityExemptListObject",
]