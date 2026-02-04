"""Validation helpers for wireless_controller/global_ - Auto-generated"""

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
    "name": "",
    "location": "",
    "acd-process-count": 0,
    "wpad-process-count": 0,
    "image-download": "enable",
    "rolling-wtp-upgrade": "disable",
    "rolling-wtp-upgrade-threshold": "-80",
    "max-retransmit": 3,
    "control-message-offload": "ebp-frame aeroscout-tag ap-list sta-list sta-cap-list stats aeroscout-mu sta-health spectral-analysis",
    "data-ethernet-II": "enable",
    "link-aggregation": "disable",
    "mesh-eth-type": 8755,
    "fiapp-eth-type": 5252,
    "discovery-mc-addr": "224.0.1.140",
    "discovery-mc-addr6": "ff02::18c",
    "max-clients": 0,
    "rogue-scan-mac-adjacency": 7,
    "ipsec-base-ip": "169.254.0.1",
    "wtp-share": "disable",
    "tunnel-mode": "compatible",
    "nac-interval": 120,
    "ap-log-server": "disable",
    "ap-log-server-ip": "0.0.0.0",
    "ap-log-server-port": 0,
    "max-sta-offline": 0,
    "max-sta-offline-ip2mac": 0,
    "max-sta-cap": 0,
    "max-sta-cap-wtp": 8,
    "max-rogue-ap": 0,
    "max-rogue-ap-wtp": 16,
    "max-rogue-sta": 0,
    "max-wids-entry": 0,
    "max-ble-device": 0,
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
    "name": "string",  # Name of the wireless controller.
    "location": "string",  # Description of the location of the wireless controller.
    "acd-process-count": "integer",  # Configure the number cw_acd daemons for multi-core CPU support (default = 0).
    "wpad-process-count": "integer",  # Wpad daemon process count for multi-core CPU support.
    "image-download": "option",  # Enable/disable WTP image download at join time.
    "rolling-wtp-upgrade": "option",  # Enable/disable rolling WTP upgrade (default = disable).
    "rolling-wtp-upgrade-threshold": "string",  # Minimum signal level/threshold in dBm required for the managed WTP to be include
    "max-retransmit": "integer",  # Maximum number of tunnel packet retransmissions (0 - 64, default = 3).
    "control-message-offload": "option",  # Configure CAPWAP control message data channel offload.
    "data-ethernet-II": "option",  # Configure the wireless controller to use Ethernet II or 802.3 frames with 802.3 
    "link-aggregation": "option",  # Enable/disable calculating the CAPWAP transmit hash to load balance sessions to 
    "mesh-eth-type": "integer",  # Mesh Ethernet identifier included in backhaul packets (0 - 65535, default = 8755
    "fiapp-eth-type": "integer",  # Ethernet type for Fortinet Inter-Access Point Protocol (IAPP), or IEEE 802.11f, 
    "discovery-mc-addr": "ipv4-address-multicast",  # Multicast IP address for AP discovery (default = 244.0.1.140).
    "discovery-mc-addr6": "ipv6-address",  # Multicast IPv6 address for AP discovery (default = FF02::18C).
    "max-clients": "integer",  # Maximum number of clients that can connect simultaneously (default = 0, meaning 
    "rogue-scan-mac-adjacency": "integer",  # Maximum numerical difference between an AP's Ethernet and wireless MAC values to
    "ipsec-base-ip": "ipv4-address",  # Base IP address for IPsec VPN tunnels between the access points and the wireless
    "wtp-share": "option",  # Enable/disable sharing of WTPs between VDOMs.
    "tunnel-mode": "option",  # Compatible/strict tunnel mode.
    "nac-interval": "integer",  # Interval in seconds between two WiFi network access control (NAC) checks (10 - 6
    "ap-log-server": "option",  # Enable/disable configuring FortiGate to redirect wireless event log messages or 
    "ap-log-server-ip": "ipv4-address",  # IP address that FortiGate or FortiAPs send log messages to.
    "ap-log-server-port": "integer",  # Port that FortiGate or FortiAPs send log messages to.
    "max-sta-offline": "integer",  # Maximum number of station offline stored on the controller (default = 0).
    "max-sta-offline-ip2mac": "integer",  # Maximum number of station offline ip2mac stored on the controller (default = 0).
    "max-sta-cap": "integer",  # Maximum number of station cap stored on the controller (default = 0).
    "max-sta-cap-wtp": "integer",  # Maximum number of station cap's wtp info stored on the controller (1 - 16, defau
    "max-rogue-ap": "integer",  # Maximum number of rogue APs stored on the controller (default = 0).
    "max-rogue-ap-wtp": "integer",  # Maximum number of rogue AP's wtp info stored on the controller (1 - 16, default 
    "max-rogue-sta": "integer",  # Maximum number of rogue stations stored on the controller (default = 0).
    "max-wids-entry": "integer",  # Maximum number of wids entries stored on the controller (default = 0).
    "max-ble-device": "integer",  # Maximum number of BLE devices stored on the controller (default = 0).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name of the wireless controller.",
    "location": "Description of the location of the wireless controller.",
    "acd-process-count": "Configure the number cw_acd daemons for multi-core CPU support (default = 0).",
    "wpad-process-count": "Wpad daemon process count for multi-core CPU support.",
    "image-download": "Enable/disable WTP image download at join time.",
    "rolling-wtp-upgrade": "Enable/disable rolling WTP upgrade (default = disable).",
    "rolling-wtp-upgrade-threshold": "Minimum signal level/threshold in dBm required for the managed WTP to be included in rolling WTP upgrade (-95 to -20, default = -80).",
    "max-retransmit": "Maximum number of tunnel packet retransmissions (0 - 64, default = 3).",
    "control-message-offload": "Configure CAPWAP control message data channel offload.",
    "data-ethernet-II": "Configure the wireless controller to use Ethernet II or 802.3 frames with 802.3 data tunnel mode (default = enable).",
    "link-aggregation": "Enable/disable calculating the CAPWAP transmit hash to load balance sessions to link aggregation nodes (default = disable).",
    "mesh-eth-type": "Mesh Ethernet identifier included in backhaul packets (0 - 65535, default = 8755).",
    "fiapp-eth-type": "Ethernet type for Fortinet Inter-Access Point Protocol (IAPP), or IEEE 802.11f, packets (0 - 65535, default = 5252).",
    "discovery-mc-addr": "Multicast IP address for AP discovery (default = 244.0.1.140).",
    "discovery-mc-addr6": "Multicast IPv6 address for AP discovery (default = FF02::18C).",
    "max-clients": "Maximum number of clients that can connect simultaneously (default = 0, meaning no limitation).",
    "rogue-scan-mac-adjacency": "Maximum numerical difference between an AP's Ethernet and wireless MAC values to match for rogue detection (0 - 31, default = 7).",
    "ipsec-base-ip": "Base IP address for IPsec VPN tunnels between the access points and the wireless controller (default = 169.254.0.1).",
    "wtp-share": "Enable/disable sharing of WTPs between VDOMs.",
    "tunnel-mode": "Compatible/strict tunnel mode.",
    "nac-interval": "Interval in seconds between two WiFi network access control (NAC) checks (10 - 600, default = 120).",
    "ap-log-server": "Enable/disable configuring FortiGate to redirect wireless event log messages or FortiAPs to send UTM log messages to a syslog server (default = disable).",
    "ap-log-server-ip": "IP address that FortiGate or FortiAPs send log messages to.",
    "ap-log-server-port": "Port that FortiGate or FortiAPs send log messages to.",
    "max-sta-offline": "Maximum number of station offline stored on the controller (default = 0).",
    "max-sta-offline-ip2mac": "Maximum number of station offline ip2mac stored on the controller (default = 0).",
    "max-sta-cap": "Maximum number of station cap stored on the controller (default = 0).",
    "max-sta-cap-wtp": "Maximum number of station cap's wtp info stored on the controller (1 - 16, default = 8).",
    "max-rogue-ap": "Maximum number of rogue APs stored on the controller (default = 0).",
    "max-rogue-ap-wtp": "Maximum number of rogue AP's wtp info stored on the controller (1 - 16, default = 16).",
    "max-rogue-sta": "Maximum number of rogue stations stored on the controller (default = 0).",
    "max-wids-entry": "Maximum number of wids entries stored on the controller (default = 0).",
    "max-ble-device": "Maximum number of BLE devices stored on the controller (default = 0).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "location": {"type": "string", "max_length": 35},
    "acd-process-count": {"type": "integer", "min": 0, "max": 255},
    "wpad-process-count": {"type": "integer", "min": 0, "max": 255},
    "rolling-wtp-upgrade-threshold": {"type": "string", "max_length": 7},
    "max-retransmit": {"type": "integer", "min": 0, "max": 64},
    "mesh-eth-type": {"type": "integer", "min": 0, "max": 65535},
    "fiapp-eth-type": {"type": "integer", "min": 0, "max": 65535},
    "max-clients": {"type": "integer", "min": 0, "max": 4294967295},
    "rogue-scan-mac-adjacency": {"type": "integer", "min": 0, "max": 31},
    "nac-interval": {"type": "integer", "min": 10, "max": 600},
    "ap-log-server-port": {"type": "integer", "min": 0, "max": 65535},
    "max-sta-offline": {"type": "integer", "min": 0, "max": 4294967295},
    "max-sta-offline-ip2mac": {"type": "integer", "min": 0, "max": 4294967295},
    "max-sta-cap": {"type": "integer", "min": 0, "max": 4294967295},
    "max-sta-cap-wtp": {"type": "integer", "min": 1, "max": 8},
    "max-rogue-ap": {"type": "integer", "min": 0, "max": 4294967295},
    "max-rogue-ap-wtp": {"type": "integer", "min": 1, "max": 16},
    "max-rogue-sta": {"type": "integer", "min": 0, "max": 4294967295},
    "max-wids-entry": {"type": "integer", "min": 0, "max": 4294967295},
    "max-ble-device": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_IMAGE_DOWNLOAD = [
    "enable",
    "disable",
]
VALID_BODY_ROLLING_WTP_UPGRADE = [
    "enable",
    "disable",
]
VALID_BODY_CONTROL_MESSAGE_OFFLOAD = [
    "ebp-frame",
    "aeroscout-tag",
    "ap-list",
    "sta-list",
    "sta-cap-list",
    "stats",
    "aeroscout-mu",
    "sta-health",
    "spectral-analysis",
]
VALID_BODY_DATA_ETHERNET_II = [
    "enable",
    "disable",
]
VALID_BODY_LINK_AGGREGATION = [
    "enable",
    "disable",
]
VALID_BODY_WTP_SHARE = [
    "enable",
    "disable",
]
VALID_BODY_TUNNEL_MODE = [
    "compatible",
    "strict",
]
VALID_BODY_AP_LOG_SERVER = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_global_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/global_."""
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


def validate_wireless_controller_global_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/global_ object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "image-download" in payload:
        is_valid, error = _validate_enum_field(
            "image-download",
            payload["image-download"],
            VALID_BODY_IMAGE_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rolling-wtp-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "rolling-wtp-upgrade",
            payload["rolling-wtp-upgrade"],
            VALID_BODY_ROLLING_WTP_UPGRADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "control-message-offload" in payload:
        is_valid, error = _validate_enum_field(
            "control-message-offload",
            payload["control-message-offload"],
            VALID_BODY_CONTROL_MESSAGE_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "data-ethernet-II" in payload:
        is_valid, error = _validate_enum_field(
            "data-ethernet-II",
            payload["data-ethernet-II"],
            VALID_BODY_DATA_ETHERNET_II,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "link-aggregation" in payload:
        is_valid, error = _validate_enum_field(
            "link-aggregation",
            payload["link-aggregation"],
            VALID_BODY_LINK_AGGREGATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wtp-share" in payload:
        is_valid, error = _validate_enum_field(
            "wtp-share",
            payload["wtp-share"],
            VALID_BODY_WTP_SHARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tunnel-mode" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-mode",
            payload["tunnel-mode"],
            VALID_BODY_TUNNEL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-log-server" in payload:
        is_valid, error = _validate_enum_field(
            "ap-log-server",
            payload["ap-log-server"],
            VALID_BODY_AP_LOG_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_global_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/global_."""
    # Validate enum values using central function
    if "image-download" in payload:
        is_valid, error = _validate_enum_field(
            "image-download",
            payload["image-download"],
            VALID_BODY_IMAGE_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rolling-wtp-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "rolling-wtp-upgrade",
            payload["rolling-wtp-upgrade"],
            VALID_BODY_ROLLING_WTP_UPGRADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "control-message-offload" in payload:
        is_valid, error = _validate_enum_field(
            "control-message-offload",
            payload["control-message-offload"],
            VALID_BODY_CONTROL_MESSAGE_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "data-ethernet-II" in payload:
        is_valid, error = _validate_enum_field(
            "data-ethernet-II",
            payload["data-ethernet-II"],
            VALID_BODY_DATA_ETHERNET_II,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "link-aggregation" in payload:
        is_valid, error = _validate_enum_field(
            "link-aggregation",
            payload["link-aggregation"],
            VALID_BODY_LINK_AGGREGATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wtp-share" in payload:
        is_valid, error = _validate_enum_field(
            "wtp-share",
            payload["wtp-share"],
            VALID_BODY_WTP_SHARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tunnel-mode" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-mode",
            payload["tunnel-mode"],
            VALID_BODY_TUNNEL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-log-server" in payload:
        is_valid, error = _validate_enum_field(
            "ap-log-server",
            payload["ap-log-server"],
            VALID_BODY_AP_LOG_SERVER,
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
    "endpoint": "wireless_controller/global_",
    "category": "cmdb",
    "api_path": "wireless-controller/global",
    "help": "Configure wireless controller global settings.",
    "total_fields": 33,
    "required_fields_count": 0,
    "fields_with_defaults_count": 33,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
