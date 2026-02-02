""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/snmp/sysinfo
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

class SysinfoPayload(TypedDict, total=False):
    """Payload type for Sysinfo operations."""
    status: Literal["enable", "disable"]
    engine_id_type: Literal["text", "hex", "mac"]
    engine_id: str
    description: str
    contact_info: str
    location: str
    trap_high_cpu_threshold: int
    trap_low_memory_threshold: int
    trap_log_full_threshold: int
    trap_free_memory_threshold: int
    trap_freeable_memory_threshold: int
    append_index: Literal["enable", "disable"]
    non_mgmt_vdom_query: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SysinfoResponse(TypedDict, total=False):
    """Response type for Sysinfo - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    engine_id_type: Literal["text", "hex", "mac"]
    engine_id: str
    description: str
    contact_info: str
    location: str
    trap_high_cpu_threshold: int
    trap_low_memory_threshold: int
    trap_log_full_threshold: int
    trap_free_memory_threshold: int
    trap_freeable_memory_threshold: int
    append_index: Literal["enable", "disable"]
    non_mgmt_vdom_query: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SysinfoObject(FortiObject):
    """Typed FortiObject for Sysinfo with field access."""
    status: Literal["enable", "disable"]
    engine_id_type: Literal["text", "hex", "mac"]
    engine_id: str
    description: str
    contact_info: str
    location: str
    trap_high_cpu_threshold: int
    trap_low_memory_threshold: int
    trap_log_full_threshold: int
    trap_free_memory_threshold: int
    trap_freeable_memory_threshold: int
    append_index: Literal["enable", "disable"]
    non_mgmt_vdom_query: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Sysinfo:
    """
    
    Endpoint: system/snmp/sysinfo
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
    ) -> SysinfoObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SysinfoPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        engine_id_type: Literal["text", "hex", "mac"] | None = ...,
        engine_id: str | None = ...,
        description: str | None = ...,
        contact_info: str | None = ...,
        location: str | None = ...,
        trap_high_cpu_threshold: int | None = ...,
        trap_low_memory_threshold: int | None = ...,
        trap_log_full_threshold: int | None = ...,
        trap_free_memory_threshold: int | None = ...,
        trap_freeable_memory_threshold: int | None = ...,
        append_index: Literal["enable", "disable"] | None = ...,
        non_mgmt_vdom_query: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SysinfoObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SysinfoPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        engine_id_type: Literal["text", "hex", "mac"] | None = ...,
        engine_id: str | None = ...,
        description: str | None = ...,
        contact_info: str | None = ...,
        location: str | None = ...,
        trap_high_cpu_threshold: int | None = ...,
        trap_low_memory_threshold: int | None = ...,
        trap_log_full_threshold: int | None = ...,
        trap_free_memory_threshold: int | None = ...,
        trap_freeable_memory_threshold: int | None = ...,
        append_index: Literal["enable", "disable"] | None = ...,
        non_mgmt_vdom_query: Literal["enable", "disable"] | None = ...,
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
    "Sysinfo",
    "SysinfoPayload",
    "SysinfoResponse",
    "SysinfoObject",
]