"""Validation helpers for router/ripng - Auto-generated"""

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
    "default-information-originate": "disable",
    "default-metric": 1,
    "max-out-metric": 0,
    "update-timer": 30,
    "timeout-timer": 180,
    "garbage-timer": 120,
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
    "default-information-originate": "option",  # Enable/disable generation of default route.
    "default-metric": "integer",  # Default metric.
    "max-out-metric": "integer",  # Maximum metric allowed to output(0 means 'not set').
    "distance": "string",  # Distance.
    "distribute-list": "string",  # Distribute list.
    "neighbor": "string",  # Neighbor.
    "network": "string",  # Network.
    "aggregate-address": "string",  # Aggregate address.
    "offset-list": "string",  # Offset list.
    "passive-interface": "string",  # Passive interface configuration.
    "redistribute": "string",  # Redistribute configuration.
    "update-timer": "integer",  # Update timer in seconds.
    "timeout-timer": "integer",  # Timeout timer in seconds.
    "garbage-timer": "integer",  # Garbage timer in seconds.
    "interface": "string",  # RIPng interface configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "default-information-originate": "Enable/disable generation of default route.",
    "default-metric": "Default metric.",
    "max-out-metric": "Maximum metric allowed to output(0 means 'not set').",
    "distance": "Distance.",
    "distribute-list": "Distribute list.",
    "neighbor": "Neighbor.",
    "network": "Network.",
    "aggregate-address": "Aggregate address.",
    "offset-list": "Offset list.",
    "passive-interface": "Passive interface configuration.",
    "redistribute": "Redistribute configuration.",
    "update-timer": "Update timer in seconds.",
    "timeout-timer": "Timeout timer in seconds.",
    "garbage-timer": "Garbage timer in seconds.",
    "interface": "RIPng interface configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "default-metric": {"type": "integer", "min": 1, "max": 16},
    "max-out-metric": {"type": "integer", "min": 0, "max": 15},
    "update-timer": {"type": "integer", "min": 5, "max": 2147483647},
    "timeout-timer": {"type": "integer", "min": 5, "max": 2147483647},
    "garbage-timer": {"type": "integer", "min": 5, "max": 2147483647},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "distance": {
        "id": {
            "type": "integer",
            "help": "Distance ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "distance": {
            "type": "integer",
            "help": "Distance (1 - 255).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 255,
        },
        "prefix6": {
            "type": "ipv6-prefix",
            "help": "Distance prefix6.",
            "default": "::/0",
        },
        "access-list6": {
            "type": "string",
            "help": "Access list for route destination.",
            "default": "",
            "max_length": 35,
        },
    },
    "distribute-list": {
        "id": {
            "type": "integer",
            "help": "Distribute list ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "direction": {
            "type": "option",
            "help": "Distribute list direction.",
            "required": True,
            "default": "out",
            "options": ["in", "out"],
        },
        "listname": {
            "type": "string",
            "help": "Distribute access/prefix list name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "interface": {
            "type": "string",
            "help": "Distribute list interface name.",
            "default": "",
            "max_length": 15,
        },
    },
    "neighbor": {
        "id": {
            "type": "integer",
            "help": "Neighbor entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip6": {
            "type": "ipv6-address",
            "help": "IPv6 link-local address.",
            "required": True,
            "default": "::",
        },
        "interface": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
    },
    "network": {
        "id": {
            "type": "integer",
            "help": "Network entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "prefix": {
            "type": "ipv6-prefix",
            "help": "Network IPv6 link-local prefix.",
            "default": "::/0",
        },
    },
    "aggregate-address": {
        "id": {
            "type": "integer",
            "help": "Aggregate address entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "prefix6": {
            "type": "ipv6-prefix",
            "help": "Aggregate address prefix.",
            "default": "::/0",
        },
    },
    "offset-list": {
        "id": {
            "type": "integer",
            "help": "Offset-list ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "direction": {
            "type": "option",
            "help": "Offset list direction.",
            "required": True,
            "default": "out",
            "options": ["in", "out"],
        },
        "access-list6": {
            "type": "string",
            "help": "IPv6 access list name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "offset": {
            "type": "integer",
            "help": "Offset.",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 16,
        },
        "interface": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 15,
        },
    },
    "passive-interface": {
        "name": {
            "type": "string",
            "help": "Passive interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "redistribute": {
        "name": {
            "type": "string",
            "help": "Redistribute name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "metric": {
            "type": "integer",
            "help": "Redistribute metric setting.",
            "default": 0,
            "min_value": 1,
            "max_value": 16,
        },
        "routemap": {
            "type": "string",
            "help": "Route map name.",
            "default": "",
            "max_length": 35,
        },
    },
    "interface": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 35,
        },
        "split-horizon-status": {
            "type": "option",
            "help": "Enable/disable split horizon.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "split-horizon": {
            "type": "option",
            "help": "Enable/disable split horizon.",
            "default": "poisoned",
            "options": ["poisoned", "regular"],
        },
        "flags": {
            "type": "integer",
            "help": "Flags.",
            "default": 8,
            "min_value": 0,
            "max_value": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_DEFAULT_INFORMATION_ORIGINATE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_router_ripng_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/ripng."""
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


def validate_router_ripng_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/ripng object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "default-information-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-originate",
            payload["default-information-originate"],
            VALID_BODY_DEFAULT_INFORMATION_ORIGINATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_router_ripng_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/ripng."""
    # Validate enum values using central function
    if "default-information-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-originate",
            payload["default-information-originate"],
            VALID_BODY_DEFAULT_INFORMATION_ORIGINATE,
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
    "endpoint": "router/ripng",
    "category": "cmdb",
    "api_path": "router/ripng",
    "help": "Configure RIPng.",
    "total_fields": 15,
    "required_fields_count": 0,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
