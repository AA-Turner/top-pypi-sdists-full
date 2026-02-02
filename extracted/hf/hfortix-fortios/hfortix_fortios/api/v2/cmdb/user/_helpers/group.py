"""Validation helpers for user/group - Auto-generated"""

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
    "id": 0,
    "group-type": "firewall",
    "authtimeout": 0,
    "auth-concurrent-override": "disable",
    "auth-concurrent-value": 0,
    "http-digest-realm": "",
    "sso-attribute-value": "",
    "user-id": "email",
    "password": "auto-generate",
    "user-name": "disable",
    "sponsor": "optional",
    "company": "optional",
    "email": "enable",
    "mobile-phone": "disable",
    "sms-server": "fortiguard",
    "sms-custom-server": "",
    "expire-type": "immediately",
    "expire": 14400,
    "max-accounts": 0,
    "multiple-guest-add": "disable",
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
    "name": "string",  # Group name.
    "id": "integer",  # Group ID.
    "group-type": "option",  # Set the group to be for firewall authentication, FSSO, RSSO,
    "authtimeout": "integer",  # Authentication timeout in minutes for this user group. 0 to 
    "auth-concurrent-override": "option",  # Enable/disable overriding the global number of concurrent au
    "auth-concurrent-value": "integer",  # Maximum number of concurrent authenticated connections per u
    "http-digest-realm": "string",  # Realm attribute for MD5-digest authentication.
    "sso-attribute-value": "string",  # RADIUS attribute value.
    "member": "string",  # Names of users, peers, LDAP severs, RADIUS servers or extern
    "match": "string",  # Group matches.
    "user-id": "option",  # Guest user ID type.
    "password": "option",  # Guest user password type.
    "user-name": "option",  # Enable/disable the guest user name entry.
    "sponsor": "option",  # Set the action for the sponsor guest user field.
    "company": "option",  # Set the action for the company guest user field.
    "email": "option",  # Enable/disable the guest user email address field.
    "mobile-phone": "option",  # Enable/disable the guest user mobile phone number field.
    "sms-server": "option",  # Send SMS through FortiGuard or other external server.
    "sms-custom-server": "string",  # SMS server.
    "expire-type": "option",  # Determine when the expiration countdown begins.
    "expire": "integer",  # Time in seconds before guest user accounts expire (1 - 31536
    "max-accounts": "integer",  # Maximum number of guest accounts that can be created for thi
    "multiple-guest-add": "option",  # Enable/disable addition of multiple guests.
    "guest": "string",  # Guest User.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Group name.",
    "id": "Group ID.",
    "group-type": "Set the group to be for firewall authentication, FSSO, RSSO, or guest users.",
    "authtimeout": "Authentication timeout in minutes for this user group. 0 to use the global user setting auth-timeout.",
    "auth-concurrent-override": "Enable/disable overriding the global number of concurrent authentication sessions for this user group.",
    "auth-concurrent-value": "Maximum number of concurrent authenticated connections per user (0 - 100).",
    "http-digest-realm": "Realm attribute for MD5-digest authentication.",
    "sso-attribute-value": "RADIUS attribute value.",
    "member": "Names of users, peers, LDAP severs, RADIUS servers or external idp servers to add to the user group.",
    "match": "Group matches.",
    "user-id": "Guest user ID type.",
    "password": "Guest user password type.",
    "user-name": "Enable/disable the guest user name entry.",
    "sponsor": "Set the action for the sponsor guest user field.",
    "company": "Set the action for the company guest user field.",
    "email": "Enable/disable the guest user email address field.",
    "mobile-phone": "Enable/disable the guest user mobile phone number field.",
    "sms-server": "Send SMS through FortiGuard or other external server.",
    "sms-custom-server": "SMS server.",
    "expire-type": "Determine when the expiration countdown begins.",
    "expire": "Time in seconds before guest user accounts expire (1 - 31536000).",
    "max-accounts": "Maximum number of guest accounts that can be created for this group (0 means unlimited).",
    "multiple-guest-add": "Enable/disable addition of multiple guests.",
    "guest": "Guest User.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "authtimeout": {"type": "integer", "min": 0, "max": 43200},
    "auth-concurrent-value": {"type": "integer", "min": 0, "max": 100},
    "http-digest-realm": {"type": "string", "max_length": 35},
    "sso-attribute-value": {"type": "string", "max_length": 511},
    "sms-custom-server": {"type": "string", "max_length": 35},
    "expire": {"type": "integer", "min": 1, "max": 31536000},
    "max-accounts": {"type": "integer", "min": 0, "max": 500},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "member": {
        "name": {
            "type": "string",
            "help": "Group member name.",
            "required": True,
            "default": "",
            "max_length": 511,
        },
    },
    "match": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "server-name": {
            "type": "string",
            "help": "Name of remote auth server.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "group-name": {
            "type": "string",
            "help": "Name of matching user or group on remote authentication server or SCIM.",
            "required": True,
            "default": "",
            "max_length": 511,
        },
    },
    "guest": {
        "id": {
            "type": "integer",
            "help": "Guest ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "user-id": {
            "type": "string",
            "help": "Guest ID.",
            "default": "",
            "max_length": 64,
        },
        "name": {
            "type": "string",
            "help": "Guest name.",
            "default": "",
            "max_length": 64,
        },
        "password": {
            "type": "password",
            "help": "Guest password.",
            "max_length": 128,
        },
        "mobile-phone": {
            "type": "string",
            "help": "Mobile phone.",
            "default": "",
            "max_length": 35,
        },
        "sponsor": {
            "type": "string",
            "help": "Set the action for the sponsor guest user field.",
            "default": "",
            "max_length": 35,
        },
        "company": {
            "type": "string",
            "help": "Set the action for the company guest user field.",
            "default": "",
            "max_length": 35,
        },
        "email": {
            "type": "string",
            "help": "Email.",
            "default": "",
            "max_length": 64,
        },
        "expiration": {
            "type": "user",
            "help": "Expire time.",
            "default": "",
        },
        "comment": {
            "type": "var-string",
            "help": "Comment.",
            "max_length": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_GROUP_TYPE = [
    "firewall",
    "fsso-service",
    "rsso",
    "guest",
]
VALID_BODY_AUTH_CONCURRENT_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_USER_ID = [
    "email",
    "auto-generate",
    "specify",
]
VALID_BODY_PASSWORD = [
    "auto-generate",
    "specify",
    "disable",
]
VALID_BODY_USER_NAME = [
    "disable",
    "enable",
]
VALID_BODY_SPONSOR = [
    "optional",
    "mandatory",
    "disabled",
]
VALID_BODY_COMPANY = [
    "optional",
    "mandatory",
    "disabled",
]
VALID_BODY_EMAIL = [
    "disable",
    "enable",
]
VALID_BODY_MOBILE_PHONE = [
    "disable",
    "enable",
]
VALID_BODY_SMS_SERVER = [
    "fortiguard",
    "custom",
]
VALID_BODY_EXPIRE_TYPE = [
    "immediately",
    "first-successful-login",
]
VALID_BODY_MULTIPLE_GUEST_ADD = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_group_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/group."""
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


def validate_user_group_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/group object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "group-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-type",
            payload["group-type"],
            VALID_BODY_GROUP_TYPE,
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
    if "user-id" in payload:
        is_valid, error = _validate_enum_field(
            "user-id",
            payload["user-id"],
            VALID_BODY_USER_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password" in payload:
        is_valid, error = _validate_enum_field(
            "password",
            payload["password"],
            VALID_BODY_PASSWORD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-name" in payload:
        is_valid, error = _validate_enum_field(
            "user-name",
            payload["user-name"],
            VALID_BODY_USER_NAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sponsor" in payload:
        is_valid, error = _validate_enum_field(
            "sponsor",
            payload["sponsor"],
            VALID_BODY_SPONSOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "company" in payload:
        is_valid, error = _validate_enum_field(
            "company",
            payload["company"],
            VALID_BODY_COMPANY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email" in payload:
        is_valid, error = _validate_enum_field(
            "email",
            payload["email"],
            VALID_BODY_EMAIL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mobile-phone" in payload:
        is_valid, error = _validate_enum_field(
            "mobile-phone",
            payload["mobile-phone"],
            VALID_BODY_MOBILE_PHONE,
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
    if "expire-type" in payload:
        is_valid, error = _validate_enum_field(
            "expire-type",
            payload["expire-type"],
            VALID_BODY_EXPIRE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multiple-guest-add" in payload:
        is_valid, error = _validate_enum_field(
            "multiple-guest-add",
            payload["multiple-guest-add"],
            VALID_BODY_MULTIPLE_GUEST_ADD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_group_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/group."""
    # Validate enum values using central function
    if "group-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-type",
            payload["group-type"],
            VALID_BODY_GROUP_TYPE,
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
    if "user-id" in payload:
        is_valid, error = _validate_enum_field(
            "user-id",
            payload["user-id"],
            VALID_BODY_USER_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "password" in payload:
        is_valid, error = _validate_enum_field(
            "password",
            payload["password"],
            VALID_BODY_PASSWORD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-name" in payload:
        is_valid, error = _validate_enum_field(
            "user-name",
            payload["user-name"],
            VALID_BODY_USER_NAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sponsor" in payload:
        is_valid, error = _validate_enum_field(
            "sponsor",
            payload["sponsor"],
            VALID_BODY_SPONSOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "company" in payload:
        is_valid, error = _validate_enum_field(
            "company",
            payload["company"],
            VALID_BODY_COMPANY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email" in payload:
        is_valid, error = _validate_enum_field(
            "email",
            payload["email"],
            VALID_BODY_EMAIL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mobile-phone" in payload:
        is_valid, error = _validate_enum_field(
            "mobile-phone",
            payload["mobile-phone"],
            VALID_BODY_MOBILE_PHONE,
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
    if "expire-type" in payload:
        is_valid, error = _validate_enum_field(
            "expire-type",
            payload["expire-type"],
            VALID_BODY_EXPIRE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multiple-guest-add" in payload:
        is_valid, error = _validate_enum_field(
            "multiple-guest-add",
            payload["multiple-guest-add"],
            VALID_BODY_MULTIPLE_GUEST_ADD,
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
    "endpoint": "user/group",
    "category": "cmdb",
    "api_path": "user/group",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure user groups.",
    "total_fields": 24,
    "required_fields_count": 0,
    "fields_with_defaults_count": 21,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
