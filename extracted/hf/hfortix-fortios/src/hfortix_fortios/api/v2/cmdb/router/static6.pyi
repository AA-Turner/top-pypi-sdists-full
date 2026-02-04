""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/static6
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

class Static6SdwanzoneItem(TypedDict, total=False):
    """Nested item for sdwan-zone field."""
    name: str


class Static6Payload(TypedDict, total=False):
    """Payload type for Static6 operations."""
    seq_num: int
    status: Literal["enable", "disable"]
    dst: str
    gateway: str
    device: str
    devindex: int
    distance: int
    weight: int
    priority: int
    comment: str
    blackhole: Literal["enable", "disable"]
    dynamic_gateway: Literal["enable", "disable"]
    sdwan_zone: str | list[str] | list[Static6SdwanzoneItem]
    dstaddr: str
    link_monitor_exempt: Literal["enable", "disable"]
    vrf: int
    bfd: Literal["enable", "disable"]
    tag: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Static6Response(TypedDict, total=False):
    """Response type for Static6 - use with .dict property for typed dict access."""
    seq_num: int
    status: Literal["enable", "disable"]
    dst: str
    gateway: str
    device: str
    devindex: int
    distance: int
    weight: int
    priority: int
    comment: str
    blackhole: Literal["enable", "disable"]
    dynamic_gateway: Literal["enable", "disable"]
    sdwan_zone: list[Static6SdwanzoneItem]
    dstaddr: str
    link_monitor_exempt: Literal["enable", "disable"]
    vrf: int
    bfd: Literal["enable", "disable"]
    tag: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Static6SdwanzoneItemObject(FortiObject[Static6SdwanzoneItem]):
    """Typed object for sdwan-zone table items with attribute access."""
    name: str


class Static6Object(FortiObject):
    """Typed FortiObject for Static6 with field access."""
    seq_num: int
    status: Literal["enable", "disable"]
    dst: str
    gateway: str
    device: str
    devindex: int
    distance: int
    weight: int
    priority: int
    comment: str
    blackhole: Literal["enable", "disable"]
    dynamic_gateway: Literal["enable", "disable"]
    sdwan_zone: FortiObjectList[Static6SdwanzoneItemObject]
    dstaddr: str
    link_monitor_exempt: Literal["enable", "disable"]
    vrf: int
    bfd: Literal["enable", "disable"]
    tag: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Static6:
    """
    
    Endpoint: router/static6
    Category: cmdb
    MKey: seq-num
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
        seq_num: int,
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
    ) -> Static6Object: ...
    
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
    ) -> FortiObjectList[Static6Object]: ...
    
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
        payload_dict: Static6Payload | None = ...,
        seq_num: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dst: str | None = ...,
        gateway: str | None = ...,
        device: str | None = ...,
        devindex: int | None = ...,
        distance: int | None = ...,
        weight: int | None = ...,
        priority: int | None = ...,
        comment: str | None = ...,
        blackhole: Literal["enable", "disable"] | None = ...,
        dynamic_gateway: Literal["enable", "disable"] | None = ...,
        sdwan_zone: str | list[str] | list[Static6SdwanzoneItem] | None = ...,
        dstaddr: str | None = ...,
        link_monitor_exempt: Literal["enable", "disable"] | None = ...,
        vrf: int | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        tag: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Static6Object: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Static6Payload | None = ...,
        seq_num: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dst: str | None = ...,
        gateway: str | None = ...,
        device: str | None = ...,
        devindex: int | None = ...,
        distance: int | None = ...,
        weight: int | None = ...,
        priority: int | None = ...,
        comment: str | None = ...,
        blackhole: Literal["enable", "disable"] | None = ...,
        dynamic_gateway: Literal["enable", "disable"] | None = ...,
        sdwan_zone: str | list[str] | list[Static6SdwanzoneItem] | None = ...,
        dstaddr: str | None = ...,
        link_monitor_exempt: Literal["enable", "disable"] | None = ...,
        vrf: int | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        tag: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Static6Object: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        seq_num: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        seq_num: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_seq_num: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        seq_num: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: Static6Payload | None = ...,
        seq_num: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dst: str | None = ...,
        gateway: str | None = ...,
        device: str | None = ...,
        devindex: int | None = ...,
        distance: int | None = ...,
        weight: int | None = ...,
        priority: int | None = ...,
        comment: str | None = ...,
        blackhole: Literal["enable", "disable"] | None = ...,
        dynamic_gateway: Literal["enable", "disable"] | None = ...,
        sdwan_zone: str | list[str] | list[Static6SdwanzoneItem] | None = ...,
        dstaddr: str | None = ...,
        link_monitor_exempt: Literal["enable", "disable"] | None = ...,
        vrf: int | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        tag: int | None = ...,
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
    "Static6",
    "Static6Payload",
    "Static6Response",
    "Static6Object",
]