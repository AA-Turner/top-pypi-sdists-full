""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wifi/client
Category: monitor
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

class ClientPayload(TypedDict, total=False):
    """Payload type for Client operations."""
    type: Literal["all", "fail-login"]
    with_triangulation: bool
    with_stats: bool
    mac: str


# ================================================================
# Response Types for Monitor/Log/Service Endpoints
# ================================================================

class ClientResponse(TypedDict, total=False):
    """Response type for Client - use with .dict property for typed dict access."""
    sta_maxrate: int
    sta_rxrate: int
    x11k_capable: bool
    x11v_capable: bool
    x11r_capable: bool
    sta_rxrate_mcs: int
    sta_rxrate_score: int
    sta_txrate: int
    sta_txrate_mcs: int
    sta_txrate_score: int
    sta_atf_val: int
    ip6: list[str]
    ip: str
    wtp_name: str
    wtp_id: str
    wtp_radio: int
    wtp_ip: str
    wtp_control_ip: str
    wtp_control_local_ip: str
    vap_name: str
    ssid: str
    user: str
    group: str
    mac: str
    os: str
    authentication: str
    uses_captive_portal: bool
    captive_portal_authenticated: int
    bytes_rx: int
    bytes_tx: int
    packets_rx: int
    packets_tx: int
    peak_bandwidth_bytes_rx: int
    peak_bandwidth_bytes_tx: int
    peak_bandwidth_packets_rx: int
    peak_bandwidth_packets_tx: int
    manufacturer: str
    data_rate_bps: int
    data_rxrate_bps: int
    data_txrate_bps: int
    snr: int
    idle_time: int
    association_time: int
    bandwidth_tx: int
    bandwidth_rx: int
    lan_authenticated: bool
    channel: int
    signal: int
    vci: str
    host: str
    security: int
    security_str: str
    encrypt: int
    noise: int
    radio_type: str
    mimo: str
    vlan_id: int
    tx_discard_percentage: int
    tx_retry_percentage: int
    mpsk_name: str
    triangulation_regions: list[str]
    health: str
    statistics: str


class ClientObject(FortiObject[ClientResponse]):
    """Typed FortiObject for Client with field access."""
    sta_maxrate: int
    sta_rxrate: int
    x11k_capable: bool
    x11v_capable: bool
    x11r_capable: bool
    sta_rxrate_mcs: int
    sta_rxrate_score: int
    sta_txrate: int
    sta_txrate_mcs: int
    sta_txrate_score: int
    sta_atf_val: int
    ip6: list[str]
    ip: str
    wtp_name: str
    wtp_id: str
    wtp_radio: int
    wtp_ip: str
    wtp_control_ip: str
    wtp_control_local_ip: str
    vap_name: str
    ssid: str
    user: str
    group: str
    mac: str
    os: str
    authentication: str
    uses_captive_portal: bool
    captive_portal_authenticated: int
    bytes_rx: int
    bytes_tx: int
    packets_rx: int
    packets_tx: int
    peak_bandwidth_bytes_rx: int
    peak_bandwidth_bytes_tx: int
    peak_bandwidth_packets_rx: int
    peak_bandwidth_packets_tx: int
    manufacturer: str
    data_rate_bps: int
    data_rxrate_bps: int
    data_txrate_bps: int
    snr: int
    idle_time: int
    association_time: int
    bandwidth_tx: int
    bandwidth_rx: int
    lan_authenticated: bool
    channel: int
    signal: int
    vci: str
    host: str
    security: int
    security_str: str
    encrypt: int
    noise: int
    radio_type: str
    mimo: str
    vlan_id: int
    tx_discard_percentage: int
    tx_retry_percentage: int
    mpsk_name: str
    triangulation_regions: list[str]
    health: str
    statistics: str



# ================================================================
# Main Endpoint Class
# ================================================================

class Client:
    """
    
    Endpoint: wifi/client
    Category: monitor
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
    
    # Service/Monitor endpoint
    def get(
        self,
        *,
        type: Literal["all", "fail-login"] | None = ...,
        with_triangulation: bool | None = ...,
        with_stats: bool | None = ...,
        mac: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[ClientObject]: ...
    


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ClientPayload | None = ...,
        type: Literal["all", "fail-login"] | None = ...,
        with_triangulation: bool | None = ...,
        with_stats: bool | None = ...,
        mac: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ClientObject: ...




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
        payload_dict: ClientPayload | None = ...,
        type: Literal["all", "fail-login"] | None = ...,
        with_triangulation: bool | None = ...,
        with_stats: bool | None = ...,
        mac: str | None = ...,
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
    "Client",
    "ClientResponse",
    "ClientObject",
]