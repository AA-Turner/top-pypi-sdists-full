"""Validation helpers for system/ssh_config - Auto-generated"""

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
    "ssh-hsk",  # Config SSH host key.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "ssh-kex-algo": "diffie-hellman-group14-sha256 diffie-hellman-group16-sha512 diffie-hellman-group18-sha512 diffie-hellman-group-exchange-sha256 curve25519-sha256@libssh.org ecdh-sha2-nistp256 ecdh-sha2-nistp384 ecdh-sha2-nistp521",
    "ssh-enc-algo": "aes256-ctr aes256-gcm@openssh.com",
    "ssh-mac-algo": "hmac-sha2-256 hmac-sha2-256-etm@openssh.com hmac-sha2-512 hmac-sha2-512-etm@openssh.com",
    "ssh-hsk-algo": "ecdsa-sha2-nistp521 ecdsa-sha2-nistp384 ecdsa-sha2-nistp256 rsa-sha2-256 rsa-sha2-512 ssh-ed25519",
    "ssh-hsk-override": "disable",
    "ssh-hsk": "",
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
    "ssh-kex-algo": "option",  # Select one or more SSH kex algorithms.
    "ssh-enc-algo": "option",  # Select one or more SSH ciphers.
    "ssh-mac-algo": "option",  # Select one or more SSH MAC algorithms.
    "ssh-hsk-algo": "option",  # Select one or more SSH hostkey algorithms.
    "ssh-hsk-override": "option",  # Enable/disable SSH host key override in SSH daemon.
    "ssh-hsk-password": "password",  # Password for ssh-hostkey.
    "ssh-hsk": "user",  # Config SSH host key.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "ssh-kex-algo": "Select one or more SSH kex algorithms.",
    "ssh-enc-algo": "Select one or more SSH ciphers.",
    "ssh-mac-algo": "Select one or more SSH MAC algorithms.",
    "ssh-hsk-algo": "Select one or more SSH hostkey algorithms.",
    "ssh-hsk-override": "Enable/disable SSH host key override in SSH daemon.",
    "ssh-hsk-password": "Password for ssh-hostkey.",
    "ssh-hsk": "Config SSH host key.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_SSH_KEX_ALGO = [
    "diffie-hellman-group1-sha1",
    "diffie-hellman-group14-sha1",
    "diffie-hellman-group14-sha256",
    "diffie-hellman-group16-sha512",
    "diffie-hellman-group18-sha512",
    "diffie-hellman-group-exchange-sha1",
    "diffie-hellman-group-exchange-sha256",
    "curve25519-sha256@libssh.org",
    "ecdh-sha2-nistp256",
    "ecdh-sha2-nistp384",
    "ecdh-sha2-nistp521",
]
VALID_BODY_SSH_ENC_ALGO = [
    "chacha20-poly1305@openssh.com",
    "aes128-ctr",
    "aes192-ctr",
    "aes256-ctr",
    "arcfour256",
    "arcfour128",
    "aes128-cbc",
    "3des-cbc",
    "blowfish-cbc",
    "cast128-cbc",
    "aes192-cbc",
    "aes256-cbc",
    "arcfour",
    "rijndael-cbc@lysator.liu.se",
    "aes128-gcm@openssh.com",
    "aes256-gcm@openssh.com",
]
VALID_BODY_SSH_MAC_ALGO = [
    "hmac-md5",
    "hmac-md5-etm@openssh.com",
    "hmac-md5-96",
    "hmac-md5-96-etm@openssh.com",
    "hmac-sha1",
    "hmac-sha1-etm@openssh.com",
    "hmac-sha2-256",
    "hmac-sha2-256-etm@openssh.com",
    "hmac-sha2-512",
    "hmac-sha2-512-etm@openssh.com",
    "hmac-ripemd160",
    "hmac-ripemd160@openssh.com",
    "hmac-ripemd160-etm@openssh.com",
    "umac-64@openssh.com",
    "umac-128@openssh.com",
    "umac-64-etm@openssh.com",
    "umac-128-etm@openssh.com",
]
VALID_BODY_SSH_HSK_ALGO = [
    "ssh-rsa",
    "ecdsa-sha2-nistp521",
    "ecdsa-sha2-nistp384",
    "ecdsa-sha2-nistp256",
    "rsa-sha2-256",
    "rsa-sha2-512",
    "ssh-ed25519",
]
VALID_BODY_SSH_HSK_OVERRIDE = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_ssh_config_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/ssh_config."""
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


def validate_system_ssh_config_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/ssh_config object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ssh-kex-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-kex-algo",
            payload["ssh-kex-algo"],
            VALID_BODY_SSH_KEX_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-enc-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-enc-algo",
            payload["ssh-enc-algo"],
            VALID_BODY_SSH_ENC_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-mac-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-mac-algo",
            payload["ssh-mac-algo"],
            VALID_BODY_SSH_MAC_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-hsk-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-hsk-algo",
            payload["ssh-hsk-algo"],
            VALID_BODY_SSH_HSK_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-hsk-override" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-hsk-override",
            payload["ssh-hsk-override"],
            VALID_BODY_SSH_HSK_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_ssh_config_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/ssh_config."""
    # Validate enum values using central function
    if "ssh-kex-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-kex-algo",
            payload["ssh-kex-algo"],
            VALID_BODY_SSH_KEX_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-enc-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-enc-algo",
            payload["ssh-enc-algo"],
            VALID_BODY_SSH_ENC_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-mac-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-mac-algo",
            payload["ssh-mac-algo"],
            VALID_BODY_SSH_MAC_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-hsk-algo" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-hsk-algo",
            payload["ssh-hsk-algo"],
            VALID_BODY_SSH_HSK_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-hsk-override" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-hsk-override",
            payload["ssh-hsk-override"],
            VALID_BODY_SSH_HSK_OVERRIDE,
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
    "endpoint": "system/ssh_config",
    "category": "cmdb",
    "api_path": "system/ssh-config",
    "help": "Configure SSH config.",
    "total_fields": 7,
    "required_fields_count": 1,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
