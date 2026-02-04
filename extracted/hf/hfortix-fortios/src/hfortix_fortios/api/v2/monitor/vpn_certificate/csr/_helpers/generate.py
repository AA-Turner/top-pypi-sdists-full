"""Validation helpers for vpn_certificate/csr/generate - Auto-generated"""

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
    "certname",  # 
    "subject",  # 
    "keytype",  # 
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
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
    "certname": "string",  # 
    "subject": "string",  # 
    "keytype": "string",  # 
    "keysize": "int",  # 
    "curvename": "string",  # 
    "orgunits": "array",  # 
    "org": "string",  # 
    "city": "string",  # 
    "state": "string",  # 
    "countrycode": "string",  # 
    "email": "string",  # 
    "subject_alt_name": "string",  # 
    "password": "string",  # 
    "scep_url": "string",  # 
    "scep_password": "string",  # 
    "scope": "string",  # 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_KEYTYPE = [
    "rsa",
    "ec",
]
VALID_BODY_KEYSIZE = [
    "1024",
    "1536",
    "2048",
    "4096",
]
VALID_BODY_CURVENAME = [
    "secp256r1",
    "secp384r1",
    "secp521r1",
]
VALID_BODY_SCOPE = [
    "vdom",
    "global",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_vpn_certificate_csr_generate_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn_certificate/csr/generate."""
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


def validate_vpn_certificate_csr_generate_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn_certificate/csr/generate object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "keytype" in payload:
        is_valid, error = _validate_enum_field(
            "keytype",
            payload["keytype"],
            VALID_BODY_KEYTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "keysize" in payload:
        is_valid, error = _validate_enum_field(
            "keysize",
            payload["keysize"],
            VALID_BODY_KEYSIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "curvename" in payload:
        is_valid, error = _validate_enum_field(
            "curvename",
            payload["curvename"],
            VALID_BODY_CURVENAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scope" in payload:
        is_valid, error = _validate_enum_field(
            "scope",
            payload["scope"],
            VALID_BODY_SCOPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_vpn_certificate_csr_generate_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn_certificate/csr/generate."""
    # Validate enum values using central function
    if "keytype" in payload:
        is_valid, error = _validate_enum_field(
            "keytype",
            payload["keytype"],
            VALID_BODY_KEYTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "keysize" in payload:
        is_valid, error = _validate_enum_field(
            "keysize",
            payload["keysize"],
            VALID_BODY_KEYSIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "curvename" in payload:
        is_valid, error = _validate_enum_field(
            "curvename",
            payload["curvename"],
            VALID_BODY_CURVENAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scope" in payload:
        is_valid, error = _validate_enum_field(
            "scope",
            payload["scope"],
            VALID_BODY_SCOPE,
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
    "endpoint": "vpn_certificate/csr/generate",
    "category": "monitor",
    "api_path": "vpn-certificate/csr/generate",
    "help": "Generate a certificate signing request (CSR) and a private key. The CSR can be retrieved / downloaded from CLI, GUI and REST API.",
    "total_fields": 16,
    "required_fields_count": 3,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
