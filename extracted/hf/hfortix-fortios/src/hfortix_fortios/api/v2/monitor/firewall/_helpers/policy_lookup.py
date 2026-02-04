"""Validation helpers for firewall/policy_lookup - Auto-generated"""

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
    "srcintf",  # 
    "sourceip",  # 
    "protocol",  # 
    "dest",  # 
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
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
    "ipv6": "boolean",  # 
    "srcintf": "string",  # 
    "sourceport": "int",  # 
    "sourceip": "string",  # 
    "protocol": "string",  # 
    "dest": "string",  # 
    "destport": "int",  # 
    "icmptype": "int",  # 
    "icmpcode": "int",  # 
    "policy_type": "string",  # 
    "auth_type": "string",  # 
    "user_group": "array",  # 
    "server_name": "string",  # 
    "user_db": "string",  # 
    "group_attr_type": "string",  # 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_POLICY_TYPE = [
    "policy",
    "proxy",
]
VALID_BODY_AUTH_TYPE = [
    "user",
    "group",
    "saml",
    "ldap",
]
VALID_BODY_GROUP_ATTR_TYPE = [
    "name",
    "id",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_policy_lookup_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/policy_lookup."""
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


def validate_firewall_policy_lookup_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/policy_lookup object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "policy_type" in payload:
        is_valid, error = _validate_enum_field(
            "policy_type",
            payload["policy_type"],
            VALID_BODY_POLICY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth_type" in payload:
        is_valid, error = _validate_enum_field(
            "auth_type",
            payload["auth_type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group_attr_type" in payload:
        is_valid, error = _validate_enum_field(
            "group_attr_type",
            payload["group_attr_type"],
            VALID_BODY_GROUP_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_policy_lookup_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/policy_lookup."""
    # Validate enum values using central function
    if "policy_type" in payload:
        is_valid, error = _validate_enum_field(
            "policy_type",
            payload["policy_type"],
            VALID_BODY_POLICY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth_type" in payload:
        is_valid, error = _validate_enum_field(
            "auth_type",
            payload["auth_type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group_attr_type" in payload:
        is_valid, error = _validate_enum_field(
            "group_attr_type",
            payload["group_attr_type"],
            VALID_BODY_GROUP_ATTR_TYPE,
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
    "endpoint": "firewall/policy_lookup",
    "category": "monitor",
    "api_path": "firewall/policy-lookup",
    "help": "Performs a policy lookup by creating a dummy packet and asking the kernel which policy would be hit.",
    "total_fields": 15,
    "required_fields_count": 4,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
