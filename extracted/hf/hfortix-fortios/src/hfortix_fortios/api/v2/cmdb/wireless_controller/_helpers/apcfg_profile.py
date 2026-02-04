"""Validation helpers for wireless_controller/apcfg_profile - Auto-generated"""

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
    "ap-family": "fap",
    "ac-type": "default",
    "ac-timer": 10,
    "ac-ip": "0.0.0.0",
    "ac-port": 5246,
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
    "name": "string",  # AP local configuration profile name.
    "ap-family": "option",  # FortiAP family type (default = fap).
    "comment": "var-string",  # Comment.
    "ac-type": "option",  # Validation controller type (default = default).
    "ac-timer": "integer",  # Maximum waiting time for the AP to join the validation controller after applying
    "ac-ip": "ipv4-address",  # IP address of the validation controller that AP must be able to join after apply
    "ac-port": "integer",  # Port of the validation controller that AP must be able to join after applying AP
    "command-list": "string",  # AP local configuration command list.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "AP local configuration profile name.",
    "ap-family": "FortiAP family type (default = fap).",
    "comment": "Comment.",
    "ac-type": "Validation controller type (default = default).",
    "ac-timer": "Maximum waiting time for the AP to join the validation controller after applying AP local configuration (3 - 30 min, default = 10).",
    "ac-ip": "IP address of the validation controller that AP must be able to join after applying AP local configuration.",
    "ac-port": "Port of the validation controller that AP must be able to join after applying AP local configuration (1024 - 49150, default = 5246).",
    "command-list": "AP local configuration command list.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "ac-timer": {"type": "integer", "min": 3, "max": 30},
    "ac-port": {"type": "integer", "min": 1024, "max": 49150},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "command-list": {
        "id": {
            "type": "integer",
            "help": "Command ID.",
            "default": 0,
            "min_value": 1,
            "max_value": 255,
        },
        "type": {
            "type": "option",
            "help": "The command type (default = non-password).",
            "default": "non-password",
            "options": ["non-password", "password"],
        },
        "name": {
            "type": "string",
            "help": "AP local configuration command name.",
            "default": "",
            "max_length": 63,
        },
        "value": {
            "type": "string",
            "help": "AP local configuration command value.",
            "default": "",
            "max_length": 127,
        },
        "passwd-value": {
            "type": "password",
            "help": "AP local configuration command password value.",
            "max_length": 128,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_AP_FAMILY = [
    "fap",
    "fap-u",
    "fap-c",
]
VALID_BODY_AC_TYPE = [
    "default",
    "specify",
    "apcfg",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_apcfg_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/apcfg_profile."""
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


def validate_wireless_controller_apcfg_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/apcfg_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ap-family" in payload:
        is_valid, error = _validate_enum_field(
            "ap-family",
            payload["ap-family"],
            VALID_BODY_AP_FAMILY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ac-type" in payload:
        is_valid, error = _validate_enum_field(
            "ac-type",
            payload["ac-type"],
            VALID_BODY_AC_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_apcfg_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/apcfg_profile."""
    # Validate enum values using central function
    if "ap-family" in payload:
        is_valid, error = _validate_enum_field(
            "ap-family",
            payload["ap-family"],
            VALID_BODY_AP_FAMILY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ac-type" in payload:
        is_valid, error = _validate_enum_field(
            "ac-type",
            payload["ac-type"],
            VALID_BODY_AC_TYPE,
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
    "endpoint": "wireless_controller/apcfg_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/apcfg-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure AP local configuration profiles.",
    "total_fields": 8,
    "required_fields_count": 0,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
