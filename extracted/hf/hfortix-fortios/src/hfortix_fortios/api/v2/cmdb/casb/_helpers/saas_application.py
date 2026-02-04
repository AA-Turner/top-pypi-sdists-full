"""Validation helpers for casb/saas_application - Auto-generated"""

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
    "uuid": "",
    "status": "enable",
    "type": "customized",
    "casb-name": "",
    "description": "",
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
    "name": "string",  # SaaS application name.
    "uuid": "string",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "status": "option",  # Enable/disable setting.
    "type": "option",  # SaaS application type.
    "casb-name": "string",  # SaaS application signature name.
    "description": "string",  # SaaS application description.
    "domains": "string",  # SaaS application domain list.
    "output-attributes": "string",  # SaaS application output attributes.
    "input-attributes": "string",  # SaaS application input attributes.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "SaaS application name.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "status": "Enable/disable setting.",
    "type": "SaaS application type.",
    "casb-name": "SaaS application signature name.",
    "description": "SaaS application description.",
    "domains": "SaaS application domain list.",
    "output-attributes": "SaaS application output attributes.",
    "input-attributes": "SaaS application input attributes.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "uuid": {"type": "string", "max_length": 36},
    "casb-name": {"type": "string", "max_length": 79},
    "description": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "domains": {
        "domain": {
            "type": "string",
            "help": "Domain list separated by space.",
            "required": True,
            "default": "",
            "max_length": 127,
        },
    },
    "output-attributes": {
        "name": {
            "type": "string",
            "help": "CASB attribute name.",
            "default": "",
            "max_length": 79,
        },
        "description": {
            "type": "string",
            "help": "CASB attribute description.",
            "default": "",
            "max_length": 63,
        },
        "type": {
            "type": "option",
            "help": "CASB attribute format type.",
            "default": "string",
            "options": ["string", "string-list", "integer", "integer-list", "boolean"],
        },
        "optional": {
            "type": "option",
            "help": "CASB output attribute optional.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
    },
    "input-attributes": {
        "name": {
            "type": "string",
            "help": "CASB attribute name.",
            "default": "",
            "max_length": 79,
        },
        "description": {
            "type": "string",
            "help": "CASB attribute description.",
            "default": "",
            "max_length": 63,
        },
        "type": {
            "type": "option",
            "help": "CASB attribute format type.",
            "default": "string",
            "options": ["string"],
        },
        "required": {
            "type": "option",
            "help": "CASB input attribute required.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "default": {
            "type": "option",
            "help": "CASB attribute default value.",
            "default": "string",
            "options": ["string", "string-list"],
        },
        "fallback-input": {
            "type": "option",
            "help": "CASB attribute legacy input.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_TYPE = [
    "built-in",
    "customized",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_casb_saas_application_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for casb/saas_application."""
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


def validate_casb_saas_application_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new casb/saas_application object."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_casb_saas_application_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update casb/saas_application."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
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
    "endpoint": "casb/saas_application",
    "category": "cmdb",
    "api_path": "casb/saas-application",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure CASB SaaS application.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
