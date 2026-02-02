""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/storm_control_policy
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

class StormControlPolicyPayload(TypedDict, total=False):
    """Payload type for StormControlPolicy operations."""
    name: str
    description: str
    storm_control_mode: Literal["global", "override", "disabled"]
    rate: int
    burst_size_level: int
    unknown_unicast: Literal["enable", "disable"]
    unknown_multicast: Literal["enable", "disable"]
    broadcast: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class StormControlPolicyResponse(TypedDict, total=False):
    """Response type for StormControlPolicy - use with .dict property for typed dict access."""
    name: str
    description: str
    storm_control_mode: Literal["global", "override", "disabled"]
    rate: int
    burst_size_level: int
    unknown_unicast: Literal["enable", "disable"]
    unknown_multicast: Literal["enable", "disable"]
    broadcast: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class StormControlPolicyObject(FortiObject):
    """Typed FortiObject for StormControlPolicy with field access."""
    name: str
    description: str
    storm_control_mode: Literal["global", "override", "disabled"]
    rate: int
    burst_size_level: int
    unknown_unicast: Literal["enable", "disable"]
    unknown_multicast: Literal["enable", "disable"]
    broadcast: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class StormControlPolicy:
    """
    
    Endpoint: switch_controller/storm_control_policy
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
    ) -> StormControlPolicyObject: ...
    
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
    ) -> FortiObjectList[StormControlPolicyObject]: ...
    
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
        payload_dict: StormControlPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        storm_control_mode: Literal["global", "override", "disabled"] | None = ...,
        rate: int | None = ...,
        burst_size_level: int | None = ...,
        unknown_unicast: Literal["enable", "disable"] | None = ...,
        unknown_multicast: Literal["enable", "disable"] | None = ...,
        broadcast: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StormControlPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: StormControlPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        storm_control_mode: Literal["global", "override", "disabled"] | None = ...,
        rate: int | None = ...,
        burst_size_level: int | None = ...,
        unknown_unicast: Literal["enable", "disable"] | None = ...,
        unknown_multicast: Literal["enable", "disable"] | None = ...,
        broadcast: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> StormControlPolicyObject: ...

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
        payload_dict: StormControlPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        storm_control_mode: Literal["global", "override", "disabled"] | None = ...,
        rate: int | None = ...,
        burst_size_level: int | None = ...,
        unknown_unicast: Literal["enable", "disable"] | None = ...,
        unknown_multicast: Literal["enable", "disable"] | None = ...,
        broadcast: Literal["enable", "disable"] | None = ...,
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
    "StormControlPolicy",
    "StormControlPolicyPayload",
    "StormControlPolicyResponse",
    "StormControlPolicyObject",
]