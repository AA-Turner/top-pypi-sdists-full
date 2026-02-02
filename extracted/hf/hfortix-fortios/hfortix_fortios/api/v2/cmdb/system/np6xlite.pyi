""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/np6xlite
Category: cmdb
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

class Np6xliteHpeItem(TypedDict, total=False):
    """Nested item for hpe field."""
    tcpsyn_max: int
    tcpsyn_ack_max: int
    tcpfin_rst_max: int
    tcp_others_max: int
    udp_max: int
    icmp_max: int
    sctp_max: int
    esp_max: int
    ip_frag_max: int
    ip_others_max: int
    arp_max: int
    l2_others_max: int
    pri_type_max: int
    enable_shaper: Literal["disable", "enable"]


class Np6xliteFpanomalyItem(TypedDict, total=False):
    """Nested item for fp-anomaly field."""
    tcp_syn_fin: Literal["allow", "drop", "trap-to-host"]
    tcp_fin_noack: Literal["allow", "drop", "trap-to-host"]
    tcp_fin_only: Literal["allow", "drop", "trap-to-host"]
    tcp_no_flag: Literal["allow", "drop", "trap-to-host"]
    tcp_syn_data: Literal["allow", "drop", "trap-to-host"]
    tcp_winnuke: Literal["allow", "drop", "trap-to-host"]
    tcp_land: Literal["allow", "drop", "trap-to-host"]
    udp_land: Literal["allow", "drop", "trap-to-host"]
    icmp_land: Literal["allow", "drop", "trap-to-host"]
    icmp_frag: Literal["allow", "drop", "trap-to-host"]
    ipv4_land: Literal["allow", "drop", "trap-to-host"]
    ipv4_proto_err: Literal["allow", "drop", "trap-to-host"]
    ipv4_unknopt: Literal["allow", "drop", "trap-to-host"]
    ipv4_optrr: Literal["allow", "drop", "trap-to-host"]
    ipv4_optssrr: Literal["allow", "drop", "trap-to-host"]
    ipv4_optlsrr: Literal["allow", "drop", "trap-to-host"]
    ipv4_optstream: Literal["allow", "drop", "trap-to-host"]
    ipv4_optsecurity: Literal["allow", "drop", "trap-to-host"]
    ipv4_opttimestamp: Literal["allow", "drop", "trap-to-host"]
    ipv4_csum_err: Literal["drop", "trap-to-host"]
    tcp_csum_err: Literal["drop", "trap-to-host"]
    udp_csum_err: Literal["drop", "trap-to-host"]
    icmp_csum_err: Literal["drop", "trap-to-host"]
    ipv6_land: Literal["allow", "drop", "trap-to-host"]
    ipv6_proto_err: Literal["allow", "drop", "trap-to-host"]
    ipv6_unknopt: Literal["allow", "drop", "trap-to-host"]
    ipv6_saddr_err: Literal["allow", "drop", "trap-to-host"]
    ipv6_daddr_err: Literal["allow", "drop", "trap-to-host"]
    ipv6_optralert: Literal["allow", "drop", "trap-to-host"]
    ipv6_optjumbo: Literal["allow", "drop", "trap-to-host"]
    ipv6_opttunnel: Literal["allow", "drop", "trap-to-host"]
    ipv6_opthomeaddr: Literal["allow", "drop", "trap-to-host"]
    ipv6_optnsap: Literal["allow", "drop", "trap-to-host"]
    ipv6_optendpid: Literal["allow", "drop", "trap-to-host"]
    ipv6_optinvld: Literal["allow", "drop", "trap-to-host"]


class Np6xlitePayload(TypedDict, total=False):
    """Payload type for Np6xlite operations."""
    name: str
    fastpath: Literal["disable", "enable"]
    per_session_accounting: Literal["disable", "traffic-log-only", "enable"]
    session_timeout_interval: int
    ipsec_inner_fragment: Literal["disable", "enable"]
    ipsec_throughput_msg_frequency: Literal["disable", "32kb", "64kb", "128kb", "256kb", "512kb", "1mb", "2mb", "4mb", "8mb", "16mb", "32mb", "64mb", "128mb", "256mb", "512mb", "1gb"]
    ipsec_sts_timeout: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    hpe: str | list[str] | list[Np6xliteHpeItem]
    fp_anomaly: str | list[str] | list[Np6xliteFpanomalyItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class Np6xliteResponse(TypedDict, total=False):
    """Response type for Np6xlite - use with .dict property for typed dict access."""
    name: str
    fastpath: Literal["disable", "enable"]
    per_session_accounting: Literal["disable", "traffic-log-only", "enable"]
    session_timeout_interval: int
    ipsec_inner_fragment: Literal["disable", "enable"]
    ipsec_throughput_msg_frequency: Literal["disable", "32kb", "64kb", "128kb", "256kb", "512kb", "1mb", "2mb", "4mb", "8mb", "16mb", "32mb", "64mb", "128mb", "256mb", "512mb", "1gb"]
    ipsec_sts_timeout: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    hpe: list[Np6xliteHpeItem]
    fp_anomaly: list[Np6xliteFpanomalyItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class Np6xliteHpeItemObject(FortiObject[Np6xliteHpeItem]):
    """Typed object for hpe table items with attribute access."""
    tcpsyn_max: int
    tcpsyn_ack_max: int
    tcpfin_rst_max: int
    tcp_others_max: int
    udp_max: int
    icmp_max: int
    sctp_max: int
    esp_max: int
    ip_frag_max: int
    ip_others_max: int
    arp_max: int
    l2_others_max: int
    pri_type_max: int
    enable_shaper: Literal["disable", "enable"]


class Np6xliteFpanomalyItemObject(FortiObject[Np6xliteFpanomalyItem]):
    """Typed object for fp-anomaly table items with attribute access."""
    tcp_syn_fin: Literal["allow", "drop", "trap-to-host"]
    tcp_fin_noack: Literal["allow", "drop", "trap-to-host"]
    tcp_fin_only: Literal["allow", "drop", "trap-to-host"]
    tcp_no_flag: Literal["allow", "drop", "trap-to-host"]
    tcp_syn_data: Literal["allow", "drop", "trap-to-host"]
    tcp_winnuke: Literal["allow", "drop", "trap-to-host"]
    tcp_land: Literal["allow", "drop", "trap-to-host"]
    udp_land: Literal["allow", "drop", "trap-to-host"]
    icmp_land: Literal["allow", "drop", "trap-to-host"]
    icmp_frag: Literal["allow", "drop", "trap-to-host"]
    ipv4_land: Literal["allow", "drop", "trap-to-host"]
    ipv4_proto_err: Literal["allow", "drop", "trap-to-host"]
    ipv4_unknopt: Literal["allow", "drop", "trap-to-host"]
    ipv4_optrr: Literal["allow", "drop", "trap-to-host"]
    ipv4_optssrr: Literal["allow", "drop", "trap-to-host"]
    ipv4_optlsrr: Literal["allow", "drop", "trap-to-host"]
    ipv4_optstream: Literal["allow", "drop", "trap-to-host"]
    ipv4_optsecurity: Literal["allow", "drop", "trap-to-host"]
    ipv4_opttimestamp: Literal["allow", "drop", "trap-to-host"]
    ipv4_csum_err: Literal["drop", "trap-to-host"]
    tcp_csum_err: Literal["drop", "trap-to-host"]
    udp_csum_err: Literal["drop", "trap-to-host"]
    icmp_csum_err: Literal["drop", "trap-to-host"]
    ipv6_land: Literal["allow", "drop", "trap-to-host"]
    ipv6_proto_err: Literal["allow", "drop", "trap-to-host"]
    ipv6_unknopt: Literal["allow", "drop", "trap-to-host"]
    ipv6_saddr_err: Literal["allow", "drop", "trap-to-host"]
    ipv6_daddr_err: Literal["allow", "drop", "trap-to-host"]
    ipv6_optralert: Literal["allow", "drop", "trap-to-host"]
    ipv6_optjumbo: Literal["allow", "drop", "trap-to-host"]
    ipv6_opttunnel: Literal["allow", "drop", "trap-to-host"]
    ipv6_opthomeaddr: Literal["allow", "drop", "trap-to-host"]
    ipv6_optnsap: Literal["allow", "drop", "trap-to-host"]
    ipv6_optendpid: Literal["allow", "drop", "trap-to-host"]
    ipv6_optinvld: Literal["allow", "drop", "trap-to-host"]


class Np6xliteObject(FortiObject):
    """Typed FortiObject for Np6xlite with field access."""
    name: str
    fastpath: Literal["disable", "enable"]
    per_session_accounting: Literal["disable", "traffic-log-only", "enable"]
    session_timeout_interval: int
    ipsec_inner_fragment: Literal["disable", "enable"]
    ipsec_throughput_msg_frequency: Literal["disable", "32kb", "64kb", "128kb", "256kb", "512kb", "1mb", "2mb", "4mb", "8mb", "16mb", "32mb", "64mb", "128mb", "256mb", "512mb", "1gb"]
    ipsec_sts_timeout: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    hpe: FortiObjectList[Np6xliteHpeItemObject]
    fp_anomaly: FortiObjectList[Np6xliteFpanomalyItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Np6xlite:
    """
    
    Endpoint: system/np6xlite
    Category: cmdb
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
    
    # Singleton endpoint (no mkey)
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
    ) -> Np6xliteObject: ...
    
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
        payload_dict: Np6xlitePayload | None = ...,
        name: str | None = ...,
        fastpath: Literal["disable", "enable"] | None = ...,
        per_session_accounting: Literal["disable", "traffic-log-only", "enable"] | None = ...,
        session_timeout_interval: int | None = ...,
        ipsec_inner_fragment: Literal["disable", "enable"] | None = ...,
        ipsec_throughput_msg_frequency: Literal["disable", "32kb", "64kb", "128kb", "256kb", "512kb", "1mb", "2mb", "4mb", "8mb", "16mb", "32mb", "64mb", "128mb", "256mb", "512mb", "1gb"] | None = ...,
        ipsec_sts_timeout: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] | None = ...,
        hpe: str | list[str] | list[Np6xliteHpeItem] | None = ...,
        fp_anomaly: str | list[str] | list[Np6xliteFpanomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Np6xliteObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: Np6xlitePayload | None = ...,
        name: str | None = ...,
        fastpath: Literal["disable", "enable"] | None = ...,
        per_session_accounting: Literal["disable", "traffic-log-only", "enable"] | None = ...,
        session_timeout_interval: int | None = ...,
        ipsec_inner_fragment: Literal["disable", "enable"] | None = ...,
        ipsec_throughput_msg_frequency: Literal["disable", "32kb", "64kb", "128kb", "256kb", "512kb", "1mb", "2mb", "4mb", "8mb", "16mb", "32mb", "64mb", "128mb", "256mb", "512mb", "1gb"] | None = ...,
        ipsec_sts_timeout: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] | None = ...,
        hpe: str | list[str] | list[Np6xliteHpeItem] | None = ...,
        fp_anomaly: str | list[str] | list[Np6xliteFpanomalyItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> Np6xliteObject: ...

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
        payload_dict: Np6xlitePayload | None = ...,
        name: str | None = ...,
        fastpath: Literal["disable", "enable"] | None = ...,
        per_session_accounting: Literal["disable", "traffic-log-only", "enable"] | None = ...,
        session_timeout_interval: int | None = ...,
        ipsec_inner_fragment: Literal["disable", "enable"] | None = ...,
        ipsec_throughput_msg_frequency: Literal["disable", "32kb", "64kb", "128kb", "256kb", "512kb", "1mb", "2mb", "4mb", "8mb", "16mb", "32mb", "64mb", "128mb", "256mb", "512mb", "1gb"] | None = ...,
        ipsec_sts_timeout: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] | None = ...,
        hpe: str | list[str] | list[Np6xliteHpeItem] | None = ...,
        fp_anomaly: str | list[str] | list[Np6xliteFpanomalyItem] | None = ...,
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
    "Np6xlite",
    "Np6xlitePayload",
    "Np6xliteResponse",
    "Np6xliteObject",
]