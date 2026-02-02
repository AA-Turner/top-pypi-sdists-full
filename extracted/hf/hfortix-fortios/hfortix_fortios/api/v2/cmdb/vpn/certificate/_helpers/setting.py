"""Validation helpers for vpn/certificate/setting - Auto-generated"""

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
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "ocsp-status": "disable",
    "ocsp-option": "server",
    "proxy": "",
    "proxy-port": 8080,
    "proxy-username": "",
    "source-ip": "",
    "ocsp-default-server": "",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
    "check-ca-cert": "enable",
    "check-ca-chain": "disable",
    "subject-match": "substring",
    "subject-set": "subset",
    "cn-match": "substring",
    "cn-allow-multi": "enable",
    "strict-ocsp-check": "disable",
    "ssl-min-proto-version": "default",
    "cmp-save-extra-certs": "disable",
    "cmp-key-usage-checking": "enable",
    "cert-expire-warning": 14,
    "certname-rsa1024": "Fortinet_SSL_RSA1024",
    "certname-rsa2048": "Fortinet_SSL_RSA2048",
    "certname-rsa4096": "Fortinet_SSL_RSA4096",
    "certname-dsa1024": "Fortinet_SSL_DSA1024",
    "certname-dsa2048": "Fortinet_SSL_DSA2048",
    "certname-ecdsa256": "Fortinet_SSL_ECDSA256",
    "certname-ecdsa384": "Fortinet_SSL_ECDSA384",
    "certname-ecdsa521": "Fortinet_SSL_ECDSA521",
    "certname-ed25519": "Fortinet_SSL_ED25519",
    "certname-ed448": "Fortinet_SSL_ED448",
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
    "ocsp-status": "option",  # Enable/disable receiving certificates using the OCSP.
    "ocsp-option": "option",  # Specify whether the OCSP URL is from certificate or configur
    "proxy": "string",  # Proxy server FQDN or IP for OCSP/CA queries during certifica
    "proxy-port": "integer",  # Proxy server port (1 - 65535, default = 8080).
    "proxy-username": "string",  # Proxy server user name.
    "proxy-password": "password",  # Proxy server password.
    "source-ip": "string",  # Source IP address for dynamic AIA and OCSP queries.
    "ocsp-default-server": "string",  # Default OCSP server.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "check-ca-cert": "option",  # Enable/disable verification of the user certificate and pass
    "check-ca-chain": "option",  # Enable/disable verification of the entire certificate chain 
    "subject-match": "option",  # When searching for a matching certificate, control how to do
    "subject-set": "option",  # When searching for a matching certificate, control how to do
    "cn-match": "option",  # When searching for a matching certificate, control how to do
    "cn-allow-multi": "option",  # When searching for a matching certificate, allow multiple CN
    "crl-verification": "string",  # CRL verification options.
    "strict-ocsp-check": "option",  # Enable/disable strict mode OCSP checking.
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (
    "cmp-save-extra-certs": "option",  # Enable/disable saving extra certificates in CMP mode (defaul
    "cmp-key-usage-checking": "option",  # Enable/disable server certificate key usage checking in CMP 
    "cert-expire-warning": "integer",  # Number of days before a certificate expires to send a warnin
    "certname-rsa1024": "string",  # 1024 bit RSA key certificate for re-signing server certifica
    "certname-rsa2048": "string",  # 2048 bit RSA key certificate for re-signing server certifica
    "certname-rsa4096": "string",  # 4096 bit RSA key certificate for re-signing server certifica
    "certname-dsa1024": "string",  # 1024 bit DSA key certificate for re-signing server certifica
    "certname-dsa2048": "string",  # 2048 bit DSA key certificate for re-signing server certifica
    "certname-ecdsa256": "string",  # 256 bit ECDSA key certificate for re-signing server certific
    "certname-ecdsa384": "string",  # 384 bit ECDSA key certificate for re-signing server certific
    "certname-ecdsa521": "string",  # 521 bit ECDSA key certificate for re-signing server certific
    "certname-ed25519": "string",  # 253 bit EdDSA key certificate for re-signing server certific
    "certname-ed448": "string",  # 456 bit EdDSA key certificate for re-signing server certific
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "ocsp-status": "Enable/disable receiving certificates using the OCSP.",
    "ocsp-option": "Specify whether the OCSP URL is from certificate or configured OCSP server.",
    "proxy": "Proxy server FQDN or IP for OCSP/CA queries during certificate verification.",
    "proxy-port": "Proxy server port (1 - 65535, default = 8080).",
    "proxy-username": "Proxy server user name.",
    "proxy-password": "Proxy server password.",
    "source-ip": "Source IP address for dynamic AIA and OCSP queries.",
    "ocsp-default-server": "Default OCSP server.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "check-ca-cert": "Enable/disable verification of the user certificate and pass authentication if any CA in the chain is trusted (default = enable).",
    "check-ca-chain": "Enable/disable verification of the entire certificate chain and pass authentication only if the chain is complete and all of the CAs in the chain are trusted (default = disable).",
    "subject-match": "When searching for a matching certificate, control how to do RDN value matching with certificate subject name (default = substring).",
    "subject-set": "When searching for a matching certificate, control how to do RDN set matching with certificate subject name (default = subset).",
    "cn-match": "When searching for a matching certificate, control how to do CN value matching with certificate subject name (default = substring).",
    "cn-allow-multi": "When searching for a matching certificate, allow multiple CN fields in certificate subject name (default = enable).",
    "crl-verification": "CRL verification options.",
    "strict-ocsp-check": "Enable/disable strict mode OCSP checking.",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "cmp-save-extra-certs": "Enable/disable saving extra certificates in CMP mode (default = disable).",
    "cmp-key-usage-checking": "Enable/disable server certificate key usage checking in CMP mode (default = enable).",
    "cert-expire-warning": "Number of days before a certificate expires to send a warning. Set to 0 to disable sending of the warning (0 - 100, default = 14).",
    "certname-rsa1024": "1024 bit RSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-rsa2048": "2048 bit RSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-rsa4096": "4096 bit RSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-dsa1024": "1024 bit DSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-dsa2048": "2048 bit DSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-ecdsa256": "256 bit ECDSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-ecdsa384": "384 bit ECDSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-ecdsa521": "521 bit ECDSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-ed25519": "253 bit EdDSA key certificate for re-signing server certificates for SSL inspection.",
    "certname-ed448": "456 bit EdDSA key certificate for re-signing server certificates for SSL inspection.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "proxy": {"type": "string", "max_length": 127},
    "proxy-port": {"type": "integer", "min": 1, "max": 65535},
    "proxy-username": {"type": "string", "max_length": 63},
    "source-ip": {"type": "string", "max_length": 63},
    "ocsp-default-server": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "cert-expire-warning": {"type": "integer", "min": 0, "max": 100},
    "certname-rsa1024": {"type": "string", "max_length": 35},
    "certname-rsa2048": {"type": "string", "max_length": 35},
    "certname-rsa4096": {"type": "string", "max_length": 35},
    "certname-dsa1024": {"type": "string", "max_length": 35},
    "certname-dsa2048": {"type": "string", "max_length": 35},
    "certname-ecdsa256": {"type": "string", "max_length": 35},
    "certname-ecdsa384": {"type": "string", "max_length": 35},
    "certname-ecdsa521": {"type": "string", "max_length": 35},
    "certname-ed25519": {"type": "string", "max_length": 35},
    "certname-ed448": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "crl-verification": {
        "expiry": {
            "type": "option",
            "help": "CRL verification option when CRL is expired (default = ignore).",
            "default": "ignore",
            "options": ["ignore", "revoke"],
        },
        "leaf-crl-absence": {
            "type": "option",
            "help": "CRL verification option when leaf CRL is absent (default = ignore).",
            "default": "ignore",
            "options": ["ignore", "revoke"],
        },
        "chain-crl-absence": {
            "type": "option",
            "help": "CRL verification option when CRL of any certificate in chain is absent (default = ignore).",
            "default": "ignore",
            "options": ["ignore", "revoke"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_OCSP_STATUS = [
    "enable",
    "mandatory",
    "disable",
]
VALID_BODY_OCSP_OPTION = [
    "certificate",
    "server",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_CHECK_CA_CERT = [
    "enable",
    "disable",
]
VALID_BODY_CHECK_CA_CHAIN = [
    "enable",
    "disable",
]
VALID_BODY_SUBJECT_MATCH = [
    "substring",
    "value",
]
VALID_BODY_SUBJECT_SET = [
    "subset",
    "superset",
]
VALID_BODY_CN_MATCH = [
    "substring",
    "value",
]
VALID_BODY_CN_ALLOW_MULTI = [
    "disable",
    "enable",
]
VALID_BODY_STRICT_OCSP_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_CMP_SAVE_EXTRA_CERTS = [
    "enable",
    "disable",
]
VALID_BODY_CMP_KEY_USAGE_CHECKING = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_vpn_certificate_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/certificate/setting."""
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


def validate_vpn_certificate_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/certificate/setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ocsp-status" in payload:
        is_valid, error = _validate_enum_field(
            "ocsp-status",
            payload["ocsp-status"],
            VALID_BODY_OCSP_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ocsp-option" in payload:
        is_valid, error = _validate_enum_field(
            "ocsp-option",
            payload["ocsp-option"],
            VALID_BODY_OCSP_OPTION,
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
    if "check-ca-cert" in payload:
        is_valid, error = _validate_enum_field(
            "check-ca-cert",
            payload["check-ca-cert"],
            VALID_BODY_CHECK_CA_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-ca-chain" in payload:
        is_valid, error = _validate_enum_field(
            "check-ca-chain",
            payload["check-ca-chain"],
            VALID_BODY_CHECK_CA_CHAIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subject-match" in payload:
        is_valid, error = _validate_enum_field(
            "subject-match",
            payload["subject-match"],
            VALID_BODY_SUBJECT_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subject-set" in payload:
        is_valid, error = _validate_enum_field(
            "subject-set",
            payload["subject-set"],
            VALID_BODY_SUBJECT_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cn-match" in payload:
        is_valid, error = _validate_enum_field(
            "cn-match",
            payload["cn-match"],
            VALID_BODY_CN_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cn-allow-multi" in payload:
        is_valid, error = _validate_enum_field(
            "cn-allow-multi",
            payload["cn-allow-multi"],
            VALID_BODY_CN_ALLOW_MULTI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-ocsp-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-ocsp-check",
            payload["strict-ocsp-check"],
            VALID_BODY_STRICT_OCSP_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmp-save-extra-certs" in payload:
        is_valid, error = _validate_enum_field(
            "cmp-save-extra-certs",
            payload["cmp-save-extra-certs"],
            VALID_BODY_CMP_SAVE_EXTRA_CERTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmp-key-usage-checking" in payload:
        is_valid, error = _validate_enum_field(
            "cmp-key-usage-checking",
            payload["cmp-key-usage-checking"],
            VALID_BODY_CMP_KEY_USAGE_CHECKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_vpn_certificate_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/certificate/setting."""
    # Validate enum values using central function
    if "ocsp-status" in payload:
        is_valid, error = _validate_enum_field(
            "ocsp-status",
            payload["ocsp-status"],
            VALID_BODY_OCSP_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ocsp-option" in payload:
        is_valid, error = _validate_enum_field(
            "ocsp-option",
            payload["ocsp-option"],
            VALID_BODY_OCSP_OPTION,
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
    if "check-ca-cert" in payload:
        is_valid, error = _validate_enum_field(
            "check-ca-cert",
            payload["check-ca-cert"],
            VALID_BODY_CHECK_CA_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-ca-chain" in payload:
        is_valid, error = _validate_enum_field(
            "check-ca-chain",
            payload["check-ca-chain"],
            VALID_BODY_CHECK_CA_CHAIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subject-match" in payload:
        is_valid, error = _validate_enum_field(
            "subject-match",
            payload["subject-match"],
            VALID_BODY_SUBJECT_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subject-set" in payload:
        is_valid, error = _validate_enum_field(
            "subject-set",
            payload["subject-set"],
            VALID_BODY_SUBJECT_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cn-match" in payload:
        is_valid, error = _validate_enum_field(
            "cn-match",
            payload["cn-match"],
            VALID_BODY_CN_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cn-allow-multi" in payload:
        is_valid, error = _validate_enum_field(
            "cn-allow-multi",
            payload["cn-allow-multi"],
            VALID_BODY_CN_ALLOW_MULTI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-ocsp-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-ocsp-check",
            payload["strict-ocsp-check"],
            VALID_BODY_STRICT_OCSP_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmp-save-extra-certs" in payload:
        is_valid, error = _validate_enum_field(
            "cmp-save-extra-certs",
            payload["cmp-save-extra-certs"],
            VALID_BODY_CMP_SAVE_EXTRA_CERTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cmp-key-usage-checking" in payload:
        is_valid, error = _validate_enum_field(
            "cmp-key-usage-checking",
            payload["cmp-key-usage-checking"],
            VALID_BODY_CMP_KEY_USAGE_CHECKING,
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
    "endpoint": "vpn/certificate/setting",
    "category": "cmdb",
    "api_path": "vpn.certificate/setting",
    "help": "VPN certificate setting.",
    "total_fields": 33,
    "required_fields_count": 1,
    "fields_with_defaults_count": 31,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
