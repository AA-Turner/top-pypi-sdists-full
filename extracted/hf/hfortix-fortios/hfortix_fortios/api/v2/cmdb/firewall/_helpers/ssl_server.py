"""Validation helpers for firewall/ssl_server - Auto-generated"""

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
    "ip": "0.0.0.0",
    "port": 443,
    "ssl-mode": "full",
    "add-header-x-forwarded-proto": "enable",
    "mapped-port": 80,
    "ssl-dh-bits": "2048",
    "ssl-algorithm": "high",
    "ssl-client-renegotiation": "allow",
    "ssl-min-version": "tls-1.1",
    "ssl-max-version": "tls-1.3",
    "ssl-send-empty-frags": "enable",
    "url-rewrite": "disable",
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
    "ip": "ipv4-address-any",  # IPv4 address of the SSL server.
    "port": "integer",  # Server service port (1 - 65535, default = 443).
    "ssl-mode": "option",  # SSL/TLS mode for encryption and decryption of traffic.
    "add-header-x-forwarded-proto": "option",  # Enable/disable adding an X-Forwarded-Proto header to forward
    "mapped-port": "integer",  # Mapped server service port (1 - 65535, default = 80).
    "ssl-cert": "string",  # List of certificate names to use for SSL connections to this
    "ssl-dh-bits": "option",  # Bit-size of Diffie-Hellman (DH) prime used in DHE-RSA negoti
    "ssl-algorithm": "option",  # Relative strength of encryption algorithms accepted in negot
    "ssl-client-renegotiation": "option",  # Allow or block client renegotiation by server.
    "ssl-min-version": "option",  # Lowest SSL/TLS version to negotiate.
    "ssl-max-version": "option",  # Highest SSL/TLS version to negotiate.
    "ssl-send-empty-frags": "option",  # Enable/disable sending empty fragments to avoid attack on CB
    "url-rewrite": "option",  # Enable/disable rewriting the URL.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Server name.",
    "ip": "IPv4 address of the SSL server.",
    "port": "Server service port (1 - 65535, default = 443).",
    "ssl-mode": "SSL/TLS mode for encryption and decryption of traffic.",
    "add-header-x-forwarded-proto": "Enable/disable adding an X-Forwarded-Proto header to forwarded requests.",
    "mapped-port": "Mapped server service port (1 - 65535, default = 80).",
    "ssl-cert": "List of certificate names to use for SSL connections to this server. (default = \"Fortinet_SSL\").",
    "ssl-dh-bits": "Bit-size of Diffie-Hellman (DH) prime used in DHE-RSA negotiation (default = 2048).",
    "ssl-algorithm": "Relative strength of encryption algorithms accepted in negotiation.",
    "ssl-client-renegotiation": "Allow or block client renegotiation by server.",
    "ssl-min-version": "Lowest SSL/TLS version to negotiate.",
    "ssl-max-version": "Highest SSL/TLS version to negotiate.",
    "ssl-send-empty-frags": "Enable/disable sending empty fragments to avoid attack on CBC IV.",
    "url-rewrite": "Enable/disable rewriting the URL.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "port": {"type": "integer", "min": 1, "max": 65535},
    "mapped-port": {"type": "integer", "min": 1, "max": 65535},
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
VALID_BODY_SSL_MODE = [
    "half",
    "full",
]
VALID_BODY_ADD_HEADER_X_FORWARDED_PROTO = [
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
VALID_BODY_SSL_CLIENT_RENEGOTIATION = [
    "allow",
    "deny",
    "secure",
]
VALID_BODY_SSL_MIN_VERSION = [
    "tls-1.0",
    "tls-1.1",
    "tls-1.2",
    "tls-1.3",
]
VALID_BODY_SSL_MAX_VERSION = [
    "tls-1.0",
    "tls-1.1",
    "tls-1.2",
    "tls-1.3",
]
VALID_BODY_SSL_SEND_EMPTY_FRAGS = [
    "enable",
    "disable",
]
VALID_BODY_URL_REWRITE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_ssl_server_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/ssl_server."""
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


def validate_firewall_ssl_server_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/ssl_server object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ssl-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-mode",
            payload["ssl-mode"],
            VALID_BODY_SSL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-header-x-forwarded-proto" in payload:
        is_valid, error = _validate_enum_field(
            "add-header-x-forwarded-proto",
            payload["add-header-x-forwarded-proto"],
            VALID_BODY_ADD_HEADER_X_FORWARDED_PROTO,
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
    if "ssl-client-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-renegotiation",
            payload["ssl-client-renegotiation"],
            VALID_BODY_SSL_CLIENT_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-version",
            payload["ssl-min-version"],
            VALID_BODY_SSL_MIN_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-max-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-max-version",
            payload["ssl-max-version"],
            VALID_BODY_SSL_MAX_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-send-empty-frags" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-send-empty-frags",
            payload["ssl-send-empty-frags"],
            VALID_BODY_SSL_SEND_EMPTY_FRAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "url-rewrite" in payload:
        is_valid, error = _validate_enum_field(
            "url-rewrite",
            payload["url-rewrite"],
            VALID_BODY_URL_REWRITE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_ssl_server_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/ssl_server."""
    # Validate enum values using central function
    if "ssl-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-mode",
            payload["ssl-mode"],
            VALID_BODY_SSL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-header-x-forwarded-proto" in payload:
        is_valid, error = _validate_enum_field(
            "add-header-x-forwarded-proto",
            payload["add-header-x-forwarded-proto"],
            VALID_BODY_ADD_HEADER_X_FORWARDED_PROTO,
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
    if "ssl-client-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-renegotiation",
            payload["ssl-client-renegotiation"],
            VALID_BODY_SSL_CLIENT_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-version",
            payload["ssl-min-version"],
            VALID_BODY_SSL_MIN_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-max-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-max-version",
            payload["ssl-max-version"],
            VALID_BODY_SSL_MAX_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-send-empty-frags" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-send-empty-frags",
            payload["ssl-send-empty-frags"],
            VALID_BODY_SSL_SEND_EMPTY_FRAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "url-rewrite" in payload:
        is_valid, error = _validate_enum_field(
            "url-rewrite",
            payload["url-rewrite"],
            VALID_BODY_URL_REWRITE,
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
    "endpoint": "firewall/ssl_server",
    "category": "cmdb",
    "api_path": "firewall/ssl-server",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure SSL servers.",
    "total_fields": 14,
    "required_fields_count": 0,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
