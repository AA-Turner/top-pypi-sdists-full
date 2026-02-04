"""Validation helpers for rule/fmwp - Auto-generated"""

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
    "status": "enable",
    "log": "enable",
    "log-packet": "disable",
    "action": "pass",
    "group": "",
    "severity": "",
    "location": "",
    "os": "",
    "application": "",
    "service": "",
    "rule-id": 0,
    "rev": 0,
    "date": 0,
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
    "name": "string",  # Rule name.
    "status": "key",  # Print all FMWP rules information.
    "log": "option",  # Enable/disable logging.
    "log-packet": "option",  # Enable/disable packet logging.
    "action": "option",  # Action.
    "group": "string",  # Group.
    "severity": "user",  # Severity.
    "location": "user",  # Vulnerable location.
    "os": "user",  # Vulnerable operation systems.
    "application": "user",  # Vulnerable applications.
    "service": "user",  # Vulnerable service.
    "rule-id": "integer",  # Rule ID.
    "rev": "integer",  # Revision.
    "date": "integer",  # Date.
    "metadata": "string",  # Meta data.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Rule name.",
    "status": "Print all FMWP rules information.",
    "log": "Enable/disable logging.",
    "log-packet": "Enable/disable packet logging.",
    "action": "Action.",
    "group": "Group.",
    "severity": "Severity.",
    "location": "Vulnerable location.",
    "os": "Vulnerable operation systems.",
    "application": "Vulnerable applications.",
    "service": "Vulnerable service.",
    "rule-id": "Rule ID.",
    "rev": "Revision.",
    "date": "Date.",
    "metadata": "Meta data.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "group": {"type": "string", "max_length": 63},
    "rule-id": {"type": "integer", "min": 0, "max": 4294967295},
    "rev": {"type": "integer", "min": 0, "max": 4294967295},
    "date": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "metadata": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "metaid": {
            "type": "integer",
            "help": "Meta ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "valueid": {
            "type": "integer",
            "help": "Value ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_LOG = [
    "disable",
    "enable",
]
VALID_BODY_LOG_PACKET = [
    "disable",
    "enable",
]
VALID_BODY_ACTION = [
    "pass",
    "block",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_rule_fmwp_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for rule/fmwp."""
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


def validate_rule_fmwp_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new rule/fmwp object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log" in payload:
        is_valid, error = _validate_enum_field(
            "log",
            payload["log"],
            VALID_BODY_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-packet" in payload:
        is_valid, error = _validate_enum_field(
            "log-packet",
            payload["log-packet"],
            VALID_BODY_LOG_PACKET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_rule_fmwp_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update rule/fmwp."""
    # Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log" in payload:
        is_valid, error = _validate_enum_field(
            "log",
            payload["log"],
            VALID_BODY_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-packet" in payload:
        is_valid, error = _validate_enum_field(
            "log-packet",
            payload["log-packet"],
            VALID_BODY_LOG_PACKET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
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
    "endpoint": "rule/fmwp",
    "category": "cmdb",
    "api_path": "rule/fmwp",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Show FMWP signatures.",
    "total_fields": 15,
    "required_fields_count": 0,
    "fields_with_defaults_count": 14,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
