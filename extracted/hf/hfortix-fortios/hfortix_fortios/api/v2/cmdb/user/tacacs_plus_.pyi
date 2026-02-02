""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/tacacs_plus_
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

class TacacsPlusPayload(TypedDict, total=False):
    """Payload type for TacacsPlus operations."""
    name: str
    server: str
    secondary_server: str
    tertiary_server: str
    port: int
    key: str
    secondary_key: str
    tertiary_key: str
    status_ttl: int
    authen_type: Literal["mschap", "chap", "pap", "ascii", "auto"]
    authorization: Literal["enable", "disable"]
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class TacacsPlusResponse(TypedDict, total=False):
    """Response type for TacacsPlus - use with .dict property for typed dict access."""
    name: str
    server: str
    secondary_server: str
    tertiary_server: str
    port: int
    key: str
    secondary_key: str
    tertiary_key: str
    status_ttl: int
    authen_type: Literal["mschap", "chap", "pap", "ascii", "auto"]
    authorization: Literal["enable", "disable"]
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class TacacsPlusObject(FortiObject):
    """Typed FortiObject for TacacsPlus with field access."""
    name: str
    server: str
    secondary_server: str
    tertiary_server: str
    port: int
    key: str
    secondary_key: str
    tertiary_key: str
    status_ttl: int
    authen_type: Literal["mschap", "chap", "pap", "ascii", "auto"]
    authorization: Literal["enable", "disable"]
    source_ip: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class TacacsPlus:
    """
    
    Endpoint: user/tacacs_plus_
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
    ) -> TacacsPlusObject: ...
    
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
    ) -> FortiObjectList[TacacsPlusObject]: ...
    
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
        payload_dict: TacacsPlusPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        port: int | None = ...,
        key: str | None = ...,
        secondary_key: str | None = ...,
        tertiary_key: str | None = ...,
        status_ttl: int | None = ...,
        authen_type: Literal["mschap", "chap", "pap", "ascii", "auto"] | None = ...,
        authorization: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TacacsPlusObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: TacacsPlusPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        port: int | None = ...,
        key: str | None = ...,
        secondary_key: str | None = ...,
        tertiary_key: str | None = ...,
        status_ttl: int | None = ...,
        authen_type: Literal["mschap", "chap", "pap", "ascii", "auto"] | None = ...,
        authorization: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> TacacsPlusObject: ...

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
        payload_dict: TacacsPlusPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        port: int | None = ...,
        key: str | None = ...,
        secondary_key: str | None = ...,
        tertiary_key: str | None = ...,
        status_ttl: int | None = ...,
        authen_type: Literal["mschap", "chap", "pap", "ascii", "auto"] | None = ...,
        authorization: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
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
    "TacacsPlus",
    "TacacsPlusPayload",
    "TacacsPlusResponse",
    "TacacsPlusObject",
]