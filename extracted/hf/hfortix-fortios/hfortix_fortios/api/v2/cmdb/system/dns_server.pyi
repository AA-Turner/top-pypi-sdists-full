""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/dns_server
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

class DnsServerPayload(TypedDict, total=False):
    """Payload type for DnsServer operations."""
    name: str
    mode: Literal["recursive", "non-recursive", "forward-only", "resolver"]
    dnsfilter_profile: str
    doh: Literal["enable", "disable"]
    doh3: Literal["enable", "disable"]
    doq: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class DnsServerResponse(TypedDict, total=False):
    """Response type for DnsServer - use with .dict property for typed dict access."""
    name: str
    mode: Literal["recursive", "non-recursive", "forward-only", "resolver"]
    dnsfilter_profile: str
    doh: Literal["enable", "disable"]
    doh3: Literal["enable", "disable"]
    doq: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class DnsServerObject(FortiObject):
    """Typed FortiObject for DnsServer with field access."""
    name: str
    mode: Literal["recursive", "non-recursive", "forward-only", "resolver"]
    dnsfilter_profile: str
    doh: Literal["enable", "disable"]
    doh3: Literal["enable", "disable"]
    doq: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class DnsServer:
    """
    
    Endpoint: system/dns_server
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
    ) -> DnsServerObject: ...
    
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
    ) -> FortiObjectList[DnsServerObject]: ...
    
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
        payload_dict: DnsServerPayload | None = ...,
        name: str | None = ...,
        mode: Literal["recursive", "non-recursive", "forward-only", "resolver"] | None = ...,
        dnsfilter_profile: str | None = ...,
        doh: Literal["enable", "disable"] | None = ...,
        doh3: Literal["enable", "disable"] | None = ...,
        doq: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DnsServerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: DnsServerPayload | None = ...,
        name: str | None = ...,
        mode: Literal["recursive", "non-recursive", "forward-only", "resolver"] | None = ...,
        dnsfilter_profile: str | None = ...,
        doh: Literal["enable", "disable"] | None = ...,
        doh3: Literal["enable", "disable"] | None = ...,
        doq: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> DnsServerObject: ...

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
        payload_dict: DnsServerPayload | None = ...,
        name: str | None = ...,
        mode: Literal["recursive", "non-recursive", "forward-only", "resolver"] | None = ...,
        dnsfilter_profile: str | None = ...,
        doh: Literal["enable", "disable"] | None = ...,
        doh3: Literal["enable", "disable"] | None = ...,
        doq: Literal["enable", "disable"] | None = ...,
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
    "DnsServer",
    "DnsServerPayload",
    "DnsServerResponse",
    "DnsServerObject",
]