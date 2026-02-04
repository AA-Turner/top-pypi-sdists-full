""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/ttl_policy
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

class TtlPolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class TtlPolicyServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class TtlPolicyPayload(TypedDict, total=False):
    """Payload type for TtlPolicy operations."""
    id: int
    status: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    srcintf: str
    srcaddr: str | list[str] | list[TtlPolicySrcaddrItem]
    service: str | list[str] | list[TtlPolicyServiceItem]
    schedule: str
    ttl: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class TtlPolicyResponse(TypedDict, total=False):
    """Response type for TtlPolicy - use with .dict property for typed dict access."""
    id: int
    status: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    srcintf: str
    srcaddr: list[TtlPolicySrcaddrItem]
    service: list[TtlPolicyServiceItem]
    schedule: str
    ttl: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class TtlPolicySrcaddrItemObject(FortiObject[TtlPolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class TtlPolicyServiceItemObject(FortiObject[TtlPolicyServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class TtlPolicyObject(FortiObject):
    """Typed FortiObject for TtlPolicy with field access."""
    id: int
    status: Literal["enable", "disable"]
    action: Literal["accept", "deny"]
    srcintf: str
    srcaddr: FortiObjectList[TtlPolicySrcaddrItemObject]
    service: FortiObjectList[TtlPolicyServiceItemObject]
    schedule: str
    ttl: str


# ================================================================
# Main Endpoint Class
# ================================================================

class TtlPolicy:
    """
    
    Endpoint: firewall/ttl_policy
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> TtlPolicyObject: ...
    
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
    ) -> FortiObjectList[TtlPolicyObject]: ...
    
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
        payload_dict: TtlPolicyPayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        srcintf: str | None = ...,
        srcaddr: str | list[str] | list[TtlPolicySrcaddrItem] | None = ...,
        service: str | list[str] | list[TtlPolicyServiceItem] | None = ...,
        schedule: str | None = ...,
        ttl: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TtlPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: TtlPolicyPayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        srcintf: str | None = ...,
        srcaddr: str | list[str] | list[TtlPolicySrcaddrItem] | None = ...,
        service: str | list[str] | list[TtlPolicyServiceItem] | None = ...,
        schedule: str | None = ...,
        ttl: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TtlPolicyObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: TtlPolicyPayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        action: Literal["accept", "deny"] | None = ...,
        srcintf: str | None = ...,
        srcaddr: str | list[str] | list[TtlPolicySrcaddrItem] | None = ...,
        service: str | list[str] | list[TtlPolicyServiceItem] | None = ...,
        schedule: str | None = ...,
        ttl: str | None = ...,
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
    "TtlPolicy",
    "TtlPolicyPayload",
    "TtlPolicyResponse",
    "TtlPolicyObject",
]