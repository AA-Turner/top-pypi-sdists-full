""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: switch_controller/snmp_sysinfo
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

class SnmpSysinfoPayload(TypedDict, total=False):
    """Payload type for SnmpSysinfo operations."""
    status: Literal["disable", "enable"]
    engine_id: str
    description: str
    contact_info: str
    location: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SnmpSysinfoResponse(TypedDict, total=False):
    """Response type for SnmpSysinfo - use with .dict property for typed dict access."""
    status: Literal["disable", "enable"]
    engine_id: str
    description: str
    contact_info: str
    location: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SnmpSysinfoObject(FortiObject):
    """Typed FortiObject for SnmpSysinfo with field access."""
    status: Literal["disable", "enable"]
    engine_id: str
    description: str
    contact_info: str
    location: str


# ================================================================
# Main Endpoint Class
# ================================================================

class SnmpSysinfo:
    """
    
    Endpoint: switch_controller/snmp_sysinfo
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
    ) -> SnmpSysinfoObject: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SnmpSysinfoPayload | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        engine_id: str | None = ...,
        description: str | None = ...,
        contact_info: str | None = ...,
        location: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SnmpSysinfoObject: ...


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
        payload_dict: SnmpSysinfoPayload | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        engine_id: str | None = ...,
        description: str | None = ...,
        contact_info: str | None = ...,
        location: str | None = ...,
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
    "SnmpSysinfo",
    "SnmpSysinfoPayload",
    "SnmpSysinfoResponse",
    "SnmpSysinfoObject",
]