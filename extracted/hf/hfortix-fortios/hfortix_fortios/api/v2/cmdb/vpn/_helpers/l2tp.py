"""Validation helpers for vpn/l2tp - Auto-generated"""

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
    "usrgrp",  # User group.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "eip": "0.0.0.0",
    "sip": "0.0.0.0",
    "usrgrp": "",
    "enforce-ipsec": "disable",
    "lcp-echo-interval": 5,
    "lcp-max-echo-fails": 3,
    "hello-interval": 60,
    "compress": "disable",
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
    "status": "option",  # Enable/disable FortiGate as a L2TP gateway.
    "eip": "ipv4-address",  # End IP.
    "sip": "ipv4-address",  # Start IP.
    "usrgrp": "string",  # User group.
    "enforce-ipsec": "option",  # Enable/disable IPsec enforcement.
    "lcp-echo-interval": "integer",  # Time in seconds between PPPoE Link Control Protocol (LCP) ec
    "lcp-max-echo-fails": "integer",  # Maximum number of missed LCP echo messages before disconnect
    "hello-interval": "integer",  # L2TP hello message interval in seconds (0 - 3600 sec, defaul
    "compress": "option",  # Enable/disable data compression.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable FortiGate as a L2TP gateway.",
    "eip": "End IP.",
    "sip": "Start IP.",
    "usrgrp": "User group.",
    "enforce-ipsec": "Enable/disable IPsec enforcement.",
    "lcp-echo-interval": "Time in seconds between PPPoE Link Control Protocol (LCP) echo requests.",
    "lcp-max-echo-fails": "Maximum number of missed LCP echo messages before disconnect.",
    "hello-interval": "L2TP hello message interval in seconds (0 - 3600 sec, default = 60).",
    "compress": "Enable/disable data compression.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "usrgrp": {"type": "string", "max_length": 35},
    "lcp-echo-interval": {"type": "integer", "min": 0, "max": 32767},
    "lcp-max-echo-fails": {"type": "integer", "min": 0, "max": 32767},
    "hello-interval": {"type": "integer", "min": 0, "max": 3600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_ENFORCE_IPSEC = [
    "enable",
    "disable",
]
VALID_BODY_COMPRESS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_vpn_l2tp_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/l2tp."""
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


def validate_vpn_l2tp_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/l2tp object."""
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
    if "enforce-ipsec" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-ipsec",
            payload["enforce-ipsec"],
            VALID_BODY_ENFORCE_IPSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "compress" in payload:
        is_valid, error = _validate_enum_field(
            "compress",
            payload["compress"],
            VALID_BODY_COMPRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_vpn_l2tp_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/l2tp."""
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
    if "enforce-ipsec" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-ipsec",
            payload["enforce-ipsec"],
            VALID_BODY_ENFORCE_IPSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "compress" in payload:
        is_valid, error = _validate_enum_field(
            "compress",
            payload["compress"],
            VALID_BODY_COMPRESS,
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
    "endpoint": "vpn/l2tp",
    "category": "cmdb",
    "api_path": "vpn/l2tp",
    "help": "Configure L2TP.",
    "total_fields": 9,
    "required_fields_count": 1,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
