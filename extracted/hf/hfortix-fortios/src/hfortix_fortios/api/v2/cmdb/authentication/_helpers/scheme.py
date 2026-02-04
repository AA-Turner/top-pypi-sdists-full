"""Validation helpers for authentication/scheme - Auto-generated"""

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
    "method",  # Authentication methods (default = basic).
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "method": "",
    "negotiate-ntlm": "enable",
    "kerberos-keytab": "",
    "domain-controller": "",
    "saml-server": "",
    "saml-timeout": 120,
    "fsso-agent-for-ntlm": "",
    "require-tfa": "disable",
    "fsso-guest": "disable",
    "user-cert": "disable",
    "cert-http-header": "disable",
    "ssh-ca": "",
    "external-idp": "",
    "group-attr-type": "display-name",
    "digest-algo": "md5 sha-256",
    "digest-rfc2069": "disable",
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
    "name": "string",  # Authentication scheme name.
    "method": "option",  # Authentication methods (default = basic).
    "negotiate-ntlm": "option",  # Enable/disable negotiate authentication for NTLM (default = disable).
    "kerberos-keytab": "string",  # Kerberos keytab setting.
    "domain-controller": "string",  # Domain controller setting.
    "saml-server": "string",  # SAML configuration.
    "saml-timeout": "integer",  # SAML authentication timeout in seconds.
    "fsso-agent-for-ntlm": "string",  # FSSO agent to use for NTLM authentication.
    "require-tfa": "option",  # Enable/disable two-factor authentication (default = disable).
    "fsso-guest": "option",  # Enable/disable user fsso-guest authentication (default = disable).
    "user-cert": "option",  # Enable/disable authentication with user certificate (default = disable).
    "cert-http-header": "option",  # Enable/disable authentication with user certificate in Client-Cert HTTP header (
    "user-database": "string",  # Authentication server to contain user information; \"local-user-db\" (default) o
    "ssh-ca": "string",  # SSH CA name.
    "external-idp": "string",  # External identity provider configuration.
    "group-attr-type": "option",  # Group attribute type used to match SCIM groups (default = display-name).
    "digest-algo": "option",  # Digest Authentication Algorithms.
    "digest-rfc2069": "option",  # Enable/disable support for the deprecated RFC2069 Digest Client (no cnonce field
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Authentication scheme name.",
    "method": "Authentication methods (default = basic).",
    "negotiate-ntlm": "Enable/disable negotiate authentication for NTLM (default = disable).",
    "kerberos-keytab": "Kerberos keytab setting.",
    "domain-controller": "Domain controller setting.",
    "saml-server": "SAML configuration.",
    "saml-timeout": "SAML authentication timeout in seconds.",
    "fsso-agent-for-ntlm": "FSSO agent to use for NTLM authentication.",
    "require-tfa": "Enable/disable two-factor authentication (default = disable).",
    "fsso-guest": "Enable/disable user fsso-guest authentication (default = disable).",
    "user-cert": "Enable/disable authentication with user certificate (default = disable).",
    "cert-http-header": "Enable/disable authentication with user certificate in Client-Cert HTTP header (default = disable).",
    "user-database": "Authentication server to contain user information; \"local-user-db\" (default) or \"123\" (for LDAP).",
    "ssh-ca": "SSH CA name.",
    "external-idp": "External identity provider configuration.",
    "group-attr-type": "Group attribute type used to match SCIM groups (default = display-name).",
    "digest-algo": "Digest Authentication Algorithms.",
    "digest-rfc2069": "Enable/disable support for the deprecated RFC2069 Digest Client (no cnonce field, default = disable).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "kerberos-keytab": {"type": "string", "max_length": 35},
    "domain-controller": {"type": "string", "max_length": 35},
    "saml-server": {"type": "string", "max_length": 35},
    "saml-timeout": {"type": "integer", "min": 30, "max": 1200},
    "fsso-agent-for-ntlm": {"type": "string", "max_length": 35},
    "ssh-ca": {"type": "string", "max_length": 35},
    "external-idp": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "user-database": {
        "name": {
            "type": "string",
            "help": "Authentication server name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_METHOD = [
    "ntlm",
    "basic",
    "digest",
    "form",
    "negotiate",
    "fsso",
    "rsso",
    "ssh-publickey",
    "cert",
    "saml",
    "entra-sso",
]
VALID_BODY_NEGOTIATE_NTLM = [
    "enable",
    "disable",
]
VALID_BODY_REQUIRE_TFA = [
    "enable",
    "disable",
]
VALID_BODY_FSSO_GUEST = [
    "enable",
    "disable",
]
VALID_BODY_USER_CERT = [
    "enable",
    "disable",
]
VALID_BODY_CERT_HTTP_HEADER = [
    "enable",
    "disable",
]
VALID_BODY_GROUP_ATTR_TYPE = [
    "display-name",
    "external-id",
]
VALID_BODY_DIGEST_ALGO = [
    "md5",
    "sha-256",
]
VALID_BODY_DIGEST_RFC2069 = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_authentication_scheme_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for authentication/scheme."""
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


def validate_authentication_scheme_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new authentication/scheme object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "method" in payload:
        is_valid, error = _validate_enum_field(
            "method",
            payload["method"],
            VALID_BODY_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "negotiate-ntlm" in payload:
        is_valid, error = _validate_enum_field(
            "negotiate-ntlm",
            payload["negotiate-ntlm"],
            VALID_BODY_NEGOTIATE_NTLM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "require-tfa" in payload:
        is_valid, error = _validate_enum_field(
            "require-tfa",
            payload["require-tfa"],
            VALID_BODY_REQUIRE_TFA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fsso-guest" in payload:
        is_valid, error = _validate_enum_field(
            "fsso-guest",
            payload["fsso-guest"],
            VALID_BODY_FSSO_GUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-cert" in payload:
        is_valid, error = _validate_enum_field(
            "user-cert",
            payload["user-cert"],
            VALID_BODY_USER_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-http-header" in payload:
        is_valid, error = _validate_enum_field(
            "cert-http-header",
            payload["cert-http-header"],
            VALID_BODY_CERT_HTTP_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-attr-type",
            payload["group-attr-type"],
            VALID_BODY_GROUP_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digest-algo" in payload:
        is_valid, error = _validate_enum_field(
            "digest-algo",
            payload["digest-algo"],
            VALID_BODY_DIGEST_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digest-rfc2069" in payload:
        is_valid, error = _validate_enum_field(
            "digest-rfc2069",
            payload["digest-rfc2069"],
            VALID_BODY_DIGEST_RFC2069,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_authentication_scheme_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update authentication/scheme."""
    # Validate enum values using central function
    if "method" in payload:
        is_valid, error = _validate_enum_field(
            "method",
            payload["method"],
            VALID_BODY_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "negotiate-ntlm" in payload:
        is_valid, error = _validate_enum_field(
            "negotiate-ntlm",
            payload["negotiate-ntlm"],
            VALID_BODY_NEGOTIATE_NTLM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "require-tfa" in payload:
        is_valid, error = _validate_enum_field(
            "require-tfa",
            payload["require-tfa"],
            VALID_BODY_REQUIRE_TFA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fsso-guest" in payload:
        is_valid, error = _validate_enum_field(
            "fsso-guest",
            payload["fsso-guest"],
            VALID_BODY_FSSO_GUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-cert" in payload:
        is_valid, error = _validate_enum_field(
            "user-cert",
            payload["user-cert"],
            VALID_BODY_USER_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-http-header" in payload:
        is_valid, error = _validate_enum_field(
            "cert-http-header",
            payload["cert-http-header"],
            VALID_BODY_CERT_HTTP_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-attr-type",
            payload["group-attr-type"],
            VALID_BODY_GROUP_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digest-algo" in payload:
        is_valid, error = _validate_enum_field(
            "digest-algo",
            payload["digest-algo"],
            VALID_BODY_DIGEST_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digest-rfc2069" in payload:
        is_valid, error = _validate_enum_field(
            "digest-rfc2069",
            payload["digest-rfc2069"],
            VALID_BODY_DIGEST_RFC2069,
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
    "endpoint": "authentication/scheme",
    "category": "cmdb",
    "api_path": "authentication/scheme",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Authentication Schemes.",
    "total_fields": 18,
    "required_fields_count": 1,
    "fields_with_defaults_count": 17,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
