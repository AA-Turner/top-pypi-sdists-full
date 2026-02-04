"""Validation helpers for extension_controller/extender_vap - Auto-generated"""

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
    "type",  # Wi-Fi VAP type local-vap / lan-extension-vap.
    "ssid",  # Wi-Fi SSID.
    "passphrase",  # Wi-Fi passphrase.
    "sae-password",  # Wi-Fi SAE Password.
    "auth-server-address",  # Wi-Fi Authentication Server Address (IPv4 format).
    "auth-server-secret",  # Wi-Fi Authentication Server Secret.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "type": "",
    "ssid": "",
    "max-clients": 0,
    "broadcast-ssid": "enable",
    "security": "WPA2-Personal",
    "dtim": 1,
    "rts-threshold": 2347,
    "pmf": "disabled",
    "target-wake-time": "enable",
    "bss-color-partial": "enable",
    "mu-mimo": "enable",
    "auth-server-address": "",
    "auth-server-port": 0,
    "auth-server-secret": "",
    "ip-address": "0.0.0.0 0.0.0.0",
    "start-ip": "0.0.0.0",
    "end-ip": "0.0.0.0",
    "allowaccess": "",
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
    "name": "string",  # Wi-Fi VAP name.
    "type": "option",  # Wi-Fi VAP type local-vap / lan-extension-vap.
    "ssid": "string",  # Wi-Fi SSID.
    "max-clients": "integer",  # Wi-Fi max clients (0 - 512), default = 0 (no limit) 
    "broadcast-ssid": "option",  # Wi-Fi broadcast SSID enable / disable.
    "security": "option",  # Wi-Fi security.
    "dtim": "integer",  # Wi-Fi DTIM (1 - 255) default = 1.
    "rts-threshold": "integer",  # Wi-Fi RTS Threshold (256 - 2347), default = 2347 (RTS/CTS disabled).
    "pmf": "option",  # Wi-Fi pmf enable/disable, default = disable.
    "target-wake-time": "option",  # Wi-Fi 802.11AX target wake time enable / disable, default = enable.
    "bss-color-partial": "option",  # Wi-Fi 802.11AX bss color partial enable / disable, default = enable.
    "mu-mimo": "option",  # Wi-Fi multi-user MIMO enable / disable, default = enable.
    "passphrase": "password",  # Wi-Fi passphrase.
    "sae-password": "password",  # Wi-Fi SAE Password.
    "auth-server-address": "string",  # Wi-Fi Authentication Server Address (IPv4 format).
    "auth-server-port": "integer",  # Wi-Fi Authentication Server Port.
    "auth-server-secret": "string",  # Wi-Fi Authentication Server Secret.
    "ip-address": "ipv4-classnet-host",  # Extender ip address.
    "start-ip": "ipv4-address",  # Start ip address.
    "end-ip": "ipv4-address",  # End ip address.
    "allowaccess": "option",  # Control management access to the managed extender. Separate entries with a space
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Wi-Fi VAP name.",
    "type": "Wi-Fi VAP type local-vap / lan-extension-vap.",
    "ssid": "Wi-Fi SSID.",
    "max-clients": "Wi-Fi max clients (0 - 512), default = 0 (no limit) ",
    "broadcast-ssid": "Wi-Fi broadcast SSID enable / disable.",
    "security": "Wi-Fi security.",
    "dtim": "Wi-Fi DTIM (1 - 255) default = 1.",
    "rts-threshold": "Wi-Fi RTS Threshold (256 - 2347), default = 2347 (RTS/CTS disabled).",
    "pmf": "Wi-Fi pmf enable/disable, default = disable.",
    "target-wake-time": "Wi-Fi 802.11AX target wake time enable / disable, default = enable.",
    "bss-color-partial": "Wi-Fi 802.11AX bss color partial enable / disable, default = enable.",
    "mu-mimo": "Wi-Fi multi-user MIMO enable / disable, default = enable.",
    "passphrase": "Wi-Fi passphrase.",
    "sae-password": "Wi-Fi SAE Password.",
    "auth-server-address": "Wi-Fi Authentication Server Address (IPv4 format).",
    "auth-server-port": "Wi-Fi Authentication Server Port.",
    "auth-server-secret": "Wi-Fi Authentication Server Secret.",
    "ip-address": "Extender ip address.",
    "start-ip": "Start ip address.",
    "end-ip": "End ip address.",
    "allowaccess": "Control management access to the managed extender. Separate entries with a space.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 15},
    "ssid": {"type": "string", "max_length": 32},
    "max-clients": {"type": "integer", "min": 0, "max": 512},
    "dtim": {"type": "integer", "min": 1, "max": 255},
    "rts-threshold": {"type": "integer", "min": 256, "max": 2347},
    "auth-server-address": {"type": "string", "max_length": 63},
    "auth-server-port": {"type": "integer", "min": 1, "max": 65535},
    "auth-server-secret": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "local-vap",
    "lan-ext-vap",
]
VALID_BODY_BROADCAST_SSID = [
    "disable",
    "enable",
]
VALID_BODY_SECURITY = [
    "OPEN",
    "WPA2-Personal",
    "WPA-WPA2-Personal",
    "WPA3-SAE",
    "WPA3-SAE-Transition",
    "WPA2-Enterprise",
    "WPA3-Enterprise-only",
    "WPA3-Enterprise-transition",
    "WPA3-Enterprise-192-bit",
]
VALID_BODY_PMF = [
    "disabled",
    "optional",
    "required",
]
VALID_BODY_TARGET_WAKE_TIME = [
    "disable",
    "enable",
]
VALID_BODY_BSS_COLOR_PARTIAL = [
    "disable",
    "enable",
]
VALID_BODY_MU_MIMO = [
    "disable",
    "enable",
]
VALID_BODY_ALLOWACCESS = [
    "ping",
    "telnet",
    "http",
    "https",
    "ssh",
    "snmp",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_extension_controller_extender_vap_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for extension_controller/extender_vap."""
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


def validate_extension_controller_extender_vap_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new extension_controller/extender_vap object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-ssid",
            payload["broadcast-ssid"],
            VALID_BODY_BROADCAST_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security" in payload:
        is_valid, error = _validate_enum_field(
            "security",
            payload["security"],
            VALID_BODY_SECURITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pmf" in payload:
        is_valid, error = _validate_enum_field(
            "pmf",
            payload["pmf"],
            VALID_BODY_PMF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "target-wake-time" in payload:
        is_valid, error = _validate_enum_field(
            "target-wake-time",
            payload["target-wake-time"],
            VALID_BODY_TARGET_WAKE_TIME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bss-color-partial" in payload:
        is_valid, error = _validate_enum_field(
            "bss-color-partial",
            payload["bss-color-partial"],
            VALID_BODY_BSS_COLOR_PARTIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mu-mimo" in payload:
        is_valid, error = _validate_enum_field(
            "mu-mimo",
            payload["mu-mimo"],
            VALID_BODY_MU_MIMO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_extension_controller_extender_vap_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update extension_controller/extender_vap."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-ssid",
            payload["broadcast-ssid"],
            VALID_BODY_BROADCAST_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security" in payload:
        is_valid, error = _validate_enum_field(
            "security",
            payload["security"],
            VALID_BODY_SECURITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pmf" in payload:
        is_valid, error = _validate_enum_field(
            "pmf",
            payload["pmf"],
            VALID_BODY_PMF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "target-wake-time" in payload:
        is_valid, error = _validate_enum_field(
            "target-wake-time",
            payload["target-wake-time"],
            VALID_BODY_TARGET_WAKE_TIME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bss-color-partial" in payload:
        is_valid, error = _validate_enum_field(
            "bss-color-partial",
            payload["bss-color-partial"],
            VALID_BODY_BSS_COLOR_PARTIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mu-mimo" in payload:
        is_valid, error = _validate_enum_field(
            "mu-mimo",
            payload["mu-mimo"],
            VALID_BODY_MU_MIMO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
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
    "endpoint": "extension_controller/extender_vap",
    "category": "cmdb",
    "api_path": "extension-controller/extender-vap",
    "mkey": "name",
    "mkey_type": "string",
    "help": "FortiExtender wifi vap configuration.",
    "total_fields": 21,
    "required_fields_count": 6,
    "fields_with_defaults_count": 19,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
