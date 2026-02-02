""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/DoS_policy
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

class DosPolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class DosPolicyDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class DosPolicyServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class DosPolicyAnomalyItem(TypedDict, total=False):
    """Nested item for anomaly field."""
    name: str
    status: Literal["disable", "enable"]
    log: Literal["enable", "disable"]
    action: Literal["pass", "block"]
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]
    threshold: int
    threshold_default: int


class DosPolicyPayload(TypedDict, total=False):
    """Payload type for DosPolicy operations."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    comments: str
    interface: str
    srcaddr: str | list[str] | list[DosPolicySrcaddrItem]
    dstaddr: str | list[str] | list[DosPolicyDstaddrItem]
    service: str | list[str] | list[DosPolicyServiceItem]
    anomaly: str | list[str] | list[DosPolicyAnomalyItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DosPolicyResponse(TypedDict, total=False):
    """Response type for DosPolicy - use with .dict property for typed dict access."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    comments: str
    interface: str
    srcaddr: list[DosPolicySrcaddrItem]
    dstaddr: list[DosPolicyDstaddrItem]
    service: list[DosPolicyServiceItem]
    anomaly: list[DosPolicyAnomalyItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DosPolicySrcaddrItemObject(FortiObject[DosPolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class DosPolicyDstaddrItemObject(FortiObject[DosPolicyDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class DosPolicyServiceItemObject(FortiObject[DosPolicyServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class DosPolicyAnomalyItemObject(FortiObject[DosPolicyAnomalyItem]):
    """Typed object for anomaly table items with attribute access."""
    name: str
    status: Literal["disable", "enable"]
    log: Literal["enable", "disable"]
    action: Literal["pass", "block"]
    quarantine: Literal["none", "attacker"]
    quarantine_expiry: str
    quarantine_log: Literal["disable", "enable"]
    threshold: int
    threshold_default: int


class DosPolicyObject(FortiObject):
    """Typed FortiObject for DosPolicy with field access."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    comments: str
    interface: str
    srcaddr: FortiObjectList[DosPolicySrcaddrItemObject]
    dstaddr: FortiObjectList[DosPolicyDstaddrItemObject]
    service: FortiObjectList[DosPolicyServiceItemObject]
    anomaly: FortiObjectList[DosPolicyAnomalyItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class DosPolicy:
    """
    
    Endpoint: firewall/DoS_policy
    Category: cmdb
    MKey: policyid
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
        policyid: int,
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
    ) -> DosPolicyObject: ...
    
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
    ) -> FortiObjectList[DosPolicyObject]: ...
    
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
        payload_dict: DosPolicyPayload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[DosPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[DosPolicyDstaddrItem] | None = ...,
        service: str | list[str] | list[DosPolicyServiceItem] | None = ...,
        anomaly: str | list[str] | list[DosPolicyAnomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DosPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DosPolicyPayload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[DosPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[DosPolicyDstaddrItem] | None = ...,
        service: str | list[str] | list[DosPolicyServiceItem] | None = ...,
        anomaly: str | list[str] | list[DosPolicyAnomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DosPolicyObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        policyid: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        policyid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DosPolicyPayload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[DosPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[DosPolicyDstaddrItem] | None = ...,
        service: str | list[str] | list[DosPolicyServiceItem] | None = ...,
        anomaly: str | list[str] | list[DosPolicyAnomalyItem] | None = ...,
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
    "DosPolicy",
    "DosPolicyPayload",
    "DosPolicyResponse",
    "DosPolicyObject",
]