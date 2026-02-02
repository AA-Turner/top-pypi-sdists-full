"""Validation helpers for vpn/certificate/crl - Auto-generated"""

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
    "name",  # Name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "crl": "",
    "range": "vdom",
    "source": "user",
    "update-vdom": "root",
    "ldap-server": "",
    "ldap-username": "",
    "http-url": "",
    "scep-url": "",
    "scep-cert": "Fortinet_CA_SSL",
    "update-interval": 0,
    "source-ip": "0.0.0.0",
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
    "name": "string",  # Name.
    "crl": "user",  # Certificate Revocation List as a PEM file.
    "range": "option",  # Either global or VDOM IP address range for the certificate.
    "source": "option",  # Certificate source type.
    "update-vdom": "string",  # VDOM for CRL update.
    "ldap-server": "string",  # LDAP server name for CRL auto-update.
    "ldap-username": "string",  # LDAP server user name.
    "ldap-password": "password",  # LDAP server user password.
    "http-url": "string",  # HTTP server URL for CRL auto-update.
    "scep-url": "string",  # SCEP server URL for CRL auto-update.
    "scep-cert": "string",  # Local certificate for SCEP communication for CRL auto-update
    "update-interval": "integer",  # Time in seconds before the FortiGate checks for an updated C
    "source-ip": "ipv4-address",  # Source IP address for communications to a HTTP or SCEP CA se
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "crl": "Certificate Revocation List as a PEM file.",
    "range": "Either global or VDOM IP address range for the certificate.",
    "source": "Certificate source type.",
    "update-vdom": "VDOM for CRL update.",
    "ldap-server": "LDAP server name for CRL auto-update.",
    "ldap-username": "LDAP server user name.",
    "ldap-password": "LDAP server user password.",
    "http-url": "HTTP server URL for CRL auto-update.",
    "scep-url": "SCEP server URL for CRL auto-update.",
    "scep-cert": "Local certificate for SCEP communication for CRL auto-update.",
    "update-interval": "Time in seconds before the FortiGate checks for an updated CRL. Set to 0 to update only when it expires.",
    "source-ip": "Source IP address for communications to a HTTP or SCEP CA server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "update-vdom": {"type": "string", "max_length": 31},
    "ldap-server": {"type": "string", "max_length": 35},
    "ldap-username": {"type": "string", "max_length": 63},
    "http-url": {"type": "string", "max_length": 255},
    "scep-url": {"type": "string", "max_length": 255},
    "scep-cert": {"type": "string", "max_length": 35},
    "update-interval": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_RANGE = [
    "global",
    "vdom",
]
VALID_BODY_SOURCE = [
    "factory",
    "user",
    "bundle",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_vpn_certificate_crl_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/certificate/crl."""
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


def validate_vpn_certificate_crl_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/certificate/crl object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "range" in payload:
        is_valid, error = _validate_enum_field(
            "range",
            payload["range"],
            VALID_BODY_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "source" in payload:
        is_valid, error = _validate_enum_field(
            "source",
            payload["source"],
            VALID_BODY_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_vpn_certificate_crl_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/certificate/crl."""
    # Validate enum values using central function
    if "range" in payload:
        is_valid, error = _validate_enum_field(
            "range",
            payload["range"],
            VALID_BODY_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "source" in payload:
        is_valid, error = _validate_enum_field(
            "source",
            payload["source"],
            VALID_BODY_SOURCE,
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
    "endpoint": "vpn/certificate/crl",
    "category": "cmdb",
    "api_path": "vpn.certificate/crl",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Certificate Revocation List as a PEM file.",
    "total_fields": 13,
    "required_fields_count": 1,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
