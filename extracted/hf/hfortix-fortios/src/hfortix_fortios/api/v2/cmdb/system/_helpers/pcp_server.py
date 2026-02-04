"""Validation helpers for system/pcp_server - Auto-generated"""

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
    "status": "option",  # Enable/disable PCP server.
    "pools": "string",  # Configure PCP pools.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable PCP server.",
    "pools": "Configure PCP pools.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "pools": {
        "name": {
            "type": "string",
            "help": "PCP pool name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "description": {
            "type": "string",
            "help": "Description.",
            "default": "",
            "max_length": 127,
        },
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "client-subnet": {
            "type": "string",
            "help": "Subnets from which PCP requests are accepted.",
            "required": True,
        },
        "ext-intf": {
            "type": "string",
            "help": "External interface name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "arp-reply": {
            "type": "option",
            "help": "Enable to respond to ARP requests for external IP (default = enable).",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "extip": {
            "type": "user",
            "help": "IP address or address range on the external interface that you want to map to an address on the internal network.",
            "required": True,
            "default": "",
        },
        "extport": {
            "type": "user",
            "help": "Incoming port number range that you want to map to a port number on the internal network.",
            "required": True,
            "default": "",
        },
        "minimal-lifetime": {
            "type": "integer",
            "help": "Minimal lifetime of a PCP mapping in seconds (60 - 300, default = 120).",
            "default": 120,
            "min_value": 60,
            "max_value": 300,
        },
        "maximal-lifetime": {
            "type": "integer",
            "help": "Maximal lifetime of a PCP mapping in seconds (3600 - 604800, default = 86400).",
            "default": 86400,
            "min_value": 3600,
            "max_value": 604800,
        },
        "client-mapping-limit": {
            "type": "integer",
            "help": "Mapping limit per client (0 - 65535, default = 0, 0 = unlimited).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "mapping-filter-limit": {
            "type": "integer",
            "help": "Filter limit per mapping (0 - 5, default = 1).",
            "default": 1,
            "min_value": 0,
            "max_value": 5,
        },
        "allow-opcode": {
            "type": "option",
            "help": "Allowed PCP opcode.",
            "default": "map peer announce",
            "options": ["map", "peer", "announce"],
        },
        "third-party": {
            "type": "option",
            "help": "Allow/disallow third party option.",
            "default": "disallow",
            "options": ["allow", "disallow"],
        },
        "third-party-subnet": {
            "type": "string",
            "help": "Subnets from which third party requests are accepted.",
        },
        "multicast-announcement": {
            "type": "option",
            "help": "Enable/disable multicast announcements.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "announcement-count": {
            "type": "integer",
            "help": "Number of multicast announcements.",
            "default": 3,
            "min_value": 3,
            "max_value": 10,
        },
        "intl-intf": {
            "type": "string",
            "help": "Internal interface name.",
            "required": True,
        },
        "recycle-delay": {
            "type": "integer",
            "help": "Minimum delay (in seconds) the PCP Server will wait before recycling mappings that have expired (0 - 3600, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 3600,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_pcp_server_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/pcp_server."""
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


def validate_system_pcp_server_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/pcp_server object."""
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

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_pcp_server_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/pcp_server."""
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
    "endpoint": "system/pcp_server",
    "category": "cmdb",
    "api_path": "system/pcp-server",
    "help": "Configure PCP server information.",
    "total_fields": 2,
    "required_fields_count": 0,
    "fields_with_defaults_count": 1,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
