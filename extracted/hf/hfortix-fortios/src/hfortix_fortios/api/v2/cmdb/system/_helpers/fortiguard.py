"""Validation helpers for system/fortiguard - Auto-generated"""

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
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "fortiguard-anycast": "enable",
    "fortiguard-anycast-source": "fortinet",
    "protocol": "https",
    "port": "443",
    "load-balance-servers": 1,
    "auto-join-forticloud": "enable",
    "update-server-location": "automatic",
    "sandbox-region": "",
    "sandbox-inline-scan": "disable",
    "update-ffdb": "enable",
    "update-uwdb": "enable",
    "update-dldb": "enable",
    "update-extdb": "enable",
    "update-build-proxy": "enable",
    "persistent-connection": "disable",
    "vdom": "",
    "auto-firmware-upgrade": "enable",
    "auto-firmware-upgrade-day": "",
    "auto-firmware-upgrade-delay": 3,
    "auto-firmware-upgrade-start-hour": 1,
    "auto-firmware-upgrade-end-hour": 4,
    "FDS-license-expiring-days": 15,
    "subscribe-update-notification": "disable",
    "antispam-force-off": "disable",
    "antispam-cache": "enable",
    "antispam-cache-ttl": 1800,
    "antispam-cache-mpermille": 1,
    "antispam-license": 4294967295,
    "antispam-expiration": 0,
    "antispam-timeout": 7,
    "outbreak-prevention-force-off": "disable",
    "outbreak-prevention-cache": "enable",
    "outbreak-prevention-cache-ttl": 300,
    "outbreak-prevention-cache-mpermille": 1,
    "outbreak-prevention-license": 4294967295,
    "outbreak-prevention-expiration": 0,
    "outbreak-prevention-timeout": 7,
    "webfilter-force-off": "disable",
    "webfilter-cache": "enable",
    "webfilter-cache-ttl": 3600,
    "webfilter-license": 4294967295,
    "webfilter-expiration": 0,
    "webfilter-timeout": 15,
    "sdns-server-ip": "",
    "sdns-server-port": 53,
    "anycast-sdns-server-ip": "0.0.0.0",
    "anycast-sdns-server-port": 853,
    "sdns-options": "",
    "source-ip": "0.0.0.0",
    "source-ip6": "::",
    "proxy-server-ip": "",
    "proxy-server-port": 0,
    "proxy-username": "",
    "ddns-server-ip": "0.0.0.0",
    "ddns-server-ip6": "::",
    "ddns-server-port": 443,
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
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
    "fortiguard-anycast": "option",  # Enable/disable use of FortiGuard's Anycast network.
    "fortiguard-anycast-source": "option",  # Configure which of Fortinet's servers to provide FortiGuard services in FortiGua
    "protocol": "option",  # Protocol used to communicate with the FortiGuard servers.
    "port": "option",  # Port used to communicate with the FortiGuard servers.
    "load-balance-servers": "integer",  # Number of servers to alternate between as first FortiGuard option.
    "auto-join-forticloud": "option",  # Automatically connect to and login to FortiCloud.
    "update-server-location": "option",  # Location from which to receive FortiGuard updates.
    "sandbox-region": "string",  # FortiCloud Sandbox region.
    "sandbox-inline-scan": "option",  # Enable/disable FortiCloud Sandbox inline-scan.
    "update-ffdb": "option",  # Enable/disable Internet Service Database update.
    "update-uwdb": "option",  # Enable/disable allowlist update.
    "update-dldb": "option",  # Enable/disable DLP signature update.
    "update-extdb": "option",  # Enable/disable external resource update.
    "update-build-proxy": "option",  # Enable/disable proxy dictionary rebuild.
    "persistent-connection": "option",  # Enable/disable use of persistent connection to receive update notification from 
    "vdom": "string",  # FortiGuard Service virtual domain name.
    "auto-firmware-upgrade": "option",  # Enable/disable automatic patch-level firmware upgrade from FortiGuard. The Forti
    "auto-firmware-upgrade-day": "option",  # Allowed day(s) of the week to install an automatic patch-level firmware upgrade 
    "auto-firmware-upgrade-delay": "integer",  # Delay of day(s) before installing an automatic patch-level firmware upgrade from
    "auto-firmware-upgrade-start-hour": "integer",  # Start time in the designated time window for automatic patch-level firmware upgr
    "auto-firmware-upgrade-end-hour": "integer",  # End time in the designated time window for automatic patch-level firmware upgrad
    "FDS-license-expiring-days": "integer",  # Threshold for number of days before FortiGuard license expiration to generate li
    "subscribe-update-notification": "option",  # Enable/disable subscription to receive update notification from FortiGuard.
    "antispam-force-off": "option",  # Enable/disable turning off the FortiGuard antispam service.
    "antispam-cache": "option",  # Enable/disable FortiGuard antispam request caching. Uses a small amount of memor
    "antispam-cache-ttl": "integer",  # Time-to-live for antispam cache entries in seconds (300 - 86400). Lower times re
    "antispam-cache-mpermille": "integer",  # Maximum permille of FortiGate memory the antispam cache is allowed to use (1 - 1
    "antispam-license": "integer",  # Interval of time between license checks for the FortiGuard antispam contract.
    "antispam-expiration": "integer",  # Expiration date of the FortiGuard antispam contract.
    "antispam-timeout": "integer",  # Antispam query time out (1 - 30 sec, default = 7).
    "outbreak-prevention-force-off": "option",  # Turn off FortiGuard Virus Outbreak Prevention service.
    "outbreak-prevention-cache": "option",  # Enable/disable FortiGuard Virus Outbreak Prevention cache.
    "outbreak-prevention-cache-ttl": "integer",  # Time-to-live for FortiGuard Virus Outbreak Prevention cache entries (300 - 86400
    "outbreak-prevention-cache-mpermille": "integer",  # Maximum permille of memory FortiGuard Virus Outbreak Prevention cache can use (1
    "outbreak-prevention-license": "integer",  # Interval of time between license checks for FortiGuard Virus Outbreak Prevention
    "outbreak-prevention-expiration": "integer",  # Expiration date of FortiGuard Virus Outbreak Prevention contract.
    "outbreak-prevention-timeout": "integer",  # FortiGuard Virus Outbreak Prevention time out (1 - 30 sec, default = 7).
    "webfilter-force-off": "option",  # Enable/disable turning off the FortiGuard web filtering service.
    "webfilter-cache": "option",  # Enable/disable FortiGuard web filter caching.
    "webfilter-cache-ttl": "integer",  # Time-to-live for web filter cache entries in seconds (300 - 86400).
    "webfilter-license": "integer",  # Interval of time between license checks for the FortiGuard web filter contract.
    "webfilter-expiration": "integer",  # Expiration date of the FortiGuard web filter contract.
    "webfilter-timeout": "integer",  # Web filter query time out (1 - 30 sec, default = 15).
    "sdns-server-ip": "user",  # IP address of the FortiGuard DNS rating server.
    "sdns-server-port": "integer",  # Port to connect to on the FortiGuard DNS rating server.
    "anycast-sdns-server-ip": "ipv4-address",  # IP address of the FortiGuard anycast DNS rating server.
    "anycast-sdns-server-port": "integer",  # Port to connect to on the FortiGuard anycast DNS rating server.
    "sdns-options": "option",  # Customization options for the FortiGuard DNS service.
    "source-ip": "ipv4-address",  # Source IPv4 address used to communicate with FortiGuard.
    "source-ip6": "ipv6-address",  # Source IPv6 address used to communicate with FortiGuard.
    "proxy-server-ip": "string",  # Hostname or IPv4 address of the proxy server.
    "proxy-server-port": "integer",  # Port used to communicate with the proxy server.
    "proxy-username": "string",  # Proxy user name.
    "proxy-password": "password",  # Proxy user password.
    "ddns-server-ip": "ipv4-address",  # IP address of the FortiDDNS server.
    "ddns-server-ip6": "ipv6-address",  # IPv6 address of the FortiDDNS server.
    "ddns-server-port": "integer",  # Port used to communicate with FortiDDNS servers.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "fortiguard-anycast": "Enable/disable use of FortiGuard's Anycast network.",
    "fortiguard-anycast-source": "Configure which of Fortinet's servers to provide FortiGuard services in FortiGuard's anycast network. Default is Fortinet.",
    "protocol": "Protocol used to communicate with the FortiGuard servers.",
    "port": "Port used to communicate with the FortiGuard servers.",
    "load-balance-servers": "Number of servers to alternate between as first FortiGuard option.",
    "auto-join-forticloud": "Automatically connect to and login to FortiCloud.",
    "update-server-location": "Location from which to receive FortiGuard updates.",
    "sandbox-region": "FortiCloud Sandbox region.",
    "sandbox-inline-scan": "Enable/disable FortiCloud Sandbox inline-scan.",
    "update-ffdb": "Enable/disable Internet Service Database update.",
    "update-uwdb": "Enable/disable allowlist update.",
    "update-dldb": "Enable/disable DLP signature update.",
    "update-extdb": "Enable/disable external resource update.",
    "update-build-proxy": "Enable/disable proxy dictionary rebuild.",
    "persistent-connection": "Enable/disable use of persistent connection to receive update notification from FortiGuard.",
    "vdom": "FortiGuard Service virtual domain name.",
    "auto-firmware-upgrade": "Enable/disable automatic patch-level firmware upgrade from FortiGuard. The FortiGate unit searches for new patches only in the same major and minor version.",
    "auto-firmware-upgrade-day": "Allowed day(s) of the week to install an automatic patch-level firmware upgrade from FortiGuard (default is none). Disallow any day of the week to use auto-firmware-upgrade-delay instead, which waits for designated days before installing an automatic patch-level firmware upgrade.",
    "auto-firmware-upgrade-delay": "Delay of day(s) before installing an automatic patch-level firmware upgrade from FortiGuard (default = 3). Set it 0 to use auto-firmware-upgrade-day instead, which selects allowed day(s) of the week for installing an automatic patch-level firmware upgrade.",
    "auto-firmware-upgrade-start-hour": "Start time in the designated time window for automatic patch-level firmware upgrade from FortiGuard in 24 hour time (0 ~ 23, default = 2). The actual upgrade time is selected randomly within the time window.",
    "auto-firmware-upgrade-end-hour": "End time in the designated time window for automatic patch-level firmware upgrade from FortiGuard in 24 hour time (0 ~ 23, default = 4). When the end time is smaller than the start time, the end time is interpreted as the next day. The actual upgrade time is selected randomly within the time window.",
    "FDS-license-expiring-days": "Threshold for number of days before FortiGuard license expiration to generate license expiring event log (1 - 100 days, default = 15).",
    "subscribe-update-notification": "Enable/disable subscription to receive update notification from FortiGuard.",
    "antispam-force-off": "Enable/disable turning off the FortiGuard antispam service.",
    "antispam-cache": "Enable/disable FortiGuard antispam request caching. Uses a small amount of memory but improves performance.",
    "antispam-cache-ttl": "Time-to-live for antispam cache entries in seconds (300 - 86400). Lower times reduce the cache size. Higher times may improve performance since the cache will have more entries.",
    "antispam-cache-mpermille": "Maximum permille of FortiGate memory the antispam cache is allowed to use (1 - 150).",
    "antispam-license": "Interval of time between license checks for the FortiGuard antispam contract.",
    "antispam-expiration": "Expiration date of the FortiGuard antispam contract.",
    "antispam-timeout": "Antispam query time out (1 - 30 sec, default = 7).",
    "outbreak-prevention-force-off": "Turn off FortiGuard Virus Outbreak Prevention service.",
    "outbreak-prevention-cache": "Enable/disable FortiGuard Virus Outbreak Prevention cache.",
    "outbreak-prevention-cache-ttl": "Time-to-live for FortiGuard Virus Outbreak Prevention cache entries (300 - 86400 sec, default = 300).",
    "outbreak-prevention-cache-mpermille": "Maximum permille of memory FortiGuard Virus Outbreak Prevention cache can use (1 - 150 permille, default = 1).",
    "outbreak-prevention-license": "Interval of time between license checks for FortiGuard Virus Outbreak Prevention contract.",
    "outbreak-prevention-expiration": "Expiration date of FortiGuard Virus Outbreak Prevention contract.",
    "outbreak-prevention-timeout": "FortiGuard Virus Outbreak Prevention time out (1 - 30 sec, default = 7).",
    "webfilter-force-off": "Enable/disable turning off the FortiGuard web filtering service.",
    "webfilter-cache": "Enable/disable FortiGuard web filter caching.",
    "webfilter-cache-ttl": "Time-to-live for web filter cache entries in seconds (300 - 86400).",
    "webfilter-license": "Interval of time between license checks for the FortiGuard web filter contract.",
    "webfilter-expiration": "Expiration date of the FortiGuard web filter contract.",
    "webfilter-timeout": "Web filter query time out (1 - 30 sec, default = 15).",
    "sdns-server-ip": "IP address of the FortiGuard DNS rating server.",
    "sdns-server-port": "Port to connect to on the FortiGuard DNS rating server.",
    "anycast-sdns-server-ip": "IP address of the FortiGuard anycast DNS rating server.",
    "anycast-sdns-server-port": "Port to connect to on the FortiGuard anycast DNS rating server.",
    "sdns-options": "Customization options for the FortiGuard DNS service.",
    "source-ip": "Source IPv4 address used to communicate with FortiGuard.",
    "source-ip6": "Source IPv6 address used to communicate with FortiGuard.",
    "proxy-server-ip": "Hostname or IPv4 address of the proxy server.",
    "proxy-server-port": "Port used to communicate with the proxy server.",
    "proxy-username": "Proxy user name.",
    "proxy-password": "Proxy user password.",
    "ddns-server-ip": "IP address of the FortiDDNS server.",
    "ddns-server-ip6": "IPv6 address of the FortiDDNS server.",
    "ddns-server-port": "Port used to communicate with FortiDDNS servers.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "load-balance-servers": {"type": "integer", "min": 1, "max": 266},
    "sandbox-region": {"type": "string", "max_length": 63},
    "vdom": {"type": "string", "max_length": 31},
    "auto-firmware-upgrade-delay": {"type": "integer", "min": 0, "max": 14},
    "auto-firmware-upgrade-start-hour": {"type": "integer", "min": 0, "max": 23},
    "auto-firmware-upgrade-end-hour": {"type": "integer", "min": 0, "max": 23},
    "FDS-license-expiring-days": {"type": "integer", "min": 1, "max": 100},
    "antispam-cache-ttl": {"type": "integer", "min": 300, "max": 86400},
    "antispam-cache-mpermille": {"type": "integer", "min": 1, "max": 150},
    "antispam-license": {"type": "integer", "min": 0, "max": 4294967295},
    "antispam-expiration": {"type": "integer", "min": 0, "max": 4294967295},
    "antispam-timeout": {"type": "integer", "min": 1, "max": 30},
    "outbreak-prevention-cache-ttl": {"type": "integer", "min": 300, "max": 86400},
    "outbreak-prevention-cache-mpermille": {"type": "integer", "min": 1, "max": 150},
    "outbreak-prevention-license": {"type": "integer", "min": 0, "max": 4294967295},
    "outbreak-prevention-expiration": {"type": "integer", "min": 0, "max": 4294967295},
    "outbreak-prevention-timeout": {"type": "integer", "min": 1, "max": 30},
    "webfilter-cache-ttl": {"type": "integer", "min": 300, "max": 86400},
    "webfilter-license": {"type": "integer", "min": 0, "max": 4294967295},
    "webfilter-expiration": {"type": "integer", "min": 0, "max": 4294967295},
    "webfilter-timeout": {"type": "integer", "min": 1, "max": 30},
    "sdns-server-port": {"type": "integer", "min": 1, "max": 65535},
    "anycast-sdns-server-port": {"type": "integer", "min": 1, "max": 65535},
    "proxy-server-ip": {"type": "string", "max_length": 63},
    "proxy-server-port": {"type": "integer", "min": 0, "max": 65535},
    "proxy-username": {"type": "string", "max_length": 64},
    "ddns-server-port": {"type": "integer", "min": 1, "max": 65535},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_FORTIGUARD_ANYCAST = [
    "enable",
    "disable",
]
VALID_BODY_FORTIGUARD_ANYCAST_SOURCE = [
    "fortinet",
    "aws",
    "debug",
]
VALID_BODY_PROTOCOL = [
    "udp",
    "http",
    "https",
]
VALID_BODY_PORT = [
    "8888",
    "53",
    "80",
    "443",
]
VALID_BODY_AUTO_JOIN_FORTICLOUD = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_SERVER_LOCATION = [
    "automatic",
    "usa",
    "eu",
]
VALID_BODY_SANDBOX_INLINE_SCAN = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_FFDB = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_UWDB = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_DLDB = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_EXTDB = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_BUILD_PROXY = [
    "enable",
    "disable",
]
VALID_BODY_PERSISTENT_CONNECTION = [
    "enable",
    "disable",
]
VALID_BODY_AUTO_FIRMWARE_UPGRADE = [
    "enable",
    "disable",
]
VALID_BODY_AUTO_FIRMWARE_UPGRADE_DAY = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]
VALID_BODY_SUBSCRIBE_UPDATE_NOTIFICATION = [
    "enable",
    "disable",
]
VALID_BODY_ANTISPAM_FORCE_OFF = [
    "enable",
    "disable",
]
VALID_BODY_ANTISPAM_CACHE = [
    "enable",
    "disable",
]
VALID_BODY_OUTBREAK_PREVENTION_FORCE_OFF = [
    "enable",
    "disable",
]
VALID_BODY_OUTBREAK_PREVENTION_CACHE = [
    "enable",
    "disable",
]
VALID_BODY_WEBFILTER_FORCE_OFF = [
    "enable",
    "disable",
]
VALID_BODY_WEBFILTER_CACHE = [
    "enable",
    "disable",
]
VALID_BODY_SDNS_OPTIONS = [
    "include-question-section",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_fortiguard_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/fortiguard."""
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


def validate_system_fortiguard_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/fortiguard object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "fortiguard-anycast" in payload:
        is_valid, error = _validate_enum_field(
            "fortiguard-anycast",
            payload["fortiguard-anycast"],
            VALID_BODY_FORTIGUARD_ANYCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiguard-anycast-source" in payload:
        is_valid, error = _validate_enum_field(
            "fortiguard-anycast-source",
            payload["fortiguard-anycast-source"],
            VALID_BODY_FORTIGUARD_ANYCAST_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port" in payload:
        is_valid, error = _validate_enum_field(
            "port",
            payload["port"],
            VALID_BODY_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-join-forticloud" in payload:
        is_valid, error = _validate_enum_field(
            "auto-join-forticloud",
            payload["auto-join-forticloud"],
            VALID_BODY_AUTO_JOIN_FORTICLOUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-server-location" in payload:
        is_valid, error = _validate_enum_field(
            "update-server-location",
            payload["update-server-location"],
            VALID_BODY_UPDATE_SERVER_LOCATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sandbox-inline-scan" in payload:
        is_valid, error = _validate_enum_field(
            "sandbox-inline-scan",
            payload["sandbox-inline-scan"],
            VALID_BODY_SANDBOX_INLINE_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-ffdb" in payload:
        is_valid, error = _validate_enum_field(
            "update-ffdb",
            payload["update-ffdb"],
            VALID_BODY_UPDATE_FFDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-uwdb" in payload:
        is_valid, error = _validate_enum_field(
            "update-uwdb",
            payload["update-uwdb"],
            VALID_BODY_UPDATE_UWDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-dldb" in payload:
        is_valid, error = _validate_enum_field(
            "update-dldb",
            payload["update-dldb"],
            VALID_BODY_UPDATE_DLDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-extdb" in payload:
        is_valid, error = _validate_enum_field(
            "update-extdb",
            payload["update-extdb"],
            VALID_BODY_UPDATE_EXTDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-build-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "update-build-proxy",
            payload["update-build-proxy"],
            VALID_BODY_UPDATE_BUILD_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "persistent-connection" in payload:
        is_valid, error = _validate_enum_field(
            "persistent-connection",
            payload["persistent-connection"],
            VALID_BODY_PERSISTENT_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-firmware-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "auto-firmware-upgrade",
            payload["auto-firmware-upgrade"],
            VALID_BODY_AUTO_FIRMWARE_UPGRADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-firmware-upgrade-day" in payload:
        is_valid, error = _validate_enum_field(
            "auto-firmware-upgrade-day",
            payload["auto-firmware-upgrade-day"],
            VALID_BODY_AUTO_FIRMWARE_UPGRADE_DAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subscribe-update-notification" in payload:
        is_valid, error = _validate_enum_field(
            "subscribe-update-notification",
            payload["subscribe-update-notification"],
            VALID_BODY_SUBSCRIBE_UPDATE_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "antispam-force-off" in payload:
        is_valid, error = _validate_enum_field(
            "antispam-force-off",
            payload["antispam-force-off"],
            VALID_BODY_ANTISPAM_FORCE_OFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "antispam-cache" in payload:
        is_valid, error = _validate_enum_field(
            "antispam-cache",
            payload["antispam-cache"],
            VALID_BODY_ANTISPAM_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbreak-prevention-force-off" in payload:
        is_valid, error = _validate_enum_field(
            "outbreak-prevention-force-off",
            payload["outbreak-prevention-force-off"],
            VALID_BODY_OUTBREAK_PREVENTION_FORCE_OFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbreak-prevention-cache" in payload:
        is_valid, error = _validate_enum_field(
            "outbreak-prevention-cache",
            payload["outbreak-prevention-cache"],
            VALID_BODY_OUTBREAK_PREVENTION_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-force-off" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-force-off",
            payload["webfilter-force-off"],
            VALID_BODY_WEBFILTER_FORCE_OFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-cache" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-cache",
            payload["webfilter-cache"],
            VALID_BODY_WEBFILTER_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdns-options" in payload:
        is_valid, error = _validate_enum_field(
            "sdns-options",
            payload["sdns-options"],
            VALID_BODY_SDNS_OPTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_fortiguard_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/fortiguard."""
    # Validate enum values using central function
    if "fortiguard-anycast" in payload:
        is_valid, error = _validate_enum_field(
            "fortiguard-anycast",
            payload["fortiguard-anycast"],
            VALID_BODY_FORTIGUARD_ANYCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiguard-anycast-source" in payload:
        is_valid, error = _validate_enum_field(
            "fortiguard-anycast-source",
            payload["fortiguard-anycast-source"],
            VALID_BODY_FORTIGUARD_ANYCAST_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port" in payload:
        is_valid, error = _validate_enum_field(
            "port",
            payload["port"],
            VALID_BODY_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-join-forticloud" in payload:
        is_valid, error = _validate_enum_field(
            "auto-join-forticloud",
            payload["auto-join-forticloud"],
            VALID_BODY_AUTO_JOIN_FORTICLOUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-server-location" in payload:
        is_valid, error = _validate_enum_field(
            "update-server-location",
            payload["update-server-location"],
            VALID_BODY_UPDATE_SERVER_LOCATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sandbox-inline-scan" in payload:
        is_valid, error = _validate_enum_field(
            "sandbox-inline-scan",
            payload["sandbox-inline-scan"],
            VALID_BODY_SANDBOX_INLINE_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-ffdb" in payload:
        is_valid, error = _validate_enum_field(
            "update-ffdb",
            payload["update-ffdb"],
            VALID_BODY_UPDATE_FFDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-uwdb" in payload:
        is_valid, error = _validate_enum_field(
            "update-uwdb",
            payload["update-uwdb"],
            VALID_BODY_UPDATE_UWDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-dldb" in payload:
        is_valid, error = _validate_enum_field(
            "update-dldb",
            payload["update-dldb"],
            VALID_BODY_UPDATE_DLDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-extdb" in payload:
        is_valid, error = _validate_enum_field(
            "update-extdb",
            payload["update-extdb"],
            VALID_BODY_UPDATE_EXTDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-build-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "update-build-proxy",
            payload["update-build-proxy"],
            VALID_BODY_UPDATE_BUILD_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "persistent-connection" in payload:
        is_valid, error = _validate_enum_field(
            "persistent-connection",
            payload["persistent-connection"],
            VALID_BODY_PERSISTENT_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-firmware-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "auto-firmware-upgrade",
            payload["auto-firmware-upgrade"],
            VALID_BODY_AUTO_FIRMWARE_UPGRADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-firmware-upgrade-day" in payload:
        is_valid, error = _validate_enum_field(
            "auto-firmware-upgrade-day",
            payload["auto-firmware-upgrade-day"],
            VALID_BODY_AUTO_FIRMWARE_UPGRADE_DAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subscribe-update-notification" in payload:
        is_valid, error = _validate_enum_field(
            "subscribe-update-notification",
            payload["subscribe-update-notification"],
            VALID_BODY_SUBSCRIBE_UPDATE_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "antispam-force-off" in payload:
        is_valid, error = _validate_enum_field(
            "antispam-force-off",
            payload["antispam-force-off"],
            VALID_BODY_ANTISPAM_FORCE_OFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "antispam-cache" in payload:
        is_valid, error = _validate_enum_field(
            "antispam-cache",
            payload["antispam-cache"],
            VALID_BODY_ANTISPAM_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbreak-prevention-force-off" in payload:
        is_valid, error = _validate_enum_field(
            "outbreak-prevention-force-off",
            payload["outbreak-prevention-force-off"],
            VALID_BODY_OUTBREAK_PREVENTION_FORCE_OFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbreak-prevention-cache" in payload:
        is_valid, error = _validate_enum_field(
            "outbreak-prevention-cache",
            payload["outbreak-prevention-cache"],
            VALID_BODY_OUTBREAK_PREVENTION_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-force-off" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-force-off",
            payload["webfilter-force-off"],
            VALID_BODY_WEBFILTER_FORCE_OFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-cache" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-cache",
            payload["webfilter-cache"],
            VALID_BODY_WEBFILTER_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdns-options" in payload:
        is_valid, error = _validate_enum_field(
            "sdns-options",
            payload["sdns-options"],
            VALID_BODY_SDNS_OPTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
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
    "endpoint": "system/fortiguard",
    "category": "cmdb",
    "api_path": "system/fortiguard",
    "help": "Configure FortiGuard services.",
    "total_fields": 60,
    "required_fields_count": 1,
    "fields_with_defaults_count": 59,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
