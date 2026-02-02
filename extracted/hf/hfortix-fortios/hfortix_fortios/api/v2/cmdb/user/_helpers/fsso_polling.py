"""Validation helpers for user/fsso_polling - Auto-generated"""

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
    "server",  # Host name or IP address of the Active Directory server.
    "user",  # User name required to log into this Active Directory server.
    "ldap-server",  # LDAP server name used in LDAP connection strings.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "status": "enable",
    "server": "",
    "default-domain": "",
    "port": 0,
    "user": "",
    "ldap-server": "",
    "logon-history": 8,
    "polling-frequency": 10,
    "smbv1": "disable",
    "smb-ntlmv1-auth": "disable",
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
    "id": "integer",  # Active Directory server ID.
    "status": "option",  # Enable/disable polling for the status of this Active Directo
    "server": "string",  # Host name or IP address of the Active Directory server.
    "default-domain": "string",  # Default domain managed by this Active Directory server.
    "port": "integer",  # Port to communicate with this Active Directory server.
    "user": "string",  # User name required to log into this Active Directory server.
    "password": "password",  # Password required to log into this Active Directory server.
    "ldap-server": "string",  # LDAP server name used in LDAP connection strings.
    "logon-history": "integer",  # Number of hours of logon history to keep, 0 means keep all h
    "polling-frequency": "integer",  # Polling frequency (every 1 to 30 seconds).
    "adgrp": "string",  # LDAP Group Info.
    "smbv1": "option",  # Enable/disable support of SMBv1 for Samba.
    "smb-ntlmv1-auth": "option",  # Enable/disable support of NTLMv1 for Samba authentication.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "Active Directory server ID.",
    "status": "Enable/disable polling for the status of this Active Directory server.",
    "server": "Host name or IP address of the Active Directory server.",
    "default-domain": "Default domain managed by this Active Directory server.",
    "port": "Port to communicate with this Active Directory server.",
    "user": "User name required to log into this Active Directory server.",
    "password": "Password required to log into this Active Directory server.",
    "ldap-server": "LDAP server name used in LDAP connection strings.",
    "logon-history": "Number of hours of logon history to keep, 0 means keep all history.",
    "polling-frequency": "Polling frequency (every 1 to 30 seconds).",
    "adgrp": "LDAP Group Info.",
    "smbv1": "Enable/disable support of SMBv1 for Samba.",
    "smb-ntlmv1-auth": "Enable/disable support of NTLMv1 for Samba authentication.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "server": {"type": "string", "max_length": 63},
    "default-domain": {"type": "string", "max_length": 35},
    "port": {"type": "integer", "min": 0, "max": 65535},
    "user": {"type": "string", "max_length": 35},
    "ldap-server": {"type": "string", "max_length": 35},
    "logon-history": {"type": "integer", "min": 0, "max": 48},
    "polling-frequency": {"type": "integer", "min": 1, "max": 30},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "adgrp": {
        "name": {
            "type": "string",
            "help": "Name.",
            "required": True,
            "default": "",
            "max_length": 511,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SMBV1 = [
    "enable",
    "disable",
]
VALID_BODY_SMB_NTLMV1_AUTH = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_fsso_polling_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/fsso_polling."""
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


def validate_user_fsso_polling_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/fsso_polling object."""
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
    if "smbv1" in payload:
        is_valid, error = _validate_enum_field(
            "smbv1",
            payload["smbv1"],
            VALID_BODY_SMBV1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "smb-ntlmv1-auth" in payload:
        is_valid, error = _validate_enum_field(
            "smb-ntlmv1-auth",
            payload["smb-ntlmv1-auth"],
            VALID_BODY_SMB_NTLMV1_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_fsso_polling_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/fsso_polling."""
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
    if "smbv1" in payload:
        is_valid, error = _validate_enum_field(
            "smbv1",
            payload["smbv1"],
            VALID_BODY_SMBV1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "smb-ntlmv1-auth" in payload:
        is_valid, error = _validate_enum_field(
            "smb-ntlmv1-auth",
            payload["smb-ntlmv1-auth"],
            VALID_BODY_SMB_NTLMV1_AUTH,
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
    "endpoint": "user/fsso_polling",
    "category": "cmdb",
    "api_path": "user/fsso-polling",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Configure FSSO active directory servers for polling mode.",
    "total_fields": 13,
    "required_fields_count": 3,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
