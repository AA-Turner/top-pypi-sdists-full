""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: web_proxy/isolator_server
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

class IsolatorServerPayload(TypedDict, total=False):
    """Payload type for IsolatorServer operations."""
    name: str
    addr_type: Literal["ip", "ipv6", "fqdn"]
    ip: str
    ipv6: str
    fqdn: str
    port: int
    interface_select_method: Literal["sdwan", "specify"]
    interface: str
    vrf_select: int
    comment: str
    masquerade: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class IsolatorServerResponse(TypedDict, total=False):
    """Response type for IsolatorServer - use with .dict property for typed dict access."""
    name: str
    addr_type: Literal["ip", "ipv6", "fqdn"]
    ip: str
    ipv6: str
    fqdn: str
    port: int
    interface_select_method: Literal["sdwan", "specify"]
    interface: str
    vrf_select: int
    comment: str
    masquerade: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class IsolatorServerObject(FortiObject):
    """Typed FortiObject for IsolatorServer with field access."""
    name: str
    addr_type: Literal["ip", "ipv6", "fqdn"]
    ip: str
    ipv6: str
    fqdn: str
    port: int
    interface_select_method: Literal["sdwan", "specify"]
    interface: str
    vrf_select: int
    comment: str
    masquerade: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class IsolatorServer:
    """
    
    Endpoint: web_proxy/isolator_server
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
    ) -> IsolatorServerObject: ...
    
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
    ) -> FortiObjectList[IsolatorServerObject]: ...
    
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
        payload_dict: IsolatorServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip", "ipv6", "fqdn"] | None = ...,
        ip: str | None = ...,
        ipv6: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        interface_select_method: Literal["sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        comment: str | None = ...,
        masquerade: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IsolatorServerObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: IsolatorServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip", "ipv6", "fqdn"] | None = ...,
        ip: str | None = ...,
        ipv6: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        interface_select_method: Literal["sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        comment: str | None = ...,
        masquerade: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> IsolatorServerObject: ...

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
        payload_dict: IsolatorServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip", "ipv6", "fqdn"] | None = ...,
        ip: str | None = ...,
        ipv6: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        interface_select_method: Literal["sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        comment: str | None = ...,
        masquerade: Literal["enable", "disable"] | None = ...,
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
    "IsolatorServer",
    "IsolatorServerPayload",
    "IsolatorServerResponse",
    "IsolatorServerObject",
]