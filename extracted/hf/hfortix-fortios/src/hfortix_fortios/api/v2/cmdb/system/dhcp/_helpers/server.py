"""Validation helpers for system/dhcp/server - Auto-generated"""

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
    "interface",  # DHCP server can assign IP configurations to clients connected to this interface.
    "timezone",  # Select the time zone to be assigned to DHCP clients.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "status": "enable",
    "lease-time": 604800,
    "mac-acl-default-action": "assign",
    "forticlient-on-net-status": "enable",
    "dns-service": "specify",
    "dns-server1": "0.0.0.0",
    "dns-server2": "0.0.0.0",
    "dns-server3": "0.0.0.0",
    "dns-server4": "0.0.0.0",
    "wifi-ac-service": "specify",
    "wifi-ac1": "0.0.0.0",
    "wifi-ac2": "0.0.0.0",
    "wifi-ac3": "0.0.0.0",
    "ntp-service": "specify",
    "ntp-server1": "0.0.0.0",
    "ntp-server2": "0.0.0.0",
    "ntp-server3": "0.0.0.0",
    "domain": "",
    "wins-server1": "0.0.0.0",
    "wins-server2": "0.0.0.0",
    "default-gateway": "0.0.0.0",
    "next-server": "0.0.0.0",
    "netmask": "0.0.0.0",
    "interface": "",
    "timezone-option": "disable",
    "timezone": "",
    "filename": "",
    "server-type": "regular",
    "ip-mode": "range",
    "conflicted-ip-timeout": 1800,
    "ipsec-lease-hold": 60,
    "auto-configuration": "enable",
    "dhcp-settings-from-fortiipam": "disable",
    "auto-managed-status": "enable",
    "ddns-update": "disable",
    "ddns-update-override": "disable",
    "ddns-server-ip": "0.0.0.0",
    "ddns-zone": "",
    "ddns-auth": "disable",
    "ddns-keyname": "",
    "ddns-ttl": 300,
    "vci-match": "disable",
    "shared-subnet": "disable",
    "relay-agent": "0.0.0.0",
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
    "id": "integer",  # ID.
    "status": "option",  # Enable/disable this DHCP configuration.
    "lease-time": "integer",  # Lease time in seconds, 0 means unlimited.
    "mac-acl-default-action": "option",  # MAC access control default action (allow or block assigning IP settings).
    "forticlient-on-net-status": "option",  # Enable/disable FortiClient-On-Net service for this DHCP server.
    "dns-service": "option",  # Options for assigning DNS servers to DHCP clients.
    "dns-server1": "ipv4-address",  # DNS server 1.
    "dns-server2": "ipv4-address",  # DNS server 2.
    "dns-server3": "ipv4-address",  # DNS server 3.
    "dns-server4": "ipv4-address",  # DNS server 4.
    "wifi-ac-service": "option",  # Options for assigning WiFi access controllers to DHCP clients.
    "wifi-ac1": "ipv4-address",  # WiFi Access Controller 1 IP address (DHCP option 138, RFC 5417).
    "wifi-ac2": "ipv4-address",  # WiFi Access Controller 2 IP address (DHCP option 138, RFC 5417).
    "wifi-ac3": "ipv4-address",  # WiFi Access Controller 3 IP address (DHCP option 138, RFC 5417).
    "ntp-service": "option",  # Options for assigning Network Time Protocol (NTP) servers to DHCP clients.
    "ntp-server1": "ipv4-address",  # NTP server 1.
    "ntp-server2": "ipv4-address",  # NTP server 2.
    "ntp-server3": "ipv4-address",  # NTP server 3.
    "domain": "string",  # Domain name suffix for the IP addresses that the DHCP server assigns to clients.
    "wins-server1": "ipv4-address",  # WINS server 1.
    "wins-server2": "ipv4-address",  # WINS server 2.
    "default-gateway": "ipv4-address",  # Default gateway IP address assigned by the DHCP server.
    "next-server": "ipv4-address",  # IP address of a server (for example, a TFTP sever) that DHCP clients can downloa
    "netmask": "ipv4-netmask",  # Netmask assigned by the DHCP server.
    "interface": "string",  # DHCP server can assign IP configurations to clients connected to this interface.
    "ip-range": "string",  # DHCP IP range configuration.
    "timezone-option": "option",  # Options for the DHCP server to set the client's time zone.
    "timezone": "string",  # Select the time zone to be assigned to DHCP clients.
    "tftp-server": "string",  # One or more hostnames or IP addresses of the TFTP servers in quotes separated by
    "filename": "string",  # Name of the boot file on the TFTP server.
    "options": "string",  # DHCP options.
    "server-type": "option",  # DHCP server can be a normal DHCP server or an IPsec DHCP server.
    "ip-mode": "option",  # Method used to assign client IP.
    "conflicted-ip-timeout": "integer",  # Time in seconds to wait after a conflicted IP address is removed from the DHCP r
    "ipsec-lease-hold": "integer",  # DHCP over IPsec leases expire this many seconds after tunnel down (0 to disable 
    "auto-configuration": "option",  # Enable/disable auto configuration.
    "dhcp-settings-from-fortiipam": "option",  # Enable/disable populating of DHCP server settings from FortiIPAM.
    "auto-managed-status": "option",  # Enable/disable use of this DHCP server once this interface has been assigned an 
    "ddns-update": "option",  # Enable/disable DDNS update for DHCP.
    "ddns-update-override": "option",  # Enable/disable DDNS update override for DHCP.
    "ddns-server-ip": "ipv4-address",  # DDNS server IP.
    "ddns-zone": "string",  # Zone of your domain name (ex. DDNS.com).
    "ddns-auth": "option",  # DDNS authentication mode.
    "ddns-keyname": "string",  # DDNS update key name.
    "ddns-key": "password_aes256",  # DDNS update key (base 64 encoding).
    "ddns-ttl": "integer",  # TTL.
    "vci-match": "option",  # Enable/disable vendor class identifier (VCI) matching. When enabled only DHCP re
    "vci-string": "string",  # One or more VCI strings in quotes separated by spaces.
    "exclude-range": "string",  # Exclude one or more ranges of IP addresses from being assigned to clients.
    "shared-subnet": "option",  # Enable/disable shared subnet.
    "relay-agent": "ipv4-address",  # Relay agent IP.
    "reserved-address": "string",  # Options for the DHCP server to assign IP settings to specific MAC addresses.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "ID.",
    "status": "Enable/disable this DHCP configuration.",
    "lease-time": "Lease time in seconds, 0 means unlimited.",
    "mac-acl-default-action": "MAC access control default action (allow or block assigning IP settings).",
    "forticlient-on-net-status": "Enable/disable FortiClient-On-Net service for this DHCP server.",
    "dns-service": "Options for assigning DNS servers to DHCP clients.",
    "dns-server1": "DNS server 1.",
    "dns-server2": "DNS server 2.",
    "dns-server3": "DNS server 3.",
    "dns-server4": "DNS server 4.",
    "wifi-ac-service": "Options for assigning WiFi access controllers to DHCP clients.",
    "wifi-ac1": "WiFi Access Controller 1 IP address (DHCP option 138, RFC 5417).",
    "wifi-ac2": "WiFi Access Controller 2 IP address (DHCP option 138, RFC 5417).",
    "wifi-ac3": "WiFi Access Controller 3 IP address (DHCP option 138, RFC 5417).",
    "ntp-service": "Options for assigning Network Time Protocol (NTP) servers to DHCP clients.",
    "ntp-server1": "NTP server 1.",
    "ntp-server2": "NTP server 2.",
    "ntp-server3": "NTP server 3.",
    "domain": "Domain name suffix for the IP addresses that the DHCP server assigns to clients.",
    "wins-server1": "WINS server 1.",
    "wins-server2": "WINS server 2.",
    "default-gateway": "Default gateway IP address assigned by the DHCP server.",
    "next-server": "IP address of a server (for example, a TFTP sever) that DHCP clients can download a boot file from.",
    "netmask": "Netmask assigned by the DHCP server.",
    "interface": "DHCP server can assign IP configurations to clients connected to this interface.",
    "ip-range": "DHCP IP range configuration.",
    "timezone-option": "Options for the DHCP server to set the client's time zone.",
    "timezone": "Select the time zone to be assigned to DHCP clients.",
    "tftp-server": "One or more hostnames or IP addresses of the TFTP servers in quotes separated by spaces.",
    "filename": "Name of the boot file on the TFTP server.",
    "options": "DHCP options.",
    "server-type": "DHCP server can be a normal DHCP server or an IPsec DHCP server.",
    "ip-mode": "Method used to assign client IP.",
    "conflicted-ip-timeout": "Time in seconds to wait after a conflicted IP address is removed from the DHCP range before it can be reused.",
    "ipsec-lease-hold": "DHCP over IPsec leases expire this many seconds after tunnel down (0 to disable forced-expiry).",
    "auto-configuration": "Enable/disable auto configuration.",
    "dhcp-settings-from-fortiipam": "Enable/disable populating of DHCP server settings from FortiIPAM.",
    "auto-managed-status": "Enable/disable use of this DHCP server once this interface has been assigned an IP address from FortiIPAM.",
    "ddns-update": "Enable/disable DDNS update for DHCP.",
    "ddns-update-override": "Enable/disable DDNS update override for DHCP.",
    "ddns-server-ip": "DDNS server IP.",
    "ddns-zone": "Zone of your domain name (ex. DDNS.com).",
    "ddns-auth": "DDNS authentication mode.",
    "ddns-keyname": "DDNS update key name.",
    "ddns-key": "DDNS update key (base 64 encoding).",
    "ddns-ttl": "TTL.",
    "vci-match": "Enable/disable vendor class identifier (VCI) matching. When enabled only DHCP requests with a matching VCI are served.",
    "vci-string": "One or more VCI strings in quotes separated by spaces.",
    "exclude-range": "Exclude one or more ranges of IP addresses from being assigned to clients.",
    "shared-subnet": "Enable/disable shared subnet.",
    "relay-agent": "Relay agent IP.",
    "reserved-address": "Options for the DHCP server to assign IP settings to specific MAC addresses.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "lease-time": {"type": "integer", "min": 300, "max": 8640000},
    "domain": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 15},
    "timezone": {"type": "string", "max_length": 63},
    "filename": {"type": "string", "max_length": 127},
    "conflicted-ip-timeout": {"type": "integer", "min": 60, "max": 8640000},
    "ipsec-lease-hold": {"type": "integer", "min": 0, "max": 8640000},
    "ddns-zone": {"type": "string", "max_length": 64},
    "ddns-keyname": {"type": "string", "max_length": 64},
    "ddns-ttl": {"type": "integer", "min": 60, "max": 86400},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ip-range": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "start-ip": {
            "type": "ipv4-address",
            "help": "Start of IP range.",
            "required": True,
            "default": "0.0.0.0",
        },
        "end-ip": {
            "type": "ipv4-address",
            "help": "End of IP range.",
            "required": True,
            "default": "0.0.0.0",
        },
        "vci-match": {
            "type": "option",
            "help": "Enable/disable vendor class identifier (VCI) matching. When enabled only DHCP requests with a matching VCI are served with this range.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "vci-string": {
            "type": "string",
            "help": "One or more VCI strings in quotes separated by spaces.",
        },
        "uci-match": {
            "type": "option",
            "help": "Enable/disable user class identifier (UCI) matching. When enabled only DHCP requests with a matching UCI are served with this range.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "uci-string": {
            "type": "string",
            "help": "One or more UCI strings in quotes separated by spaces.",
        },
        "lease-time": {
            "type": "integer",
            "help": "Lease time in seconds, 0 means default lease time.",
            "default": 0,
            "min_value": 300,
            "max_value": 8640000,
        },
    },
    "tftp-server": {
        "tftp-server": {
            "type": "string",
            "help": "TFTP server.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
    },
    "options": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "code": {
            "type": "integer",
            "help": "DHCP option code.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "type": {
            "type": "option",
            "help": "DHCP option type.",
            "default": "hex",
            "options": ["hex", "string", "ip", "fqdn"],
        },
        "value": {
            "type": "string",
            "help": "DHCP option value.",
            "default": "",
            "max_length": 312,
        },
        "ip": {
            "type": "user",
            "help": "DHCP option IPs.",
            "default": "",
        },
        "vci-match": {
            "type": "option",
            "help": "Enable/disable vendor class identifier (VCI) matching. When enabled only DHCP requests with a matching VCI are served with this option.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "vci-string": {
            "type": "string",
            "help": "One or more VCI strings in quotes separated by spaces.",
        },
        "uci-match": {
            "type": "option",
            "help": "Enable/disable user class identifier (UCI) matching. When enabled only DHCP requests with a matching UCI are served with this option.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "uci-string": {
            "type": "string",
            "help": "One or more UCI strings in quotes separated by spaces.",
        },
    },
    "vci-string": {
        "vci-string": {
            "type": "string",
            "help": "VCI strings.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
    },
    "exclude-range": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "start-ip": {
            "type": "ipv4-address",
            "help": "Start of IP range.",
            "required": True,
            "default": "0.0.0.0",
        },
        "end-ip": {
            "type": "ipv4-address",
            "help": "End of IP range.",
            "required": True,
            "default": "0.0.0.0",
        },
        "vci-match": {
            "type": "option",
            "help": "Enable/disable vendor class identifier (VCI) matching. When enabled only DHCP requests with a matching VCI are served with this range.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "vci-string": {
            "type": "string",
            "help": "One or more VCI strings in quotes separated by spaces.",
        },
        "uci-match": {
            "type": "option",
            "help": "Enable/disable user class identifier (UCI) matching. When enabled only DHCP requests with a matching UCI are served with this range.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "uci-string": {
            "type": "string",
            "help": "One or more UCI strings in quotes separated by spaces.",
        },
        "lease-time": {
            "type": "integer",
            "help": "Lease time in seconds, 0 means default lease time.",
            "default": 0,
            "min_value": 300,
            "max_value": 8640000,
        },
    },
    "reserved-address": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "type": {
            "type": "option",
            "help": "DHCP reserved-address type.",
            "default": "mac",
            "options": ["mac", "option82"],
        },
        "ip": {
            "type": "ipv4-address",
            "help": "IP address to be reserved for the MAC address.",
            "required": True,
            "default": "0.0.0.0",
        },
        "mac": {
            "type": "mac-address",
            "help": "MAC address of the client that will get the reserved IP address.",
            "required": True,
            "default": "00:00:00:00:00:00",
        },
        "action": {
            "type": "option",
            "help": "Options for the DHCP server to configure the client with the reserved MAC address.",
            "default": "reserved",
            "options": ["assign", "block", "reserved"],
        },
        "circuit-id-type": {
            "type": "option",
            "help": "DHCP option type.",
            "default": "string",
            "options": ["hex", "string"],
        },
        "circuit-id": {
            "type": "string",
            "help": "Option 82 circuit-ID of the client that will get the reserved IP address.",
            "default": "",
            "max_length": 312,
        },
        "remote-id-type": {
            "type": "option",
            "help": "DHCP option type.",
            "default": "string",
            "options": ["hex", "string"],
        },
        "remote-id": {
            "type": "string",
            "help": "Option 82 remote-ID of the client that will get the reserved IP address.",
            "default": "",
            "max_length": 312,
        },
        "description": {
            "type": "var-string",
            "help": "Description.",
            "max_length": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_MAC_ACL_DEFAULT_ACTION = [
    "assign",
    "block",
]
VALID_BODY_FORTICLIENT_ON_NET_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_DNS_SERVICE = [
    "local",
    "default",
    "specify",
]
VALID_BODY_WIFI_AC_SERVICE = [
    "specify",
    "local",
]
VALID_BODY_NTP_SERVICE = [
    "local",
    "default",
    "specify",
]
VALID_BODY_TIMEZONE_OPTION = [
    "disable",
    "default",
    "specify",
]
VALID_BODY_SERVER_TYPE = [
    "regular",
    "ipsec",
]
VALID_BODY_IP_MODE = [
    "range",
    "usrgrp",
]
VALID_BODY_AUTO_CONFIGURATION = [
    "disable",
    "enable",
]
VALID_BODY_DHCP_SETTINGS_FROM_FORTIIPAM = [
    "disable",
    "enable",
]
VALID_BODY_AUTO_MANAGED_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_DDNS_UPDATE = [
    "disable",
    "enable",
]
VALID_BODY_DDNS_UPDATE_OVERRIDE = [
    "disable",
    "enable",
]
VALID_BODY_DDNS_AUTH = [
    "disable",
    "tsig",
]
VALID_BODY_VCI_MATCH = [
    "disable",
    "enable",
]
VALID_BODY_SHARED_SUBNET = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_dhcp_server_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/dhcp/server."""
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


def validate_system_dhcp_server_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/dhcp/server object."""
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
    if "mac-acl-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "mac-acl-default-action",
            payload["mac-acl-default-action"],
            VALID_BODY_MAC_ACL_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticlient-on-net-status" in payload:
        is_valid, error = _validate_enum_field(
            "forticlient-on-net-status",
            payload["forticlient-on-net-status"],
            VALID_BODY_FORTICLIENT_ON_NET_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-service" in payload:
        is_valid, error = _validate_enum_field(
            "dns-service",
            payload["dns-service"],
            VALID_BODY_DNS_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wifi-ac-service" in payload:
        is_valid, error = _validate_enum_field(
            "wifi-ac-service",
            payload["wifi-ac-service"],
            VALID_BODY_WIFI_AC_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ntp-service" in payload:
        is_valid, error = _validate_enum_field(
            "ntp-service",
            payload["ntp-service"],
            VALID_BODY_NTP_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "timezone-option" in payload:
        is_valid, error = _validate_enum_field(
            "timezone-option",
            payload["timezone-option"],
            VALID_BODY_TIMEZONE_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ip-mode",
            payload["ip-mode"],
            VALID_BODY_IP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-configuration" in payload:
        is_valid, error = _validate_enum_field(
            "auto-configuration",
            payload["auto-configuration"],
            VALID_BODY_AUTO_CONFIGURATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-settings-from-fortiipam" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-settings-from-fortiipam",
            payload["dhcp-settings-from-fortiipam"],
            VALID_BODY_DHCP_SETTINGS_FROM_FORTIIPAM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-managed-status" in payload:
        is_valid, error = _validate_enum_field(
            "auto-managed-status",
            payload["auto-managed-status"],
            VALID_BODY_AUTO_MANAGED_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ddns-update" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-update",
            payload["ddns-update"],
            VALID_BODY_DDNS_UPDATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ddns-update-override" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-update-override",
            payload["ddns-update-override"],
            VALID_BODY_DDNS_UPDATE_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ddns-auth" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-auth",
            payload["ddns-auth"],
            VALID_BODY_DDNS_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vci-match" in payload:
        is_valid, error = _validate_enum_field(
            "vci-match",
            payload["vci-match"],
            VALID_BODY_VCI_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "shared-subnet" in payload:
        is_valid, error = _validate_enum_field(
            "shared-subnet",
            payload["shared-subnet"],
            VALID_BODY_SHARED_SUBNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_dhcp_server_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/dhcp/server."""
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
    if "mac-acl-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "mac-acl-default-action",
            payload["mac-acl-default-action"],
            VALID_BODY_MAC_ACL_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticlient-on-net-status" in payload:
        is_valid, error = _validate_enum_field(
            "forticlient-on-net-status",
            payload["forticlient-on-net-status"],
            VALID_BODY_FORTICLIENT_ON_NET_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-service" in payload:
        is_valid, error = _validate_enum_field(
            "dns-service",
            payload["dns-service"],
            VALID_BODY_DNS_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wifi-ac-service" in payload:
        is_valid, error = _validate_enum_field(
            "wifi-ac-service",
            payload["wifi-ac-service"],
            VALID_BODY_WIFI_AC_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ntp-service" in payload:
        is_valid, error = _validate_enum_field(
            "ntp-service",
            payload["ntp-service"],
            VALID_BODY_NTP_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "timezone-option" in payload:
        is_valid, error = _validate_enum_field(
            "timezone-option",
            payload["timezone-option"],
            VALID_BODY_TIMEZONE_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ip-mode",
            payload["ip-mode"],
            VALID_BODY_IP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-configuration" in payload:
        is_valid, error = _validate_enum_field(
            "auto-configuration",
            payload["auto-configuration"],
            VALID_BODY_AUTO_CONFIGURATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-settings-from-fortiipam" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-settings-from-fortiipam",
            payload["dhcp-settings-from-fortiipam"],
            VALID_BODY_DHCP_SETTINGS_FROM_FORTIIPAM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-managed-status" in payload:
        is_valid, error = _validate_enum_field(
            "auto-managed-status",
            payload["auto-managed-status"],
            VALID_BODY_AUTO_MANAGED_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ddns-update" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-update",
            payload["ddns-update"],
            VALID_BODY_DDNS_UPDATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ddns-update-override" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-update-override",
            payload["ddns-update-override"],
            VALID_BODY_DDNS_UPDATE_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ddns-auth" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-auth",
            payload["ddns-auth"],
            VALID_BODY_DDNS_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vci-match" in payload:
        is_valid, error = _validate_enum_field(
            "vci-match",
            payload["vci-match"],
            VALID_BODY_VCI_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "shared-subnet" in payload:
        is_valid, error = _validate_enum_field(
            "shared-subnet",
            payload["shared-subnet"],
            VALID_BODY_SHARED_SUBNET,
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
    "endpoint": "system/dhcp/server",
    "category": "cmdb",
    "api_path": "system.dhcp/server",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Configure DHCP servers.",
    "total_fields": 52,
    "required_fields_count": 2,
    "fields_with_defaults_count": 45,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
