""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: vpn/kmip_server
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

class KmipServerServerlistItem(TypedDict, total=False):
    """Nested item for server-list field."""
    id: int
    status: Literal["enable", "disable"]
    server: str
    port: int
    cert: str


class KmipServerPayload(TypedDict, total=False):
    """Payload type for KmipServer operations."""
    name: str
    server_list: str | list[str] | list[KmipServerServerlistItem]
    username: str
    password: str
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    server_identity_check: Literal["enable", "disable"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    source_ip: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class KmipServerResponse(TypedDict, total=False):
    """Response type for KmipServer - use with .dict property for typed dict access."""
    name: str
    server_list: list[KmipServerServerlistItem]
    username: str
    password: str
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    server_identity_check: Literal["enable", "disable"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    source_ip: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class KmipServerServerlistItemObject(FortiObject[KmipServerServerlistItem]):
    """Typed object for server-list table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    server: str
    port: int
    cert: str


class KmipServerObject(FortiObject):
    """Typed FortiObject for KmipServer with field access."""
    name: str
    server_list: FortiObjectList[KmipServerServerlistItemObject]
    username: str
    password: str
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    server_identity_check: Literal["enable", "disable"]
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int
    source_ip: str


# ================================================================
# Main Endpoint Class
# ================================================================

class KmipServer:
    """
    
    Endpoint: vpn/kmip_server
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
    ) -> KmipServerObject: ...
    
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
    ) -> FortiObjectList[KmipServerObject]: ...
    
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
        payload_dict: KmipServerPayload | None = ...,
        name: str | None = ...,
        server_list: str | list[str] | list[KmipServerServerlistItem] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KmipServerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: KmipServerPayload | None = ...,
        name: str | None = ...,
        server_list: str | list[str] | list[KmipServerServerlistItem] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> KmipServerObject: ...

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
        payload_dict: KmipServerPayload | None = ...,
        name: str | None = ...,
        server_list: str | list[str] | list[KmipServerServerlistItem] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        source_ip: str | None = ...,
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
    "KmipServer",
    "KmipServerPayload",
    "KmipServerResponse",
    "KmipServerObject",
]