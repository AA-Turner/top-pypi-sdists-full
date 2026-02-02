"""Validation helpers for web_proxy/forward_server_group - Auto-generated"""

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
    "affinity": "enable",
    "ldb-method": "weighted",
    "group-down-option": "block",
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
    "name": "string",  # Configure a forward server group consisting one or multiple 
    "affinity": "option",  # Enable/disable affinity, attaching a source-ip's traffic to 
    "ldb-method": "option",  # Load balance method: weighted or least-session.
    "group-down-option": "option",  # Action to take when all of the servers in the forward server
    "server-list": "string",  # Add web forward servers to a list to form a server group. Op
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Configure a forward server group consisting one or multiple forward servers. Supports failover and load balancing.",
    "affinity": "Enable/disable affinity, attaching a source-ip's traffic to the assigned forwarding server until the forward-server-affinity-timeout is reached (under web-proxy global).",
    "ldb-method": "Load balance method: weighted or least-session.",
    "group-down-option": "Action to take when all of the servers in the forward server group are down: block sessions until at least one server is back up or pass sessions to their destination.",
    "server-list": "Add web forward servers to a list to form a server group. Optionally assign weights to each server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "server-list": {
        "name": {
            "type": "string",
            "help": "Forward server name.",
            "default": "",
            "max_length": 63,
        },
        "weight": {
            "type": "integer",
            "help": "Optionally assign a weight of the forwarding server for weighted load balancing (1 - 100, default = 10).",
            "default": 10,
            "min_value": 1,
            "max_value": 100,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_AFFINITY = [
    "enable",
    "disable",
]
VALID_BODY_LDB_METHOD = [
    "weighted",
    "least-session",
    "active-passive",
]
VALID_BODY_GROUP_DOWN_OPTION = [
    "block",
    "pass",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_web_proxy_forward_server_group_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for web_proxy/forward_server_group."""
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


def validate_web_proxy_forward_server_group_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new web_proxy/forward_server_group object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "affinity" in payload:
        is_valid, error = _validate_enum_field(
            "affinity",
            payload["affinity"],
            VALID_BODY_AFFINITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldb-method" in payload:
        is_valid, error = _validate_enum_field(
            "ldb-method",
            payload["ldb-method"],
            VALID_BODY_LDB_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-down-option" in payload:
        is_valid, error = _validate_enum_field(
            "group-down-option",
            payload["group-down-option"],
            VALID_BODY_GROUP_DOWN_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_web_proxy_forward_server_group_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update web_proxy/forward_server_group."""
    # Validate enum values using central function
    if "affinity" in payload:
        is_valid, error = _validate_enum_field(
            "affinity",
            payload["affinity"],
            VALID_BODY_AFFINITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldb-method" in payload:
        is_valid, error = _validate_enum_field(
            "ldb-method",
            payload["ldb-method"],
            VALID_BODY_LDB_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-down-option" in payload:
        is_valid, error = _validate_enum_field(
            "group-down-option",
            payload["group-down-option"],
            VALID_BODY_GROUP_DOWN_OPTION,
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
    "endpoint": "web_proxy/forward_server_group",
    "category": "cmdb",
    "api_path": "web-proxy/forward-server-group",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure a forward server group consisting or multiple forward servers. Supports failover and load balancing.",
    "total_fields": 5,
    "required_fields_count": 0,
    "fields_with_defaults_count": 4,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
