""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/h2qp_conn_capability
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

class H2qpConnCapabilityPayload(TypedDict, total=False):
    """Payload type for H2qpConnCapability operations."""
    name: str
    icmp_port: Literal["closed", "open", "unknown"]
    ftp_port: Literal["closed", "open", "unknown"]
    ssh_port: Literal["closed", "open", "unknown"]
    http_port: Literal["closed", "open", "unknown"]
    tls_port: Literal["closed", "open", "unknown"]
    pptp_vpn_port: Literal["closed", "open", "unknown"]
    voip_tcp_port: Literal["closed", "open", "unknown"]
    voip_udp_port: Literal["closed", "open", "unknown"]
    ikev2_port: Literal["closed", "open", "unknown"]
    ikev2_xx_port: Literal["closed", "open", "unknown"]
    esp_port: Literal["closed", "open", "unknown"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class H2qpConnCapabilityResponse(TypedDict, total=False):
    """Response type for H2qpConnCapability - use with .dict property for typed dict access."""
    name: str
    icmp_port: Literal["closed", "open", "unknown"]
    ftp_port: Literal["closed", "open", "unknown"]
    ssh_port: Literal["closed", "open", "unknown"]
    http_port: Literal["closed", "open", "unknown"]
    tls_port: Literal["closed", "open", "unknown"]
    pptp_vpn_port: Literal["closed", "open", "unknown"]
    voip_tcp_port: Literal["closed", "open", "unknown"]
    voip_udp_port: Literal["closed", "open", "unknown"]
    ikev2_port: Literal["closed", "open", "unknown"]
    ikev2_xx_port: Literal["closed", "open", "unknown"]
    esp_port: Literal["closed", "open", "unknown"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class H2qpConnCapabilityObject(FortiObject):
    """Typed FortiObject for H2qpConnCapability with field access."""
    name: str
    icmp_port: Literal["closed", "open", "unknown"]
    ftp_port: Literal["closed", "open", "unknown"]
    ssh_port: Literal["closed", "open", "unknown"]
    http_port: Literal["closed", "open", "unknown"]
    tls_port: Literal["closed", "open", "unknown"]
    pptp_vpn_port: Literal["closed", "open", "unknown"]
    voip_tcp_port: Literal["closed", "open", "unknown"]
    voip_udp_port: Literal["closed", "open", "unknown"]
    ikev2_port: Literal["closed", "open", "unknown"]
    ikev2_xx_port: Literal["closed", "open", "unknown"]
    esp_port: Literal["closed", "open", "unknown"]


# ================================================================
# Main Endpoint Class
# ================================================================

class H2qpConnCapability:
    """
    
    Endpoint: wireless_controller/hotspot20/h2qp_conn_capability
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
    ) -> H2qpConnCapabilityObject: ...
    
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
    ) -> FortiObjectList[H2qpConnCapabilityObject]: ...
    
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
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpConnCapabilityObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> H2qpConnCapabilityObject: ...

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
        payload_dict: H2qpConnCapabilityPayload | None = ...,
        name: str | None = ...,
        icmp_port: Literal["closed", "open", "unknown"] | None = ...,
        ftp_port: Literal["closed", "open", "unknown"] | None = ...,
        ssh_port: Literal["closed", "open", "unknown"] | None = ...,
        http_port: Literal["closed", "open", "unknown"] | None = ...,
        tls_port: Literal["closed", "open", "unknown"] | None = ...,
        pptp_vpn_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_tcp_port: Literal["closed", "open", "unknown"] | None = ...,
        voip_udp_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_port: Literal["closed", "open", "unknown"] | None = ...,
        ikev2_xx_port: Literal["closed", "open", "unknown"] | None = ...,
        esp_port: Literal["closed", "open", "unknown"] | None = ...,
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
    "H2qpConnCapability",
    "H2qpConnCapabilityPayload",
    "H2qpConnCapabilityResponse",
    "H2qpConnCapabilityObject",
]