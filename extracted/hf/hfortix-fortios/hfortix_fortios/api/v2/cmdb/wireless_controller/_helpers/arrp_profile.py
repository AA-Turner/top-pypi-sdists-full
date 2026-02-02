"""Validation helpers for wireless_controller/arrp_profile - Auto-generated"""

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
    "selection-period": 3600,
    "monitor-period": 300,
    "weight-managed-ap": 50,
    "weight-rogue-ap": 10,
    "weight-noise-floor": 40,
    "weight-channel-load": 20,
    "weight-spectral-rssi": 40,
    "weight-weather-channel": 0,
    "weight-dfs-channel": 0,
    "threshold-ap": 250,
    "threshold-noise-floor": "-85",
    "threshold-channel-load": 60,
    "threshold-spectral-rssi": "-65",
    "threshold-tx-retries": 300,
    "threshold-rx-errors": 50,
    "include-weather-channel": "enable",
    "include-dfs-channel": "enable",
    "override-darrp-optimize": "disable",
    "darrp-optimize": 86400,
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
    "name": "string",  # WiFi ARRP profile name.
    "comment": "var-string",  # Comment.
    "selection-period": "integer",  # Period in seconds to measure average channel load, noise flo
    "monitor-period": "integer",  # Period in seconds to measure average transmit retries and re
    "weight-managed-ap": "integer",  # Weight in DARRP channel score calculation for managed APs (0
    "weight-rogue-ap": "integer",  # Weight in DARRP channel score calculation for rogue APs (0 -
    "weight-noise-floor": "integer",  # Weight in DARRP channel score calculation for noise floor (0
    "weight-channel-load": "integer",  # Weight in DARRP channel score calculation for channel load (
    "weight-spectral-rssi": "integer",  # Weight in DARRP channel score calculation for spectral RSSI 
    "weight-weather-channel": "integer",  # Weight in DARRP channel score calculation for weather channe
    "weight-dfs-channel": "integer",  # Weight in DARRP channel score calculation for DFS channel (0
    "threshold-ap": "integer",  # Threshold to reject channel in DARRP channel selection phase
    "threshold-noise-floor": "string",  # Threshold in dBm to reject channel in DARRP channel selectio
    "threshold-channel-load": "integer",  # Threshold in percentage to reject channel in DARRP channel s
    "threshold-spectral-rssi": "string",  # Threshold in dBm to reject channel in DARRP channel selectio
    "threshold-tx-retries": "integer",  # Threshold in percentage for transmit retries to trigger chan
    "threshold-rx-errors": "integer",  # Threshold in percentage for receive errors to trigger channe
    "include-weather-channel": "option",  # Enable/disable use of weather channel in DARRP channel selec
    "include-dfs-channel": "option",  # Enable/disable use of DFS channel in DARRP channel selection
    "override-darrp-optimize": "option",  # Enable to override setting darrp-optimize and darrp-optimize
    "darrp-optimize": "integer",  # Time for running Distributed Automatic Radio Resource Provis
    "darrp-optimize-schedules": "string",  # Firewall schedules for DARRP running time. DARRP will run pe
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "WiFi ARRP profile name.",
    "comment": "Comment.",
    "selection-period": "Period in seconds to measure average channel load, noise floor, spectral RSSI (default = 3600).",
    "monitor-period": "Period in seconds to measure average transmit retries and receive errors (default = 300).",
    "weight-managed-ap": "Weight in DARRP channel score calculation for managed APs (0 - 2000, default = 50).",
    "weight-rogue-ap": "Weight in DARRP channel score calculation for rogue APs (0 - 2000, default = 10).",
    "weight-noise-floor": "Weight in DARRP channel score calculation for noise floor (0 - 2000, default = 40).",
    "weight-channel-load": "Weight in DARRP channel score calculation for channel load (0 - 2000, default = 20).",
    "weight-spectral-rssi": "Weight in DARRP channel score calculation for spectral RSSI (0 - 2000, default = 40).",
    "weight-weather-channel": "Weight in DARRP channel score calculation for weather channel (0 - 2000, default = 0).",
    "weight-dfs-channel": "Weight in DARRP channel score calculation for DFS channel (0 - 2000, default = 0).",
    "threshold-ap": "Threshold to reject channel in DARRP channel selection phase 1 due to surrounding APs (0 - 500, default = 250).",
    "threshold-noise-floor": "Threshold in dBm to reject channel in DARRP channel selection phase 1 due to noise floor (-95 to -20, default = -85).",
    "threshold-channel-load": "Threshold in percentage to reject channel in DARRP channel selection phase 1 due to channel load (0 - 100, default = 60).",
    "threshold-spectral-rssi": "Threshold in dBm to reject channel in DARRP channel selection phase 1 due to spectral RSSI (-95 to -20, default = -65).",
    "threshold-tx-retries": "Threshold in percentage for transmit retries to trigger channel reselection in DARRP monitor stage (0 - 1000, default = 300).",
    "threshold-rx-errors": "Threshold in percentage for receive errors to trigger channel reselection in DARRP monitor stage (0 - 100, default = 50).",
    "include-weather-channel": "Enable/disable use of weather channel in DARRP channel selection phase 1 (default = enable).",
    "include-dfs-channel": "Enable/disable use of DFS channel in DARRP channel selection phase 1 (default = enable).",
    "override-darrp-optimize": "Enable to override setting darrp-optimize and darrp-optimize-schedules (default = disable).",
    "darrp-optimize": "Time for running Distributed Automatic Radio Resource Provisioning (DARRP) optimizations (0 - 86400 sec, default = 86400, 0 = disable).",
    "darrp-optimize-schedules": "Firewall schedules for DARRP running time. DARRP will run periodically based on darrp-optimize within the schedules. Separate multiple schedule names with a space.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "selection-period": {"type": "integer", "min": 0, "max": 65535},
    "monitor-period": {"type": "integer", "min": 0, "max": 65535},
    "weight-managed-ap": {"type": "integer", "min": 0, "max": 2000},
    "weight-rogue-ap": {"type": "integer", "min": 0, "max": 2000},
    "weight-noise-floor": {"type": "integer", "min": 0, "max": 2000},
    "weight-channel-load": {"type": "integer", "min": 0, "max": 2000},
    "weight-spectral-rssi": {"type": "integer", "min": 0, "max": 2000},
    "weight-weather-channel": {"type": "integer", "min": 0, "max": 2000},
    "weight-dfs-channel": {"type": "integer", "min": 0, "max": 2000},
    "threshold-ap": {"type": "integer", "min": 0, "max": 500},
    "threshold-noise-floor": {"type": "string", "max_length": 7},
    "threshold-channel-load": {"type": "integer", "min": 0, "max": 100},
    "threshold-spectral-rssi": {"type": "string", "max_length": 7},
    "threshold-tx-retries": {"type": "integer", "min": 0, "max": 1000},
    "threshold-rx-errors": {"type": "integer", "min": 0, "max": 100},
    "darrp-optimize": {"type": "integer", "min": 0, "max": 86400},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "darrp-optimize-schedules": {
        "name": {
            "type": "string",
            "help": "Schedule name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_INCLUDE_WEATHER_CHANNEL = [
    "enable",
    "disable",
]
VALID_BODY_INCLUDE_DFS_CHANNEL = [
    "enable",
    "disable",
]
VALID_BODY_OVERRIDE_DARRP_OPTIMIZE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_arrp_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/arrp_profile."""
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


def validate_wireless_controller_arrp_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/arrp_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "include-weather-channel" in payload:
        is_valid, error = _validate_enum_field(
            "include-weather-channel",
            payload["include-weather-channel"],
            VALID_BODY_INCLUDE_WEATHER_CHANNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-dfs-channel" in payload:
        is_valid, error = _validate_enum_field(
            "include-dfs-channel",
            payload["include-dfs-channel"],
            VALID_BODY_INCLUDE_DFS_CHANNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-darrp-optimize" in payload:
        is_valid, error = _validate_enum_field(
            "override-darrp-optimize",
            payload["override-darrp-optimize"],
            VALID_BODY_OVERRIDE_DARRP_OPTIMIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_arrp_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/arrp_profile."""
    # Validate enum values using central function
    if "include-weather-channel" in payload:
        is_valid, error = _validate_enum_field(
            "include-weather-channel",
            payload["include-weather-channel"],
            VALID_BODY_INCLUDE_WEATHER_CHANNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-dfs-channel" in payload:
        is_valid, error = _validate_enum_field(
            "include-dfs-channel",
            payload["include-dfs-channel"],
            VALID_BODY_INCLUDE_DFS_CHANNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-darrp-optimize" in payload:
        is_valid, error = _validate_enum_field(
            "override-darrp-optimize",
            payload["override-darrp-optimize"],
            VALID_BODY_OVERRIDE_DARRP_OPTIMIZE,
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
    "endpoint": "wireless_controller/arrp_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/arrp-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure WiFi Automatic Radio Resource Provisioning (ARRP) profiles.",
    "total_fields": 22,
    "required_fields_count": 0,
    "fields_with_defaults_count": 20,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
