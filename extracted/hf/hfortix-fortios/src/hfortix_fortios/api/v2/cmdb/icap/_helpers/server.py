"""Validation helpers for icap/server - Auto-generated"""

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
    "healthcheck-service",  # ICAP Service name to use for health checks.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "addr-type": "ip4",
    "ip-address": "0.0.0.0",
    "ip6-address": "::",
    "fqdn": "",
    "port": 1344,
    "max-connections": 100,
    "secure": "disable",
    "ssl-cert": "",
    "healthcheck": "disable",
    "healthcheck-service": "",
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
    "name": "string",  # Server name.
    "addr-type": "option",  # Address type of the remote ICAP server: IPv4, IPv6 or FQDN.
    "ip-address": "ipv4-address-any",  # IPv4 address of the ICAP server.
    "ip6-address": "ipv6-address",  # IPv6 address of the ICAP server.
    "fqdn": "string",  # ICAP remote server Fully Qualified Domain Name (FQDN).
    "port": "integer",  # ICAP server port.
    "max-connections": "integer",  # Maximum number of concurrent connections to ICAP server (unlimited = 0, default 
    "secure": "option",  # Enable/disable secure connection to ICAP server.
    "ssl-cert": "string",  # CA certificate name.
    "healthcheck": "option",  # Enable/disable ICAP remote server health checking. Attempts to connect to the re
    "healthcheck-service": "string",  # ICAP Service name to use for health checks.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Server name.",
    "addr-type": "Address type of the remote ICAP server: IPv4, IPv6 or FQDN.",
    "ip-address": "IPv4 address of the ICAP server.",
    "ip6-address": "IPv6 address of the ICAP server.",
    "fqdn": "ICAP remote server Fully Qualified Domain Name (FQDN).",
    "port": "ICAP server port.",
    "max-connections": "Maximum number of concurrent connections to ICAP server (unlimited = 0, default = 100). Must not be less than wad-worker-count.",
    "secure": "Enable/disable secure connection to ICAP server.",
    "ssl-cert": "CA certificate name.",
    "healthcheck": "Enable/disable ICAP remote server health checking. Attempts to connect to the remote ICAP server to verify that the server is operating normally.",
    "healthcheck-service": "ICAP Service name to use for health checks.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "fqdn": {"type": "string", "max_length": 255},
    "port": {"type": "integer", "min": 1, "max": 65535},
    "max-connections": {"type": "integer", "min": 0, "max": 4294967295},
    "ssl-cert": {"type": "string", "max_length": 79},
    "healthcheck-service": {"type": "string", "max_length": 127},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_ADDR_TYPE = [
    "ip4",
    "ip6",
    "fqdn",
]
VALID_BODY_SECURE = [
    "disable",
    "enable",
]
VALID_BODY_HEALTHCHECK = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_icap_server_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for icap/server."""
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


def validate_icap_server_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new icap/server object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "addr-type",
            payload["addr-type"],
            VALID_BODY_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secure" in payload:
        is_valid, error = _validate_enum_field(
            "secure",
            payload["secure"],
            VALID_BODY_SECURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "healthcheck" in payload:
        is_valid, error = _validate_enum_field(
            "healthcheck",
            payload["healthcheck"],
            VALID_BODY_HEALTHCHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_icap_server_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update icap/server."""
    # Validate enum values using central function
    if "addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "addr-type",
            payload["addr-type"],
            VALID_BODY_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secure" in payload:
        is_valid, error = _validate_enum_field(
            "secure",
            payload["secure"],
            VALID_BODY_SECURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "healthcheck" in payload:
        is_valid, error = _validate_enum_field(
            "healthcheck",
            payload["healthcheck"],
            VALID_BODY_HEALTHCHECK,
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
    "endpoint": "icap/server",
    "category": "cmdb",
    "api_path": "icap/server",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure ICAP servers.",
    "total_fields": 11,
    "required_fields_count": 1,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
