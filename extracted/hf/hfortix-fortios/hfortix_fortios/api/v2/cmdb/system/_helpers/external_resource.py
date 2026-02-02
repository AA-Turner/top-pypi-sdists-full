"""Validation helpers for system/external_resource - Auto-generated"""

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
    "name",  # External resource name.
    "resource",  # URL of external resource.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "uuid": "00000000-0000-0000-0000-000000000000",
    "status": "enable",
    "type": "category",
    "namespace": "",
    "object-array-path": "$.addresses",
    "address-name-field": "$.name",
    "address-data-field": "$.value",
    "address-comment-field": "$.description",
    "update-method": "feed",
    "category": 0,
    "username": "",
    "client-cert-auth": "disable",
    "client-cert": "",
    "resource": "",
    "server-identity-check": "none",
    "refresh-rate": 5,
    "source-ip": "0.0.0.0",
    "source-ip-interface": "",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
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
    "name": "string",  # External resource name.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned 
    "status": "option",  # Enable/disable user resource.
    "type": "option",  # User resource type.
    "namespace": "string",  # Generic external connector address namespace.
    "object-array-path": "string",  # JSON Path to array of generic addresses in resource.
    "address-name-field": "string",  # JSON Path to address name in generic address entry.
    "address-data-field": "string",  # JSON Path to address data in generic address entry.
    "address-comment-field": "string",  # JSON Path to address description in generic address entry.
    "update-method": "option",  # External resource update method.
    "category": "integer",  # User resource category.
    "username": "string",  # HTTP basic authentication user name.
    "password": "varlen_password",  # HTTP basic authentication password.
    "client-cert-auth": "option",  # Enable/disable using client certificate for TLS authenticati
    "client-cert": "string",  # Client certificate name.
    "comments": "var-string",  # Comment.
    "resource": "string",  # URL of external resource.
    "user-agent": "var-string",  # HTTP User-Agent header (default = 'curl/7.58.0').
    "server-identity-check": "option",  # Certificate verification option.
    "refresh-rate": "integer",  # Time interval to refresh external resource (1 - 43200 min, d
    "source-ip": "ipv4-address",  # Source IPv4 address used to communicate with server.
    "source-ip-interface": "string",  # IPv4 Source interface for communication with the server.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "External resource name.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "status": "Enable/disable user resource.",
    "type": "User resource type.",
    "namespace": "Generic external connector address namespace.",
    "object-array-path": "JSON Path to array of generic addresses in resource.",
    "address-name-field": "JSON Path to address name in generic address entry.",
    "address-data-field": "JSON Path to address data in generic address entry.",
    "address-comment-field": "JSON Path to address description in generic address entry.",
    "update-method": "External resource update method.",
    "category": "User resource category.",
    "username": "HTTP basic authentication user name.",
    "password": "HTTP basic authentication password.",
    "client-cert-auth": "Enable/disable using client certificate for TLS authentication.",
    "client-cert": "Client certificate name.",
    "comments": "Comment.",
    "resource": "URL of external resource.",
    "user-agent": "HTTP User-Agent header (default = 'curl/7.58.0').",
    "server-identity-check": "Certificate verification option.",
    "refresh-rate": "Time interval to refresh external resource (1 - 43200 min, default = 5 min).",
    "source-ip": "Source IPv4 address used to communicate with server.",
    "source-ip-interface": "IPv4 Source interface for communication with the server.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "namespace": {"type": "string", "max_length": 15},
    "object-array-path": {"type": "string", "max_length": 511},
    "address-name-field": {"type": "string", "max_length": 511},
    "address-data-field": {"type": "string", "max_length": 511},
    "address-comment-field": {"type": "string", "max_length": 511},
    "category": {"type": "integer", "min": 192, "max": 221},
    "username": {"type": "string", "max_length": 64},
    "client-cert": {"type": "string", "max_length": 79},
    "resource": {"type": "string", "max_length": 511},
    "refresh-rate": {"type": "integer", "min": 1, "max": 43200},
    "source-ip-interface": {"type": "string", "max_length": 15},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_TYPE = [
    "category",
    "domain",
    "malware",
    "address",
    "mac-address",
    "data",
    "generic-address",
]
VALID_BODY_UPDATE_METHOD = [
    "feed",
    "push",
]
VALID_BODY_CLIENT_CERT_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_SERVER_IDENTITY_CHECK = [
    "none",
    "basic",
    "full",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_external_resource_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/external_resource."""
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


def validate_system_external_resource_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/external_resource object."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-method" in payload:
        is_valid, error = _validate_enum_field(
            "update-method",
            payload["update-method"],
            VALID_BODY_UPDATE_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert-auth",
            payload["client-cert-auth"],
            VALID_BODY_CLIENT_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_external_resource_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/external_resource."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-method" in payload:
        is_valid, error = _validate_enum_field(
            "update-method",
            payload["update-method"],
            VALID_BODY_UPDATE_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert-auth",
            payload["client-cert-auth"],
            VALID_BODY_CLIENT_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
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
    "endpoint": "system/external_resource",
    "category": "cmdb",
    "api_path": "system/external-resource",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure external resource.",
    "total_fields": 25,
    "required_fields_count": 3,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
