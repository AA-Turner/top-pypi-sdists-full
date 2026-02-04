""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: user/fsso
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

class FssoPayload(TypedDict, total=False):
    """Payload type for Fsso operations."""
    name: str
    type: Literal["default", "fortinac"]
    server: str
    port: int
    password: str
    server2: str
    port2: int
    password2: str
    server3: str
    port3: int
    password3: str
    server4: str
    port4: int
    password4: str
    server5: str
    port5: int
    password5: str
    logon_timeout: int
    ldap_server: str
    group_poll_interval: int
    ldap_poll: Literal["enable", "disable"]
    ldap_poll_interval: int
    ldap_poll_filter: str
    user_info_server: str
    ssl: Literal["enable", "disable"]
    sni: str
    ssl_server_host_ip_check: Literal["enable", "disable"]
    ssl_trusted_cert: str
    source_ip: str
    source_ip6: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FssoResponse(TypedDict, total=False):
    """Response type for Fsso - use with .dict property for typed dict access."""
    name: str
    type: Literal["default", "fortinac"]
    server: str
    port: int
    password: str
    server2: str
    port2: int
    password2: str
    server3: str
    port3: int
    password3: str
    server4: str
    port4: int
    password4: str
    server5: str
    port5: int
    password5: str
    logon_timeout: int
    ldap_server: str
    group_poll_interval: int
    ldap_poll: Literal["enable", "disable"]
    ldap_poll_interval: int
    ldap_poll_filter: str
    user_info_server: str
    ssl: Literal["enable", "disable"]
    sni: str
    ssl_server_host_ip_check: Literal["enable", "disable"]
    ssl_trusted_cert: str
    source_ip: str
    source_ip6: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FssoObject(FortiObject):
    """Typed FortiObject for Fsso with field access."""
    name: str
    type: Literal["default", "fortinac"]
    server: str
    port: int
    password: str
    server2: str
    port2: int
    password2: str
    server3: str
    port3: int
    password3: str
    server4: str
    port4: int
    password4: str
    server5: str
    port5: int
    password5: str
    logon_timeout: int
    ldap_server: str
    group_poll_interval: int
    ldap_poll: Literal["enable", "disable"]
    ldap_poll_interval: int
    ldap_poll_filter: str
    user_info_server: str
    ssl: Literal["enable", "disable"]
    sni: str
    ssl_server_host_ip_check: Literal["enable", "disable"]
    ssl_trusted_cert: str
    source_ip: str
    source_ip6: str
    interface_select_method: Literal["auto", "sdwan", "specify"]
    interface: str
    vrf_select: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Fsso:
    """
    
    Endpoint: user/fsso
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
    ) -> FssoObject: ...
    
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
    ) -> FortiObjectList[FssoObject]: ...
    
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
        payload_dict: FssoPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "fortinac"] | None = ...,
        server: str | None = ...,
        port: int | None = ...,
        password: str | None = ...,
        server2: str | None = ...,
        port2: int | None = ...,
        password2: str | None = ...,
        server3: str | None = ...,
        port3: int | None = ...,
        password3: str | None = ...,
        server4: str | None = ...,
        port4: int | None = ...,
        password4: str | None = ...,
        server5: str | None = ...,
        port5: int | None = ...,
        password5: str | None = ...,
        logon_timeout: int | None = ...,
        ldap_server: str | None = ...,
        group_poll_interval: int | None = ...,
        ldap_poll: Literal["enable", "disable"] | None = ...,
        ldap_poll_interval: int | None = ...,
        ldap_poll_filter: str | None = ...,
        user_info_server: str | None = ...,
        ssl: Literal["enable", "disable"] | None = ...,
        sni: str | None = ...,
        ssl_server_host_ip_check: Literal["enable", "disable"] | None = ...,
        ssl_trusted_cert: str | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FssoObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FssoPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "fortinac"] | None = ...,
        server: str | None = ...,
        port: int | None = ...,
        password: str | None = ...,
        server2: str | None = ...,
        port2: int | None = ...,
        password2: str | None = ...,
        server3: str | None = ...,
        port3: int | None = ...,
        password3: str | None = ...,
        server4: str | None = ...,
        port4: int | None = ...,
        password4: str | None = ...,
        server5: str | None = ...,
        port5: int | None = ...,
        password5: str | None = ...,
        logon_timeout: int | None = ...,
        ldap_server: str | None = ...,
        group_poll_interval: int | None = ...,
        ldap_poll: Literal["enable", "disable"] | None = ...,
        ldap_poll_interval: int | None = ...,
        ldap_poll_filter: str | None = ...,
        user_info_server: str | None = ...,
        ssl: Literal["enable", "disable"] | None = ...,
        sni: str | None = ...,
        ssl_server_host_ip_check: Literal["enable", "disable"] | None = ...,
        ssl_trusted_cert: str | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FssoObject: ...

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
        payload_dict: FssoPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "fortinac"] | None = ...,
        server: str | None = ...,
        port: int | None = ...,
        password: str | None = ...,
        server2: str | None = ...,
        port2: int | None = ...,
        password2: str | None = ...,
        server3: str | None = ...,
        port3: int | None = ...,
        password3: str | None = ...,
        server4: str | None = ...,
        port4: int | None = ...,
        password4: str | None = ...,
        server5: str | None = ...,
        port5: int | None = ...,
        password5: str | None = ...,
        logon_timeout: int | None = ...,
        ldap_server: str | None = ...,
        group_poll_interval: int | None = ...,
        ldap_poll: Literal["enable", "disable"] | None = ...,
        ldap_poll_interval: int | None = ...,
        ldap_poll_filter: str | None = ...,
        user_info_server: str | None = ...,
        ssl: Literal["enable", "disable"] | None = ...,
        sni: str | None = ...,
        ssl_server_host_ip_check: Literal["enable", "disable"] | None = ...,
        ssl_trusted_cert: str | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
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
    "Fsso",
    "FssoPayload",
    "FssoResponse",
    "FssoObject",
]