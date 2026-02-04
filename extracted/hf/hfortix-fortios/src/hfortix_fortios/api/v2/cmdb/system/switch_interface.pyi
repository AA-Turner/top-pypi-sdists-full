""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/switch_interface
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

class SwitchInterfaceSpansourceportItem(TypedDict, total=False):
    """Nested item for span-source-port field."""
    interface_name: str


class SwitchInterfaceMemberItem(TypedDict, total=False):
    """Nested item for member field."""
    interface_name: str


class SwitchInterfacePayload(TypedDict, total=False):
    """Payload type for SwitchInterface operations."""
    name: str
    vdom: str
    span_dest_port: str
    span_source_port: str | list[str] | list[SwitchInterfaceSpansourceportItem]
    member: str | list[str] | list[SwitchInterfaceMemberItem]
    type: Literal["switch", "hub"]
    intra_switch_policy: Literal["implicit", "explicit"]
    mac_ttl: int
    span: Literal["disable", "enable"]
    span_direction: Literal["rx", "tx", "both"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SwitchInterfaceResponse(TypedDict, total=False):
    """Response type for SwitchInterface - use with .dict property for typed dict access."""
    name: str
    vdom: str
    span_dest_port: str
    span_source_port: list[SwitchInterfaceSpansourceportItem]
    member: list[SwitchInterfaceMemberItem]
    type: Literal["switch", "hub"]
    intra_switch_policy: Literal["implicit", "explicit"]
    mac_ttl: int
    span: Literal["disable", "enable"]
    span_direction: Literal["rx", "tx", "both"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SwitchInterfaceSpansourceportItemObject(FortiObject[SwitchInterfaceSpansourceportItem]):
    """Typed object for span-source-port table items with attribute access."""
    interface_name: str


class SwitchInterfaceMemberItemObject(FortiObject[SwitchInterfaceMemberItem]):
    """Typed object for member table items with attribute access."""
    interface_name: str


class SwitchInterfaceObject(FortiObject):
    """Typed FortiObject for SwitchInterface with field access."""
    name: str
    span_dest_port: str
    span_source_port: FortiObjectList[SwitchInterfaceSpansourceportItemObject]
    member: FortiObjectList[SwitchInterfaceMemberItemObject]
    type: Literal["switch", "hub"]
    intra_switch_policy: Literal["implicit", "explicit"]
    mac_ttl: int
    span: Literal["disable", "enable"]
    span_direction: Literal["rx", "tx", "both"]


# ================================================================
# Main Endpoint Class
# ================================================================

class SwitchInterface:
    """
    
    Endpoint: system/switch_interface
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
    ) -> SwitchInterfaceObject: ...
    
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
    ) -> FortiObjectList[SwitchInterfaceObject]: ...
    
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
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[SwitchInterfaceSpansourceportItem] | None = ...,
        member: str | list[str] | list[SwitchInterfaceMemberItem] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SwitchInterfaceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[SwitchInterfaceSpansourceportItem] | None = ...,
        member: str | list[str] | list[SwitchInterfaceMemberItem] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SwitchInterfaceObject: ...

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
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[SwitchInterfaceSpansourceportItem] | None = ...,
        member: str | list[str] | list[SwitchInterfaceMemberItem] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
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
    "SwitchInterface",
    "SwitchInterfacePayload",
    "SwitchInterfaceResponse",
    "SwitchInterfaceObject",
]