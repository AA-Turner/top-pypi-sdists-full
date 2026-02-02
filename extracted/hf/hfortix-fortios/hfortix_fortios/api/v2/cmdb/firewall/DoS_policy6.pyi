""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/DoS_policy6
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

class DosPolicy6SrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class DosPolicy6DstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class DosPolicy6ServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class DosPolicy6AnomalyItem(TypedDict, total=False):
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


class DosPolicy6Payload(TypedDict, total=False):
    """Payload type for DosPolicy6 operations."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    comments: str
    interface: str
    srcaddr: str | list[str] | list[DosPolicy6SrcaddrItem]
    dstaddr: str | list[str] | list[DosPolicy6DstaddrItem]
    service: str | list[str] | list[DosPolicy6ServiceItem]
    anomaly: str | list[str] | list[DosPolicy6AnomalyItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DosPolicy6Response(TypedDict, total=False):
    """Response type for DosPolicy6 - use with .dict property for typed dict access."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    comments: str
    interface: str
    srcaddr: list[DosPolicy6SrcaddrItem]
    dstaddr: list[DosPolicy6DstaddrItem]
    service: list[DosPolicy6ServiceItem]
    anomaly: list[DosPolicy6AnomalyItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DosPolicy6SrcaddrItemObject(FortiObject[DosPolicy6SrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class DosPolicy6DstaddrItemObject(FortiObject[DosPolicy6DstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class DosPolicy6ServiceItemObject(FortiObject[DosPolicy6ServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class DosPolicy6AnomalyItemObject(FortiObject[DosPolicy6AnomalyItem]):
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


class DosPolicy6Object(FortiObject):
    """Typed FortiObject for DosPolicy6 with field access."""
    policyid: int
    status: Literal["enable", "disable"]
    name: str
    comments: str
    interface: str
    srcaddr: FortiObjectList[DosPolicy6SrcaddrItemObject]
    dstaddr: FortiObjectList[DosPolicy6DstaddrItemObject]
    service: FortiObjectList[DosPolicy6ServiceItemObject]
    anomaly: FortiObjectList[DosPolicy6AnomalyItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class DosPolicy6:
    """
    
    Endpoint: firewall/DoS_policy6
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
    ) -> DosPolicy6Object: ...
    
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
    ) -> FortiObjectList[DosPolicy6Object]: ...
    
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
        payload_dict: DosPolicy6Payload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[DosPolicy6SrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[DosPolicy6DstaddrItem] | None = ...,
        service: str | list[str] | list[DosPolicy6ServiceItem] | None = ...,
        anomaly: str | list[str] | list[DosPolicy6AnomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DosPolicy6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DosPolicy6Payload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[DosPolicy6SrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[DosPolicy6DstaddrItem] | None = ...,
        service: str | list[str] | list[DosPolicy6ServiceItem] | None = ...,
        anomaly: str | list[str] | list[DosPolicy6AnomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DosPolicy6Object: ...

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
        payload_dict: DosPolicy6Payload | None = ...,
        policyid: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        interface: str | None = ...,
        srcaddr: str | list[str] | list[DosPolicy6SrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[DosPolicy6DstaddrItem] | None = ...,
        service: str | list[str] | list[DosPolicy6ServiceItem] | None = ...,
        anomaly: str | list[str] | list[DosPolicy6AnomalyItem] | None = ...,
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
    "DosPolicy6",
    "DosPolicy6Payload",
    "DosPolicy6Response",
    "DosPolicy6Object",
]