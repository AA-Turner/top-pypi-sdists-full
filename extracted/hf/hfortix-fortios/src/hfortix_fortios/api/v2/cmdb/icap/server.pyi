""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: icap/server
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

class ServerPayload(TypedDict, total=False):
    """Payload type for Server operations."""
    name: str
    addr_type: Literal["ip4", "ip6", "fqdn"]
    ip_address: str
    ip6_address: str
    fqdn: str
    port: int
    max_connections: int
    secure: Literal["disable", "enable"]
    ssl_cert: str
    healthcheck: Literal["disable", "enable"]
    healthcheck_service: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ServerResponse(TypedDict, total=False):
    """Response type for Server - use with .dict property for typed dict access."""
    name: str
    addr_type: Literal["ip4", "ip6", "fqdn"]
    ip_address: str
    ip6_address: str
    fqdn: str
    port: int
    max_connections: int
    secure: Literal["disable", "enable"]
    ssl_cert: str
    healthcheck: Literal["disable", "enable"]
    healthcheck_service: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ServerObject(FortiObject):
    """Typed FortiObject for Server with field access."""
    name: str
    addr_type: Literal["ip4", "ip6", "fqdn"]
    ip_address: str
    ip6_address: str
    fqdn: str
    port: int
    max_connections: int
    secure: Literal["disable", "enable"]
    ssl_cert: str
    healthcheck: Literal["disable", "enable"]
    healthcheck_service: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Server:
    """
    
    Endpoint: icap/server
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
    ) -> ServerObject: ...
    
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
    ) -> FortiObjectList[ServerObject]: ...
    
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
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ServerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ServerObject: ...

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
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
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
    "Server",
    "ServerPayload",
    "ServerResponse",
    "ServerObject",
]