"""Validation helpers for user/peer - Auto-generated"""

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
    "mandatory-ca-verify": "enable",
    "ca": "",
    "subject": "",
    "cn": "",
    "cn-type": "string",
    "mfa-mode": "none",
    "mfa-server": "",
    "mfa-username": "",
    "ocsp-override-server": "",
    "two-factor": "disable",
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
    "name": "string",  # Peer name.
    "mandatory-ca-verify": "option",  # Determine what happens to the peer if the CA certificate is 
    "ca": "string",  # Name of the CA certificate.
    "subject": "string",  # Peer certificate name constraints.
    "cn": "string",  # Peer certificate common name.
    "cn-type": "option",  # Peer certificate common name type.
    "mfa-mode": "option",  # MFA mode for remote peer authentication/authorization.
    "mfa-server": "string",  # Name of a remote authenticator. Performs client access right
    "mfa-username": "string",  # Unified username for remote authentication.
    "mfa-password": "password",  # Unified password for remote authentication. This field may b
    "ocsp-override-server": "string",  # Online Certificate Status Protocol (OCSP) server for certifi
    "two-factor": "option",  # Enable/disable two-factor authentication, applying certifica
    "passwd": "password",  # Peer's password used for two-factor authentication.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Peer name.",
    "mandatory-ca-verify": "Determine what happens to the peer if the CA certificate is not installed. Disable to automatically consider the peer certificate as valid.",
    "ca": "Name of the CA certificate.",
    "subject": "Peer certificate name constraints.",
    "cn": "Peer certificate common name.",
    "cn-type": "Peer certificate common name type.",
    "mfa-mode": "MFA mode for remote peer authentication/authorization.",
    "mfa-server": "Name of a remote authenticator. Performs client access right check.",
    "mfa-username": "Unified username for remote authentication.",
    "mfa-password": "Unified password for remote authentication. This field may be left empty when RADIUS authentication is used, in which case the FortiGate will use the RADIUS username as a password. ",
    "ocsp-override-server": "Online Certificate Status Protocol (OCSP) server for certificate retrieval.",
    "two-factor": "Enable/disable two-factor authentication, applying certificate and password-based authentication.",
    "passwd": "Peer's password used for two-factor authentication.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "ca": {"type": "string", "max_length": 127},
    "subject": {"type": "string", "max_length": 255},
    "cn": {"type": "string", "max_length": 255},
    "mfa-server": {"type": "string", "max_length": 35},
    "mfa-username": {"type": "string", "max_length": 35},
    "ocsp-override-server": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_MANDATORY_CA_VERIFY = [
    "enable",
    "disable",
]
VALID_BODY_CN_TYPE = [
    "string",
    "email",
    "FQDN",
    "ipv4",
    "ipv6",
]
VALID_BODY_MFA_MODE = [
    "none",
    "password",
    "subject-identity",
]
VALID_BODY_TWO_FACTOR = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_peer_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/peer."""
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


def validate_user_peer_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/peer object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "mandatory-ca-verify" in payload:
        is_valid, error = _validate_enum_field(
            "mandatory-ca-verify",
            payload["mandatory-ca-verify"],
            VALID_BODY_MANDATORY_CA_VERIFY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cn-type" in payload:
        is_valid, error = _validate_enum_field(
            "cn-type",
            payload["cn-type"],
            VALID_BODY_CN_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mfa-mode" in payload:
        is_valid, error = _validate_enum_field(
            "mfa-mode",
            payload["mfa-mode"],
            VALID_BODY_MFA_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "two-factor" in payload:
        is_valid, error = _validate_enum_field(
            "two-factor",
            payload["two-factor"],
            VALID_BODY_TWO_FACTOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_peer_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/peer."""
    # Validate enum values using central function
    if "mandatory-ca-verify" in payload:
        is_valid, error = _validate_enum_field(
            "mandatory-ca-verify",
            payload["mandatory-ca-verify"],
            VALID_BODY_MANDATORY_CA_VERIFY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cn-type" in payload:
        is_valid, error = _validate_enum_field(
            "cn-type",
            payload["cn-type"],
            VALID_BODY_CN_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mfa-mode" in payload:
        is_valid, error = _validate_enum_field(
            "mfa-mode",
            payload["mfa-mode"],
            VALID_BODY_MFA_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "two-factor" in payload:
        is_valid, error = _validate_enum_field(
            "two-factor",
            payload["two-factor"],
            VALID_BODY_TWO_FACTOR,
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
    "endpoint": "user/peer",
    "category": "cmdb",
    "api_path": "user/peer",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure peer users.",
    "total_fields": 13,
    "required_fields_count": 0,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
