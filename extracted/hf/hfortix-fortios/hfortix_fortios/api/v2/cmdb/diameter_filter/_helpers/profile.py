"""Validation helpers for diameter_filter/profile - Auto-generated"""

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
    "name",  # Profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "monitor-all-messages": "disable",
    "log-packet": "disable",
    "track-requests-answers": "enable",
    "missing-request-action": "block",
    "protocol-version-invalid": "block",
    "message-length-invalid": "block",
    "request-error-flag-set": "block",
    "cmd-flags-reserve-set": "block",
    "command-code-invalid": "block",
    "command-code-range": "",
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
    "name": "string",  # Profile name.
    "comment": "var-string",  # Comment.
    "monitor-all-messages": "option",  # Enable/disable logging for all User Name and Result Code AVP
    "log-packet": "option",  # Enable/disable packet log for triggered diameter settings.
    "track-requests-answers": "option",  # Enable/disable validation that each answer has a correspondi
    "missing-request-action": "option",  # Action to be taken for answers without corresponding request
    "protocol-version-invalid": "option",  # Action to be taken for invalid protocol version.
    "message-length-invalid": "option",  # Action to be taken for invalid message length.
    "request-error-flag-set": "option",  # Action to be taken for request messages with error flag set.
    "cmd-flags-reserve-set": "option",  # Action to be taken for messages with cmd flag reserve bits s
    "command-code-invalid": "option",  # Action to be taken for messages with invalid command code.
    "command-code-range": "user",  # Valid range for command codes (0-16777215).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "comment": "Comment.",
    "monitor-all-messages": "Enable/disable logging for all User Name and Result Code AVP messages.",
    "log-packet": "Enable/disable packet log for triggered diameter settings.",
    "track-requests-answers": "Enable/disable validation that each answer has a corresponding request.",
    "missing-request-action": "Action to be taken for answers without corresponding request.",
    "protocol-version-invalid": "Action to be taken for invalid protocol version.",
    "message-length-invalid": "Action to be taken for invalid message length.",
    "request-error-flag-set": "Action to be taken for request messages with error flag set.",
    "cmd-flags-reserve-set": "Action to be taken for messages with cmd flag reserve bits set.",
    "command-code-invalid": "Action to be taken for messages with invalid command code.",
    "command-code-range": "Valid range for command codes (0-16777215).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_MONITOR_ALL_MESSAGES = [
    "disable",
    "enable",
]
VALID_BODY_LOG_PACKET = [
    "disable",
    "enable",
]
VALID_BODY_TRACK_REQUESTS_ANSWERS = [
    "disable",
    "enable",
]
VALID_BODY_MISSING_REQUEST_ACTION = [
    "allow",
    "block",
    "reset",
    "monitor",
]
VALID_BODY_PROTOCOL_VERSION_INVALID = [
    "allow",
    "block",
    "reset",
    "monitor",
]
VALID_BODY_MESSAGE_LENGTH_INVALID = [
    "allow",
    "block",
    "reset",
    "monitor",
]
VALID_BODY_REQUEST_ERROR_FLAG_SET = [
    "allow",
    "block",
    "reset",
    "monitor",
]
VALID_BODY_CMD_FLAGS_RESERVE_SET = [
    "allow",
    "block",
    "reset",
    "monitor",
]
VALID_BODY_COMMAND_CODE_INVALID = [
    "allow",
    "block",
    "reset",
    "monitor",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_diameter_filter_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for diameter_filter/profile."""
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


def validate_diameter_filter_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new diameter_filter/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "monitor-all-messages" in payload:
        is_valid, error = _validate_enum_field(
            "monitor-all-messages",
            payload["monitor-all-messages"],
            VALID_BODY_MONITOR_ALL_MESSAGES,
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
    if "track-requests-answers" in payload:
        is_valid, error = _validate_enum_field(
            "track-requests-answers",
            payload["track-requests-answers"],
            VALID_BODY_TRACK_REQUESTS_ANSWERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "missing-request-action" in payload:
        is_valid, error = _validate_enum_field(
            "missing-request-action",
            payload["missing-request-action"],
            VALID_BODY_MISSING_REQUEST_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol-version-invalid" in payload:
        is_valid, error = _validate_enum_field(
            "protocol-version-invalid",
            payload["protocol-version-invalid"],
            VALID_BODY_PROTOCOL_VERSION_INVALID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "message-length-invalid" in payload:
        is_valid, error = _validate_enum_field(
            "message-length-invalid",
            payload["message-length-invalid"],
            VALID_BODY_MESSAGE_LENGTH_INVALID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "request-error-flag-set" in payload:
        is_valid, error = _validate_enum_field(
            "request-error-flag-set",
            payload["request-error-flag-set"],
            VALID_BODY_REQUEST_ERROR_FLAG_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmd-flags-reserve-set" in payload:
        is_valid, error = _validate_enum_field(
            "cmd-flags-reserve-set",
            payload["cmd-flags-reserve-set"],
            VALID_BODY_CMD_FLAGS_RESERVE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "command-code-invalid" in payload:
        is_valid, error = _validate_enum_field(
            "command-code-invalid",
            payload["command-code-invalid"],
            VALID_BODY_COMMAND_CODE_INVALID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_diameter_filter_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update diameter_filter/profile."""
    # Validate enum values using central function
    if "monitor-all-messages" in payload:
        is_valid, error = _validate_enum_field(
            "monitor-all-messages",
            payload["monitor-all-messages"],
            VALID_BODY_MONITOR_ALL_MESSAGES,
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
    if "track-requests-answers" in payload:
        is_valid, error = _validate_enum_field(
            "track-requests-answers",
            payload["track-requests-answers"],
            VALID_BODY_TRACK_REQUESTS_ANSWERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "missing-request-action" in payload:
        is_valid, error = _validate_enum_field(
            "missing-request-action",
            payload["missing-request-action"],
            VALID_BODY_MISSING_REQUEST_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol-version-invalid" in payload:
        is_valid, error = _validate_enum_field(
            "protocol-version-invalid",
            payload["protocol-version-invalid"],
            VALID_BODY_PROTOCOL_VERSION_INVALID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "message-length-invalid" in payload:
        is_valid, error = _validate_enum_field(
            "message-length-invalid",
            payload["message-length-invalid"],
            VALID_BODY_MESSAGE_LENGTH_INVALID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "request-error-flag-set" in payload:
        is_valid, error = _validate_enum_field(
            "request-error-flag-set",
            payload["request-error-flag-set"],
            VALID_BODY_REQUEST_ERROR_FLAG_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmd-flags-reserve-set" in payload:
        is_valid, error = _validate_enum_field(
            "cmd-flags-reserve-set",
            payload["cmd-flags-reserve-set"],
            VALID_BODY_CMD_FLAGS_RESERVE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "command-code-invalid" in payload:
        is_valid, error = _validate_enum_field(
            "command-code-invalid",
            payload["command-code-invalid"],
            VALID_BODY_COMMAND_CODE_INVALID,
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
    "endpoint": "diameter_filter/profile",
    "category": "cmdb",
    "api_path": "diameter-filter/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Diameter filter profiles.",
    "total_fields": 12,
    "required_fields_count": 1,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
