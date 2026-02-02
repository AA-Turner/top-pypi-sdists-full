"""Validation helpers for wireless_controller/mpsk_profile - Auto-generated"""

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
    "mpsk-concurrent-clients": 0,
    "mpsk-external-server-auth": "disable",
    "mpsk-external-server": "",
    "mpsk-type": "wpa2-personal",
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
    "name": "string",  # MPSK profile name.
    "mpsk-concurrent-clients": "integer",  # Maximum number of concurrent clients that connect using the 
    "mpsk-external-server-auth": "option",  # Enable/Disable MPSK external server authentication (default 
    "mpsk-external-server": "string",  # RADIUS server to be used to authenticate MPSK users.
    "mpsk-type": "option",  # Select the security type of keys for this profile.
    "mpsk-group": "string",  # List of multiple PSK groups.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "MPSK profile name.",
    "mpsk-concurrent-clients": "Maximum number of concurrent clients that connect using the same passphrase in multiple PSK authentication (0 - 65535, default = 0, meaning no limitation).",
    "mpsk-external-server-auth": "Enable/Disable MPSK external server authentication (default = disable).",
    "mpsk-external-server": "RADIUS server to be used to authenticate MPSK users.",
    "mpsk-type": "Select the security type of keys for this profile.",
    "mpsk-group": "List of multiple PSK groups.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "mpsk-concurrent-clients": {"type": "integer", "min": 0, "max": 65535},
    "mpsk-external-server": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "mpsk-group": {
        "name": {
            "type": "string",
            "help": "MPSK group name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "vlan-type": {
            "type": "option",
            "help": "MPSK group VLAN options.",
            "default": "no-vlan",
            "options": ["no-vlan", "fixed-vlan"],
        },
        "vlan-id": {
            "type": "integer",
            "help": "Optional VLAN ID.",
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "mpsk-key": {
            "type": "string",
            "help": "List of multiple PSK entries.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_MPSK_EXTERNAL_SERVER_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_MPSK_TYPE = [
    "wpa2-personal",
    "wpa3-sae",
    "wpa3-sae-transition",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_mpsk_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/mpsk_profile."""
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


def validate_wireless_controller_mpsk_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/mpsk_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "mpsk-external-server-auth" in payload:
        is_valid, error = _validate_enum_field(
            "mpsk-external-server-auth",
            payload["mpsk-external-server-auth"],
            VALID_BODY_MPSK_EXTERNAL_SERVER_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mpsk-type" in payload:
        is_valid, error = _validate_enum_field(
            "mpsk-type",
            payload["mpsk-type"],
            VALID_BODY_MPSK_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_mpsk_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/mpsk_profile."""
    # Validate enum values using central function
    if "mpsk-external-server-auth" in payload:
        is_valid, error = _validate_enum_field(
            "mpsk-external-server-auth",
            payload["mpsk-external-server-auth"],
            VALID_BODY_MPSK_EXTERNAL_SERVER_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mpsk-type" in payload:
        is_valid, error = _validate_enum_field(
            "mpsk-type",
            payload["mpsk-type"],
            VALID_BODY_MPSK_TYPE,
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
    "endpoint": "wireless_controller/mpsk_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/mpsk-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure MPSK profile.",
    "total_fields": 6,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
