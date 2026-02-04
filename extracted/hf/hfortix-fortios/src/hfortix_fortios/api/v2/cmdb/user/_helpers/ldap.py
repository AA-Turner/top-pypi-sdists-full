"""Validation helpers for user/ldap - Auto-generated"""

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
    "server",  # LDAP server CN domain name or IP.
    "dn",  # Distinguished name used to look up entries on the LDAP server.
    "username",  # Username (full DN) for initial binding.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "server": "",
    "secondary-server": "",
    "tertiary-server": "",
    "status-ttl": 300,
    "server-identity-check": "enable",
    "source-ip": "",
    "source-ip-interface": "",
    "source-port": 0,
    "cnid": "cn",
    "dn": "",
    "type": "simple",
    "two-factor": "disable",
    "two-factor-authentication": "",
    "two-factor-notification": "",
    "two-factor-filter": "",
    "username": "",
    "group-member-check": "user-attr",
    "group-search-base": "",
    "group-object-filter": "(\u0026(objectcategory=group)(member=*))",
    "group-filter": "",
    "secure": "disable",
    "ssl-min-proto-version": "default",
    "ca-cert": "",
    "port": 389,
    "password-expiry-warning": "disable",
    "password-renewal": "disable",
    "member-attr": "memberOf",
    "account-key-processing": "same",
    "account-key-cert-field": "othername",
    "account-key-filter": "(\u0026(userPrincipalName=%s)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))",
    "search-type": "",
    "client-cert-auth": "disable",
    "client-cert": "",
    "obtain-user-info": "enable",
    "user-info-exchange-server": "",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
    "antiphish": "disable",
    "password-attr": "userPassword",
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
    "name": "string",  # LDAP server entry name.
    "server": "string",  # LDAP server CN domain name or IP.
    "secondary-server": "string",  # Secondary LDAP server CN domain name or IP.
    "tertiary-server": "string",  # Tertiary LDAP server CN domain name or IP.
    "status-ttl": "integer",  # Time for which server reachability is cached so that when a server is unreachabl
    "server-identity-check": "option",  # Enable/disable LDAP server identity check (verify server domain name/IP address 
    "source-ip": "string",  # FortiGate IP address to be used for communication with the LDAP server.
    "source-ip-interface": "string",  # Source interface for communication with the LDAP server.
    "source-port": "integer",  # Source port to be used for communication with the LDAP server.
    "cnid": "string",  # Common name identifier for the LDAP server. The common name identifier for most 
    "dn": "string",  # Distinguished name used to look up entries on the LDAP server.
    "type": "option",  # Authentication type for LDAP searches.
    "two-factor": "option",  # Enable/disable two-factor authentication.
    "two-factor-authentication": "option",  # Authentication method by FortiToken Cloud.
    "two-factor-notification": "option",  # Notification method for user activation by FortiToken Cloud.
    "two-factor-filter": "string",  # Filter used to synchronize users to FortiToken Cloud.
    "username": "string",  # Username (full DN) for initial binding.
    "password": "password",  # Password for initial binding.
    "group-member-check": "option",  # Group member checking methods.
    "group-search-base": "string",  # Search base used for group searching.
    "group-object-filter": "string",  # Filter used for group searching.
    "group-filter": "string",  # Filter used for group matching.
    "secure": "option",  # Port to be used for authentication.
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (default is to follow
    "ca-cert": "string",  # CA certificate name.
    "port": "integer",  # Port to be used for communication with the LDAP server (default = 389).
    "password-expiry-warning": "option",  # Enable/disable password expiry warnings.
    "password-renewal": "option",  # Enable/disable online password renewal.
    "member-attr": "string",  # Name of attribute from which to get group membership.
    "account-key-processing": "option",  # Account key processing operation. The FortiGate will keep either the whole domai
    "account-key-cert-field": "option",  # Define subject identity field in certificate for user access right checking.
    "account-key-filter": "string",  # Account key filter, using the UPN as the search filter.
    "search-type": "option",  # Search type.
    "client-cert-auth": "option",  # Enable/disable using client certificate for TLS authentication.
    "client-cert": "string",  # Client certificate name.
    "obtain-user-info": "option",  # Enable/disable obtaining of user information.
    "user-info-exchange-server": "string",  # MS Exchange server from which to fetch user information.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "antiphish": "option",  # Enable/disable AntiPhishing credential backend.
    "password-attr": "string",  # Name of attribute to get password hash.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "LDAP server entry name.",
    "server": "LDAP server CN domain name or IP.",
    "secondary-server": "Secondary LDAP server CN domain name or IP.",
    "tertiary-server": "Tertiary LDAP server CN domain name or IP.",
    "status-ttl": "Time for which server reachability is cached so that when a server is unreachable, it will not be retried for at least this period of time (0 = cache disabled, default = 300).",
    "server-identity-check": "Enable/disable LDAP server identity check (verify server domain name/IP address against the server certificate).",
    "source-ip": "FortiGate IP address to be used for communication with the LDAP server.",
    "source-ip-interface": "Source interface for communication with the LDAP server.",
    "source-port": "Source port to be used for communication with the LDAP server.",
    "cnid": "Common name identifier for the LDAP server. The common name identifier for most LDAP servers is \"cn\".",
    "dn": "Distinguished name used to look up entries on the LDAP server.",
    "type": "Authentication type for LDAP searches.",
    "two-factor": "Enable/disable two-factor authentication.",
    "two-factor-authentication": "Authentication method by FortiToken Cloud.",
    "two-factor-notification": "Notification method for user activation by FortiToken Cloud.",
    "two-factor-filter": "Filter used to synchronize users to FortiToken Cloud.",
    "username": "Username (full DN) for initial binding.",
    "password": "Password for initial binding.",
    "group-member-check": "Group member checking methods.",
    "group-search-base": "Search base used for group searching.",
    "group-object-filter": "Filter used for group searching.",
    "group-filter": "Filter used for group matching.",
    "secure": "Port to be used for authentication.",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "ca-cert": "CA certificate name.",
    "port": "Port to be used for communication with the LDAP server (default = 389).",
    "password-expiry-warning": "Enable/disable password expiry warnings.",
    "password-renewal": "Enable/disable online password renewal.",
    "member-attr": "Name of attribute from which to get group membership.",
    "account-key-processing": "Account key processing operation. The FortiGate will keep either the whole domain or strip the domain from the subject identity.",
    "account-key-cert-field": "Define subject identity field in certificate for user access right checking.",
    "account-key-filter": "Account key filter, using the UPN as the search filter.",
    "search-type": "Search type.",
    "client-cert-auth": "Enable/disable using client certificate for TLS authentication.",
    "client-cert": "Client certificate name.",
    "obtain-user-info": "Enable/disable obtaining of user information.",
    "user-info-exchange-server": "MS Exchange server from which to fetch user information.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "antiphish": "Enable/disable AntiPhishing credential backend.",
    "password-attr": "Name of attribute to get password hash.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "server": {"type": "string", "max_length": 63},
    "secondary-server": {"type": "string", "max_length": 63},
    "tertiary-server": {"type": "string", "max_length": 63},
    "status-ttl": {"type": "integer", "min": 0, "max": 600},
    "source-ip": {"type": "string", "max_length": 63},
    "source-ip-interface": {"type": "string", "max_length": 15},
    "source-port": {"type": "integer", "min": 0, "max": 65535},
    "cnid": {"type": "string", "max_length": 20},
    "dn": {"type": "string", "max_length": 511},
    "two-factor-filter": {"type": "string", "max_length": 2047},
    "username": {"type": "string", "max_length": 511},
    "group-search-base": {"type": "string", "max_length": 511},
    "group-object-filter": {"type": "string", "max_length": 2047},
    "group-filter": {"type": "string", "max_length": 2047},
    "ca-cert": {"type": "string", "max_length": 79},
    "port": {"type": "integer", "min": 1, "max": 65535},
    "member-attr": {"type": "string", "max_length": 63},
    "account-key-filter": {"type": "string", "max_length": 2047},
    "client-cert": {"type": "string", "max_length": 79},
    "user-info-exchange-server": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "password-attr": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_SERVER_IDENTITY_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_TYPE = [
    "simple",
    "anonymous",
    "regular",
]
VALID_BODY_TWO_FACTOR = [
    "disable",
    "fortitoken-cloud",
]
VALID_BODY_TWO_FACTOR_AUTHENTICATION = [
    "fortitoken",
    "email",
    "sms",
]
VALID_BODY_TWO_FACTOR_NOTIFICATION = [
    "email",
    "sms",
]
VALID_BODY_GROUP_MEMBER_CHECK = [
    "user-attr",
    "group-object",
    "posix-group-object",
]
VALID_BODY_SECURE = [
    "disable",
    "starttls",
    "ldaps",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_PASSWORD_EXPIRY_WARNING = [
    "enable",
    "disable",
]
VALID_BODY_PASSWORD_RENEWAL = [
    "enable",
    "disable",
]
VALID_BODY_ACCOUNT_KEY_PROCESSING = [
    "same",
    "strip",
]
VALID_BODY_ACCOUNT_KEY_CERT_FIELD = [
    "othername",
    "rfc822name",
    "dnsname",
    "cn",
]
VALID_BODY_SEARCH_TYPE = [
    "recursive",
]
VALID_BODY_CLIENT_CERT_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_OBTAIN_USER_INFO = [
    "enable",
    "disable",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_ANTIPHISH = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_ldap_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/ldap."""
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


def validate_user_ldap_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/ldap object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
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
    if "two-factor-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "two-factor-authentication",
            payload["two-factor-authentication"],
            VALID_BODY_TWO_FACTOR_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "two-factor-notification" in payload:
        is_valid, error = _validate_enum_field(
            "two-factor-notification",
            payload["two-factor-notification"],
            VALID_BODY_TWO_FACTOR_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-member-check" in payload:
        is_valid, error = _validate_enum_field(
            "group-member-check",
            payload["group-member-check"],
            VALID_BODY_GROUP_MEMBER_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secure" in payload:
        is_valid, error = _validate_enum_field(
            "secure",
            payload["secure"],
            VALID_BODY_SECURE,
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
    if "password-expiry-warning" in payload:
        is_valid, error = _validate_enum_field(
            "password-expiry-warning",
            payload["password-expiry-warning"],
            VALID_BODY_PASSWORD_EXPIRY_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password-renewal" in payload:
        is_valid, error = _validate_enum_field(
            "password-renewal",
            payload["password-renewal"],
            VALID_BODY_PASSWORD_RENEWAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-processing" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-processing",
            payload["account-key-processing"],
            VALID_BODY_ACCOUNT_KEY_PROCESSING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-cert-field" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-cert-field",
            payload["account-key-cert-field"],
            VALID_BODY_ACCOUNT_KEY_CERT_FIELD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "search-type" in payload:
        is_valid, error = _validate_enum_field(
            "search-type",
            payload["search-type"],
            VALID_BODY_SEARCH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert-auth",
            payload["client-cert-auth"],
            VALID_BODY_CLIENT_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "obtain-user-info" in payload:
        is_valid, error = _validate_enum_field(
            "obtain-user-info",
            payload["obtain-user-info"],
            VALID_BODY_OBTAIN_USER_INFO,
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
    if "antiphish" in payload:
        is_valid, error = _validate_enum_field(
            "antiphish",
            payload["antiphish"],
            VALID_BODY_ANTIPHISH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_ldap_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/ldap."""
    # Validate enum values using central function
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
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
    if "two-factor-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "two-factor-authentication",
            payload["two-factor-authentication"],
            VALID_BODY_TWO_FACTOR_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "two-factor-notification" in payload:
        is_valid, error = _validate_enum_field(
            "two-factor-notification",
            payload["two-factor-notification"],
            VALID_BODY_TWO_FACTOR_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-member-check" in payload:
        is_valid, error = _validate_enum_field(
            "group-member-check",
            payload["group-member-check"],
            VALID_BODY_GROUP_MEMBER_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secure" in payload:
        is_valid, error = _validate_enum_field(
            "secure",
            payload["secure"],
            VALID_BODY_SECURE,
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
    if "password-expiry-warning" in payload:
        is_valid, error = _validate_enum_field(
            "password-expiry-warning",
            payload["password-expiry-warning"],
            VALID_BODY_PASSWORD_EXPIRY_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password-renewal" in payload:
        is_valid, error = _validate_enum_field(
            "password-renewal",
            payload["password-renewal"],
            VALID_BODY_PASSWORD_RENEWAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-processing" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-processing",
            payload["account-key-processing"],
            VALID_BODY_ACCOUNT_KEY_PROCESSING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "account-key-cert-field" in payload:
        is_valid, error = _validate_enum_field(
            "account-key-cert-field",
            payload["account-key-cert-field"],
            VALID_BODY_ACCOUNT_KEY_CERT_FIELD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "search-type" in payload:
        is_valid, error = _validate_enum_field(
            "search-type",
            payload["search-type"],
            VALID_BODY_SEARCH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert-auth",
            payload["client-cert-auth"],
            VALID_BODY_CLIENT_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "obtain-user-info" in payload:
        is_valid, error = _validate_enum_field(
            "obtain-user-info",
            payload["obtain-user-info"],
            VALID_BODY_OBTAIN_USER_INFO,
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
    if "antiphish" in payload:
        is_valid, error = _validate_enum_field(
            "antiphish",
            payload["antiphish"],
            VALID_BODY_ANTIPHISH,
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
    "endpoint": "user/ldap",
    "category": "cmdb",
    "api_path": "user/ldap",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure LDAP server entries.",
    "total_fields": 42,
    "required_fields_count": 4,
    "fields_with_defaults_count": 41,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
