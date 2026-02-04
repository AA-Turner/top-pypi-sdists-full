"""Validation helpers for wireless_controller/inter_controller - Auto-generated"""

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
    "inter-controller-mode": "disable",
    "l3-roaming": "disable",
    "inter-controller-pri": "primary",
    "fast-failover-max": 10,
    "fast-failover-wait": 10,
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
    "inter-controller-mode": "option",  # Configure inter-controller mode (disable, l2-roaming, 1+1, default = disable).
    "l3-roaming": "option",  # Enable/disable layer 3 roaming (default = disable).
    "inter-controller-key": "password",  # Secret key for inter-controller communications.
    "inter-controller-pri": "option",  # Configure inter-controller's priority (primary or secondary, default = primary).
    "fast-failover-max": "integer",  # Maximum number of retransmissions for fast failover HA messages between peer wir
    "fast-failover-wait": "integer",  # Minimum wait time before an AP transitions from secondary controller to primary 
    "inter-controller-peer": "string",  # Fast failover peer wireless controller list.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "inter-controller-mode": "Configure inter-controller mode (disable, l2-roaming, 1+1, default = disable).",
    "l3-roaming": "Enable/disable layer 3 roaming (default = disable).",
    "inter-controller-key": "Secret key for inter-controller communications.",
    "inter-controller-pri": "Configure inter-controller's priority (primary or secondary, default = primary).",
    "fast-failover-max": "Maximum number of retransmissions for fast failover HA messages between peer wireless controllers (3 - 64, default = 10).",
    "fast-failover-wait": "Minimum wait time before an AP transitions from secondary controller to primary controller (10 - 86400 sec, default = 10).",
    "inter-controller-peer": "Fast failover peer wireless controller list.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "fast-failover-max": {"type": "integer", "min": 3, "max": 64},
    "fast-failover-wait": {"type": "integer", "min": 10, "max": 86400},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "inter-controller-peer": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "peer-ip": {
            "type": "ipv4-address",
            "help": "Peer wireless controller's IP address.",
            "default": "0.0.0.0",
        },
        "peer-port": {
            "type": "integer",
            "help": "Port used by the wireless controller's for inter-controller communications (1024 - 49150, default = 5246).",
            "default": 5246,
            "min_value": 1024,
            "max_value": 49150,
        },
        "peer-priority": {
            "type": "option",
            "help": "Peer wireless controller's priority (primary or secondary, default = primary).",
            "default": "primary",
            "options": ["primary", "secondary"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_INTER_CONTROLLER_MODE = [
    "disable",
    "l2-roaming",
    "1+1",
]
VALID_BODY_L3_ROAMING = [
    "enable",
    "disable",
]
VALID_BODY_INTER_CONTROLLER_PRI = [
    "primary",
    "secondary",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_inter_controller_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/inter_controller."""
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


def validate_wireless_controller_inter_controller_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/inter_controller object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "inter-controller-mode" in payload:
        is_valid, error = _validate_enum_field(
            "inter-controller-mode",
            payload["inter-controller-mode"],
            VALID_BODY_INTER_CONTROLLER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l3-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "l3-roaming",
            payload["l3-roaming"],
            VALID_BODY_L3_ROAMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inter-controller-pri" in payload:
        is_valid, error = _validate_enum_field(
            "inter-controller-pri",
            payload["inter-controller-pri"],
            VALID_BODY_INTER_CONTROLLER_PRI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_inter_controller_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/inter_controller."""
    # Validate enum values using central function
    if "inter-controller-mode" in payload:
        is_valid, error = _validate_enum_field(
            "inter-controller-mode",
            payload["inter-controller-mode"],
            VALID_BODY_INTER_CONTROLLER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l3-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "l3-roaming",
            payload["l3-roaming"],
            VALID_BODY_L3_ROAMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inter-controller-pri" in payload:
        is_valid, error = _validate_enum_field(
            "inter-controller-pri",
            payload["inter-controller-pri"],
            VALID_BODY_INTER_CONTROLLER_PRI,
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
    "endpoint": "wireless_controller/inter_controller",
    "category": "cmdb",
    "api_path": "wireless-controller/inter-controller",
    "help": "Configure inter wireless controller operation.",
    "total_fields": 7,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
