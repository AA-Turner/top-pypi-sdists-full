""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_fortiguard
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

class InternetServiceFortiguardEntryPortrangeItem(TypedDict, total=False):
    """Nested item for entry.port-range field."""
    id: int
    start_port: int
    end_port: int


class InternetServiceFortiguardEntryDstItem(TypedDict, total=False):
    """Nested item for entry.dst field."""
    name: str


class InternetServiceFortiguardEntryDst6Item(TypedDict, total=False):
    """Nested item for entry.dst6 field."""
    name: str


class InternetServiceFortiguardEntryItem(TypedDict, total=False):
    """Nested item for entry field."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: str | list[str] | list[InternetServiceFortiguardEntryPortrangeItem]
    dst: str | list[str] | list[InternetServiceFortiguardEntryDstItem]
    dst6: str | list[str] | list[InternetServiceFortiguardEntryDst6Item]


class InternetServiceFortiguardPayload(TypedDict, total=False):
    """Payload type for InternetServiceFortiguard operations."""
    name: str
    comment: str
    entry: str | list[str] | list[InternetServiceFortiguardEntryItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InternetServiceFortiguardResponse(TypedDict, total=False):
    """Response type for InternetServiceFortiguard - use with .dict property for typed dict access."""
    name: str
    comment: str
    entry: list[InternetServiceFortiguardEntryItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InternetServiceFortiguardEntryPortrangeItemObject(FortiObject[InternetServiceFortiguardEntryPortrangeItem]):
    """Typed object for entry.port-range table items with attribute access."""
    id: int
    start_port: int
    end_port: int


class InternetServiceFortiguardEntryDstItemObject(FortiObject[InternetServiceFortiguardEntryDstItem]):
    """Typed object for entry.dst table items with attribute access."""
    name: str


class InternetServiceFortiguardEntryDst6ItemObject(FortiObject[InternetServiceFortiguardEntryDst6Item]):
    """Typed object for entry.dst6 table items with attribute access."""
    name: str


class InternetServiceFortiguardEntryItemObject(FortiObject[InternetServiceFortiguardEntryItem]):
    """Typed object for entry table items with attribute access."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: FortiObjectList[InternetServiceFortiguardEntryPortrangeItemObject]
    dst: FortiObjectList[InternetServiceFortiguardEntryDstItemObject]
    dst6: FortiObjectList[InternetServiceFortiguardEntryDst6ItemObject]


class InternetServiceFortiguardObject(FortiObject):
    """Typed FortiObject for InternetServiceFortiguard with field access."""
    name: str
    comment: str
    entry: FortiObjectList[InternetServiceFortiguardEntryItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceFortiguard:
    """
    
    Endpoint: firewall/internet_service_fortiguard
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceFortiguardObject: ...
    
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[InternetServiceFortiguardObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: InternetServiceFortiguardPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceFortiguardEntryItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceFortiguardObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceFortiguardPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceFortiguardEntryItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceFortiguardObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServiceFortiguardPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceFortiguardEntryItem] | None = ...,
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
    "InternetServiceFortiguard",
    "InternetServiceFortiguardPayload",
    "InternetServiceFortiguardResponse",
    "InternetServiceFortiguardObject",
]