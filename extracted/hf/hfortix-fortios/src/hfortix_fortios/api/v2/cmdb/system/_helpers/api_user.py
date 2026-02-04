"""Validation helpers for system/api_user - Auto-generated"""

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
    "accprofile",  # Admin user access profile.
    "peer-group",  # Peer group name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "accprofile": "",
    "schedule": "",
    "cors-allow-origin": "",
    "peer-auth": "disable",
    "peer-group": "",
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
    "name": "string",  # User name.
    "comments": "var-string",  # Comment.
    "api-key": "password-2",  # Admin user password.
    "accprofile": "string",  # Admin user access profile.
    "vdom": "string",  # Virtual domains.
    "schedule": "string",  # Schedule name.
    "cors-allow-origin": "string",  # Value for Access-Control-Allow-Origin on API responses. Avoid using '*' if possi
    "peer-auth": "option",  # Enable/disable peer authentication.
    "peer-group": "string",  # Peer group name.
    "trusthost": "string",  # Trusthost.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "User name.",
    "comments": "Comment.",
    "api-key": "Admin user password.",
    "accprofile": "Admin user access profile.",
    "vdom": "Virtual domains.",
    "schedule": "Schedule name.",
    "cors-allow-origin": "Value for Access-Control-Allow-Origin on API responses. Avoid using '*' if possible.",
    "peer-auth": "Enable/disable peer authentication.",
    "peer-group": "Peer group name.",
    "trusthost": "Trusthost.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "accprofile": {"type": "string", "max_length": 35},
    "schedule": {"type": "string", "max_length": 35},
    "cors-allow-origin": {"type": "string", "max_length": 269},
    "peer-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "vdom": {
        "name": {
            "type": "string",
            "help": "Virtual domain name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "trusthost": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "type": {
            "type": "option",
            "help": "Trusthost type.",
            "default": "ipv4-trusthost",
            "options": ["ipv4-trusthost", "ipv6-trusthost"],
        },
        "ipv4-trusthost": {
            "type": "ipv4-classnet",
            "help": "IPv4 trusted host address.",
            "default": "0.0.0.0 0.0.0.0",
        },
        "ipv6-trusthost": {
            "type": "ipv6-prefix",
            "help": "IPv6 trusted host address.",
            "default": "::/0",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_PEER_AUTH = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_api_user_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/api_user."""
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


def validate_system_api_user_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/api_user object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "peer-auth" in payload:
        is_valid, error = _validate_enum_field(
            "peer-auth",
            payload["peer-auth"],
            VALID_BODY_PEER_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_api_user_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/api_user."""
    # Validate enum values using central function
    if "peer-auth" in payload:
        is_valid, error = _validate_enum_field(
            "peer-auth",
            payload["peer-auth"],
            VALID_BODY_PEER_AUTH,
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
    "endpoint": "system/api_user",
    "category": "cmdb",
    "api_path": "system/api-user",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure API users.",
    "total_fields": 10,
    "required_fields_count": 2,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
