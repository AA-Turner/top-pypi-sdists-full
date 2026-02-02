""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: virtual_patch/profile
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

class ProfileExemptionRuleItem(TypedDict, total=False):
    """Nested item for exemption.rule field."""
    id: int


class ProfileExemptionDeviceItem(TypedDict, total=False):
    """Nested item for exemption.device field."""
    mac: str


class ProfileExemptionItem(TypedDict, total=False):
    """Nested item for exemption field."""
    id: int
    status: Literal["enable", "disable"]
    rule: str | list[str] | list[ProfileExemptionRuleItem]
    device: str | list[str] | list[ProfileExemptionDeviceItem]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    comment: str
    severity: str | list[str]
    action: Literal["pass", "block"]
    log: Literal["enable", "disable"]
    exemption: str | list[str] | list[ProfileExemptionItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    comment: str
    severity: str
    action: Literal["pass", "block"]
    log: Literal["enable", "disable"]
    exemption: list[ProfileExemptionItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileExemptionRuleItemObject(FortiObject[ProfileExemptionRuleItem]):
    """Typed object for exemption.rule table items with attribute access."""
    id: int


class ProfileExemptionDeviceItemObject(FortiObject[ProfileExemptionDeviceItem]):
    """Typed object for exemption.device table items with attribute access."""
    mac: str


class ProfileExemptionItemObject(FortiObject[ProfileExemptionItem]):
    """Typed object for exemption table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    rule: FortiObjectList[ProfileExemptionRuleItemObject]
    device: FortiObjectList[ProfileExemptionDeviceItemObject]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    comment: str
    severity: str
    action: Literal["pass", "block"]
    log: Literal["enable", "disable"]
    exemption: FortiObjectList[ProfileExemptionItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: virtual_patch/profile
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
        comment: str | None = ...,
        severity: str | list[str] | None = ...,
        action: Literal["pass", "block"] | None = ...,
        log: Literal["enable", "disable"] | None = ...,
        exemption: str | list[str] | list[ProfileExemptionItem] | None = ...,
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
        comment: str | None = ...,
        severity: str | list[str] | None = ...,
        action: Literal["pass", "block"] | None = ...,
        log: Literal["enable", "disable"] | None = ...,
        exemption: str | list[str] | list[ProfileExemptionItem] | None = ...,
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
        comment: str | None = ...,
        severity: Literal["info", "low", "medium", "high", "critical"] | list[str] | None = ...,
        action: Literal["pass", "block"] | None = ...,
        log: Literal["enable", "disable"] | None = ...,
        exemption: str | list[str] | list[ProfileExemptionItem] | None = ...,
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