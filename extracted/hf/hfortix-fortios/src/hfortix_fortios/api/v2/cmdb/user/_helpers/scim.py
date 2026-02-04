"""Validation helpers for user/scim - Auto-generated"""

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
    "name",  # SCIM client name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "id": 0,
    "status": "disable",
    "base-url": "",
    "auth-method": "token",
    "token-certificate": "",
    "certificate": "",
    "client-identity-check": "enable",
    "cascade": "disable",
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
    "name": "string",  # SCIM client name.
    "id": "integer",  # SCIM client ID.
    "status": "option",  # Enable/disable System for Cross-domain Identity Management (SCIM).
    "base-url": "string",  # Server URL to receive SCIM create, read, update, delete (CRUD) requests.
    "auth-method": "option",  # TLS client authentication methods (default = bearer token).
    "token-certificate": "string",  # Certificate for token verification.
    "secret": "password",  # Secret for token verification or base authentication.
    "certificate": "string",  # Certificate for client verification during TLS handshake.
    "client-identity-check": "option",  # Enable/disable client identity check.
    "cascade": "option",  # Enable/disable to follow SCIM users/groups changes in IDP.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "SCIM client name.",
    "id": "SCIM client ID.",
    "status": "Enable/disable System for Cross-domain Identity Management (SCIM).",
    "base-url": "Server URL to receive SCIM create, read, update, delete (CRUD) requests.",
    "auth-method": "TLS client authentication methods (default = bearer token).",
    "token-certificate": "Certificate for token verification.",
    "secret": "Secret for token verification or base authentication.",
    "certificate": "Certificate for client verification during TLS handshake.",
    "client-identity-check": "Enable/disable client identity check.",
    "cascade": "Enable/disable to follow SCIM users/groups changes in IDP.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "base-url": {"type": "string", "max_length": 127},
    "token-certificate": {"type": "string", "max_length": 79},
    "certificate": {"type": "string", "max_length": 79},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_METHOD = [
    "token",
    "base",
]
VALID_BODY_CLIENT_IDENTITY_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_CASCADE = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_scim_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/scim."""
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


def validate_user_scim_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/scim object."""
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
    if "auth-method" in payload:
        is_valid, error = _validate_enum_field(
            "auth-method",
            payload["auth-method"],
            VALID_BODY_AUTH_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "client-identity-check",
            payload["client-identity-check"],
            VALID_BODY_CLIENT_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cascade" in payload:
        is_valid, error = _validate_enum_field(
            "cascade",
            payload["cascade"],
            VALID_BODY_CASCADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_scim_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/scim."""
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
    if "auth-method" in payload:
        is_valid, error = _validate_enum_field(
            "auth-method",
            payload["auth-method"],
            VALID_BODY_AUTH_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "client-identity-check",
            payload["client-identity-check"],
            VALID_BODY_CLIENT_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cascade" in payload:
        is_valid, error = _validate_enum_field(
            "cascade",
            payload["cascade"],
            VALID_BODY_CASCADE,
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
    "endpoint": "user/scim",
    "category": "cmdb",
    "api_path": "user/scim",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure SCIM client entries.",
    "total_fields": 10,
    "required_fields_count": 1,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
