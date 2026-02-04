"""Validation helpers for user/external_identity_provider - Auto-generated"""

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
    "type",  # External identity provider type.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "type": "",
    "version": "",
    "url": "",
    "user-attr-name": "userPrincipalName",
    "group-attr-name": "id",
    "port": 0,
    "source-ip": "",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
    "server-identity-check": "enable",
    "timeout": 5,
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
    "name": "string",  # External identity provider name.
    "type": "option",  # External identity provider type.
    "version": "option",  # External identity API version.
    "url": "string",  # External identity provider URL (e.g. \"https://example.com:8080/api/v1\").
    "user-attr-name": "string",  # User attribute name in authentication query.
    "group-attr-name": "string",  # Group attribute name in authentication query.
    "port": "integer",  # External identity provider service port number (0 to use default).
    "source-ip": "string",  # Use this IPv4/v6 address to connect to the external identity provider.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "server-identity-check": "option",  # Enable/disable server's identity check against its certificate and subject alter
    "timeout": "integer",  # Connection timeout value in seconds (default=5).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "External identity provider name.",
    "type": "External identity provider type.",
    "version": "External identity API version.",
    "url": "External identity provider URL (e.g. \"https://example.com:8080/api/v1\").",
    "user-attr-name": "User attribute name in authentication query.",
    "group-attr-name": "Group attribute name in authentication query.",
    "port": "External identity provider service port number (0 to use default).",
    "source-ip": "Use this IPv4/v6 address to connect to the external identity provider.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "server-identity-check": "Enable/disable server's identity check against its certificate and subject alternative name(s).",
    "timeout": "Connection timeout value in seconds (default=5).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "url": {"type": "string", "max_length": 127},
    "user-attr-name": {"type": "string", "max_length": 63},
    "group-attr-name": {"type": "string", "max_length": 63},
    "port": {"type": "integer", "min": 0, "max": 65535},
    "source-ip": {"type": "string", "max_length": 63},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "timeout": {"type": "integer", "min": 1, "max": 60},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "ms-graph",
]
VALID_BODY_VERSION = [
    "v1.0",
    "beta",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_SERVER_IDENTITY_CHECK = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_external_identity_provider_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/external_identity_provider."""
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


def validate_user_external_identity_provider_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/external_identity_provider object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "version" in payload:
        is_valid, error = _validate_enum_field(
            "version",
            payload["version"],
            VALID_BODY_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_external_identity_provider_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/external_identity_provider."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "version" in payload:
        is_valid, error = _validate_enum_field(
            "version",
            payload["version"],
            VALID_BODY_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
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
    "endpoint": "user/external_identity_provider",
    "category": "cmdb",
    "api_path": "user/external-identity-provider",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure external identity provider.",
    "total_fields": 13,
    "required_fields_count": 2,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
