"""Validation helpers for system/sdwan - Auto-generated"""

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
    "status": "disable",
    "load-balance-mode": "source-ip-based",
    "speedtest-bypass-routing": "disable",
    "duplication-max-num": 2,
    "duplication-max-discrepancy": 250,
    "neighbor-hold-down": "disable",
    "neighbor-hold-down-time": 0,
    "app-perf-log-period": 0,
    "neighbor-hold-boot-time": 0,
    "fail-detect": "disable",
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
    "status": "option",  # Enable/disable SD-WAN.
    "load-balance-mode": "option",  # Algorithm or mode to use for load balancing Internet traffic to SD-WAN members.
    "speedtest-bypass-routing": "option",  # Enable/disable bypass routing when speedtest on a SD-WAN member.
    "duplication-max-num": "integer",  # Maximum number of interface members a packet is duplicated in the SD-WAN zone (2
    "duplication-max-discrepancy": "integer",  # Maximum discrepancy between two packets for deduplication in milliseconds (250 -
    "neighbor-hold-down": "option",  # Enable/disable hold switching from the secondary neighbor to the primary neighbo
    "neighbor-hold-down-time": "integer",  # Waiting period in seconds when switching from the secondary neighbor to the prim
    "app-perf-log-period": "integer",  # Time interval in seconds that application performance logs are generated (0 - 36
    "neighbor-hold-boot-time": "integer",  # Waiting period in seconds when switching from the primary neighbor to the second
    "fail-detect": "option",  # Enable/disable SD-WAN Internet connection status checking (failure detection).
    "fail-alert-interfaces": "string",  # Physical interfaces that will be alerted.
    "zone": "string",  # Configure SD-WAN zones.
    "members": "string",  # FortiGate interfaces added to the SD-WAN.
    "health-check": "string",  # SD-WAN status checking or health checking. Identify a server on the Internet and
    "service": "string",  # Create SD-WAN rules (also called services) to control how sessions are distribut
    "neighbor": "string",  # Create SD-WAN neighbor from BGP neighbor table to control route advertisements a
    "duplication": "string",  # Create SD-WAN duplication rule.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable SD-WAN.",
    "load-balance-mode": "Algorithm or mode to use for load balancing Internet traffic to SD-WAN members.",
    "speedtest-bypass-routing": "Enable/disable bypass routing when speedtest on a SD-WAN member.",
    "duplication-max-num": "Maximum number of interface members a packet is duplicated in the SD-WAN zone (2 - 4, default = 2; if set to 3, the original packet plus 2 more copies are created).",
    "duplication-max-discrepancy": "Maximum discrepancy between two packets for deduplication in milliseconds (250 - 1000, default = 250).",
    "neighbor-hold-down": "Enable/disable hold switching from the secondary neighbor to the primary neighbor.",
    "neighbor-hold-down-time": "Waiting period in seconds when switching from the secondary neighbor to the primary neighbor when hold-down is disabled. (0 - 10000000, default = 0).",
    "app-perf-log-period": "Time interval in seconds that application performance logs are generated (0 - 3600, default = 0).",
    "neighbor-hold-boot-time": "Waiting period in seconds when switching from the primary neighbor to the secondary neighbor from the neighbor start. (0 - 10000000, default = 0).",
    "fail-detect": "Enable/disable SD-WAN Internet connection status checking (failure detection).",
    "fail-alert-interfaces": "Physical interfaces that will be alerted.",
    "zone": "Configure SD-WAN zones.",
    "members": "FortiGate interfaces added to the SD-WAN.",
    "health-check": "SD-WAN status checking or health checking. Identify a server on the Internet and determine how SD-WAN verifies that the FortiGate can communicate with it.",
    "service": "Create SD-WAN rules (also called services) to control how sessions are distributed to interfaces in the SD-WAN.",
    "neighbor": "Create SD-WAN neighbor from BGP neighbor table to control route advertisements according to SLA status.",
    "duplication": "Create SD-WAN duplication rule.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "duplication-max-num": {"type": "integer", "min": 2, "max": 4},
    "duplication-max-discrepancy": {"type": "integer", "min": 250, "max": 1000},
    "neighbor-hold-down-time": {"type": "integer", "min": 0, "max": 10000000},
    "app-perf-log-period": {"type": "integer", "min": 0, "max": 3600},
    "neighbor-hold-boot-time": {"type": "integer", "min": 0, "max": 10000000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "fail-alert-interfaces": {
        "name": {
            "type": "string",
            "help": "Physical interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "zone": {
        "name": {
            "type": "string",
            "help": "Zone name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "advpn-select": {
            "type": "option",
            "help": "Enable/disable selection of ADVPN based on SDWAN information.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "advpn-health-check": {
            "type": "string",
            "help": "Health check for ADVPN local overlay link quality.",
            "default": "",
            "max_length": 35,
        },
        "service-sla-tie-break": {
            "type": "option",
            "help": "Method of selecting member if more than one meets the SLA.",
            "default": "cfg-order",
            "options": ["cfg-order", "fib-best-match", "priority", "input-device"],
        },
        "minimum-sla-meet-members": {
            "type": "integer",
            "help": "Minimum number of members which meet SLA when the neighbor is preferred.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
    },
    "members": {
        "seq-num": {
            "type": "integer",
            "help": "Sequence number(1-512).",
            "default": 0,
            "min_value": 0,
            "max_value": 512,
        },
        "interface": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 15,
        },
        "zone": {
            "type": "string",
            "help": "Zone name.",
            "default": "virtual-wan-link",
            "max_length": 35,
        },
        "gateway": {
            "type": "ipv4-address",
            "help": "The default gateway for this interface. Usually the default gateway of the Internet service provider that this interface is connected to.",
            "default": "0.0.0.0",
        },
        "preferred-source": {
            "type": "ipv4-address",
            "help": "Preferred source of route for this member.",
            "default": "0.0.0.0",
        },
        "source": {
            "type": "ipv4-address",
            "help": "Source IP address used in the health-check packet to the server.",
            "default": "0.0.0.0",
        },
        "gateway6": {
            "type": "ipv6-address",
            "help": "IPv6 gateway.",
            "default": "::",
        },
        "source6": {
            "type": "ipv6-address",
            "help": "Source IPv6 address used in the health-check packet to the server.",
            "default": "::",
        },
        "cost": {
            "type": "integer",
            "help": "Cost of this interface for services in SLA mode (0 - 4294967295, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "weight": {
            "type": "integer",
            "help": "Weight of this interface for weighted load balancing. (1 - 255) More traffic is directed to interfaces with higher weights.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "priority": {
            "type": "integer",
            "help": "Priority of the interface for IPv4 (1 - 65535, default = 1). Used for SD-WAN rules or priority rules.",
            "default": 1,
            "min_value": 1,
            "max_value": 65535,
        },
        "priority6": {
            "type": "integer",
            "help": "Priority of the interface for IPv6 (1 - 65535, default = 1024). Used for SD-WAN rules or priority rules.",
            "default": 1024,
            "min_value": 1,
            "max_value": 65535,
        },
        "priority-in-sla": {
            "type": "integer",
            "help": "Preferred priority of routes to this member when this member is in-sla (0 - 65535, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "priority-out-sla": {
            "type": "integer",
            "help": "Preferred priority of routes to this member when this member is out-of-sla (0 - 65535, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "spillover-threshold": {
            "type": "integer",
            "help": "Egress spillover threshold for this interface (0 - 16776000 kbit/s). When this traffic volume threshold is reached, new sessions spill over to other interfaces in the SD-WAN.",
            "default": 0,
            "min_value": 0,
            "max_value": 16776000,
        },
        "ingress-spillover-threshold": {
            "type": "integer",
            "help": "Ingress spillover threshold for this interface (0 - 16776000 kbit/s). When this traffic volume threshold is reached, new sessions spill over to other interfaces in the SD-WAN.",
            "default": 0,
            "min_value": 0,
            "max_value": 16776000,
        },
        "volume-ratio": {
            "type": "integer",
            "help": "Measured volume ratio (this value / sum of all values = percentage of link volume, 1 - 255).",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this interface in the SD-WAN.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "transport-group": {
            "type": "integer",
            "help": "Measured transport group (0 - 255).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "comment": {
            "type": "var-string",
            "help": "Comments.",
            "max_length": 255,
        },
    },
    "health-check": {
        "name": {
            "type": "string",
            "help": "Status check or health check name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "fortiguard": {
            "type": "option",
            "help": "Enable/disable use of FortiGuard predefined server.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "fortiguard-name": {
            "type": "string",
            "help": "Predefined health-check target name.",
            "default": "",
            "max_length": 35,
        },
        "probe-packets": {
            "type": "option",
            "help": "Enable/disable transmission of probe packets.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "addr-mode": {
            "type": "option",
            "help": "Address mode (IPv4 or IPv6).",
            "default": "ipv4",
            "options": ["ipv4", "ipv6"],
        },
        "system-dns": {
            "type": "option",
            "help": "Enable/disable system DNS as the probe server.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "server": {
            "type": "string",
            "help": "IP address or FQDN name of the server.",
            "default": "",
            "max_length": 79,
        },
        "detect-mode": {
            "type": "option",
            "help": "The mode determining how to detect the server.",
            "default": "active",
            "options": ["active", "passive", "prefer-passive", "remote", "agent-based"],
        },
        "protocol": {
            "type": "option",
            "help": "Protocol used to determine if the FortiGate can communicate with the server.",
            "default": "ping",
            "options": ["ping", "tcp-echo", "udp-echo", "http", "https", "twamp", "dns", "tcp-connect", "ftp"],
        },
        "port": {
            "type": "integer",
            "help": "Port number used to communicate with the server over the selected protocol (0 - 65535, default = 0, auto select. http, tcp-connect: 80, udp-echo, tcp-echo: 7, dns: 53, ftp: 21, twamp: 862).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "quality-measured-method": {
            "type": "option",
            "help": "Method to measure the quality of tcp-connect.",
            "default": "half-open",
            "options": ["half-open", "half-close"],
        },
        "security-mode": {
            "type": "option",
            "help": "Twamp controller security mode.",
            "default": "none",
            "options": ["none", "authentication"],
        },
        "user": {
            "type": "string",
            "help": "The user name to access probe server.",
            "default": "",
            "max_length": 64,
        },
        "password": {
            "type": "password",
            "help": "TWAMP controller password in authentication mode.",
            "max_length": 128,
        },
        "packet-size": {
            "type": "integer",
            "help": "Packet size of a TWAMP test session. (124/158 - 1024)",
            "default": 124,
            "min_value": 0,
            "max_value": 65535,
        },
        "ha-priority": {
            "type": "integer",
            "help": "HA election priority (1 - 50).",
            "default": 1,
            "min_value": 1,
            "max_value": 50,
        },
        "ftp-mode": {
            "type": "option",
            "help": "FTP mode.",
            "default": "passive",
            "options": ["passive", "port"],
        },
        "ftp-file": {
            "type": "string",
            "help": "Full path and file name on the FTP server to download for FTP health-check to probe.",
            "default": "",
            "max_length": 254,
        },
        "http-get": {
            "type": "string",
            "help": "URL used to communicate with the server if the protocol if the protocol is HTTP.",
            "default": "/",
            "max_length": 1024,
        },
        "http-agent": {
            "type": "string",
            "help": "String in the http-agent field in the HTTP header.",
            "default": "Chrome/ Safari/",
            "max_length": 1024,
        },
        "http-match": {
            "type": "string",
            "help": "Response string expected from the server if the protocol is HTTP.",
            "default": "",
            "max_length": 1024,
        },
        "dns-request-domain": {
            "type": "string",
            "help": "Fully qualified domain name to resolve for the DNS probe.",
            "default": "www.example.com",
            "max_length": 255,
        },
        "dns-match-ip": {
            "type": "ipv4-address",
            "help": "Response IP expected from DNS server if the protocol is DNS.",
            "default": "0.0.0.0",
        },
        "interval": {
            "type": "integer",
            "help": "Status check interval in milliseconds, or the time between attempting to connect to the server (20 - 3600*1000 msec, default = 500).",
            "default": 500,
            "min_value": 20,
            "max_value": 3600000,
        },
        "probe-timeout": {
            "type": "integer",
            "help": "Time to wait before a probe packet is considered lost (20 - 3600*1000 msec, default = 500).",
            "default": 500,
            "min_value": 20,
            "max_value": 3600000,
        },
        "agent-probe-timeout": {
            "type": "integer",
            "help": "Time to wait before a probe packet is considered lost when detect-mode is agent (5000 - 3600*1000 msec, default = 60000).",
            "default": 60000,
            "min_value": 5000,
            "max_value": 3600000,
        },
        "remote-probe-timeout": {
            "type": "integer",
            "help": "Time to wait before a probe packet is considered lost when detect-mode is remote (20 - 3600*1000 msec, default = 5000).",
            "default": 5000,
            "min_value": 20,
            "max_value": 3600000,
        },
        "failtime": {
            "type": "integer",
            "help": "Number of failures before server is considered lost (1 - 3600, default = 5).",
            "default": 5,
            "min_value": 1,
            "max_value": 3600,
        },
        "recoverytime": {
            "type": "integer",
            "help": "Number of successful responses received before server is considered recovered (1 - 3600, default = 5).",
            "default": 5,
            "min_value": 1,
            "max_value": 3600,
        },
        "probe-count": {
            "type": "integer",
            "help": "Number of most recent probes that should be used to calculate latency and jitter (5 - 30, default = 30).",
            "default": 30,
            "min_value": 5,
            "max_value": 30,
        },
        "diffservcode": {
            "type": "user",
            "help": "Differentiated services code point (DSCP) in the IP header of the probe packet.",
            "default": "",
        },
        "update-cascade-interface": {
            "type": "option",
            "help": "Enable/disable update cascade interface.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "update-static-route": {
            "type": "option",
            "help": "Enable/disable updating the static route.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "update-bgp-route": {
            "type": "option",
            "help": "Enable/disable updating the BGP route.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "embed-measured-health": {
            "type": "option",
            "help": "Enable/disable embedding measured health information.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "sla-id-redistribute": {
            "type": "integer",
            "help": "Select the ID from the SLA sub-table. The selected SLA's priority value will be distributed into the routing table (0 - 32, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 32,
        },
        "sla-fail-log-period": {
            "type": "integer",
            "help": "Time interval in seconds that SLA fail log messages will be generated (0 - 3600, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 3600,
        },
        "sla-pass-log-period": {
            "type": "integer",
            "help": "Time interval in seconds that SLA pass log messages will be generated (0 - 3600, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 3600,
        },
        "threshold-warning-packetloss": {
            "type": "integer",
            "help": "Warning threshold for packet loss (percentage, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 100,
        },
        "threshold-alert-packetloss": {
            "type": "integer",
            "help": "Alert threshold for packet loss (percentage, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 100,
        },
        "threshold-warning-latency": {
            "type": "integer",
            "help": "Warning threshold for latency (ms, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "threshold-alert-latency": {
            "type": "integer",
            "help": "Alert threshold for latency (ms, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "threshold-warning-jitter": {
            "type": "integer",
            "help": "Warning threshold for jitter (ms, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "threshold-alert-jitter": {
            "type": "integer",
            "help": "Alert threshold for jitter (ms, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "vrf": {
            "type": "integer",
            "help": "Virtual Routing Forwarding ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 511,
        },
        "source": {
            "type": "ipv4-address",
            "help": "Source IP address used in the health-check packet to the server.",
            "default": "0.0.0.0",
        },
        "source6": {
            "type": "ipv6-address",
            "help": "Source IPv6 address used in the health-check packet to server.",
            "default": "::",
        },
        "members": {
            "type": "string",
            "help": "Member sequence number list.",
        },
        "mos-codec": {
            "type": "option",
            "help": "Codec to use for MOS calculation (default = g711).",
            "default": "g711",
            "options": ["g711", "g722", "g729"],
        },
        "class-id": {
            "type": "integer",
            "help": "Traffic class ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "packet-loss-weight": {
            "type": "integer",
            "help": "Coefficient of packet-loss in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "latency-weight": {
            "type": "integer",
            "help": "Coefficient of latency in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "jitter-weight": {
            "type": "integer",
            "help": "Coefficient of jitter in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "bandwidth-weight": {
            "type": "integer",
            "help": "Coefficient of reciprocal of available bidirectional bandwidth in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "sla": {
            "type": "string",
            "help": "Service level agreement (SLA).",
        },
    },
    "service": {
        "id": {
            "type": "integer",
            "help": "SD-WAN rule ID (1 - 4000).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4000,
        },
        "name": {
            "type": "string",
            "help": "SD-WAN rule name.",
            "default": "",
            "max_length": 35,
        },
        "addr-mode": {
            "type": "option",
            "help": "Address mode (IPv4 or IPv6).",
            "default": "ipv4",
            "options": ["ipv4", "ipv6"],
        },
        "load-balance": {
            "type": "option",
            "help": "Enable/disable load-balance.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "input-device": {
            "type": "string",
            "help": "Source interface name.",
        },
        "input-device-negate": {
            "type": "option",
            "help": "Enable/disable negation of input device match.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "input-zone": {
            "type": "string",
            "help": "Source input-zone name.",
        },
        "mode": {
            "type": "option",
            "help": "Control how the SD-WAN rule sets the priority of interfaces in the SD-WAN.",
            "default": "manual",
            "options": ["auto", "manual", "priority", "sla"],
        },
        "zone-mode": {
            "type": "option",
            "help": "Enable/disable zone mode.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "minimum-sla-meet-members": {
            "type": "integer",
            "help": "Minimum number of members which meet SLA.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "hash-mode": {
            "type": "option",
            "help": "Hash algorithm for selected priority members for load balance mode.",
            "default": "round-robin",
            "options": ["round-robin", "source-ip-based", "source-dest-ip-based", "inbandwidth", "outbandwidth", "bibandwidth"],
        },
        "shortcut-priority": {
            "type": "option",
            "help": "High priority of ADVPN shortcut for this service.",
            "default": "auto",
            "options": ["enable", "disable", "auto"],
        },
        "role": {
            "type": "option",
            "help": "Service role to work with neighbor.",
            "default": "standalone",
            "options": ["standalone", "primary", "secondary"],
        },
        "standalone-action": {
            "type": "option",
            "help": "Enable/disable service when selected neighbor role is standalone while service role is not standalone.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "quality-link": {
            "type": "integer",
            "help": "Quality grade.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "tos": {
            "type": "user",
            "help": "Type of service bit pattern.",
            "default": "",
        },
        "tos-mask": {
            "type": "user",
            "help": "Type of service evaluated bits.",
            "default": "",
        },
        "protocol": {
            "type": "integer",
            "help": "Protocol number.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "start-port": {
            "type": "integer",
            "help": "Start destination port number.",
            "default": 1,
            "min_value": 0,
            "max_value": 65535,
        },
        "end-port": {
            "type": "integer",
            "help": "End destination port number.",
            "default": 65535,
            "min_value": 0,
            "max_value": 65535,
        },
        "start-src-port": {
            "type": "integer",
            "help": "Start source port number.",
            "default": 1,
            "min_value": 0,
            "max_value": 65535,
        },
        "end-src-port": {
            "type": "integer",
            "help": "End source port number.",
            "default": 65535,
            "min_value": 0,
            "max_value": 65535,
        },
        "dst": {
            "type": "string",
            "help": "Destination address name.",
        },
        "dst-negate": {
            "type": "option",
            "help": "Enable/disable negation of destination address match.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "src": {
            "type": "string",
            "help": "Source address name.",
        },
        "dst6": {
            "type": "string",
            "help": "Destination address6 name.",
        },
        "src6": {
            "type": "string",
            "help": "Source address6 name.",
        },
        "src-negate": {
            "type": "option",
            "help": "Enable/disable negation of source address match.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "users": {
            "type": "string",
            "help": "User name.",
        },
        "groups": {
            "type": "string",
            "help": "User groups.",
        },
        "internet-service": {
            "type": "option",
            "help": "Enable/disable use of Internet service for application-based load balancing.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "internet-service-custom": {
            "type": "string",
            "help": "Custom Internet service name list.",
        },
        "internet-service-custom-group": {
            "type": "string",
            "help": "Custom Internet Service group list.",
        },
        "internet-service-fortiguard": {
            "type": "string",
            "help": "FortiGuard Internet service name list.",
        },
        "internet-service-name": {
            "type": "string",
            "help": "Internet service name list.",
        },
        "internet-service-group": {
            "type": "string",
            "help": "Internet Service group list.",
        },
        "internet-service-app-ctrl": {
            "type": "string",
            "help": "Application control based Internet Service ID list.",
        },
        "internet-service-app-ctrl-group": {
            "type": "string",
            "help": "Application control based Internet Service group list.",
        },
        "internet-service-app-ctrl-category": {
            "type": "string",
            "help": "IDs of one or more application control categories.",
        },
        "health-check": {
            "type": "string",
            "help": "Health check list.",
        },
        "link-cost-factor": {
            "type": "option",
            "help": "Link cost factor.",
            "default": "latency",
            "options": ["latency", "jitter", "packet-loss", "inbandwidth", "outbandwidth", "bibandwidth", "custom-profile-1"],
        },
        "packet-loss-weight": {
            "type": "integer",
            "help": "Coefficient of packet-loss in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "latency-weight": {
            "type": "integer",
            "help": "Coefficient of latency in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "jitter-weight": {
            "type": "integer",
            "help": "Coefficient of jitter in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "bandwidth-weight": {
            "type": "integer",
            "help": "Coefficient of reciprocal of available bidirectional bandwidth in the formula of custom-profile-1.",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "link-cost-threshold": {
            "type": "integer",
            "help": "Percentage threshold change of link cost values that will result in policy route regeneration (0 - 10000000, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 10000000,
        },
        "hold-down-time": {
            "type": "integer",
            "help": "Waiting period in seconds when switching from the back-up member to the primary member (0 - 10000000, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 10000000,
        },
        "sla-stickiness": {
            "type": "option",
            "help": "Enable/disable SLA stickiness (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dscp-forward": {
            "type": "option",
            "help": "Enable/disable forward traffic DSCP tag.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dscp-reverse": {
            "type": "option",
            "help": "Enable/disable reverse traffic DSCP tag.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dscp-forward-tag": {
            "type": "user",
            "help": "Forward traffic DSCP tag.",
            "default": "",
        },
        "dscp-reverse-tag": {
            "type": "user",
            "help": "Reverse traffic DSCP tag.",
            "default": "",
        },
        "sla": {
            "type": "string",
            "help": "Service level agreement (SLA).",
        },
        "priority-members": {
            "type": "string",
            "help": "Member sequence number list.",
        },
        "priority-zone": {
            "type": "string",
            "help": "Priority zone name list.",
        },
        "status": {
            "type": "option",
            "help": "Enable/disable SD-WAN service.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "gateway": {
            "type": "option",
            "help": "Enable/disable SD-WAN service gateway.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "default": {
            "type": "option",
            "help": "Enable/disable use of SD-WAN as default service.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "sla-compare-method": {
            "type": "option",
            "help": "Method to compare SLA value for SLA mode.",
            "default": "order",
            "options": ["order", "number"],
        },
        "fib-best-match-force": {
            "type": "option",
            "help": "Enable/disable force using fib-best-match oif as outgoing interface.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tie-break": {
            "type": "option",
            "help": "Method of selecting member if more than one meets the SLA.",
            "default": "zone",
            "options": ["zone", "cfg-order", "fib-best-match", "priority", "input-device"],
        },
        "use-shortcut-sla": {
            "type": "option",
            "help": "Enable/disable use of ADVPN shortcut for quality comparison.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "passive-measurement": {
            "type": "option",
            "help": "Enable/disable passive measurement based on the service criteria.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "agent-exclusive": {
            "type": "option",
            "help": "Set/unset the service as agent use exclusively.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "shortcut": {
            "type": "option",
            "help": "Enable/disable shortcut for this service.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "comment": {
            "type": "var-string",
            "help": "Comments.",
            "max_length": 255,
        },
    },
    "neighbor": {
        "ip": {
            "type": "string",
            "help": "IP/IPv6 address of neighbor or neighbor-group name.",
            "required": True,
            "default": "",
            "max_length": 45,
        },
        "member": {
            "type": "string",
            "help": "Member sequence number list.",
        },
        "service-id": {
            "type": "integer",
            "help": "SD-WAN service ID to work with the neighbor.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "minimum-sla-meet-members": {
            "type": "integer",
            "help": "Minimum number of members which meet SLA when the neighbor is preferred.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "mode": {
            "type": "option",
            "help": "What metric to select the neighbor.",
            "default": "sla",
            "options": ["sla", "speedtest"],
        },
        "role": {
            "type": "option",
            "help": "Role of neighbor.",
            "default": "standalone",
            "options": ["standalone", "primary", "secondary"],
        },
        "route-metric": {
            "type": "option",
            "help": "Route-metric of neighbor.",
            "default": "preferable",
            "options": ["preferable", "priority"],
        },
        "health-check": {
            "type": "string",
            "help": "SD-WAN health-check name.",
            "default": "",
            "max_length": 35,
        },
        "sla-id": {
            "type": "integer",
            "help": "SLA ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "duplication": {
        "id": {
            "type": "integer",
            "help": "Duplication rule ID (1 - 255).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 255,
        },
        "service-id": {
            "type": "string",
            "help": "SD-WAN service rule ID list.",
        },
        "srcaddr": {
            "type": "string",
            "help": "Source address or address group names.",
        },
        "dstaddr": {
            "type": "string",
            "help": "Destination address or address group names.",
        },
        "srcaddr6": {
            "type": "string",
            "help": "Source address6 or address6 group names.",
        },
        "dstaddr6": {
            "type": "string",
            "help": "Destination address6 or address6 group names.",
        },
        "srcintf": {
            "type": "string",
            "help": "Incoming (ingress) interfaces or zones.",
        },
        "dstintf": {
            "type": "string",
            "help": "Outgoing (egress) interfaces or zones.",
        },
        "service": {
            "type": "string",
            "help": "Service and service group name.",
        },
        "packet-duplication": {
            "type": "option",
            "help": "Configure packet duplication method.",
            "default": "disable",
            "options": ["disable", "force", "on-demand"],
        },
        "sla-match-service": {
            "type": "option",
            "help": "Enable/disable packet duplication matching health-check SLAs in service rule.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "packet-de-duplication": {
            "type": "option",
            "help": "Enable/disable discarding of packets that have been duplicated.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_LOAD_BALANCE_MODE = [
    "source-ip-based",
    "weight-based",
    "usage-based",
    "source-dest-ip-based",
    "measured-volume-based",
]
VALID_BODY_SPEEDTEST_BYPASS_ROUTING = [
    "disable",
    "enable",
]
VALID_BODY_NEIGHBOR_HOLD_DOWN = [
    "enable",
    "disable",
]
VALID_BODY_FAIL_DETECT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_sdwan_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/sdwan."""
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


def validate_system_sdwan_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/sdwan object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "load-balance-mode" in payload:
        is_valid, error = _validate_enum_field(
            "load-balance-mode",
            payload["load-balance-mode"],
            VALID_BODY_LOAD_BALANCE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "speedtest-bypass-routing" in payload:
        is_valid, error = _validate_enum_field(
            "speedtest-bypass-routing",
            payload["speedtest-bypass-routing"],
            VALID_BODY_SPEEDTEST_BYPASS_ROUTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "neighbor-hold-down" in payload:
        is_valid, error = _validate_enum_field(
            "neighbor-hold-down",
            payload["neighbor-hold-down"],
            VALID_BODY_NEIGHBOR_HOLD_DOWN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-detect" in payload:
        is_valid, error = _validate_enum_field(
            "fail-detect",
            payload["fail-detect"],
            VALID_BODY_FAIL_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_sdwan_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/sdwan."""
    # Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "load-balance-mode" in payload:
        is_valid, error = _validate_enum_field(
            "load-balance-mode",
            payload["load-balance-mode"],
            VALID_BODY_LOAD_BALANCE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "speedtest-bypass-routing" in payload:
        is_valid, error = _validate_enum_field(
            "speedtest-bypass-routing",
            payload["speedtest-bypass-routing"],
            VALID_BODY_SPEEDTEST_BYPASS_ROUTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "neighbor-hold-down" in payload:
        is_valid, error = _validate_enum_field(
            "neighbor-hold-down",
            payload["neighbor-hold-down"],
            VALID_BODY_NEIGHBOR_HOLD_DOWN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-detect" in payload:
        is_valid, error = _validate_enum_field(
            "fail-detect",
            payload["fail-detect"],
            VALID_BODY_FAIL_DETECT,
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
    "endpoint": "system/sdwan",
    "category": "cmdb",
    "api_path": "system/sdwan",
    "help": "Configure redundant Internet connections with multiple outbound links and health-check profiles.",
    "total_fields": 17,
    "required_fields_count": 0,
    "fields_with_defaults_count": 10,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
