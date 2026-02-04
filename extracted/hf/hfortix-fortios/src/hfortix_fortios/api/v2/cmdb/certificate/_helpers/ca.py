"""Validation helpers for certificate/ca - Auto-generated"""

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
    "ca",  # CA certificate as a PEM file.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "ca": "",
    "range": "global",
    "source": "user",
    "ssl-inspection-trusted": "enable",
    "scep-url": "",
    "est-url": "",
    "auto-update-days": 0,
    "auto-update-days-warning": 0,
    "source-ip": "0.0.0.0",
    "ca-identifier": "",
    "obsolete": "disable",
    "fabric-ca": "disable",
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
    "ca": "user",  # CA certificate as a PEM file.
    "range": "option",  # Either global or VDOM IP address range for the CA certificate.
    "source": "option",  # CA certificate source type.
    "ssl-inspection-trusted": "option",  # Enable/disable this CA as a trusted CA for SSL inspection.
    "scep-url": "string",  # URL of the SCEP server.
    "est-url": "string",  # URL of the EST server.
    "auto-update-days": "integer",  # Number of days to wait before requesting an updated CA certificate (0 - 42949672
    "auto-update-days-warning": "integer",  # Number of days before an expiry-warning message is generated (0 - 4294967295, 0 
    "source-ip": "ipv4-address",  # Source IP address for communications to the SCEP server.
    "ca-identifier": "string",  # CA identifier of the SCEP server.
    "obsolete": "option",  # Enable/disable this CA as obsoleted.
    "fabric-ca": "option",  # Enable/disable synchronization of CA across Security Fabric.
    "details": "key",  # Print CA certificate detailed information.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "ca": "CA certificate as a PEM file.",
    "range": "Either global or VDOM IP address range for the CA certificate.",
    "source": "CA certificate source type.",
    "ssl-inspection-trusted": "Enable/disable this CA as a trusted CA for SSL inspection.",
    "scep-url": "URL of the SCEP server.",
    "est-url": "URL of the EST server.",
    "auto-update-days": "Number of days to wait before requesting an updated CA certificate (0 - 4294967295, 0 = disabled).",
    "auto-update-days-warning": "Number of days before an expiry-warning message is generated (0 - 4294967295, 0 = disabled).",
    "source-ip": "Source IP address for communications to the SCEP server.",
    "ca-identifier": "CA identifier of the SCEP server.",
    "obsolete": "Enable/disable this CA as obsoleted.",
    "fabric-ca": "Enable/disable synchronization of CA across Security Fabric.",
    "details": "Print CA certificate detailed information.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "scep-url": {"type": "string", "max_length": 255},
    "est-url": {"type": "string", "max_length": 255},
    "auto-update-days": {"type": "integer", "min": 0, "max": 4294967295},
    "auto-update-days-warning": {"type": "integer", "min": 0, "max": 4294967295},
    "ca-identifier": {"type": "string", "max_length": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "details": {
        "<CA certficate name>": {
            "type": "value",
            "help": "CA certificate name.",
        },
    },
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
VALID_BODY_SSL_INSPECTION_TRUSTED = [
    "enable",
    "disable",
]
VALID_BODY_OBSOLETE = [
    "disable",
    "enable",
]
VALID_BODY_FABRIC_CA = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_certificate_ca_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for certificate/ca."""
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


def validate_certificate_ca_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new certificate/ca object."""
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
    if "ssl-inspection-trusted" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-inspection-trusted",
            payload["ssl-inspection-trusted"],
            VALID_BODY_SSL_INSPECTION_TRUSTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "obsolete" in payload:
        is_valid, error = _validate_enum_field(
            "obsolete",
            payload["obsolete"],
            VALID_BODY_OBSOLETE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fabric-ca" in payload:
        is_valid, error = _validate_enum_field(
            "fabric-ca",
            payload["fabric-ca"],
            VALID_BODY_FABRIC_CA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_certificate_ca_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update certificate/ca."""
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
    if "ssl-inspection-trusted" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-inspection-trusted",
            payload["ssl-inspection-trusted"],
            VALID_BODY_SSL_INSPECTION_TRUSTED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "obsolete" in payload:
        is_valid, error = _validate_enum_field(
            "obsolete",
            payload["obsolete"],
            VALID_BODY_OBSOLETE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fabric-ca" in payload:
        is_valid, error = _validate_enum_field(
            "fabric-ca",
            payload["fabric-ca"],
            VALID_BODY_FABRIC_CA,
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
    "endpoint": "certificate/ca",
    "category": "cmdb",
    "api_path": "certificate/ca",
    "mkey": "name",
    "mkey_type": "string",
    "help": "CA certificate.",
    "total_fields": 14,
    "required_fields_count": 2,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
