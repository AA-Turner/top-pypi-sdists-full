"""Validation helpers for user/password_policy - Auto-generated"""

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
    "expire-status": "disable",
    "expire-days": 180,
    "warn-days": 15,
    "expired-password-renewal": "disable",
    "minimum-length": 8,
    "min-lower-case-letter": 0,
    "min-upper-case-letter": 0,
    "min-non-alphanumeric": 0,
    "min-number": 0,
    "min-change-characters": 0,
    "reuse-password": "enable",
    "reuse-password-limit": 0,
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
    "name": "string",  # Password policy name.
    "expire-status": "option",  # Enable/disable password expiration.
    "expire-days": "integer",  # Time in days before the user's password expires.
    "warn-days": "integer",  # Time in days before a password expiration warning message is displayed to the us
    "expired-password-renewal": "option",  # Enable/disable renewal of a password that already is expired.
    "minimum-length": "integer",  # Minimum password length (8 - 128, default = 8).
    "min-lower-case-letter": "integer",  # Minimum number of lowercase characters in password (0 - 128, default = 0).
    "min-upper-case-letter": "integer",  # Minimum number of uppercase characters in password (0 - 128, default = 0).
    "min-non-alphanumeric": "integer",  # Minimum number of non-alphanumeric characters in password (0 - 128, default = 0)
    "min-number": "integer",  # Minimum number of numeric characters in password (0 - 128, default = 0).
    "min-change-characters": "integer",  # Minimum number of unique characters in new password which do not exist in old pa
    "reuse-password": "option",  # Enable/disable reuse of password. If both reuse-password and min-change-characte
    "reuse-password-limit": "integer",  # Number of times passwords can be reused (0 - 20, default = 0. If set to 0, can r
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Password policy name.",
    "expire-status": "Enable/disable password expiration.",
    "expire-days": "Time in days before the user's password expires.",
    "warn-days": "Time in days before a password expiration warning message is displayed to the user upon login.",
    "expired-password-renewal": "Enable/disable renewal of a password that already is expired.",
    "minimum-length": "Minimum password length (8 - 128, default = 8).",
    "min-lower-case-letter": "Minimum number of lowercase characters in password (0 - 128, default = 0).",
    "min-upper-case-letter": "Minimum number of uppercase characters in password (0 - 128, default = 0).",
    "min-non-alphanumeric": "Minimum number of non-alphanumeric characters in password (0 - 128, default = 0).",
    "min-number": "Minimum number of numeric characters in password (0 - 128, default = 0).",
    "min-change-characters": "Minimum number of unique characters in new password which do not exist in old password (0 - 128, default = 0. This attribute overrides reuse-password if both are enabled).",
    "reuse-password": "Enable/disable reuse of password. If both reuse-password and min-change-characters are enabled, min-change-characters overrides.",
    "reuse-password-limit": "Number of times passwords can be reused (0 - 20, default = 0. If set to 0, can reuse password an unlimited number of times.).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "expire-days": {"type": "integer", "min": 0, "max": 999},
    "warn-days": {"type": "integer", "min": 0, "max": 30},
    "minimum-length": {"type": "integer", "min": 8, "max": 128},
    "min-lower-case-letter": {"type": "integer", "min": 0, "max": 128},
    "min-upper-case-letter": {"type": "integer", "min": 0, "max": 128},
    "min-non-alphanumeric": {"type": "integer", "min": 0, "max": 128},
    "min-number": {"type": "integer", "min": 0, "max": 128},
    "min-change-characters": {"type": "integer", "min": 0, "max": 128},
    "reuse-password-limit": {"type": "integer", "min": 0, "max": 20},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_EXPIRE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_EXPIRED_PASSWORD_RENEWAL = [
    "enable",
    "disable",
]
VALID_BODY_REUSE_PASSWORD = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_password_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/password_policy."""
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


def validate_user_password_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/password_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "expire-status" in payload:
        is_valid, error = _validate_enum_field(
            "expire-status",
            payload["expire-status"],
            VALID_BODY_EXPIRE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "expired-password-renewal" in payload:
        is_valid, error = _validate_enum_field(
            "expired-password-renewal",
            payload["expired-password-renewal"],
            VALID_BODY_EXPIRED_PASSWORD_RENEWAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reuse-password" in payload:
        is_valid, error = _validate_enum_field(
            "reuse-password",
            payload["reuse-password"],
            VALID_BODY_REUSE_PASSWORD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_password_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/password_policy."""
    # Validate enum values using central function
    if "expire-status" in payload:
        is_valid, error = _validate_enum_field(
            "expire-status",
            payload["expire-status"],
            VALID_BODY_EXPIRE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "expired-password-renewal" in payload:
        is_valid, error = _validate_enum_field(
            "expired-password-renewal",
            payload["expired-password-renewal"],
            VALID_BODY_EXPIRED_PASSWORD_RENEWAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reuse-password" in payload:
        is_valid, error = _validate_enum_field(
            "reuse-password",
            payload["reuse-password"],
            VALID_BODY_REUSE_PASSWORD,
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
    "endpoint": "user/password_policy",
    "category": "cmdb",
    "api_path": "user/password-policy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure user password policy.",
    "total_fields": 13,
    "required_fields_count": 0,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
