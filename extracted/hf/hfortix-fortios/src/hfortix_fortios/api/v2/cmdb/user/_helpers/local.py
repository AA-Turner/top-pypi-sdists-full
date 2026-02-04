"""Validation helpers for user/local - Auto-generated"""

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
    "passwd",  # User's password.
    "ldap-server",  # Name of LDAP server with which the user must authenticate.
    "radius-server",  # Name of RADIUS server with which the user must authenticate.
    "tacacs+-server",  # Name of TACACS+ server with which the user must authenticate.
    "saml-server",  # Name of SAML server with which the user must authenticate.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "id": 0,
    "status": "enable",
    "type": "password",
    "ldap-server": "",
    "radius-server": "",
    "tacacs+-server": "",
    "saml-server": "",
    "two-factor": "disable",
    "two-factor-authentication": "",
    "two-factor-notification": "",
    "fortitoken": "",
    "email-to": "",
    "sms-server": "fortiguard",
    "sms-custom-server": "",
    "sms-phone": "",
    "passwd-policy": "",
    "passwd-time": "",
    "authtimeout": 0,
    "workstation": "",
    "auth-concurrent-override": "disable",
    "auth-concurrent-value": 0,
    "ppk-identity": "",
    "qkd-profile": "",
    "username-sensitivity": "enable",
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
    "name": "string",  # Local user name.
    "id": "integer",  # User ID.
    "status": "option",  # Enable/disable allowing the local user to authenticate with the FortiGate unit.
    "type": "option",  # Authentication method.
    "passwd": "password",  # User's password.
    "ldap-server": "string",  # Name of LDAP server with which the user must authenticate.
    "radius-server": "string",  # Name of RADIUS server with which the user must authenticate.
    "tacacs+-server": "string",  # Name of TACACS+ server with which the user must authenticate.
    "saml-server": "string",  # Name of SAML server with which the user must authenticate.
    "two-factor": "option",  # Enable/disable two-factor authentication.
    "two-factor-authentication": "option",  # Authentication method by FortiToken Cloud.
    "two-factor-notification": "option",  # Notification method for user activation by FortiToken Cloud.
    "fortitoken": "string",  # Two-factor recipient's FortiToken serial number.
    "email-to": "string",  # Two-factor recipient's email address.
    "sms-server": "option",  # Send SMS through FortiGuard or other external server.
    "sms-custom-server": "string",  # Two-factor recipient's SMS server.
    "sms-phone": "string",  # Two-factor recipient's mobile phone number.
    "passwd-policy": "string",  # Password policy to apply to this user, as defined in config user password-policy
    "passwd-time": "user",  # Time of the last password update.
    "authtimeout": "integer",  # Time in minutes before the authentication timeout for a user is reached.
    "workstation": "string",  # Name of the remote user workstation, if you want to limit the user to authentica
    "auth-concurrent-override": "option",  # Enable/disable overriding the policy-auth-concurrent under config system global.
    "auth-concurrent-value": "integer",  # Maximum number of concurrent logins permitted from the same user.
    "ppk-secret": "password-3",  # IKEv2 Postquantum Preshared Key (ASCII string or hexadecimal encoded with a lead
    "ppk-identity": "string",  # IKEv2 Postquantum Preshared Key Identity.
    "qkd-profile": "string",  # Quantum Key Distribution (QKD) profile.
    "username-sensitivity": "option",  # Enable/disable case and accent sensitivity when performing username matching (ac
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Local user name.",
    "id": "User ID.",
    "status": "Enable/disable allowing the local user to authenticate with the FortiGate unit.",
    "type": "Authentication method.",
    "passwd": "User's password.",
    "ldap-server": "Name of LDAP server with which the user must authenticate.",
    "radius-server": "Name of RADIUS server with which the user must authenticate.",
    "tacacs+-server": "Name of TACACS+ server with which the user must authenticate.",
    "saml-server": "Name of SAML server with which the user must authenticate.",
    "two-factor": "Enable/disable two-factor authentication.",
    "two-factor-authentication": "Authentication method by FortiToken Cloud.",
    "two-factor-notification": "Notification method for user activation by FortiToken Cloud.",
    "fortitoken": "Two-factor recipient's FortiToken serial number.",
    "email-to": "Two-factor recipient's email address.",
    "sms-server": "Send SMS through FortiGuard or other external server.",
    "sms-custom-server": "Two-factor recipient's SMS server.",
    "sms-phone": "Two-factor recipient's mobile phone number.",
    "passwd-policy": "Password policy to apply to this user, as defined in config user password-policy.",
    "passwd-time": "Time of the last password update.",
    "authtimeout": "Time in minutes before the authentication timeout for a user is reached.",
    "workstation": "Name of the remote user workstation, if you want to limit the user to authenticate only from a particular workstation.",
    "auth-concurrent-override": "Enable/disable overriding the policy-auth-concurrent under config system global.",
    "auth-concurrent-value": "Maximum number of concurrent logins permitted from the same user.",
    "ppk-secret": "IKEv2 Postquantum Preshared Key (ASCII string or hexadecimal encoded with a leading 0x).",
    "ppk-identity": "IKEv2 Postquantum Preshared Key Identity.",
    "qkd-profile": "Quantum Key Distribution (QKD) profile.",
    "username-sensitivity": "Enable/disable case and accent sensitivity when performing username matching (accents are stripped and case is ignored when disabled).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 64},
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "ldap-server": {"type": "string", "max_length": 35},
    "radius-server": {"type": "string", "max_length": 35},
    "tacacs+-server": {"type": "string", "max_length": 35},
    "saml-server": {"type": "string", "max_length": 35},
    "fortitoken": {"type": "string", "max_length": 16},
    "email-to": {"type": "string", "max_length": 63},
    "sms-custom-server": {"type": "string", "max_length": 35},
    "sms-phone": {"type": "string", "max_length": 15},
    "passwd-policy": {"type": "string", "max_length": 35},
    "authtimeout": {"type": "integer", "min": 0, "max": 1440},
    "workstation": {"type": "string", "max_length": 35},
    "auth-concurrent-value": {"type": "integer", "min": 0, "max": 100},
    "ppk-identity": {"type": "string", "max_length": 35},
    "qkd-profile": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_TYPE = [
    "password",
    "radius",
    "tacacs+",
    "ldap",
    "saml",
]
VALID_BODY_TWO_FACTOR = [
    "disable",
    "fortitoken",
    "fortitoken-cloud",
    "email",
    "sms",
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
VALID_BODY_SMS_SERVER = [
    "fortiguard",
    "custom",
]
VALID_BODY_AUTH_CONCURRENT_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_USERNAME_SENSITIVITY = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_local_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/local."""
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


def validate_user_local_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/local object."""
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
    if "sms-server" in payload:
        is_valid, error = _validate_enum_field(
            "sms-server",
            payload["sms-server"],
            VALID_BODY_SMS_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-concurrent-override" in payload:
        is_valid, error = _validate_enum_field(
            "auth-concurrent-override",
            payload["auth-concurrent-override"],
            VALID_BODY_AUTH_CONCURRENT_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "username-sensitivity" in payload:
        is_valid, error = _validate_enum_field(
            "username-sensitivity",
            payload["username-sensitivity"],
            VALID_BODY_USERNAME_SENSITIVITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_local_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/local."""
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
    if "sms-server" in payload:
        is_valid, error = _validate_enum_field(
            "sms-server",
            payload["sms-server"],
            VALID_BODY_SMS_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-concurrent-override" in payload:
        is_valid, error = _validate_enum_field(
            "auth-concurrent-override",
            payload["auth-concurrent-override"],
            VALID_BODY_AUTH_CONCURRENT_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "username-sensitivity" in payload:
        is_valid, error = _validate_enum_field(
            "username-sensitivity",
            payload["username-sensitivity"],
            VALID_BODY_USERNAME_SENSITIVITY,
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
    "endpoint": "user/local",
    "category": "cmdb",
    "api_path": "user/local",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure local users.",
    "total_fields": 27,
    "required_fields_count": 5,
    "fields_with_defaults_count": 25,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
