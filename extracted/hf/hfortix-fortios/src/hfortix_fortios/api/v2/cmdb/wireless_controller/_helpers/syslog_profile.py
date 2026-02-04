"""Validation helpers for wireless_controller/syslog_profile - Auto-generated"""

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
    "server-status": "enable",
    "server": "",
    "server-port": 514,
    "server-type": "standard",
    "log-level": "information",
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
    "name": "string",  # WTP system log server profile name.
    "comment": "var-string",  # Comment.
    "server-status": "option",  # Enable/disable FortiAP units to send log messages to a syslog server (default = 
    "server": "string",  # Syslog server CN domain name or IP address.
    "server-port": "integer",  # Port number of syslog server that FortiAP units send log messages to (default = 
    "server-type": "option",  # Configure syslog server type (default = standard).
    "log-level": "option",  # Lowest level of log messages that FortiAP units send to this server (default = i
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "WTP system log server profile name.",
    "comment": "Comment.",
    "server-status": "Enable/disable FortiAP units to send log messages to a syslog server (default = enable).",
    "server": "Syslog server CN domain name or IP address.",
    "server-port": "Port number of syslog server that FortiAP units send log messages to (default = 514).",
    "server-type": "Configure syslog server type (default = standard).",
    "log-level": "Lowest level of log messages that FortiAP units send to this server (default = information).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "server": {"type": "string", "max_length": 63},
    "server-port": {"type": "integer", "min": 0, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_SERVER_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SERVER_TYPE = [
    "standard",
    "fortianalyzer",
]
VALID_BODY_LOG_LEVEL = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debugging",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_syslog_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/syslog_profile."""
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


def validate_wireless_controller_syslog_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/syslog_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "server-status" in payload:
        is_valid, error = _validate_enum_field(
            "server-status",
            payload["server-status"],
            VALID_BODY_SERVER_STATUS,
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
    if "log-level" in payload:
        is_valid, error = _validate_enum_field(
            "log-level",
            payload["log-level"],
            VALID_BODY_LOG_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_syslog_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/syslog_profile."""
    # Validate enum values using central function
    if "server-status" in payload:
        is_valid, error = _validate_enum_field(
            "server-status",
            payload["server-status"],
            VALID_BODY_SERVER_STATUS,
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
    if "log-level" in payload:
        is_valid, error = _validate_enum_field(
            "log-level",
            payload["log-level"],
            VALID_BODY_LOG_LEVEL,
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
    "endpoint": "wireless_controller/syslog_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/syslog-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Wireless Termination Points (WTP) system log server profile.",
    "total_fields": 7,
    "required_fields_count": 0,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
