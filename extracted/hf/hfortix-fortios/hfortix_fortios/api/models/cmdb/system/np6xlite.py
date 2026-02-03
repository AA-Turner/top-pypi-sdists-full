"""
Pydantic Models for CMDB - system/np6xlite

Runtime validation models for system/np6xlite configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class Np6xliteHpe(BaseModel):
    """
    Child table model for hpe.
    
    HPE configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    tcpsyn_max: int | None = Field(default=None, description="Maximum TCP SYN only packet rate (1K - 1G pps, default = 600K pps).")    
    tcpsyn_ack_max: int | None = Field(default=None, description="Maximum TCP carries SYN and ACK flags packet rate (1K - 1G pps, default = 600K pps).")    
    tcpfin_rst_max: int | None = Field(default=None, description="Maximum TCP carries FIN or RST flags packet rate (1K - 1G pps, default = 600K pps).")    
    tcp_others_max: int | None = Field(default=None, description="Maximum TCP packet rate for TCP packets that match none of the 3 types above (1K - 1G pps, default = 600K pps).")    
    udp_max: int | None = Field(default=None, description="Maximum UDP packet rate (1K - 1G pps, default = 600K pps).")    
    icmp_max: int | None = Field(default=None, description="Maximum ICMP packet rate (1K - 1G pps, default = 200K pps).")    
    sctp_max: int | None = Field(default=None, description="Maximum SCTP packet rate (1K - 1G pps, default = 200K pps).")    
    esp_max: int | None = Field(default=None, description="Maximum ESP packet rate (1K - 1G pps, default = 200K pps).")    
    ip_frag_max: int | None = Field(default=None, description="Maximum fragmented IP packet rate (1K - 1G pps, default = 200K pps).")    
    ip_others_max: int | None = Field(default=None, description="Maximum IP packet rate for other packets (packet types that cannot be set with other options) (1K - 1G pps, default = 200K pps).")    
    arp_max: int | None = Field(default=None, description="Maximum ARP packet rate (1K - 1G pps, default = 200K pps).")    
    l2_others_max: int | None = Field(default=None, description="Maximum L2 packet rate for L2 packets that are not ARP packets (1K - 1G pps, default = 200K pps).")    
    pri_type_max: int | None = Field(default=None, description="Maximum overflow rate of priority type traffic (1K - 1G pps, default = 200K pps). Includes L2: HA, 802.3ad LACP, heartbeats. L3: OSPF. L4_TCP: BGP. L4_UDP: IKE, SLBC, BFD.")    
    enable_shaper: Literal["disable", "enable"] | None = Field(default=None, description="Enable/Disable NPU host protection engine (HPE) shaper.    disable:Disable NPU HPE shaping based on packet type.    enable:Enable NPU HPE shaping based on packet type.")
class Np6xliteFpAnomaly(BaseModel):
    """
    Child table model for fp-anomaly.
    
    NP6XLITE IPv4 anomaly protection. The trap-to-host forwards anomaly sessions to the CPU.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    tcp_syn_fin: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="TCP SYN flood SYN/FIN flag set anomalies.    allow:Allow TCP packets with syn_fin flag set to pass.    drop:Drop TCP packets with syn_fin flag set.    trap-to-host:Forward TCP packets with syn_fin flag set to FortiOS.")    
    tcp_fin_noack: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="TCP SYN flood with FIN flag set without ACK setting anomalies.    allow:Allow TCP packets with FIN flag set without ack setting to pass.    drop:Drop TCP packets with FIN flag set without ack setting.    trap-to-host:Forward TCP packets with FIN flag set without ack setting to FortiOS.")    
    tcp_fin_only: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="TCP SYN flood with only FIN flag set anomalies.    allow:Allow TCP packets with FIN flag set only to pass.    drop:Drop TCP packets with FIN flag set only.    trap-to-host:Forward TCP packets with FIN flag set only to FortiOS.")    
    tcp_no_flag: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="TCP SYN flood with no flag set anomalies.    allow:Allow TCP packets without flag set to pass.    drop:Drop TCP packets without flag set.    trap-to-host:Forward TCP packets without flag set to FortiOS.")    
    tcp_syn_data: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="TCP SYN flood packets with data anomalies.    allow:Allow TCP syn packets with data to pass.    drop:Drop TCP syn packets with data.    trap-to-host:Forward TCP syn packets with data to FortiOS.")    
    tcp_winnuke: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="TCP WinNuke anomalies.    allow:Allow TCP packets winnuke attack to pass.    drop:Drop TCP packets winnuke attack.    trap-to-host:Forward TCP packets winnuke attack to FortiOS.")    
    tcp_land: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="TCP land anomalies.    allow:Allow TCP land attack to pass.    drop:Drop TCP land attack.    trap-to-host:Forward TCP land attack to FortiOS.")    
    udp_land: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="UDP land anomalies.    allow:Allow UDP land attack to pass.    drop:Drop UDP land attack.    trap-to-host:Forward UDP land attack to FortiOS.")    
    icmp_land: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="ICMP land anomalies.    allow:Allow ICMP land attack to pass.    drop:Drop ICMP land attack.    trap-to-host:Forward ICMP land attack to FortiOS.")    
    icmp_frag: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Layer 3 fragmented packets that could be part of layer 4 ICMP anomalies.    allow:Allow L3 fragment packet with L4 protocol as ICMP attack to pass.    drop:Drop L3 fragment packet with L4 protocol as ICMP attack.    trap-to-host:Forward L3 fragment packet with L4 protocol as ICMP attack to FortiOS.")    
    ipv4_land: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Land anomalies.    allow:Allow IPv4 land attack to pass.    drop:Drop IPv4 land attack.    trap-to-host:Forward IPv4 land attack to FortiOS.")    
    ipv4_proto_err: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Invalid layer 4 protocol anomalies.    allow:Allow IPv4 invalid L4 protocol to pass.    drop:Drop IPv4 invalid L4 protocol.    trap-to-host:Forward IPv4 invalid L4 protocol to FortiOS.")    
    ipv4_unknopt: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Unknown option anomalies.    allow:Allow IPv4 with unknown options to pass.    drop:Drop IPv4 with unknown options.    trap-to-host:Forward IPv4 with unknown options to FortiOS.")    
    ipv4_optrr: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Record route option anomalies.    allow:Allow IPv4 with record route option to pass.    drop:Drop IPv4 with record route option.    trap-to-host:Forward IPv4 with record route option to FortiOS.")    
    ipv4_optssrr: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Strict source record route option anomalies.    allow:Allow IPv4 with strict source record route option to pass.    drop:Drop IPv4 with strict source record route option.    trap-to-host:Forward IPv4 with strict source record route option to FortiOS.")    
    ipv4_optlsrr: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Loose source record route option anomalies.    allow:Allow IPv4 with loose source record route option to pass.    drop:Drop IPv4 with loose source record route option.    trap-to-host:Forward IPv4 with loose source record route option to FortiOS.")    
    ipv4_optstream: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Stream option anomalies.    allow:Allow IPv4 with stream option to pass.    drop:Drop IPv4 with stream option.    trap-to-host:Forward IPv4 with stream option to FortiOS.")    
    ipv4_optsecurity: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Security option anomalies.    allow:Allow IPv4 with security option to pass.    drop:Drop IPv4 with security option.    trap-to-host:Forward IPv4 with security option to FortiOS.")    
    ipv4_opttimestamp: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Timestamp option anomalies.    allow:Allow IPv4 with timestamp option to pass.    drop:Drop IPv4 with timestamp option.    trap-to-host:Forward IPv4 with timestamp option to FortiOS.")    
    ipv4_csum_err: Literal["drop", "trap-to-host"] | None = Field(default=None, description="Invalid IPv4 IP checksum anomalies.    drop:Drop IPv4 invalid IP checksum.    trap-to-host:Forward IPv4 invalid IP checksum to main CPU for processing.")    
    tcp_csum_err: Literal["drop", "trap-to-host"] | None = Field(default=None, description="Invalid IPv4 TCP checksum anomalies.    drop:Drop IPv4 invalid TCP checksum.    trap-to-host:Forward IPv4 invalid TCP checksum to main CPU for processing.")    
    udp_csum_err: Literal["drop", "trap-to-host"] | None = Field(default=None, description="Invalid IPv4 UDP checksum anomalies.    drop:Drop IPv4 invalid UDP checksum.    trap-to-host:Forward IPv4 invalid UDP checksum to main CPU for processing.")    
    icmp_csum_err: Literal["drop", "trap-to-host"] | None = Field(default=None, description="Invalid IPv4 ICMP checksum anomalies.    drop:Drop IPv4 invalid ICMP checksum.    trap-to-host:Forward IPv4 invalid ICMP checksum to main CPU for processing.")    
    ipv6_land: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Land anomalies.    allow:Allow IPv6 land attack to pass.    drop:Drop IPv6 land attack.    trap-to-host:Forward IPv6 land attack to FortiOS.")    
    ipv6_proto_err: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Layer 4 invalid protocol anomalies.    allow:Allow IPv6 L4 invalid protocol to pass.    drop:Drop IPv6 L4 invalid protocol.    trap-to-host:Forward IPv6 L4 invalid protocol to FortiOS.")    
    ipv6_unknopt: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Unknown option anomalies.    allow:Allow IPv6 with unknown options to pass.    drop:Drop IPv6 with unknown options.    trap-to-host:Forward IPv6 with unknown options to FortiOS.")    
    ipv6_saddr_err: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Source address as multicast anomalies.    allow:Allow IPv6 with source address as multicast to pass.    drop:Drop IPv6 with source address as multicast.    trap-to-host:Forward IPv6 with source address as multicast to FortiOS.")    
    ipv6_daddr_err: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Destination address as unspecified or loopback address anomalies.    allow:Allow IPv6 with destination address as unspecified or loopback address to pass.    drop:Drop IPv6 with destination address as unspecified or loopback address.    trap-to-host:Forward IPv6 with destination address as unspecified or loopback address to FortiOS.")    
    ipv6_optralert: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Router alert option anomalies.    allow:Allow IPv6 with router alert option to pass.    drop:Drop IPv6 with router alert option.    trap-to-host:Forward IPv6 with router alert option to FortiOS.")    
    ipv6_optjumbo: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Jumbo options anomalies.    allow:Allow IPv6 with jumbo option to pass.    drop:Drop IPv6 with jumbo option.    trap-to-host:Forward IPv6 with jumbo option to FortiOS.")    
    ipv6_opttunnel: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Tunnel encapsulation limit option anomalies.    allow:Allow IPv6 with tunnel encapsulation limit to pass.    drop:Drop IPv6 with tunnel encapsulation limit.    trap-to-host:Forward IPv6 with tunnel encapsulation limit to FortiOS.")    
    ipv6_opthomeaddr: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Home address option anomalies.    allow:Allow IPv6 with home address option to pass.    drop:Drop IPv6 with home address option.    trap-to-host:Forward IPv6 with home address option to FortiOS.")    
    ipv6_optnsap: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Network service access point address option anomalies.    allow:Allow IPv6 with network service access point address option to pass.    drop:Drop IPv6 with network service access point address option.    trap-to-host:Forward IPv6 with network service access point address option to FortiOS.")    
    ipv6_optendpid: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="End point identification anomalies.    allow:Allow IPv6 with end point identification option to pass.    drop:Drop IPv6 with end point identification option.    trap-to-host:Forward IPv6 with end point identification option to FortiOS.")    
    ipv6_optinvld: Literal["allow", "drop", "trap-to-host"] | None = Field(default=None, description="Invalid option anomalies.Invalid option anomalies.    allow:Allow IPv6 with invalid option to pass.    drop:Drop IPv6 with invalid option.    trap-to-host:Forward IPv6 with invalid option to FortiOS.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class Np6xliteIpsecThroughputMsgFrequencyEnum(str, Enum):
    """Allowed values for ipsec_throughput_msg_frequency field."""
    DISABLE = "disable"
    V_32KB = "32kb"
    V_64KB = "64kb"
    V_128KB = "128kb"
    V_256KB = "256kb"
    V_512KB = "512kb"
    V_1MB = "1mb"
    V_2MB = "2mb"
    V_4MB = "4mb"
    V_8MB = "8mb"
    V_16MB = "16mb"
    V_32MB = "32mb"
    V_64MB = "64mb"
    V_128MB = "128mb"
    V_256MB = "256mb"
    V_512MB = "512mb"
    V_1GB = "1gb"

class Np6xliteIpsecStsTimeoutEnum(str, Enum):
    """Allowed values for ipsec_sts_timeout field."""
    V_1 = "1"
    V_2 = "2"
    V_3 = "3"
    V_4 = "4"
    V_5 = "5"
    V_6 = "6"
    V_7 = "7"
    V_8 = "8"
    V_9 = "9"
    V_10 = "10"


# ============================================================================
# Main Model
# ============================================================================

class Np6xliteModel(BaseModel):
    """
    Pydantic model for system/np6xlite configuration.
    
    Configuration for system/np6xlite
    
    Validation Rules:        - name: pattern=        - fastpath: pattern=        - per_session_accounting: pattern=        - session_timeout_interval: pattern=        - ipsec_inner_fragment: pattern=        - ipsec_throughput_msg_frequency: pattern=        - ipsec_sts_timeout: pattern=        - hpe: pattern=        - fp_anomaly: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(default=None, description="Device Name.")    
    fastpath: Literal["disable", "enable"] | None = Field(default=None, description="Enable/disable NP6XLITE offloading (also called fast path).    disable:Disable NP6XLITE offloading (fast path).    enable:Enable NP6XLITE offloading (fast path).")    
    per_session_accounting: Literal["disable", "traffic-log-only", "enable"] | None = Field(default=None, description="Enable/disable per-session accounting.    disable:Disable per-session accounting.    traffic-log-only:Per-session accounting only for sessions with traffic logging enabled in firewall policy.    enable:Per-session accounting for all sessions.")    
    session_timeout_interval: int | None = Field(default=None, description="Set session timeout interval (0 - 1000 sec, default 40 sec).")    
    ipsec_inner_fragment: Literal["disable", "enable"] | None = Field(default=None, description="Enable/disable NP6XLite IPsec fragmentation type: inner.    disable:NP6XLite ipsec fragmentation type: outer.    enable:Enable NP6XLite ipsec fragmentation type: inner.")    
    ipsec_throughput_msg_frequency: Np6xliteIpsecThroughputMsgFrequencyEnum | None = Field(default=None, description="Set NP6XLite IPsec throughput message frequency (0 = disable).    disable:Disable NP6Xlite throughput update message.    32kb:Set NP6Xlite throughput update message frequency to 32KB.    64kb:Set NP6Xlite throughput update message frequency to 64KB.    128kb:Set NP6Xlite throughput update message frequency to 128KB.    256kb:Set NP6Xlite throughput update message frequency to 256KB.    512kb:Set NP6Xlite throughput update message frequency to 512KB.    1mb:Set NP6Xlite throughput update message frequency to 1MB.    2mb:Set NP6Xlite throughput update message frequency to 2MB.    4mb:Set NP6Xlite throughput update message frequency to 4MB.    8mb:Set NP6Xlite throughput update message frequency to 8MB.    16mb:Set NP6Xlite throughput update message frequency to 16MB.    32mb:Set NP6Xlite throughput update message frequency to 32MB.    64mb:Set NP6Xlite throughput update message frequency to 64MB.    128mb:Set NP6Xlite throughput update message frequency to 128MB.    256mb:Set NP6Xlite throughput update message frequency to 256MB.    512mb:Set NP6Xlite throughput update message frequency to 512MB.    1gb:Set NP6Xlite throughput update message frequency to 1GB.")    
    ipsec_sts_timeout: Np6xliteIpsecStsTimeoutEnum | None = Field(default=None, description="Set NP6XLite IPsec STS message timeout.    1:Set NP6Xlite STS message timeout to 1 sec (recommended for IPSec throughput GUI).    2:Set NP6Xlite STS message timeout to 2 sec.    3:Set NP6Xlite STS message timeout to 3 sec.    4:Set NP6Xlite STS message timeout to 4 sec.    5:Set NP6Xlite STS message timeout to 5 sec (default).    6:Set NP6Xlite STS message timeout to 6 sec.    7:Set NP6Xlite STS message timeout to 7 sec.    8:Set NP6Xlite STS message timeout to 8 sec.    9:Set NP6Xlite STS message timeout to 9 sec.    10:Set NP6Xlite STS message timeout to 10 sec.")    
    hpe: list[Np6xliteHpe] = Field(default_factory=list, description="HPE configuration.")    
    fp_anomaly: list[Np6xliteFpAnomaly] = Field(default_factory=list, description="NP6XLITE IPv4 anomaly protection. The trap-to-host forwards anomaly sessions to the CPU.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def to_fortios_dict(self) -> dict[str, Any]:
        """
        Convert model to FortiOS API payload format.
        
        Returns:
            Dict suitable for POST/PUT operations
        """
        # Export with exclude_none to avoid sending null values
        return self.model_dump(exclude_none=True, by_alias=True)
    
    @classmethod
    def from_fortios_response(cls, data: dict[str, Any]) -> "Np6xliteModel":
        """
        Create model instance from FortiOS API response.
        
        Args:
            data: Response data from API
            
        Returns:
            Validated model instance
        """
        return cls(**data)

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "Np6xliteModel",    "Np6xliteHpe",    "Np6xliteFpAnomaly",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T19:10:41.249557Z
# ============================================================================