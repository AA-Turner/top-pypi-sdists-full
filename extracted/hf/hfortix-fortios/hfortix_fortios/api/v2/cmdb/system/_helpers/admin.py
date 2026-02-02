"""Validation helpers for system/admin - Auto-generated"""

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
    "remote-group",  # User group name used for remote auth.
    "password",  # Admin user password.
    "peer-group",  # Name of peer group defined under config user group which has PKI members. Used for peer certificate authentication (for HTTPS admin access).
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "remote-auth": "disable",
    "remote-group": "",
    "wildcard": "disable",
    "peer-auth": "disable",
    "peer-group": "",
    "trusthost1": "0.0.0.0 0.0.0.0",
    "trusthost2": "0.0.0.0 0.0.0.0",
    "trusthost3": "0.0.0.0 0.0.0.0",
    "trusthost4": "0.0.0.0 0.0.0.0",
    "trusthost5": "0.0.0.0 0.0.0.0",
    "trusthost6": "0.0.0.0 0.0.0.0",
    "trusthost7": "0.0.0.0 0.0.0.0",
    "trusthost8": "0.0.0.0 0.0.0.0",
    "trusthost9": "0.0.0.0 0.0.0.0",
    "trusthost10": "0.0.0.0 0.0.0.0",
    "ip6-trusthost1": "::/0",
    "ip6-trusthost2": "::/0",
    "ip6-trusthost3": "::/0",
    "ip6-trusthost4": "::/0",
    "ip6-trusthost5": "::/0",
    "ip6-trusthost6": "::/0",
    "ip6-trusthost7": "::/0",
    "ip6-trusthost8": "::/0",
    "ip6-trusthost9": "::/0",
    "ip6-trusthost10": "::/0",
    "accprofile": "",
    "allow-remove-admin-session": "enable",
    "ssh-public-key1": "",
    "ssh-public-key2": "",
    "ssh-public-key3": "",
    "ssh-certificate": "",
    "schedule": "",
    "accprofile-override": "disable",
    "vdom-override": "disable",
    "password-expire": "0000-00-00 00:00:00",
    "force-password-change": "disable",
    "two-factor": "disable",
    "two-factor-authentication": "",
    "two-factor-notification": "",
    "fortitoken": "",
    "email-to": "",
    "sms-server": "fortiguard",
    "sms-custom-server": "",
    "sms-phone": "",
    "guest-auth": "disable",
    "guest-lang": "",
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
    "name": "string",  # User name.
    "vdom": "string",  # Virtual domain(s) that the administrator can access.
    "remote-auth": "option",  # Enable/disable authentication using a remote RADIUS, LDAP, o
    "remote-group": "string",  # User group name used for remote auth.
    "wildcard": "option",  # Enable/disable wildcard RADIUS authentication.
    "password": "password-2",  # Admin user password.
    "peer-auth": "option",  # Set to enable peer certificate authentication (for HTTPS adm
    "peer-group": "string",  # Name of peer group defined under config user group which has
    "trusthost1": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost2": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost3": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost4": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost5": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost6": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost7": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost8": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost9": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "trusthost10": "ipv4-classnet",  # Any IPv4 address or subnet address and netmask from which th
    "ip6-trusthost1": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost2": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost3": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost4": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost5": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost6": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost7": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost8": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost9": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "ip6-trusthost10": "ipv6-prefix",  # Any IPv6 address from which the administrator can connect to
    "accprofile": "string",  # Access profile for this administrator. Access profiles contr
    "allow-remove-admin-session": "option",  # Enable/disable allow admin session to be removed by privileg
    "comments": "var-string",  # Comment.
    "ssh-public-key1": "user",  # Public key of an SSH client. The client is authenticated wit
    "ssh-public-key2": "user",  # Public key of an SSH client. The client is authenticated wit
    "ssh-public-key3": "user",  # Public key of an SSH client. The client is authenticated wit
    "ssh-certificate": "string",  # Select the certificate to be used by the FortiGate for authe
    "schedule": "string",  # Firewall schedule used to restrict when the administrator ca
    "accprofile-override": "option",  # Enable to use the name of an access profile provided by the 
    "vdom-override": "option",  # Enable to use the names of VDOMs provided by the remote auth
    "password-expire": "datetime",  # Password expire time.
    "force-password-change": "option",  # Enable/disable force password change on next login.
    "two-factor": "option",  # Enable/disable two-factor authentication.
    "two-factor-authentication": "option",  # Authentication method by FortiToken Cloud.
    "two-factor-notification": "option",  # Notification method for user activation by FortiToken Cloud.
    "fortitoken": "string",  # This administrator's FortiToken serial number.
    "email-to": "string",  # This administrator's email address.
    "sms-server": "option",  # Send SMS messages using the FortiGuard SMS server or a custo
    "sms-custom-server": "string",  # Custom SMS server to send SMS messages to.
    "sms-phone": "string",  # Phone number on which the administrator receives SMS message
    "guest-auth": "option",  # Enable/disable guest authentication.
    "guest-usergroups": "string",  # Select guest user groups.
    "guest-lang": "string",  # Guest management portal language.
    "status": "key",  # print admin status information
    "list": "key",  # print admin list information
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "User name.",
    "vdom": "Virtual domain(s) that the administrator can access.",
    "remote-auth": "Enable/disable authentication using a remote RADIUS, LDAP, or TACACS+ server.",
    "remote-group": "User group name used for remote auth.",
    "wildcard": "Enable/disable wildcard RADIUS authentication.",
    "password": "Admin user password.",
    "peer-auth": "Set to enable peer certificate authentication (for HTTPS admin access).",
    "peer-group": "Name of peer group defined under config user group which has PKI members. Used for peer certificate authentication (for HTTPS admin access).",
    "trusthost1": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost2": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost3": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost4": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost5": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost6": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost7": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost8": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost9": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "trusthost10": "Any IPv4 address or subnet address and netmask from which the administrator can connect to the FortiGate unit. Default allows access from any IPv4 address.",
    "ip6-trusthost1": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost2": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost3": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost4": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost5": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost6": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost7": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost8": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost9": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "ip6-trusthost10": "Any IPv6 address from which the administrator can connect to the FortiGate unit. Default allows access from any IPv6 address.",
    "accprofile": "Access profile for this administrator. Access profiles control administrator access to FortiGate features.",
    "allow-remove-admin-session": "Enable/disable allow admin session to be removed by privileged admin users.",
    "comments": "Comment.",
    "ssh-public-key1": "Public key of an SSH client. The client is authenticated without being asked for credentials. Create the public-private key pair in the SSH client application.",
    "ssh-public-key2": "Public key of an SSH client. The client is authenticated without being asked for credentials. Create the public-private key pair in the SSH client application.",
    "ssh-public-key3": "Public key of an SSH client. The client is authenticated without being asked for credentials. Create the public-private key pair in the SSH client application.",
    "ssh-certificate": "Select the certificate to be used by the FortiGate for authentication with an SSH client.",
    "schedule": "Firewall schedule used to restrict when the administrator can log in. No schedule means no restrictions.",
    "accprofile-override": "Enable to use the name of an access profile provided by the remote authentication server to control the FortiGate features that this administrator can access.",
    "vdom-override": "Enable to use the names of VDOMs provided by the remote authentication server to control the VDOMs that this administrator can access.",
    "password-expire": "Password expire time.",
    "force-password-change": "Enable/disable force password change on next login.",
    "two-factor": "Enable/disable two-factor authentication.",
    "two-factor-authentication": "Authentication method by FortiToken Cloud.",
    "two-factor-notification": "Notification method for user activation by FortiToken Cloud.",
    "fortitoken": "This administrator's FortiToken serial number.",
    "email-to": "This administrator's email address.",
    "sms-server": "Send SMS messages using the FortiGuard SMS server or a custom server.",
    "sms-custom-server": "Custom SMS server to send SMS messages to.",
    "sms-phone": "Phone number on which the administrator receives SMS messages.",
    "guest-auth": "Enable/disable guest authentication.",
    "guest-usergroups": "Select guest user groups.",
    "guest-lang": "Guest management portal language.",
    "status": "print admin status information",
    "list": "print admin list information",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 64},
    "remote-group": {"type": "string", "max_length": 35},
    "peer-group": {"type": "string", "max_length": 35},
    "accprofile": {"type": "string", "max_length": 35},
    "ssh-certificate": {"type": "string", "max_length": 35},
    "schedule": {"type": "string", "max_length": 35},
    "fortitoken": {"type": "string", "max_length": 16},
    "email-to": {"type": "string", "max_length": 63},
    "sms-custom-server": {"type": "string", "max_length": 35},
    "sms-phone": {"type": "string", "max_length": 15},
    "guest-lang": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "vdom": {
        "name": {
            "type": "string",
            "help": "Virtual domain name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "guest-usergroups": {
        "name": {
            "type": "string",
            "help": "Select guest user groups.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_REMOTE_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_WILDCARD = [
    "enable",
    "disable",
]
VALID_BODY_PEER_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_REMOVE_ADMIN_SESSION = [
    "enable",
    "disable",
]
VALID_BODY_ACCPROFILE_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_VDOM_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_FORCE_PASSWORD_CHANGE = [
    "enable",
    "disable",
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
VALID_BODY_GUEST_AUTH = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_admin_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/admin."""
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


def validate_system_admin_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/admin object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "remote-auth" in payload:
        is_valid, error = _validate_enum_field(
            "remote-auth",
            payload["remote-auth"],
            VALID_BODY_REMOTE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wildcard" in payload:
        is_valid, error = _validate_enum_field(
            "wildcard",
            payload["wildcard"],
            VALID_BODY_WILDCARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-auth" in payload:
        is_valid, error = _validate_enum_field(
            "peer-auth",
            payload["peer-auth"],
            VALID_BODY_PEER_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-remove-admin-session" in payload:
        is_valid, error = _validate_enum_field(
            "allow-remove-admin-session",
            payload["allow-remove-admin-session"],
            VALID_BODY_ALLOW_REMOVE_ADMIN_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "accprofile-override" in payload:
        is_valid, error = _validate_enum_field(
            "accprofile-override",
            payload["accprofile-override"],
            VALID_BODY_ACCPROFILE_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vdom-override" in payload:
        is_valid, error = _validate_enum_field(
            "vdom-override",
            payload["vdom-override"],
            VALID_BODY_VDOM_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "force-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "force-password-change",
            payload["force-password-change"],
            VALID_BODY_FORCE_PASSWORD_CHANGE,
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
    if "guest-auth" in payload:
        is_valid, error = _validate_enum_field(
            "guest-auth",
            payload["guest-auth"],
            VALID_BODY_GUEST_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_admin_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/admin."""
    # Validate enum values using central function
    if "remote-auth" in payload:
        is_valid, error = _validate_enum_field(
            "remote-auth",
            payload["remote-auth"],
            VALID_BODY_REMOTE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wildcard" in payload:
        is_valid, error = _validate_enum_field(
            "wildcard",
            payload["wildcard"],
            VALID_BODY_WILDCARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-auth" in payload:
        is_valid, error = _validate_enum_field(
            "peer-auth",
            payload["peer-auth"],
            VALID_BODY_PEER_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-remove-admin-session" in payload:
        is_valid, error = _validate_enum_field(
            "allow-remove-admin-session",
            payload["allow-remove-admin-session"],
            VALID_BODY_ALLOW_REMOVE_ADMIN_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "accprofile-override" in payload:
        is_valid, error = _validate_enum_field(
            "accprofile-override",
            payload["accprofile-override"],
            VALID_BODY_ACCPROFILE_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vdom-override" in payload:
        is_valid, error = _validate_enum_field(
            "vdom-override",
            payload["vdom-override"],
            VALID_BODY_VDOM_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "force-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "force-password-change",
            payload["force-password-change"],
            VALID_BODY_FORCE_PASSWORD_CHANGE,
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
    if "guest-auth" in payload:
        is_valid, error = _validate_enum_field(
            "guest-auth",
            payload["guest-auth"],
            VALID_BODY_GUEST_AUTH,
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
    "endpoint": "system/admin",
    "category": "cmdb",
    "api_path": "system/admin",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure admin users.",
    "total_fields": 53,
    "required_fields_count": 3,
    "fields_with_defaults_count": 47,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
