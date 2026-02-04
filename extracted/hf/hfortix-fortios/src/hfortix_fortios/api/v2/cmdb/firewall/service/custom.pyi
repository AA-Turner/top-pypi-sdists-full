""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/service/custom
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

class CustomAppcategoryItem(TypedDict, total=False):
    """Nested item for app-category field."""
    id: int


class CustomApplicationItem(TypedDict, total=False):
    """Nested item for application field."""
    id: int


class CustomPayload(TypedDict, total=False):
    """Payload type for Custom operations."""
    name: str
    uuid: str
    proxy: Literal["enable", "disable"]
    category: str
    protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"]
    helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"]
    iprange: str
    fqdn: str
    protocol_number: int
    icmptype: int
    icmpcode: int
    tcp_portrange: str
    udp_portrange: str
    udplite_portrange: str
    sctp_portrange: str
    tcp_halfclose_timer: int
    tcp_halfopen_timer: int
    tcp_timewait_timer: int
    tcp_rst_timer: int
    udp_idle_timer: int
    session_ttl: str
    check_reset_range: Literal["disable", "strict", "default"]
    comment: str
    color: int
    app_service_type: Literal["disable", "app-id", "app-category"]
    app_category: str | list[str] | list[CustomAppcategoryItem]
    application: str | list[str] | list[CustomApplicationItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class CustomResponse(TypedDict, total=False):
    """Response type for Custom - use with .dict property for typed dict access."""
    name: str
    uuid: str
    proxy: Literal["enable", "disable"]
    category: str
    protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"]
    helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"]
    iprange: str
    fqdn: str
    protocol_number: int
    icmptype: int
    icmpcode: int
    tcp_portrange: str
    udp_portrange: str
    udplite_portrange: str
    sctp_portrange: str
    tcp_halfclose_timer: int
    tcp_halfopen_timer: int
    tcp_timewait_timer: int
    tcp_rst_timer: int
    udp_idle_timer: int
    session_ttl: str
    check_reset_range: Literal["disable", "strict", "default"]
    comment: str
    color: int
    app_service_type: Literal["disable", "app-id", "app-category"]
    app_category: list[CustomAppcategoryItem]
    application: list[CustomApplicationItem]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class CustomAppcategoryItemObject(FortiObject[CustomAppcategoryItem]):
    """Typed object for app-category table items with attribute access."""
    id: int


class CustomApplicationItemObject(FortiObject[CustomApplicationItem]):
    """Typed object for application table items with attribute access."""
    id: int


class CustomObject(FortiObject):
    """Typed FortiObject for Custom with field access."""
    name: str
    uuid: str
    proxy: Literal["enable", "disable"]
    category: str
    protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"]
    helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"]
    iprange: str
    fqdn: str
    protocol_number: int
    icmptype: int
    icmpcode: int
    tcp_portrange: str
    udp_portrange: str
    udplite_portrange: str
    sctp_portrange: str
    tcp_halfclose_timer: int
    tcp_halfopen_timer: int
    tcp_timewait_timer: int
    tcp_rst_timer: int
    udp_idle_timer: int
    session_ttl: str
    check_reset_range: Literal["disable", "strict", "default"]
    comment: str
    color: int
    app_service_type: Literal["disable", "app-id", "app-category"]
    app_category: FortiObjectList[CustomAppcategoryItemObject]
    application: FortiObjectList[CustomApplicationItemObject]
    fabric_object: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Custom:
    """
    
    Endpoint: firewall/service/custom
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
    ) -> CustomObject: ...
    
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
    ) -> FortiObjectList[CustomObject]: ...
    
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
        payload_dict: CustomPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        proxy: Literal["enable", "disable"] | None = ...,
        category: str | None = ...,
        protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"] | None = ...,
        helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"] | None = ...,
        iprange: str | None = ...,
        fqdn: str | None = ...,
        protocol_number: int | None = ...,
        icmptype: int | None = ...,
        icmpcode: int | None = ...,
        tcp_portrange: str | None = ...,
        udp_portrange: str | None = ...,
        udplite_portrange: str | None = ...,
        sctp_portrange: str | None = ...,
        tcp_halfclose_timer: int | None = ...,
        tcp_halfopen_timer: int | None = ...,
        tcp_timewait_timer: int | None = ...,
        tcp_rst_timer: int | None = ...,
        udp_idle_timer: int | None = ...,
        session_ttl: str | None = ...,
        check_reset_range: Literal["disable", "strict", "default"] | None = ...,
        comment: str | None = ...,
        color: int | None = ...,
        app_service_type: Literal["disable", "app-id", "app-category"] | None = ...,
        app_category: str | list[str] | list[CustomAppcategoryItem] | None = ...,
        application: str | list[str] | list[CustomApplicationItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CustomObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: CustomPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        proxy: Literal["enable", "disable"] | None = ...,
        category: str | None = ...,
        protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"] | None = ...,
        helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"] | None = ...,
        iprange: str | None = ...,
        fqdn: str | None = ...,
        protocol_number: int | None = ...,
        icmptype: int | None = ...,
        icmpcode: int | None = ...,
        tcp_portrange: str | None = ...,
        udp_portrange: str | None = ...,
        udplite_portrange: str | None = ...,
        sctp_portrange: str | None = ...,
        tcp_halfclose_timer: int | None = ...,
        tcp_halfopen_timer: int | None = ...,
        tcp_timewait_timer: int | None = ...,
        tcp_rst_timer: int | None = ...,
        udp_idle_timer: int | None = ...,
        session_ttl: str | None = ...,
        check_reset_range: Literal["disable", "strict", "default"] | None = ...,
        comment: str | None = ...,
        color: int | None = ...,
        app_service_type: Literal["disable", "app-id", "app-category"] | None = ...,
        app_category: str | list[str] | list[CustomAppcategoryItem] | None = ...,
        application: str | list[str] | list[CustomApplicationItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> CustomObject: ...

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
        payload_dict: CustomPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        proxy: Literal["enable", "disable"] | None = ...,
        category: str | None = ...,
        protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"] | None = ...,
        helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"] | None = ...,
        iprange: str | None = ...,
        fqdn: str | None = ...,
        protocol_number: int | None = ...,
        icmptype: int | None = ...,
        icmpcode: int | None = ...,
        tcp_portrange: str | None = ...,
        udp_portrange: str | None = ...,
        udplite_portrange: str | None = ...,
        sctp_portrange: str | None = ...,
        tcp_halfclose_timer: int | None = ...,
        tcp_halfopen_timer: int | None = ...,
        tcp_timewait_timer: int | None = ...,
        tcp_rst_timer: int | None = ...,
        udp_idle_timer: int | None = ...,
        session_ttl: str | None = ...,
        check_reset_range: Literal["disable", "strict", "default"] | None = ...,
        comment: str | None = ...,
        color: int | None = ...,
        app_service_type: Literal["disable", "app-id", "app-category"] | None = ...,
        app_category: str | list[str] | list[CustomAppcategoryItem] | None = ...,
        application: str | list[str] | list[CustomApplicationItem] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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
    "Custom",
    "CustomPayload",
    "CustomResponse",
    "CustomObject",
]