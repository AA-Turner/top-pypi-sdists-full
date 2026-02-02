""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/pppoe_interface
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

class PppoeInterfacePayload(TypedDict, total=False):
    """Payload type for PppoeInterface operations."""
    name: str
    dial_on_demand: Literal["enable", "disable"]
    ipv6: Literal["enable", "disable"]
    device: str
    username: str
    password: str
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    ipunnumbered: str
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]
    idle_timeout: int
    multilink: Literal["enable", "disable"]
    mrru: int
    disc_retry_timeout: int
    padt_retry_timeout: int
    service_name: str
    ac_name: str
    lcp_echo_interval: int
    lcp_max_echo_fails: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class PppoeInterfaceResponse(TypedDict, total=False):
    """Response type for PppoeInterface - use with .dict property for typed dict access."""
    name: str
    dial_on_demand: Literal["enable", "disable"]
    ipv6: Literal["enable", "disable"]
    device: str
    username: str
    password: str
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    ipunnumbered: str
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]
    idle_timeout: int
    multilink: Literal["enable", "disable"]
    mrru: int
    disc_retry_timeout: int
    padt_retry_timeout: int
    service_name: str
    ac_name: str
    lcp_echo_interval: int
    lcp_max_echo_fails: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class PppoeInterfaceObject(FortiObject):
    """Typed FortiObject for PppoeInterface with field access."""
    name: str
    dial_on_demand: Literal["enable", "disable"]
    ipv6: Literal["enable", "disable"]
    device: str
    username: str
    password: str
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    ipunnumbered: str
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]
    idle_timeout: int
    multilink: Literal["enable", "disable"]
    mrru: int
    disc_retry_timeout: int
    padt_retry_timeout: int
    service_name: str
    ac_name: str
    lcp_echo_interval: int
    lcp_max_echo_fails: int


# ================================================================
# Main Endpoint Class
# ================================================================

class PppoeInterface:
    """
    
    Endpoint: system/pppoe_interface
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
    ) -> PppoeInterfaceObject: ...
    
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
    ) -> FortiObjectList[PppoeInterfaceObject]: ...
    
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
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PppoeInterfaceObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> PppoeInterfaceObject: ...

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
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
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
    "PppoeInterface",
    "PppoeInterfacePayload",
    "PppoeInterfaceResponse",
    "PppoeInterfaceObject",
]