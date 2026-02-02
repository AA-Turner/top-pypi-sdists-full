"""Validation helpers for firewall/on_demand_sniffer - Auto-generated"""

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
    "interface",  # Interface name that on-demand packet sniffer will take place.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "interface": "",
    "max-packet-count": 0,
    "non-ip-packet": "disable",
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
    "name": "string",  # On-demand packet sniffer name.
    "interface": "string",  # Interface name that on-demand packet sniffer will take place
    "max-packet-count": "integer",  # Maximum number of packets to capture per on-demand packet sn
    "hosts": "string",  # IPv4 or IPv6 hosts to filter in this traffic sniffer.
    "ports": "string",  # Ports to filter for in this traffic sniffer.
    "protocols": "string",  # Protocols to filter in this traffic sniffer.
    "non-ip-packet": "option",  # Include non-IP packets.
    "advanced-filter": "var-string",  # Advanced freeform filter that will be used over existing fil
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "On-demand packet sniffer name.",
    "interface": "Interface name that on-demand packet sniffer will take place.",
    "max-packet-count": "Maximum number of packets to capture per on-demand packet sniffer.",
    "hosts": "IPv4 or IPv6 hosts to filter in this traffic sniffer.",
    "ports": "Ports to filter for in this traffic sniffer.",
    "protocols": "Protocols to filter in this traffic sniffer.",
    "non-ip-packet": "Include non-IP packets.",
    "advanced-filter": "Advanced freeform filter that will be used over existing filter settings if set. Can only be used by super admin.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 35},
    "max-packet-count": {"type": "integer", "min": 1, "max": 20000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "hosts": {
        "host": {
            "type": "string",
            "help": "IPv4 or IPv6 host.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
    },
    "ports": {
        "port": {
            "type": "integer",
            "help": "Port to filter in this traffic sniffer.",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 65536,
        },
    },
    "protocols": {
        "protocol": {
            "type": "integer",
            "help": "Integer value for the protocol type as defined by IANA (0 - 255).",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_NON_IP_PACKET = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_on_demand_sniffer_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/on_demand_sniffer."""
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


def validate_firewall_on_demand_sniffer_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/on_demand_sniffer object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "non-ip-packet" in payload:
        is_valid, error = _validate_enum_field(
            "non-ip-packet",
            payload["non-ip-packet"],
            VALID_BODY_NON_IP_PACKET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_on_demand_sniffer_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/on_demand_sniffer."""
    # Validate enum values using central function
    if "non-ip-packet" in payload:
        is_valid, error = _validate_enum_field(
            "non-ip-packet",
            payload["non-ip-packet"],
            VALID_BODY_NON_IP_PACKET,
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
    "endpoint": "firewall/on_demand_sniffer",
    "category": "cmdb",
    "api_path": "firewall/on-demand-sniffer",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure on-demand packet sniffer.",
    "total_fields": 8,
    "required_fields_count": 1,
    "fields_with_defaults_count": 4,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
