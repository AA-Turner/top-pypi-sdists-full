"""Validation helpers for wireless_controller/ble_profile - Auto-generated"""

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
    "comment": "",
    "advertising": "",
    "ibeacon-uuid": "005ea414-cbd1-11e5-9956-625662870761",
    "major-id": 1000,
    "minor-id": 2000,
    "eddystone-namespace": "0102030405",
    "eddystone-instance": "abcdef",
    "eddystone-url": "http://www.fortinet.com",
    "txpower": "0",
    "beacon-interval": 100,
    "ble-scanning": "disable",
    "scan-type": "active",
    "scan-threshold": "-90",
    "scan-period": 4000,
    "scan-time": 1000,
    "scan-interval": 50,
    "scan-window": 50,
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
    "name": "string",  # Bluetooth Low Energy profile name.
    "comment": "string",  # Comment.
    "advertising": "option",  # Advertising type.
    "ibeacon-uuid": "string",  # Universally Unique Identifier (UUID; automatically assigned 
    "major-id": "integer",  # Major ID.
    "minor-id": "integer",  # Minor ID.
    "eddystone-namespace": "string",  # Eddystone namespace ID.
    "eddystone-instance": "string",  # Eddystone instance ID.
    "eddystone-url": "string",  # Eddystone URL.
    "txpower": "option",  # Transmit power level (default = 0).
    "beacon-interval": "integer",  # Beacon interval (default = 100 msec).
    "ble-scanning": "option",  # Enable/disable Bluetooth Low Energy (BLE) scanning.
    "scan-type": "option",  # Scan Type (default = active).
    "scan-threshold": "string",  # Minimum signal level/threshold in dBm required for the AP to
    "scan-period": "integer",  # Scan Period (default = 4000 msec).
    "scan-time": "integer",  # Scan Time (default = 1000 msec).
    "scan-interval": "integer",  # Scan Interval (default = 50 msec).
    "scan-window": "integer",  # Scan Windows (default = 50 msec).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Bluetooth Low Energy profile name.",
    "comment": "Comment.",
    "advertising": "Advertising type.",
    "ibeacon-uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "major-id": "Major ID.",
    "minor-id": "Minor ID.",
    "eddystone-namespace": "Eddystone namespace ID.",
    "eddystone-instance": "Eddystone instance ID.",
    "eddystone-url": "Eddystone URL.",
    "txpower": "Transmit power level (default = 0).",
    "beacon-interval": "Beacon interval (default = 100 msec).",
    "ble-scanning": "Enable/disable Bluetooth Low Energy (BLE) scanning.",
    "scan-type": "Scan Type (default = active).",
    "scan-threshold": "Minimum signal level/threshold in dBm required for the AP to report detected BLE device (-95 to -20, default = -90).",
    "scan-period": "Scan Period (default = 4000 msec).",
    "scan-time": "Scan Time (default = 1000 msec).",
    "scan-interval": "Scan Interval (default = 50 msec).",
    "scan-window": "Scan Windows (default = 50 msec).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "comment": {"type": "string", "max_length": 63},
    "ibeacon-uuid": {"type": "string", "max_length": 63},
    "major-id": {"type": "integer", "min": 0, "max": 65535},
    "minor-id": {"type": "integer", "min": 0, "max": 65535},
    "eddystone-namespace": {"type": "string", "max_length": 20},
    "eddystone-instance": {"type": "string", "max_length": 12},
    "eddystone-url": {"type": "string", "max_length": 127},
    "beacon-interval": {"type": "integer", "min": 40, "max": 3500},
    "scan-threshold": {"type": "string", "max_length": 7},
    "scan-period": {"type": "integer", "min": 1000, "max": 10000},
    "scan-time": {"type": "integer", "min": 1000, "max": 10000},
    "scan-interval": {"type": "integer", "min": 10, "max": 1000},
    "scan-window": {"type": "integer", "min": 10, "max": 1000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_ADVERTISING = [
    "ibeacon",
    "eddystone-uid",
    "eddystone-url",
]
VALID_BODY_TXPOWER = [
    "0",
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
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
]
VALID_BODY_BLE_SCANNING = [
    "enable",
    "disable",
]
VALID_BODY_SCAN_TYPE = [
    "active",
    "passive",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_ble_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/ble_profile."""
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


def validate_wireless_controller_ble_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/ble_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "advertising" in payload:
        is_valid, error = _validate_enum_field(
            "advertising",
            payload["advertising"],
            VALID_BODY_ADVERTISING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "txpower" in payload:
        is_valid, error = _validate_enum_field(
            "txpower",
            payload["txpower"],
            VALID_BODY_TXPOWER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ble-scanning" in payload:
        is_valid, error = _validate_enum_field(
            "ble-scanning",
            payload["ble-scanning"],
            VALID_BODY_BLE_SCANNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scan-type" in payload:
        is_valid, error = _validate_enum_field(
            "scan-type",
            payload["scan-type"],
            VALID_BODY_SCAN_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_ble_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/ble_profile."""
    # Validate enum values using central function
    if "advertising" in payload:
        is_valid, error = _validate_enum_field(
            "advertising",
            payload["advertising"],
            VALID_BODY_ADVERTISING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "txpower" in payload:
        is_valid, error = _validate_enum_field(
            "txpower",
            payload["txpower"],
            VALID_BODY_TXPOWER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ble-scanning" in payload:
        is_valid, error = _validate_enum_field(
            "ble-scanning",
            payload["ble-scanning"],
            VALID_BODY_BLE_SCANNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scan-type" in payload:
        is_valid, error = _validate_enum_field(
            "scan-type",
            payload["scan-type"],
            VALID_BODY_SCAN_TYPE,
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
    "endpoint": "wireless_controller/ble_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/ble-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Bluetooth Low Energy profile.",
    "total_fields": 18,
    "required_fields_count": 0,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
