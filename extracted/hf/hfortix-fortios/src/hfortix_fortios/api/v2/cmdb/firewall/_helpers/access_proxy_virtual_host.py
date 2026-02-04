"""Validation helpers for firewall/access_proxy_virtual_host - Auto-generated"""

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
    "ssl-certificate",  # SSL certificates for this host.
    "host",  # The host name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "host": "",
    "host-type": "sub-string",
    "replacemsg-group": "",
    "empty-cert-action": "block",
    "user-agent-detect": "enable",
    "client-cert": "enable",
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
    "name": "string",  # Virtual host name.
    "ssl-certificate": "string",  # SSL certificates for this host.
    "host": "string",  # The host name.
    "host-type": "option",  # Type of host pattern.
    "replacemsg-group": "string",  # Access-proxy-virtual-host replacement message override group.
    "empty-cert-action": "option",  # Action for an empty client certificate.
    "user-agent-detect": "option",  # Enable/disable detecting device type by HTTP user-agent if no client certificate
    "client-cert": "option",  # Enable/disable requesting client certificate.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Virtual host name.",
    "ssl-certificate": "SSL certificates for this host.",
    "host": "The host name.",
    "host-type": "Type of host pattern.",
    "replacemsg-group": "Access-proxy-virtual-host replacement message override group.",
    "empty-cert-action": "Action for an empty client certificate.",
    "user-agent-detect": "Enable/disable detecting device type by HTTP user-agent if no client certificate is provided.",
    "client-cert": "Enable/disable requesting client certificate.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "host": {"type": "string", "max_length": 79},
    "replacemsg-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ssl-certificate": {
        "name": {
            "type": "string",
            "help": "Certificate list.",
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_HOST_TYPE = [
    "sub-string",
    "wildcard",
]
VALID_BODY_EMPTY_CERT_ACTION = [
    "accept",
    "block",
    "accept-unmanageable",
]
VALID_BODY_USER_AGENT_DETECT = [
    "disable",
    "enable",
]
VALID_BODY_CLIENT_CERT = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_access_proxy_virtual_host_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/access_proxy_virtual_host."""
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


def validate_firewall_access_proxy_virtual_host_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/access_proxy_virtual_host object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "host-type" in payload:
        is_valid, error = _validate_enum_field(
            "host-type",
            payload["host-type"],
            VALID_BODY_HOST_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "empty-cert-action" in payload:
        is_valid, error = _validate_enum_field(
            "empty-cert-action",
            payload["empty-cert-action"],
            VALID_BODY_EMPTY_CERT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-agent-detect" in payload:
        is_valid, error = _validate_enum_field(
            "user-agent-detect",
            payload["user-agent-detect"],
            VALID_BODY_USER_AGENT_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert",
            payload["client-cert"],
            VALID_BODY_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_access_proxy_virtual_host_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/access_proxy_virtual_host."""
    # Validate enum values using central function
    if "host-type" in payload:
        is_valid, error = _validate_enum_field(
            "host-type",
            payload["host-type"],
            VALID_BODY_HOST_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "empty-cert-action" in payload:
        is_valid, error = _validate_enum_field(
            "empty-cert-action",
            payload["empty-cert-action"],
            VALID_BODY_EMPTY_CERT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-agent-detect" in payload:
        is_valid, error = _validate_enum_field(
            "user-agent-detect",
            payload["user-agent-detect"],
            VALID_BODY_USER_AGENT_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert",
            payload["client-cert"],
            VALID_BODY_CLIENT_CERT,
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
    "endpoint": "firewall/access_proxy_virtual_host",
    "category": "cmdb",
    "api_path": "firewall/access-proxy-virtual-host",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Access Proxy virtual hosts.",
    "total_fields": 8,
    "required_fields_count": 2,
    "fields_with_defaults_count": 7,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
