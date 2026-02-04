"""Validation helpers for router/policy - Auto-generated"""

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
    "seq-num": 0,
    "input-device-negate": "disable",
    "src-negate": "disable",
    "dst-negate": "disable",
    "action": "permit",
    "protocol": 0,
    "start-port": 0,
    "end-port": 65535,
    "start-source-port": 0,
    "end-source-port": 65535,
    "gateway": "0.0.0.0",
    "output-device": "",
    "tos": "",
    "tos-mask": "",
    "status": "enable",
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
    "seq-num": "integer",  # Sequence number(1-65535).
    "input-device": "string",  # Incoming interface name.
    "input-device-negate": "option",  # Enable/disable negation of input device match.
    "src": "string",  # Source IP and mask (x.x.x.x/x).
    "srcaddr": "string",  # Source address name.
    "src-negate": "option",  # Enable/disable negating source address match.
    "dst": "string",  # Destination IP and mask (x.x.x.x/x).
    "dstaddr": "string",  # Destination address name.
    "dst-negate": "option",  # Enable/disable negating destination address match.
    "action": "option",  # Action of the policy route.
    "protocol": "integer",  # Protocol number (0 - 255).
    "start-port": "integer",  # Start destination port number (0 - 65535).
    "end-port": "integer",  # End destination port number (0 - 65535).
    "start-source-port": "integer",  # Start source port number (0 - 65535).
    "end-source-port": "integer",  # End source port number (0 - 65535).
    "gateway": "ipv4-address",  # IP address of the gateway.
    "output-device": "string",  # Outgoing interface name.
    "tos": "user",  # Type of service bit pattern.
    "tos-mask": "user",  # Type of service evaluated bits.
    "status": "option",  # Enable/disable this policy route.
    "comments": "var-string",  # Optional comments.
    "internet-service-id": "string",  # Destination Internet Service ID.
    "internet-service-custom": "string",  # Custom Destination Internet Service name.
    "internet-service-fortiguard": "string",  # FortiGuard Destination Internet Service name.
    "users": "string",  # List of users.
    "groups": "string",  # List of user groups.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "seq-num": "Sequence number(1-65535).",
    "input-device": "Incoming interface name.",
    "input-device-negate": "Enable/disable negation of input device match.",
    "src": "Source IP and mask (x.x.x.x/x).",
    "srcaddr": "Source address name.",
    "src-negate": "Enable/disable negating source address match.",
    "dst": "Destination IP and mask (x.x.x.x/x).",
    "dstaddr": "Destination address name.",
    "dst-negate": "Enable/disable negating destination address match.",
    "action": "Action of the policy route.",
    "protocol": "Protocol number (0 - 255).",
    "start-port": "Start destination port number (0 - 65535).",
    "end-port": "End destination port number (0 - 65535).",
    "start-source-port": "Start source port number (0 - 65535).",
    "end-source-port": "End source port number (0 - 65535).",
    "gateway": "IP address of the gateway.",
    "output-device": "Outgoing interface name.",
    "tos": "Type of service bit pattern.",
    "tos-mask": "Type of service evaluated bits.",
    "status": "Enable/disable this policy route.",
    "comments": "Optional comments.",
    "internet-service-id": "Destination Internet Service ID.",
    "internet-service-custom": "Custom Destination Internet Service name.",
    "internet-service-fortiguard": "FortiGuard Destination Internet Service name.",
    "users": "List of users.",
    "groups": "List of user groups.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "seq-num": {"type": "integer", "min": 1, "max": 65535},
    "protocol": {"type": "integer", "min": 0, "max": 255},
    "start-port": {"type": "integer", "min": 0, "max": 65535},
    "end-port": {"type": "integer", "min": 0, "max": 65535},
    "start-source-port": {"type": "integer", "min": 0, "max": 65535},
    "end-source-port": {"type": "integer", "min": 0, "max": 65535},
    "output-device": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "input-device": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "src": {
        "subnet": {
            "type": "string",
            "help": "IP and mask.",
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr": {
        "name": {
            "type": "string",
            "help": "Address/group name.",
            "default": "",
            "max_length": 79,
        },
    },
    "dst": {
        "subnet": {
            "type": "string",
            "help": "IP and mask.",
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr": {
        "name": {
            "type": "string",
            "help": "Address/group name.",
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-id": {
        "id": {
            "type": "integer",
            "help": "Destination Internet Service ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "internet-service-custom": {
        "name": {
            "type": "string",
            "help": "Custom Destination Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Destination Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "users": {
        "name": {
            "type": "string",
            "help": "User name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "groups": {
        "name": {
            "type": "string",
            "help": "Group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_INPUT_DEVICE_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_SRC_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_DST_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_ACTION = [
    "deny",
    "permit",
]
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_router_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/policy."""
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


def validate_router_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "input-device-negate" in payload:
        is_valid, error = _validate_enum_field(
            "input-device-negate",
            payload["input-device-negate"],
            VALID_BODY_INPUT_DEVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "src-negate",
            payload["src-negate"],
            VALID_BODY_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dst-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dst-negate",
            payload["dst-negate"],
            VALID_BODY_DST_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
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


def validate_router_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/policy."""
    # Validate enum values using central function
    if "input-device-negate" in payload:
        is_valid, error = _validate_enum_field(
            "input-device-negate",
            payload["input-device-negate"],
            VALID_BODY_INPUT_DEVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "src-negate",
            payload["src-negate"],
            VALID_BODY_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dst-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dst-negate",
            payload["dst-negate"],
            VALID_BODY_DST_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
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
    "endpoint": "router/policy",
    "category": "cmdb",
    "api_path": "router/policy",
    "mkey": "seq-num",
    "mkey_type": "integer",
    "help": "Configure IPv4 routing policies.",
    "total_fields": 26,
    "required_fields_count": 0,
    "fields_with_defaults_count": 15,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
