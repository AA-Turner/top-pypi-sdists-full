"""Validation helpers for firewall/shaper/per_ip_shaper - Auto-generated"""

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
    "max-bandwidth": 0,
    "bandwidth-unit": "kbps",
    "max-concurrent-session": 0,
    "max-concurrent-tcp-session": 0,
    "max-concurrent-udp-session": 0,
    "diffserv-forward": "disable",
    "diffserv-reverse": "disable",
    "diffservcode-forward": "",
    "diffservcode-rev": "",
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
    "name": "string",  # Traffic shaper name.
    "max-bandwidth": "integer",  # Upper bandwidth limit enforced by this shaper (0 - 80000000)
    "bandwidth-unit": "option",  # Unit of measurement for maximum bandwidth for this shaper (K
    "max-concurrent-session": "integer",  # Maximum number of concurrent sessions allowed by this shaper
    "max-concurrent-tcp-session": "integer",  # Maximum number of concurrent TCP sessions allowed by this sh
    "max-concurrent-udp-session": "integer",  # Maximum number of concurrent UDP sessions allowed by this sh
    "diffserv-forward": "option",  # Enable/disable changing the Forward (original) DiffServ sett
    "diffserv-reverse": "option",  # Enable/disable changing the Reverse (reply) DiffServ setting
    "diffservcode-forward": "user",  # Forward (original) DiffServ setting to be applied to traffic
    "diffservcode-rev": "user",  # Reverse (reply) DiffServ setting to be applied to traffic ac
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Traffic shaper name.",
    "max-bandwidth": "Upper bandwidth limit enforced by this shaper (0 - 80000000). 0 means no limit. Units depend on the bandwidth-unit setting.",
    "bandwidth-unit": "Unit of measurement for maximum bandwidth for this shaper (Kbps, Mbps or Gbps).",
    "max-concurrent-session": "Maximum number of concurrent sessions allowed by this shaper (0 - 2097000). 0 means no limit.",
    "max-concurrent-tcp-session": "Maximum number of concurrent TCP sessions allowed by this shaper (0 - 2097000). 0 means no limit.",
    "max-concurrent-udp-session": "Maximum number of concurrent UDP sessions allowed by this shaper (0 - 2097000). 0 means no limit.",
    "diffserv-forward": "Enable/disable changing the Forward (original) DiffServ setting applied to traffic accepted by this shaper.",
    "diffserv-reverse": "Enable/disable changing the Reverse (reply) DiffServ setting applied to traffic accepted by this shaper.",
    "diffservcode-forward": "Forward (original) DiffServ setting to be applied to traffic accepted by this shaper.",
    "diffservcode-rev": "Reverse (reply) DiffServ setting to be applied to traffic accepted by this shaper.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "max-bandwidth": {"type": "integer", "min": 0, "max": 80000000},
    "max-concurrent-session": {"type": "integer", "min": 0, "max": 2097000},
    "max-concurrent-tcp-session": {"type": "integer", "min": 0, "max": 2097000},
    "max-concurrent-udp-session": {"type": "integer", "min": 0, "max": 2097000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_BANDWIDTH_UNIT = [
    "kbps",
    "mbps",
    "gbps",
]
VALID_BODY_DIFFSERV_FORWARD = [
    "enable",
    "disable",
]
VALID_BODY_DIFFSERV_REVERSE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_shaper_per_ip_shaper_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/shaper/per_ip_shaper."""
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


def validate_firewall_shaper_per_ip_shaper_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/shaper/per_ip_shaper object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "bandwidth-unit" in payload:
        is_valid, error = _validate_enum_field(
            "bandwidth-unit",
            payload["bandwidth-unit"],
            VALID_BODY_BANDWIDTH_UNIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-forward" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-forward",
            payload["diffserv-forward"],
            VALID_BODY_DIFFSERV_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-reverse" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-reverse",
            payload["diffserv-reverse"],
            VALID_BODY_DIFFSERV_REVERSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_shaper_per_ip_shaper_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/shaper/per_ip_shaper."""
    # Validate enum values using central function
    if "bandwidth-unit" in payload:
        is_valid, error = _validate_enum_field(
            "bandwidth-unit",
            payload["bandwidth-unit"],
            VALID_BODY_BANDWIDTH_UNIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-forward" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-forward",
            payload["diffserv-forward"],
            VALID_BODY_DIFFSERV_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-reverse" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-reverse",
            payload["diffserv-reverse"],
            VALID_BODY_DIFFSERV_REVERSE,
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
    "endpoint": "firewall/shaper/per_ip_shaper",
    "category": "cmdb",
    "api_path": "firewall.shaper/per-ip-shaper",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure per-IP traffic shaper.",
    "total_fields": 10,
    "required_fields_count": 0,
    "fields_with_defaults_count": 10,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
