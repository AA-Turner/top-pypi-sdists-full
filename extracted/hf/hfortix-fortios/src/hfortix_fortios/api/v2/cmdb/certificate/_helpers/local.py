"""Validation helpers for certificate/local - Auto-generated"""

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
    "private-key",  # PEM format key encrypted with a password.
    "acme-domain",  # A valid domain that resolves to this FortiGate unit.
    "acme-email",  # Contact email address that is required by some CAs like LetsEncrypt.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "comments": "",
    "private-key": "",
    "certificate": "",
    "csr": "",
    "state": "",
    "scep-url": "",
    "range": "global",
    "source": "user",
    "auto-regenerate-days": 0,
    "auto-regenerate-days-warning": 0,
    "ca-identifier": "",
    "name-encoding": "printable",
    "source-ip": "0.0.0.0",
    "ike-localid": "",
    "ike-localid-type": "asn1dn",
    "enroll-protocol": "none",
    "private-key-retain": "disable",
    "cmp-server": "",
    "cmp-path": "",
    "cmp-server-cert": "",
    "cmp-regeneration-method": "keyupate",
    "acme-ca-url": "https://acme-v02.api.letsencrypt.org/directory",
    "acme-domain": "",
    "acme-email": "",
    "acme-rsa-key-size": 2048,
    "acme-renew-window": 30,
    "est-server": "",
    "est-ca-id": "",
    "est-http-username": "",
    "est-client-cert": "",
    "est-server-cert": "",
    "est-srp-username": "",
    "est-regeneration-method": "create-new-key",
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
    "password": "password",  # Password as a PEM file.
    "comments": "string",  # Comment.
    "private-key": "user",  # PEM format key encrypted with a password.
    "certificate": "user",  # PEM format certificate.
    "csr": "user",  # Certificate Signing Request.
    "state": "user",  # Certificate Signing Request State.
    "scep-url": "string",  # SCEP server URL.
    "range": "option",  # Either a global or VDOM IP address range for the certificate.
    "source": "option",  # Certificate source type.
    "auto-regenerate-days": "integer",  # Number of days to wait before expiry of an updated local certificate is requeste
    "auto-regenerate-days-warning": "integer",  # Number of days to wait before an expiry warning message is generated (0 = disabl
    "scep-password": "password",  # SCEP server challenge password for auto-regeneration.
    "ca-identifier": "string",  # CA identifier of the CA server for signing via SCEP.
    "name-encoding": "option",  # Name encoding method for auto-regeneration.
    "source-ip": "ipv4-address",  # Source IP address for communications to the SCEP server.
    "ike-localid": "string",  # Local ID the FortiGate uses for authentication as a VPN client.
    "ike-localid-type": "option",  # IKE local ID type.
    "enroll-protocol": "option",  # Certificate enrollment protocol.
    "private-key-retain": "option",  # Enable/disable retention of private key during SCEP renewal (default = disable).
    "cmp-server": "string",  # Address and port for CMP server (format = address:port).
    "cmp-path": "string",  # Path location inside CMP server.
    "cmp-server-cert": "string",  # CMP server certificate.
    "cmp-regeneration-method": "option",  # CMP auto-regeneration method.
    "acme-ca-url": "string",  # The URL for the ACME CA server (Let's Encrypt is the default provider).
    "acme-domain": "string",  # A valid domain that resolves to this FortiGate unit.
    "acme-email": "string",  # Contact email address that is required by some CAs like LetsEncrypt.
    "acme-eab-key-id": "var-string",  # External Account Binding Key ID (optional setting).
    "acme-eab-key-hmac": "password",  # External Account Binding HMAC Key (URL-encoded base64).
    "acme-rsa-key-size": "integer",  # Length of the RSA private key of the generated cert (Minimum 2048 bits).
    "acme-renew-window": "integer",  # Beginning of the renewal window (in days before certificate expiration, 30 by de
    "est-server": "string",  # Address and port for EST server (e.g. https://example.com:1234).
    "est-ca-id": "string",  # CA identifier of the CA server for signing via EST.
    "est-http-username": "string",  # HTTP Authentication username for signing via EST.
    "est-http-password": "password",  # HTTP Authentication password for signing via EST.
    "est-client-cert": "string",  # Certificate used to authenticate this FortiGate to EST server.
    "est-server-cert": "string",  # EST server's certificate must be verifiable by this certificate to be authentica
    "est-srp-username": "string",  # EST SRP authentication username.
    "est-srp-password": "password",  # EST SRP authentication password.
    "est-regeneration-method": "option",  # EST behavioral options during re-enrollment.
    "details": "key",  # Print local certificate detailed information.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "password": "Password as a PEM file.",
    "comments": "Comment.",
    "private-key": "PEM format key encrypted with a password.",
    "certificate": "PEM format certificate.",
    "csr": "Certificate Signing Request.",
    "state": "Certificate Signing Request State.",
    "scep-url": "SCEP server URL.",
    "range": "Either a global or VDOM IP address range for the certificate.",
    "source": "Certificate source type.",
    "auto-regenerate-days": "Number of days to wait before expiry of an updated local certificate is requested (0 = disabled).",
    "auto-regenerate-days-warning": "Number of days to wait before an expiry warning message is generated (0 = disabled).",
    "scep-password": "SCEP server challenge password for auto-regeneration.",
    "ca-identifier": "CA identifier of the CA server for signing via SCEP.",
    "name-encoding": "Name encoding method for auto-regeneration.",
    "source-ip": "Source IP address for communications to the SCEP server.",
    "ike-localid": "Local ID the FortiGate uses for authentication as a VPN client.",
    "ike-localid-type": "IKE local ID type.",
    "enroll-protocol": "Certificate enrollment protocol.",
    "private-key-retain": "Enable/disable retention of private key during SCEP renewal (default = disable).",
    "cmp-server": "Address and port for CMP server (format = address:port).",
    "cmp-path": "Path location inside CMP server.",
    "cmp-server-cert": "CMP server certificate.",
    "cmp-regeneration-method": "CMP auto-regeneration method.",
    "acme-ca-url": "The URL for the ACME CA server (Let's Encrypt is the default provider).",
    "acme-domain": "A valid domain that resolves to this FortiGate unit.",
    "acme-email": "Contact email address that is required by some CAs like LetsEncrypt.",
    "acme-eab-key-id": "External Account Binding Key ID (optional setting).",
    "acme-eab-key-hmac": "External Account Binding HMAC Key (URL-encoded base64).",
    "acme-rsa-key-size": "Length of the RSA private key of the generated cert (Minimum 2048 bits).",
    "acme-renew-window": "Beginning of the renewal window (in days before certificate expiration, 30 by default).",
    "est-server": "Address and port for EST server (e.g. https://example.com:1234).",
    "est-ca-id": "CA identifier of the CA server for signing via EST.",
    "est-http-username": "HTTP Authentication username for signing via EST.",
    "est-http-password": "HTTP Authentication password for signing via EST.",
    "est-client-cert": "Certificate used to authenticate this FortiGate to EST server.",
    "est-server-cert": "EST server's certificate must be verifiable by this certificate to be authenticated.",
    "est-srp-username": "EST SRP authentication username.",
    "est-srp-password": "EST SRP authentication password.",
    "est-regeneration-method": "EST behavioral options during re-enrollment.",
    "details": "Print local certificate detailed information.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "comments": {"type": "string", "max_length": 511},
    "scep-url": {"type": "string", "max_length": 255},
    "auto-regenerate-days": {"type": "integer", "min": 0, "max": 4294967295},
    "auto-regenerate-days-warning": {"type": "integer", "min": 0, "max": 4294967295},
    "ca-identifier": {"type": "string", "max_length": 255},
    "ike-localid": {"type": "string", "max_length": 63},
    "cmp-server": {"type": "string", "max_length": 63},
    "cmp-path": {"type": "string", "max_length": 255},
    "cmp-server-cert": {"type": "string", "max_length": 79},
    "acme-ca-url": {"type": "string", "max_length": 255},
    "acme-domain": {"type": "string", "max_length": 255},
    "acme-email": {"type": "string", "max_length": 255},
    "acme-rsa-key-size": {"type": "integer", "min": 2048, "max": 4096},
    "acme-renew-window": {"type": "integer", "min": 1, "max": 60},
    "est-server": {"type": "string", "max_length": 255},
    "est-ca-id": {"type": "string", "max_length": 255},
    "est-http-username": {"type": "string", "max_length": 63},
    "est-client-cert": {"type": "string", "max_length": 79},
    "est-server-cert": {"type": "string", "max_length": 79},
    "est-srp-username": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "details": {
        "<certficate name>": {
            "type": "value",
            "help": "Local certificate name.",
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
VALID_BODY_NAME_ENCODING = [
    "printable",
    "utf8",
]
VALID_BODY_IKE_LOCALID_TYPE = [
    "asn1dn",
    "fqdn",
]
VALID_BODY_ENROLL_PROTOCOL = [
    "none",
    "scep",
    "cmpv2",
    "acme2",
    "est",
]
VALID_BODY_PRIVATE_KEY_RETAIN = [
    "enable",
    "disable",
]
VALID_BODY_CMP_REGENERATION_METHOD = [
    "keyupate",
    "renewal",
]
VALID_BODY_EST_REGENERATION_METHOD = [
    "create-new-key",
    "use-existing-key",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_certificate_local_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for certificate/local."""
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


def validate_certificate_local_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new certificate/local object."""
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
    if "name-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "name-encoding",
            payload["name-encoding"],
            VALID_BODY_NAME_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-localid-type" in payload:
        is_valid, error = _validate_enum_field(
            "ike-localid-type",
            payload["ike-localid-type"],
            VALID_BODY_IKE_LOCALID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enroll-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "enroll-protocol",
            payload["enroll-protocol"],
            VALID_BODY_ENROLL_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "private-key-retain" in payload:
        is_valid, error = _validate_enum_field(
            "private-key-retain",
            payload["private-key-retain"],
            VALID_BODY_PRIVATE_KEY_RETAIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmp-regeneration-method" in payload:
        is_valid, error = _validate_enum_field(
            "cmp-regeneration-method",
            payload["cmp-regeneration-method"],
            VALID_BODY_CMP_REGENERATION_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "est-regeneration-method" in payload:
        is_valid, error = _validate_enum_field(
            "est-regeneration-method",
            payload["est-regeneration-method"],
            VALID_BODY_EST_REGENERATION_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_certificate_local_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update certificate/local."""
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
    if "name-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "name-encoding",
            payload["name-encoding"],
            VALID_BODY_NAME_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-localid-type" in payload:
        is_valid, error = _validate_enum_field(
            "ike-localid-type",
            payload["ike-localid-type"],
            VALID_BODY_IKE_LOCALID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enroll-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "enroll-protocol",
            payload["enroll-protocol"],
            VALID_BODY_ENROLL_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "private-key-retain" in payload:
        is_valid, error = _validate_enum_field(
            "private-key-retain",
            payload["private-key-retain"],
            VALID_BODY_PRIVATE_KEY_RETAIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmp-regeneration-method" in payload:
        is_valid, error = _validate_enum_field(
            "cmp-regeneration-method",
            payload["cmp-regeneration-method"],
            VALID_BODY_CMP_REGENERATION_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "est-regeneration-method" in payload:
        is_valid, error = _validate_enum_field(
            "est-regeneration-method",
            payload["est-regeneration-method"],
            VALID_BODY_EST_REGENERATION_METHOD,
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
    "endpoint": "certificate/local",
    "category": "cmdb",
    "api_path": "certificate/local",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Local keys and certificates.",
    "total_fields": 41,
    "required_fields_count": 4,
    "fields_with_defaults_count": 34,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
