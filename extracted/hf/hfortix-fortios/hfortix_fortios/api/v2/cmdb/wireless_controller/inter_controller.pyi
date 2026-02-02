""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/inter_controller
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

class InterControllerIntercontrollerpeerItem(TypedDict, total=False):
    """Nested item for inter-controller-peer field."""
    id: int
    peer_ip: str
    peer_port: int
    peer_priority: Literal["primary", "secondary"]


class InterControllerPayload(TypedDict, total=False):
    """Payload type for InterController operations."""
    inter_controller_mode: Literal["disable", "l2-roaming", "1+1"]
    l3_roaming: Literal["enable", "disable"]
    inter_controller_key: str
    inter_controller_pri: Literal["primary", "secondary"]
    fast_failover_max: int
    fast_failover_wait: int
    inter_controller_peer: str | list[str] | list[InterControllerIntercontrollerpeerItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class InterControllerResponse(TypedDict, total=False):
    """Response type for InterController - use with .dict property for typed dict access."""
    inter_controller_mode: Literal["disable", "l2-roaming", "1+1"]
    l3_roaming: Literal["enable", "disable"]
    inter_controller_key: str
    inter_controller_pri: Literal["primary", "secondary"]
    fast_failover_max: int
    fast_failover_wait: int
    inter_controller_peer: list[InterControllerIntercontrollerpeerItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class InterControllerIntercontrollerpeerItemObject(FortiObject[InterControllerIntercontrollerpeerItem]):
    """Typed object for inter-controller-peer table items with attribute access."""
    id: int
    peer_ip: str
    peer_port: int
    peer_priority: Literal["primary", "secondary"]


class InterControllerObject(FortiObject):
    """Typed FortiObject for InterController with field access."""
    inter_controller_mode: Literal["disable", "l2-roaming", "1+1"]
    l3_roaming: Literal["enable", "disable"]
    inter_controller_key: str
    inter_controller_pri: Literal["primary", "secondary"]
    fast_failover_max: int
    fast_failover_wait: int
    inter_controller_peer: FortiObjectList[InterControllerIntercontrollerpeerItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class InterController:
    """
    
    Endpoint: wireless_controller/inter_controller
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterControllerObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: InterControllerPayload | None = ...,
        inter_controller_mode: Literal["disable", "l2-roaming", "1+1"] | None = ...,
        l3_roaming: Literal["enable", "disable"] | None = ...,
        inter_controller_key: str | None = ...,
        inter_controller_pri: Literal["primary", "secondary"] | None = ...,
        fast_failover_max: int | None = ...,
        fast_failover_wait: int | None = ...,
        inter_controller_peer: str | list[str] | list[InterControllerIntercontrollerpeerItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> InterControllerObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InterControllerPayload | None = ...,
        inter_controller_mode: Literal["disable", "l2-roaming", "1+1"] | None = ...,
        l3_roaming: Literal["enable", "disable"] | None = ...,
        inter_controller_key: str | None = ...,
        inter_controller_pri: Literal["primary", "secondary"] | None = ...,
        fast_failover_max: int | None = ...,
        fast_failover_wait: int | None = ...,
        inter_controller_peer: str | list[str] | list[InterControllerIntercontrollerpeerItem] | None = ...,
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
    "InterController",
    "InterControllerPayload",
    "InterControllerResponse",
    "InterControllerObject",
]