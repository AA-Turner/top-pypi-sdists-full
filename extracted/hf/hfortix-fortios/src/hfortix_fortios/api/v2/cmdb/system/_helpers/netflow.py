"""Validation helpers for system/netflow - Auto-generated"""

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
    "active-flow-timeout": 1800,
    "inactive-flow-timeout": 15,
    "template-tx-timeout": 1800,
    "template-tx-counter": 20,
    "session-cache-size": "default",
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
    "active-flow-timeout": "integer",  # Timeout to report active flows (60 - 3600 sec, default = 1800).
    "inactive-flow-timeout": "integer",  # Timeout for periodic report of finished flows (10 - 600 sec, default = 15).
    "template-tx-timeout": "integer",  # Timeout for periodic template flowset transmission (60 - 86400 sec, default = 18
    "template-tx-counter": "integer",  # Counter of flowset records before resending a template flowset record.
    "session-cache-size": "option",  # Maximum RAM usage allowed for Netflow session cache.
    "exclusion-filters": "string",  # Exclusion filters
    "collectors": "string",  # Netflow collectors.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "active-flow-timeout": "Timeout to report active flows (60 - 3600 sec, default = 1800).",
    "inactive-flow-timeout": "Timeout for periodic report of finished flows (10 - 600 sec, default = 15).",
    "template-tx-timeout": "Timeout for periodic template flowset transmission (60 - 86400 sec, default = 1800).",
    "template-tx-counter": "Counter of flowset records before resending a template flowset record.",
    "session-cache-size": "Maximum RAM usage allowed for Netflow session cache.",
    "exclusion-filters": "Exclusion filters",
    "collectors": "Netflow collectors.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "active-flow-timeout": {"type": "integer", "min": 60, "max": 3600},
    "inactive-flow-timeout": {"type": "integer", "min": 10, "max": 600},
    "template-tx-timeout": {"type": "integer", "min": 60, "max": 86400},
    "template-tx-counter": {"type": "integer", "min": 10, "max": 6000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "exclusion-filters": {
        "id": {
            "type": "integer",
            "help": "Filter ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "source-ip": {
            "type": "user",
            "help": "Session source address.",
            "default": "",
        },
        "destination-ip": {
            "type": "user",
            "help": "Session destination address.",
            "default": "",
        },
        "source-port": {
            "type": "user",
            "help": "Session source port number or range.",
            "default": "",
        },
        "destination-port": {
            "type": "user",
            "help": "Session destination port number or range.",
            "default": "",
        },
        "protocol": {
            "type": "integer",
            "help": "Session IP protocol (0 - 255, default = 255, meaning any).",
            "default": 255,
            "min_value": 0,
            "max_value": 255,
        },
    },
    "collectors": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 6,
        },
        "collector-ip": {
            "type": "string",
            "help": "Collector IP.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "collector-port": {
            "type": "integer",
            "help": "NetFlow collector port number.",
            "default": 2055,
            "min_value": 0,
            "max_value": 65535,
        },
        "source-ip": {
            "type": "string",
            "help": "Source IP address for communication with the NetFlow agent.",
            "default": "",
            "max_length": 63,
        },
        "source-ip-interface": {
            "type": "string",
            "help": "Name of the interface used to determine the source IP for exporting packets.",
            "default": "",
            "max_length": 15,
        },
        "interface-select-method": {
            "type": "option",
            "help": "Specify how to select outgoing interface to reach server.",
            "default": "auto",
            "options": ["auto", "sdwan", "specify"],
        },
        "interface": {
            "type": "string",
            "help": "Specify outgoing interface to reach server.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "vrf-select": {
            "type": "integer",
            "help": "VRF ID used for connection to server.",
            "default": 0,
            "min_value": 0,
            "max_value": 511,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SESSION_CACHE_SIZE = [
    "min",
    "default",
    "max",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_netflow_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/netflow."""
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


def validate_system_netflow_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/netflow object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "session-cache-size" in payload:
        is_valid, error = _validate_enum_field(
            "session-cache-size",
            payload["session-cache-size"],
            VALID_BODY_SESSION_CACHE_SIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_netflow_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/netflow."""
    # Validate enum values using central function
    if "session-cache-size" in payload:
        is_valid, error = _validate_enum_field(
            "session-cache-size",
            payload["session-cache-size"],
            VALID_BODY_SESSION_CACHE_SIZE,
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
    "endpoint": "system/netflow",
    "category": "cmdb",
    "api_path": "system/netflow",
    "help": "Configure NetFlow.",
    "total_fields": 7,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
