"""Validation helpers for wireless_controller/snmp - Auto-generated"""

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
    "engine-id": "",
    "contact-info": "",
    "trap-high-cpu-threshold": 80,
    "trap-high-mem-threshold": 80,
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
    "engine-id": "string",  # AC SNMP engineID string (maximum 24 characters).
    "contact-info": "string",  # Contact Information.
    "trap-high-cpu-threshold": "integer",  # CPU usage when trap is sent.
    "trap-high-mem-threshold": "integer",  # Memory usage when trap is sent.
    "community": "string",  # SNMP Community Configuration.
    "user": "string",  # SNMP User Configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "engine-id": "AC SNMP engineID string (maximum 24 characters).",
    "contact-info": "Contact Information.",
    "trap-high-cpu-threshold": "CPU usage when trap is sent.",
    "trap-high-mem-threshold": "Memory usage when trap is sent.",
    "community": "SNMP Community Configuration.",
    "user": "SNMP User Configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "engine-id": {"type": "string", "max_length": 23},
    "contact-info": {"type": "string", "max_length": 31},
    "trap-high-cpu-threshold": {"type": "integer", "min": 10, "max": 100},
    "trap-high-mem-threshold": {"type": "integer", "min": 10, "max": 100},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "community": {
        "id": {
            "type": "integer",
            "help": "Community ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "name": {
            "type": "string",
            "help": "Community name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this SNMP community.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "query-v1-status": {
            "type": "option",
            "help": "Enable/disable SNMP v1 queries.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "query-v2c-status": {
            "type": "option",
            "help": "Enable/disable SNMP v2c queries.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "trap-v1-status": {
            "type": "option",
            "help": "Enable/disable SNMP v1 traps.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "trap-v2c-status": {
            "type": "option",
            "help": "Enable/disable SNMP v2c traps.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "hosts": {
            "type": "string",
            "help": "Configure IPv4 SNMP managers (hosts).",
        },
        "hosts6": {
            "type": "string",
            "help": "Configure IPv6 SNMP managers (hosts).",
        },
    },
    "user": {
        "name": {
            "type": "string",
            "help": "SNMP user name.",
            "required": True,
            "default": "",
            "max_length": 32,
        },
        "status": {
            "type": "option",
            "help": "SNMP user enable.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "queries": {
            "type": "option",
            "help": "Enable/disable SNMP queries for this user.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "trap-status": {
            "type": "option",
            "help": "Enable/disable traps for this SNMP user.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "security-level": {
            "type": "option",
            "help": "Security level for message authentication and encryption.",
            "default": "no-auth-no-priv",
            "options": ["no-auth-no-priv", "auth-no-priv", "auth-priv"],
        },
        "auth-proto": {
            "type": "option",
            "help": "Authentication protocol.",
            "default": "sha",
            "options": ["md5", "sha", "sha224", "sha256", "sha384", "sha512"],
        },
        "auth-pwd": {
            "type": "password",
            "help": "Password for authentication protocol.",
            "required": True,
            "max_length": 128,
        },
        "priv-proto": {
            "type": "option",
            "help": "Privacy (encryption) protocol.",
            "default": "aes",
            "options": ["aes", "des", "aes256", "aes256cisco"],
        },
        "priv-pwd": {
            "type": "password",
            "help": "Password for privacy (encryption) protocol.",
            "required": True,
            "max_length": 128,
        },
        "notify-hosts": {
            "type": "ipv4-address",
            "help": "Configure SNMP User Notify Hosts.",
            "default": "",
        },
        "notify-hosts6": {
            "type": "ipv6-address",
            "help": "Configure IPv6 SNMP User Notify Hosts.",
            "default": "",
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_snmp_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/snmp."""
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


def validate_wireless_controller_snmp_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/snmp object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_snmp_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/snmp."""
    # Validate enum values using central function

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
    "endpoint": "wireless_controller/snmp",
    "category": "cmdb",
    "api_path": "wireless-controller/snmp",
    "help": "Configure SNMP.",
    "total_fields": 6,
    "required_fields_count": 0,
    "fields_with_defaults_count": 4,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
