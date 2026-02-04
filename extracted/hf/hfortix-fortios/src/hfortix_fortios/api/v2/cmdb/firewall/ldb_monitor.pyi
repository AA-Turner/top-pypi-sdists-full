""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/ldb_monitor
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

class LdbMonitorPayload(TypedDict, total=False):
    """Payload type for LdbMonitor operations."""
    name: str
    type: Literal["ping", "tcp", "http", "https", "dns"]
    interval: int
    timeout: int
    retry: int
    port: int
    src_ip: str
    http_get: str
    http_match: str
    http_max_redirects: int
    dns_protocol: Literal["udp", "tcp"]
    dns_request_domain: str
    dns_match_ip: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LdbMonitorResponse(TypedDict, total=False):
    """Response type for LdbMonitor - use with .dict property for typed dict access."""
    name: str
    type: Literal["ping", "tcp", "http", "https", "dns"]
    interval: int
    timeout: int
    retry: int
    port: int
    src_ip: str
    http_get: str
    http_match: str
    http_max_redirects: int
    dns_protocol: Literal["udp", "tcp"]
    dns_request_domain: str
    dns_match_ip: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LdbMonitorObject(FortiObject):
    """Typed FortiObject for LdbMonitor with field access."""
    name: str
    type: Literal["ping", "tcp", "http", "https", "dns"]
    interval: int
    timeout: int
    retry: int
    port: int
    src_ip: str
    http_get: str
    http_match: str
    http_max_redirects: int
    dns_protocol: Literal["udp", "tcp"]
    dns_request_domain: str
    dns_match_ip: str


# ================================================================
# Main Endpoint Class
# ================================================================

class LdbMonitor:
    """
    
    Endpoint: firewall/ldb_monitor
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
    ) -> LdbMonitorObject: ...
    
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
    ) -> FortiObjectList[LdbMonitorObject]: ...
    
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
        payload_dict: LdbMonitorPayload | None = ...,
        name: str | None = ...,
        type: Literal["ping", "tcp", "http", "https", "dns"] | None = ...,
        interval: int | None = ...,
        timeout: int | None = ...,
        retry: int | None = ...,
        port: int | None = ...,
        src_ip: str | None = ...,
        http_get: str | None = ...,
        http_match: str | None = ...,
        http_max_redirects: int | None = ...,
        dns_protocol: Literal["udp", "tcp"] | None = ...,
        dns_request_domain: str | None = ...,
        dns_match_ip: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LdbMonitorObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LdbMonitorPayload | None = ...,
        name: str | None = ...,
        type: Literal["ping", "tcp", "http", "https", "dns"] | None = ...,
        interval: int | None = ...,
        timeout: int | None = ...,
        retry: int | None = ...,
        port: int | None = ...,
        src_ip: str | None = ...,
        http_get: str | None = ...,
        http_match: str | None = ...,
        http_max_redirects: int | None = ...,
        dns_protocol: Literal["udp", "tcp"] | None = ...,
        dns_request_domain: str | None = ...,
        dns_match_ip: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LdbMonitorObject: ...

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
        payload_dict: LdbMonitorPayload | None = ...,
        name: str | None = ...,
        type: Literal["ping", "tcp", "http", "https", "dns"] | None = ...,
        interval: int | None = ...,
        timeout: int | None = ...,
        retry: int | None = ...,
        port: int | None = ...,
        src_ip: str | None = ...,
        http_get: str | None = ...,
        http_match: str | None = ...,
        http_max_redirects: int | None = ...,
        dns_protocol: Literal["udp", "tcp"] | None = ...,
        dns_request_domain: str | None = ...,
        dns_match_ip: str | None = ...,
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
    "LdbMonitor",
    "LdbMonitorPayload",
    "LdbMonitorResponse",
    "LdbMonitorObject",
]