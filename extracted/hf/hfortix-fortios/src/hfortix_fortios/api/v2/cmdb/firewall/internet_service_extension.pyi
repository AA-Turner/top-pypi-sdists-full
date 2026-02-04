""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/internet_service_extension
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

class InternetServiceExtensionEntryPortrangeItem(TypedDict, total=False):
    """Nested item for entry.port-range field."""
    id: int
    start_port: int
    end_port: int


class InternetServiceExtensionEntryDstItem(TypedDict, total=False):
    """Nested item for entry.dst field."""
    name: str


class InternetServiceExtensionEntryDst6Item(TypedDict, total=False):
    """Nested item for entry.dst6 field."""
    name: str


class InternetServiceExtensionDisableentryPortrangeItem(TypedDict, total=False):
    """Nested item for disable-entry.port-range field."""
    id: int
    start_port: int
    end_port: int


class InternetServiceExtensionDisableentryIprangeItem(TypedDict, total=False):
    """Nested item for disable-entry.ip-range field."""
    id: int
    start_ip: str
    end_ip: str


class InternetServiceExtensionDisableentryIp6rangeItem(TypedDict, total=False):
    """Nested item for disable-entry.ip6-range field."""
    id: int
    start_ip6: str
    end_ip6: str


class InternetServiceExtensionEntryItem(TypedDict, total=False):
    """Nested item for entry field."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: str | list[str] | list[InternetServiceExtensionEntryPortrangeItem]
    dst: str | list[str] | list[InternetServiceExtensionEntryDstItem]
    dst6: str | list[str] | list[InternetServiceExtensionEntryDst6Item]


class InternetServiceExtensionDisableentryItem(TypedDict, total=False):
    """Nested item for disable-entry field."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: str | list[str] | list[InternetServiceExtensionDisableentryPortrangeItem]
    ip_range: str | list[str] | list[InternetServiceExtensionDisableentryIprangeItem]
    ip6_range: str | list[str] | list[InternetServiceExtensionDisableentryIp6rangeItem]


class InternetServiceExtensionPayload(TypedDict, total=False):
    """Payload type for InternetServiceExtension operations."""
    id: int
    comment: str
    entry: str | list[str] | list[InternetServiceExtensionEntryItem]
    disable_entry: str | list[str] | list[InternetServiceExtensionDisableentryItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InternetServiceExtensionResponse(TypedDict, total=False):
    """Response type for InternetServiceExtension - use with .dict property for typed dict access."""
    id: int
    comment: str
    entry: list[InternetServiceExtensionEntryItem]
    disable_entry: list[InternetServiceExtensionDisableentryItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InternetServiceExtensionEntryPortrangeItemObject(FortiObject[InternetServiceExtensionEntryPortrangeItem]):
    """Typed object for entry.port-range table items with attribute access."""
    id: int
    start_port: int
    end_port: int


class InternetServiceExtensionEntryDstItemObject(FortiObject[InternetServiceExtensionEntryDstItem]):
    """Typed object for entry.dst table items with attribute access."""
    name: str


class InternetServiceExtensionEntryDst6ItemObject(FortiObject[InternetServiceExtensionEntryDst6Item]):
    """Typed object for entry.dst6 table items with attribute access."""
    name: str


class InternetServiceExtensionDisableentryPortrangeItemObject(FortiObject[InternetServiceExtensionDisableentryPortrangeItem]):
    """Typed object for disable-entry.port-range table items with attribute access."""
    id: int
    start_port: int
    end_port: int


class InternetServiceExtensionDisableentryIprangeItemObject(FortiObject[InternetServiceExtensionDisableentryIprangeItem]):
    """Typed object for disable-entry.ip-range table items with attribute access."""
    id: int
    start_ip: str
    end_ip: str


class InternetServiceExtensionDisableentryIp6rangeItemObject(FortiObject[InternetServiceExtensionDisableentryIp6rangeItem]):
    """Typed object for disable-entry.ip6-range table items with attribute access."""
    id: int
    start_ip6: str
    end_ip6: str


class InternetServiceExtensionEntryItemObject(FortiObject[InternetServiceExtensionEntryItem]):
    """Typed object for entry table items with attribute access."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: FortiObjectList[InternetServiceExtensionEntryPortrangeItemObject]
    dst: FortiObjectList[InternetServiceExtensionEntryDstItemObject]
    dst6: FortiObjectList[InternetServiceExtensionEntryDst6ItemObject]


class InternetServiceExtensionDisableentryItemObject(FortiObject[InternetServiceExtensionDisableentryItem]):
    """Typed object for disable-entry table items with attribute access."""
    id: int
    addr_mode: Literal["ipv4", "ipv6"]
    protocol: int
    port_range: FortiObjectList[InternetServiceExtensionDisableentryPortrangeItemObject]
    ip_range: FortiObjectList[InternetServiceExtensionDisableentryIprangeItemObject]
    ip6_range: FortiObjectList[InternetServiceExtensionDisableentryIp6rangeItemObject]


class InternetServiceExtensionObject(FortiObject):
    """Typed FortiObject for InternetServiceExtension with field access."""
    id: int
    comment: str
    entry: FortiObjectList[InternetServiceExtensionEntryItemObject]
    disable_entry: FortiObjectList[InternetServiceExtensionDisableentryItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class InternetServiceExtension:
    """
    
    Endpoint: firewall/internet_service_extension
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
    ) -> InternetServiceExtensionObject: ...
    
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
    ) -> FortiObjectList[InternetServiceExtensionObject]: ...
    
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
        payload_dict: InternetServiceExtensionPayload | None = ...,
        id: int | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceExtensionEntryItem] | None = ...,
        disable_entry: str | list[str] | list[InternetServiceExtensionDisableentryItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceExtensionObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InternetServiceExtensionPayload | None = ...,
        id: int | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceExtensionEntryItem] | None = ...,
        disable_entry: str | list[str] | list[InternetServiceExtensionDisableentryItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InternetServiceExtensionObject: ...

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
        payload_dict: InternetServiceExtensionPayload | None = ...,
        id: int | None = ...,
        comment: str | None = ...,
        entry: str | list[str] | list[InternetServiceExtensionEntryItem] | None = ...,
        disable_entry: str | list[str] | list[InternetServiceExtensionDisableentryItem] | None = ...,
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
    "InternetServiceExtension",
    "InternetServiceExtensionPayload",
    "InternetServiceExtensionResponse",
    "InternetServiceExtensionObject",
]