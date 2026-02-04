""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/fortisandbox
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

class FortisandboxPayload(TypedDict, total=False):
    """Payload type for Fortisandbox operations."""
    status: Literal["enable", "disable"]
    forticloud: Literal["enable", "disable"]
    inline_scan: Literal["enable", "disable"]
    server: str
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    enc_algorithm: Literal["default", "high", "low"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    email: str
    ca: str
    cn: str
    certificate_verification: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FortisandboxResponse(TypedDict, total=False):
    """Response type for Fortisandbox - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    forticloud: Literal["enable", "disable"]
    inline_scan: Literal["enable", "disable"]
    server: str
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    enc_algorithm: Literal["default", "high", "low"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    email: str
    ca: str
    cn: str
    certificate_verification: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FortisandboxObject(FortiObject):
    """Typed FortiObject for Fortisandbox with field access."""
    status: Literal["enable", "disable"]
    forticloud: Literal["enable", "disable"]
    inline_scan: Literal["enable", "disable"]
    server: str
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    enc_algorithm: Literal["default", "high", "low"]
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    email: str
    ca: str
    cn: str
    certificate_verification: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Fortisandbox:
    """
    
    Endpoint: system/fortisandbox
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
    ) -> FortisandboxObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FortisandboxPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        forticloud: Literal["enable", "disable"] | None = ...,
        inline_scan: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        enc_algorithm: Literal["default", "high", "low"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        email: str | None = ...,
        ca: str | None = ...,
        cn: str | None = ...,
        certificate_verification: Literal["enable", "disable"] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortisandboxObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FortisandboxPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        forticloud: Literal["enable", "disable"] | None = ...,
        inline_scan: Literal["enable", "disable"] | None = ...,
        server: str | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        enc_algorithm: Literal["default", "high", "low"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        email: str | None = ...,
        ca: str | None = ...,
        cn: str | None = ...,
        certificate_verification: Literal["enable", "disable"] | None = ...,
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
    "Fortisandbox",
    "FortisandboxPayload",
    "FortisandboxResponse",
    "FortisandboxObject",
]