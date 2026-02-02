"""Validation helpers for ftp_proxy/explicit - Auto-generated"""

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
    "status": "disable",
    "incoming-port": "",
    "incoming-ip": "0.0.0.0",
    "outgoing-ip": "",
    "sec-default-action": "deny",
    "server-data-mode": "client",
    "ssl": "disable",
    "ssl-dh-bits": "2048",
    "ssl-algorithm": "high",
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
    "status": "option",  # Enable/disable the explicit FTP proxy.
    "incoming-port": "user",  # Accept incoming FTP requests on one or more ports.
    "incoming-ip": "ipv4-address-any",  # Accept incoming FTP requests from this IP address. An interf
    "outgoing-ip": "ipv4-address-any",  # Outgoing FTP requests will leave from this IP address. An in
    "sec-default-action": "option",  # Accept or deny explicit FTP proxy sessions when no FTP proxy
    "server-data-mode": "option",  # Determine mode of data session on FTP server side.
    "ssl": "option",  # Enable/disable the explicit FTPS proxy.
    "ssl-cert": "string",  # List of certificate names to use for SSL connections to this
    "ssl-dh-bits": "option",  # Bit-size of Diffie-Hellman (DH) prime used in DHE-RSA negoti
    "ssl-algorithm": "option",  # Relative strength of encryption algorithms accepted in negot
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable the explicit FTP proxy.",
    "incoming-port": "Accept incoming FTP requests on one or more ports.",
    "incoming-ip": "Accept incoming FTP requests from this IP address. An interface must have this IP address.",
    "outgoing-ip": "Outgoing FTP requests will leave from this IP address. An interface must have this IP address.",
    "sec-default-action": "Accept or deny explicit FTP proxy sessions when no FTP proxy firewall policy exists.",
    "server-data-mode": "Determine mode of data session on FTP server side.",
    "ssl": "Enable/disable the explicit FTPS proxy.",
    "ssl-cert": "List of certificate names to use for SSL connections to this server.",
    "ssl-dh-bits": "Bit-size of Diffie-Hellman (DH) prime used in DHE-RSA negotiation (default = 2048).",
    "ssl-algorithm": "Relative strength of encryption algorithms accepted in negotiation.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ssl-cert": {
        "name": {
            "type": "string",
            "help": "Certificate list.",
            "default": "Fortinet_SSL",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SEC_DEFAULT_ACTION = [
    "accept",
    "deny",
]
VALID_BODY_SERVER_DATA_MODE = [
    "client",
    "passive",
]
VALID_BODY_SSL = [
    "enable",
    "disable",
]
VALID_BODY_SSL_DH_BITS = [
    "768",
    "1024",
    "1536",
    "2048",
]
VALID_BODY_SSL_ALGORITHM = [
    "high",
    "medium",
    "low",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_ftp_proxy_explicit_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for ftp_proxy/explicit."""
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


def validate_ftp_proxy_explicit_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new ftp_proxy/explicit object."""
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
    if "sec-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "sec-default-action",
            payload["sec-default-action"],
            VALID_BODY_SEC_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-data-mode" in payload:
        is_valid, error = _validate_enum_field(
            "server-data-mode",
            payload["server-data-mode"],
            VALID_BODY_SERVER_DATA_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl" in payload:
        is_valid, error = _validate_enum_field(
            "ssl",
            payload["ssl"],
            VALID_BODY_SSL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-dh-bits" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-dh-bits",
            payload["ssl-dh-bits"],
            VALID_BODY_SSL_DH_BITS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-algorithm",
            payload["ssl-algorithm"],
            VALID_BODY_SSL_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_ftp_proxy_explicit_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update ftp_proxy/explicit."""
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
    if "sec-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "sec-default-action",
            payload["sec-default-action"],
            VALID_BODY_SEC_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-data-mode" in payload:
        is_valid, error = _validate_enum_field(
            "server-data-mode",
            payload["server-data-mode"],
            VALID_BODY_SERVER_DATA_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl" in payload:
        is_valid, error = _validate_enum_field(
            "ssl",
            payload["ssl"],
            VALID_BODY_SSL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-dh-bits" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-dh-bits",
            payload["ssl-dh-bits"],
            VALID_BODY_SSL_DH_BITS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-algorithm",
            payload["ssl-algorithm"],
            VALID_BODY_SSL_ALGORITHM,
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
    "endpoint": "ftp_proxy/explicit",
    "category": "cmdb",
    "api_path": "ftp-proxy/explicit",
    "help": "Configure explicit FTP proxy settings.",
    "total_fields": 10,
    "required_fields_count": 0,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
