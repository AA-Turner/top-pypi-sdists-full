""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/virtual_switch
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class VirtualSwitchPortItem(TypedDict, total=False):
    """Nested item for port field."""
    name: str
    alias: str


class VirtualSwitchPayload(TypedDict, total=False):
    """Payload type for VirtualSwitch operations."""
    name: str
    physical_switch: str
    vlan: int
    port: str | list[str] | list[VirtualSwitchPortItem]
    span: Literal["disable", "enable"]
    span_source_port: str
    span_dest_port: str
    span_direction: Literal["rx", "tx", "both"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class VirtualSwitchResponse(TypedDict, total=False):
    """Response type for VirtualSwitch - use with .dict property for typed dict access."""
    name: str
    physical_switch: str
    vlan: int
    port: list[VirtualSwitchPortItem]
    span: Literal["disable", "enable"]
    span_source_port: str
    span_dest_port: str
    span_direction: Literal["rx", "tx", "both"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class VirtualSwitchPortItemObject(FortiObject[VirtualSwitchPortItem]):
    """Typed object for port table items with attribute access."""
    name: str
    alias: str


class VirtualSwitchObject(FortiObject):
    """Typed FortiObject for VirtualSwitch with field access."""
    name: str
    physical_switch: str
    vlan: int
    port: FortiObjectList[VirtualSwitchPortItemObject]
    span: Literal["disable", "enable"]
    span_source_port: str
    span_dest_port: str
    span_direction: Literal["rx", "tx", "both"]


# ================================================================
# Main Endpoint Class
# ================================================================

class VirtualSwitch:
    """
    
    Endpoint: system/virtual_switch
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
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
    ) -> VirtualSwitchObject: ...
    
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
        payload_dict: VirtualSwitchPayload | None = ...,
        name: str | None = ...,
        physical_switch: str | None = ...,
        vlan: int | None = ...,
        port: str | list[str] | list[VirtualSwitchPortItem] | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_source_port: str | None = ...,
        span_dest_port: str | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VirtualSwitchObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: VirtualSwitchPayload | None = ...,
        name: str | None = ...,
        physical_switch: str | None = ...,
        vlan: int | None = ...,
        port: str | list[str] | list[VirtualSwitchPortItem] | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_source_port: str | None = ...,
        span_dest_port: str | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> VirtualSwitchObject: ...

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
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
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
        payload_dict: VirtualSwitchPayload | None = ...,
        name: str | None = ...,
        physical_switch: str | None = ...,
        vlan: int | None = ...,
        port: str | list[str] | list[VirtualSwitchPortItem] | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_source_port: str | None = ...,
        span_dest_port: str | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
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
    "VirtualSwitch",
    "VirtualSwitchPayload",
    "VirtualSwitchResponse",
    "VirtualSwitchObject",
]