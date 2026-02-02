""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/qos_map
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

class QosMapDscpexceptItem(TypedDict, total=False):
    """Nested item for dscp-except field."""
    index: int
    dscp: int
    up: int


class QosMapDscprangeItem(TypedDict, total=False):
    """Nested item for dscp-range field."""
    index: int
    up: int
    low: int
    high: int


class QosMapPayload(TypedDict, total=False):
    """Payload type for QosMap operations."""
    name: str
    dscp_except: str | list[str] | list[QosMapDscpexceptItem]
    dscp_range: str | list[str] | list[QosMapDscprangeItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class QosMapResponse(TypedDict, total=False):
    """Response type for QosMap - use with .dict property for typed dict access."""
    name: str
    dscp_except: list[QosMapDscpexceptItem]
    dscp_range: list[QosMapDscprangeItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class QosMapDscpexceptItemObject(FortiObject[QosMapDscpexceptItem]):
    """Typed object for dscp-except table items with attribute access."""
    index: int
    dscp: int
    up: int


class QosMapDscprangeItemObject(FortiObject[QosMapDscprangeItem]):
    """Typed object for dscp-range table items with attribute access."""
    index: int
    up: int
    low: int
    high: int


class QosMapObject(FortiObject):
    """Typed FortiObject for QosMap with field access."""
    name: str
    dscp_except: FortiObjectList[QosMapDscpexceptItemObject]
    dscp_range: FortiObjectList[QosMapDscprangeItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class QosMap:
    """
    
    Endpoint: wireless_controller/hotspot20/qos_map
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
    ) -> QosMapObject: ...
    
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
    ) -> FortiObjectList[QosMapObject]: ...
    
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
        payload_dict: QosMapPayload | None = ...,
        name: str | None = ...,
        dscp_except: str | list[str] | list[QosMapDscpexceptItem] | None = ...,
        dscp_range: str | list[str] | list[QosMapDscprangeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QosMapObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: QosMapPayload | None = ...,
        name: str | None = ...,
        dscp_except: str | list[str] | list[QosMapDscpexceptItem] | None = ...,
        dscp_range: str | list[str] | list[QosMapDscprangeItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> QosMapObject: ...

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
        payload_dict: QosMapPayload | None = ...,
        name: str | None = ...,
        dscp_except: str | list[str] | list[QosMapDscpexceptItem] | None = ...,
        dscp_range: str | list[str] | list[QosMapDscprangeItem] | None = ...,
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
    "QosMap",
    "QosMapPayload",
    "QosMapResponse",
    "QosMapObject",
]