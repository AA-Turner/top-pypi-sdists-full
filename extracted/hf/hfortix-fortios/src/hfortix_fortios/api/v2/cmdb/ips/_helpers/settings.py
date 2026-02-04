"""Validation helpers for ips/settings - Auto-generated"""

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
    "packet-log-history": 1,
    "packet-log-post-attack": 0,
    "packet-log-memory": 256,
    "ips-packet-quota": 0,
    "proxy-inline-ips": "enable",
    "ha-session-pickup": "connectivity",
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
    "packet-log-history": "integer",  # Number of packets to capture before and including the one in which the IPS signa
    "packet-log-post-attack": "integer",  # Number of packets to log after the IPS signature is detected (0 - 255).
    "packet-log-memory": "integer",  # Maximum memory can be used by packet log (64 - 8192 kB).
    "ips-packet-quota": "integer",  # Maximum amount of disk space in MB for logged packets when logging to disk. Rang
    "proxy-inline-ips": "option",  # Enable/disable proxy-mode policy inline IPS support.
    "ha-session-pickup": "option",  # IPS HA failover session pickup preference.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "packet-log-history": "Number of packets to capture before and including the one in which the IPS signature is detected (1 - 255).",
    "packet-log-post-attack": "Number of packets to log after the IPS signature is detected (0 - 255).",
    "packet-log-memory": "Maximum memory can be used by packet log (64 - 8192 kB).",
    "ips-packet-quota": "Maximum amount of disk space in MB for logged packets when logging to disk. Range depends on disk size.",
    "proxy-inline-ips": "Enable/disable proxy-mode policy inline IPS support.",
    "ha-session-pickup": "IPS HA failover session pickup preference.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "packet-log-history": {"type": "integer", "min": 1, "max": 255},
    "packet-log-post-attack": {"type": "integer", "min": 0, "max": 255},
    "packet-log-memory": {"type": "integer", "min": 64, "max": 8192},
    "ips-packet-quota": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_PROXY_INLINE_IPS = [
    "disable",
    "enable",
]
VALID_BODY_HA_SESSION_PICKUP = [
    "connectivity",
    "security",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_ips_settings_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for ips/settings."""
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


def validate_ips_settings_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new ips/settings object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "proxy-inline-ips" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-inline-ips",
            payload["proxy-inline-ips"],
            VALID_BODY_PROXY_INLINE_IPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-session-pickup" in payload:
        is_valid, error = _validate_enum_field(
            "ha-session-pickup",
            payload["ha-session-pickup"],
            VALID_BODY_HA_SESSION_PICKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_ips_settings_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update ips/settings."""
    # Validate enum values using central function
    if "proxy-inline-ips" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-inline-ips",
            payload["proxy-inline-ips"],
            VALID_BODY_PROXY_INLINE_IPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-session-pickup" in payload:
        is_valid, error = _validate_enum_field(
            "ha-session-pickup",
            payload["ha-session-pickup"],
            VALID_BODY_HA_SESSION_PICKUP,
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
    "endpoint": "ips/settings",
    "category": "cmdb",
    "api_path": "ips/settings",
    "help": "Configure IPS VDOM parameter.",
    "total_fields": 6,
    "required_fields_count": 0,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
