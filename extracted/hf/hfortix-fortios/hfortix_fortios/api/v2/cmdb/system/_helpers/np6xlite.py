"""Validation helpers for system/np6xlite - Auto-generated"""

from typing import Any, TypedDict, Literal
from typing_extensions import NotRequired

# Import common validators from central _helpers module
from hfortix_fortios._helpers import (
    validate_enable_disable,
    validate_integer_range,
    validate_string_length,
    validate_port_number,
    validate_ip_address,
    validate_ipv6_address,
    validate_mac_address,
)

# Import central validation functions (avoid duplication across 1,062 files)
from hfortix_fortios._helpers.validation import (
    validate_required_fields as _validate_required_fields,
    validate_enum_field as _validate_enum_field,
    validate_query_parameter as _validate_query_parameter,
)

# ============================================================================
# Required Fields Validation
# Auto-generated from schema
# ============================================================================

# ⚠️  IMPORTANT: FortiOS schemas have known issues with required field marking:

# Do NOT use this list for strict validation - test with the actual FortiOS API!

# Fields marked as required (after filtering false positives)
REQUIRED_FIELDS = [
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
}

# ============================================================================
# Deprecated Fields
# Auto-generated from schema - warns users about deprecated fields
# ============================================================================

# Deprecated fields with migration guidance
DEPRECATED_FIELDS = {
}

# ============================================================================
# Field Metadata (Type Information & Descriptions)
# Auto-generated from schema - use for IDE autocomplete and documentation
# ============================================================================

# Field types mapping
FIELD_TYPES = {
    "name": "string",  # Device Name.
    "fastpath": "option",  # Enable/disable NP6XLITE offloading (also called fast path).    disable:Disable N
    "per-session-accounting": "option",  # Enable/disable per-session accounting.    disable:Disable per-session accounting
    "session-timeout-interval": "integer",  # Set session timeout interval (0 - 1000 sec, default 40 sec).
    "ipsec-inner-fragment": "option",  # Enable/disable NP6XLite IPsec fragmentation type: inner.    disable:NP6XLite ips
    "ipsec-throughput-msg-frequency": "option",  # Set NP6XLite IPsec throughput message frequency (0 = disable).    disable:Disabl
    "ipsec-sts-timeout": "option",  # Set NP6XLite IPsec STS message timeout.    1:Set NP6Xlite STS message timeout to
    "hpe": "table",  # HPE configuration.
    "fp-anomaly": "table",  # NP6XLITE IPv4 anomaly protection. The trap-to-host forwards anomaly sessions to 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Device Name.",
    "fastpath": "Enable/disable NP6XLITE offloading (also called fast path).    disable:Disable NP6XLITE offloading (fast path).    enable:Enable NP6XLITE offloading (fast path).",
    "per-session-accounting": "Enable/disable per-session accounting.    disable:Disable per-session accounting.    traffic-log-only:Per-session accounting only for sessions with traffic logging enabled in firewall policy.    enable:Per-session accounting for all sessions.",
    "session-timeout-interval": "Set session timeout interval (0 - 1000 sec, default 40 sec).",
    "ipsec-inner-fragment": "Enable/disable NP6XLite IPsec fragmentation type: inner.    disable:NP6XLite ipsec fragmentation type: outer.    enable:Enable NP6XLite ipsec fragmentation type: inner.",
    "ipsec-throughput-msg-frequency": "Set NP6XLite IPsec throughput message frequency (0 = disable).    disable:Disable NP6Xlite throughput update message.    32kb:Set NP6Xlite throughput update message frequency to 32KB.    64kb:Set NP6Xlite throughput update message frequency to 64KB.    128kb:Set NP6Xlite throughput update message frequency to 128KB.    256kb:Set NP6Xlite throughput update message frequency to 256KB.    512kb:Set NP6Xlite throughput update message frequency to 512KB.    1mb:Set NP6Xlite throughput update message frequency to 1MB.    2mb:Set NP6Xlite throughput update message frequency to 2MB.    4mb:Set NP6Xlite throughput update message frequency to 4MB.    8mb:Set NP6Xlite throughput update message frequency to 8MB.    16mb:Set NP6Xlite throughput update message frequency to 16MB.    32mb:Set NP6Xlite throughput update message frequency to 32MB.    64mb:Set NP6Xlite throughput update message frequency to 64MB.    128mb:Set NP6Xlite throughput update message frequency to 128MB.    256mb:Set NP6Xlite throughput update message frequency to 256MB.    512mb:Set NP6Xlite throughput update message frequency to 512MB.    1gb:Set NP6Xlite throughput update message frequency to 1GB.",
    "ipsec-sts-timeout": "Set NP6XLite IPsec STS message timeout.    1:Set NP6Xlite STS message timeout to 1 sec (recommended for IPSec throughput GUI).    2:Set NP6Xlite STS message timeout to 2 sec.    3:Set NP6Xlite STS message timeout to 3 sec.    4:Set NP6Xlite STS message timeout to 4 sec.    5:Set NP6Xlite STS message timeout to 5 sec (default).    6:Set NP6Xlite STS message timeout to 6 sec.    7:Set NP6Xlite STS message timeout to 7 sec.    8:Set NP6Xlite STS message timeout to 8 sec.    9:Set NP6Xlite STS message timeout to 9 sec.    10:Set NP6Xlite STS message timeout to 10 sec.",
    "hpe": "HPE configuration.",
    "fp-anomaly": "NP6XLITE IPv4 anomaly protection. The trap-to-host forwards anomaly sessions to the CPU.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "hpe": {
        "tcpsyn-max": {
            "type": "integer",
            "help": "Maximum TCP SYN only packet rate (1K - 1G pps, default = 600K pps).",
        },
        "tcpsyn-ack-max": {
            "type": "integer",
            "help": "Maximum TCP carries SYN and ACK flags packet rate (1K - 1G pps, default = 600K pps).",
        },
        "tcpfin-rst-max": {
            "type": "integer",
            "help": "Maximum TCP carries FIN or RST flags packet rate (1K - 1G pps, default = 600K pps).",
        },
        "tcp-others-max": {
            "type": "integer",
            "help": "Maximum TCP packet rate for TCP packets that match none of the 3 types above (1K - 1G pps, default = 600K pps).",
        },
        "udp-max": {
            "type": "integer",
            "help": "Maximum UDP packet rate (1K - 1G pps, default = 600K pps).",
        },
        "icmp-max": {
            "type": "integer",
            "help": "Maximum ICMP packet rate (1K - 1G pps, default = 200K pps).",
        },
        "sctp-max": {
            "type": "integer",
            "help": "Maximum SCTP packet rate (1K - 1G pps, default = 200K pps).",
        },
        "esp-max": {
            "type": "integer",
            "help": "Maximum ESP packet rate (1K - 1G pps, default = 200K pps).",
        },
        "ip-frag-max": {
            "type": "integer",
            "help": "Maximum fragmented IP packet rate (1K - 1G pps, default = 200K pps).",
        },
        "ip-others-max": {
            "type": "integer",
            "help": "Maximum IP packet rate for other packets (packet types that cannot be set with other options) (1K - 1G pps, default = 200K pps).",
        },
        "arp-max": {
            "type": "integer",
            "help": "Maximum ARP packet rate (1K - 1G pps, default = 200K pps).",
        },
        "l2-others-max": {
            "type": "integer",
            "help": "Maximum L2 packet rate for L2 packets that are not ARP packets (1K - 1G pps, default = 200K pps).",
        },
        "pri-type-max": {
            "type": "integer",
            "help": "Maximum overflow rate of priority type traffic (1K - 1G pps, default = 200K pps). Includes L2: HA, 802.3ad LACP, heartbeats. L3: OSPF. L4_TCP: BGP. L4_UDP: IKE, SLBC, BFD.",
        },
        "enable-shaper": {
            "type": "option",
            "help": "Enable/Disable NPU host protection engine (HPE) shaper.    disable:Disable NPU HPE shaping based on packet type.    enable:Enable NPU HPE shaping based on packet type.",
            "options": ["disable", "enable"],
        },
    },
    "fp-anomaly": {
        "tcp-syn-fin": {
            "type": "option",
            "help": "TCP SYN flood SYN/FIN flag set anomalies.    allow:Allow TCP packets with syn_fin flag set to pass.    drop:Drop TCP packets with syn_fin flag set.    trap-to-host:Forward TCP packets with syn_fin flag set to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "tcp-fin-noack": {
            "type": "option",
            "help": "TCP SYN flood with FIN flag set without ACK setting anomalies.    allow:Allow TCP packets with FIN flag set without ack setting to pass.    drop:Drop TCP packets with FIN flag set without ack setting.    trap-to-host:Forward TCP packets with FIN flag set without ack setting to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "tcp-fin-only": {
            "type": "option",
            "help": "TCP SYN flood with only FIN flag set anomalies.    allow:Allow TCP packets with FIN flag set only to pass.    drop:Drop TCP packets with FIN flag set only.    trap-to-host:Forward TCP packets with FIN flag set only to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "tcp-no-flag": {
            "type": "option",
            "help": "TCP SYN flood with no flag set anomalies.    allow:Allow TCP packets without flag set to pass.    drop:Drop TCP packets without flag set.    trap-to-host:Forward TCP packets without flag set to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "tcp-syn-data": {
            "type": "option",
            "help": "TCP SYN flood packets with data anomalies.    allow:Allow TCP syn packets with data to pass.    drop:Drop TCP syn packets with data.    trap-to-host:Forward TCP syn packets with data to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "tcp-winnuke": {
            "type": "option",
            "help": "TCP WinNuke anomalies.    allow:Allow TCP packets winnuke attack to pass.    drop:Drop TCP packets winnuke attack.    trap-to-host:Forward TCP packets winnuke attack to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "tcp-land": {
            "type": "option",
            "help": "TCP land anomalies.    allow:Allow TCP land attack to pass.    drop:Drop TCP land attack.    trap-to-host:Forward TCP land attack to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "udp-land": {
            "type": "option",
            "help": "UDP land anomalies.    allow:Allow UDP land attack to pass.    drop:Drop UDP land attack.    trap-to-host:Forward UDP land attack to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "icmp-land": {
            "type": "option",
            "help": "ICMP land anomalies.    allow:Allow ICMP land attack to pass.    drop:Drop ICMP land attack.    trap-to-host:Forward ICMP land attack to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "icmp-frag": {
            "type": "option",
            "help": "Layer 3 fragmented packets that could be part of layer 4 ICMP anomalies.    allow:Allow L3 fragment packet with L4 protocol as ICMP attack to pass.    drop:Drop L3 fragment packet with L4 protocol as ICMP attack.    trap-to-host:Forward L3 fragment packet with L4 protocol as ICMP attack to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-land": {
            "type": "option",
            "help": "Land anomalies.    allow:Allow IPv4 land attack to pass.    drop:Drop IPv4 land attack.    trap-to-host:Forward IPv4 land attack to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-proto-err": {
            "type": "option",
            "help": "Invalid layer 4 protocol anomalies.    allow:Allow IPv4 invalid L4 protocol to pass.    drop:Drop IPv4 invalid L4 protocol.    trap-to-host:Forward IPv4 invalid L4 protocol to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-unknopt": {
            "type": "option",
            "help": "Unknown option anomalies.    allow:Allow IPv4 with unknown options to pass.    drop:Drop IPv4 with unknown options.    trap-to-host:Forward IPv4 with unknown options to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-optrr": {
            "type": "option",
            "help": "Record route option anomalies.    allow:Allow IPv4 with record route option to pass.    drop:Drop IPv4 with record route option.    trap-to-host:Forward IPv4 with record route option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-optssrr": {
            "type": "option",
            "help": "Strict source record route option anomalies.    allow:Allow IPv4 with strict source record route option to pass.    drop:Drop IPv4 with strict source record route option.    trap-to-host:Forward IPv4 with strict source record route option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-optlsrr": {
            "type": "option",
            "help": "Loose source record route option anomalies.    allow:Allow IPv4 with loose source record route option to pass.    drop:Drop IPv4 with loose source record route option.    trap-to-host:Forward IPv4 with loose source record route option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-optstream": {
            "type": "option",
            "help": "Stream option anomalies.    allow:Allow IPv4 with stream option to pass.    drop:Drop IPv4 with stream option.    trap-to-host:Forward IPv4 with stream option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-optsecurity": {
            "type": "option",
            "help": "Security option anomalies.    allow:Allow IPv4 with security option to pass.    drop:Drop IPv4 with security option.    trap-to-host:Forward IPv4 with security option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-opttimestamp": {
            "type": "option",
            "help": "Timestamp option anomalies.    allow:Allow IPv4 with timestamp option to pass.    drop:Drop IPv4 with timestamp option.    trap-to-host:Forward IPv4 with timestamp option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv4-csum-err": {
            "type": "option",
            "help": "Invalid IPv4 IP checksum anomalies.    drop:Drop IPv4 invalid IP checksum.    trap-to-host:Forward IPv4 invalid IP checksum to main CPU for processing.",
            "options": ["drop", "trap-to-host"],
        },
        "tcp-csum-err": {
            "type": "option",
            "help": "Invalid IPv4 TCP checksum anomalies.    drop:Drop IPv4 invalid TCP checksum.    trap-to-host:Forward IPv4 invalid TCP checksum to main CPU for processing.",
            "options": ["drop", "trap-to-host"],
        },
        "udp-csum-err": {
            "type": "option",
            "help": "Invalid IPv4 UDP checksum anomalies.    drop:Drop IPv4 invalid UDP checksum.    trap-to-host:Forward IPv4 invalid UDP checksum to main CPU for processing.",
            "options": ["drop", "trap-to-host"],
        },
        "icmp-csum-err": {
            "type": "option",
            "help": "Invalid IPv4 ICMP checksum anomalies.    drop:Drop IPv4 invalid ICMP checksum.    trap-to-host:Forward IPv4 invalid ICMP checksum to main CPU for processing.",
            "options": ["drop", "trap-to-host"],
        },
        "ipv6-land": {
            "type": "option",
            "help": "Land anomalies.    allow:Allow IPv6 land attack to pass.    drop:Drop IPv6 land attack.    trap-to-host:Forward IPv6 land attack to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-proto-err": {
            "type": "option",
            "help": "Layer 4 invalid protocol anomalies.    allow:Allow IPv6 L4 invalid protocol to pass.    drop:Drop IPv6 L4 invalid protocol.    trap-to-host:Forward IPv6 L4 invalid protocol to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-unknopt": {
            "type": "option",
            "help": "Unknown option anomalies.    allow:Allow IPv6 with unknown options to pass.    drop:Drop IPv6 with unknown options.    trap-to-host:Forward IPv6 with unknown options to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-saddr-err": {
            "type": "option",
            "help": "Source address as multicast anomalies.    allow:Allow IPv6 with source address as multicast to pass.    drop:Drop IPv6 with source address as multicast.    trap-to-host:Forward IPv6 with source address as multicast to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-daddr-err": {
            "type": "option",
            "help": "Destination address as unspecified or loopback address anomalies.    allow:Allow IPv6 with destination address as unspecified or loopback address to pass.    drop:Drop IPv6 with destination address as unspecified or loopback address.    trap-to-host:Forward IPv6 with destination address as unspecified or loopback address to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-optralert": {
            "type": "option",
            "help": "Router alert option anomalies.    allow:Allow IPv6 with router alert option to pass.    drop:Drop IPv6 with router alert option.    trap-to-host:Forward IPv6 with router alert option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-optjumbo": {
            "type": "option",
            "help": "Jumbo options anomalies.    allow:Allow IPv6 with jumbo option to pass.    drop:Drop IPv6 with jumbo option.    trap-to-host:Forward IPv6 with jumbo option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-opttunnel": {
            "type": "option",
            "help": "Tunnel encapsulation limit option anomalies.    allow:Allow IPv6 with tunnel encapsulation limit to pass.    drop:Drop IPv6 with tunnel encapsulation limit.    trap-to-host:Forward IPv6 with tunnel encapsulation limit to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-opthomeaddr": {
            "type": "option",
            "help": "Home address option anomalies.    allow:Allow IPv6 with home address option to pass.    drop:Drop IPv6 with home address option.    trap-to-host:Forward IPv6 with home address option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-optnsap": {
            "type": "option",
            "help": "Network service access point address option anomalies.    allow:Allow IPv6 with network service access point address option to pass.    drop:Drop IPv6 with network service access point address option.    trap-to-host:Forward IPv6 with network service access point address option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-optendpid": {
            "type": "option",
            "help": "End point identification anomalies.    allow:Allow IPv6 with end point identification option to pass.    drop:Drop IPv6 with end point identification option.    trap-to-host:Forward IPv6 with end point identification option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
        "ipv6-optinvld": {
            "type": "option",
            "help": "Invalid option anomalies.Invalid option anomalies.    allow:Allow IPv6 with invalid option to pass.    drop:Drop IPv6 with invalid option.    trap-to-host:Forward IPv6 with invalid option to FortiOS.",
            "options": ["allow", "drop", "trap-to-host"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FASTPATH = [
    "disable",
    "enable",
]
VALID_BODY_PER_SESSION_ACCOUNTING = [
    "disable",
    "traffic-log-only",
    "enable",
]
VALID_BODY_IPSEC_INNER_FRAGMENT = [
    "disable",
    "enable",
]
VALID_BODY_IPSEC_THROUGHPUT_MSG_FREQUENCY = [
    "disable",
    "32kb",
    "64kb",
    "128kb",
    "256kb",
    "512kb",
    "1mb",
    "2mb",
    "4mb",
    "8mb",
    "16mb",
    "32mb",
    "64mb",
    "128mb",
    "256mb",
    "512mb",
    "1gb",
]
VALID_BODY_IPSEC_STS_TIMEOUT = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_np6xlite_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/np6xlite."""
    # Validate query parameters using central function
    if "action" in params:
        is_valid, error = _validate_query_parameter(
            "action",
            params.get("action"),
            VALID_QUERY_ACTION
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# POST Validation
# ============================================================================


def validate_system_np6xlite_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/np6xlite object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "fastpath" in payload:
        is_valid, error = _validate_enum_field(
            "fastpath",
            payload["fastpath"],
            VALID_BODY_FASTPATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-session-accounting" in payload:
        is_valid, error = _validate_enum_field(
            "per-session-accounting",
            payload["per-session-accounting"],
            VALID_BODY_PER_SESSION_ACCOUNTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-inner-fragment" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-inner-fragment",
            payload["ipsec-inner-fragment"],
            VALID_BODY_IPSEC_INNER_FRAGMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-throughput-msg-frequency" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-throughput-msg-frequency",
            payload["ipsec-throughput-msg-frequency"],
            VALID_BODY_IPSEC_THROUGHPUT_MSG_FREQUENCY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-sts-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-sts-timeout",
            payload["ipsec-sts-timeout"],
            VALID_BODY_IPSEC_STS_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_np6xlite_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/np6xlite."""
    # Validate enum values using central function
    if "fastpath" in payload:
        is_valid, error = _validate_enum_field(
            "fastpath",
            payload["fastpath"],
            VALID_BODY_FASTPATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-session-accounting" in payload:
        is_valid, error = _validate_enum_field(
            "per-session-accounting",
            payload["per-session-accounting"],
            VALID_BODY_PER_SESSION_ACCOUNTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-inner-fragment" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-inner-fragment",
            payload["ipsec-inner-fragment"],
            VALID_BODY_IPSEC_INNER_FRAGMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-throughput-msg-frequency" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-throughput-msg-frequency",
            payload["ipsec-throughput-msg-frequency"],
            VALID_BODY_IPSEC_THROUGHPUT_MSG_FREQUENCY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-sts-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-sts-timeout",
            payload["ipsec-sts-timeout"],
            VALID_BODY_IPSEC_STS_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# Metadata Access Functions
# Imported from central module to avoid duplication across 1,062 files
# Bound to this endpoint's data using functools.partial (saves ~7KB per file)
# ============================================================================

from functools import partial
from hfortix_fortios._helpers.metadata import (
    get_field_description,
    get_field_type,
    get_field_constraints,
    get_field_default,
    get_field_options,
    get_nested_schema,
    get_all_fields,
    get_field_metadata,
    validate_field_value,
)

# Bind module-specific data to central functions using partial application
get_field_description = partial(get_field_description, FIELD_DESCRIPTIONS)
get_field_type = partial(get_field_type, FIELD_TYPES)
get_field_constraints = partial(get_field_constraints, FIELD_CONSTRAINTS)
get_field_default = partial(get_field_default, FIELDS_WITH_DEFAULTS)
get_field_options = partial(get_field_options, globals())
get_nested_schema = partial(get_nested_schema, NESTED_SCHEMAS)
get_all_fields = partial(get_all_fields, FIELD_TYPES)
get_field_metadata = partial(get_field_metadata, FIELD_TYPES, FIELD_DESCRIPTIONS, 
                             FIELD_CONSTRAINTS, FIELDS_WITH_DEFAULTS, REQUIRED_FIELDS,
                             NESTED_SCHEMAS, globals())
validate_field_value = partial(validate_field_value, FIELD_TYPES, FIELD_DESCRIPTIONS,
                               FIELD_CONSTRAINTS, globals())


# ============================================================================
# Schema Information
# Metadata about this endpoint schema
# ============================================================================

SCHEMA_INFO = {
    "endpoint": "system/np6xlite",
    "category": "cmdb",
    "api_path": "system/np6xlite",
    "help": "Configuration for system/np6xlite",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
