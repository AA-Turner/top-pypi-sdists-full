""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: ftp_proxy/explicit
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

class ExplicitSslcertItem(TypedDict, total=False):
    """Nested item for ssl-cert field."""
    name: str


class ExplicitPayload(TypedDict, total=False):
    """Payload type for Explicit operations."""
    status: Literal["enable", "disable"]
    incoming_port: str
    incoming_ip: str
    outgoing_ip: str | list[str]
    sec_default_action: Literal["accept", "deny"]
    server_data_mode: Literal["client", "passive"]
    ssl: Literal["enable", "disable"]
    ssl_cert: str | list[str] | list[ExplicitSslcertItem]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ssl_algorithm: Literal["high", "medium", "low"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ExplicitResponse(TypedDict, total=False):
    """Response type for Explicit - use with .dict property for typed dict access."""
    status: Literal["enable", "disable"]
    incoming_port: str
    incoming_ip: str
    outgoing_ip: str | list[str]
    sec_default_action: Literal["accept", "deny"]
    server_data_mode: Literal["client", "passive"]
    ssl: Literal["enable", "disable"]
    ssl_cert: list[ExplicitSslcertItem]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ssl_algorithm: Literal["high", "medium", "low"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ExplicitSslcertItemObject(FortiObject[ExplicitSslcertItem]):
    """Typed object for ssl-cert table items with attribute access."""
    name: str


class ExplicitObject(FortiObject):
    """Typed FortiObject for Explicit with field access."""
    status: Literal["enable", "disable"]
    incoming_port: str
    incoming_ip: str
    outgoing_ip: str | list[str]
    sec_default_action: Literal["accept", "deny"]
    server_data_mode: Literal["client", "passive"]
    ssl: Literal["enable", "disable"]
    ssl_cert: FortiObjectList[ExplicitSslcertItemObject]
    ssl_dh_bits: Literal["768", "1024", "1536", "2048"]
    ssl_algorithm: Literal["high", "medium", "low"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Explicit:
    """
    
    Endpoint: ftp_proxy/explicit
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
    ) -> ExplicitObject: ...
    
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
        payload_dict: ExplicitPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        incoming_port: str | None = ...,
        incoming_ip: str | None = ...,
        outgoing_ip: str | list[str] | None = ...,
        sec_default_action: Literal["accept", "deny"] | None = ...,
        server_data_mode: Literal["client", "passive"] | None = ...,
        ssl: Literal["enable", "disable"] | None = ...,
        ssl_cert: str | list[str] | list[ExplicitSslcertItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ExplicitObject: ...


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
        payload_dict: ExplicitPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        incoming_port: str | None = ...,
        incoming_ip: str | None = ...,
        outgoing_ip: str | list[str] | None = ...,
        sec_default_action: Literal["accept", "deny"] | None = ...,
        server_data_mode: Literal["client", "passive"] | None = ...,
        ssl: Literal["enable", "disable"] | None = ...,
        ssl_cert: str | list[str] | list[ExplicitSslcertItem] | None = ...,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048"] | None = ...,
        ssl_algorithm: Literal["high", "medium", "low"] | None = ...,
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
    "Explicit",
    "ExplicitPayload",
    "ExplicitResponse",
    "ExplicitObject",
]