"""Validation helpers for wireless_controller/wag_profile - Auto-generated"""

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
    "tunnel-type": "l2tpv3",
    "wag-ip": "0.0.0.0",
    "wag-port": 1701,
    "ping-interval": 1,
    "ping-number": 5,
    "return-packet-timeout": 160,
    "dhcp-ip-addr": "0.0.0.0",
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
    "name": "string",  # Tunnel profile name.
    "comment": "var-string",  # Comment.
    "tunnel-type": "option",  # Tunnel type.
    "wag-ip": "ipv4-address",  # IP Address of the wireless access gateway.
    "wag-port": "integer",  # UDP port of the wireless access gateway.
    "ping-interval": "integer",  # Interval between two tunnel monitoring echo packets (1 - 655
    "ping-number": "integer",  # Number of the tunnel monitoring echo packets (1 - 65535, def
    "return-packet-timeout": "integer",  # Window of time for the return packets from the tunnel's remo
    "dhcp-ip-addr": "ipv4-address",  # IP address of the monitoring DHCP request packet sent throug
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Tunnel profile name.",
    "comment": "Comment.",
    "tunnel-type": "Tunnel type.",
    "wag-ip": "IP Address of the wireless access gateway.",
    "wag-port": "UDP port of the wireless access gateway.",
    "ping-interval": "Interval between two tunnel monitoring echo packets (1 - 65535 sec, default = 1).",
    "ping-number": "Number of the tunnel monitoring echo packets (1 - 65535, default = 5).",
    "return-packet-timeout": "Window of time for the return packets from the tunnel's remote end (1 - 65535 sec, default = 160).",
    "dhcp-ip-addr": "IP address of the monitoring DHCP request packet sent through the tunnel.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "wag-port": {"type": "integer", "min": 0, "max": 65535},
    "ping-interval": {"type": "integer", "min": 1, "max": 65535},
    "ping-number": {"type": "integer", "min": 1, "max": 65535},
    "return-packet-timeout": {"type": "integer", "min": 1, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_TUNNEL_TYPE = [
    "l2tpv3",
    "gre",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_wag_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/wag_profile."""
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


def validate_wireless_controller_wag_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/wag_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "tunnel-type" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-type",
            payload["tunnel-type"],
            VALID_BODY_TUNNEL_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_wag_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/wag_profile."""
    # Validate enum values using central function
    if "tunnel-type" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-type",
            payload["tunnel-type"],
            VALID_BODY_TUNNEL_TYPE,
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
    "endpoint": "wireless_controller/wag_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/wag-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure wireless access gateway (WAG) profiles used for tunnels on AP.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 8,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
