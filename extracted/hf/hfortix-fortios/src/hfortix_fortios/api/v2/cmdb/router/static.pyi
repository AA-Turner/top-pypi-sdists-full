""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: router/static
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

class StaticSdwanzoneItem(TypedDict, total=False):
    """Nested item for sdwan-zone field."""
    name: str


class StaticPayload(TypedDict, total=False):
    """Payload type for Static operations."""
    seq_num: int
    status: Literal["enable", "disable"]
    dst: str
    src: str
    gateway: str
    preferred_source: str
    distance: int
    weight: int
    priority: int
    device: str
    comment: str
    blackhole: Literal["enable", "disable"]
    dynamic_gateway: Literal["enable", "disable"]
    sdwan_zone: str | list[str] | list[StaticSdwanzoneItem]
    dstaddr: str
    internet_service: int
    internet_service_custom: str
    internet_service_fortiguard: str
    link_monitor_exempt: Literal["enable", "disable"]
    tag: int
    vrf: int
    bfd: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StaticResponse(TypedDict, total=False):
    """Response type for Static - use with .dict property for typed dict access."""
    seq_num: int
    status: Literal["enable", "disable"]
    dst: str
    src: str
    gateway: str
    preferred_source: str
    distance: int
    weight: int
    priority: int
    device: str
    comment: str
    blackhole: Literal["enable", "disable"]
    dynamic_gateway: Literal["enable", "disable"]
    sdwan_zone: list[StaticSdwanzoneItem]
    dstaddr: str
    internet_service: int
    internet_service_custom: str
    internet_service_fortiguard: str
    link_monitor_exempt: Literal["enable", "disable"]
    tag: int
    vrf: int
    bfd: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StaticSdwanzoneItemObject(FortiObject[StaticSdwanzoneItem]):
    """Typed object for sdwan-zone table items with attribute access."""
    name: str


class StaticObject(FortiObject):
    """Typed FortiObject for Static with field access."""
    seq_num: int
    status: Literal["enable", "disable"]
    dst: str
    src: str
    gateway: str
    preferred_source: str
    distance: int
    weight: int
    priority: int
    device: str
    comment: str
    blackhole: Literal["enable", "disable"]
    dynamic_gateway: Literal["enable", "disable"]
    sdwan_zone: FortiObjectList[StaticSdwanzoneItemObject]
    dstaddr: str
    internet_service: int
    internet_service_custom: str
    internet_service_fortiguard: str
    link_monitor_exempt: Literal["enable", "disable"]
    tag: int
    vrf: int
    bfd: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Static:
    """
    
    Endpoint: router/static
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
    ) -> StaticObject: ...
    
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
    ) -> FortiObjectList[StaticObject]: ...
    
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
        payload_dict: StaticPayload | None = ...,
        seq_num: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dst: str | None = ...,
        src: str | None = ...,
        gateway: str | None = ...,
        preferred_source: str | None = ...,
        distance: int | None = ...,
        weight: int | None = ...,
        priority: int | None = ...,
        device: str | None = ...,
        comment: str | None = ...,
        blackhole: Literal["enable", "disable"] | None = ...,
        dynamic_gateway: Literal["enable", "disable"] | None = ...,
        sdwan_zone: str | list[str] | list[StaticSdwanzoneItem] | None = ...,
        dstaddr: str | None = ...,
        internet_service: int | None = ...,
        internet_service_custom: str | None = ...,
        internet_service_fortiguard: str | None = ...,
        link_monitor_exempt: Literal["enable", "disable"] | None = ...,
        tag: int | None = ...,
        vrf: int | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StaticObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StaticPayload | None = ...,
        seq_num: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dst: str | None = ...,
        src: str | None = ...,
        gateway: str | None = ...,
        preferred_source: str | None = ...,
        distance: int | None = ...,
        weight: int | None = ...,
        priority: int | None = ...,
        device: str | None = ...,
        comment: str | None = ...,
        blackhole: Literal["enable", "disable"] | None = ...,
        dynamic_gateway: Literal["enable", "disable"] | None = ...,
        sdwan_zone: str | list[str] | list[StaticSdwanzoneItem] | None = ...,
        dstaddr: str | None = ...,
        internet_service: int | None = ...,
        internet_service_custom: str | None = ...,
        internet_service_fortiguard: str | None = ...,
        link_monitor_exempt: Literal["enable", "disable"] | None = ...,
        tag: int | None = ...,
        vrf: int | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StaticObject: ...

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
        payload_dict: StaticPayload | None = ...,
        seq_num: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        dst: str | None = ...,
        src: str | None = ...,
        gateway: str | None = ...,
        preferred_source: str | None = ...,
        distance: int | None = ...,
        weight: int | None = ...,
        priority: int | None = ...,
        device: str | None = ...,
        comment: str | None = ...,
        blackhole: Literal["enable", "disable"] | None = ...,
        dynamic_gateway: Literal["enable", "disable"] | None = ...,
        sdwan_zone: str | list[str] | list[StaticSdwanzoneItem] | None = ...,
        dstaddr: str | None = ...,
        internet_service: int | None = ...,
        internet_service_custom: str | None = ...,
        internet_service_fortiguard: str | None = ...,
        link_monitor_exempt: Literal["enable", "disable"] | None = ...,
        tag: int | None = ...,
        vrf: int | None = ...,
        bfd: Literal["enable", "disable"] | None = ...,
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
    "Static",
    "StaticPayload",
    "StaticResponse",
    "StaticObject",
]