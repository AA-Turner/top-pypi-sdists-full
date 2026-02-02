""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/mac_policy
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

class MacPolicyPayload(TypedDict, total=False):
    """Payload type for MacPolicy operations."""
    name: str
    description: str
    fortilink: str
    vlan: str
    traffic_policy: str
    count: Literal["disable", "enable"]
    bounce_port_link: Literal["disable", "enable"]
    bounce_port_duration: int
    poe_reset: Literal["disable", "enable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class MacPolicyResponse(TypedDict, total=False):
    """Response type for MacPolicy - use with .dict property for typed dict access."""
    name: str
    description: str
    fortilink: str
    vlan: str
    traffic_policy: str
    count: Literal["disable", "enable"]
    bounce_port_link: Literal["disable", "enable"]
    bounce_port_duration: int
    poe_reset: Literal["disable", "enable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class MacPolicyObject(FortiObject):
    """Typed FortiObject for MacPolicy with field access."""
    name: str
    description: str
    fortilink: str
    vlan: str
    traffic_policy: str
    count: Literal["disable", "enable"]
    bounce_port_link: Literal["disable", "enable"]
    bounce_port_duration: int
    poe_reset: Literal["disable", "enable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class MacPolicy:
    """
    
    Endpoint: switch_controller/mac_policy
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
    ) -> MacPolicyObject: ...
    
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
    ) -> FortiObjectList[MacPolicyObject]: ...
    
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
        payload_dict: MacPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        traffic_policy: str | None = ...,
        count: Literal["disable", "enable"] | None = ...,
        bounce_port_link: Literal["disable", "enable"] | None = ...,
        bounce_port_duration: int | None = ...,
        poe_reset: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MacPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: MacPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        traffic_policy: str | None = ...,
        count: Literal["disable", "enable"] | None = ...,
        bounce_port_link: Literal["disable", "enable"] | None = ...,
        bounce_port_duration: int | None = ...,
        poe_reset: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> MacPolicyObject: ...

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
        payload_dict: MacPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        traffic_policy: str | None = ...,
        count: Literal["disable", "enable"] | None = ...,
        bounce_port_link: Literal["disable", "enable"] | None = ...,
        bounce_port_duration: int | None = ...,
        poe_reset: Literal["disable", "enable"] | None = ...,
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
    "MacPolicy",
    "MacPolicyPayload",
    "MacPolicyResponse",
    "MacPolicyObject",
]