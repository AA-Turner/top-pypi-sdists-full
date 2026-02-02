""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/probe_response
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

class ProbeResponsePayload(TypedDict, total=False):
    """Payload type for ProbeResponse operations."""
    port: int
    http_probe_value: str
    ttl_mode: Literal["reinit", "decrease", "retain"]
    mode: Literal["none", "http-probe", "twamp"]
    security_mode: Literal["none", "authentication"]
    password: str
    timeout: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProbeResponseResponse(TypedDict, total=False):
    """Response type for ProbeResponse - use with .dict property for typed dict access."""
    port: int
    http_probe_value: str
    ttl_mode: Literal["reinit", "decrease", "retain"]
    mode: Literal["none", "http-probe", "twamp"]
    security_mode: Literal["none", "authentication"]
    password: str
    timeout: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProbeResponseObject(FortiObject):
    """Typed FortiObject for ProbeResponse with field access."""
    port: int
    http_probe_value: str
    ttl_mode: Literal["reinit", "decrease", "retain"]
    mode: Literal["none", "http-probe", "twamp"]
    security_mode: Literal["none", "authentication"]
    password: str
    timeout: int


# ================================================================
# Main Endpoint Class
# ================================================================

class ProbeResponse:
    """
    
    Endpoint: system/probe_response
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
    ) -> ProbeResponseObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProbeResponsePayload | None = ...,
        port: int | None = ...,
        http_probe_value: str | None = ...,
        ttl_mode: Literal["reinit", "decrease", "retain"] | None = ...,
        mode: Literal["none", "http-probe", "twamp"] | None = ...,
        security_mode: Literal["none", "authentication"] | None = ...,
        password: str | None = ...,
        timeout: int | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProbeResponseObject: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ProbeResponsePayload | None = ...,
        port: int | None = ...,
        http_probe_value: str | None = ...,
        ttl_mode: Literal["reinit", "decrease", "retain"] | None = ...,
        mode: Literal["none", "http-probe", "twamp"] | None = ...,
        security_mode: Literal["none", "authentication"] | None = ...,
        password: str | None = ...,
        timeout: int | None = ...,
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
    "ProbeResponse",
    "ProbeResponsePayload",
    "ProbeResponseResponse",
    "ProbeResponseObject",
]