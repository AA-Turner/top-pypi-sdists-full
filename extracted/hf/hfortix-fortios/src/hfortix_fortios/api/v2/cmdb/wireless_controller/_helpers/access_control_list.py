"""Validation helpers for wireless_controller/access_control_list - Auto-generated"""

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
    "comment": "",
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
    "name": "string",  # AP access control list name.
    "comment": "string",  # Description.
    "layer3-ipv4-rules": "string",  # AP ACL layer3 ipv4 rule list.
    "layer3-ipv6-rules": "string",  # AP ACL layer3 ipv6 rule list.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "AP access control list name.",
    "comment": "Description.",
    "layer3-ipv4-rules": "AP ACL layer3 ipv4 rule list.",
    "layer3-ipv6-rules": "AP ACL layer3 ipv6 rule list.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "comment": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "layer3-ipv4-rules": {
        "rule-id": {
            "type": "integer",
            "help": "Rule ID (1 - 65535).",
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
        "comment": {
            "type": "string",
            "help": "Description.",
            "default": "",
            "max_length": 63,
        },
        "srcaddr": {
            "type": "user",
            "help": "Source IP address (any | local-LAN | IPv4 address[/<network mask | mask length>], default = any).",
            "default": "",
        },
        "srcport": {
            "type": "integer",
            "help": "Source port (0 - 65535, default = 0, meaning any).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "dstaddr": {
            "type": "user",
            "help": "Destination IP address (any | local-LAN | IPv4 address[/<network mask | mask length>], default = any).",
            "default": "",
        },
        "dstport": {
            "type": "integer",
            "help": "Destination port (0 - 65535, default = 0, meaning any).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "protocol": {
            "type": "integer",
            "help": "Protocol type as defined by IANA (0 - 255, default = 255, meaning any).",
            "default": 255,
            "min_value": 0,
            "max_value": 255,
        },
        "action": {
            "type": "option",
            "help": "Policy action (allow | deny).",
            "default": "",
            "options": ["allow", "deny"],
        },
    },
    "layer3-ipv6-rules": {
        "rule-id": {
            "type": "integer",
            "help": "Rule ID (1 - 65535).",
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
        "comment": {
            "type": "string",
            "help": "Description.",
            "default": "",
            "max_length": 63,
        },
        "srcaddr": {
            "type": "user",
            "help": "Source IPv6 address (any | local-LAN | IPv6 address[/prefix length]), default = any.",
            "default": "",
        },
        "srcport": {
            "type": "integer",
            "help": "Source port (0 - 65535, default = 0, meaning any).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "dstaddr": {
            "type": "user",
            "help": "Destination IPv6 address (any | local-LAN | IPv6 address[/prefix length]), default = any.",
            "default": "",
        },
        "dstport": {
            "type": "integer",
            "help": "Destination port (0 - 65535, default = 0, meaning any).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "protocol": {
            "type": "integer",
            "help": "Protocol type as defined by IANA (0 - 255, default = 255, meaning any).",
            "default": 255,
            "min_value": 0,
            "max_value": 255,
        },
        "action": {
            "type": "option",
            "help": "Policy action (allow | deny).",
            "default": "",
            "options": ["allow", "deny"],
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_access_control_list_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/access_control_list."""
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


def validate_wireless_controller_access_control_list_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/access_control_list object."""
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


def validate_wireless_controller_access_control_list_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/access_control_list."""
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
    "endpoint": "wireless_controller/access_control_list",
    "category": "cmdb",
    "api_path": "wireless-controller/access-control-list",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure WiFi bridge access control list.",
    "total_fields": 4,
    "required_fields_count": 0,
    "fields_with_defaults_count": 2,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
