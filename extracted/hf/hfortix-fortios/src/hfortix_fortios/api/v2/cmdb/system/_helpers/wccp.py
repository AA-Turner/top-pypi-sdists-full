"""Validation helpers for system/wccp - Auto-generated"""

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
    "service-id": "",
    "router-id": "0.0.0.0",
    "cache-id": "0.0.0.0",
    "group-address": "0.0.0.0",
    "server-list": "",
    "router-list": "",
    "ports-defined": "",
    "server-type": "forward",
    "ports": "",
    "authentication": "disable",
    "forward-method": "GRE",
    "cache-engine-method": "GRE",
    "service-type": "auto",
    "primary-hash": "dst-ip",
    "priority": 0,
    "protocol": 0,
    "assignment-weight": 0,
    "assignment-bucket-format": "cisco-implementation",
    "return-method": "GRE",
    "assignment-method": "HASH",
    "assignment-srcaddr-mask": "0.0.23.65",
    "assignment-dstaddr-mask": "0.0.0.0",
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
    "service-id": "string",  # Service ID.
    "router-id": "ipv4-address",  # IP address known to all cache engines. If all cache engines connect to the same 
    "cache-id": "ipv4-address",  # IP address known to all routers. If the addresses are the same, use the default 
    "group-address": "ipv4-address-multicast",  # IP multicast address used by the cache routers. For the FortiGate to ignore mult
    "server-list": "user",  # IP addresses and netmasks for up to four cache servers.
    "router-list": "user",  # IP addresses of one or more WCCP routers.
    "ports-defined": "option",  # Match method.
    "server-type": "option",  # Cache server type.
    "ports": "user",  # Service ports.
    "authentication": "option",  # Enable/disable MD5 authentication.
    "password": "password",  # Password for MD5 authentication.
    "forward-method": "option",  # Method used to forward traffic to the cache servers.
    "cache-engine-method": "option",  # Method used to forward traffic to the routers or to return to the cache engine.
    "service-type": "option",  # WCCP service type used by the cache server for logical interception and redirect
    "primary-hash": "option",  # Hash method.
    "priority": "integer",  # Service priority.
    "protocol": "integer",  # Service protocol.
    "assignment-weight": "integer",  # Assignment of hash weight/ratio for the WCCP cache engine.
    "assignment-bucket-format": "option",  # Assignment bucket format for the WCCP cache engine.
    "return-method": "option",  # Method used to decline a redirected packet and return it to the FortiGate unit.
    "assignment-method": "option",  # Hash key assignment preference.
    "assignment-srcaddr-mask": "ipv4-netmask-any",  # Assignment source address mask.
    "assignment-dstaddr-mask": "ipv4-netmask-any",  # Assignment destination address mask.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "service-id": "Service ID.",
    "router-id": "IP address known to all cache engines. If all cache engines connect to the same FortiGate interface, use the default 0.0.0.0.",
    "cache-id": "IP address known to all routers. If the addresses are the same, use the default 0.0.0.0.",
    "group-address": "IP multicast address used by the cache routers. For the FortiGate to ignore multicast WCCP traffic, use the default 0.0.0.0.",
    "server-list": "IP addresses and netmasks for up to four cache servers.",
    "router-list": "IP addresses of one or more WCCP routers.",
    "ports-defined": "Match method.",
    "server-type": "Cache server type.",
    "ports": "Service ports.",
    "authentication": "Enable/disable MD5 authentication.",
    "password": "Password for MD5 authentication.",
    "forward-method": "Method used to forward traffic to the cache servers.",
    "cache-engine-method": "Method used to forward traffic to the routers or to return to the cache engine.",
    "service-type": "WCCP service type used by the cache server for logical interception and redirection of traffic.",
    "primary-hash": "Hash method.",
    "priority": "Service priority.",
    "protocol": "Service protocol.",
    "assignment-weight": "Assignment of hash weight/ratio for the WCCP cache engine.",
    "assignment-bucket-format": "Assignment bucket format for the WCCP cache engine.",
    "return-method": "Method used to decline a redirected packet and return it to the FortiGate unit.",
    "assignment-method": "Hash key assignment preference.",
    "assignment-srcaddr-mask": "Assignment source address mask.",
    "assignment-dstaddr-mask": "Assignment destination address mask.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "service-id": {"type": "string", "max_length": 3},
    "priority": {"type": "integer", "min": 0, "max": 255},
    "protocol": {"type": "integer", "min": 0, "max": 255},
    "assignment-weight": {"type": "integer", "min": 0, "max": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_PORTS_DEFINED = [
    "source",
    "destination",
]
VALID_BODY_SERVER_TYPE = [
    "forward",
    "proxy",
]
VALID_BODY_AUTHENTICATION = [
    "enable",
    "disable",
]
VALID_BODY_FORWARD_METHOD = [
    "GRE",
    "L2",
    "any",
]
VALID_BODY_CACHE_ENGINE_METHOD = [
    "GRE",
    "L2",
]
VALID_BODY_SERVICE_TYPE = [
    "auto",
    "standard",
    "dynamic",
]
VALID_BODY_PRIMARY_HASH = [
    "src-ip",
    "dst-ip",
    "src-port",
    "dst-port",
]
VALID_BODY_ASSIGNMENT_BUCKET_FORMAT = [
    "wccp-v2",
    "cisco-implementation",
]
VALID_BODY_RETURN_METHOD = [
    "GRE",
    "L2",
    "any",
]
VALID_BODY_ASSIGNMENT_METHOD = [
    "HASH",
    "MASK",
    "any",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_wccp_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/wccp."""
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


def validate_system_wccp_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/wccp object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ports-defined" in payload:
        is_valid, error = _validate_enum_field(
            "ports-defined",
            payload["ports-defined"],
            VALID_BODY_PORTS_DEFINED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forward-method" in payload:
        is_valid, error = _validate_enum_field(
            "forward-method",
            payload["forward-method"],
            VALID_BODY_FORWARD_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-engine-method" in payload:
        is_valid, error = _validate_enum_field(
            "cache-engine-method",
            payload["cache-engine-method"],
            VALID_BODY_CACHE_ENGINE_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-type" in payload:
        is_valid, error = _validate_enum_field(
            "service-type",
            payload["service-type"],
            VALID_BODY_SERVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "primary-hash" in payload:
        is_valid, error = _validate_enum_field(
            "primary-hash",
            payload["primary-hash"],
            VALID_BODY_PRIMARY_HASH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assignment-bucket-format" in payload:
        is_valid, error = _validate_enum_field(
            "assignment-bucket-format",
            payload["assignment-bucket-format"],
            VALID_BODY_ASSIGNMENT_BUCKET_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "return-method" in payload:
        is_valid, error = _validate_enum_field(
            "return-method",
            payload["return-method"],
            VALID_BODY_RETURN_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assignment-method" in payload:
        is_valid, error = _validate_enum_field(
            "assignment-method",
            payload["assignment-method"],
            VALID_BODY_ASSIGNMENT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_wccp_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/wccp."""
    # Validate enum values using central function
    if "ports-defined" in payload:
        is_valid, error = _validate_enum_field(
            "ports-defined",
            payload["ports-defined"],
            VALID_BODY_PORTS_DEFINED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forward-method" in payload:
        is_valid, error = _validate_enum_field(
            "forward-method",
            payload["forward-method"],
            VALID_BODY_FORWARD_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-engine-method" in payload:
        is_valid, error = _validate_enum_field(
            "cache-engine-method",
            payload["cache-engine-method"],
            VALID_BODY_CACHE_ENGINE_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-type" in payload:
        is_valid, error = _validate_enum_field(
            "service-type",
            payload["service-type"],
            VALID_BODY_SERVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "primary-hash" in payload:
        is_valid, error = _validate_enum_field(
            "primary-hash",
            payload["primary-hash"],
            VALID_BODY_PRIMARY_HASH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assignment-bucket-format" in payload:
        is_valid, error = _validate_enum_field(
            "assignment-bucket-format",
            payload["assignment-bucket-format"],
            VALID_BODY_ASSIGNMENT_BUCKET_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "return-method" in payload:
        is_valid, error = _validate_enum_field(
            "return-method",
            payload["return-method"],
            VALID_BODY_RETURN_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assignment-method" in payload:
        is_valid, error = _validate_enum_field(
            "assignment-method",
            payload["assignment-method"],
            VALID_BODY_ASSIGNMENT_METHOD,
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
    "endpoint": "system/wccp",
    "category": "cmdb",
    "api_path": "system/wccp",
    "mkey": "service-id",
    "mkey_type": "string",
    "help": "Configure WCCP.",
    "total_fields": 23,
    "required_fields_count": 0,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
