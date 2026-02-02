"""Validation helpers for system/password_policy_guest_admin - Auto-generated"""

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
    "status": "disable",
    "apply-to": "guest-admin-password",
    "minimum-length": 12,
    "min-lower-case-letter": 1,
    "min-upper-case-letter": 1,
    "min-non-alphanumeric": 1,
    "min-number": 1,
    "expire-status": "disable",
    "expire-day": 90,
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
    "status": "option",  # Enable/disable setting a password policy for locally defined
    "apply-to": "option",  # Guest administrator to which this password policy applies.
    "minimum-length": "integer",  # Minimum password length (12 - 128, default = 12).
    "min-lower-case-letter": "integer",  # Minimum number of lowercase characters in password (0 - 128,
    "min-upper-case-letter": "integer",  # Minimum number of uppercase characters in password (0 - 128,
    "min-non-alphanumeric": "integer",  # Minimum number of non-alphanumeric characters in password (0
    "min-number": "integer",  # Minimum number of numeric characters in password (0 - 128, d
    "expire-status": "option",  # Enable/disable password expiration.
    "expire-day": "integer",  # Number of days after which passwords expire (1 - 999 days, d
    "reuse-password": "option",  # Enable/disable reuse of password.
    "reuse-password-limit": "integer",  # Number of times passwords can be reused (0 - 20, default = 0
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable setting a password policy for locally defined administrator passwords and IPsec VPN pre-shared keys.",
    "apply-to": "Guest administrator to which this password policy applies.",
    "minimum-length": "Minimum password length (12 - 128, default = 12).",
    "min-lower-case-letter": "Minimum number of lowercase characters in password (0 - 128, default = 1).",
    "min-upper-case-letter": "Minimum number of uppercase characters in password (0 - 128, default = 1).",
    "min-non-alphanumeric": "Minimum number of non-alphanumeric characters in password (0 - 128, default = 1).",
    "min-number": "Minimum number of numeric characters in password (0 - 128, default = 1).",
    "expire-status": "Enable/disable password expiration.",
    "expire-day": "Number of days after which passwords expire (1 - 999 days, default = 90).",
    "reuse-password": "Enable/disable reuse of password.",
    "reuse-password-limit": "Number of times passwords can be reused (0 - 20, default = 0. If set to 0, can reuse password an unlimited number of times.).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "minimum-length": {"type": "integer", "min": 12, "max": 128},
    "min-lower-case-letter": {"type": "integer", "min": 0, "max": 128},
    "min-upper-case-letter": {"type": "integer", "min": 0, "max": 128},
    "min-non-alphanumeric": {"type": "integer", "min": 0, "max": 128},
    "min-number": {"type": "integer", "min": 0, "max": 128},
    "expire-day": {"type": "integer", "min": 1, "max": 999},
    "reuse-password-limit": {"type": "integer", "min": 0, "max": 20},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_APPLY_TO = [
    "guest-admin-password",
]
VALID_BODY_EXPIRE_STATUS = [
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


def validate_system_password_policy_guest_admin_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/password_policy_guest_admin."""
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


def validate_system_password_policy_guest_admin_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/password_policy_guest_admin object."""
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
    if "apply-to" in payload:
        is_valid, error = _validate_enum_field(
            "apply-to",
            payload["apply-to"],
            VALID_BODY_APPLY_TO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "expire-status" in payload:
        is_valid, error = _validate_enum_field(
            "expire-status",
            payload["expire-status"],
            VALID_BODY_EXPIRE_STATUS,
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


def validate_system_password_policy_guest_admin_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/password_policy_guest_admin."""
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
    if "apply-to" in payload:
        is_valid, error = _validate_enum_field(
            "apply-to",
            payload["apply-to"],
            VALID_BODY_APPLY_TO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "expire-status" in payload:
        is_valid, error = _validate_enum_field(
            "expire-status",
            payload["expire-status"],
            VALID_BODY_EXPIRE_STATUS,
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
    "endpoint": "system/password_policy_guest_admin",
    "category": "cmdb",
    "api_path": "system/password-policy-guest-admin",
    "help": "Configure the password policy for guest administrators.",
    "total_fields": 11,
    "required_fields_count": 0,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
