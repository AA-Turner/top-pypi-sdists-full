""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/syslog_profile
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

class SyslogProfilePayload(TypedDict, total=False):
    """Payload type for SyslogProfile operations."""
    name: str
    comment: str
    server_status: Literal["enable", "disable"]
    server: str
    server_port: int
    server_type: Literal["standard", "fortianalyzer"]
    log_level: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debugging"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SyslogProfileResponse(TypedDict, total=False):
    """Response type for SyslogProfile - use with .dict property for typed dict access."""
    name: str
    comment: str
    server_status: Literal["enable", "disable"]
    server: str
    server_port: int
    server_type: Literal["standard", "fortianalyzer"]
    log_level: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debugging"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SyslogProfileObject(FortiObject):
    """Typed FortiObject for SyslogProfile with field access."""
    name: str
    comment: str
    server_status: Literal["enable", "disable"]
    server: str
    server_port: int
    server_type: Literal["standard", "fortianalyzer"]
    log_level: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debugging"]


# ================================================================
# Main Endpoint Class
# ================================================================

class SyslogProfile:
    """
    
    Endpoint: wireless_controller/syslog_profile
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
    ) -> SyslogProfileObject: ...
    
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
    ) -> FortiObjectList[SyslogProfileObject]: ...
    
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
        payload_dict: SyslogProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        server_status: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        server_port: int | None = ...,
        server_type: Literal["standard", "fortianalyzer"] | None = ...,
        log_level: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debugging"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SyslogProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SyslogProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        server_status: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        server_port: int | None = ...,
        server_type: Literal["standard", "fortianalyzer"] | None = ...,
        log_level: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debugging"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SyslogProfileObject: ...

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
        payload_dict: SyslogProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        server_status: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        server_port: int | None = ...,
        server_type: Literal["standard", "fortianalyzer"] | None = ...,
        log_level: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debugging"] | None = ...,
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
    "SyslogProfile",
    "SyslogProfilePayload",
    "SyslogProfileResponse",
    "SyslogProfileObject",
]